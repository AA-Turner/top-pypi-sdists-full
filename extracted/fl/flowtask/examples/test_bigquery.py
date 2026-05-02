import asyncio
from asyncdb import AsyncDB
from asyncdb.drivers.bigquery import bigquery
from flowtask.conf import (
    BIGQUERY_DEFAULT_CREDENTIALS,
    BIGQUERY_DEFAULT_PROJECT
)

# create a pool with parameters
params = {
    "credentials": str(BIGQUERY_DEFAULT_CREDENTIALS),
    "project_id": BIGQUERY_DEFAULT_PROJECT
}

async def connect_using_bq():
    db = bigquery(params=params)
    async with await db.connection() as conn:
        print(
            f"Connected: {conn.is_connected()}"
        )

async def connect_using_abs():
    db = AsyncDB('bigquery', params=params)
    async with await db.connection() as conn:
        print(
            f"Connected: {conn.is_connected()}"
        )

if __name__ == '__main__':
    asyncio.run(
        connect_using_bq()
    )
    asyncio.run(
        connect_using_abs()
    )
