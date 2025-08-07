from datetime import datetime

from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.messages import ModelMessage
from pydantic_ai.usage import Usage

from tinybird.tb.modules.agent.animations import ThinkingAnimation
from tinybird.tb.modules.agent.models import create_model
from tinybird.tb.modules.agent.prompts import resources_prompt
from tinybird.tb.modules.agent.tools.mock import generate_mock_fixture
from tinybird.tb.modules.agent.utils import TinybirdAgentContext
from tinybird.tb.modules.project import Project

mock_sql_instructions = """
## When generating the SQL query to generate mock data

Given the schema for a Tinybird datasource, return a valid clickhouse sql query to generate some random data that matches that schema.
Response format MUST be just a valid clickhouse sql query.

<example>
    <example_datasource_schema>
SCHEMA >
    experience_gained Int16 `json:$.experience_gained`,
    level Int16 `json:$.level`,
    monster_kills Int16 `json:$.monster_kills`,
    player_id String `json:$.player_id`,
    pvp_kills Int16 `json:$.pvp_kills`,
    quest_completions Int16 `json:$.quest_completions`,
    timestamp DateTime `json:$.timestamp`
    </example_datasource_schema>
    <example_output>

SELECT
    rand() % 1000 AS experience_gained, -- Random experience gained between 0 and 999
    1 + rand() % 100 AS level,          -- Random level between 1 and 100
    rand() % 500 AS monster_kills,      -- Random monster kills between 0 and 499
    concat('player_', toString(rand() % 10000)) AS player_id, -- Random player IDs like "player_1234"
    rand() % 50 AS pvp_kills,           -- Random PvP kills between 0 and 49
    rand() % 200 AS quest_completions,  -- Random quest completions between 0 and 199
    now() - rand() % 86400 AS timestamp -- Random timestamp within the last day
FROM numbers(10)
    </example_output>
</example>

<instructions>
- The query MUST return a random sample of data that matches the schema.
- The query MUST return a valid clickhouse sql query.
- The query MUST be valid for clickhouse and Tinybird.
- FROM numbers([number_of_rows]) part is mandatory.
- If json paths are present (e.g. `userAgent` String `json:$.userAgent`), rely on the json paths to generate the sample record.
- If the schema has nested json paths (e.g. `json:$.location.country`), generate nested JSON objects accordingly.
- Use recent dates to avoid generating dates that are too far in the past.
- Do NOT include ```clickhouse or ```sql or any other wrapping text to the sql query.
- Do NOT use any of these functions: elementAt
- Do NOT add a semicolon at the end of the query
- Do NOT add any FORMAT at the end of the query, because it will be added later by Tinybird.
- Do not use any function that is not present in the list of general functions, character insensitive functions and aggregate functions.
- If the function is not present in the list, the sql query will fail, so avoid at all costs to use any function that is not present in the list.
</instructions>

<more_examples>
# Examples with different schemas, like an array field or a nested JSON field:

## Example schema with an array field:

### Schema:

SCHEMA >
    `order_id` UInt64 `json:$.order_id`,
    `customer_id` UInt64 `json:$.customer_id`,
    `order_date` DateTime `json:$.order_date`,
    `total_amount` Float64 `json:$.total_amount`,
    `items` Array(String) `json:$.items[:]` // This is an array field

### Desired final output of the query:
{
  "order_id": 123456,
  "customer_id": 7890,
  "order_date": "2024-11-30T10:30:00.000Z",
  "total_amount": 150.0,
  "items": ["item1", "item2", "item3"]
}

### Example SQL output with an array field:

SELECT
  concat('ord_', toString(rand() % 10000)) AS order_id,
  concat('cust_', toString(rand() % 10000)) AS customer_id,
  now() - rand() % 86400 AS order_date,
  rand() % 1000 AS total_amount,
  arrayMap(x -> concat('item_', toString(x)), range(1, rand() % 5 + 1)) AS items
FROM numbers(ROWS)

## Example schema with nested JSON paths:

### Schema:

SCHEMA >
    `timestamp` DateTime `json:$.timestamp`,
    `location_country` String `json:$.location.country`,
    `location_region` String `json:$.location.region`,
    `location_city` String `json:$.location.city`,
    `location_latitude` String `json:$.location.latitude`,
    `location_longitude` String `json:$.location.longitude`

### Important: Understanding JSON paths
When you see json paths like `json:$.location.country`, it means the data should be structured as nested JSON:
- `json:$.location.country` → the country field is nested inside the location object
- `json:$.location.region` → the region field is nested inside the location object

### Desired final output structure:
{
  "timestamp": "2024-11-30T10:30:00.000Z",
  "location": {
    "country": "United States",
    "region": "California", 
    "city": "San Francisco",
    "latitude": "37.7749",
    "longitude": "-122.4194"
  }
}

### Example SQL output for nested JSON paths:

SELECT
    timestamp,
    CAST(concat('{
        "country": "', country, '",
        "region": "', region, '",
        "city": "', city, '",
        "latitude": "', latitude, '",
        "longitude": "', longitude, '"
    }'), 'JSON') AS location
FROM
(
    SELECT
        now() - rand() % 86400 AS timestamp,
        ['United States', 'Canada', 'United Kingdom', 'Germany', 'France'][(rand() % 5) + 1] AS country,
        ['California', 'Texas', 'New York', 'Ontario', 'London'][(rand() % 5) + 1] AS region,
        ['San Francisco', 'Los Angeles', 'New York', 'Toronto', 'London'][(rand() % 5) + 1] AS city,
        toString(round(rand() * 180 - 90, 4)) AS latitude,
        toString(round(rand() * 360 - 180, 4)) AS longitude
    FROM numbers(10)
)
</more_examples>
"""


class MockAgent:
    def __init__(
        self,
        dangerously_skip_permissions: bool,
        prompt_mode: bool,
        token: str,
        user_token: str,
        host: str,
        workspace_id: str,
        project: Project,
        thinking_animation: ThinkingAnimation,
    ):
        self.dangerously_skip_permissions = dangerously_skip_permissions or prompt_mode
        self.token = token
        self.user_token = user_token
        self.host = host
        self.workspace_id = workspace_id
        self.project = project
        self.thinking_animation = thinking_animation
        self.messages: list[ModelMessage] = []
        self.agent = Agent(
            deps_type=TinybirdAgentContext,
            instructions=[
                f"""
You are part of Tinybird Code, an agentic CLI that can help users to work with Tinybird.                 
You are a sub-agent of the main Tinybird Code agent. You are responsible for generating mock data for a datasource.
You will be given a datasource name and you will use `generate_mock_fixture` tool to generate a sql query to execute to generate the mock data.
When finish return the result of the mock data generation: the path of the fixture file, the number of rows generated, the datasource name and if the data was appended to the datasource.

# Info
Today is {datetime.now().strftime("%Y-%m-%d")}
""",
                mock_sql_instructions,
            ],
            tools=[
                Tool(
                    generate_mock_fixture,
                    docstring_format="google",
                    require_parameter_descriptions=True,
                    takes_ctx=True,
                ),
            ],
        )

        @self.agent.instructions
        def get_project_files(ctx: RunContext[TinybirdAgentContext]) -> str:
            return resources_prompt(self.project)

    def run(self, task: str, deps: TinybirdAgentContext, usage: Usage):
        result = self.agent.run_sync(
            task,
            deps=deps,
            usage=usage,
            message_history=self.messages,
            model=create_model(self.user_token, self.host, self.workspace_id, run_id=deps.run_id),
        )
        self.messages.extend(result.new_messages())
        return result
