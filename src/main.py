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

    user_input = int(
        input(
            """Выберите функцию для выполнения:
1) Получить список всех компаний и количество вакансий у каждой компании.
2) Получить список всех вакансий с указанием названия компании,
   названия вакансии и зарплаты и ссылки на вакансию.
3) Получить среднюю зарплату по вакансиям.
4) Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.
5) Получить список всех вакансий, в названии которых содержатся переданные в метод слова.
"""
        )
    )

    while user_input not in [1, 2, 3, 4, 5]:
        user_input = int(input("Введите цифру от 1 до 5:\n"))

    if user_input == 1:
        function_output1 = head_hunter_db.get_companies_and_vacancies_count()
        for company in function_output1:
            print(f"Компания: {company[0]}, количество вакансий = {company[1]}.")

    elif user_input == 2:
        function_output2 = head_hunter_db.get_all_vacancies()
        for vacancy in function_output2:
            print(f"Компания: {vacancy[0]}, вакансия: {vacancy[1]}, зарплата", end="")
            if vacancy[3]:
                print(f" от {vacancy[3]}", end="")
            if vacancy[2]:
                print(f" до {vacancy[2]}", end="")
            print(f".\nПодробнее: {vacancy[4]}.\n")

    elif user_input == 3:
        function_output3 = head_hunter_db.get_avg_salary()
        print(f"Средняя зарплата по вакансиям = {function_output3}.")

    elif user_input == 4:
        function_output4 = head_hunter_db.get_vacancies_with_higher_salary()
        for vacancy in function_output4:
            print(f"Вакансия: {vacancy[2]}, зарплата", end="")
            if vacancy[4]:
                print(f" от {vacancy[4]}", end="")
            if vacancy[3]:
                print(f" до {vacancy[3]}", end="")
            print(f".\nПодробнее: {vacancy[5]}.\n")

    elif user_input == 5:
        user_words = list(input("Введите слова для поиска через пробел:\n").split())
        function_output5 = head_hunter_db.get_vacancies_with_keyword(user_words)
        for vacancy in function_output5:
            print(f"Вакансия: {vacancy[2]}, зарплата", end="")
            if vacancy[4]:
                print(f" от {vacancy[4]}", end="")
            if vacancy[3]:
                print(f" до {vacancy[3]}", end="")
            print(f".\nПодробнее: {vacancy[5]}.\n")


if __name__ == "__main__":
    main()
