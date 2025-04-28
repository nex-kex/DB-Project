from src.config import config
from src.DB_class import DBManager
from src.HH_class import HH


def main() -> None:
    hh_database = HH()
    params = config()
    head_hunter_db = DBManager("headhunterdb", params)
    head_hunter_db.create_database()

    db_data = hh_database.get_top_employers_vacancies()
    head_hunter_db.save_data_to_database(db_data)

    print(head_hunter_db.get_companies_and_vacancies_count())
    print(head_hunter_db.get_all_vacancies())
    print(head_hunter_db.get_avg_salary())
    print(head_hunter_db.get_vacancies_with_higher_salary())
    print(head_hunter_db.get_vacancies_with_keyword(["Менеджер", "Аналитик"]))


if __name__ == "__main__":
    main()
