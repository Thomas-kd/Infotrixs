import argparse
import requests
import json
import time
from datetime import datetime

API_KEY = "4865055161c24e48ab263446230410"
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"

# Initialize favorite_cities as an empty list
favorite_cities = []

# Load favorite cities from a file (if it exists)
try:
    with open("favorite_cities.txt", "r") as file:
        favorite_cities = [line.strip() for line in file]
except FileNotFoundError:
    pass

def save_favorite_cities():
    # Save favorite cities to a file
    with open("favorite_cities.txt", "w") as file:
        file.write("\n".join(favorite_cities))

def check_weather(city_name):
    try:
        params = {"key": API_KEY, "q": city_name}
        response = requests.get(WEATHER_API_URL, params=params)
        data = response.json()

        if "error" in data:
            print(f"Error: {data['error']['message']}")
        else:
            city = data["location"]["name"]
            country = data["location"]["country"]
            temperature = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]

            print(f"Weather in {city}, {country}:")
            print(f"Temperature: {temperature}°C")
            print(f"Condition: {condition}")
            print(f"Last Updated: {data['current']['last_updated']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def add_favorite(city_name):
    if city_name not in favorite_cities:
        favorite_cities.append(city_name)
        print(f"{city_name} added to favorites.")
        save_favorite_cities()  # Save the updated list of favorite cities
    else:
        print(f"{city_name} is already in favorites.")

def remove_favorite(city_name):
    if city_name in favorite_cities:
        favorite_cities.remove(city_name)
        print(f"{city_name} removed from favorites.")
        save_favorite_cities()  # Save the updated list of favorite cities
    else:
        print(f"{city_name} is not in favorites.")

def list_favorites():
    print("Favorite Cities:")
    for city in favorite_cities:
        print(city)

def main():
    print("WEATHER CHECKING APPLICATION")

    parser = argparse.ArgumentParser(description="Weather Checking CLI Application")
    parser.add_argument("action", choices=["C", "A", "R", "L"], help="Action to perform (C: check, A: add, R: remove, L: list)")
    parser.add_argument("city_name", nargs="?", default=None, help="City name (for check/add/remove actions)")
    args = parser.parse_args()

    if args.action == "C":
        if args.city_name:
            check_weather(args.city_name)
        else:
            print("Please provide a city name for the 'C' action.")
    elif args.action == "A":
        if args.city_name:
            add_favorite(args.city_name)
        else:
            print("Please provide a city name for the 'A' action.")
    elif args.action == "R":
        if args.city_name:
            remove_favorite(args.city_name)
        else:
            print("Please provide a city name for the 'R' action.")
    elif args.action == "L":
        list_favorites()

if __name__ == "__main__":
    main()