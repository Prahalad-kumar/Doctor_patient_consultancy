from django.db import models
from django.utils import timezone

class Doctor(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50)
    years_of_experience = models.PositiveIntegerField()
    qualification = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15,default='Not Provided')
    address = models.CharField(max_length=200,default='Unknown Address')
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"
