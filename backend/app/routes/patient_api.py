import sys
import os
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import db, Consultation, User
from ..services.ml_service import ml_service

# Add backend dir to path to import constants
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(basedir)
from constants import symptoms_dict

patient_bp = Blueprint('patient_api', __name__)

@patient_bp.route('/symptoms', methods=['GET'])
def get_symptoms():
    """Return list of all available symptoms for the frontend autocomplete"""
    return jsonify({'symptoms': list(symptoms_dict.keys())}), 200

@patient_bp.route('/predict', methods=['POST'])
@login_required
def predict():
    data = request.get_json()
    symptoms_list = data.get('symptoms', [])
    
    if not symptoms_list:
        return jsonify({'message': 'Please provide at least one symptom'}), 400
        
    try:
        predicted_disease = ml_service.get_predicted_value(symptoms_list)
        dis_des, precautions, medications, rec_diet, workout = ml_service.helper(predicted_disease)
        
        my_precautions = [i for i in precautions] if precautions else []
        meds_str = ", ".join(medications) if medications else ""
        
        # We no longer save the consultation here. It just returns the data.
        
        return jsonify({
            'message': 'Prediction completed. Medications pending doctor approval.',
            'disease': predicted_disease,
            'description': dis_des,
            'precautions': my_precautions,
            'diet': rec_diet,
            'workout': workout,
            'pending_medications': medications
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

@patient_bp.route('/doctors', methods=['GET'])
@login_required
def get_doctors():
    # Only return verified doctors
    doctors = User.query.filter_by(role='doctor', is_verified=True).all()
    return jsonify({
        'doctors': [{'id': d.id, 'username': d.username} for d in doctors]
    }), 200

@patient_bp.route('/submit', methods=['POST'])
@login_required
def submit_consultation():
    data = request.get_json()
    
    symptoms = data.get('symptoms')
    predicted_disease = data.get('predicted_disease')
    ai_medications = data.get('ai_medications')
    patient_notes = data.get('patient_notes')
    assigned_doctor_id = data.get('assigned_doctor_id')
    
    if not symptoms or not predicted_disease or not assigned_doctor_id:
        return jsonify({'message': 'Symptoms, prediction, and doctor selection are required'}), 400
        
    new_consultation = Consultation(
        patient_id=current_user.id,
        assigned_doctor_id=assigned_doctor_id,
        symptoms=symptoms,
        predicted_disease=predicted_disease,
        ai_medications=ai_medications,
        patient_notes=patient_notes,
        status='Pending'
    )
    db.session.add(new_consultation)
    db.session.commit()

    return jsonify({'message': 'Consultation submitted to doctor successfully.'}), 201

@patient_bp.route('/history', methods=['GET'])
@login_required
def history():
    consultations = Consultation.query.filter_by(patient_id=current_user.id).order_by(Consultation.id.desc()).all()
    return jsonify({
        'history': [c.to_dict() for c in consultations]
    }), 200
