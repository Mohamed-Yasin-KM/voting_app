# Voting App

A Flask-based voting application that collects voter information with age validation and PostgreSQL database integration.

## Features

- User registration form with name, age, city, and phone number
- Age validation (must be 18 or older)
- PostgreSQL database integration
- Error and success logging
- Clean, responsive UI

## Requirements

- Python 3.12+
- PostgreSQL database
- pip or uv package manager

## Installation

1. **Clone the repository**
   ```bash
   cd gitops
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Configure environment variables**
   
   Copy `.env.example` to `.env` and update with your PostgreSQL credentials:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your database configuration:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=voting_app
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

4. **Create PostgreSQL database**
   ```bash
   createdb voting_app
   ```

## Running the Application

```bash
python voting_app/main.py
```

The application will start on `http://localhost:5000`

## Project Structure

```
voting_app/
├── main.py                 # Flask application & routes
├── config.py              # Configuration management
├── logger.py              # Logging setup
├── models.py              # Database models
├── __init__.py            # Package initialization
└── templates/
    ├── index.html         # Registration form
    ├── success.html       # Success confirmation page
    └── error.html         # Error message page
```

## How It Works

1. **User accesses** `http://localhost:5000` and sees the registration form
2. **User enters** name, age, city, and phone number
3. **Form validation**:
   - If age < 18: Shows error page and logs to `logs/error.log`
   - If age >= 18: Saves to database and shows success page, logs to `logs/success.log`
4. **Database**: User data is stored in PostgreSQL `voters` table
5. **Logging**: All events are logged with timestamps

## Logging

The application creates two log files in the `logs/` directory:

- **error.log**: Contains all error events (age validation failures, database errors, etc.)
- **success.log**: Contains all successful voter registrations

Each log entry includes:
- Timestamp
- Log level (ERROR, INFO)
- User information
- Event details

## Database Schema

The `voters` table contains:
- `id`: Primary key
- `name`: Voter's full name
- `age`: Voter's age
- `city`: Voter's city
- `phone_number`: Voter's phone number
- `created_at`: Registration timestamp

## Error Handling

- **Age < 18**: User sees error message "You must be at least 18 years old to register"
- **Missing fields**: Form validation requires all fields
- **Invalid age**: Age must be a valid number
- **Database errors**: Handled gracefully with error logging

## Development

The application uses:
- **Flask** for web framework
- **SQLAlchemy** for ORM
- **psycopg2** for PostgreSQL connection
- **python-dotenv** for environment management
