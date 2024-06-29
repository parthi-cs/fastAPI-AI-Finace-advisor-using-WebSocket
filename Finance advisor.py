from fastapi import FastAPI, HTTPException, WebSocket, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class UserData(BaseModel):
    income: float
    expenses: float
    savings: float
    debt: float

class FinancialAdvice(BaseModel):
    advice: str

@app.get("/")
async def get():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>AI Personal Finance Advisor</title>
        </head>
        <body>
            <h1>AI Personal Finance Advisor</h1>
            <form action="/advice" method="post">
                <label for="income">Monthly Income:</label><br>
                <input type="number" id="income" name="income"><br>
                <label for="expenses">Monthly Expenses:</label><br>
                <input type="number" id="expenses" name="expenses"><br>
                <label for="savings">Current Savings:</label><br>
                <input type="number" id="savings" name="savings"><br>
                <label for="debt">Current Debt:</label><br>
                <input type="number" id="debt" name="debt"><br>
                <input type="submit" value="Get Advice">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/advice", response_model=FinancialAdvice)
async def get_advice(income: float = Form(...), expenses: float = Form(...), savings: float = Form(...), debt: float = Form(...)):
    user_data = UserData(income=income, expenses=expenses, savings=savings, debt=debt)
    advice = generate_advice(user_data)
    return FinancialAdvice(advice=advice)

def generate_advice(user_data: UserData) -> str:
    # More comprehensive rule-based financial advice
    if user_data.debt > user_data.income:
        return "Your debt is higher than your income.Focus on paying off your debt."
    elif user_data.expenses >= user_data.income:
        return "Your expenses are high or higher than your income. Try to cut down on unnecessary expenses."
    elif user_data.savings < 3 * user_data.expenses:
        return "Your savings are less than 3 months' worth of expenses. Build an emergency fund."
    elif user_data.savings > 6 * user_data.expenses and user_data.debt == 0:
        return "Your finances look great! Consider to invest your savings."
    else:
        return "Keep saving and managing your finances wisely."

# WebSocket for real-time interaction (optional)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        user_data = UserData(**data)
        advice = generate_advice(user_data)
        await websocket.send_json({"advice": advice})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
