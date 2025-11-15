from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Patient
from doctor.models import Doctor  # Assuming doctor app exists
from datetime import datetime,date
from django.contrib import messages
from doctor.models import Doctor  # Only doctor used
# ===============================
# 🧾 1️⃣ PATIENT SIGNUP
# ===============================
def patient_signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = make_password(request.POST.get('password'))
        blood_group = request.POST.get('blood_group')
        medical_history = request.POST.get('medical_history')

        # Validate duplicate email
        if Patient.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please log in.")
            return redirect('patient_login')

        # Convert DOB safely
        if date_of_birth:
            try:
                dob_parsed = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
                if dob_parsed > date.today():
                    messages.error(request, "Date of birth cannot be in the future.")
                    return redirect('patient_signup')  # or patient_update_profile
                date_of_birth = dob_parsed
            except ValueError:
                messages.error(request, "Invalid date format for Date of Birth.")
                return redirect('patient_signup')
        else:
            messages.error(request, "Please enter your date of birth.")
            return redirect('patient_signup')

        # Create patient
        Patient.objects.create(
            full_name=full_name,
            gender=gender,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            email=email,
            address=address,
            password=password,
            blood_group=blood_group,
            medical_history=medical_history
        )

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('patient_login')

    return render(request, 'patient/patient_signup.html',{'Today':date.today()})

# ===============================
# 🔐 2️⃣ LOGIN
# ===============================
def patient_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            patient = Patient.objects.get(email=email)
            if check_password(password, patient.password):
                request.session['patient_id'] = patient.id
                messages.success(request, f"Welcome back, {patient.full_name}!")
                return redirect('patient_dashboard')
            else:
                messages.error(request, 'Invalid password.')
        except Patient.DoesNotExist:
            messages.error(request, 'No account found with this email.')

    return render(request, 'patient/patient_login.html')

# ===============================
# 🏠 3️⃣ DASHBOARD
# ===============================
def patient_dashboard(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')

    patient = get_object_or_404(Patient, id=patient_id)

    # Mock appointments for demo (replace with your Appointment model later)
    appointments = [
        {
            "doctor": Doctor(fname="Prahlad", lname="Kumar", specialization="Cardiology"),
            "date": "2025-11-10",
            "time": "10:30 AM",
        },
        {
            "doctor": Doctor(fname="Evelyn", lname="Reed", specialization="Dermatology"),
            "date": "2025-11-18",
            "time": "9:00 AM",
        },
    ]

    context = {
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, 'patient/patient_dashboard.html', context)

# ===============================
# 🚪 4️⃣ LOGOUT
# ===============================
def patient_logout(request):
    request.session.flush()
    return redirect('home')

# ===============================
# 👤 5️⃣ PROFILE PAGE
# ===============================
def patient_profile(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')

    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'patient/patient_profile.html', {'patient': patient})

# ===============================
# ✏️ 6️⃣ UPDATE PROFILE
# ===============================
def patient_update_profile(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')

    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        patient.full_name = request.POST.get('full_name')
        patient.email = request.POST.get('email')
        patient.phone_number = request.POST.get('phone_number')
        patient.address = request.POST.get('address')
        patient.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('patient_profile')

    return render(request, 'patient/patient_profile.html', {'patient': patient})

# ===============================
# 🔑 7️⃣ CHANGE PASSWORD
# ===============================
def patient_change_password(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')

    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        if check_password(current_password, patient.password):
            patient.password = make_password(new_password)
            patient.save()
            messages.success(request, "Password changed successfully.")
            return redirect('patient_profile')
        else:
            messages.error(request, "Current password is incorrect.")

    return render(request, 'patient/patient_profile.html', {'patient': patient})

# ===============================
# 🧬 8️⃣ UPDATE MEDICAL INFO
# ===============================
def patient_update_medical_info(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')

    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        patient.blood_group = request.POST.get('blood_group')
        patient.medical_history = request.POST.get('medical_history')
        patient.save()
        messages.success(request, "Medical info updated successfully.")
        return redirect('patient_profile')

    return render(request, 'patient/patient_profile.html', {'patient': patient})

# ===============================
# 👨‍⚕️ 9️⃣ FIND DOCTORS
# ===============================


def find_doctors(request):
    # Get search and filter parameters
    search_query = request.GET.get('doctor_name', '').strip()
    specialty_filter = request.GET.get('specialty', '').strip()

    # Start with all doctors
    doctors = Doctor.objects.all()

    # Filter by name (case-insensitive)
    if search_query:
        doctors = doctors.filter(fname__icontains=search_query) | doctors.filter(lname__icontains=search_query)

    # Filter by specialization
    if specialty_filter:
        doctors = doctors.filter(specialization__iexact=specialty_filter)

    # Get distinct list of specializations for dropdown
    specialties = Doctor.objects.values_list('specialization', flat=True).distinct()

    return render(request, 'patient/find_doctors.html', {
        'doctors': doctors,
        'specialties': specialties,
        'search_query': search_query,
        'specialty_filter': specialty_filter
    })

# ===============================
# 📅 🔟 BOOK APPOINTMENT
# ===============================

def book_apponiment(request, doctor_id):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        messages.error(request, "Please log in to book an appointment.")
        return redirect('patient_login')

    doctor = get_object_or_404(Doctor, id=doctor_id)
    available_times = ["09:00 AM", "10:00 AM", "11:30 AM", "02:00 PM", "03:30 PM"]

    if request.method == 'POST':
        selected_date = request.POST.get('date')
        selected_time = request.POST.get('time')

        # Validate date input
        try:
            appointment_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
            if appointment_date < date.today():
                messages.error(request, "Appointment date cannot be in the past.")
                return redirect('book_apponiment', doctor_id=doctor_id)
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format.")
            return redirect('book_apponiment', doctor_id=doctor_id)

        if not selected_time:
            messages.error(request, "Please select a time slot.")
            return redirect('book_apponiment', doctor_id=doctor_id)

        # No DB saving yet — just simulate
        messages.success(
            request,
            f"Appointment booked successfully with Dr. {doctor.fname} {doctor.lname} on {appointment_date} at {selected_time}."
        )
        return redirect('patient_dashboard')

    return render(request, 'patient/book_apponiment.html', {
        'doctor': doctor,
        'available_times': available_times,
        'today': date.today(),
    })
