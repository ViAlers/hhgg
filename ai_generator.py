import os
from openai import OpenAI
from config import Config
from typing import Dict, Optional

class AIGenerator:
    def __init__(self):
        self.config = Config()
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
        
    def generate_ai_section(self, vacancy: Dict, section_type: str) -> Optional[str]:
        prompt = self._create_prompt(vacancy, section_type)
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI Generation Error: {str(e)}")
            return None

    def _create_prompt(self, vacancy: Dict, section_type: str) -> str:
        base_prompt = f"""
        Ты профессиональный HR-консультант. Создай {section_type} для резюме, идеально соответствующего этой вакансии:
        
        Название: {vacancy['name']}
        Описание: {vacancy['description'][:1000]}
        Требования: {vacancy['experience']['name'] if vacancy.get('experience') else 'Не указано'}
        
        Требования к резюме:
        - Максимально релевантно позиции
        - Используй профессиональную лексику
        - Подчеркни соответствие требованиям вакансии
        - Длина: 3-5 пунктов
        """
        
        section_specific = {
            "summary": "краткое профессиональное резюме (3-5 предложений)",
            "skills": "раздел ключевых навыков",
            "experience": "описание соответствующего опыта работы"
        }
        
        return base_prompt + f"\nСгенерируй: {section_specific[section_type]}"
