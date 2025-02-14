import requests

def get_hh_vacancies(query, area=1, per_page=10):
    """Функция получает вакансии с hh.ru по заданному запросу."""
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': query,  # Поисковый запрос
        'area': area,  # ID региона (1 — Россия)
        'per_page': per_page,  # Количество вакансий на странице
        'page': 0  # Номер страницы
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        vacancies = response.json()['items']
        results = []

        for vacancy in vacancies:
            name = vacancy.get('name', 'Нет названия')
            employer = vacancy.get('employer', {}).get('name', 'Не указано')
            salary = vacancy.get('salary')
            salary_text = "Не указана"
            if salary:
                if salary.get('from') and salary.get('to'):
                    salary_text = f"{salary['from']} - {salary['to']} {salary['currency']}"
                elif salary.get('from'):
                    salary_text = f"от {salary['from']} {salary['currency']}"
                elif salary.get('to'):
                    salary_text = f"до {salary['to']} {salary['currency']}"

            description = vacancy.get('snippet', {}).get('responsibility', 'Нет описания')
            url = vacancy.get('alternate_url', '#')

            results.append({
                'title': name,
                'company': employer,
                'salary': salary_text,
                'description': description,
                'url': url
            })
        
        return results
    else:
        print(f"Ошибка запроса: {response.status_code}")
        return []
