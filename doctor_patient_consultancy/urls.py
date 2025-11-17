# doctor_patient_consultancy/urls.py
from django.contrib import admin
from django.urls import path
from patient import views as patient_views
from doctor import views as doctor_views
from . import views as core_views
from apponiment import views as appointment_views

urlpatterns = [
    # home
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('patient/', core_views.patient, name='patient'),
    path('doctor/', core_views.doctor, name='doctor'),
    path('about/', core_views.about, name='about'),
    path('contact/', core_views.contact, name='contact'),

    # Patient urls
    path('patient/signup/', patient_views.patient_signup, name='patient_signup'),
    path('patient/login/', patient_views.patient_login, name='patient_login'),
    path('patient/dashboard/', patient_views.patient_dashboard, name='patient_dashboard'),
    path('patient/logout/', patient_views.patient_logout, name='patient_logout'),
    path('patient/profile/', patient_views.patient_profile, name='patient_profile'),
    path('patient/profile/update/', patient_views.patient_update_profile, name='patient_update_profile'),
    path('patient/change-password/', patient_views.patient_change_password, name='patient_change_password'),
    path('patient/medical-info/update/', patient_views.patient_update_medical_info, name='patient_update_medical_info'),
    path('patient/find-doctors/', patient_views.find_doctors, name='find_doctors'),
    path('patient/book-apponiment/<int:doctor_id>/', patient_views.book_apponiment, name='book_apponiment'),

    # Doctor urls
    path('doctor/create-account/', doctor_views.create_account, name='create_account'),
    path('doctor/login/', doctor_views.doctor_login, name='doctor_login'),
    path('doctor/logout/', doctor_views.doctor_logout, name='doctor_logout'),
    path('doctor/dashboard/', doctor_views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/profile/', doctor_views.doctor_profile, name='doctor_profile'),
    path('doctor/schedule/', doctor_views.doctor_schedule, name='doctor_schedule'),
    path('doctor/update-profile/', doctor_views.doctor_update_profile, name='doctor_update_profile'),
    path('doctor/change-password/', doctor_views.doctor_change_password, name='doctor_change_password'),

    # Appointment urls
    path('appointment/book/<int:doctor_id>/', appointment_views.book_appointment, name='book_appointment'),
    path('appointment/patient-appointments/', appointment_views.patient_appointments, name='patient_appointments'),
    path('appointment/doctor-appointments/', appointment_views.doctor_appointments, name='doctor_appointments'),
    path('appointment/update-status/<int:id>/<str:status>/', appointment_views.update_status, name='update_status'),
    path('appointment/cancel/<int:id>/', appointment_views.cancel_by_patient, name='cancel_by_patient'),
]
