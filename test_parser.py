import requests
from bs4 import BeautifulSoup
import random

def test_hh_parser(job_title, city_name):
    """Тестируем, что реально приходит с HH.ru"""

    city_mapping = {
        "москва": "1",
        "санкт-петербург": "2",
        "краснодар": "53",
        "екатеринбург": "3",
        "новосибирск": "4"
    }

    city_id = city_mapping.get(city_name.lower())

    if not city_id:
        print("⚠️ Город не найден. Введите другой город.")
        return

    url = f"https://hh.ru/search/vacancy?text={job_title}&area={city_id}"
    
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        ])
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Ошибка запроса к HH.ru: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # 🔹 Выведем весь HTML в консоль
    print("\n🔹 HTML-страницы HH.ru (первые 1000 символов):\n")
    print(response.text[:1000])

if __name__ == "__main__":
    job_title = input("Введите название вакансии: ")
    city_name = input("Введите название города: ")
    test_hh_parser(job_title, city_name)
