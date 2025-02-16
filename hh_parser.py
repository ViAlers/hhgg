import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from anticaptchaofficial import AnticaptchaRecaptchaV2Proxyless

def get_hh_vacancies(job_title, city, min_salary=None, employment_type=None, experience=None):
    """Получает вакансии с hh.ru с использованием Selenium."""
    
    # Настройки для Chrome
    options = Options()
    options.headless = True  # Запускать браузер в фоновом режиме без GUI
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = 'https://hh.ru/search/vacancy'
    
    search_url = f"{url}?text={job_title}&area={city}"
    if min_salary:
        search_url += f"&salary={min_salary}"
    if employment_type:
        search_url += f"&employment={employment_type}"
    if experience:
        search_url += f"&experience={experience}"
    
    driver.get(search_url)
    
    # Решение CAPTCHA через 2Captcha
    print("Обрабатываем CAPTCHA через 2Captcha...")
    solver = AnticaptchaRecaptchaV2Proxyless()
    solver.set_key('YOUR_2CAPTCHA_API_KEY')  # Замените на ваш ключ 2Captcha

    # Получаем ключ для reCAPTCHA
    recaptcha_key = driver.find_element(By.CSS_SELECTOR, 'div.g-recaptcha').get_attribute('data-sitekey')
    
    solver.set_website_url(driver.current_url)
    solver.set_website_key(recaptcha_key)
    
    # Отправляем CAPTCHA на решение
    result = solver.solve_and_return_solution()
    
    if result != 0:
        print("CAPTCHA решена успешно.")
        driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{result}';")
        driver.find_element(By.ID, 'submit').click()  # Нажимаем кнопку после решения CAPTCHA
        time.sleep(5)
    else:
        print(f"Ошибка решения CAPTCHA: {solver.error_code}")
    
    # Получаем вакансии после решения CAPTCHA
    vacancies = []
    try:
        vacancy_elements = driver.find_elements(By.CSS_SELECTOR, 'div.vacancy-serp-item')
        for element in vacancy_elements:
            title = element.find_element(By.CSS_SELECTOR, 'a.bloko-link').text
            company = element.find_element(By.CSS_SELECTOR, 'a.bloko-link_secondary').text
            salary = element.find_element(By.CSS_SELECTOR, 'span.bloko-header-section-3').text
            city = element.find_element(By.CSS_SELECTOR, 'div.vacancy-serp-item__location').text
            url = element.find_element(By.CSS_SELECTOR, 'a.bloko-link').get_attribute('href')
            
            vacancies.append({
                'title': title,
                'company': company,
                'salary': salary,
                'city': city,
                'url': url
            })
    except Exception as e:
        print(f"Ошибка при парсинге вакансий: {e}")
    
    driver.quit()
    
    return vacancies
