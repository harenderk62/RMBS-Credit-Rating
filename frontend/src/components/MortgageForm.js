import React, { useState } from "react";

// Initial state for the form fields
const initialFormState = {
  credit_score: "",
  loan_amount: "",
  property_value: "",
  annual_income: "",
  debt_amount: "",
  loan_type: "fixed",
  property_type: "single_family",
};

function MortgageForm({ onAddMortgage }) {
  const [formData, setFormData] = useState(initialFormState);
  const [errors, setErrors] = useState({});

  // numeric Fields
  const numericFields = [
    { name: "credit_score", label: "Credit Score" },
    { name: "loan_amount", label: "Loan Amount" },
    { name: "property_value", label: "Property Value" },
    { name: "annual_income", label: "Annual Income" },
    { name: "debt_amount", label: "Debt Amount" },
  ];

  // select inputs fields
  const selectFields = [
    {
      name: "loan_type",
      label: "Loan Type",
      options: [
        { value: "fixed", label: "Fixed" },
        { value: "adjustable", label: "Adjustable" },
      ],
    },
    {
      name: "property_type",
      label: "Property Type",
      options: [
        { value: "single_family", label: "Single Family" },
        { value: "condo", label: "Condo" },
      ],
    },
  ];

  // Validate the form inputs
  const validate = () => {
    let newErrors = {};

    // Validate credit score: must be a number between 0 and 850
    const creditScore = parseInt(formData.credit_score, 10);
    if (isNaN(creditScore) || creditScore < 0 || creditScore > 850) {
      newErrors.credit_score = "Credit score must be between 0 and 850.";
    }

    // Validate numeric fields: must be positive numbers
    numericFields.forEach(({ name }) => {
      if (name === "credit_score") return;
      if (
        isNaN(parseFloat(formData[name])) ||
        parseFloat(formData[name]) <= 0
      ) {
        newErrors[name] = `${name.replace("_", " ")} must be greater than 0.`;
      }
    });

    // Validate debt amount: must be 0 or positive
    if (
      isNaN(parseFloat(formData.debt_amount)) ||
      parseFloat(formData.debt_amount) < 0
    ) {
      newErrors.debt_amount = "Debt amount must be 0 or a positive number.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form field changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value, // Update the specific field in the form data state
    }));
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;

    const dataToSend = {
      credit_score: parseInt(formData.credit_score, 10),
      loan_amount: parseFloat(formData.loan_amount),
      property_value: parseFloat(formData.property_value),
      annual_income: parseFloat(formData.annual_income),
      debt_amount: parseFloat(formData.debt_amount),
      loan_type: formData.loan_type,
      property_type: formData.property_type,
    };

    // POST call to send the mortgage data to the backend
    fetch("http://localhost:8000/mortgages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dataToSend),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to add mortgage");
        }
        return response.json();
      })
      .then(() => {
        alert(`Mortgage added successfully`);
        onAddMortgage(); // Refresh the list of mortgages in the parent component
        setFormData(initialFormState);
      })
      .catch((error) => {
        console.error("Error adding mortgage:", error);
        alert("There was an error adding the mortgage. Please try again.");
      });
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
      <h2>Add a New Mortgage</h2>
      {/* Render input fields for numeric values */}
      {numericFields.map(({ name, label }) => (
        <div key={name}>
          <label>{label}:</label>
          <input
            type="number"
            name={name}
            value={formData[name]}
            onChange={handleChange}
          />
          {errors[name] && <span style={{ color: "red" }}>{errors[name]}</span>}
        </div>
      ))}
      {/* Render select fields for loan type and property type */}
      {selectFields.map(({ name, label, options }) => (
        <div key={name}>
          <label>{label}:</label>
          <select name={name} value={formData[name]} onChange={handleChange}>
            {options.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
      ))}
      <button type="submit" style={{ marginTop: "10px" }}>
        Add Mortgage
      </button>
    </form>
  );
}

export default MortgageForm;
