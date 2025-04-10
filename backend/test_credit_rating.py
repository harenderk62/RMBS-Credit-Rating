import pytest
from fastapi.testclient import TestClient
from app import app
from credit_rating import calculate_risk_score
from models import Mortgage, LoanType, PropertyType


# Use TestClient to make requests to your FastAPI app
client = TestClient(app)

# Unit Test for the credit rating algorithm


def test_calculate_risk_score_valid():
    mortgage = Mortgage(
        credit_score=750,
        loan_amount=200000,
        property_value=250000,
        annual_income=60000,
        debt_amount=10000,
        loan_type=LoanType.fixed,
        property_type=PropertyType.single_family,
    )

    risk_score = calculate_risk_score(mortgage)
    credit_rating = "AAA" if risk_score <= 2 else (
        "BBB" if risk_score <= 5 else "C")

    assert credit_rating == "AAA", f"Expected AAA, but got {credit_rating}"


def test_calculate_risk_score_high_risk():
    mortgage = Mortgage(
        credit_score=600,
        loan_amount=300000,
        property_value=250000,
        annual_income=40000,
        debt_amount=50000,
        loan_type=LoanType.adjustable,
        property_type=PropertyType.condo,
    )

    risk_score = calculate_risk_score(mortgage)
    credit_rating = "AAA" if risk_score <= 2 else (
        "BBB" if risk_score <= 5 else "C")

    assert credit_rating == "C", f"Expected C, but got {credit_rating}"


def test_calculate_risk_score_edge_case_low_credit_score():
    mortgage = Mortgage(
        credit_score=300,
        loan_amount=100000,
        property_value=120000,
        annual_income=30000,
        debt_amount=5000,
        loan_type=LoanType.fixed,
        property_type=PropertyType.single_family,
    )

    risk_score = calculate_risk_score(mortgage)
    credit_rating = "AAA" if risk_score <= 2 else (
        "BBB" if risk_score <= 5 else "C")

    assert credit_rating == "AAA", f"Expected AAA, but got {credit_rating}"


def test_calculate_risk_score_invalid_credit_score():
    mortgage = Mortgage(
        credit_score=1000,  # Invalid credit score
        loan_amount=150000,
        property_value=180000,
        annual_income=50000,
        debt_amount=20000,
        loan_type=LoanType.fixed,
        property_type=PropertyType.single_family,
    )

    try:
        risk_score = calculate_risk_score(mortgage)
    except ValueError as e:
        assert str(
            e) == "Credit score must be between 0 and 850", "Expected ValueError for invalid credit score"


def test_calculate_risk_score_negative_loan_amount():
    mortgage = Mortgage(
        credit_score=700,
        loan_amount=-50000,  # Invalid loan amount
        property_value=100000,
        annual_income=30000,
        debt_amount=10000,
        loan_type=LoanType.adjustable,
        property_type=PropertyType.condo,
    )

    try:
        risk_score = calculate_risk_score(mortgage)
    except ValueError as e:
        assert str(
            e) == "Loan amount must be greater than 0", "Expected ValueError for negative loan amount"


# FastAPI endpoint testing
@pytest.mark.parametrize("mortgage_data, expected_rating", [
    ({"credit_score": 750, "loan_amount": 200000, "property_value": 250000, "annual_income": 60000,
     "debt_amount": 10000, "loan_type": "fixed", "property_type": "single_family"}, "AAA"),
    ({"credit_score": 600, "loan_amount": 300000, "property_value": 250000, "annual_income": 40000,
     "debt_amount": 50000, "loan_type": "adjustable", "property_type": "condo"}, "C"),
    ({"credit_score": 300, "loan_amount": 100000, "property_value": 120000, "annual_income": 30000,
     "debt_amount": 5000, "loan_type": "fixed", "property_type": "single_family"}, "AAA"),
])
def test_create_mortgage_with_credit_rating(mortgage_data, expected_rating):
    response = client.post("/mortgages", json=mortgage_data)
    assert response.status_code == 200
    assert response.json()[
        "credit_rating"] == expected_rating, f"Expected {expected_rating}, but got {response.json()['credit_rating']}"


# Test handling of missing or incorrect data during mortgage creation
def test_create_mortgage_invalid_data():
    # Invalid data (credit_score > 850)
    invalid_data = {
        "credit_score": 900,  # Invalid credit score
        "loan_amount": 100000,
        "property_value": 150000,
        "annual_income": 50000,
        "debt_amount": 10000,
        "loan_type": "fixed",
        "property_type": "single_family",
    }

    response = client.post("/mortgages", json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity error


# Test edge cases where data might be missing or incorrect
def test_create_mortgage_missing_field():
    # Missing 'loan_amount' field
    missing_field_data = {
        "credit_score": 700,
        "property_value": 150000,
        "annual_income": 50000,
        "debt_amount": 10000,
        "loan_type": "fixed",
        "property_type": "single_family",
    }

    response = client.post("/mortgages", json=missing_field_data)
    assert response.status_code == 422  # Unprocessable Entity error
