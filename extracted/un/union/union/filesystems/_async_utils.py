import asyncio
from concurrent.futures import ThreadPoolExecutor


def create_channel_with_loop(loop, create_channel, *args, **kwargs):
    """Calls create_channel in another thread that sets `loop` to that's thread's event loop.

    This is useful with `grpc.aio.secure_channel`, which grabs the thread-local event loop
    https://github.com/grpc/grpc/blob/c938a7b564eebbd9f8eef8718e2d70e0bd35f093/src/python/grpcio/grpc/_cython/_cygrpc/aio/common.pyx.pxi#L177-L194
    """

    def create_channel_worker(loop_, *args, **kwargs):
        asyncio.set_event_loop(loop_)
        return create_channel(*args, **kwargs)

    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(create_channel_worker, loop, *args, **kwargs)
    return future.result()


async def if_coro(result):
    if asyncio.iscoroutine(result):  # or inspect.iscoroutine,... and so on
        return await result
    else:
        return result
