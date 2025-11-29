from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    passhash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False)
    patient_profile = db.relationship('Patient', backref='user', uselist=False)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    overview = db.Column(db.Text)
    doctors = db.relationship('Doctor', backref='department', lazy=True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    availability = db.relationship('DoctorAvailability', backref='doctor', lazy=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    contact = db.Column(db.String(20))
    address = db.Column(db.String(200))
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    history = db.relationship('Treatment', backref='patient', lazy=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Booked')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    treatment_record = db.relationship('Treatment', backref='appointment', uselist=False)

class DoctorAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    morning_slot = db.Column(db.String(200))
    afternoon_slot = db.Column(db.String(200))
    evening_slot = db.Column(db.String(200))

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), unique=True, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    visit_date = db.Column(db.Date, default=datetime.utcnow)