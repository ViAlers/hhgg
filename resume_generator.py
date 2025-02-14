import json

def ask_user_details(requirements):
    """
    Запрашивает у пользователя информацию, соответствующую требованиям вакансии.
    """
    print("\nПрограмма составит для вас идеальное резюме на основе вакансии.")
    
    user_details = {}
    
    for req in requirements:
        answer = input(f"У вас есть опыт в '{req}'? (да/нет) ")
        if answer.lower() == 'да':
            description = input(f"Опишите ваш опыт работы с '{req}': ")
            user_details[req] = description
        else:
            user_details[req] = "Нет опыта"

    return user_details

def generate_resume(vacancy, user_details):
    """
    Формирует резюме на основе данных пользователя и вакансии.
    """
    resume = {
        "Имя": input("Введите ваше имя: "),
        "Контактный email": input("Введите ваш email: "),
        "Должность": vacancy["name"],
        "Компания": vacancy["employer"]["name"],
        "Навыки": user_details
    }
    
    resume_text = f"""
    {resume['Имя']}
    Email: {resume['Контактный email']}

    Желаемая должность: {resume['Должность']} в компании {resume['Компания']}

    Навыки и опыт:
    """
    
    for skill, desc in user_details.items():
        resume_text += f"- {skill}: {desc}\n"

    print("\nГотовое резюме:")
    print(resume_text)

    # Сохраняем в файл
    with open("resume.json", "w", encoding="utf-8") as f:
        json.dump(resume, f, ensure_ascii=False, indent=4)

    print("\nРезюме сохранено в файл 'resume.json'!")

    return resume_text
