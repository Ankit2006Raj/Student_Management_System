from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Avg

class Student(models.Model):
    GRADE_CHOICES = [
        ('A', 'A Grade (90-100)'),
        ('B', 'B Grade (80-89)'),
        ('C', 'C Grade (70-79)'),
        ('D', 'D Grade (60-69)'),
        ('F', 'F Grade (0-59)'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    # User Account (Optional - for student portal access)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='student_profile')
    
    # Basic Information
    name = models.CharField(max_length=100)
    roll_number = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    
    # Address Information
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, default='India')
    
    # Guardian Information
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)
    guardian_relation = models.CharField(max_length=50, blank=True, null=True)
    
    # Academic Information
    marks = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Enter marks between 0 and 100"
    )
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True)
    admission_date = models.DateField(default=timezone.now)
    class_name = models.CharField(max_length=50, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True, help_text="Internal notes about the student")

    def __str__(self):
        return f"{self.name} ({self.roll_number})"
    
    def save(self, *args, **kwargs):
        # Auto-calculate grade based on marks
        if self.marks >= 90:
            self.grade = 'A'
        elif self.marks >= 80:
            self.grade = 'B'
        elif self.marks >= 70:
            self.grade = 'C'
        elif self.marks >= 60:
            self.grade = 'D'
        else:
            self.grade = 'F'
        super().save(*args, **kwargs)
    
    def get_grade_display_full(self):
        grade_map = {
            'A': 'Excellent',
            'B': 'Very Good',
            'C': 'Good',
            'D': 'Average',
            'F': 'Fail'
        }
        return grade_map.get(self.grade, 'N/A')
    
    def get_attendance_percentage(self):
        """Calculate attendance percentage"""
        total = Attendance.objects.filter(student=self).count()
        if total == 0:
            return 0
        present = Attendance.objects.filter(student=self, status='P').count()
        return round((present / total) * 100, 2)
    
    def get_enrolled_courses(self):
        """Get all courses the student is enrolled in"""
        return self.enrollments.filter(is_active=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['roll_number']),
            models.Index(fields=['email']),
            models.Index(fields=['grade']),
            models.Index(fields=['class_name']),
        ]


class Course(models.Model):
    """Course/Subject Model"""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField(default=3)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_taught')
    semester = models.CharField(max_length=50, blank=True, null=True)
    academic_year = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_enrolled_students_count(self):
        return self.enrollments.filter(is_active=True).count()
    
    class Meta:
        ordering = ['code']


class Enrollment(models.Model):
    """Student Course Enrollment"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    final_grade = models.CharField(max_length=2, blank=True, null=True)
    final_marks = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.student.name} - {self.course.code}"


class Attendance(models.Model):
    """Daily Attendance Tracking"""
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances', null=True, blank=True)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    remarks = models.TextField(blank=True, null=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.get_status_display()}"


class Assignment(models.Model):
    """Assignments for courses"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    total_marks = models.IntegerField(default=100)
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"
    
    def is_overdue(self):
        return timezone.now() > self.due_date
    
    class Meta:
        ordering = ['-due_date']


class Submission(models.Model):
    """Student Assignment Submissions"""
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submission_file = models.FileField(upload_to='submissions/')
    submission_text = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)
    marks_obtained = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    feedback = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student.name} - {self.assignment.title}"
    
    def is_late(self):
        return self.submitted_at > self.assignment.due_date


class Notification(models.Model):
    """Notification System"""
    NOTIFICATION_TYPES = [
        ('INFO', 'Information'),
        ('SUCCESS', 'Success'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('ASSIGNMENT', 'Assignment'),
        ('GRADE', 'Grade'),
        ('ATTENDANCE', 'Attendance'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='INFO')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Announcement(models.Model):
    """School-wide or class-specific announcements"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    target_class = models.CharField(max_length=50, blank=True, null=True, help_text="Leave blank for all students")
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0, help_text="Higher number = higher priority")
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return self.title
    
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
