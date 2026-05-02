# -*- coding: utf-8 -*-
"""Flowtask is a tool for execution of Tasks.

Flowtask can execute DAG (Directed Acyclic Graph) tasks declared in a variety of formats.
  - YAML
  - JSON
  - TOML
Flowtask is designed to be used as a library or command-line tool.

Usage Example:

A Flowtask Task is a component-based declarative workflow that can be executed from the command line or API.

```yaml title="programs/test/tasks/sentiment_analysis.yaml"
# filename: sentiment_analysis.yaml
name: An Example Task for Sentiment Analysis
description: Preparing The Information for Sentiment Analysis
steps:
  - RethinkDBQuery:
      table: test_data
      schema: default
  - tExplode:
      column: reviews
      drop_original: false
  - SentimentAnalysis:
      text_column: text
      sentiment_model: "tabularisai/robust-sentiment-analysis"
      sentiment_levels: 5
      emotions_model: "bhadresh-savani/distilbert-base-uncased-emotion"
  - CopyToRethink:
      tablename: sentiment_analysis
      schema: default
```

The above example is a simple task that reads data from a RethinkDB table,
explodes the reviews column, performs sentiment analysis,
and copies the results to another RethinkDB table.

For execution we can use a command-line tool:
```bash
task --program=test --task=sentiment_analysis --no-worker
```

Or we can use the Python API:
```python
from flowtask.runner import TaskRunner

runner = Runner(program='test', task='sentiment_analysis', no_worker=True)
async with runner as job:
    if await job.start():
        await job.run()
```

or even call it from a REST API:
```python
import aiohttp
async def run_task(program, task):
    async with aiohttp.ClientSession() as session:
    async with session.post(
            'http://localhost:8080/api/v1/tasks',
            json={'program': program, 'task': task}
        ) as response:
        return await response.json()

async def main():
    result = await run_task('test','sentiment_analysis')
    print(result)

asyncio.run(main())
```

This code will execute the `sentiment_analysis` task using the `test` program and will print the results to the console.
"""

## more information
from .version import (
    __title__,
    __description__,
    __version__,
    __author__,
    __author_email__,
    __copyright__,
    __license__
)


def version():
    """version.
    Returns:
        str: current version of Navigator flowtask.
    """
    return __version__
