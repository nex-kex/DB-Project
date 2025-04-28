from configparser import ConfigParser


def config(filename: str = "database.ini", section: str = "postgresql") -> dict:
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    return db
