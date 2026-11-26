from django.contrib import admin
from .models import Appointment

class AppointmentAdminPerso(admin.ModelAdmin):
    list_display = (
        'id', 'reason', 'status',
        'duration_minutes', 'appointment_date',
        'doctor', 'patient',
    )
    list_filter = ('status', 'appointment_date')
    list_editable = ('status',)
    search_fields = ('doctor__username',)
admin.site.register(Appointment, AppointmentAdminPerso)

