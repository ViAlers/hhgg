import requests

# Функция для получения списка вакансий с hh.ru
def get_vacancies(query="Data Scientist", region=1, per_page=5, page=0):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': query,   # Поисковый запрос
        'area': region,  # ID региона (1 — Россия)
        'per_page': per_page,
        'page': page
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()['items']  # Возвращаем список вакансий
    else:
        print(f"Ошибка запроса: {response.status_code}")
        return []  # Возвращаем пустой список в случае ошибки
