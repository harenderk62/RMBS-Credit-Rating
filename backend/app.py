from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from fastapi.middleware.cors import CORSMiddleware
from models import init_db, SessionLocal, Mortgage, LoanType, PropertyType
from credit_rating import calculate_risk_score, calculate_rmbs_rating
from logging_config import get_logger
from contextlib import asynccontextmanager

# Set up logging
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    init_db()  # Initialize the database (creating tables, etc.)
    logger.info("Database initialized.")
    yield
    logger.info("Shutting down application...")

# Create an instance of FastAPI with lifespan event handler
app = FastAPI(lifespan=lifespan)

# Define allowed origins for CORS
origins = [
    # Frontend URL
    "http://localhost:3000",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model to validate the data when creating or updating a mortgage


class MortgageCreate(BaseModel):
    credit_score: int = Field(..., ge=0, le=850)
    loan_amount: float = Field(..., gt=0)
    property_value: float = Field(..., gt=0)
    annual_income: float = Field(..., gt=0)
    debt_amount: float = Field(..., ge=0)
    loan_type: LoanType
    property_type: PropertyType

    # field validator for the credit score field to ensure it's within the allowed range
    @field_validator("credit_score")
    def validate_credit_score(cls, v):
        if v < 0 or v > 850:
            raise ValueError("Credit score must be between 0 and 850")
        return v


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Route to create a new mortgage and calculate its risk score
@app.post("/mortgages", summary="Create a new mortgage and calculate its risk score")
def create_mortgage(mortgage_data: MortgageCreate, db=Depends(get_db)):
    # Log the received mortgage data
    logger.debug(f"Received mortgage data: {mortgage_data}")

    # Create a new mortgage record in the database
    new_mortgage = Mortgage(
        credit_score=mortgage_data.credit_score,
        loan_amount=mortgage_data.loan_amount,
        property_value=mortgage_data.property_value,
        annual_income=mortgage_data.annual_income,
        debt_amount=mortgage_data.debt_amount,
        loan_type=mortgage_data.loan_type,
        property_type=mortgage_data.property_type,
    )
    db.add(new_mortgage)
    db.commit()
    db.refresh(new_mortgage)  # Refresh the object to get the generated ID

    # Calculate the risk score based on the mortgage data
    risk_score = calculate_risk_score(new_mortgage)
    logger.info(
        f"Mortgage with ID {new_mortgage.id} created. Risk Score = {risk_score}")

    return {
        "message": "Mortgage created successfully",
        "mortgage_id": new_mortgage.id,
        "individual_risk_score": risk_score,
    }


# Route to retrieve all mortgages and their RMBS rating
@app.get("/mortgages", summary="Retrieve all mortgages and the overall RMBS rating")
def get_all_mortgages(db=Depends(get_db)):
    # Fetch all mortgage records from the database
    mortgages = db.query(Mortgage).all()

    if not mortgages:
        logger.warning("No mortgages found in the database.")
        return {
            "mortgages": [],
            "rmbs_rating": "N/A (No mortgages found)"
        }

    # Create a list of mortgages with their credit rating and other details
    mortgage_list = []
    for m in mortgages:
        # Calculate risk score and credit rating for each mortgage
        risk_score = calculate_risk_score(m)
        credit_rating = calculate_rmbs_rating(
            risk_score)
        mortgage_list.append({
            "id": m.id,
            "credit_score": m.credit_score,
            "loan_amount": m.loan_amount,
            "property_value": m.property_value,
            "annual_income": m.annual_income,
            "debt_amount": m.debt_amount,
            "loan_type": m.loan_type,
            "property_type": m.property_type,
            "created_at": m.created_at,
            "credit_rating": credit_rating
        })

    return {
        "mortgages": mortgage_list,
    }


# update an existing mortgage and recalculate its risk score
@app.put("/mortgages/{id}", summary="Update an existing mortgage and recalculate its risk score")
def update_mortgage(id: int, mortgage_data: MortgageCreate, db=Depends(get_db)):
    # Fetch the mortgage record by its ID
    mortgage = db.query(Mortgage).filter(Mortgage.id == id).first()
    if not mortgage:
        raise HTTPException(status_code=404, detail="Mortgage not found")

    # Update the mortgage fields with the new data
    mortgage.credit_score = mortgage_data.credit_score
    mortgage.loan_amount = mortgage_data.loan_amount
    mortgage.property_value = mortgage_data.property_value
    mortgage.annual_income = mortgage_data.annual_income
    mortgage.debt_amount = mortgage_data.debt_amount
    mortgage.loan_type = mortgage_data.loan_type
    mortgage.property_type = mortgage_data.property_type

    # Commit the changes to the database
    db.commit()
    db.refresh(mortgage)

    # Recalculate the risk score and credit rating after updating the mortgage
    risk_score = calculate_risk_score(mortgage)
    credit_rating = calculate_rmbs_rating(risk_score)
    logger.info(
        f"Mortgage with ID {mortgage.id} updated. New Risk Score = {credit_rating}")

    return {
        "message": "Mortgage updated successfully",
        "mortgage_id": mortgage.id,
        "individual_risk_score": credit_rating,
    }


# delete a mortgage by its ID
@app.delete("/mortgages/{id}", summary="Delete a mortgage")
def delete_mortgage(id: int, db=Depends(get_db)):
    # Fetch the mortgage record by its ID
    mortgage = db.query(Mortgage).filter(Mortgage.id == id).first()
    if not mortgage:
        raise HTTPException(status_code=404, detail="Mortgage not found")

    # Delete the mortgage from the database
    db.delete(mortgage)
    db.commit()  # Commit the transaction to remove the record
    logger.info(f"Mortgage with ID {id} deleted.")

    return {"message": "Mortgage deleted successfully"}
