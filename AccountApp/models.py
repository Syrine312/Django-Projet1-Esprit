from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accountapp_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accountapp_user_set',
        blank=True,
    )

class Speciality(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
phone_validator = RegexValidator(
regex=r"^\d{8}$",
message="Le téléphone doit contenir 8 chiffres."
)

class Doctor(User):
    license_number = models.CharField(
    max_length=6, unique=True,
    validators=[MinLengthValidator(6)]
    )
    phone_number=models.CharField(max_length=15, validators=[phone_validator])
    specialities = models.ManyToManyField(Speciality, related_name='doctors')
    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

def validate_past_date(value):
    if value > timezone.now().date():
        raise ValidationError("La date de naissance ne peut pas être dans le futur.")
class Patient(User):
    national_id=models.CharField(max_length=8, unique=True, validators=[RegexValidator(
    r"^\d{8}$", message="La CIN doit contenir 8 chiffres."
    )])
    phone=models.CharField(max_length=15, validators=[phone_validator])
    birth_date=models.DateField(validators=[validate_past_date])
    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'