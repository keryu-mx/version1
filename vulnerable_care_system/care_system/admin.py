from django.contrib import admin
from .models import Subject, Custodian, Alarm

# Register the Subject model
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'hospital', 'doctor_name', 'doctor_contact')
    search_fields = ('name', 'hospital', 'doctor_name')
    list_filter = ('hospital',)

# Register the Custodian model
@admin.register(Custodian)
class CustodianAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'whatsapp_number')
    search_fields = ('user__username', 'phone_number', 'whatsapp_number')
    filter_horizontal = ('subjects',)  # For easier management of ManyToMany relationships

# Register the Alarm model
@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display = ('subject', 'timestamp', 'resolved')
    list_filter = ('resolved', 'timestamp')
    search_fields = ('subject__name',)