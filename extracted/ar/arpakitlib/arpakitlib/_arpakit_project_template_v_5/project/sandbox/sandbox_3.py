import asyncio

from arpakitlib.ar_pydantic_schema_from_sqlalchemy_model import pydantic_schema_from_sqlalchemy_model
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM


def __sandbox():
    a = pydantic_schema_from_sqlalchemy_model(sqlalchemy_model=UserDBM, include_defaults=True)
    print(a())


async def __async_sandbox():
    pass


if __name__ == '__main__':
    __sandbox()
    asyncio.run(__async_sandbox())
