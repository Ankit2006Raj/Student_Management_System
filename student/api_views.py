from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import (
    Student, Course, Enrollment, Attendance,
    Assignment, Submission, Notification, Announcement
)
from .serializers import (
    StudentSerializer, CourseSerializer, EnrollmentSerializer,
    AttendanceSerializer, AssignmentSerializer, SubmissionSerializer,
    NotificationSerializer, AnnouncementSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    """API endpoint for students"""
    queryset = Student.objects.filter(is_active=True)
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['grade', 'class_name', 'section', 'gender']
    search_fields = ['name', 'roll_number', 'email']
    ordering_fields = ['name', 'roll_number', 'marks', 'created_at']
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get attendance records for a student"""
        student = self.get_object()
        attendances = Attendance.objects.filter(student=student)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        """Get enrolled courses for a student"""
        student = self.get_object()
        enrollments = Enrollment.objects.filter(student=student, is_active=True)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    """API endpoint for courses"""
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['semester', 'academic_year']
    search_fields = ['code', 'name']
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get enrolled students for a course"""
        course = self.get_object()
        enrollments = Enrollment.objects.filter(course=course, is_active=True)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """API endpoint for enrollments"""
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'course', 'is_active']


class AttendanceViewSet(viewsets.ModelViewSet):
    """API endpoint for attendance"""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'course', 'status', 'date']
    ordering_fields = ['date']


class AssignmentViewSet(viewsets.ModelViewSet):
    """API endpoint for assignments"""
    queryset = Assignment.objects.filter(is_active=True)
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course']
    ordering_fields = ['due_date', 'created_at']


class SubmissionViewSet(viewsets.ModelViewSet):
    """API endpoint for submissions"""
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assignment', 'student']


class NotificationViewSet(viewsets.ModelViewSet):
    """API endpoint for notifications"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return notifications for the current user"""
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'success', 'message': 'All notifications marked as read'})


class AnnouncementViewSet(viewsets.ModelViewSet):
    """API endpoint for announcements"""
    queryset = Announcement.objects.filter(is_active=True)
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['priority', 'created_at']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stats_api(request):
    """Get dashboard statistics"""
    total_students = Student.objects.filter(is_active=True).count()
    total_courses = Course.objects.filter(is_active=True).count()
    average_marks = Student.objects.filter(is_active=True).aggregate(Avg('marks'))['marks__avg'] or 0
    
    # Grade distribution
    grade_distribution = Student.objects.filter(is_active=True).values('grade').annotate(count=Count('grade'))
    
    # Attendance stats
    total_attendance = Attendance.objects.count()
    present_count = Attendance.objects.filter(status='P').count()
    attendance_percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0
    
    return Response({
        'total_students': total_students,
        'total_courses': total_courses,
        'average_marks': round(average_marks, 2),
        'grade_distribution': list(grade_distribution),
        'attendance_percentage': round(attendance_percentage, 2),
    })
