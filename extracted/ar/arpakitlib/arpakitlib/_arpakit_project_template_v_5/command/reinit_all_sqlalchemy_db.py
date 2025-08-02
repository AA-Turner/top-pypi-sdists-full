from project.core.settings import get_cached_settings
from project.core.util import setup_logging
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db


def __command():
    setup_logging()
    get_cached_settings().raise_if_prod_mode()
    get_cached_sqlalchemy_db().reinit_all()


if __name__ == '__main__':
    __command()
