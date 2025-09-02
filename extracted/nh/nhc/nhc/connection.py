import asyncio

class AsyncNetcat:

    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    host: str
    port: int

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        """Establishes an asynchronous connection."""
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    async def send(self, data: bytes):
        """Sends data asynchronously."""
        if self.writer:
            self.writer.write(data)
            await self.writer.drain()

    async def receive(self, num_bytes: int = 1024) -> bytes:
        """Receives data asynchronously."""
        if self.reader:
            return await self.reader.read(num_bytes)
        return b""

    async def receive_line(self) -> str:
        """Receives a single line asynchronously."""
        if self.reader:
            return await self.reader.readline()
        return ""

    async def close(self):
        """Closes the connection."""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

class NHCConnection(AsyncNetcat):
    """ A class to communicate with Niko Home Control. """
    async def send(self, s: str):
        await super().send(s.encode())
        return await self.receive_line()
    
    async def write(self, s: str):
        await super().send(s.encode())
