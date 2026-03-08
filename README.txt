Predict_Rx - Health Care Center
=================================

This is a Machine Learning based web application that predicts potential diseases based on user-inputted symptoms. It provides a comprehensive report including disease description, precautions, medications, recommended diets, and workouts.

Prerequisites
-------------
Ensure you have Python installed on your system.

Installation
------------
1. Open a terminal or command prompt in the project directory.
2. Install the required Python libraries using pip:

   pip install -r requirements.txt

Running the Application
-----------------------
1. Run the main application file:

   python main.py

2. Once the server starts, open your web browser and navigate to:

   http://127.0.0.1:5000/

Usage
-----
1. On the home page, start typing symptoms in the input box (e.g., "itching", "headache").
2. Select symptoms from the dropdown list that appears.
3. Alternatively, click the "Start Speech Recognition" button and speak your symptoms clearly.
4. Click "Predict Disease" to see the results.
5. Use the colored buttons to toggle between different information sections (Disease, Description, Precaution, etc.).

Project Structure
-----------------
- main.py: The main Flask application file containing routes and logic.
- templates/: Contains HTML files for the frontend.
- static/: Contains static assets like images and CSS.
- datasets/: Contains the CSV files used for the knowledge base.
- models/: Contains the pre-trained Machine Learning model (svc.pkl).
- constants.py: Contains dictionaries mapping symptoms to indices.
