import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

url_Scheduled = "https://api.football-data.org/v4/teams/81/matches?status=SCHEDULED"
url_results = "https://api.football-data.org/v4/teams/81/matches?status=FINISHED"
headers = {"X-Auth-Token": api_key}


print("1. Upcoming Matches")
print("2. Recent Results")
print("3. Exit")
user_choice = input("Enter a number:")
if user_choice == "1":
    response = requests.get(url_Scheduled, headers=headers)
    data = response.json()

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
elif user_choice == "2":

    response = requests.get(url_results, headers=headers)
    data = response.json()
    for m, match in enumerate (data['matches'][-3:], 1):
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        competition_name = match['competition']['name']

        home_result = match['score']['fullTime']['home']
        away_result = match['score']['fullTime']['away']
        print(f"Match Number {m}: {competition_name}")
        print(f"{home_team} {home_result} - {away_result} {away_team}")

        print()



elif user_choice == "3":
    print("Goodbye")
    exit()
else:
    print("Invalid input")
    exit()