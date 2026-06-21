from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import db, Consultation, User
from functools import wraps

doctor_bp = Blueprint('doctor_api', __name__)

def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'doctor':
            return jsonify({'message': 'Doctor access required.'}), 403
        if not getattr(current_user, 'is_verified', True):
            return jsonify({'message': 'Your doctor account is pending verification by an admin.'}), 403
        return f(*args, **kwargs)
    return decorated_function

@doctor_bp.route('/dashboard', methods=['GET'])
@login_required
@doctor_required
def dashboard():
    pending = Consultation.query.filter_by(status='Pending', assigned_doctor_id=current_user.id).all()
    approved = Consultation.query.filter_by(status='Approved', assigned_doctor_id=current_user.id).all()
    
    # Let's attach patient names to make the dashboard better
    def format_consultation(c):
        data = c.to_dict()
        patient = User.query.get(c.patient_id)
        data['patient_name'] = patient.username if patient else 'Unknown'
        return data
        
    return jsonify({
        'pending': [format_consultation(c) for c in pending],
        'approved': [format_consultation(c) for c in approved]
    }), 200

@doctor_bp.route('/approve/<int:consultation_id>', methods=['POST'])
@login_required
@doctor_required
def approve(consultation_id):
        
    consultation = Consultation.query.get_or_404(consultation_id)
    
    data = request.get_json()
    approved_meds = data.get('approved_medications')
    
    if approved_meds:
        consultation.doctor_medications = approved_meds
        consultation.status = 'Approved'
        db.session.commit()
        return jsonify({'message': 'Consultation approved successfully', 'consultation': consultation.to_dict()}), 200
        
    return jsonify({'message': 'Approved medications required'}), 400
