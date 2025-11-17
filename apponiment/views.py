# apponiment/views.py
from datetime import datetime, timedelta, time, date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Appointment
from doctor.models import Doctor
from patient.models import Patient


# ---------------------------------------------------------
# GENERATE TIME SLOTS (9AM – 5PM, 30-minute slots)
# ---------------------------------------------------------
def generate_time_slots():
    slots = []
    start = datetime.strptime("09:00 AM", "%I:%M %p")
    end = datetime.strptime("05:00 PM", "%I:%M %p")

    while start < end:
        slots.append(start.strftime("%I:%M %p"))
        start += timedelta(minutes=30)

    return slots


# ---------------------------------------------------------
# PATIENT: BOOK APPOINTMENT (uses form field names 'date' and 'time')
# ---------------------------------------------------------
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    all_slots = generate_time_slots()

    if request.method == "POST":
        patient_id = request.session.get("patient_id")

        if not patient_id:
            messages.error(request, "Please login to book.")
            return redirect("patient_login")

        patient = get_object_or_404(Patient, id=patient_id)
        date_str = request.POST.get("date")
        time_str = request.POST.get("time")

        # parse
        try:
            appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            messages.error(request, "Invalid date.")
            return render(request, "appointment/book.html", {
                "doctor": doctor,
                "slots": all_slots,
            })

        try:
            appointment_time = datetime.strptime(time_str, "%I:%M %p").time()
        except:
            messages.error(request, "Invalid time.")
            return render(request, "appointment/book.html", {
                "doctor": doctor,
                "slots": all_slots,
            })

        if appointment_date < date.today():
            messages.error(request, "Cannot book in the past.")
            return render(request, "appointment/book.html", {
                "doctor": doctor,
                "slots": all_slots,
            })

        # Check if already booked
        if Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists():
            messages.error(request, "This time slot is already booked!")
            return render(request, "appointment/book.html", {
                "doctor": doctor,
                "slots": all_slots,
            })

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status="Pending"
        )

        messages.success(request, "Appointment booked successfully!")
        return redirect("patient_appointments")

    return render(request, "appointment/book.html", {
        "doctor": doctor,
        "slots": all_slots,
    })


# ---------------------------------------------------------
# PATIENT: VIEW BOOKINGS
# ---------------------------------------------------------
def patient_appointments(request):
    patient_id = request.session.get("patient_id")
    if not patient_id:
        return redirect("patient_login")

    patient = get_object_or_404(Patient, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient).order_by("-appointment_date", "-appointment_time")

    return render(request, "appointment/patient_appointments.html", {
        "appointments": appointments
    })


# ---------------------------------------------------------
# DOCTOR: VIEW ALL APPOINTMENTS
# ---------------------------------------------------------
def doctor_appointments(request):
    doctor_id = request.session.get("doctor_id")
    if not doctor_id:
        return redirect("doctor_login")

    doctor = get_object_or_404(Doctor, id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor).order_by("appointment_date", "appointment_time")

    return render(request, "appointment/doctor_appointments.html", {
        "appointments": appointments
    })


# ---------------------------------------------------------
# DOCTOR: UPDATE APPOINTMENT STATUS (Approve / Cancel / Complete)
# ---------------------------------------------------------
def update_status(request, id, status):
    appointment = get_object_or_404(Appointment, id=id)

    if status not in ["Approved", "Cancelled", "Completed"]:
        messages.error(request, "Invalid status")
        return redirect("doctor_appointments")

    appointment.status = status
    appointment.save()

    messages.success(request, "Status updated successfully!")
    # Redirect back to where the request came from when possible
    ref = request.META.get('HTTP_REFERER')
    if ref:
        return redirect(ref)
    return redirect("doctor_appointments")


# ---------------------------------------------------------
# PATIENT: CANCEL (via patient dashboard)
# ---------------------------------------------------------
def cancel_by_patient(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    if appointment.status == "Completed":
        messages.error(request, "Completed appointments cannot be cancelled.")
        return redirect("patient_appointments")

    appointment.status = "Cancelled"
    appointment.save()

    messages.success(request, "Appointment cancelled.")
    return redirect("patient_appointments")
