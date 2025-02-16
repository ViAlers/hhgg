# core.py
import requests
import requests_cache
from typing import Dict, List, Optional
from config import Config

class HHApiClient:
    def __init__(self):
        self.config = Config()
        self._init_session()

    def _init_session(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JobAssistant/1.0 (aalers@example.com)',
            'Authorization': f'Bearer {self.config.HH_API_KEY}'
        })
        requests_cache.install_cache(
            'hh_cache',
            expire_after=self.config.CACHE_EXPIRE,
            allowable_methods=('GET', 'HEAD')
            
    def get_vacancies(self, search_query: str, area: str = '113') -> Optional[List[Dict]]:
        params = {
            'text': search_query,
            'area': area,
            'per_page': 50
        }
        
        try:
            response = self.session.get(
                self.config.HH_API_URL,
                params=params,
                timeout=self.config.SESSION_TIMEOUT
            )
            response.raise_for_status()
            return response.json().get('items', [])
            
        except requests.exceptions.RequestException as e:
            print(f"API Error: {str(e)}")
            return None

class ResumeGenerator:
    @staticmethod
    def _extract_keywords(vacancy: Dict) -> List[str]:
        # Базовый парсинг ключевых слов из текста вакансии
        text = f"{vacancy['name']} {vacancy['description']}".lower()
        return list(set([word.strip('.,!') for word in text.split() if len(word) > 3]))

    def generate_for_vacancy(self, vacancy: Dict) -> Dict:
        keywords = self._extract_keywords(vacancy)
        
        return {
            'title': vacancy['name'],
            'custom_position': f"Python Developer ({vacancy['department']['name']})" if vacancy.get('department') else "Python Developer",
            'skills': keywords[:15],  # Топ-15 ключевых слов
            'experience': self._format_experience(vacancy.get('experience')),
            'custom_section': {
                'company_requirements': keywords,
                'original_vacancy_id': vacancy['id']
            }
        }

    def _format_experience(self, exp: Dict) -> str:
        # Форматирование опыта под требования вакансии
        if exp['id'] == 'noExperience':
            return "Готов рассматривать начальные позиции"
        return f"Опыт работы: {exp['name']}"
