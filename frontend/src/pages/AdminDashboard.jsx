import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [consultations, setConsultations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [statsRes, usersRes, consultsRes] = await Promise.all([
        axios.get('http://localhost:5000/api/admin/stats'),
        axios.get('http://localhost:5000/api/admin/users'),
        axios.get('http://localhost:5000/api/admin/consultations')
      ]);
      setStats(statsRes.data);
      setUsers(usersRes.data.users);
      setConsultations(consultsRes.data.consultations);
      setError('');
    } catch (err) {
      if (err.response?.status === 401 || err.response?.status === 403) {
        setError('Unauthorized access. Please log in as an administrator.');
      } else {
        setError('Failed to fetch dashboard data. Make sure the server is running.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleVerify = async (userId) => {
    try {
      await axios.post(`http://localhost:5000/api/admin/user/${userId}/verify`);
      fetchDashboardData(); // Refresh data
    } catch (err) {
      alert(err.response?.data?.message || 'Failed to verify user');
    }
  };

  const handleBan = async (userId) => {
    try {
      await axios.post(`http://localhost:5000/api/admin/user/${userId}/ban`);
      fetchDashboardData(); // Refresh data
    } catch (err) {
      alert(err.response?.data?.message || 'Failed to ban user');
    }
  };

  const handleExport = () => {
    window.location.href = 'http://localhost:5000/api/admin/export';
  };

  if (loading) return <div className="app-container text-center mt-5"><h4>Loading Dashboard...</h4></div>;
  if (error) return <div className="app-container text-center mt-5"><div className="error-message">{error}</div></div>;

  return (
    <div className="app-container">
      <div className="dashboard-title text-center">
        <h2>Admin Overview</h2>
        <p className="text-muted">Platform Statistics and User Management</p>
      </div>

      <div className="grid-2 mb-4" style={{ gap: '1rem', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
        <div className="result-section text-center" style={{ padding: '1.5rem', background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)', color: 'white' }}>
          <h4 style={{ color: 'rgba(255,255,255,0.8)' }}>Total Patients</h4>
          <h2 style={{ fontSize: '2.5rem', margin: '0.5rem 0', color: 'white' }}>{stats?.total_patients}</h2>
        </div>
        <div className="result-section text-center" style={{ padding: '1.5rem', background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', color: 'white' }}>
          <h4 style={{ color: 'rgba(255,255,255,0.8)' }}>Total Doctors</h4>
          <h2 style={{ fontSize: '2.5rem', margin: '0.5rem 0', color: 'white' }}>{stats?.total_doctors}</h2>
        </div>
        <div className="result-section text-center" style={{ padding: '1.5rem', background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', color: 'white' }}>
          <h4 style={{ color: 'rgba(255,255,255,0.8)' }}>Total Consultations</h4>
          <h2 style={{ fontSize: '2.5rem', margin: '0.5rem 0', color: 'white' }}>{stats?.total_consultations}</h2>
        </div>
        <div className="result-section text-center" style={{ padding: '1.5rem', background: 'linear-gradient(135deg, #f43f5e 0%, #e11d48 100%)', color: 'white' }}>
          <h4 style={{ color: 'rgba(255,255,255,0.8)' }}>Pending Approvals</h4>
          <h2 style={{ fontSize: '2.5rem', margin: '0.5rem 0', color: 'white' }}>{stats?.pending_cases}</h2>
        </div>
      </div>

      <div className="result-section mt-5" style={{ padding: '2rem' }}>
        <h3>Registered Users</h3>
        <div style={{ overflowX: 'auto', marginTop: '1rem' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #e2e8f0' }}>
                <th style={{ padding: '1rem' }}>ID</th>
                <th style={{ padding: '1rem' }}>Username</th>
                <th style={{ padding: '1rem' }}>Role</th>
                <th style={{ padding: '1rem' }}>Status</th>
                <th style={{ padding: '1rem', textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id} style={{ borderBottom: '1px solid #f1f5f9', opacity: u.is_banned ? 0.5 : 1 }}>
                  <td style={{ padding: '1rem' }}>{u.id}</td>
                  <td style={{ padding: '1rem', fontWeight: '500' }}>{u.username}</td>
                  <td style={{ padding: '1rem' }}>
                    <span className={`badge ${u.role === 'doctor' ? 'badge-success' : 'badge-warning'}`} style={{ backgroundColor: u.role === 'doctor' ? '#10b981' : '#6366f1' }}>
                      {u.role.toUpperCase()}
                    </span>
                  </td>
                  <td style={{ padding: '1rem' }}>
                    {u.is_banned ? (
                      <span className="text-danger"><i className="fas fa-ban"></i> Banned</span>
                    ) : u.role === 'doctor' && !u.is_verified ? (
                      <span className="text-warning"><i className="fas fa-clock"></i> Pending</span>
                    ) : (
                      <span className="text-success"><i className="fas fa-check-circle"></i> Active</span>
                    )}
                  </td>
                  <td style={{ padding: '1rem', textAlign: 'right' }}>
                    {u.role === 'doctor' && (
                      <button 
                        onClick={() => handleVerify(u.id)}
                        className="btn btn-sm" 
                        style={{ marginRight: '10px', backgroundColor: u.is_verified ? '#94a3b8' : '#10b981', color: 'white', padding: '0.4rem 0.8rem', borderRadius: '6px', border: 'none', cursor: 'pointer' }}
                      >
                        {u.is_verified ? 'Revoke Verification' : 'Verify Doctor'}
                      </button>
                    )}
                    <button 
                      onClick={() => handleBan(u.id)}
                      className="btn btn-sm"
                      style={{ backgroundColor: u.is_banned ? '#94a3b8' : '#ef4444', color: 'white', padding: '0.4rem 0.8rem', borderRadius: '6px', border: 'none', cursor: 'pointer' }}
                    >
                      {u.is_banned ? 'Unban' : 'Ban'}
                    </button>
                  </td>
                </tr>
              ))}
              {users.length === 0 && (
                <tr>
                  <td colSpan="3" className="text-center" style={{ padding: '2rem', color: '#94a3b8' }}>No users found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="result-section mt-5" style={{ padding: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3>Global Consultation Log</h3>
          <button onClick={handleExport} style={{ backgroundColor: '#0f172a', color: 'white', padding: '0.6rem 1.2rem', borderRadius: '8px', border: 'none', cursor: 'pointer', fontWeight: 'bold' }}>
            <i className="fas fa-download me-2"></i> Download Full CSV Audit
          </button>
        </div>
        <div style={{ overflowX: 'auto', marginTop: '1rem', maxHeight: '400px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
            <thead style={{ position: 'sticky', top: 0, backgroundColor: 'white', zIndex: 1 }}>
              <tr style={{ borderBottom: '2px solid #e2e8f0' }}>
                <th style={{ padding: '1rem' }}>ID</th>
                <th style={{ padding: '1rem' }}>Patient Name</th>
                <th style={{ padding: '1rem' }}>Assigned Doctor</th>
                <th style={{ padding: '1rem' }}>Predicted Disease</th>
                <th style={{ padding: '1rem' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {consultations.map(c => (
                <tr key={c.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                  <td style={{ padding: '1rem' }}>#{c.id}</td>
                  <td style={{ padding: '1rem', fontWeight: '500' }}>{c.patient_name}</td>
                  <td style={{ padding: '1rem', color: '#64748b' }}>Dr. {c.doctor_name}</td>
                  <td style={{ padding: '1rem', color: '#ef4444', fontWeight: '500' }}>{c.predicted_disease}</td>
                  <td style={{ padding: '1rem' }}>
                    <span className={`badge ${c.status === 'Approved' ? 'badge-success' : 'badge-warning'}`}>
                      {c.status}
                    </span>
                  </td>
                </tr>
              ))}
              {consultations.length === 0 && (
                <tr>
                  <td colSpan="4" className="text-center" style={{ padding: '2rem', color: '#94a3b8' }}>No consultations found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
