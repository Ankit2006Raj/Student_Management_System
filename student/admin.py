from django.contrib import admin
from .models import (
    Student, Course, Enrollment, Attendance,
    Assignment, Submission, Notification, Announcement
)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_number', 'email', 'marks', 'grade', 'class_name', 'is_active']
    search_fields = ['name', 'roll_number', 'email']
    list_filter = ['grade', 'class_name', 'section', 'gender', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'roll_number', 'email', 'phone', 'date_of_birth', 'gender', 'photo')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Guardian Information', {
            'fields': ('guardian_name', 'guardian_phone', 'guardian_email', 'guardian_relation')
        }),
        ('Academic', {
            'fields': ('marks', 'grade', 'admission_date', 'class_name', 'section')
        }),
        ('Metadata', {
            'fields': ('is_active', 'notes', 'created_at', 'updated_at')
        }),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'teacher', 'credits', 'semester', 'is_active']
    search_fields = ['code', 'name']
    list_filter = ['semester', 'academic_year', 'is_active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date', 'final_grade', 'is_active']
    search_fields = ['student__name', 'course__name']
    list_filter = ['is_active', 'enrollment_date']
    autocomplete_fields = ['student', 'course']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date', 'status', 'marked_by']
    search_fields = ['student__name', 'course__name']
    list_filter = ['status', 'date']
    date_hierarchy = 'date'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'due_date', 'total_marks', 'created_by', 'is_active']
    search_fields = ['title', 'course__name']
    list_filter = ['course', 'due_date', 'is_active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'submitted_at', 'marks_obtained', 'graded_by']
    search_fields = ['student__name', 'assignment__title']
    list_filter = ['submitted_at', 'graded_at']
    readonly_fields = ['submitted_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    list_filter = ['notification_type', 'is_read', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'target_class', 'priority', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['is_active', 'priority', 'created_at']
    readonly_fields = ['created_at']
