import asyncio
import logging

from project.core.settings import get_cached_settings
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import ApiKeyDBM

_logger = logging.getLogger(__name__)


def make_test_api_keys():
    get_cached_settings().raise_if_prod_mode()
    with get_cached_sqlalchemy_db().new_session() as session:
        session.query(ApiKeyDBM).delete()
        session.commit()
        for i in range(1000):
            api_key = ApiKeyDBM(value=str(i + 1))
            session.add(api_key)
            _logger.info(api_key)
        session.commit()


async def async_make_test_data_1():
    get_cached_settings().raise_if_prod_mode()


def __example():
    make_test_api_keys()


async def __async_example():
    await async_make_test_data_1()


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
