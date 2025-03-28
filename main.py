from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = FastAPI()

# Enable CORS for all domains (frontend needs this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with ["https://aismartbetfrontend.vercel.app"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your Odds API key
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4/sports"

# Root route (optional)
@app.get("/")
def read_root():
    return {"message": "AI SmartBet backend is live 🚀"}

# Get list of available sports
@app.get("/sports")
def get_sports():
    try:
        response = requests.get(f"{BASE_URL}", params={"apiKey": ODDS_API_KEY})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get odds for a specific sport (e.g., basketball_nba)
@app.get("/odds/{sport_key}")
def get_odds(sport_key: str):
    try:
        url = f"{BASE_URL}/{sport_key}/odds"
        params = {
            "apiKey": ODDS_API_KEY,
            "regions": "us",            # or "us,uk,eu"
            "markets": "h2h",           # head-to-head bets
            "oddsFormat": "decimal",    # or "american"
            "dateFormat": "iso"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
