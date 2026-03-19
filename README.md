# Predict_Rx - AI-Powered Medical Diagnostic Platform

A full-stack web application that uses Machine Learning to predict diseases from symptoms, featuring a "Doctor-in-the-loop" system for medication approval.

**Live Demo:** https://predict-rx.onrender.com

---

## 1. Project Overview

Predict_Rx is a web-based healthcare application designed to provide accessible, preliminary medical diagnoses. At its core, the platform utilizes a **Support Vector Classifier (SVC)** Machine Learning model to predict potential diseases based on user-reported symptoms. 

The application implements a secure, dual-role authentication system for Patients and Doctors. It ensures medical safety by requiring a registered doctor to review and approve any AI-suggested medications before they are revealed to the patient, creating a "Human-in-the-Loop" safety architecture.

## 2. Key Features

- **AI-Powered Disease Prediction:** Uses an SVC model to predict one of 41 diseases from 132 symptoms.
- **Dual-Role User System:** Separate login and dashboard experiences for Patients and Doctors.
- **Doctor Approval Workflow:** AI-suggested medications are locked until a doctor reviews and approves them.
- **Patient Consultation History:** Patients can view their past predictions and check the approval status of their medications.
- **Speech-to-Text Symptom Input:** Integrates the Web Speech API for hands-free symptom entry.
- **Smart Autocomplete:** A custom JavaScript feature suggests valid symptoms to prevent input errors.
- **Printable Medical Reports:** Generates a clean, printer-friendly report of the final diagnosis and approved medications.
- **Modern UI/UX:** Features a responsive design, smooth animations, and toast notifications for a professional user experience.

---

## 3. Technology Stack

| Category      | Technology                                       | Purpose                                                 |
|---------------|--------------------------------------------------|---------------------------------------------------------|
| **Backend**       | Python, Flask                                    | Core application logic, routing, and server management. |
| **Frontend**      | HTML, CSS, JavaScript, Bootstrap 5               | User interface, styling, and client-side interactions.  |
| **Database**      | PostgreSQL (Production), SQLite (Local)          | Storing user and consultation data.                     |
| **DB Hosting**    | Neon.tech                                        | Free, serverless PostgreSQL provider for production.    |
| **ORM**           | Flask-SQLAlchemy                                 | Interacting with the database using Python objects.     |
| **Authentication**| Flask-Login, Werkzeug Security                   | Managing user sessions and hashing passwords securely.  |
| **ML Library**    | Scikit-learn, Pandas, NumPy                      | Training the model and processing data.                 |
| **Deployment**    | Render, Gunicorn                                 | Hosting the application and serving it in production.   |

---

## 4. Local Setup & Installation

Follow these steps to run the project on your local machine.

### Prerequisites
- Python 3.x installed
- Git installed

### Step-by-Step Guide

**1. Clone the Repository**
Open your terminal or command prompt and run:
```sh
git clone https://github.com/YugantikMahapatra/Predict_Rx.git
cd Predict_Rx
```


**2. Create a Virtual Environment**
It's best practice to create a virtual environment to manage project dependencies.
```sh
# For Windows
python -m venv venv

# For macOS/Linux
python3 -m venv venv
```

**3. Activate the Virtual Environment**
```sh
# For Windows
venv\Scripts\activate

# For macOS/Linux
source venv/bin/activate
```
You will see `(venv)` at the beginning of your terminal prompt.

**4. Install Required Packages**
Install all the necessary libraries from the `requirements.txt` file.
```sh
pip install -r requirements.txt
```
> **Note:** If you see an error related to `gunicorn` on Windows, you can ignore it. Gunicorn is only used for deployment on Linux-based servers like Render.

**5. Run the Application**
Start the Flask development server.
```sh
python main.py
```
The application will create a local `clinic.db` file for your database and automatically create a default doctor account.

**6. Access the Application**
Open your web browser and navigate to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 5. Default Login Credentials

A default doctor account is created automatically when you first run the app. Use these credentials to access the Doctor Dashboard.

- **Username:** `doctor_admin`
- **Password:** `doctor123`

You can register new patient accounts through the website's registration page.
