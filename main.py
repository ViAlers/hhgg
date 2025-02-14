from job_search import get_hh_vacancies

def main():
    query = input("Введите название вакансии для поиска: ")
    vacancies = get_hh_vacancies(query)

    if not vacancies:
        print("Вакансии не найдены.")
        return

    print("\nНайденные вакансии:\n")
    for idx, vacancy in enumerate(vacancies):
        print(f"{idx + 1}. {vacancy['title']} ({vacancy['company']})")
        print(f"   Зарплата: {vacancy['salary']}")
        print(f"   Описание: {vacancy['description']}")
        print(f"   Ссылка: {vacancy['url']}\n")

if __name__ == "__main__":
    main()
