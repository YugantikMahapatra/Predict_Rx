import { useState, useEffect } from 'react';
import axios from 'axios';

function Home() {
  const [symptomsList, setSymptomsList] = useState([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [patientNotes, setPatientNotes] = useState('');
  const [submitSuccess, setSubmitSuccess] = useState('');
  const [doctors, setDoctors] = useState([]);
  const [selectedDoctorId, setSelectedDoctorId] = useState('');

  const user = JSON.parse(localStorage.getItem('user'));

  useEffect(() => {
    // Fetch available symptoms and verified doctors
    const fetchData = async () => {
      try {
        const [symptomsRes, doctorsRes] = await Promise.all([
          axios.get('http://localhost:5000/api/patient/symptoms'),
          axios.get('http://localhost:5000/api/patient/doctors')
        ]);
        setSymptomsList(symptomsRes.data.symptoms);
        setDoctors(doctorsRes.data.doctors);
      } catch (err) {
        console.error("Failed to load data", err);
      }
    };
    fetchData();
  }, []);

  const handlePredict = async (e) => {
    e.preventDefault();
    if (!user) {
      setError('You must be logged in to make a prediction.');
      return;
    }
    
    setLoading(true);
    setError('');
    setSubmitSuccess('');
    setPrediction(null);
    
    // Parse symptoms (assuming comma-separated for simplicity)
    const symptomsArray = selectedSymptoms.split(',').map(s => s.trim()).filter(s => s !== '');
    
    try {
      const response = await axios.post('http://localhost:5000/api/patient/predict', {
        symptoms: symptomsArray
      });
      setPrediction(response.data);
    } catch (err) {
      if (err.response?.status === 401) {
        setError('Your session has expired. Please log out and log in again.');
      } else {
        setError(err.response?.data?.message || 'Prediction failed. Make sure symptoms are spelled correctly.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitToDoctor = async () => {
    if (!selectedDoctorId) {
      setError('Please select a doctor to assign this consultation to.');
      return;
    }

    try {
      const symptomsArray = selectedSymptoms.split(',').map(s => s.trim()).filter(s => s !== '');
      await axios.post('http://localhost:5000/api/patient/submit', {
        symptoms: symptomsArray.join(', '),
        predicted_disease: prediction.disease,
        ai_medications: prediction.pending_medications.join(', '),
        patient_notes: patientNotes,
        assigned_doctor_id: selectedDoctorId
      });
      setSubmitSuccess('Consultation successfully submitted to the doctor for review!');
      setPrediction(null); // Clear prediction after submission
      setSelectedSymptoms('');
      setPatientNotes('');
    } catch (err) {
      if (err.response?.status === 401) {
        setError('Your session has expired. Please log out and log in again.');
      } else {
        setError(err.response?.data?.message || 'Failed to submit consultation.');
      }
    }
  };

  return (
    <div className="home-container">
      <div className="hero-section text-center">
        <h1 className="hero-title">PredictRx Health Assistant</h1>
        <p className="hero-subtitle">Get an instant AI preliminary analysis, seamlessly sent to our verified doctors for professional review.</p>
      </div>

      <div className="prediction-card">
        <form onSubmit={handlePredict}>
          <div className="form-group">
            <label>Select Symptoms (comma separated)</label>
            <input 
              type="text" 
              className="symptoms-input"
              value={selectedSymptoms} 
              onChange={(e) => setSelectedSymptoms(e.target.value)} 
              placeholder="e.g., itching, skin_rash, stomach_pain"
              disabled={!user}
            />
            {!user && <small className="text-warning">Please login to predict</small>}
          </div>
          
          <button type="submit" className="btn-primary btn-predict" disabled={loading || !user}>
            {loading ? 'Analyzing...' : 'Predict Disease'}
          </button>
        </form>
        
        {error && <div className="error-message mt-4">{error}</div>}
      </div>

      {prediction && (
        <div className="results-container mt-5">
          <h2 className="text-center mb-4">AI Prediction Results</h2>
          
          <div className="result-section disease-box">
            <h3>Predicted Disease</h3>
            <p className="disease-name">{prediction.disease}</p>
          </div>
          
          <div className="result-section">
            <h3>Description</h3>
            <p>{prediction.description}</p>
          </div>
          
          <div className="grid-2">
            <div className="result-section">
              <h3>Precautions</h3>
              <ul>
                {prediction.precautions.map((p, idx) => (
                  <li key={idx}>{p}</li>
                ))}
              </ul>
            </div>
            
            <div className="result-section warning-box">
              <h3>Medications</h3>
              <p>Status: <span className="text-warning">AI Suggested (Not Yet Approved)</span></p>
              <ul>
                {prediction.pending_medications.map((m, idx) => (
                  <li key={idx}>{m}</li>
                ))}
              </ul>
            </div>
          </div>
          
          {/* New Patient Notes Section */}
          <div className="result-section mt-4">
            <h3>Consultation Submission</h3>
            
            <div className="form-group mb-3 text-start">
              <label><strong>Assign to Doctor:</strong></label>
              <select 
                className="form-control mt-1 p-2" 
                value={selectedDoctorId} 
                onChange={(e) => setSelectedDoctorId(e.target.value)}
                style={{ borderRadius: '8px', border: '2px solid #e2e8f0', width: '100%', outline: 'none' }}
              >
                <option value="">-- Select a Verified Doctor --</option>
                {doctors.map(doc => (
                  <option key={doc.id} value={doc.id}>Dr. {doc.username}</option>
                ))}
              </select>
            </div>

            <label className="text-start d-block mt-3"><strong>Extra Notes for the Doctor:</strong></label>
            <textarea 
              className="form-control w-100 p-3 mt-1" 
              rows="4" 
              placeholder="e.g. I felt this after eating seafood yesterday..."
              value={patientNotes}
              onChange={(e) => setPatientNotes(e.target.value)}
              style={{ borderRadius: '8px', border: '2px solid #e2e8f0', width: '100%', outline: 'none' }}
            ></textarea>
            
            <button onClick={handleSubmitToDoctor} className="btn-primary mt-3" style={{ background: '#10b981', width: '100%' }}>
              <i className="fas fa-paper-plane me-2"></i> Submit to Doctor for Review
            </button>
          </div>
        </div>
      )}
      
      {submitSuccess && (
        <div className="alert alert-success mt-4" style={{ backgroundColor: '#d1fae5', color: '#065f46', padding: '1rem', borderRadius: '12px', textAlign: 'center', border: '1px solid #34d399' }}>
          <strong>Success!</strong> {submitSuccess}
          <br/>
          <a href="/history" className="btn btn-sm btn-dark mt-2">View My History</a>
        </div>
      )}

      {/* Professional Medical Disclaimer */}
      <div className="disclaimer-alert mt-5">
        <p><strong><i className="fas fa-shield-alt"></i> Medical Disclaimer:</strong> This AI prediction tool is for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always submit your results for doctor review and consult a qualified healthcare provider.</p>
      </div>
    </div>
  );
}

export default Home;
