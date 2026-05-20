import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

try:
    with open("weather.json", "r") as file:
        weather = json.load(file)
except FileNotFoundError:
    weather = []


while True:
    print("\n=== Menu Options ===")
    print("1. Check weather")
    print("2. View search history(cities you searched)")
    print("3. Delete search history")
    print("4. Exit")

    pick = input("Enter 1-4: ")

    if pick == '1':
        city_name = input("Enter city name: ")
        api = os.getenv('WEATHER_API_KEY')
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()

            if data.get('cod') != 200:
                print(f"City {city_name} not found. Try again.")
            else:
                temp = data['main']['temp']
                condition = data['weather'][0]['description']
                humidity = data['main']['humidity']
                farenheit = (temp * 9 / 5) + 32
                print(f"\nWeather in {city_name}")
                print(f"\nTemperature: {round(temp, 1)}°C or {round(farenheit, 1)}°F")
                print(f"\nCondition: {condition.title()}")
                print(f"Humidity: {humidity}")
                weather.append({"name": city_name, "temperature": temp, "condition": condition.title()})
        except requests.exceptions.RequestException:
            print("Network error. Check your internet connection.")
        except KeyError:
            print("Unexpected error. Try again.")
    elif pick == '2':
        if len(weather) == 0:
            print("No search history yet!")
        else:
            print("\n=== Weather History ===")
            for i, wea in enumerate(weather, 1):
                print(f"{i}. {wea['name']}: {wea['temperature']} - {wea['condition']}")
    elif pick == '3':
        delete = input("Delete all or specific one? (all/one): ")
        if delete.lower() == 'all':
            print("Deleted search history!")
            weather.clear()
        elif delete.lower() == 'one':
            which = input("Enter the name of the city: ")
            Found = False
            for city in weather:
                if city["name"].lower() == which.lower():
                    weather.remove(city)
                    print(f"{which} is removed!")
                    Found = True
                    break
            if not Found:
                print(f"City {which} is not found!")
        else:
            print("Invalid choice. Please enter all or one.")
    elif pick == '4':
        with open("weather.json", "w") as file:
            json.dump(weather, file, indent=4)
        print("Sayonara")
        break
    else:
        print("Invalid choice. Please enter 1-4.")