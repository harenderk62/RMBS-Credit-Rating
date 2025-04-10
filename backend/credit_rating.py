from models import Mortgage

# Calculate risk score based on martgage value


def calculate_risk_score(mortgage: Mortgage) -> int:
    risk_score = 0

    # LTV ratio
    ltv = mortgage.loan_amount / mortgage.property_value
    if ltv > 0.9:
        risk_score += 2
    elif ltv > 0.8:
        risk_score += 1

    # DTI ratio
    dti = mortgage.debt_amount / mortgage.annual_income
    if dti > 0.5:
        risk_score += 2
    elif dti > 0.4:
        risk_score += 1

    # Credit score
    if mortgage.credit_score >= 700:
        risk_score -= 1
    elif mortgage.credit_score < 650:
        risk_score += 1

    # Loan Type
    if mortgage.loan_type == "fixed":
        risk_score -= 1
    elif mortgage.loan_type == "adjustable":
        risk_score += 1

    # Property Type
    if mortgage.property_type == "condo":
        risk_score += 1

    return risk_score

# Calculate RMBS rating based on risk score


def calculate_rmbs_rating(risk_score: int) -> str:
    if risk_score <= 2:
        return "AAA"
    elif risk_score <= 5:
        return "BBB"
    else:
        return "C"
