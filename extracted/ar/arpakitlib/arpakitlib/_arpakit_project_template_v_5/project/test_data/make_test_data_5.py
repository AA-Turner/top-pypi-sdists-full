import asyncio

from project.core.settings import get_cached_settings


def make_test_data_5():
    get_cached_settings().raise_if_prod_mode()


async def async_make_test_data_5():
    get_cached_settings().raise_if_prod_mode()


def __example():
    make_test_data_5()


async def __async_example():
    await async_make_test_data_5()


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
