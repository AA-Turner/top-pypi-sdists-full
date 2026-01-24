import asyncio
import asyncio_dgram


async def main():
    c = await asyncio_dgram.connect(("127.0.0.1", 12345))
    print(c.sockname, c.peername, c.socket is None)
    await c.send(b"hi")

    # Force "connection lost"
    c._transport.close()
    try:
        await c.send(b"uh oh")
    except asyncio_dgram.TransportClosed:
        print("ignoring transport closed")
    print(c.sockname, c.peername, c.socket is None)

    await asyncio.sleep(10)
    print(c.sockname, c.peername, c.socket is None)


asyncio.run(main())
