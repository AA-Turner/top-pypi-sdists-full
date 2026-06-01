"""
Demonstrates the smplkit runtime SDK for Smpl Logging.

Prerequisites:
    - ``pip install smplkit-sdk``
    - A valid smplkit API key, provided via one of:
        - ``SMPLKIT_API_KEY`` environment variable
        - ``~/.smplkit`` configuration file (see SDK docs)

Usage::

    python examples/logging_runtime_showcase.py
"""

import asyncio

from smplkit import AsyncSmplClient


async def main() -> None:

    # create the client (use SmplClient for synchronous use)
    async with AsyncSmplClient(
        environment="production", service="showcase-service"
    ) as client:
        await client.logging.install()
        print("All loggers are now controlled by smplkit")


if __name__ == "__main__":
    asyncio.run(main())
