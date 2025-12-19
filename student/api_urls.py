from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'students', api_views.StudentViewSet)
router.register(r'courses', api_views.CourseViewSet)
router.register(r'enrollments', api_views.EnrollmentViewSet)
router.register(r'attendance', api_views.AttendanceViewSet)
router.register(r'assignments', api_views.AssignmentViewSet)
router.register(r'submissions', api_views.SubmissionViewSet)
router.register(r'notifications', api_views.NotificationViewSet)
router.register(r'announcements', api_views.AnnouncementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', api_views.stats_api, name='api_stats'),
]
