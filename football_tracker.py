import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

url_Scheduled = "https://api.football-data.org/v4/teams/81/matches?status=SCHEDULED"
url_results = "https://api.football-data.org/v4/teams/81/matches?status=FINISHED"
headers = {"X-Auth-Token": api_key}

def get_matches(url):
    try :
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        print("No connection")
        return None
    if response.status_code == 400:
        print("Invalid API Key")
        return None
    if response.status_code == 403:
        print("Your plan doesn't include this data")
        return None
    if response.status_code == 429:
        print("Wait a minute and try again!")
        return None
    if response.status_code != 200:
        print(f"Something went wrong, status: {response.status_code}")
        return None
    return response.json()['matches']

def show_upcoming(matches):
    for m, match in enumerate(matches[:3], 1):
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

def show_results(matches):
    for m, match in enumerate(matches[-3:], 1):
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        competition_name = match['competition']['name']
        match_date = match['utcDate']
        delta_match = datetime.fromisoformat(match_date)
        clean_date = delta_match.strftime("%A, %d %B")
        print(clean_date)
        home_result = match['score']['fullTime']['home']
        away_result = match['score']['fullTime']['away']
        print(f"Match Number {m}: {competition_name}")
        print(f"{home_team} {home_result} - {away_result} {away_team}")
        print()


while True:
    print("1. Upcoming Matches")
    print("2. Recent Results")
    print("3. Exit")
    user_choice = input("Enter a number:")

    if user_choice == "1":
        matches = get_matches(url_Scheduled)
        if matches is None:
            continue
        if not matches:
            print("No matches found")
            continue
        show_upcoming(matches)

    elif user_choice == "2":
        matches = get_matches(url_results)
        if matches is None:
            continue
        if not matches:
            print("No recent results found")
            continue
        show_results(matches)

    elif user_choice == "3":
        print("Goodbye")
        break
    else:
        print("Invalid input")
