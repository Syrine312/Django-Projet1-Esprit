from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from AccountApp.models import Doctor, Patient


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        CONFIRMED = 'confirmed', 'Confirmé'
        CANCELLED = 'cancelled', 'Annulé'

    reason = models.TextField(max_length=255)
    prescription = models.FileField(upload_to='prescriptions/', blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    doctor = models.ForeignKey(
        "AccountApp.Doctor", on_delete=models.CASCADE
    )
    patient = models.ForeignKey(
        "AccountApp.Patient", on_delete=models.CASCADE
    )

    def clean(self):
        super().clean()
        modified_date = self._state.adding or (
            not Appointment.objects.filter(
                pk=self.pk,
                appointment_date=self.appointment_date,
            ).exists()
        )
        if self.appointment_date and modified_date and (
            self.appointment_date <= timezone.now()
        ):
            raise ValidationError("Appointment date cannot be in the past.")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment'
            )
        ]
        ordering = ['appointment_date']

