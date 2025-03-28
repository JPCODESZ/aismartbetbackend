import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load the mock data
df = pd.read_csv("mock_nba_data.csv")

# Feature engineering: convert odds to implied probabilities
df["home_implied_prob"] = 1 / df["home_odds"]
df["away_implied_prob"] = 1 / df["away_odds"]

# Feature: difference between home and away implied probabilities
df["prob_diff"] = df["home_implied_prob"] - df["away_implied_prob"]

# Input features
X = df[["home_implied_prob", "away_implied_prob", "prob_diff"]]
y = df["home_win"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost classifier
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# Evaluate accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.2f}")

# Save the trained model to a file
joblib.dump(model, "nba_ai_model.pkl")
print("✅ Model saved as nba_ai_model.pkl")
