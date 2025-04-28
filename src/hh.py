import requests


class Employer:

    def __init__(self, employer_id, name, url, open_vacancies, vacancies):
        self.employer_id = employer_id
        self.name = name
        self.url = url
        self.open_vacancies = open_vacancies
        self.vacancies = vacancies


class HH:
    """Класс для получения данных с сайта hh.ru.
    По умолчанию регион поиска - Краснодар, количество вакансий - 10 (максимум 100)."""

    def __init__(self, text="", area=53, per_page=10):
        self.params = {
            "text": text,
            "only_with_vacancies": True,
            "sort_by": "by_vacancies_open",
            "page": 0,
            "per_page": per_page,
            "area": area,
        }
        self.url = "https://api.hh.ru/employers"

    def get_top_employers_vacancies(self):
        """Возвращает информацию о компаниях с наибольшим числом открытых вакансий."""

        # try:
        response = requests.get(url=self.url, params=self.params)
        response.raise_for_status()
        data = response.json()["items"]
        employers = []

        for employer in data:
            vacancies_data = requests.get(
                url=f"https://api.hh.ru/vacancies?employer_id={employer["id"]}").json()
            vacancies_list = []
            for vacancy in vacancies_data:

                if not vacancy["salary"].get("to"):
                    salary_to = "null"
                    salary_from = "null"
                else:
                    salary_to = vacancy["salary"]["to"]
                    salary_from = vacancy["salary"]["from"]

                vacancies_list.append({
                    "vacancy_id": vacancy["vacancy_id"],
                    "employer_id": vacancy["employer_id"],
                    "name": vacancy["name"],
                    "description": vacancy["description"],
                    "salary_from": salary_from,
                    "salary_to": salary_to
                })

            employers.append(
                {
                    "employer_id": employer["id"],
                    "name": employer["name"],
                    "url": employer["url"],
                    "open_vacancies": employer["open_vacancies"],
                    "vacancies": vacancies_list
                }
            )

        return employers

        # except Exception as e:
        #     print(f"Ошибка: {e}")
        #     return []
