# main.py
from core import HHApiClient, ResumeGenerator
import sys

def print_menu():
    print("\n" + "="*50)
    print("1. Поиск вакансий")
    print("2. Выход")
    print("="*50)

def main():
    try:
        client = HHApiClient()
        generator = ResumeGenerator()
        
        while True:
            print_menu()
            choice = input("Выберите действие: ")
            
            if choice == '1':
                search_query = input("Введите поисковый запрос для вакансий: ")
                
                if vacancies := client.get_vacancies(search_query):
                    print(f"\nНайдено вакансий: {len(vacancies)}")
                    for idx, vacancy in enumerate(vacancies[:3], 1):
                        print(f"\n{idx}. {vacancy['name']}")
                        print(f"Зарплата: {vacancy['salary'] or 'не указана'}")
                        
                        resume = generator.generate_for_vacancy(vacancy)
                        print("\nСгенерированное резюме:")
                        print(f"Позиция: {resume['position']}")
                        print(f"\nПрофессиональное резюме:\n{resume['summary']}")
                        print(f"\nКлючевые навыки:\n{resume['skills']}")
                        print(f"\nОпыт:\n{resume['experience']}")
                else:
                    print("Не удалось получить вакансии. Попробуйте изменить запрос.")
            elif choice == '2':
                print("Выход из программы")
                sys.exit()
            else:
                print("Неверный выбор, попробуйте снова")
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
