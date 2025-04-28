import psycopg2


class DBManager:

    def __init__(self, db_name: str, params: dict):
        self.name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self) -> list:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=self.name, **self.params)
        cur = conn.cursor()

        query = """
            SELECT name, open_vacancies FROM employers;
        """

        cur.execute(query)
        result = cur.fetchall()

        conn.close()
        return result

    def get_all_vacancies(self) -> list:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(dbname=self.name, **self.params)
        cur = conn.cursor()

        query = """
                SELECT employers.name AS employer_name, vacancies.name AS vacancy_name,
                vacancies.salary_to, vacancies.salary_from
                FROM vacancies
                INNER JOIN employers USING(employer_id);
            """

        cur.execute(query)
        result = cur.fetchall()

        conn.close()
        return result

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(dbname=self.name, **self.params)
        cur = conn.cursor()

        query = """
                    SELECT AVG((salary_to + salary_from) / 2) FROM vacancies
                    WHERE salary_to IS NOT NULL OR salary_from IS NOT NULL;
                """

        cur.execute(query)
        result = round(float(cur.fetchone()[0]), 2)

        conn.close()
        return result

    def get_vacancies_with_higher_salary(self) -> list:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        average_salary = self.get_avg_salary()

        conn = psycopg2.connect(dbname=self.name, **self.params)
        cur = conn.cursor()

        query = f"""
                    SELECT * FROM vacancies
                    WHERE salary_from > {average_salary} OR salary_to > {average_salary};
                """

        cur.execute(query)
        result = cur.fetchall()

        conn.close()
        return result

    def get_vacancies_with_keyword(self, keywords: list) -> list:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""

        conn = psycopg2.connect(dbname=self.name, **self.params)
        cur = conn.cursor()
        result = []

        for keyword in keywords:

            query = f"""
                        SELECT * FROM vacancies
                        WHERE name LIKE '%{keyword}%';
                    """

            cur.execute(query)
            result.append(cur.fetchall())

        conn.close()
        return result

    def create_database(self) -> None:
        """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях."""

        conn = psycopg2.connect(dbname="postgres", **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f"DROP DATABASE {self.name}")
        except psycopg2.errors.InvalidCatalogName:
            pass

        cur.execute(f"CREATE DATABASE {self.name}")

        conn.close()

        conn = psycopg2.connect(dbname=self.name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employers (
                    employer_id INT PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    url VARCHAR NOT NULL,
                    open_vacancies INT NOT NULL
                )
            """
            )

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_id INT PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    name VARCHAR NOT NULL,
                    salary_from INT,
                    salary_to INT
                )
            """
            )

        conn.commit()
        conn.close()

    def save_data_to_database(self, data: list[dict]) -> None:
        """Сохранение данных о работодателях и вакансиях в базу данных."""

        conn = psycopg2.connect(dbname=self.name, **self.params)

        with conn.cursor() as cur:
            for employer in data:
                cur.execute(
                    """
                    INSERT INTO employers (employer_id, name, url, open_vacancies)
                    VALUES (%s, %s, %s, %s)
                    RETURNING employer_id
                    """,
                    (employer["employer_id"], employer["name"], employer["url"], employer["open_vacancies"]),
                )

                for vacancy in employer["vacancies"]:
                    cur.execute(
                        """
                        INSERT INTO vacancies (vacancy_id, employer_id, name, salary_from, salary_to)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            vacancy["vacancy_id"],
                            vacancy["employer_id"],
                            vacancy["name"],
                            vacancy["salary_from"],
                            vacancy["salary_to"],
                        ),
                    )

        conn.commit()
        conn.close()
