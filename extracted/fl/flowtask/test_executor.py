import asyncio
from typing import TypeVar, Type
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.asyncio import AsyncIOExecutor

T_aobj = TypeVar('T_aobj', bound='CallableClass')

async def tick():
    print(f"Tick! The async time is {datetime.now()}")

class CallableClass:

    async def __new__(cls: Type[T_aobj], *args, **kwargs) -> T_aobj:
        instance = super().__new__(cls)
        await instance.__ainit__(*args, **kwargs)  # No need to call __init__ manually
        return instance

    def __init__(self, name):
        self.name = name

    async def __call__(self):
        print(f"Running job {self.name} asynchronously.")

    async def __ainit__(self, *args, **kwargs) -> None:
        # Add any additional async initialization logic here
        pass

async def main():
    # Create instance of callable class
    instance = await CallableClass("MyJob")
    print('HERE > ', asyncio.iscoroutinefunction(instance.__call__))  # Correct check

    # Create scheduler
    scheduler = AsyncIOScheduler(executors={"default": AsyncIOExecutor()})

    # Add job, explicitly wrapping in ensure_future to avoid warnings
    scheduler.add_job(lambda: asyncio.ensure_future(instance()), 'interval', seconds=10)

    # Add tick
    scheduler.add_job(tick, 'interval', seconds=3)

    # Start scheduler
    scheduler.start()

    # Run the event loop for a minute
    await asyncio.sleep(60)

if __name__ == '__main__':
    try:
        asyncio.run(main())  # Simplified event loop management
    except KeyboardInterrupt:
        pass
