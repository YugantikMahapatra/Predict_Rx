import { useState, useEffect } from 'react';
import axios from 'axios';

function PatientHistory() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await axios.get('https://predict-rx.onrender.com/api/patient/history');
        setHistory(response.data.history);
      } catch (err) {
        setError('Failed to load history');
      }
    };
    fetchHistory();
  }, []);

  return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">My Consultation History</h2>
      {error && <div className="error-message">{error}</div>}
      
      {history.length === 0 ? (
        <p className="text-center mt-5">You have no past consultations.</p>
      ) : (
        <div className="history-list">
          {history.map(c => (
            <div key={c.id} className="history-card">
              <div className="history-header">
                <h3>{c.predicted_disease}</h3>
                <span className={`badge ${c.status === 'Approved' ? 'badge-success' : 'badge-warning'}`}>
                  {c.status}
                </span>
              </div>
              <div className="history-body">
                <p><strong>Symptoms:</strong> {c.symptoms}</p>
                {c.patient_notes && (
                  <p><strong>My Notes:</strong> {c.patient_notes}</p>
                )}
                {c.status === 'Approved' ? (
                  <div className="approved-meds">
                    <strong><i className="fas fa-check-circle"></i> Doctor Approved Medications:</strong>
                    <p>{c.doctor_medications}</p>
                  </div>
                ) : (
                  <p className="text-muted">Waiting for doctor review...</p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PatientHistory;
