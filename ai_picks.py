import pandas as pd
import joblib

# Load the trained model
model = joblib.load("nba_ai_model.pkl")

def implied_prob(odds):
    return 1 / odds if odds > 0 else 0

def calculate_edge(model_prob, bookie_prob):
    return (model_prob - bookie_prob) * 100  # percentage edge

def find_best_bets(upcoming_games):
    picks = []

    for game in upcoming_games:
        home_team = game["home_team"]
        away_team = game["away_team"]
        home_odds = game["home_odds"]
        away_odds = game["away_odds"]

        home_implied = implied_prob(home_odds)
        away_implied = implied_prob(away_odds)
        prob_diff = home_implied - away_implied

        # Create model input
        features = pd.DataFrame([{
            "home_implied_prob": home_implied,
            "away_implied_prob": away_implied,
            "prob_diff": prob_diff
        }])

        model_prob = model.predict_proba(features)[0][1]  # chance home wins
        edge = calculate_edge(model_prob, home_implied)

        # Return the bet if edge > 5%
        if edge > 5:
            picks.append({
                "matchup": f"{away_team} @ {home_team}",
                "model_win_prob": round(model_prob, 3),
                "bookie_implied_prob": round(home_implied, 3),
                "edge_percent": round(edge, 2),
                "bet": f"{home_team} ML",
                "odds": home_odds
            })

    return picks
