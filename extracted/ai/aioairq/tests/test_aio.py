import asyncio
import aiohttp
from aioairq import AirQ

ADDRESS = "airq"
PASSWORD = "bad-air-room"

async def main():
    async with aiohttp.ClientSession(cookie_jar=aiohttp.DummyCookieJar()) as session:
        airq = AirQ(ADDRESS, PASSWORD, session)

        config = await airq.get("config")
        print(f"Available sensors: {config['sensors']}")

asyncio.run(main())

