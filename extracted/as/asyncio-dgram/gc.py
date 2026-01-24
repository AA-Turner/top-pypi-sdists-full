import asyncio
import asyncio_dgram


async def amain() -> None:
    bound = await asyncio_dgram.bind(("127.0.0.1", 5531))
    c = await asyncio_dgram.connect(("127.0.0.1", 5531))

    await asyncio.sleep(1)

    print("done-=---------------------------------------")


if __name__ == "__main__":
    asyncio.run(amain())
