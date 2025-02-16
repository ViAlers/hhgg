import requests
from hh_parser import get_hh_vacancies

def main():
    print("🔍 Добро пожаловать в систему умного поиска работы!")

    job_title = input("Введите название вакансии для поиска: ")
    city_name = input("Введите название города (например, Москва, Краснодар): ")

    print("\n🔍 Поиск вакансий на HH.ru...")
    hh_vacancies = get_hh_vacancies(job_title, city_name)

    if not hh_vacancies:
        print("\n⚠️ Вакансии не найдены. Попробуйте изменить параметры поиска.")
        return

    print("\n📋 Найденные вакансии:")
    for idx, vacancy in enumerate(hh_vacancies, start=1):
        print(f"\n[{idx}] {vacancy['title']} ({vacancy['company']})")
        print(f"💰 Зарплата: {vacancy['salary']}")
        print(f"📍 Город: {vacancy['city']}")
        print(f"🔗 Ссылка: {vacancy['url']}")

if __name__ == "__main__":
    main()

