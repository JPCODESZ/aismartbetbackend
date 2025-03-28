from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import requests



load_dotenv()

app = FastAPI()

# ✅ CORS setup for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or set to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root health check
@app.get("/")
def read_root():
    return {"message": "AI SmartBet Backend is running 🚀"}

# ✅ Get all sports
@app.get("/sports")
def get_sports():
    try:
        response = requests.get(
            "https://api.the-odds-api.com/v4/sports",
            params={"apiKey": os.getenv("ODDS_API_KEY")}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get odds for a specific sport
@app.get("/odds/{sport_key}")
def get_odds(sport_key: str):
    try:
        url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"
        params = {
            "apiKey": os.getenv("ODDS_API_KEY"),
            "regions": "us",
            "markets": "h2h",
            "oddsFormat": "decimal"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ AI-Powered Betting Picks
@app.get("/ai-picks")
def get_ai_picks():
    upcoming = [
        {"home_team": "Lakers", "away_team": "Suns", "home_odds": 1.75, "away_odds": 2.10},
        {"home_team": "Celtics", "away_team": "Heat", "home_odds": 2.05, "away_odds": 1.70},
        {"home_team": "Bucks", "away_team": "Knicks", "home_odds": 1.62, "away_odds": 2.30},
    ]
    return find_best_bets(upcoming)
