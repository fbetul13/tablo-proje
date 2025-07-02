-- Students Management System Database Setup
-- Run this SQL in your PostgreSQL database

-- Create the students table
CREATE TABLE IF NOT EXISTS students (
    id BIGINT PRIMARY KEY,
    lastname VARCHAR(50) NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0 AND age < 150)
);

-- Insert sample data (your original data)
INSERT INTO students (id, lastname, firstname, age) VALUES
    (190765346, 'kaya', 'sude', 24),
    (202136528, 'demir', 'melih', 23),
    (210358402, 'kaya', 'bilge', 22),
    (230975836, 'ozdogan', 'ece', 20),
    (220218318, 'eroglu', 'betul', 21)
ON CONFLICT (id) DO NOTHING;

-- Create index for better performance
CREATE INDEX IF NOT EXISTS idx_students_lastname ON students(lastname);
CREATE INDEX IF NOT EXISTS idx_students_firstname ON students(firstname);

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON TABLE students TO your_username;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_username; 