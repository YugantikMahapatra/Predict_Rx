# PredictRx: AI-Assisted Healthcare Triage Platform

PredictRx is a modern, enterprise-grade healthcare application that utilizes Machine Learning to provide preliminary diagnoses based on patient symptoms. To ensure medical safety and compliance, the application employs a strict Role-Based Access Control (RBAC) system where AI predictions must be manually reviewed and approved by verified human doctors.

## 🌟 Core Architecture

The platform is split into two robust services:
1. **Frontend:** A responsive, glassmorphism-styled React.js application powered by Vite.
2. **Backend:** A RESTful Flask API that handles authentication, database management (SQLAlchemy), and Machine Learning inference (Scikit-Learn).

## 👥 Role-Based Access Control (RBAC)

PredictRx features a 3-tier security architecture to ensure medical safety:

### 1. Patients
- **Registration:** Anyone can register as a patient.
- **Workflow:** Patients select their symptoms from a searchable interface. The AI model instantly provides a preliminary diagnosis, recommended diet, and suggested medications.
- **Human Review:** Before the medications are "prescribed", the patient can add contextual notes. The consultation is then submitted to the global queue for doctor approval.
- **History:** Patients have a dedicated dashboard to view past consultations and see if their pending cases have been approved by a doctor.

### 2. Doctors
- **Registration & Verification:** Users can register as a Doctor, but they are placed in a **Pending Verification** lock-state. They cannot access patient data until an Admin verifies their medical credentials.
- **Dashboard:** Verified doctors have access to the global queue of pending consultations.
- **Approval Workflow:** Doctors review the patient's symptoms, the patient's custom notes, and the AI's preliminary diagnosis. The doctor can then edit, overwrite, or approve the final list of medications.

### 3. Administrators
- **Global Oversight:** Admins have access to a secure dashboard showing platform analytics (Total Patients, Doctors, and Pending Cases).
- **User Management:** Admins can verify pending doctor accounts or instantly ban malicious users.
- **Auditing:** Admins can view a live feed of all global consultations.
- **Data Export:** Admins can export the entire consultation history to a CSV file for legal auditing or HIPAA compliance tracking.

## 🚀 Key Technical Features

* **Machine Learning Integration:** Uses a trained Support Vector Classifier (SVC) pickled model to predict diseases based on a massive matrix of potential symptoms.
* **Modern UI/UX:** Built with React, featuring a custom premium CSS design system (glassmorphism cards, dynamic gradients, Outfit typography).
* **RESTful Architecture:** Clear separation of concerns. The Flask backend acts purely as a JSON API, making it perfectly suited for future deployment on Render, AWS, or Vercel.
* **Secure Authentication:** Cookie/Session-based authentication using Flask-Login and Werkzeug password hashing.

## 🛠️ Local Development Setup

### 1. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```
*The backend runs on `http://localhost:5000`.*
*Note: On the very first run, the SQLite database is generated automatically, and a default admin account is seeded (`admin` / `admin123`).*

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*The frontend runs on `http://localhost:5173`.*

## 🚢 Deployment Roadmap (Render + PostgreSQL)

To move this application from localhost to a live production environment:
1. **Database:** Swap the local SQLite `clinic.db` for a cloud PostgreSQL provider like **Neon** or **Supabase**. Update the `.env` `DATABASE_URL`.
2. **Backend:** Deploy the `backend` folder as a "Web Service" on Render.
3. **Frontend:** Update `axios` base URLs in React to point to the live Render backend URL, then deploy the `frontend` folder as a "Static Site" on Render.
4. **Cron Job:** Set up a free ping service (like cron-job.org) to hit the backend every 14 minutes to prevent Render's free tier from sleeping.
