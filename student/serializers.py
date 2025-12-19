from rest_framework import serializers
from .models import (
    Student, Course, Enrollment, Attendance, 
    Assignment, Submission, Notification, Announcement
)

class StudentSerializer(serializers.ModelSerializer):
    attendance_percentage = serializers.SerializerMethodField()
    enrolled_courses_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = '__all__'
    
    def get_attendance_percentage(self, obj):
        return obj.get_attendance_percentage()
    
    def get_enrolled_courses_count(self, obj):
        return obj.enrollments.filter(is_active=True).count()


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    enrolled_students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = '__all__'
    
    def get_enrolled_students_count(self, obj):
        return obj.get_enrolled_students_count()


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = '__all__'
    
    def get_is_overdue(self, obj):
        return obj.is_overdue()


class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    is_late = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = '__all__'
    
    def get_is_late(self, obj):
        return obj.is_late()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class AnnouncementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = '__all__'
    
    def get_is_expired(self, obj):
        return obj.is_expired()
