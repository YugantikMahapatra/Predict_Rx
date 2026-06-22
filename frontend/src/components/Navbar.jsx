import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

// Ensure axios sends cookies with every request
axios.defaults.withCredentials = true;

function Navbar() {
  const navigate = useNavigate();
  // We will manage state properly later, for now let's build the UI
  const user = JSON.parse(localStorage.getItem('user'));

  const handleLogout = async () => {
    try {
      await axios.post('https://predict-rx.onrender.com/api/auth/logout');
    } catch (err) {
      console.error("Failed to logout on backend", err);
    } finally {
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          🏥 Predict_Rx
        </Link>
        
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-links">Home</Link>
          </li>
          
          {user ? (
            <>
              {user.role === 'admin' ? (
                <>
                  <li><Link to="/admin" className="nav-links">Overview</Link></li>
                  <li><span style={{ color: '#475569', fontWeight: '500' }}>Admin</span></li>
                  <li><button onClick={handleLogout} className="btn-logout">Logout</button></li>
                </>
              ) : user.role === 'doctor' ? (
                <>
                  <li><Link to="/doctor" className="nav-links">Dashboard</Link></li>
                  <li><span style={{ color: '#475569', fontWeight: '500' }}>Dr. {user.username}</span></li>
                  <li><button onClick={handleLogout} className="btn-logout">Logout</button></li>
                </>
              ) : (
                <>
                  <li><Link to="/history" className="nav-links">My History</Link></li>
                  <li><button onClick={handleLogout} className="btn-logout">Logout ({user.username})</button></li>
                </>
              )}
            </>
          ) : (
            <>
              <li className="nav-item">
                <Link to="/login" className="nav-links">Login</Link>
              </li>
              <li className="nav-item">
                <Link to="/register" className="nav-links">Register</Link>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
