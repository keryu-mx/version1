from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    medical_conditions = models.TextField(blank=True, null=True)
    hospital = models.CharField(max_length=100, blank=True, null=True)
    doctor_name = models.CharField(max_length=100, blank=True, null=True)
    doctor_contact = models.CharField(max_length=20, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return self.name

class Custodian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20)
    subjects = models.ManyToManyField(Subject, related_name='custodians')

    def __str__(self):
        return self.user.username

class Alarm(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='alarms')
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Alarm for {self.subject.name} at {self.timestamp}"