import logging

from arpakitlib.ar_json_util import transfer_data_to_json_str
from project.core.setup_logging import setup_logging
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db

_logger = logging.getLogger()


def __command():
    setup_logging()
    _logger.info(transfer_data_to_json_str(get_cached_sqlalchemy_db().get_table_name_to_amount()))


if __name__ == '__main__':
    __command()
