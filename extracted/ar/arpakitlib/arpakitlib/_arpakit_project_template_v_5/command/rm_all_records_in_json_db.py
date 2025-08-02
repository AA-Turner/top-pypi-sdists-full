from project.core.settings import get_cached_settings
from project.core.util import setup_logging
from project.json_db.json_db import get_cached_json_db


def __command():
    setup_logging()
    get_cached_settings().raise_if_mode_prod()
    get_cached_json_db().rm_all_records()


if __name__ == '__main__':
    __command()
