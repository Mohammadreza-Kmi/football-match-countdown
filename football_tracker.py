import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

url = "https://api.football-data.org/v4/teams/81/matches?status=SCHEDULED"
headers = {"X-Auth-Token": api_key}

response = requests.get(url, headers=headers)
data = response.json()

# Grab the first match from the list
if not data['matches']:
    print("No matches found")
    exit()
else:
    next_match = data['matches'][0]

# Extract the team names and the date
home_team = next_match['homeTeam']['name']
away_team = next_match['awayTeam']['name']
match_date = next_match['utcDate']

delta_match = datetime.fromisoformat(match_date)
current_time = datetime.now(timezone.utc)
time_left = delta_match - current_time

print(f"Next Match: {home_team} vs {away_team}")
days_left = time_left.days
hours_left = time_left.seconds // 3600
print(f"Get ready! Only {days_left} days, {hours_left} hours left until kick off!")