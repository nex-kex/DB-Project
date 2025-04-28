from src.config import config
from src.hh import HH
from src.utils import create_database, save_data_to_database


def main():
    hh_database = HH()
    db_name = "HeadHunterDB"
    params = config()
    create_database(db_name, params)

    db_data = hh_database.get_top_employers_vacancies()
    save_data_to_database(db_data, db_name, params)

if __name__ == "__main__":
    main()
