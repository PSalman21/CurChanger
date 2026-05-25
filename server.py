from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

SUPPORTED_CURRENCIES = {"USD", "EUR", "RUB", "GBP", "JPY", "CNY"}
API_KEY = "YOUR_API_KEY"
class ConvertRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

async def get_live_rates():
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=5)
        data = response.json()
        
        if data.get("result") != "success":
            raise Exception("API error")
        
        return data["conversion_rates"]

@app.post("/convert")
async def convert(request: ConvertRequest):
    if request.from_currency not in SUPPORTED_CURRENCIES:
        raise HTTPException(status_code=400, detail="Unknown currency")
    
    if request.to_currency not in SUPPORTED_CURRENCIES:
        raise HTTPException(status_code=400, detail="Unknown currency")
    
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    try:
        rates = await get_live_rates()
        
        from_rate = rates[request.from_currency]
        to_rate = rates[request.to_currency]
        
    except:
        raise HTTPException(status_code=503, detail="Exchange rates unavailable")
    
    result = (request.amount / from_rate) * to_rate
    
    return {
        "from_currency": request.from_currency,
        "to_currency": request.to_currency,
        "amount": request.amount,
        "converted_amount": round(result, 2),
        "rate": round(to_rate / from_rate, 4)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000)
