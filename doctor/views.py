from django.shortcuts import render, redirect
from doctor.models import Doctor
from django.contrib.auth.hashers import make_password, check_password
from patient.views import *
from doctor_patient_consultancy.views import *
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
        contact_num = request.POST.get('contact_number')
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

        doctor = Doctor(
            fname=fname,
            lname=lname,
            email=email,
            password=make_password(password),
            specialization=specialty,
            years_of_experience=experience_years,
            qualification=qualification,
            contact_num=contact_num,
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
def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')

    doctor = Doctor.objects.get(id=doctor_id)

    return render(request, 'doctor_dashboard.html', {'doctor': doctor})



# -----------------------------
# PROFILE
# -----------------------------
def doctor_profile(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')

    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'doctor_profile.html', {"doctor": doctor})



# -----------------------------
# UPDATE PROFILE
# -----------------------------
def doctor_update_profile(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')

    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == 'POST':
        doctor.contact_num = request.POST.get('contact_number')
        doctor.specialization = request.POST.get('specialty')
        doctor.years_of_experience = request.POST.get('experience_years')
        doctor.qualification = request.POST.get('qualification')
        doctor.address = request.POST.get('office_address')
        doctor.bio = request.POST.get('bio')
        doctor.save()

        return render(request, 'doctor_update_profile.html', {
            'doctor': doctor,
            'success': "Profile updated successfully!"
        })

    return render(request, 'doctor_update_profile.html', {'doctor': doctor})

def doctor_schedule(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')

    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'doctor_schedule.html', {"doctor": doctor})

def doctor_change_password(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'doctor_change_password.html', {'doctor': doctor})
