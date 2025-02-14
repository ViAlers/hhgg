import requests
from bs4 import BeautifulSoup

def get_superjob_vacancies(query, pages=1):
    """Функция парсит вакансии с SuperJob по заданному запросу."""
    base_url = "https://www.superjob.ru"
    search_url = f"{base_url}/vacancy/search/?keywords={query}"

    vacancies = []

    for page in range(1, pages + 1):
        url = f"{search_url}&page={page}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        if response.status_code != 200:
            print(f"Ошибка запроса к SuperJob: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "lxml")
        vacancy_blocks = soup.find_all("div", class_="f-test-vacancy-item")

        for vacancy in vacancy_blocks:
            title_tag = vacancy.find("a", class_="f-test-link-Vacancy")
            company_tag = vacancy.find("a", class_="f-test-link-Company")
            salary_tag = vacancy.find("span", class_="f-test-text-company-item-salary")

            title = title_tag.text.strip() if title_tag else "Не указано"
            company = company_tag.text.strip() if company_tag else "Не указано"
            salary = salary_tag.text.strip() if salary_tag else "Не указана"
            url = base_url + title_tag["href"] if title_tag else "#"

            vacancies.append({
                "title": title,
                "company": company,
                "salary": salary,
                "url": url
            })

    return vacancies
