from crewai.flow import Flow, start, listen
from typing import Optional
import asyncio
from pydantic import BaseModel


class ParallelFlow(Flow):
    @start()
    def begin_process(self):
        print("Starting the process...")
        return "process_started"

    @listen("begin_process")
    async def process_data_1(self, trigger_result):
        print(f"Listener 1 received: {trigger_result}")
        await asyncio.sleep(2)  # Simulate work
        print("Data 1 processed")
        return "data_1_complete"

    @listen("begin_process")
    async def process_data_2(self, trigger_result):
        print(f"Listener 2 received: {trigger_result}")
        await asyncio.sleep(1)  # Simulate work
        print("Data 2 processed")
        return "data_2_complete"

    @listen("begin_process")
    async def process_data_3(self, trigger_result):
        print(f"Listener 3 received: {trigger_result}")
        await asyncio.sleep(3)  # Simulate work
        print("Data 3 processed")
        return "data_3_complete"


# Usage example
flow = ParallelFlow()
result = flow.kickoff()
print(f"Flow completed with state: {flow.state}")
