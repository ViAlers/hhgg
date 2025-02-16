import requests
from bs4 import BeautifulSoup

def get_superjob_vacancies(job_title, city, min_salary, employment_type, experience):
    job_title = job_title.replace(" ", "+")
    city = city.replace(" ", "+")
    url = f"https://www.superjob.ru/vacancy/search/?keywords={job_title}&geo%5Bt%5D%5B0%5D={city}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка при запросе к SuperJob: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    vacancies = []

    for vacancy in soup.find_all("div", class_="f-test-vacancy-item"):
        title_tag = vacancy.find("a", class_="icMQ_ _6AfZ9")
        company_tag = vacancy.find("span", class_="_3nMqD f-test-text-vacancy-item-company-name")
        salary_tag = vacancy.find("span", class_="_2Wp8I")
        city_tag = vacancy.find("span", class_="_3nMqD f-test-text-company-item-location")

        title = title_tag.text.strip() if title_tag else "Без названия"
        link = f"https://www.superjob.ru{title_tag['href']}" if title_tag else "#"
        company = company_tag.text.strip() if company_tag else "Не указано"
        salary = salary_tag.text.strip() if salary_tag else "Не указана"
        city = city_tag.text.strip().split(",")[0] if city_tag else "Не указан"

        vacancies.append({
            "title": title,
            "company": company,
            "salary": salary,
            "city": city,
            "url": link
        })

    return vacancies
