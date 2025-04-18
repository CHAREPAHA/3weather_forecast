from weather_api import get_weather

API_KEY = "30dec169b35cd183df01398d269b2cf9"
city = input("Введите город: ").capitalize()

weather = get_weather(city, API_KEY)

if weather:
    print(f"Погода в {weather['city']}: {weather['temperature']}°C, {weather['description']}")
