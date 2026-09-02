import asyncio

from dotenv import load_dotenv

from novita_sandbox.core.envd.filesystem.filesystem_pb2 import EventType
from novita_sandbox.core import Sandbox as NovitaSandbox
from novita_sandbox.core.envd.filesystem.filesystem_pb2 import EventType
from novita_sandbox.core import Sandbox

load_dotenv()

code = """
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Define the data for the pie chart
categories = ["No", "No, in blue"]
sizes = [90, 10] 

# Step 2: Create the figure and axis objects
fig, ax = plt.subplots(figsize=(8, 8))

plt.xlabel("x")
plt.ylabel("y")

# Step 3: Create the pie chart
ax.pie(sizes, labels=categories, autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors[:len(categories)])

# Step 4: Add title and legend
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.title('Will I wake up early tomorrow?')

# Step 5: Show the plot
plt.show()
"""

code = "print('Hello, world!')"

async def run():
    sbx = Sandbox.create(timeout=60)
    sbx.files.write('/tmp/test.txt', 'Hello, World!')
    content = sbx.files.read('/tmp/test.txt')
    print(content)
    res = sbx.commands.run('ls -la /tmp')
    print(res)
    sbx.kill()

asyncio.run(run())
