# Copyright 2023 Canonical Ltd.
# Licensed under the Apache V2, see LICENCE file for details.

import asyncio

from juju.model import Model


async def status():
    model = Model()
    await model.connect()

    status = await model.get_status()
    await model.disconnect()

    print("Applications:", list(status.applications.keys()))
    print("Machines:", list(status.machines.keys()))
    print("Relations:", status.relations)

    return status


if __name__ == "__main__":
    asyncio.run(status())
