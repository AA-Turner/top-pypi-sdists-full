import asyncio
from flowtask.components.Pokemon import Pokemon


async def check_pokemon():
    pokemon = Pokemon(
        type='health',
        credentials={
            "BASE_URL": "POKEMON_BASE_URL",
            "CLIENT_ID": "POKEMON_CLIENT_ID",
            "CLIENT_SECRET": "POKEMON_CLIENT_SECRET",
        }
    )
    # async context
    async with pokemon as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')

async def get_locations():
    pokemon = Pokemon(
        type='locations',
        credentials={
            "BASE_URL": "POKEMON_BASE_URL",
            "CLIENT_ID": "POKEMON_CLIENT_ID",
            "CLIENT_SECRET": "POKEMON_CLIENT_SECRET",
        }
    )
    # async context
    async with pokemon as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')

async def check_inventory():
    pokemon = Pokemon(
        type='inventory',
        credentials={
            "BASE_URL": "POKEMON_BASE_URL",
            "CLIENT_ID": "POKEMON_CLIENT_ID",
            "CLIENT_SECRET": "POKEMON_CLIENT_SECRET",
        },
        ids=['Q00603']
    )
    # async context
    async with pokemon as comp:
        try:
            result = await comp.run()
            print(len(result), type(result))
            print('RESULT >> ')
            print(result)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    # asyncio.run(check_pokemon())
    # asyncio.run(get_locations())
    asyncio.run(check_inventory())
