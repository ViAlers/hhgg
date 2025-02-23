# core.py
import requests
import requests_cache
from typing import Dict, List, Optional
from config import Config
import time
import json
import os

class HHApiClient:
    def __init__(self):
        self.config = Config()
        self.access_token = None
        self._init_session()
        self.cache_file = 'vacancies_cache.json'
        self._authenticate()
        
    def _init_session(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JobAssistant/3.0',
            'Accept': 'application/json'
        })
        requests_cache.install_cache(
            'hh_cache',
            expire_after=self.config.CACHE_EXPIRE,
            allowable_methods=('GET', 'HEAD')
        )
            
    def _authenticate(self):
        auth_url = f"{self.config.HH_API_URL}/oauth/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.config.HH_CLIENT_ID,
            'client_secret': self.config.HH_CLIENT_SECRET
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(auth_url, data=data, headers=headers, timeout=self.config.REQUEST_TIMEOUT)
            response.raise_for_status()
            self.access_token = response.json()['access_token']
            self.session.headers['Authorization'] = f'Bearer {self.access_token}'
        except Exception as e:
            print(f"Ошибка авторизации: {str(e)}")
            raise
            
    def get_vacancies(self, search_query: str, area: str = '113') -> Optional[List[Dict]]:
        if cached := self._load_from_cache(search_query):
            print("Используем кешированные данные")
            return cached
            
        vacancies = self._fetch_vacancies(search_query, area)
        if vacancies:
            self._save_to_cache(search_query, vacancies)
        return vacancies
        
    def _fetch_vacancies(self, search_query: str, area: str) -> Optional[List[Dict]]:
        url = f"{self.config.HH_API_URL}/vacancies"
        params = {
            'text': search_query,
            'area': area,
            'per_page': 50,
            'only_with_salary': True
        }
        
        for attempt in range(self.config.MAX_RETRIES):
            try:
                response = self.session.get(url, params=params, timeout=self.config.REQUEST_TIMEOUT)
                response.raise_for_status()
                return self._process_vacancies(response.json()['items'])
            except requests.exceptions.Timeout:
                print(f"Таймаут соединения (попытка {attempt + 1}/{self.config.MAX_RETRIES})")
                time.sleep(2 ** attempt)
            except requests.exceptions.RequestException as e:
                print(f"Ошибка сети: {str(e)}")
                return None
        return None
        
    def _process_vacancies(self, raw_vacancies: List[Dict]) -> List[Dict]:
        return [{
            'id': v['id'],
            'name': v['name'],
            'description': v['snippet']['requirement'] or '',
            'experience': v['experience'],
            'skills': [s['name'] for s in v.get('key_skills', [])],
            'salary': v['salary']
        } for v in raw_vacancies]
        
    def _load_from_cache(self, query: str) -> Optional[List[Dict]]:
        if not os.path.exists(self.cache_file):
            return None
            
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
                return cache.get(query)
        except Exception:
            return None
            
    def _save_to_cache(self, query: str, data: List[Dict]):
        cache = {}
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
            except Exception:
                pass
                
        cache[query] = data
        with open(self.cache_file, 'w') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)

class ResumeGenerator:
    def __init__(self):
        self.config = Config()
        self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"  # Уточните URL в документации DeepSeek
        self.headers = {
            "Authorization": f"Bearer {self.config.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

    def generate_for_vacancy(self, vacancy: Dict) -> Dict:
        base_resume = self._create_base_resume(vacancy)
        ai_sections = self._generate_ai_sections(vacancy)
        return {**base_resume, **ai_sections}

    def _create_base_resume(self, vacancy: Dict) -> Dict:
        return {
            'vacancy_id': vacancy['id'],
            'position': vacancy['name'],
            'base_skills': vacancy['skills'][:self.config.MAX_SKILLS],
            'salary_expectations': self._calculate_salary(vacancy.get('salary'))
        }

    def _generate_ai_sections(self, vacancy: Dict) -> Dict:
        prompt = self._create_prompt(vacancy)
        try:
            response = requests.post(
                self.deepseek_url,
                headers=self.headers,
                json={
                    "model": "deepseek-chat",  # Уточните модель в документации
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=self.config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return self._parse_ai_response(response.json()['choices'][0]['message']['content'])
        except Exception as e:
            print(f"Ошибка генерации AI: {str(e)}")
            return {}

    def _create_prompt(self, vacancy: Dict) -> str:
        return f"""
        Сгенерируй профессиональное резюме для вакансии:
        Название: {vacancy['name']}
        Описание: {vacancy['description'][:1000]}
        Требуемые навыки: {', '.join(vacancy['skills'])}
        
        Формат ответа:
        Резюме|||
        Профессиональное резюме: [3-5 предложений]
        |||
        Навыки|||
        - [5-7 ключевых навыков]
        |||
        Опыт|||
        - [3 пункта релевантного опыта]
        """

    def _parse_ai_response(self, text: str) -> Dict:
        sections = {}
        current_section = None
        
        for line in text.split('\n'):
            if '|||' in line:
                current_section = line.split('|||')[0].strip().lower()
                sections[current_section] = []
            elif current_section and line.strip():
                sections[current_section].append(line.strip())
        
        return {
            'summary': '\n'.join(sections.get('резюме', [])),
            'skills': '\n'.join(sections.get('навыки', [])),
            'experience': '\n'.join(sections.get('опыт', []))
        }

    def _calculate_salary(self, salary_data: Optional[Dict]) -> Dict:
        if not salary_data:
            return {'from': None, 'to': None}
        
        return {
            'from': salary_data.get('from'),
            'to': salary_data.get('to'),
            'currency': salary_data.get('currency')
        }
