import asyncio
from flowtask.components.RethinkDBQuery import RethinkDBQuery


print(RethinkDBQuery.__mro__)

async def main():
    qry = RethinkDBQuery(
        table='stores_reviews',
        schema='epson',
        columns=['store_id', 'reviews', 'rating', 'user_ratings_total'],
        as_dataframe=True
    )
    async with qry as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
        except Exception as e:
            print(f'Error: {e}')


if __name__ == '__main__':
    asyncio.run(main())
