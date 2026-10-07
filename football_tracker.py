import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
headers = {"X-Auth-Token": api_key}


def get_matches(url):
    try:
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


def get_teams():
    try:
        response = requests.get("https://api.football-data.org/v4/teams?limit=500", headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        print("No connection")
        return None
    if response.status_code != 200:
        print(f"Could not load teams, status: {response.status_code}")
        return None
    return response.json()['teams']


def get_and_check(url, empty_message):
    matches = get_matches(url)
    if matches is None:
        return None
    if not matches:
        print(empty_message)
        return None
    return matches


def find_teams(query, teams):
    query = query.lower()
    found = []
    for team in teams:
        if query in team['name'].lower():
            found.append(team)
    return found


def ask_team_name(teams):
    while True:
        query = input("Enter your team name: ")
        result = find_teams(query, teams)
        if result:
            return result
        print("Team not found")


def ask_choice(result):
    for number, team in enumerate(result, 1):
        print(number, team['name'])

    while True:
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please type a number.")
            continue
        if 1 <= choice <= len(result):
            return result[choice - 1]
        print("Number out of range.")


def choose_team(teams):
    result = ask_team_name(teams)
    return ask_choice(result)


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


teams = get_teams()
if not teams:
    exit()

team = choose_team(teams)

while True:
    url_Scheduled = f"https://api.football-data.org/v4/teams/{team['id']}/matches?status=SCHEDULED"
    url_results = f"https://api.football-data.org/v4/teams/{team['id']}/matches?status=FINISHED"

    print(f"--- {team['name']} ---")
    print("1. Upcoming Matches")
    print("2. Recent Results")
    print("3. Change team")
    print("4. Exit")
    user_choice = input("Enter a number:")

    if user_choice == "1":
        matches = get_and_check(url_Scheduled, "No matches found")
        if not matches:
            continue
        show_upcoming(matches)

    elif user_choice == "2":
        matches = get_and_check(url_results, "No recent results found")
        if not matches:
            continue
        show_results(matches)

    elif user_choice == "3":
        team = choose_team(teams)

    elif user_choice == "4":
        print("Goodbye")
        break
    else:
        print("Invalid input")