> **Mortgage Application**

> **Introduction**

This is a full-stack mortgage application with the following functionalities:

Create, update, delete, and retrieve mortgage records.
Calculate a mortgage's risk score and credit rating based on certain borrower data.
I have uses FastAPI for the backend, React for the frontend, and MySQL for database storage.

> **Backend Setup**

Installation
Clone the repository

Create a virtual environment:
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Set up environment variables: Create a .env file with the following contents:

DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_NAME=mortgage_db
LOG_LEVEL=INFO
LOG_FILE=app.log
Install MySQL (if not already installed):

> **Running the Backend**

Run the FastAPI application:
uvicorn app:app --reload
This will start the backend on http://localhost:8000.

API Documentation: You can access the automatically generated API documentation using Swagger at:
http://localhost:8000/docs

> **Frontend Setup**

Installation
Clone the repository

Install dependencies:
npm install

Start the React development server:
npm start
The frontend will be available at http://localhost:3000.

Frontend Requirements:

Ensure the backend is running before starting the frontend.

> **Database Setup**

MySQL Database Setup
Create Database: The database will be automatically created if it doesn't exist when the backend runs. Ensure that you have MySQL running locally, or provide the correct database configuration in the .env file.

Tables: The Mortgage table is created on application startup if it doesn’t already exist.

Key Technical Decisions

Database Design:
We used SQLAlchemy as the ORM to interact with the MySQL database. This allows us to easily manage models and perform CRUD operations.
Enum types (LoanType and PropertyType) are used to limit the values for loan type and property type, ensuring data integrity.

Performance Optimizations:
Database indexing was implemented on frequently queried columns (credit_score, loan_type) to speed up data retrieval.
Connection pooling is enabled with SQLAlchemy to efficiently manage database connections.

> Logging:

Structured logging is implemented using Python's logging module, allowing both file and console logging with detailed timestamps, log levels, and log messages.

Design Decisions
Modular Design:
The backend code is split into several modules for clarity and maintainability:
app.py contains the FastAPI application and route handlers.
models.py defines the database schema and ORM classes.
credit_rating.py calculates the mortgage risk score and RMBS rating.
logging_config.py handles logging configuration.

Frontend Components:
The frontend is built using React, and it is divided into modular components such as MortgageForm and MortgageList for maintaining clean, reusable code.
Data validation and error handling are implemented to ensure user inputs are valid before submitting.

Error Handling:
Proper error handling is in place for both frontend and backend. The backend raises appropriate HTTP exceptions when records are not found or when invalid data is received. The frontend handles these errors gracefully and provides feedback to users.

API Documentation:
FastAPI automatically generates Swagger and ReDoc API documentation for the backend, making it easy for developers to test and interact with the API directly.

> **Testing**

Backend Testing
We use pytest for testing the backend API and business logic. Tests are written to ensure the application works correctly with various inputs, including valid and invalid data. The test cases validate the logic for creating, updating, and deleting mortgages, as well as the credit rating calculation.

1. Install Test Dependencies
   Install pytest and related dependencies:

pip install pytest pytest-asyncio
Test Directory Structure: The backend tests are located in the backend directory. The core test file is test_credit_rating.py, which contains the unit tests for the mortgage calculation logic and the API tests for creating, updating, and deleting mortgages.

To run the backend tests, execute the following command in your terminal: pytest test_credit_rating.py

Additional Notes:
Ensure you have MySQL installed and running locally.
You can adjust database credentials and API secrets through the .env file.
