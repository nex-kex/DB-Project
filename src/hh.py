import requests


class HH:
    """Класс для получения данных с сайта hh.ru.
    По умолчанию регион поиска - Краснодар, количество вакансий - 10 (максимум 100)."""

    def __init__(self, text="", area=53, amount=10):
        self.params = {
            "text": text,
            "only_with_vacancies": True,
            "sort_by": "by_vacancies_open",
            "page": 0,
            "per_page": amount,
            "area": area,
        }
        self.url = "https://api.hh.ru/employers"

    def get_top_employers(self):
        """Возвращает информацию о компаниях с наибольшим числом открытых вакансий."""

        try:
            response = requests.get(url=self.url, params=self.params)
            response.raise_for_status()
            employers = response.json()["items"]
            return employers

        except Exception as e:
            print(f"Ошибка: {e}")
            return []
