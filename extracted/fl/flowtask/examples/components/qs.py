import asyncio
from flowtask.components.QS import QS


async def query():
    qs = QS(
        query="troc_mileage.tpl",
        from_templates_dir=True,
        conditions={
            "tenant": "pokemon",
            "firstdate": "{first}",
            "lastdate": "{last}",
            "forms": [4193]
        },
        program="troc",
        masks={
            "first": [
                "date_diff_dow",
                {
                    "day_of_week": "monday",
                    "diff": 8,
                    "mask": "%Y-%m-%d"
                }
            ],
            "last": [
                "date_diff_dow",
                {
                    "day_of_week": "monday",
                    "diff": 2,
                    "mask": "%Y-%m-%d"
                }
            ]
        }
    )
    async with qs as comp:
        print(comp)


async def pokemon_tickets():
    qs = QS(
        query="pokemon_tickets.tpl",
        program="pokemon"
    )
    async with qs as comp:
        print(comp)

if __name__ == '__main__':
    asyncio.run(pokemon_tickets())
