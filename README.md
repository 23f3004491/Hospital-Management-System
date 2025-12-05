# 🏥 Hospital Management System

A comprehensive web-based Hospital Management System built with Flask, enabling efficient management of hospital operations including doctors, patients, appointments, and treatments.

---

## 📋 Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Default Credentials](#default-credentials)
- [Database Schema](#database-schema)
- [Screenshots](#screenshots)
- [API Endpoints](#api-endpoints)
- [Author](#author)

---

## ✨ Features

### 👨‍💼 Admin Dashboard
- Manage doctors (add, edit, delete, blacklist)
- Manage patients (edit, delete, blacklist)
- Manage departments
- View all appointments and treatment history
- System-wide statistics and overview

### 👨‍⚕️ Doctor Dashboard
- View assigned appointments
- Manage availability (morning, afternoon, evening slots)
- Update patient treatment records
- View patient medical history
- Complete patient visits with diagnosis and prescription

### 👤 Patient Dashboard
- Search doctors by department
- Book appointments based on doctor availability
- View appointment history
- View medical history and treatments
- Manage profile information

### 🔐 Authentication
- Secure login and registration
- Role-based access control (Admin, Doctor, Patient)
- Session management
- Password hashing

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Flask** | Backend web framework |
| **Flask-SQLAlchemy** | ORM for database operations |
| **SQLite** | Database |
| **Jinja2** | Template engine |
| **Bootstrap 5** | Frontend styling |
| **HTML/CSS** | Frontend structure and design |
| **Werkzeug** | Password hashing and security |

---

## 📁 Project Structure

```
Hospital Management System_1/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore file
│
├── models/
│   └── models.py               # Database models
│
├── controllers/
│   ├── __init__.py
│   └── routes.py               # All route definitions
│
├── instance/
│   └── hospital.db             # SQLite database
│
├── templates/                  # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dasboard.html
│   ├── add_doctor.html
│   ├── patient_dashboard.html
│   ├── doctor_dasboard.html
│   ├── book_appoinment.html
│   ├── departments.html
│   ├── department_details.html
│   ├── doctor_availability.html
│   ├── doctor_availability_check.html
│   ├── doctor_details.html
│   ├── edit_patient.html
│   ├── patient_history.html
│   ├── patient_history_doctor.html
│   ├── patient_profile.html
│   ├── patient_search_doctors.html
│   ├── update_patient_history.html
│   └── view_appointment_history.html
│
└── venv/                       # Virtual environment
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Hospital Management System_1"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   ```
   http://127.0.0.1:5000
   ```

---

## 💻 Usage

### For Admin
1. Login with admin credentials
2. Add departments and doctors
3. Manage patients and appointments
4. View system statistics

### For Doctor
1. Register/Login as doctor (added by admin)
2. Set availability slots
3. View and manage appointments
4. Update patient treatment records

### For Patient
1. Register a new account
2. Complete profile information
3. Search doctors by department
4. Book appointments
5. View medical history

---

## 🔑 Default Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@hms.com | admin123 |

---

## 🗄️ Database Schema

### User
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| email | String | Unique, Not Null |
| passhash | String | Not Null |
| role | String | Not Null |
| is_active | Boolean | Default: True |
| is_admin | Boolean | Default: False |

### Department
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| name | String | Unique, Not Null |
| overview | Text | - |

### Doctor
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | FK → User.id, Unique |
| department_id | Integer | FK → Department.id |
| name | String | Not Null |
| experience_years | Integer | - |
| bio | Text | - |

### Patient
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | FK → User.id, Unique |
| name | String | Not Null |
| age | Integer | - |
| gender | String | - |
| contact | String | - |
| address | String | - |

### Appointment
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| doctor_id | Integer | FK → Doctor.id |
| patient_id | Integer | FK → Patient.id |
| date | Date | Not Null |
| time_slot | String | Not Null |
| status | String | Default: 'Booked' |
| created_at | DateTime | Default: UTC Now |

### DoctorAvailability
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| doctor_id | Integer | FK → Doctor.id |
| date | Date | Not Null |
| morning_slot | String | - |
| afternoon_slot | String | - |
| evening_slot | String | - |

### Treatment
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key |
| appointment_id | Integer | FK → Appointment.id, Unique |
| patient_id | Integer | FK → Patient.id |
| diagnosis | Text | - |
| prescription | Text | - |
| notes | Text | - |
| visit_date | Date | Default: UTC Now |

---

## 🔗 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/login` | User login |
| GET/POST | `/register` | User registration |
| GET | `/logout` | User logout |

### Admin Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/dashboard` | Admin dashboard |
| GET/POST | `/admin/add_doctor` | Add new doctor |
| GET/POST | `/admin/doctor/<id>/edit` | Edit doctor |
| POST | `/admin/doctor/<id>/delete` | Delete doctor |
| POST | `/admin/doctor/<id>/blacklist` | Blacklist doctor |
| GET/POST | `/admin/patient/<id>/edit` | Edit patient |
| POST | `/admin/patient/<id>/delete` | Delete patient |
| POST | `/admin/patient/<id>/blacklist` | Blacklist patient |

### Doctor Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/doctor/dashboard` | Doctor dashboard |
| GET/POST | `/doctor/availability` | Manage availability |
| GET | `/doctor/patient/<id>/history` | View patient history |
| GET/POST | `/doctor/appointment/<id>/complete` | Complete appointment |

### Patient Routes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/patient/dashboard` | Patient dashboard |
| GET/POST | `/patient/profile` | Manage profile |
| GET | `/patient/search_doctors` | Search doctors |
| GET/POST | `/patient/book_appointment/<id>` | Book appointment |
| GET | `/patient/history` | View medical history |
| GET | `/patient/appointments` | View appointments |

---

## 📸 Screenshots

> Add screenshots of your application here

---

## 👨‍💻 Author

- **Name:** Tarun Gangwar
- **Roll Number:** 23f3004491
- **Email:** 23f3004491@ds.study.iitm.ac.in
- **Institution:** Indian Institute of Technology Madras 

---

## 📄 License

This project is created for educational purposes.

---

## 🙏 Acknowledgements

- Flask Documentation
- Bootstrap Documentation
- SQLAlchemy Documentation

---

Video Explanation - https://drive.google.com/file/d/1uGWhQON6PaMx90wtVO91IU7MJc-djGrg/view?usp=sharing

