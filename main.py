from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle
import ast
from constants import symptoms_dict, diseases_list

# Initialize Flask application
app = Flask(__name__)

# ============================================================
# Load Datasets
# ============================================================
# These CSV files contain the medical knowledge base for the application.
# They map diseases to their descriptions, precautions, medications, diets, and workouts.
sym_des_df = pd.read_csv("datasets/symtoms_df.csv")
precautions_df = pd.read_csv("datasets/precautions_df.csv")
workout_df = pd.read_csv("datasets/workout_df.csv")
description_df = pd.read_csv("datasets/description.csv")
medications_df = pd.read_csv('datasets/medications.csv')
diets_df = pd.read_csv("datasets/diets.csv")

# ============================================================
# Load Machine Learning Model
# ============================================================
# The SVC (Support Vector Classifier) model is pre-trained to predict diseases based on symptoms.
svc = pickle.load(open('models/svc.pkl','rb'))

# ============================================================
# Helper Functions
# ============================================================

def helper(dis):
    """
    Retrieves detailed information about a predicted disease.
    
    Args:
        dis (str): The name of the predicted disease.
        
    Returns:
        tuple: Contains description, precautions, medications, diet, and workout recommendations.
    """
    # Get Description
    desc = description_df[description_df['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    # Get Precautions
    pre = precautions_df[precautions_df['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    # Get Medications
    med = medications_df[medications_df['Disease'] == dis]['Medication']
    med = [ast.literal_eval(m) for m in med.values] # Convert string representation of list to actual list
    if med:
        med = med[0]
    else:
        med = []

    # Get Diet
    die = diets_df[diets_df['Disease'] == dis]['Diet']
    die = [ast.literal_eval(d) for d in die.values] # Convert string representation of list to actual list
    if die:
        die = die[0]
    else:
        die = []

    # Get Workout
    wrkout = workout_df[workout_df['disease'] == dis] ['workout']

    return desc,pre,med,die,wrkout

def get_predicted_value(patient_symptoms):
    """
    Predicts the disease based on a list of symptoms using the trained SVC model.
    
    Args:
        patient_symptoms (list): A list of symptom strings.
        
    Returns:
        str: The predicted disease name.
    """
    input_vector = np.zeros(len(symptoms_dict))
    # Map the patient's symptoms to the input vector expected by the model
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]

# ============================================================
# Application Routes
# ============================================================

@app.route("/")
def index():
    """
    Renders the home page with the symptom input form.
    Passes the list of all available symptoms to the template for autocomplete.
    """
    return render_template("index.html", symptoms_list=list(symptoms_dict.keys()))

@app.route('/predict', methods=['GET', 'POST'])
def home():
    """
    Handles the prediction logic.
    Accepts POST requests with symptom data, predicts the disease, and renders the results.
    """
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        
        # Validate input: Check if symptoms are empty or just the placeholder text
        if not symptoms or symptoms == "Symptoms":
            message = "Please either write symptoms or you have written misspelled symptoms"
            return render_template('index.html', message=message, symptoms_list=list(symptoms_dict.keys()))
        else:
            # Process the input string into a list of symptoms
            # Split by comma and strip whitespace
            user_symptoms = [s.strip() for s in symptoms.split(',')]
            # Remove any extra characters like brackets or quotes if present
            user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
            # Filter out empty strings (e.g. from trailing commas)
            user_symptoms = [s for s in user_symptoms if s]

            if not user_symptoms:
                message = "Please select at least one symptom."
                return render_template('index.html', message=message, symptoms_list=list(symptoms_dict.keys()))
            
            try:
                # Predict the disease
                predicted_disease = get_predicted_value(user_symptoms)
                
                # Fetch detailed information about the disease
                dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)

                # Flatten precautions list
                my_precautions = []
                for i in precautions[0]:
                    my_precautions.append(i)

                # Render the template with all the results
                return render_template('index.html', predicted_disease=predicted_disease, dis_des=dis_des,
                                       my_precautions=my_precautions, medications=medications, my_diet=rec_diet,
                                       workout=workout, symptoms_list=list(symptoms_dict.keys()))
            except KeyError as e:
                # Handle cases where a symptom is not found in the dictionary
                message = f"Symptom not recognized: {e}. Please check spelling."
                return render_template('index.html', message=message, symptoms_list=list(symptoms_dict.keys()))
            except Exception as e:
                # Handle any other unexpected errors
                message = f"An error occurred: {e}"
                return render_template('index.html', message=message, symptoms_list=list(symptoms_dict.keys()))

    return render_template('index.html', symptoms_list=list(symptoms_dict.keys()))

@app.route('/about')
def about():
    """Renders the About Us page."""
    return render_template("about.html")

@app.route('/contact')
def contact():
    """Renders the Contact Us page."""
    return render_template("contact.html")

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)