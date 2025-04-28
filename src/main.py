from src.config import config
from src.hh import HH
from src.utils import create_database, save_data_to_database


test_db = HH(per_page=20)
params = config()
create_database("hhdb", params)
save_data_to_database(test_db.get_top_employers_vacancies(), "hhdb", params)
