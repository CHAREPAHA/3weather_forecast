import requests;
from googletrans import Translator
translator = Translator()

city = input("Введите город: ").capitalize()
result = translator.translate(city, src='ru', dest='en')



my_api_key = "30dec169b35cd183df01398d269b2cf9"
url = f"https://api.openweathermap.org/data/2.5/weather?q={result.text}&appid={my_api_key}&units=metric&lang=ru"

response = requests.get(url)



if response.ok:
    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    print(f"Погода в {city}: {temp}°C, {description}")
else:
    print("Ошибка при получении данных:", response.status_code)