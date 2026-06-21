import os
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from .models import db, User

# Initialize Login Manager
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config.Config')
    
    # Initialize CORS for all domains, specifically allowing credentials (cookies) to be sent from React
    CORS(app, supports_credentials=True)
    
    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    
    # Set up database and default user
    with app.app_context():
        db.create_all()
        # Create a default doctor account if none exists
        if not User.query.filter_by(username='doctor_admin').first():
            new_doctor = User(username='doctor_admin', role='doctor')
            new_doctor.set_password('doctor123')
            db.session.add(new_doctor)
            db.session.commit()

        # Seed an admin account if none exists
        if not User.query.filter_by(role='admin').first():
            admin_user = User(username='admin', role='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Seeded default admin user: admin / admin123")

    # Import and Register Blueprints (Routes)
    # We will create these next!
    from .routes.auth_api import auth_bp
    from .routes.patient_api import patient_bp
    from .routes.doctor_api import doctor_bp
    from .routes.admin_api import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patient_bp, url_prefix='/api/patient')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    return app
