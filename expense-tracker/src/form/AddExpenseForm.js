import React, { useState } from 'react';

const AddExpenseForm = () => {
    const [title, setTitle] = useState('');
    const [amount, setAmount] = useState('');

    const addExpense = async (expense) => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/expense`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(expense),
            });

            if (!response.ok) {
                throw new Error('Failed to add expense');
            }

            const data = await response.json();
            console.log('Expense added:', data);
            alert('Expense added successfully!');
        } catch (error) {
            console.error('Error:', error.message);
            alert('Error adding expense');
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const newExpense = {
            title,
            amount: parseFloat(amount),
            date: new Date().toISOString()
        };
        addExpense(newExpense);
        setTitle('');
        setAmount('');
    };

    const fetchExpenses = async () => {
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/expense`);
            const data = await response.json();
            console.log("Expenses:", data);
            setExpenses(data); // If you store them in state
        } catch (error) {
            console.error("Error fetching expenses:", error);
        }
    };


    return (
        <form onSubmit={handleSubmit} style={{ margin: '20px' }}>
            <h2>Add New Expense</h2>
            <div>
                <label>Title: </label>
                <input
                    type="text"
                    value={title}
                    required
                    onChange={(e) => setTitle(e.target.value)}
                />
            </div>
            <div>
                <label>Amount: </label>
                <input
                    type="number"
                    value={amount}
                    required
                    onChange={(e) => setAmount(e.target.value)}
                />
            </div>
            <button type="submit">Add Expense</button>
        </form>
    );
};

export default AddExpenseForm;
