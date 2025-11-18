# doctor_patient_consultancy/views.py
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'index.html')

def patient(request):
    return redirect('patient_login')

def doctor(request):
    return redirect('doctor_login')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
