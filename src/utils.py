import psycopg2


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INT PRIMARY KEY,
                name VARCHAR NOT NULL,
                url VARCHAR NOT NULL,
                open_vacancies INT NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id INT PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                name VARCHAR NOT NULL,
                salary_from INT,
                salary_to INT
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict], database_name: str, params: dict):
    """Сохранение данных о работодателях и вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            cur.execute(
                """
                INSERT INTO employers (employer_id, name, url, open_vacancies)
                VALUES (%s, %s, %s, %s)
                RETURNING employer_id
                """,
                (employer['employer_id'], employer['name'], employer['url'], employer['open_vacancies'])
            )

            for vacancy in employer['vacancies']:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, employer_id, name, salary_from, salary_to)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (vacancy["vacancy_id"], vacancy["employer_id"], vacancy["name"],
                     vacancy["salary_from"], vacancy["salary_to"])
                )

    conn.commit()
    conn.close()
