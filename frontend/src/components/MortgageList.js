import React, { useState } from "react";

// Configuration for all the fields in the form (both for displaying and editing)
const fields = [
  { name: "credit_score", label: "Credit Score", type: "number" },
  { name: "loan_amount", label: "Loan Amount", type: "number" },
  { name: "property_value", label: "Property Value", type: "number" },
  { name: "annual_income", label: "Annual Income", type: "number" },
  { name: "debt_amount", label: "Debt Amount", type: "number" },
  {
    name: "loan_type",
    label: "Loan Type",
    type: "select",
    options: ["fixed", "adjustable"],
  },
  {
    name: "property_type",
    label: "Property Type",
    type: "select",
    options: ["single_family", "condo"],
  },
];

const MortgageList = ({ mortgages, refreshMortgages }) => {
  const [editingId, setEditingId] = useState(null);
  const [editData, setEditData] = useState({});

  // Handles the change in form fields when editing
  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditData((prev) => ({ ...prev, [name]: value }));
  };

  // Starts editing an existing mortgage, populating the form with current data
  const startEditing = (mortgage) => {
    setEditingId(mortgage.id);
    const data = {};
    fields.forEach(({ name }) => (data[name] = mortgage[name]));
    setEditData(data);
  };

  // Cancels editing and resets the form data
  const cancelEditing = () => {
    setEditingId(null);
    setEditData({});
  };

  // Sends a PUT request to update in the database
  const updateMortgage = (id) => {
    const dataToSend = {
      credit_score: parseInt(editData.credit_score, 10),
      loan_amount: parseFloat(editData.loan_amount),
      property_value: parseFloat(editData.property_value),
      annual_income: parseFloat(editData.annual_income),
      debt_amount: parseFloat(editData.debt_amount),
      loan_type: editData.loan_type,
      property_type: editData.property_type,
    };

    fetch(`http://localhost:8000/mortgages/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dataToSend),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to update mortgage");
        }
        return response.json();
      })
      .then(() => {
        setEditingId(null);
        setEditData({});
        refreshMortgages();
      })
      .catch((error) => {
        console.error("Error updating mortgage:", error);
        alert("Error updating mortgage");
      });
  };

  // Sends a DELETE request to remove a mortgage from the database
  const deleteMortgage = (id) => {
    fetch(`http://localhost:8000/mortgages/${id}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to delete mortgage");
        }
        refreshMortgages();
      })
      .catch((error) => {
        console.error("Error deleting mortgage:", error);
        alert("Error deleting mortgage");
      });
  };

  return (
    <div>
      <h2>Mortgage List</h2>
      {mortgages.length === 0 ? (
        <p>No mortgages available.</p>
      ) : (
        <table border="1" cellPadding="5" cellSpacing="0">
          <thead>
            <tr>
              <th>ID</th>
              {fields.map((field) => (
                <th key={field.name}>{field.label}</th>
              ))}
              <th>Credit Rating</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {/* Mapping through mortgages to display each row in the table */}
            {mortgages.map((m) => (
              <tr key={m.id}>
                <td>{m.id}</td>

                {fields.map(({ name, type, options }) => (
                  <td key={name}>
                    {editingId === m.id ? (
                      // When in edit mode, render input fields
                      type === "select" ? (
                        <select
                          name={name}
                          value={editData[name]}
                          onChange={handleEditChange}
                        >
                          {options.map((opt) => (
                            <option key={opt} value={opt}>
                              {opt}
                            </option>
                          ))}
                        </select>
                      ) : (
                        <input
                          type="number"
                          name={name}
                          value={editData[name]}
                          onChange={handleEditChange}
                        />
                      )
                    ) : (
                      // When not in edit mode, display the mortgage's value
                      m[name]
                    )}
                  </td>
                ))}
                <td>{m.credit_rating}</td>
                <td>
                  {editingId === m.id ? (
                    <>
                      {/* Save and Cancel buttons when in edit mode */}
                      <button onClick={() => updateMortgage(m.id)}>Save</button>
                      <button onClick={cancelEditing}>Cancel</button>
                    </>
                  ) : (
                    <>
                      {/* Edit and Delete buttons when in view mode */}
                      <button onClick={() => startEditing(m)}>Edit</button>
                      <button onClick={() => deleteMortgage(m.id)}>
                        Delete
                      </button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default MortgageList;
