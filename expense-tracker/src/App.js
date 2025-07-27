import React, { useState } from "react";

function App() {
  const [amount, setAmount] = useState("");
  const [expenses, setExpenses] = useState([]);

  const addExpense = async () => {
    const res = await fetch("https://<your-api-id>.execute-api.<region>.amazonaws.com/prod/expense", {
      method: "POST",
      body: JSON.stringify({ amount }),
    });
    if (res.ok) {
      setExpenses([...expenses, amount]);
      setAmount("");
    }
  };

  return (
    <div>
      <h1>Expense Tracker</h1>
      <input value={amount} onChange={(e) => setAmount(e.target.value)} />
      <button onClick={addExpense}>Add</button>
      <ul>{expenses.map((e, i) => <li key={i}>{e}</li>)}</ul>
    </div>
  );
}

export default App;
