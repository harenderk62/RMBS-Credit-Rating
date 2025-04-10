import React, { useState, useEffect } from "react";
import MortgageForm from "./components/MortgageForm";
import MortgageList from "./components/MortgageList";
import "./App.css";

function App() {
  const [mortgages, setMortgages] = useState([]);

  // GET request to fetch mortgage data
  const fetchMortgages = () => {
    fetch("http://localhost:8000/mortgages")
      .then((response) => response.json())
      .then((data) => {
        setMortgages(data.mortgages);
      })
      .catch((error) => console.error("Error fetching mortgages:", error));
  };

  useEffect(() => {
    fetchMortgages();
  }, []);

  const handleAddMortgage = () => {
    fetchMortgages();
  };

  return (
    <div className="App">
      <h1>Mortgage Application</h1>
      {/* Render MortgageForm component*/}
      <MortgageForm onAddMortgage={handleAddMortgage} />
      {/* Render MortgageList component */}
      <MortgageList mortgages={mortgages} refreshMortgages={fetchMortgages} />
    </div>
  );
}

export default App;
