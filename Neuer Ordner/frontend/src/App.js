import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [editingId, setEditingId] = useState(null);
  
  const [formData, setFormData] = useState({
    id: '',
    lastname: '',
    firstname: '',
    age: ''
  });

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/students`);
      setStudents(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch students. Please check if the server is running.');
      console.error('Error fetching students:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const resetForm = () => {
    setFormData({
      id: '',
      lastname: '',
      firstname: '',
      age: ''
    });
    setEditingId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (editingId) {
        // Update existing student
        await axios.put(`${API_BASE_URL}/students/${editingId}`, {
          lastname: formData.lastname,
          firstname: formData.firstname,
          age: parseInt(formData.age)
        });
        setSuccess('Student updated successfully!');
      } else {
        // Create new student
        await axios.post(`${API_BASE_URL}/students`, {
          id: parseInt(formData.id),
          lastname: formData.lastname,
          firstname: formData.firstname,
          age: parseInt(formData.age)
        });
        setSuccess('Student added successfully!');
      }
      
      resetForm();
      fetchStudents();
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'An error occurred';
      setError(errorMessage);
      setTimeout(() => setError(''), 5000);
    }
  };

  const handleEdit = (student) => {
    setFormData({
      id: student.id.toString(),
      lastname: student.lastname,
      firstname: student.firstname,
      age: student.age.toString()
    });
    setEditingId(student.id);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this student?')) {
      try {
        await axios.delete(`${API_BASE_URL}/students/${id}`);
        setSuccess('Student deleted successfully!');
        fetchStudents();
        setTimeout(() => setSuccess(''), 3000);
      } catch (err) {
        setError('Failed to delete student');
        setTimeout(() => setError(''), 5000);
      }
    }
  };

  const handleCancel = () => {
    resetForm();
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading students...</div>
      </div>
    );
  }

  return (
    <div className="container">
      <h1 className="header">Students Management System</h1>
      
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
      
      <div className="form-container">
        <h2 className="form-title">
          {editingId ? 'Edit Student' : 'Add New Student'}
        </h2>
        
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="id">ID:</label>
              <input
                type="number"
                id="id"
                name="id"
                value={formData.id}
                onChange={handleInputChange}
                disabled={editingId !== null}
                required={editingId === null}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="lastname">Last Name:</label>
              <input
                type="text"
                id="lastname"
                name="lastname"
                value={formData.lastname}
                onChange={handleInputChange}
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="firstname">First Name:</label>
              <input
                type="text"
                id="firstname"
                name="firstname"
                value={formData.firstname}
                onChange={handleInputChange}
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="age">Age:</label>
              <input
                type="number"
                id="age"
                name="age"
                value={formData.age}
                onChange={handleInputChange}
                min="1"
                max="120"
                required
              />
            </div>
          </div>
          
          <div className="action-buttons">
            <button type="submit" className="btn btn-primary">
              {editingId ? 'Update Student' : 'Add Student'}
            </button>
            {editingId && (
              <button type="button" className="btn btn-danger" onClick={handleCancel}>
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>
      
      <div className="table-container">
        {students.length === 0 ? (
          <div className="empty-state">
            <h3>No students found</h3>
            <p>Add your first student using the form above.</p>
          </div>
        ) : (
          <table className="students-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Last Name</th>
                <th>First Name</th>
                <th>Age</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {students.map((student) => (
                <tr key={student.id}>
                  <td>{student.id}</td>
                  <td>{student.lastname}</td>
                  <td>{student.firstname}</td>
                  <td>{student.age}</td>
                  <td>
                    <div className="action-buttons">
                      <button
                        className="btn btn-success"
                        onClick={() => handleEdit(student)}
                      >
                        Edit
                      </button>
                      <button
                        className="btn btn-danger"
                        onClick={() => handleDelete(student.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App; 