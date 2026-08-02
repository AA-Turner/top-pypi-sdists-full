from rich import print

from .exceptions import TrydanError
from .trydan import Trydan


async def trydan_status(ip: str) -> int:
    """Retrieve Trydan Status."""
    async with Trydan(ip) as trydan:
        data = await trydan.get_data()

    print(data)

    return 0


async def trydan_connected(ip: str) -> int:
    """Retrieve Trydan Status."""
    async with Trydan(ip) as trydan:
        await trydan.get_data()

        print(trydan.connected)

    return 0


async def trydan_charging(ip: str) -> int:
    """Retrieve Trydan Status."""
    async with Trydan(ip) as trydan:
        await trydan.get_data()

        print(trydan.charging)

    return 0


async def trydan_ready(ip: str) -> int:
    """Retrieve Trydan Status."""
    async with Trydan(ip) as trydan:
        await trydan.get_data()

        print(trydan.ready)

    return 0


async def trydan_set(ip: str, keyword: str, value: str) -> int:
    """Set KeyWord value in Trydan."""
    async with Trydan(ip) as trydan:
        try:
            await trydan.set_keyword(keyword, value)
        except TrydanError as err:
            print(err)
            return 1
    return 0


async def trydan_pause(ip: str) -> int:
    """Pause Trydan."""
    async with Trydan(ip) as trydan:
        try:
            await trydan.pause()
        except TrydanError as err:
            print(err)
            return 1
    return 0


async def trydan_resume(ip: str) -> int:
    """Resume Trydan."""
    async with Trydan(ip) as trydan:
        try:
            await trydan.resume()
        except TrydanError as err:
            print(err)
            return 1
    return 0


async def trydan_lock(ip: str) -> int:
    """Lock Trydan."""
    async with Trydan(ip) as trydan:
        try:
            await trydan.lock()
        except TrydanError as err:
            print(err)
            return 1

    return 0


async def trydan_unlock(ip: str) -> int:
    """Unlock Trydan."""
    async with Trydan(ip) as trydan:
        try:
            await trydan.unlock()
        except TrydanError as err:
            print(err)
            return 1
    return 0


async def trydan_intensity(ip: str, intensity: int) -> int:
    """Set Intensity in Trydan."""
    async with Trydan(ip) as trydan:
        try:
            await trydan.intensity(intensity)
        except TrydanError as err:
            print(err)
            return 1

    return 0
