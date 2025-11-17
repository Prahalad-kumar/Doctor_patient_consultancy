# patient/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from datetime import datetime, date

from .models import Patient
from doctor.models import Doctor
from apponiment.models import Appointment
from apponiment.views import generate_time_slots


# ===============================
# 🧾 PATIENT SIGNUP
# ===============================
def patient_signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password_raw = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        blood_group = request.POST.get('blood_group')
        medical_history = request.POST.get('medical_history')

        # Validate passwords
        if password_raw != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('patient_signup')

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
                    return redirect('patient_signup')
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
            date_of_birth=dob_parsed,
            phone_number=phone_number,
            email=email,
            address=address,
            password=make_password(password_raw),
            blood_group=blood_group,
            medical_history=medical_history
        )

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('patient_login')

    return render(request, 'patient/patient_signup.html', {'Today': date.today()})


# ===============================
# 🔐 PATIENT LOGIN
# ===============================
def patient_login(request):
    storage = messages.get_messages(request)
    storage.used = True
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
# 🏠 PATIENT DASHBOARD (real DB appointments)
# ===============================
def patient_dashboard(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')

    patient = get_object_or_404(Patient, id=patient_id)

    # Real upcoming appointments (today and future)
    appointments = Appointment.objects.filter(
        patient=patient,
        appointment_date__gte=date.today()
    ).order_by('appointment_date', 'appointment_time')

    return render(request, 'patient/patient_dashboard.html', {
        'patient': patient,
        'appointments': appointments,
    })


# ===============================
# 🚪 LOGOUT
# ===============================
def patient_logout(request):
    request.session.flush()
    return redirect('home')


# ===============================
# 👤 PROFILE
# ===============================
def patient_profile(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')

    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'patient/patient_profile.html', {'patient': patient})


# ===============================
# ✏️ UPDATE PROFILE
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
# 🔑 CHANGE PASSWORD
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
# 🧬 UPDATE MEDICAL INFO
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
# 👨‍⚕️ FIND DOCTORS
# ===============================
def find_doctors(request):
    search_query = request.GET.get('doctor_name', '').strip()
    specialty_filter = request.GET.get('specialty', '').strip()

    doctors = Doctor.objects.all()

    if search_query:
        doctors = doctors.filter(fname__icontains=search_query) | doctors.filter(lname__icontains=search_query)

    if specialty_filter:
        doctors = doctors.filter(specialization__iexact=specialty_filter)

    specialties = Doctor.objects.values_list('specialization', flat=True).distinct()

    return render(request, 'patient/find_doctors.html', {
        'doctors': doctors,
        'specialties': specialties,
        'search_query': search_query,
        'specialty_filter': specialty_filter
    })


# ===============================
# 📅 BOOK APPOINTMENT (uses Appointment model)
# ===============================
def book_apponiment(request, doctor_id):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        messages.error(request, "Please log in to book an appointment.")
        return redirect('patient_login')

    patient = get_object_or_404(Patient, id=patient_id)
    doctor = get_object_or_404(Doctor, id=doctor_id)

    # All time slots (9 AM - 5 PM, 30 mins)
    all_slots = generate_time_slots()

    # Selected date (GET)
    selected_date = request.GET.get('date')
    available_slots = all_slots

    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()

            # Get booked slots for selected date
            booked = Appointment.objects.filter(doctor=doctor, appointment_date=selected_date_obj)
            taken_times = [a.appointment_time.strftime("%I:%M %p") for a in booked]

            # Remove booked slots
            available_slots = [s for s in all_slots if s not in taken_times]

            # ⛔ Hide past time slots if selected date = today
            if selected_date_obj == date.today():
                now = datetime.now().time()

                filtered_slots = []
                for s in available_slots:
                    slot_time = datetime.strptime(s, "%I:%M %p").time()
                    if slot_time > now:  # only future slots
                        filtered_slots.append(s)

                available_slots = filtered_slots

        except Exception:
            available_slots = all_slots

    # -----------------------------
    # Handle FORM SUBMIT (POST)
    # -----------------------------
    if request.method == 'POST':

        date_input = request.POST.get('date')
        time_input = request.POST.get('time')

        # Parse date
        try:
            appointment_date = datetime.strptime(date_input, "%Y-%m-%d").date()
        except:
            messages.error(request, "Invalid date selected.")
            return redirect('book_apponiment', doctor_id=doctor_id)

        # Parse time
        try:
            appointment_time = datetime.strptime(time_input, "%I:%M %p").time()
        except:
            messages.error(request, "Invalid time selected.")
            return redirect('book_apponiment', doctor_id=doctor_id)

        # ⛔ Prevent past date
        if appointment_date < date.today():
            messages.error(request, "You cannot book a past date.")
            return redirect('book_apponiment', doctor_id=doctor_id)

        # ⛔ Prevent past time on today's date
        if appointment_date == date.today():
            now = datetime.now().time()
            if appointment_time <= now:
                messages.error(request, "You cannot book a past time slot.")
                return redirect('book_apponiment', doctor_id=doctor_id)

        # ⛔ Prevent booking already-taken slot
        if Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists():
            messages.error(request, "This time slot is already booked!")
            return redirect('book_apponiment', doctor_id=doctor_id)

        # ✅ Create appointment
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status="Pending"
        )

        messages.success(request, "Appointment booked successfully!")
        return redirect('patient_appointments')

    # -----------------------------
    # Render page
    # -----------------------------
    return render(request, 'patient/book_apponiment.html', {
        'doctor': doctor,
        'slots': available_slots,
        'today': date.today(),
        'selected_date': selected_date or '',
    })

