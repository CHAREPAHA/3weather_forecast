import requests
import csv
import os

def get_weather(city: str, api_key: str) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }

        _save_to_csv(weather_info)
        return weather_info

    except requests.exceptions.HTTPError:
        if response.status_code == 401:
            print("Ошибка: Неверный API-ключ.")
        elif response.status_code == 404:
            print(f"Ошибка: Город '{city}' не найден.")
        else:
            print(f"HTTP ошибка: {response.status_code}")
        return {}
    except requests.exceptions.RequestException:
        print("Ошибка сети. Проверьте подключение к интернету.")
        return {}

def _save_to_csv(weather_data: dict, filename: str = "weather_data.csv"):

    write_header = not os.path.exists(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["Город", "Температура (°C)", "Описание"])
        writer.writerow([
            weather_data["city"],
            weather_data["temperature"],
            weather_data["description"]
        ])



def get_weather_forecast(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&cnt=3&lang=ru"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") == "200":
        forecast = []
        for item in data["list"]:
            forecast.append({
                "date": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "description": item["weather"][0]["description"]
            })
        return forecast
    return None