import requests


class HH:
    """Класс для получения данных с сайта hh.ru.
    По умолчанию регион поиска - Краснодар, количество вакансий - 10 (максимум 100)."""

    def __init__(self, text: str = "", area: int = 53, per_page: int = 10):
        self.params = {
            "text": text,
            "only_with_vacancies": True,
            "sort_by": "by_vacancies_open",
            "page": 0,
            "per_page": per_page,
            "area": area,
        }
        self.url = "https://api.hh.ru/employers"

    def get_top_employers_vacancies(self) -> list:
        """Возвращает информацию о компаниях с наибольшим числом открытых вакансий."""

        try:
            response = requests.get(url=self.url, params=self.params)
            response.raise_for_status()
            data = response.json()["items"]
            employers = []

            for employer in data:
                vacancies_data = requests.get(
                    params={"per_page": 100, "vacancy_search_order": "salary_desc", "only_with_salary": True},
                    url=f"https://api.hh.ru/vacancies?employer_id={employer["id"]}",
                ).json()["items"]
                vacancies_list = []
                for vacancy in vacancies_data:
                    try:
                        salary_to = vacancy["salary"]["to"]
                        salary_from = vacancy["salary"]["from"]
                    except TypeError:
                        salary_to = vacancy["salary"]
                        salary_from = vacancy["salary"]

                    vacancies_list.append(
                        {
                            "vacancy_id": vacancy["id"],
                            "employer_id": vacancy["employer"]["id"],
                            "name": vacancy["name"],
                            "salary_from": salary_from,
                            "salary_to": salary_to,
                        }
                    )

                employers.append(
                    {
                        "employer_id": employer["id"],
                        "name": employer["name"],
                        "url": employer["url"],
                        "open_vacancies": employer["open_vacancies"],
                        "vacancies": vacancies_list,
                    }
                )

            return employers

        except Exception as e:
            print(f"Ошибка: {e}")
            return []
