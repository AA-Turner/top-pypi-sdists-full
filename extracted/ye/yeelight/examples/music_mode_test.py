# !!! WARNING !!!
# This code will result in rapid flashing of the light.
# Do not use if you are prone to seizures.
# !!! WARNING !!!
import asyncio
import time

from yeelight import Bulb
from yeelight.aio import AsyncBulb

BULBIP = "10.76.19.240"


def do_nothing(param):
    pass


async def main():
    bulb = AsyncBulb(BULBIP, duration=0)
    await bulb.async_listen(do_nothing)
    await bulb.async_turn_on()
    await bulb.async_get_properties()
    await bulb.async_start_music()
    print(bulb.music_mode)

    counter = 0
    while True:
        # Long enough to test reconnects
        if counter > 200:
            break
        await bulb.async_set_rgb(255, 0, 0)
        counter += 1
        print(counter)
        await asyncio.sleep(0.1)
        await bulb.async_set_rgb(0, 255, 0)
        counter += 1
        print(counter)
        await asyncio.sleep(0.1)
        await bulb.async_set_rgb(0, 0, 255)
        counter += 1
        print(counter)
        await asyncio.sleep(0.1)
    await bulb.async_stop_music()
    await bulb.async_set_rgb(255, 0, 0)
    await bulb.async_stop_listening()


def main_sync():
    bulb = Bulb(BULBIP, duration=0)
    bulb.turn_on()
    bulb.start_music()

    counter = 0
    while True:
        bulb.set_rgb(255, 0, 0)
        counter += 1
        print(counter)
        time.sleep(0.1)
        bulb.set_rgb(0, 255, 0)
        counter += 1
        print(counter)
        time.sleep(0.1)
        bulb.set_rgb(0, 0, 255)
        counter += 1
        print(counter)
        time.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
    main_sync()
