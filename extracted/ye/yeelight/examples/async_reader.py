import asyncio
import logging
import pprint

from yeelight.aio import AsyncBulb

BULBIP = "192.168.107.116"


logging.basicConfig(level=logging.DEBUG)


def my_callback(data):
    pprint.pprint(data)


async def yeelight_asyncio_demo():
    bulb = AsyncBulb(BULBIP)
    await bulb.async_listen(my_callback)
    print("turn on:", await bulb.async_turn_on())
    await asyncio.sleep(2)
    print("turn off:", await bulb.async_turn_off())
    await asyncio.sleep(2)
    print("turn on:", await bulb.async_turn_on())
    for i in range(10):
        brightness = (i + 1) * 10
        print(
            f"set brightness {brightness}:", await bulb.async_set_brightness(brightness)
        )
        await asyncio.sleep(1)
    await asyncio.sleep(500)
    await bulb.async_stop_listening()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(yeelight_asyncio_demo())
