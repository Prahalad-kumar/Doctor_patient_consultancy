# doctor/views.py
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from .models import Doctor

# -----------------------------
# SIGNUP
# -----------------------------
def create_account(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        specialty = request.POST.get('specialty')
        experience_years = request.POST.get('experience_years')
        qualification = request.POST.get('qualification')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('office_address')
        bio = request.POST.get('bio')

        # check password confirmation
        if request.POST.get('password') != request.POST.get('confirm_password'):
            return render(request, 'doctor_signup.html', {
                'error': "Passwords do not match!"
            })

        # duplicate email
        if Doctor.objects.filter(email=email).exists():
            return render(request, 'doctor_signup.html', {
                'error': "Email already exists!"
            })

        # sanitize/convert experience_years
        try:
            exp = int(experience_years) if experience_years else 0
        except ValueError:
            exp = 0

        doctor = Doctor(
            fname=fname,
            lname=lname,
            email=email,
            password=make_password(password),
            specialization=specialty,
            years_of_experience=exp,
            qualification=qualification,
            contact_number=contact_number,
            address=address,
            bio=bio
        )
        doctor.save()

        return render(request, 'doctor_login.html', {
            'success': "Account created successfully! Please login."
        })

    return render(request, 'doctor_signup.html')


# -----------------------------
# LOGIN
# -----------------------------
def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            doctor = Doctor.objects.get(email=email)
        except Doctor.DoesNotExist:
            return render(request, 'doctor_login.html', {
                'error': "Email not registered!"
            })

        if not check_password(password, doctor.password):
            return render(request, 'doctor_login.html', {
                'error': "Incorrect password!"
            })

        # login success
        request.session['doctor_id'] = doctor.id
        return redirect('doctor_dashboard')

    return render(request, 'doctor_login.html')


# -----------------------------
# LOGOUT
# -----------------------------
def doctor_logout(request):
    request.session.flush()
    return redirect('home')


# -----------------------------
# DASHBOARD
# -----------------------------
from apponiment.models import Appointment
from datetime import datetime, timedelta

def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')

    doctor = get_object_or_404(Doctor, id=doctor_id)

    today = date.today()
    # Today's appointments
    todays_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=today
    ).order_by('appointment_time')

    # Weekly count (Mon-Sun)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    weekly_count = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__range=[start_of_week, end_of_week]
    ).count()

    context = {
        'doctor': doctor,
        'todays_appointments': todays_appointments,
        'todays_count': todays_appointments.count(),
        'weekly_count': weekly_count,
    }
    return render(request, 'doctor_dashboard.html', context)


# -----------------------------
# PROFILE
# -----------------------------
def doctor_profile(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')

    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor_profile.html', {"doctor": doctor})


# -----------------------------
# UPDATE PROFILE
# -----------------------------
def doctor_update_profile(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')

    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        # Use correct field names from model
        doctor.contact_number = request.POST.get('contact_number')
        doctor.specialization = request.POST.get('specialty')
        try:
            doctor.years_of_experience = int(request.POST.get('experience_years') or 0)
        except ValueError:
            doctor.years_of_experience = 0
        doctor.qualification = request.POST.get('qualification')
        doctor.address = request.POST.get('office_address')
        doctor.bio = request.POST.get('bio')
        doctor.save()

        return render(request, 'doctor_update_profile.html', {
            'doctor': doctor,
            'success': "Profile updated successfully!"
        })

    return render(request, 'doctor_update_profile.html', {'doctor': doctor})


# -----------------------------
# SCHEDULE (list all appointments)
# -----------------------------
def doctor_schedule(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')

    doctor = get_object_or_404(Doctor, id=doctor_id)

    # optional filter by date passed via GET ?date=YYYY-MM-DD
    date_str = request.GET.get('date')
    appointments = Appointment.objects.filter(doctor=doctor).order_by('appointment_date', 'appointment_time')
    if date_str:
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
            appointments = appointments.filter(appointment_date=d)
        except:
            pass

    return render(request, 'doctor_schedule.html', {
        "doctor": doctor,
        "appointments": appointments
    })


# -----------------------------
# CHANGE PASSWORD
# -----------------------------
def doctor_change_password(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')

    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new = request.POST.get('confirm_new_password')

        if new_password != confirm_new:
            return render(request, 'doctor_change_password.html', {'doctor': doctor, 'error': "New passwords do not match."})

        if check_password(current_password, doctor.password):
            doctor.password = make_password(new_password)
            doctor.save()
            messages.success(request, "Password changed successfully.")
            return redirect('doctor_profile')
        else:
            messages.error(request, "Current password is incorrect.")

    return render(request, 'doctor_change_password.html', {'doctor': doctor})
