from job_search import get_hh_vacancies
from superjob_parser import get_superjob_vacancies

def main():
    query = input("Введите название вакансии для поиска: ")
    
    print("\n🔍 Поиск вакансий на hh.ru...")
    hh_vacancies = get_hh_vacancies(query)

    print("\n🔍 Поиск вакансий на SuperJob...")
    sj_vacancies = get_superjob_vacancies(query)

    all_vacancies = hh_vacancies + sj_vacancies

    if not all_vacancies:
        print("❌ Вакансии не найдены.")
        return

    print("\n✅ Найденные вакансии:\n")
    for idx, vacancy in enumerate(all_vacancies):
        print(f"{idx + 1}. {vacancy['title']} ({vacancy['company']})")
        print(f"   💰 Зарплата: {vacancy['salary']}")
        print(f"   🔗 Ссылка: {vacancy['url']}\n")

if __name__ == "__main__":
    main()
