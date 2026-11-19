from django.db import models
from AccountApp.models import Doctor, Patient

class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        CONFIRMED = 'confirmed', 'confirme'
        CANCELLED = 'cancelled', 'Annule'
    reason = models.TextField(max_length=255)
    prescription=models.FileField(upload_to='prescriptions/', blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    doctor = models.ForeignKey(
"AccountApp.Doctor", on_delete=models.CASCADE #ki yemchi l doctor yetsaf5 l appointment m3ah, yetsaf7 l appointment m3ah
)
patient = models.ForeignKey(
"AccountApp.Patient", on_delete=models.CASCADE
)
