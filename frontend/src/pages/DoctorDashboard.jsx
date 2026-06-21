import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function DoctorDashboard() {
  const [pending, setPending] = useState([]);
  const [approved, setApproved] = useState([]);
  const [error, setError] = useState('');
  const [approvalMeds, setApprovalMeds] = useState({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5000/api/doctor/dashboard');
      setPending(response.data.pending);
      setApproved(response.data.approved);
      setError('');
    } catch (err) {
      if (err.response?.status === 403 && err.response?.data?.message?.includes('pending verification')) {
        setError('VerificationPending');
      } else if (err.response?.status === 403 || err.response?.status === 401) {
        navigate('/');
      } else {
        setError('Failed to load dashboard');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, [navigate]);

  const handleApprove = async (consultationId) => {
    const meds = approvalMeds[consultationId];
    if (!meds) {
      alert("Please enter approved medications.");
      return;
    }
    
    try {
      await axios.post(`http://localhost:5000/api/doctor/approve/${consultationId}`, {
        approved_medications: meds
      });
      fetchDashboard(); // Refresh lists
    } catch (err) {
      setError('Failed to approve consultation');
    }
  };

  const handleMedChange = (id, value) => {
    setApprovalMeds({ ...approvalMeds, [id]: value });
  };

  if (loading) return <div className="app-container text-center mt-5"><h4>Loading Dashboard...</h4></div>;
  
  if (error === 'VerificationPending') {
    return (
      <div className="app-container text-center mt-5">
        <div className="result-section warning-box" style={{ maxWidth: '600px', margin: '0 auto', padding: '3rem' }}>
          <i className="fas fa-user-clock" style={{ fontSize: '4rem', color: '#f59e0b', marginBottom: '1.5rem' }}></i>
          <h2>Account Pending Verification</h2>
          <p className="mt-3 text-muted">Your doctor account has been created successfully, but it is currently pending manual verification by an administrator. You will gain access to patient files once your medical credentials have been approved.</p>
        </div>
      </div>
    );
  }

  if (error) return <div className="app-container text-center mt-5"><div className="error-message">{error}</div></div>;

  return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">Doctor Dashboard</h2>
      
      <div className="dashboard-section">
        <h3>Pending Approvals ({pending.length})</h3>
        {pending.length === 0 ? <p>No pending consultations.</p> : (
          <div className="card-grid">
            {pending.map(c => (
              <div key={c.id} className="consultation-card pending-card">
                <h4>Patient: {c.patient_name}</h4>
                <p><strong>Symptoms:</strong> {c.symptoms}</p>
                {c.patient_notes && (
                  <div style={{ backgroundColor: '#f1f5f9', padding: '10px', borderRadius: '8px', margin: '10px 0', borderLeft: '4px solid #6366f1' }}>
                    <p style={{ margin: 0 }}><strong>Patient Notes:</strong> <em>"{c.patient_notes}"</em></p>
                  </div>
                )}
                <p><strong>AI Prediction:</strong> <span className="text-danger">{c.predicted_disease}</span></p>
                <p><strong>AI Medications:</strong> {c.ai_medications}</p>
                
                <div className="approval-form mt-3">
                  <input 
                    type="text" 
                    placeholder="Enter final approved medications"
                    value={approvalMeds[c.id] ?? c.ai_medications}
                    onChange={(e) => handleMedChange(c.id, e.target.value)}
                  />
                  <button onClick={() => handleApprove(c.id)} className="btn-success">Approve</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="dashboard-section mt-5">
        <h3>Recently Approved ({approved.length})</h3>
        <div className="card-grid">
          {approved.map(c => (
            <div key={c.id} className="consultation-card approved-card">
              <h4>Patient: {c.patient_name}</h4>
              <p><strong>Disease:</strong> {c.predicted_disease}</p>
              <p><strong>Approved Meds:</strong> {c.doctor_medications}</p>
              <span className="badge badge-success">Approved</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default DoctorDashboard;
