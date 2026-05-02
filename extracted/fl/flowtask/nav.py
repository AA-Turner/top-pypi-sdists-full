import asyncio
from qw.discovery import get_server_discovery
from navigator import Application
from navigator.ext.memcache import Memcache
from app import Main


async def start_server(loop):
    transport, discovery_server = await get_server_discovery(event_loop=loop)
    print(':: Starting Discovery Server ::')
    return transport, discovery_server

async def navigator():
    # define new Application
    app = Application(Main, enable_jinja2=True)
    ## installing extensions:
    mcache = Memcache()
    mcache.setup(app)
    # Enable WebSockets Support
    app.add_websockets()

    # # Discovery Server:
    # # Create a background task for service discovery
    # try:
    #     loop = asyncio.get_event_loop()
    # except RuntimeError:
    #     loop = asyncio.new_event_loop
    #     asyncio.set_event_loop(loop)
    # transport, server = await start_server(loop)

    # # Define a cleanup function to close the transport on shutdown
    # async def on_shutdown(app):
    #     transport.close()
    #     print('==== EXIT FROM DataIntegrator =====')

    # # Register the cleanup function
    # app.get_app().on_shutdown.append(on_shutdown)

    # returns App.
    return app.setup()
    # return app
