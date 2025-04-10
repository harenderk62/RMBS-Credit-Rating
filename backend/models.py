import os
import enum
import pymysql
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine, Column, Integer, Float, Enum, TIMESTAMP, func, Index
)
from sqlalchemy.orm import sessionmaker, declarative_base
from pymysql import OperationalError

# Load environment variables
load_dotenv()

# database connection details
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "mortgage_db")

# Construct the database URL for SQLAlchemy
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# SQLAlchemy engine to connect to the database
engine = create_engine(DATABASE_URL, echo=False)

# session maker for handling database sessions
SessionLocal = sessionmaker(bind=engine)

# base class for model definitions in SQLAlchemy
Base = declarative_base()

# Enum for loan types


class LoanType(str, enum.Enum):
    fixed = "fixed"
    adjustable = "adjustable"

# Enum for property types


class PropertyType(str, enum.Enum):
    single_family = "single_family"
    condo = "condo"

# Mortgage model for the 'mortgages' table in the database


class Mortgage(Base):
    __tablename__ = "mortgages"

    # Column definitions for the Mortgage table
    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary key
    credit_score = Column(Integer, nullable=False)
    loan_amount = Column(Float, nullable=False)
    property_value = Column(Float, nullable=False)
    annual_income = Column(Float, nullable=False)
    debt_amount = Column(Float, nullable=False)
    loan_type = Column(Enum(LoanType), nullable=False)
    property_type = Column(Enum(PropertyType), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Indexing columns that are frequently queried
    __table_args__ = (
        Index('ix_credit_score', 'credit_score'),
        Index('ix_loan_type', 'loan_type'),
    )

# create the database if it doesn't exist


def create_database_if_not_exists():
    try:
        conn = pymysql.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
        result = cursor.fetchone()

        # If the database doesn't exist, create it
        if not result:
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database '{DB_NAME}' created.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

        # Close the cursor and the connection
        cursor.close()
        conn.close()

    except OperationalError as e:
        print(f"Error connecting to MySQL: {e}")

# Initialize the database by creating tables (if they don't already exist)


def init_db():
    create_database_if_not_exists()
    # Create the tables for all models defined using Base
    Base.metadata.create_all(bind=engine)
    print("Tables created if they didn't already exist.")
