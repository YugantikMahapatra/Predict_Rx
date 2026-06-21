import os
import numpy as np
import pandas as pd
import pickle
import ast
import sys

# Get the base directory (the `backend` folder)
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# We need to import constants from the backend directory
sys.path.append(basedir)
from constants import symptoms_dict, diseases_list

class MLService:
    def __init__(self):
        # Load Datasets
        self.sym_des_df = pd.read_csv(os.path.join(basedir, "datasets", "symtoms_df.csv"))
        self.precautions_df = pd.read_csv(os.path.join(basedir, "datasets", "precautions_df.csv"))
        self.workout_df = pd.read_csv(os.path.join(basedir, "datasets", "workout_df.csv"))
        self.description_df = pd.read_csv(os.path.join(basedir, "datasets", "description.csv"))
        self.medications_df = pd.read_csv(os.path.join(basedir, "datasets", "medications.csv"))
        self.diets_df = pd.read_csv(os.path.join(basedir, "datasets", "diets.csv"))
        
        # Load Machine Learning Model
        model_path = os.path.join(basedir, 'models', 'svc.pkl')
        self.svc = pickle.load(open(model_path, 'rb'))

    def helper(self, dis):
        # Get Description
        desc = self.description_df[self.description_df['Disease'] == dis]['Description']
        desc = " ".join([w for w in desc])

        # Get Precautions
        pre = self.precautions_df[self.precautions_df['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
        pre = [col for col in pre.values]
        if pre:
            pre = pre[0].tolist()
        else:
            pre = []

        # Get Medications
        med = self.medications_df[self.medications_df['Disease'] == dis]['Medication']
        med = [ast.literal_eval(m) for m in med.values]
        if med:
            med = med[0]
        else:
            med = []

        # Get Diet
        die = self.diets_df[self.diets_df['Disease'] == dis]['Diet']
        die = [ast.literal_eval(d) for d in die.values]
        if die:
            die = die[0]
        else:
            die = []

        # Get Workout
        wrkout = self.workout_df[self.workout_df['disease'] == dis]['workout'].tolist()

        return desc, pre, med, die, wrkout

    def get_predicted_value(self, patient_symptoms):
        input_vector = np.zeros(len(symptoms_dict))
        for item in patient_symptoms:
            if item in symptoms_dict:
                input_vector[symptoms_dict[item]] = 1
        prediction_index = self.svc.predict([input_vector])[0]
        return diseases_list[prediction_index]

# Instantiate the service so it's loaded once in memory
ml_service = MLService()
