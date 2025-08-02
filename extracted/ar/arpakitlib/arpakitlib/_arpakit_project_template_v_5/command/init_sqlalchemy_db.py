from project.core.util import setup_logging
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db


def __command():
    setup_logging()
    get_cached_sqlalchemy_db().init()


if __name__ == '__main__':
    __command()
