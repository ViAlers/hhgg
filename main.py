import json
import requests

# Мок-данные вакансий
vacancies = [
    {
        "position": "Data Scientist",
        "company": "TechCorp",
        "requirements": [
            "Python", 
            "Machine Learning", 
            "Data Analysis"
        ]
    },
    {
        "position": "Software Engineer",
        "company": "CodeWorks",
        "requirements": [
            "Java", 
            "Spring", 
            "Database Management"
        ]
    }
]

# Функция для анализа вакансий
def analyze_vacancies(vacancies):
    analysis = []
    for vacancy in vacancies:
        position = vacancy['position']
        company = vacancy['company']
        requirements = ', '.join(vacancy['requirements'])
        analysis.append({
            'position': position,
            'company': company,
            'requirements': requirements
        })
    return analysis

# Функция для генерации резюме (пока заглушка)
def generate_resume(vacancy):
    resume = f"Resume for {vacancy['position']} at {vacancy['company']}\n"
    resume += f"Required skills: {', '.join(vacancy['requirements'])}\n"
    return resume

def main():
    # Анализируем вакансии
    analysis = analyze_vacancies(vacancies)
    print("Vacancy Analysis:\n")
    for item in analysis:
        print(f"Position: {item['position']}")
        print(f"Company: {item['company']}")
        print(f"Requirements: {item['requirements']}\n")
        
    # Генерируем резюме для первой вакансии
    print("Generated Resume:\n")
    print(generate_resume(vacancies[0]))

if __name__ == '__main__':
    main()
from hh_api import get_vacancies

# Получаем вакансии
vacancies = get_vacancies("Python Developer", region=1, per_page=5)

# Выводим результаты
for vacancy in vacancies:
    print(f"Вакансия: {vacancy['name']}")
    print(f"Компания: {vacancy['employer']['name']}")
    print(f"Ссылка: {vacancy['alternate_url']}")
    print("-" * 40)
