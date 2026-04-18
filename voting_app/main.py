from flask import Flask, render_template, request, redirect
from models import SessionLocal, Voter, create_tables
from config import Config
from logger import logger
import json

app = Flask(__name__, template_folder='templates')

@app.before_request
def initialize_db():
    """Initialize database tables on first request"""
    if not hasattr(app, 'db_initialized'):
        try:
            create_tables()
            app.db_initialized = True
            logger.info("Database tables initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")

@app.route('/')
def index():
    """Display voter registration form"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle voter registration"""
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            age = request.form.get('age', '').strip()
            city = request.form.get('city', '').strip()
            phone_number = request.form.get('phone_number', '').strip()

            # Validate required fields
            if not all([name, age, city, phone_number]):
                error_msg = "All fields are required"
                logger.error(f"Missing fields - Name: {name}, Age: {age}, City: {city}, Phone: {phone_number}")
                return render_template('error.html', error_message=error_msg), 400

            # Convert age to integer
            try:
                age = int(age)
            except ValueError:
                error_msg = "Age must be a valid number"
                logger.error(f"Invalid age format: {age}")
                return render_template('error.html', error_message=error_msg), 400

            # Age validation
            if age < 18:
                error_msg = f"You must be at least 18 years old to register. Your age is {age}."
                logger.error(f"Age validation failed for {name}: age={age}, city={city}, phone={phone_number}")
                return render_template('error.html', error_message=error_msg), 403

            # Save to database
            session = SessionLocal()
            try:
                voter = Voter(
                    name=name,
                    age=age,
                    city=city,
                    phone_number=phone_number
                )
                session.add(voter)
                session.commit()
                voter_id = voter.id

                # Log success
                logger.info(f"Voter registration successful - Name: {name}, Age: {age}, City: {city}, Phone: {phone_number}, ID: {voter_id}")

                return render_template('success.html',
                                     name=name,
                                     age=age,
                                     city=city,
                                     phone_number=phone_number)
            except Exception as db_error:
                session.rollback()
                logger.error(f"Database error during registration: {str(db_error)}")
                error_msg = "Database error occurred. Please try again."
                return render_template('error.html', error_message=error_msg), 500
            finally:
                session.close()

        except Exception as e:
            logger.error(f"Unexpected error during voter registration: {str(e)}")
            error_msg = "An unexpected error occurred. Please try again."
            return render_template('error.html', error_message=error_msg), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return "Page not found", 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return "Internal server error", 500

if __name__ == '__main__':
    app.run(debug=True)