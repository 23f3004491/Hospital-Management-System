# Hospital Management System

A comprehensive web-based Hospital Management System built with Flask and SQLAlchemy for managing patients, doctors, departments, and appointments.

## Features

### Patient Features
- **User Registration & Login** - Secure authentication system
- **Book Appointments** - Browse doctors and book appointments with available time slots
- **View Appointments** - See upcoming and past appointments
- **Medical History** - Access treatment records and medical history
- **Profile Management** - Update personal information
- **Cancel/Reschedule** - Modify appointment bookings

### Doctor Features
- **Dashboard** - View upcoming appointments for the next 7 days
- **Availability Management** - Set availability for morning, afternoon, and evening slots
- **Patient History** - Update patient treatment records with diagnosis, prescription, and notes
- **Appointment Management** - Complete or cancel appointments

### Admin Features
- **User Management** - Add, edit, delete doctors and patients
- **Blacklist Management** - Deactivate users when needed
- **Department Management** - Manage medical departments
- **Appointment Tracking** - View all appointments and completed visits
- **Search Functionality** - Search doctors and patients by name, email, or department
- **System Dashboard** - Overview of doctors, patients, and appointments

## Tech Stack

- **Backend**: Flask (Python Web Framework)
- **Database**: SQLAlchemy ORM with SQLite
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Authentication**: Flask Sessions with password hashing
- **Security**: Werkzeug security utilities

## Installation

### Prerequisites
- Python 3.7+
- pip (Python Package Manager)

### Setup Instructions

1. **Clone the repository**
```bash
cd Hospital-Management-System
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Set up environment variables**

Create a `.env` file in the root directory:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
SQLALCHEMY_DATABASE_URI=sqlite:///hospital.db
```

6. **Run the application**
```bash
flask run
```

The application will be available at `http://127.0.0.1:5000`

## Project Structure

```
Hospital-Management-System/
├── app.py                 # Flask application initialization
├── config.py              # Configuration settings
├── models.py              # Database models
├── routes.py              # Application routes
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── patient_dashboard.html
│   ├── doctor_details.html
│   ├── doctor_dasboard.html
│   └── ... (other templates)
├── static/                # Static files (CSS, JS, images)
└── hospital.db            # SQLite database (created after first run)
```

## Database Models

### User
- email (unique)
- password hash
- role (admin, doctor, patient)
- is_active status

### Patient
- name
- age
- gender
- contact
- address
- user_id (foreign key)

### Doctor
- name
- department_id
- experience_years
- bio
- user_id (foreign key)

### Department
- name
- overview

### Appointment
- doctor_id
- patient_id
- date
- time_slot
- status (Booked, Completed, Cancelled)

### DoctorAvailability
- doctor_id
- date
- morning_slot
- afternoon_slot
- evening_slot

### Treatment
- appointment_id
- patient_id
- diagnosis
- prescription
- notes
- visit_date

## Default Login Credentials

### Admin
- **Email**: admin@hms.com
- **Password**: admin123

## Usage Guide

### For Patients
1. Register with your email and name
2. Login to your dashboard
3. Browse departments and doctors
4. Check doctor availability
5. Book an appointment by selecting date and time slot
6. View your appointment history
7. Update your profile

### For Doctors
1. Login with credentials (created by admin)
2. View upcoming appointments on dashboard
3. Set your availability for next 7 days
4. Update patient history after appointments
5. Cancel appointments if needed

### For Admin
1. Login with admin credentials
2. Add new doctors and assign departments
3. Manage users (edit, delete, blacklist)
4. Search for specific doctors or patients
5. Monitor all appointments and completed visits
6. View system statistics

## API Routes

### Authentication
- `GET /` - Home page
- `POST /register` - Register new patient
- `POST /login` - User login
- `GET /logout` - User logout

### Patient Routes
- `GET /patient/dashboard` - Patient dashboard
- `GET /patient/history` - Medical history
- `GET /patient/profile` - Patient profile
- `POST /patient/profile` - Update profile
- `POST /book_appointment` - Book appointment
- `POST /appointment/<id>/cancel` - Cancel appointment
- `POST /appointment/<id>/reschedule` - Reschedule appointment

### Doctor Routes
- `GET /doctor/dashboard` - Doctor dashboard
- `GET /doctor/availability` - Manage availability
- `POST /doctor/availability` - Update availability
- `GET /appointment/<id>/complete` - Complete appointment form
- `POST /appointment/<id>/complete` - Mark appointment complete

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/search` - Search users
- `POST /admin/add_doctor` - Add new doctor
- `POST /admin/doctor/<id>/edit` - Edit doctor
- `POST /admin/doctor/<id>/delete` - Delete doctor
- `POST /admin/patient/<id>/blacklist` - Blacklist patient

### Browse Routes
- `GET /department/<id>` - View department doctors
- `GET /doctor/<id>` - View doctor details
- `GET /doctor/<id>/availability` - Check doctor availability

## Features Highlights

- ✅ Role-based access control (Patient, Doctor, Admin)
- ✅ Secure password hashing with Werkzeug
- ✅ Session-based authentication
- ✅ Responsive Bootstrap UI
- ✅ Real-time appointment booking
- ✅ Doctor availability management
- ✅ Medical history tracking
- ✅ Search and filter functionality
- ✅ User blacklisting system
- ✅ Dynamic appointment scheduling

## Security Features

- Password hashing with werkzeug.security
- Session-based authentication
- Role-based access control (RBAC)
- CSRF protection
- SQL injection prevention (ORM)
- User account blacklisting

## Future Enhancements

- Email notifications for appointments
- SMS reminders
- Online payment integration
- Prescription printing
- Medical reports generation
- Video consultation feature
- Appointment ratings and reviews
- Doctor availability calendar view
- Patient health records (PDF export)

## Troubleshooting

### Issue: Database not found
**Solution**: Delete `hospital.db` and restart the application. The database will be recreated automatically.

### Issue: Port 5000 already in use
**Solution**: 
```bash
flask run --port 5001
```

### Issue: Module import errors
**Solution**: Ensure virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@hms.com or open an issue in the repository.

## Authors

- Development Team - Hospital Management System

## Acknowledgments

- Flask documentation and community
- Bootstrap framework
- SQLAlchemy ORM

---

**Last Updated**: November 9, 2025

**Version**: 1.0.0