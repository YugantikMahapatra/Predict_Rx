import csv
import io
from flask import Blueprint, jsonify, Response
from flask_login import login_required, current_user
from ..models import db, User, Consultation

admin_bp = Blueprint('admin_api', __name__)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'message': 'Admin access required.'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/stats', methods=['GET'])
@login_required
@admin_required
def get_stats():
    total_patients = User.query.filter_by(role='patient').count()
    total_doctors = User.query.filter_by(role='doctor').count()
    total_consultations = Consultation.query.count()
    pending_cases = Consultation.query.filter_by(status='Pending').count()
    
    return jsonify({
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_consultations': total_consultations,
        'pending_cases': pending_cases
    }), 200

@admin_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    users = User.query.filter(User.role != 'admin').all()
    return jsonify({
        'users': [u.to_dict() for u in users]
    }), 200

@admin_bp.route('/user/<int:user_id>/verify', methods=['POST'])
@login_required
@admin_required
def verify_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != 'doctor':
        return jsonify({'message': 'Only doctors require verification.'}), 400
    
    user.is_verified = not user.is_verified
    db.session.commit()
    return jsonify({'message': f"Doctor {'verified' if user.is_verified else 'unverified'} successfully.", 'user': user.to_dict()}), 200

@admin_bp.route('/user/<int:user_id>/ban', methods=['POST'])
@login_required
@admin_required
def ban_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        return jsonify({'message': 'Cannot ban an administrator.'}), 400
        
    user.is_banned = not user.is_banned
    db.session.commit()
    return jsonify({'message': f"User {'banned' if user.is_banned else 'unbanned'} successfully.", 'user': user.to_dict()}), 200

@admin_bp.route('/consultations', methods=['GET'])
@login_required
@admin_required
def get_consultations():
    consultations = Consultation.query.order_by(Consultation.id.desc()).all()
    
    result = []
    for c in consultations:
        data = c.to_dict()
        patient = User.query.get(c.patient_id)
        doctor = User.query.get(c.assigned_doctor_id) if c.assigned_doctor_id else None
        data['patient_name'] = patient.username if patient else 'Unknown'
        data['doctor_name'] = doctor.username if doctor else 'Unassigned'
        result.append(data)
        
    return jsonify({
        'consultations': result
    }), 200

@admin_bp.route('/export', methods=['GET'])
@login_required
@admin_required
def export_csv():
    consultations = Consultation.query.all()
    
    # Create in-memory CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['ID', 'Patient ID', 'Symptoms', 'Predicted Disease', 'AI Medications', 'Doctor Medications', 'Patient Notes', 'Status'])
    
    for c in consultations:
        writer.writerow([
            c.id, c.patient_id, c.symptoms, c.predicted_disease, 
            c.ai_medications, c.doctor_medications, c.patient_notes, c.status
        ])
        
    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=consultations_audit.csv"}
    )
