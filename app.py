from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from config import *
from models.models import db, User, Department, Doctor, Patient, Appointment, DoctorAvailability, Treatment
from controllers.routes import init_routes

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

init_routes(app)

def init_database():
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(email='admin@hms.com').first()
        if not admin:
            admin = User(
                email='admin@hms.com',
                passhash=generate_password_hash('admin123'),
                role='admin',
                is_active=True,
                is_admin=True
            )
            db.session.add(admin)
            
            departments = [
                Department(name='Cardiology', overview='Heart and cardiovascular system'),
                Department(name='Orthopedics', overview='Bone and joint treatment'),
                Department(name='Pediatrics', overview='Child healthcare'),
                Department(name='Neurology', overview='Brain and nervous system'),
                Department(name='Oncology', overview='Cancer treatment'),
                Department(name='Dermatology', overview='Skin care')
            ]
            for dept in departments:
                db.session.add(dept)
            
            db.session.commit()
            
init_database()

if __name__ == '__main__':
    app.run(debug=True)