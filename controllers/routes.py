from flask import render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, date
from models.models import db, User, Department, Doctor, Patient, Appointment, DoctorAvailability, Treatment

def init_routes(app):
    
    def login_required(fn):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash("Please log in first.", "warning")
                return redirect(url_for('login'))
            return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper

    def role_required(*roles):
        def decorator(fn):
            def wrapper(*args, **kwargs):
                if 'user_id' not in session:
                    flash("Please log in first.", "warning")
                    return redirect(url_for('login'))
                user = User.query.get(session['user_id'])
                if not user or user.role not in roles:
                    abort(403)
                return fn(*args, **kwargs)
            wrapper.__name__ = fn.__name__
            return wrapper
        return decorator

    def _current_user():
        uid = session.get('user_id')
        return User.query.get(uid) if uid else None

    def _doctor_slot_taken(doctor_id: int, appt_date: date, time_slot: str) -> bool:
        clash = Appointment.query.filter_by(
            doctor_id=doctor_id,
            date=appt_date,
            time_slot=time_slot
        ).filter(Appointment.status != "Cancelled").first()
        return clash is not None

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            name = request.form.get("name", "").strip()
            password = request.form.get("password", "")

            if not all([email, name, password]):
                flash("All fields are required.", "danger")
                return render_template("register.html")

            if User.query.filter_by(email=email).first():
                flash("Email already registered. Please login.", "warning")
                return redirect(url_for("login"))

            user = User(
                email=email,
                passhash=generate_password_hash(password),
                role="patient",
                is_active=True
            )
            db.session.add(user)
            db.session.commit()

            patient = Patient(user_id=user.id, name=name)
            db.session.add(patient)
            db.session.commit()

            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")

            if not email or not password:
                flash("Email and password are required.", "danger")
                return render_template("login.html")

            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.passhash, password):
                if not user.is_active:
                    flash("Your account has been deactivated. Please contact admin.", "danger")
                    return render_template("login.html")
                    
                session["user_id"] = user.id
                session["role"] = user.role

                if user.role == "admin":
                    return redirect(url_for("admin_dashboard"))
                elif user.role == "doctor":
                    return redirect(url_for("doctor_dashboard"))
                else:
                    return redirect(url_for("patient_dashboard"))
            else:
                flash("Invalid email or password.", "danger")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logged out.", "info")
        return redirect(url_for("login"))

    @app.route("/admin/dashboard")
    @role_required("admin")
    def admin_dashboard():
        doctors = Doctor.query.all()
        patients = Patient.query.all()
        
        today = date.today()
        appts = Appointment.query.filter(
            Appointment.status == "Booked",
            Appointment.date >= today
        ).order_by(Appointment.date.asc()).all()
        
        completed_appts = Appointment.query.filter(
            Appointment.status == "Completed"
        ).order_by(Appointment.date.desc()).limit(50).all()

        return render_template(
            "admin_dasboard.html",
            doctor_count=len(doctors),
            patient_count=len(patients),
            appointment_count=len(appts),
            doctors=doctors,
            patients=patients,
            appointments=appts,
            completed_appointments=completed_appts
        )

    @app.route("/admin/patient/<int:patient_id>/edit", methods=["GET", "POST"])
    @role_required("admin")
    def admin_edit_patient(patient_id):
        patient = Patient.query.get_or_404(patient_id)
        
        if request.method == "POST":
            patient.name = request.form.get("name", patient.name).strip()
            db.session.commit()
            flash("Patient name updated successfully.", "success")
            return redirect(url_for("admin_dashboard"))
        
        treatments = Treatment.query.join(Appointment).filter(
            Appointment.patient_id == patient_id
        ).order_by(Treatment.visit_date.desc()).all()
        
        return render_template("edit_patient.html", patient=patient, treatments=treatments)

    @app.route("/appointment/<int:appt_id>/history")
    @role_required("admin")
    def view_appointment_history(appt_id):
        appointment = Appointment.query.get_or_404(appt_id)
        treatment = Treatment.query.filter_by(appointment_id=appt_id).first()
        
        return render_template("view_appointment_history.html", appointment=appointment, treatment=treatment)

    @app.route("/admin/add_doctor", methods=["GET", "POST"])
    @role_required("admin")
    def admin_add_doctor():
        departments = Department.query.order_by(Department.name.asc()).all()

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            dept_id = request.form.get("department", "").strip()
            experience_years = request.form.get("experience_years") or None
            bio = request.form.get("bio", "").strip()

            if not all([name, email, password, dept_id]) or dept_id == "Choose...":
                flash("Name, email, password, and department are required.", "danger")
                return render_template("add_doctor.html", departments=departments)

            if User.query.filter_by(email=email).first():
                flash("Email already in use.", "warning")
                return render_template("add_doctor.html", departments=departments)

            user = User(
                email=email,
                passhash=generate_password_hash(password),
                role="doctor",
                is_active=True
            )
            db.session.add(user)
            db.session.commit()

            doctor = Doctor(
                user_id=user.id,
                department_id=int(dept_id),
                name=name,
                experience_years=int(experience_years) if experience_years else None,
                bio=bio
            )
            db.session.add(doctor)
            db.session.commit()

            flash("Doctor created successfully.", "success")
            return redirect(url_for("admin_dashboard"))

        return render_template("add_doctor.html", departments=departments)

    @app.route("/admin/doctor/<int:doc_id>/edit", methods=["GET", "POST"])
    @role_required("admin")
    def admin_edit_doctor(doc_id):
        doctor = Doctor.query.get_or_404(doc_id)
        departments = Department.query.order_by(Department.name.asc()).all()

        if request.method == "POST":
            doctor.name = request.form.get("name", doctor.name).strip()
            doctor.department_id = int(request.form.get("department") or doctor.department_id)
            exp = request.form.get("experience_years")
            doctor.experience_years = int(exp) if exp else doctor.experience_years
            doctor.bio = request.form.get("bio", doctor.bio).strip()
            db.session.commit()
            flash("Doctor updated.", "success")
            return redirect(url_for("admin_dashboard"))

        return render_template("add_doctor.html", departments=departments, doctor=doctor)

    @app.route("/admin/doctor/<int:doc_id>/delete", methods=["POST"])
    @role_required("admin")
    def admin_delete_doctor(doc_id):
        doctor = Doctor.query.get_or_404(doc_id)
        user_id = doctor.user_id
        
        appointments = Appointment.query.filter_by(doctor_id=doc_id).all()
        for appointment in appointments:
            Treatment.query.filter_by(appointment_id=appointment.id).delete()
        
        Appointment.query.filter_by(doctor_id=doc_id).delete()
        DoctorAvailability.query.filter_by(doctor_id=doc_id).delete()
        
        db.session.delete(doctor)
        db.session.commit()
        
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        
        flash("Doctor deleted successfully.", "success")
        return redirect(url_for("admin_dashboard"))

    @app.route("/admin/patient/<int:patient_id>/delete", methods=["POST"])
    @role_required("admin")
    def admin_delete_patient(patient_id):
        patient = Patient.query.get_or_404(patient_id)
        user_id = patient.user_id
        
        appointments = Appointment.query.filter_by(patient_id=patient_id).all()
        for appointment in appointments:
            Treatment.query.filter_by(appointment_id=appointment.id).delete()
        
        Appointment.query.filter_by(patient_id=patient_id).delete()
        
        db.session.delete(patient)
        db.session.commit()
        
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        
        flash("Patient deleted successfully.", "success")
        return redirect(url_for("admin_dashboard"))

    @app.route('/admin/patient/<int:patient_id>/blacklist', methods=['POST'])
    @role_required('admin')
    def admin_blacklist_patient(patient_id):
        patient = Patient.query.get_or_404(patient_id)
        user = User.query.get(patient.user_id)
        
        if user:
            user.is_active = False
            db.session.commit()
            flash('Patient has been blacklisted successfully', 'success')
        
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/doctor/<int:doc_id>/blacklist', methods=['POST'])
    @role_required('admin')
    def admin_blacklist_doctor(doc_id):
        doctor = Doctor.query.get_or_404(doc_id)
        user = User.query.get(doctor.user_id)
        
        if user:
            user.is_active = False
            db.session.commit()
            flash('Doctor has been blacklisted successfully', 'success')
        
        return redirect(url_for('admin_dashboard'))

    @app.route("/admin/search")
    @role_required("admin")
    def admin_search():
        q = (request.args.get("q") or "").strip().lower()
        by = (request.args.get("by") or "doctor").lower()

        doctors = Doctor.query.all()
        patients = Patient.query.all()

        if q:
            if by == "doctor":
                doctors = Doctor.query.join(User, Doctor.user_id == User.id)\
                    .join(Department, Doctor.department_id == Department.id)\
                    .filter(
                        db.or_(
                            db.func.lower(Doctor.name).contains(q),
                            db.func.lower(Department.name).contains(q),
                            db.func.lower(User.email).contains(q)
                        )
                    ).all()
            else:
                patients = Patient.query.join(User, Patient.user_id == User.id)\
                    .filter(
                        db.or_(
                            db.func.lower(Patient.name).contains(q),
                            db.func.lower(User.email).contains(q),
                            db.cast(Patient.id, db.String).contains(q),
                            db.func.lower(Patient.contact).contains(q)
                        )
                    ).all()

        today = date.today()
        appts = Appointment.query.filter(
            Appointment.status == "Booked",
            Appointment.date >= today
        ).order_by(Appointment.date.asc()).all()
        
        completed_appts = Appointment.query.filter(
            Appointment.status == "Completed"
        ).order_by(Appointment.date.desc()).limit(50).all()

        return render_template(
            "admin_dasboard.html",
            doctor_count=Doctor.query.count(),
            patient_count=Patient.query.count(),
            appointment_count=len(appts),
            doctors=doctors,
            patients=patients,
            appointments=appts,
            completed_appointments=completed_appts,
            search_query=q,
            search_type=by
        )

    @app.route("/department/<int:dept_id>")
    @login_required
    def department_details(dept_id):
        department = Department.query.get_or_404(dept_id)
        doctors = Doctor.query.filter_by(department_id=dept_id)\
            .order_by(Doctor.name.asc()).all()
        
        return render_template(
            "department_details.html",
            department=department,
            doctors=doctors
        )

    @app.route("/doctor/<int:doc_id>")
    @login_required
    def doctor_details(doc_id):
        doctor = Doctor.query.get_or_404(doc_id)
        avail = DoctorAvailability.query.filter_by(doctor_id=doc_id)\
                .order_by(DoctorAvailability.date.asc()).all()
        return render_template("doctor_details.html", doctor=doctor, availability=avail)

    @app.route("/doctor/<int:doc_id>/availability")
    @login_required
    def check_doctor_availability(doc_id):
        doctor = Doctor.query.get_or_404(doc_id)
        
        today = date.today()
        seven_days = today + timedelta(days=7)
        
        availability = DoctorAvailability.query.filter(
            DoctorAvailability.doctor_id == doc_id,
            DoctorAvailability.date >= today,
            DoctorAvailability.date <= seven_days
        ).order_by(DoctorAvailability.date.asc()).all()
        
        return render_template(
            "doctor_availability_check.html",
            doctor=doctor,
            availability=availability,
            today=today
        )

    @app.route("/patient/dashboard")
    @role_required("patient")
    def patient_dashboard():
        user = _current_user()
        patient = Patient.query.filter_by(user_id=user.id).first()
        if not patient:
            flash("Patient profile not found.", "warning")
            return redirect(url_for("home"))

        today = date.today()
        departments = Department.query.order_by(Department.name.asc()).all()

        upcoming_appointments = Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.date >= today
        ).order_by(Appointment.date.asc()).all()

        return render_template(
            "patient_dashboard.html",
            patient=patient,
            departments=departments,
            upcoming_appointments=upcoming_appointments
        )

    @app.route("/patient/history")
    @role_required("patient")
    def patient_history():
        user = _current_user()
        patient = Patient.query.filter_by(user_id=user.id).first()
        if not patient:
            flash("Patient profile not found.", "warning")
            return redirect(url_for("home"))

        appointments = Appointment.query.filter_by(patient_id=patient.id)\
            .order_by(Appointment.date.desc()).all()
            
        treatments = Treatment.query.join(Appointment)\
            .filter(Appointment.patient_id == patient.id)\
            .order_by(Treatment.visit_date.desc()).all()
            
        return render_template("patient_history.html", 
                            appointments=appointments,
                            treatments=treatments)

    @app.route("/patient/profile", methods=["GET", "POST"])
    @role_required("patient")
    def patient_profile():
        user = _current_user()
        patient = Patient.query.filter_by(user_id=user.id).first()

        if request.method == "POST":
            patient.name = request.form.get("name", patient.name).strip()
            db.session.commit()
            flash("Profile updated.", "success")
            return redirect(url_for("patient_profile"))

        return render_template("patient_profile.html", patient=patient)

    @app.route("/book_appointment", methods=["POST"])
    @role_required("patient")
    def book_appointment():
        user = _current_user()
        patient = Patient.query.filter_by(user_id=user.id).first()
        
        if not patient:
            flash("Patient profile not found.", "warning")
            return redirect(url_for("patient_dashboard"))
        
        doctor_id = request.form.get("doctor_id")
        appointment_date = request.form.get("date")
        time_slot = request.form.get("time_slot")
        
        if not all([doctor_id, appointment_date, time_slot]):
            flash("All appointment details are required.", "danger")
            return redirect(url_for("patient_dashboard"))
        
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            flash("Doctor not found.", "warning")
            return redirect(url_for("patient_dashboard"))
        
        appt_date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        
        if _doctor_slot_taken(int(doctor_id), appt_date_obj, time_slot):
            flash("This time slot is already booked. Please choose another.", "danger")
            return redirect(url_for("patient_dashboard"))

        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=int(doctor_id),
            date=appt_date_obj,
            time_slot=time_slot,
            status="Booked"
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        flash("Appointment booked successfully!", "success")
        return redirect(url_for("patient_dashboard"))

    @app.route("/appointment/<int:appt_id>/cancel", methods=["POST"])
    @role_required("patient")
    def cancel_appointment(appt_id):
        user = _current_user()
        patient = Patient.query.filter_by(user_id=user.id).first()
        appt = Appointment.query.get_or_404(appt_id)
        if appt.patient_id != patient.id:
            abort(403)
        appt.status = "Cancelled"
        db.session.commit()
        flash("Appointment cancelled.", "info")
        return redirect(url_for("patient_dashboard"))

    @app.route("/appointment/<int:appt_id>/reschedule", methods=["POST"])
    @role_required("patient")
    def reschedule_appointment(appt_id):
        user = _current_user()
        patient = Patient.query.filter_by(user_id=user.id).first()
        appt = Appointment.query.get_or_404(appt_id)
        if appt.patient_id != patient.id:
            abort(403)

        new_date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        new_slot = request.form["time_slot"].strip()

        if _doctor_slot_taken(appt.doctor_id, new_date, new_slot):
            flash("New slot is not available.", "danger")
            return redirect(url_for("patient_dashboard"))

        appt.date = new_date
        appt.time_slot = new_slot
        appt.status = "Booked"
        db.session.commit()
        flash("Appointment rescheduled.", "success")
        return redirect(url_for("patient_dashboard"))

    @app.route("/doctor/dashboard")
    @role_required("doctor")
    def doctor_dashboard():
        user = _current_user()
        doctor = Doctor.query.filter_by(user_id=user.id).first()
        
        if not doctor:
            flash("Doctor profile not found.", "warning")
            return redirect(url_for("home"))
        
        today = date.today()
        seven = today + timedelta(days=7)

        appts = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.date >= today,
            Appointment.date <= seven
        ).order_by(Appointment.date.asc()).all()
        
        return render_template("doctor_dasboard.html", doctor=doctor, appointments=appts, today=today)

    @app.route("/doctor/availability", methods=["GET", "POST"])
    @role_required("doctor")
    def doctor_availability():
        user = _current_user()
        doctor = Doctor.query.filter_by(user_id=user.id).first()
        
        if not doctor:
            flash("Doctor profile not found.", "warning")
            return redirect(url_for("home"))
        
        if request.method == "POST":
            for i in range(7):
                date_str = request.form.get(f"date_{i}")
                morning = request.form.get(f"morning_{i}", "").strip()
                afternoon = request.form.get(f"afternoon_{i}", "").strip()
                evening = request.form.get(f"evening_{i}", "").strip()
                
                avail_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                
                existing = DoctorAvailability.query.filter_by(
                    doctor_id=doctor.id,
                    date=avail_date
                ).first()
                
                if existing:
                    existing.morning_slot = morning if morning else None
                    existing.afternoon_slot = afternoon if afternoon else None
                    existing.evening_slot = evening if evening else None
                else:
                    if morning or afternoon or evening:
                        avail = DoctorAvailability(
                            doctor_id=doctor.id,
                            date=avail_date,
                            morning_slot=morning if morning else None,
                            afternoon_slot=afternoon if afternoon else None,
                            evening_slot=evening if evening else None
                        )
                        db.session.add(avail)
            
            db.session.commit()
            flash("Availability updated successfully!", "success")
            return redirect(url_for("doctor_availability"))
        
        today = date.today()
        saved_availability = DoctorAvailability.query.filter_by(doctor_id=doctor.id)\
            .filter(DoctorAvailability.date >= today)\
            .filter(DoctorAvailability.date <= today + timedelta(days=30))\
            .order_by(DoctorAvailability.date.asc()).all()
        
        return render_template("doctor_availability.html", 
                            today=today, 
                            timedelta=timedelta,
                            saved_availability=saved_availability)

    @app.route("/doctor/availability/<int:avail_id>/delete", methods=["POST"])
    @role_required("doctor")
    def delete_availability(avail_id):
        avail = DoctorAvailability.query.get_or_404(avail_id)
        user = _current_user()
        doctor = Doctor.query.filter_by(user_id=user.id).first()
        
        if avail.doctor_id != doctor.id:
            flash("Unauthorized access.", "danger")
            return redirect(url_for("doctor_availability"))
        
        db.session.delete(avail)
        db.session.commit()
        flash("Availability deleted successfully.", "success")
        return redirect(url_for("doctor_availability"))

    @app.route("/appointment/<int:appt_id>/complete", methods=["GET", "POST"])
    @role_required("doctor")
    def update_patient_history(appt_id):
        user = _current_user()
        doctor = Doctor.query.filter_by(user_id=user.id).first()
        appt = Appointment.query.get_or_404(appt_id)
        if appt.doctor_id != doctor.id:
            abort(403)
        patient = appt.patient

        if request.method == "POST":
            diagnosis = request.form.get("diagnosis", "")
            prescription = request.form.get("prescription", "")
            notes = request.form.get("notes", "")

            treat = Treatment.query.filter_by(appointment_id=appt.id).first()
            if not treat:
                treat = Treatment(appointment_id=appt.id, patient_id=patient.id)
                db.session.add(treat)
            treat.diagnosis = diagnosis
            treat.prescription = prescription
            treat.notes = notes
            treat.visit_date = date.today()

            appt.status = "Completed"
            db.session.commit()

            flash("Visit marked completed and history updated.", "success")
            return redirect(url_for("doctor_dashboard"))

        return render_template("update_patient_history.html", appointment=appt, patient=patient)

    @app.route("/appointment/<int:appt_id>/cancel_by_doctor", methods=["POST"])
    @role_required("doctor")
    def cancel_by_doctor(appt_id):
        user = _current_user()
        doctor = Doctor.query.filter_by(user_id=user.id).first()
        appt = Appointment.query.get_or_404(appt_id)
        if appt.doctor_id != doctor.id:
            abort(403)
        appt.status = "Cancelled"
        db.session.commit()
        flash("Appointment cancelled.", "info")
        return redirect(url_for("doctor_dashboard"))

    @app.route("/doctor/patient/<int:patient_id>/history")
    @role_required("doctor")
    def view_patient_history_by_doctor(patient_id):
        patient = Patient.query.get_or_404(patient_id)
        
        appointments = Appointment.query.filter_by(patient_id=patient.id)\
            .order_by(Appointment.date.desc()).all()
            
        treatments = Treatment.query.join(Appointment)\
            .filter(Appointment.patient_id == patient.id)\
            .order_by(Treatment.visit_date.desc()).all()
            
        return render_template("patient_history_doctor.html", 
                            patient=patient,
                            appointments=appointments,
                            treatments=treatments)

    @app.route("/patient/search_doctors")
    @role_required("patient")
    def patient_search_doctors():
        q = (request.args.get("q") or "").strip().lower()
        
        doctors = []
        if q:
            doctors = Doctor.query.join(Department)\
                .filter(
                    db.or_(
                        db.func.lower(Doctor.name).contains(q),
                        db.func.lower(Department.name).contains(q)
                    )
                ).all()
                
        return render_template("patient_search_doctors.html", doctors=doctors, query=q)
