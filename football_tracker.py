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
    for m, match in enumerate (data['matches'][:3], 1):



        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        competition_name = match['competition']['name']
        match_date = match['utcDate']

        delta_match = datetime.fromisoformat(match_date)
        current_time = datetime.now(timezone.utc)
        time_left = delta_match - current_time
        clean_date = delta_match.strftime("%A, %d %B")

        print(f"Match Number {m}: {home_team} vs {away_team}")
        print(competition_name)
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        print(clean_date)
        print(f"Get ready! Only {days_left} days, {hours_left} hours left until kick off!")
        print()
