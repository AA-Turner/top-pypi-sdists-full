"""Add a memory, then recall it.

SUPERMEMORY_API_KEY=... uv run examples/quickstart.py
"""

import time

from supermemory import Supermemory

client = Supermemory()
namespace = "example_user"

added = client.add(namespace, content="Alex prefers morning meetings and hates Mondays.", id="alex-prefs")
print(f"added {added.id} ({added.status})")

# Ingestion is asynchronous; give it a moment before recalling.
time.sleep(5)

response = client.search(namespace, query="When does Alex like to meet?", limit=3)
for result in response.results:
    print(f"{result.similarity:.2f}  {result.memory or result.chunk}")
