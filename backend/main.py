from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from logic import run_analysis
import os

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    ticker: str
    groq_api_key: str
    tavily_api_key: str

@app.post("/analyze")
async def analyze_stock(data: RequestData):
    try:
        # Print to confirm we received data
        print(f"Received request for: {data.ticker}") 
        
        result = run_analysis(data.ticker, data.groq_api_key, data.tavily_api_key)
        return result
    except Exception as e:
        # --- NEW CODE TO PRINT ERROR ---
        import traceback
        traceback.print_exc()
        print(f"ERROR: {str(e)}")
        # -------------------------------
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)