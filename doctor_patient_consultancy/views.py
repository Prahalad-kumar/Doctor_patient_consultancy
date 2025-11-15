from django.shortcuts import render, redirect
from doctor.models import Doctor
from doctor.views import *
from patient.views import *
def home(request):
    return render(request, 'home.html')

def patient(request):
    return redirect(request,'patient_login')

def doctor(request):
    return redirect(request,'doctor_login')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
