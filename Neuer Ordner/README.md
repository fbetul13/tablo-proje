# Students Management System

A full-stack JavaScript application for managing student records with a Node.js/Express backend and React frontend.

## Features

- ✅ Create, Read, Update, Delete (CRUD) operations for students
- ✅ PostgreSQL database integration
- ✅ Modern React frontend with responsive design
- ✅ RESTful API endpoints
- ✅ Form validation and error handling
- ✅ Real-time data updates
- ✅ Mobile-responsive design

## Tech Stack

### Backend
- **Node.js** - JavaScript runtime
- **Express.js** - Web framework
- **PostgreSQL** - Database
- **pg** - PostgreSQL client for Node.js
- **CORS** - Cross-origin resource sharing

### Frontend
- **React** - JavaScript library for building user interfaces
- **Axios** - HTTP client for API calls
- **CSS3** - Styling with modern CSS features

## Project Structure

```
students-app/
├── server.js              # Express server
├── package.json           # Backend dependencies
├── database.sql           # Database setup script
├── frontend/              # React application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── App.css        # Component styles
│   │   ├── index.js       # React entry point
│   │   └── index.css      # Global styles
│   └── package.json       # Frontend dependencies
└── README.md              # This file
```

## Prerequisites

- Node.js (v14 or higher)
- PostgreSQL (v12 or higher)
- npm or yarn package manager

## Installation & Setup

### 1. Database Setup

1. **Install PostgreSQL** if you haven't already
2. **Create a database** for the application
3. **Run the database setup script**:

```sql
-- Connect to your PostgreSQL database and run:
\i database.sql
```

Or copy and paste the contents of `database.sql` into your PostgreSQL client (like DBeaver).

### 2. Backend Setup

1. **Install backend dependencies**:
```bash
npm install
```

2. **Configure database connection**:
   Edit `server.js` and update the PostgreSQL connection settings:
   ```javascript
   const pool = new Pool({
     user: 'your_username',        // Your PostgreSQL username
     host: 'localhost',
     database: 'your_database',    // Your database name
     password: 'your_password',    // Your PostgreSQL password
     port: 5432,
   });
   ```

3. **Start the backend server**:
```bash
npm start
```

The server will run on `http://localhost:5000`

### 3. Frontend Setup

1. **Navigate to the frontend directory**:
```bash
cd frontend
```

2. **Install frontend dependencies**:
```bash
npm install
```

3. **Start the React development server**:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students` | Get all students |
| GET | `/api/students/:id` | Get a specific student |
| POST | `/api/students` | Create a new student |
| PUT | `/api/students/:id` | Update a student |
| DELETE | `/api/students/:id` | Delete a student |
| GET | `/api/health` | Health check endpoint |

## Usage

1. **View Students**: The application loads and displays all students in a table
2. **Add Student**: Fill out the form and click "Add Student"
3. **Edit Student**: Click the "Edit" button next to any student to modify their information
4. **Delete Student**: Click the "Delete" button to remove a student (with confirmation)

## Database Schema

```sql
CREATE TABLE students (
    id BIGINT PRIMARY KEY,
    lastname VARCHAR(50) NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0 AND age < 150)
);
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Verify PostgreSQL is running
   - Check connection credentials in `server.js`
   - Ensure the database exists

2. **Port Already in Use**:
   - Backend: Change port in `server.js` (line 108)
   - Frontend: React will automatically suggest an alternative port

3. **CORS Errors**:
   - Ensure the backend is running on port 5000
   - Check that CORS is properly configured in `server.js`

4. **Module Not Found Errors**:
   - Run `npm install` in both root and frontend directories
   - Clear node_modules and reinstall if needed

### Development Commands

```bash
# Backend development (with auto-restart)
npm run dev

# Frontend development
cd frontend && npm start

# Build frontend for production
cd frontend && npm run build
```

## Sample Data

The application comes with sample data:
- ID: 190765346, Name: sude kaya, Age: 24
- ID: 202136528, Name: melih demir, Age: 23
- ID: 210358402, Name: bilge kaya, Age: 22
- ID: 230975836, Name: ece ozdogan, Age: 20
- ID: 220218318, Name: betul eroglu, Age: 21

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [ISC License](LICENSE).