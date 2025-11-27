# 🩺 **Doctor-Patient Consultancy System**  
*A Production-Ready Healthcare Appointment & Scheduling Platform*  
👨‍⚕️👩‍⚕️📅💊  

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue" />
  <img src="https://img.shields.io/badge/Django-5.2-green" />
  <img src="https://img.shields.io/badge/Postgres-Railway-blueviolet" />
  <img src="https://img.shields.io/badge/Deploy-Railway-purple" />
  <img src="https://img.shields.io/badge/Security-Env_Vars-critical" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" />
</p>

---

# 📑 **Table of Contents**
- [🩺 Doctor-Patient Consultancy System](#-doctor-patient-consultancy-system)
  - [🚀 Project Overview](#-project-overview)
  - [🎯 Why Recruiters Will Love This](#-why-recruiters-will-love-this)
  - [✨ Key Features (Impact-Oriented)](#-key-features-impact-oriented)
  - [🛠 Tech Stack](#-tech-stack)
  - [🧠 Skills Demonstrated](#-skills-demonstrated)
  - [🗄️ Database Models (ERD)](#️-database-models-erd)
  - [🏛️ System Architecture Diagram](#️-system-architecture-diagram)
  - [🎞️ Appointment Booking Workflow](#️-appointment-booking-workflow)
  - [📦 Installation Guide](#-installation-guide-local-development)
  - [🚀 Deployment (Railway)](#-deployment-railway)
  - [🖼️ Screenshots](#️-screenshots-add-later)
  - [📊 Real-World Use Cases](#-real-world-use-cases)
  - [🚧 Roadmap](#-roadmap)
  - [👤 Author](#-author)
  - [📄 License](#-license)

---

# 🚀 **Project Overview**
The **Doctor-Patient Consultancy System** is a secure, scalable Django-based healthcare platform that enables:

- Efficient appointment booking  
- Doctor–Patient management  
- Medical record storage  
- Role-based scheduling functionality  
- Production deployment with PostgreSQL & Railway  

This project is built with a **production-first mindset**, ideal for recruiters evaluating backend engineering capability.

---

# 🎯 **Why Recruiters Will Love This**
- 💼 Real-world healthcare workflow  
- 🏗 Professional backend architecture  
- 🔐 Strong security (CSRF, env vars, hashed passwords)  
- 🗄 PostgreSQL relational model with ERD  
- 🚀 Live production-level deployment skills  
- 📅 Complex scheduling logic  

---

# ✨ **Key Features (Impact-Oriented)**

## 👨‍⚕️ Doctor Module
- Manage professional profile  
- Approve / cancel / complete appointments  
- Dashboard showing upcoming patients  
- Authentication + secure session handling  

---

## 🧑‍🦰 Patient Module
- Signup/login securely  
- Update profile & medical history  
- Find doctors by name/specialization  
- View appointment history  

---

## 📅 Appointment Management
- Auto 30-min slot generation (9AM–5PM)  
- Double-booking prevention  
- Appointment lifecycle:  
  **Pending → Approved → Completed / Cancelled**  
- Transaction-safe workflows  

---

# 🛠 **Tech Stack**
| Layer | Technology |
|-------|------------|
| Backend | Django 5.2, Python 3.11 |
| Database | PostgreSQL |
| Deployment | Railway |
| Frontend | Django Templates (HTML/CSS) |
| Security | Django Auth, CSRF, Validation |

---

# 🧠 **Skills Demonstrated**
✔ Django MVC Architecture  
✔ Scheduling & Appointment Logic  
✔ Secure Authentication  
✔ PostgreSQL Schema Design  
✔ Environment Variable Security  
✔ Production Deployment (Railway + Gunicorn)  
✔ Template Rendering  
✔ Form Validation  
✔ CSRF + Session Security  

---

# 🗄️ **Database Models (ERD)**

```mermaid
erDiagram
    PATIENT ||--o{ APPOINTMENT : books
    DOCTOR ||--o{ APPOINTMENT : receives

    PATIENT {
        int id
        string full_name
        string gender
        date date_of_birth
        string phone_number
        string email
        string address
        string password
        string blood_group
        text medical_history
    }

    DOCTOR {
        int id
        string fname
        string lname
        string email
        string password
        string specialization
        int years_of_experience
        string qualification
        string contact_number
        string address
        text bio
    }

    APPOINTMENT {
        int id
        date appointment_date
        time appointment_time
        string status
    }
```

---

# 🏛️ **System Architecture Diagram**

```mermaid
graph LR
    A[🧑‍🦰 Patient] -->|Books| B(🌐 Django Views)
    C[👨‍⚕️ Doctor] -->|Manages| B

    B -->|CRUD| D[(🗄 PostgreSQL DB)]
    B -->|Render| E[🎨 Templates]

    subgraph Security Layer
        X[🔐 Session Auth]
        Y[🔒 CSRF Protection]
    end

    B --> X
    B --> Y

    D --> Z[(🚀 Railway Deployment)]
```

---

# 🎞️ **Appointment Booking Workflow**

```mermaid
sequenceDiagram
    autonumber
    participant P as 🧑‍🦰 Patient
    participant Sys as 🌐 System
    participant D as 👨‍⚕️ Doctor
    participant DB as 🗄 Database

    P->>Sys: Search doctor
    Sys->>DB: Fetch doctor list
    DB-->>Sys: List returned
    Sys-->>P: Display doctors

    P->>Sys: Request booking
    Sys->>DB: Check booked slots
    Sys-->>P: Show available slots

    P->>Sys: Book slot
    Sys->>DB: Validate + Save (Pending)
    DB-->>Sys: OK
    Sys-->>D: Notify doctor
    Sys-->>P: Booking confirmed
```

---

# 📦 **Installation Guide (Local Development)**

```bash
git clone <repo-url>
cd doctor_patient_consultancy

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

# 🚀 **Deployment (Railway)**

```bash
railway login
railway init

railway variables set SECRET_KEY="..."
railway variables set DATABASE_URL="postgres://..."
railway variables set DEBUG="False"
railway variables set RAILWAY_PUBLIC_DOMAIN="your-app.up.railway.app"

railway up
```

**Production Server:**

```bash
gunicorn doctor_patient_consultancy.wsgi:application --bind 0.0.0.0:$PORT --workers 3
```

---

# 🖼️ Screenshots

---

## 🏠 Home Page
![Home Page](./screenshots/home.png)

---

## 🔐 Doctor Login Page
![Doctor Login Page](./screenshots/doctor-login.png)

---

## 🔐 Patient Login Page
![Patient Login Page](./screenshots/patient-login.png)

---

## 🏠 Patient Dashboard
![Patient Dashboard](./screenshots/patient-dashboard.png)

---

## 👨‍⚕️ Doctor Dashboard
![Doctor Dashboard](./screenshots/doctor-dashboard.png)

---

## 👨‍⚕️ Doctor Profile
![Doctor Profile](./screenshots/doctor-profile.png)

---

## 👤 Patient Profile
![Patient Profile](./screenshots/patient-profile.png)

---

## 📝 Doctor Profile Update
![Patient Profile Update](./screenshots/doctor-update-profile.png)

---

## 📝 Doctor find Page
![Doctor find Page](./screenshots/find-doctor.png)

---

## 📅 Appointment Booking
![Appointment Booking](./screenshots/Booking.png)

---

## 📋 Doctor Appointment Management
![Doctor Appointment Management](./screenshots/doctor-sechdule.png)


---

# 📊 **Real-World Use Cases**
- Private clinics  
- Telemedicine startups  
- Hospital scheduling backend  
- Healthcare MVP validation  
- Backend engineer portfolio projects  

---

# 🚧 **Roadmap**
- SMS/email reminders  
- Doctor–patient chat  
- RBAC (Admin/Doctor/Patient roles)  
- Analytics dashboard  
- Calendar sync  
- Prescription uploads  

---

# 👤 **Author**
**PRAHALAD KUMAR**  
Python Developer | Backend Engineer  
📧 Email: **Prahaladkr1@gmail.com**  
🐙 GitHub: https://github.com/Prahalad-kumar  
🔗 LinkedIn: https://www.linkedin.com/in/prahalad-kumar-86a81a327/  

---

# 📄 **License**
MIT License  
