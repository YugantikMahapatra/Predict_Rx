import os
from flask import Flask, request, render_template, redirect, url_for, flash
import numpy as np
import pandas as pd
import pickle
import ast
from constants import symptoms_dict, diseases_list
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask application
app = Flask(__name__)

# ============================================================
# Database & Authentication Setup
# ============================================================
app.config['SECRET_KEY'] = 'your-super-secret-key-change-this' # Required for session management
# Use SQLite for local development, can be easily changed to Postgres later
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///clinic.db')
# Fix for Render Postgres URLs (postgres:// -> postgresql://)
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Where to redirect if not logged in

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False) # 'patient' or 'doctor'

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    predicted_disease = db.Column(db.String(150), nullable=False)
    ai_medications = db.Column(db.Text, nullable=False) # Stored as comma separated string
    doctor_medications = db.Column(db.Text, nullable=True) # Final approved meds
    status = db.Column(db.String(50), default='Pending') # 'Pending' or 'Approved'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize database tables (runs only once)
with app.app_context():
    db.create_all()
    # Create a default doctor account if none exists
    if not User.query.filter_by(username='doctor_admin').first():
        hashed_password = generate_password_hash('doctor123')
        new_doctor = User(username='doctor_admin', password=hashed_password, role='doctor')
        db.session.add(new_doctor)
        db.session.commit()

# ============================================================
# Load Datasets
# ============================================================
sym_des_df = pd.read_csv("datasets/symtoms_df.csv")
precautions_df = pd.read_csv("datasets/precautions_df.csv")
workout_df = pd.read_csv("datasets/workout_df.csv")
description_df = pd.read_csv("datasets/description.csv")
medications_df = pd.read_csv('datasets/medications.csv')
diets_df = pd.read_csv("datasets/diets.csv")

# ============================================================
# Load Machine Learning Model
# ============================================================
svc = pickle.load(open('models/svc.pkl','rb'))

# ============================================================
# Helper Functions
# ============================================================

def helper(dis):
    # Get Description
    desc = description_df[description_df['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    # Get Precautions
    pre = precautions_df[precautions_df['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    # Get Medications
    med = medications_df[medications_df['Disease'] == dis]['Medication']
    med = [ast.literal_eval(m) for m in med.values]
    if med:
        med = med[0]
    else:
        med = []

    # Get Diet
    die = diets_df[diets_df['Disease'] == dis]['Diet']
    die = [ast.literal_eval(d) for d in die.values]
    if die:
        die = die[0]
    else:
        die = []

    # Get Workout
    wrkout = workout_df[workout_df['disease'] == dis] ['workout']

    return desc,pre,med,die,wrkout

def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]

# ============================================================
# Authentication Routes
# ============================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'patient') # default to patient if not provided

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ============================================================
# Application Routes
# ============================================================

@app.route("/")
def index():
    return render_template("index.html", symptoms_list=list(symptoms_dict.keys()))

@app.route('/predict', methods=['GET', 'POST'])
@login_required # Require user to be logged in to predict
def home():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        
        if not symptoms or symptoms == "Symptoms":
            message = "Please either write symptoms or you have written misspelled symptoms"
            return render_template('index.html', message=message, symptoms_list=list(symptoms_dict.keys()))
        else:
            user_symptoms = [s.strip() for s in symptoms.split(',')]
            user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
            user_symptoms = [s for s in user_symptoms if s]

            if not user_symptoms:
                message = "Please select at least one symptom."
                return render_template('index.html', message=message, symptoms_list=list(symptoms_dict.keys()))
            
            try:
                predicted_disease = get_predicted_value(user_symptoms)
                dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)

                my_precautions = []
                for i in precautions[0]:
                    my_precautions.append(i)

                # Convert medications list to a string for database storage
                meds_str = ", ".join(medications)
                
                # Save the consultation to the database
                new_consultation = Consultation(
                    patient_id=current_user.id,
                    symptoms=", ".join(user_symptoms),
                    predicted_disease=predicted_disease,
                    ai_medications=meds_str
                )
                db.session.add(new_consultation)
                db.session.commit()

                flash('Prediction completed. Medications are pending doctor approval.', 'info')
                
                # Note: We are NOT passing medications to the template here anymore, 
                # or we pass a placeholder message instead.
                pending_message = ["Your AI suggested medications are awaiting doctor approval."]

                return render_template('index.html', predicted_disease=predicted_disease, dis_des=dis_des,
                                       my_precautions=my_precautions, medications=pending_message, my_diet=rec_diet,
                                       workout=workout, symptoms_list=list(symptoms_dict.keys()))
            except KeyError as e:
                message = f"Symptom not recognized: {e}. Please check spelling."
                return render_template('index.html', message=message, symptoms_list=list(symptoms_dict.keys()))
            except Exception as e:
                message = f"An error occurred: {e}"
                return render_template('index.html', message=message, symptoms_list=list(symptoms_dict.keys()))

    return render_template('index.html', symptoms_list=list(symptoms_dict.keys()))

@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    # Only allow doctors to access this page
    if current_user.role != 'doctor':
        flash('Access denied. Doctor privileges required.', 'danger')
        return redirect(url_for('index'))
    
    # Fetch all pending consultations
    pending_consultations = Consultation.query.filter_by(status='Pending').all()
    # Fetch all approved consultations
    approved_consultations = Consultation.query.filter_by(status='Approved').all()
    
    return render_template('doctor_dashboard.html', 
                           pending_consultations=pending_consultations,
                           approved_consultations=approved_consultations)

@app.route('/approve_medication/<int:consultation_id>', methods=['POST'])
@login_required
def approve_medication(consultation_id):
    if current_user.role != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
        
    consultation = Consultation.query.get_or_404(consultation_id)
    # The doctor can edit the medications in the form before approving
    approved_meds = request.form.get('approved_medications')
    
    if approved_meds:
        consultation.doctor_medications = approved_meds
        consultation.status = 'Approved'
        db.session.commit()
        flash(f'Consultation #{consultation_id} approved successfully.', 'success')
    
    return redirect(url_for('doctor_dashboard'))

@app.route('/my_history')
@login_required
def my_history():
    # Fetch history for the current logged-in patient
    my_consultations = Consultation.query.filter_by(patient_id=current_user.id).order_by(Consultation.id.desc()).all()
    return render_template('patient_history.html', consultations=my_consultations)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)