from project.core.settings import get_cached_settings
from project.core.util import setup_logging
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db


def __command():
    setup_logging()
    get_cached_settings().raise_if_prod_mode()
    get_cached_sqlalchemy_db().drop()
    get_cached_sqlalchemy_db().drop_celery_tables()
    get_cached_sqlalchemy_db().drop_alembic_tables()


if __name__ == '__main__':
    __command()
