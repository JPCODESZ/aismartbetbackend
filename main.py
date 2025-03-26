from fastapi import FastAPI, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

ODDS_API_KEY = os.getenv('ODDS_API_KEY')
ODDS_API_URL = 'https://api.the-odds-api.com/v4/sports'

@app.get('/')
def read_root():
    return {"status": "Betting AI Backend running!"}

@app.get('/sports')
def get_sports():
    response = httpx.get(f"{ODDS_API_URL}?apiKey={ODDS_API_KEY}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching sports")
    return response.json()

@app.get('/odds/{sport_key}')
def get_odds(sport_key: str, regions: str = 'us', markets: str = 'h2h'):
    odds_response = httpx.get(
        f"{ODDS_API_URL}/{sport_key}/odds",
        params={
            'apiKey': ODDS_API_KEY,
            'regions': regions,
            'markets': markets,
        }
    )

    if odds_response.status_code != 200:
        raise HTTPException(status_code=odds_response.status_code, detail="Error fetching odds")

    return odds_response.json()
