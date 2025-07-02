const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');

const app = express();
app.use(cors());
app.use(express.json());

// PostgreSQL connection configuration
// Update these values according to your database setup
const pool = new Pool({
  user: 'postgres', // Change to your PostgreSQL username
  host: 'localhost',
  database: 'your_database_name', // Change to your database name
  password: 'your_password', // Change to your PostgreSQL password
  port: 5432,
});

// Test database connection
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('Database connection error:', err);
  } else {
    console.log('Database connected successfully');
  }
});

// Get all students
app.get('/api/students', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM students ORDER BY id');
    res.json(result.rows);
  } catch (err) {
    console.error('Error fetching students:', err);
    res.status(500).json({ error: 'Failed to fetch students' });
  }
});

// Get a single student by ID
app.get('/api/students/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query('SELECT * FROM students WHERE id = $1', [id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Student not found' });
    }
    
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error fetching student:', err);
    res.status(500).json({ error: 'Failed to fetch student' });
  }
});

// Add a new student
app.post('/api/students', async (req, res) => {
  try {
    const { id, lastname, firstname, age } = req.body;
    
    // Validate required fields
    if (!id || !lastname || !firstname || !age) {
      return res.status(400).json({ error: 'All fields are required' });
    }
    
    const result = await pool.query(
      'INSERT INTO students (id, lastname, firstname, age) VALUES ($1, $2, $3, $4) RETURNING *',
      [id, lastname, firstname, age]
    );
    
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error('Error creating student:', err);
    if (err.code === '23505') { // Unique violation
      res.status(400).json({ error: 'Student with this ID already exists' });
    } else {
      res.status(500).json({ error: 'Failed to create student' });
    }
  }
});

// Update a student
app.put('/api/students/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { lastname, firstname, age } = req.body;
    
    // Validate required fields
    if (!lastname || !firstname || !age) {
      return res.status(400).json({ error: 'All fields are required' });
    }
    
    const result = await pool.query(
      'UPDATE students SET lastname = $1, firstname = $2, age = $3 WHERE id = $4 RETURNING *',
      [lastname, firstname, age, id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Student not found' });
    }
    
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error updating student:', err);
    res.status(500).json({ error: 'Failed to update student' });
  }
});

// Delete a student
app.delete('/api/students/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query('DELETE FROM students WHERE id = $1 RETURNING *', [id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Student not found' });
    }
    
    res.json({ message: 'Student deleted successfully' });
  } catch (err) {
    console.error('Error deleting student:', err);
    res.status(500).json({ error: 'Failed to delete student' });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Server is running' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`Students API: http://localhost:${PORT}/api/students`);
}); 