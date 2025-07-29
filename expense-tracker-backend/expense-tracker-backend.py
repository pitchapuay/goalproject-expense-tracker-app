from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI()

# Enable CORS for all origins (insecure for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expense model
class Expense(BaseModel):
    title: str
    amount: float
    date: str  # Could use datetime in real apps

# POST endpoint to save an expense
@app.post("/expense")
async def save_expense(expense: Expense):
    print(f"Received expense: {expense}")
    # Here you would typically store it in a DB
    return {"message": "Expense saved successfully", "data": expense}

# For Lambda entry point
handler = Mangum(app)