from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False) # 'patient', 'doctor', or 'admin'
    is_verified = db.Column(db.Boolean, default=True) # Doctors require manual verification
    is_banned = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'is_verified': self.is_verified,
            'is_banned': self.is_banned
        }

class Consultation(db.Model):
    __tablename__ = 'consultations'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    symptoms = db.Column(db.String(500), nullable=False)
    predicted_disease = db.Column(db.String(150), nullable=False)
    ai_medications = db.Column(db.Text, nullable=False) # Stored as comma separated string
    doctor_medications = db.Column(db.Text, nullable=True) # Final approved meds
    patient_notes = db.Column(db.Text, nullable=True) # Extra info from patient
    status = db.Column(db.String(50), default='Pending') # 'Pending' or 'Approved'

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'assigned_doctor_id': self.assigned_doctor_id,
            'symptoms': self.symptoms,
            'predicted_disease': self.predicted_disease,
            'ai_medications': self.ai_medications,
            'doctor_medications': self.doctor_medications,
            'patient_notes': self.patient_notes,
            'status': self.status
        }
