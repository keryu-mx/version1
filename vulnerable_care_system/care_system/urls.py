
from django.urls import path, include
from .views import (
    SubjectViewSet,
    CustodianViewSet,
    AlarmViewSet,
    generate_qr_code_api,
    get_qr_code_api,  # Ensure this is imported
    trigger_alarm_via_qr_code_api,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'custodians', CustodianViewSet)
router.register(r'alarms', AlarmViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate-qr-code/', generate_qr_code_api, name='generate_qr_code'),
    path('get-qr-code/<int:subject_id>/', get_qr_code_api, name='get_qr_code'),  # Ensure this is included
    path('trigger-alarm-via-qr-code/', trigger_alarm_via_qr_code_api, name='trigger_alarm_via_qr_code'),
]