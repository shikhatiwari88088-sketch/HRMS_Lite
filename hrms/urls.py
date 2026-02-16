from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import EmployeeViewSet, AttendanceViewSet, dashboard_stats

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'attendance', AttendanceViewSet)

urlpatterns = router.urls + [
    path('dashboard/', dashboard_stats),
]
