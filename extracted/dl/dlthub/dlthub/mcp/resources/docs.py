# ruff: noqa: F401, E501, W291, W293

from mcp.server.fastmcp.resources.types import TextResource


# TODO determine a principled approach to get the version associated with the `dlt` version
# TODO glossary could be part of the "rules" / system prompt
# TODO use tags set on the original docs to facilitat retrieval
# TODO register subheaders such as "docs.glossary.resource" as resource(docs://core/glossary/resource)


def glossary() -> TextResource:
    content = """
# Glossary
## Source
- A location with structured data, organized into resources.
  - API with endpoints
  - Spreadsheet with tabs
  - Database with tables
- Refers to the software component extracting data from a source.

## Resource
- Logical grouping of similar data within a source.
  - API endpoint
  - Spreadsheet tab
  - Database table
- Refers to the software component extracting data from the source.

## Destination
- Data store where source data is loaded, e.g., Google BigQuery.

## Pipeline
- Transfers data from the source to the destination, following schema instructions (extracting, normalizing, loading data).

## Verified Source
- A Python module from `dlt init` for creating pipelines extracting data from a specific Source.
- Must be published to be "verified" with tests, test data, scripts, documentation, and reviewed datasets.

## Schema
- Describes the structure of normalized data (tables, column types).
- Provides instructions for processing and loading data into the destination.

## Config
- Runtime values that can change pipeline behavior between environments (e.g., local vs. production).

## Credentials
- A configuration subset with elements kept secret and never shared in plain text.
"""
    return TextResource(
        text=content,
        name="docs.glossary",
        uri="docs://core/glossary",
        mime_type="text/markdown",
    )


def pipeline() -> TextResource:
    content = """
# Pipeline
## Overview
A `pipeline` in `dlt` moves data from Python to a [destination](glossary.md#destination). It accepts `dlt` [sources](source.md), [resources](resource.md), generators, lists, and iterables. Running a pipeline evaluates resources and loads data into the destination.

### Example
```py
import dlt

pipeline = dlt.pipeline(destination="duckdb", dataset_name="sequence")
info = pipeline.run([{'id':1}, {'id':2}, {'id':3}], table_name="three")
print(info)
```

## Creating a Pipeline
To instantiate a pipeline, use `dlt.pipeline()` with:

- pipeline_name: Identifies the pipeline in logs and monitoring. Defaults to the script filename if omitted.
- destination: Target destination for data. Can be set later in `run()`.
- dataset_name: Logical group of tables (e.g., a database schema). Defaults to `{pipeline_name}_dataset` when required.

## Running a Pipeline
Call `run(data, **kwargs)` to load data.

### Parameters:
- data: `dlt` source, resource, generator, iterator, or iterable.
- write_disposition (default: `append`):
  - `append`: Adds new data.
  - `replace`: Replaces existing data.
  - `skip`: Skips loading.
  - `merge`: Deduplicates/merges using `primary_key` and `merge_key`.
- table_name: Explicitly sets table name if it can't be inferred.

### Example
```py
import dlt

def generate_rows(n):
    for i in range(n):
        yield {'id': i}

pipeline = dlt.pipeline(destination='bigquery', dataset_name='sql_data')
info = pipeline.run(generate_rows(10))
print(info)
```

## Pipeline Working Directory
Each pipeline stores extracted files, schemas, execution traces, and state in `~/.dlt/pipelines/<pipeline_name>`.

- Use `dlt pipeline info` or inspect programmatically.
- Override with `pipelines_dir` when creating the pipeline.
- Attach an instance to an existing working folder using `dlt.attach`.

### Separate Environments with `pipelines_dir`
Run multiple pipelines with the same name but different configurations (e.g., dev/staging/prod) by setting `pipelines_dir`.
```py
import dlt
from dlt.common.pipeline import get_dlt_pipelines_dir

pipelines_dir = os.path.join(get_dlt_pipelines_dir(), "dev")
pipeline = dlt.pipeline(destination="duckdb", dataset_name="sequence", pipelines_dir=pipelines_dir)
```

## Development Mode
To reset state and load data into a new dataset on every run, set `dev_mode=True`.

## Refreshing Data and State
Use `refresh` in `pipeline.run()` or `extract()` to reset sources/resources:

| Mode | Effect |
|------|--------|
| `drop_sources` | Drops all tables and pipeline state for sources in `run()`. |
| `drop_resources` | Drops tables and resource state only for selected resources. |
| `drop_data` | Truncates tables but retains schema; resets incremental states. |

### Example
```py
pipeline.run(airtable_emojis(), refresh="drop_sources")
```
"""
    return TextResource(
        text=content,
        name="docs.pipeline",
        uri="docs://core/pipeline",
        mime_type="text/markdown",
    )


def full_loading() -> TextResource:
    content = """
# Full Loading
## Overview
Full loading in dlt refers to completely reloading data in tables by removing existing data and replacing it with new data from the source. Resources not selected during this process will retain their data at the destination.

## Performing a Full Load
To execute a full load, use `write_disposition='replace'` with your resource:

```python
p = dlt.pipeline(destination="bigquery", dataset_name="github")
# Your data retrieval code here
p.run(issues, write_disposition="replace", primary_key="id", table_name="issues")
```

## Replace Strategies for Full Load
dlt provides three strategies for full load: `truncate-and-insert`, `insert-from-staging`, and `staging-optimized`. The strategies ensure different performance and data consistency levels, which may vary across destinations.

Configure the strategy in `config.toml`:

```toml
[destination]
replace_strategy = "staging-optimized"
```

### Strategies Explained
- truncate-and-insert: Default, fastest, truncates tables before loading new data. Risk of downtime during load.
- insert-from-staging: Slowest, loads data into staging first, then inserts in one transaction, ensuring zero downtime.
- staging-optimized: Benefits from `insert-from-staging` but optimized for faster loading. May drop and recreate tables, affecting views and constraints. Behaves differently per destination:
  - Postgres: Replaces tables directly.
  - BigQuery: Uses a [clone command](https://cloud.google.com/bigquery/docs/table-clones-create) for table replacement.
  - Snowflake: Similar cloning [command](https://docs.snowflake.com/en/sql-reference/sql/create-clone).

Check individual destination documentation for specific implementations or fallbacks to `insert-from-staging`.
"""
    return TextResource(
        text=content,
        name="docs.full_loading",
        uri="docs://core/full_loading",
        mime_type="text/markdown",
    )


def incremental_loading() -> TextResource:
    content = """
# Incremental Loading
## Overview
Incremental loading transfers only new or changed data, offering low-latency and cost-effective data operations. Here's a concise guide on how to efficiently manage incremental loading using different strategies and tools available in dlt.

## Write Dispositions
### Options
1. Full Load: Replaces the entire dataset (`write_disposition='replace'`).
2. Append: Simply appends new data (`write_disposition='append'`).
3. Merge: Incorporates new data using keys for upserts and deduplication (`write_disposition='merge'`).

### Decision Flow
- Determine if the data is stateful or stateless.
- For stateful data, assess if incremental extraction is possible.

## Merge Strategies
### Strategies
1. Delete-Insert: Default strategy for deduplication.
2. SCD2: Tracks historical changes.
3. Upsert: Updates if a key exists, or inserts otherwise.

### Key Points
- Proper indexing speeds up lookups.
- Merge strategies require managing keys and deduplication marks.
- Configure aspects like data validity, record deletion, and row hashing for advanced operations.

## Incremental Loading with API Cursors
### Steps
1. Identify cursor field (e.g., `updated_at`).
2. Fetch records incrementally using this cursor.
3. `dlt` manages deduplication and tracks state.

### Example
```python
@dlt.resource(primary_key="id")
def repo_issues(updated_at=incremental("updated_at")):
    for page in fetch_issues(since=updated_at.start_value):
        yield page
```

## Handling Backfills and Airflow Integration
### Backfills
- Define ranges using `initial_value` and `end_value`.
- Run them independently of incremental loads.

### Airflow
- Utilize `allow_external_schedulers=True` to let Airflow control batch periods.
- Develop separate DAGs for backfill and incremental processes.

## Custom Implementations
### Use of Pipeline State
- Store fresh state variables during data loading.
- Use `dlt.current.resource_state()` for state management.

### Troubleshooting
- Ensure consistent configurations between runs.
- Check logs for incremental binding messages and state updates.
"""
    return TextResource(
        text=content,
        name="docs.incremental_loading",
        uri="docs://core/incremental_loading",
        mime_type="text/markdown",
    )


def resource() -> TextResource:
    content = """
# Resource
## Overview
A resource in `dlt` is a function that yields data, typically defined using the `@dlt.resource` decorator. It can be sync or async. Resources can be standalone, or grouped under a `@dlt.source`.

## Resource Definition
### Declaring a Resource
Key arguments include:
- `name`: Specifies the generated table's name.
- `write_disposition`: Determines how the data is loaded, with options such as `append`, `replace`, and `merge`.

### Schema Definition
`dlt` infers table schemas from resource data. You can customize it using hints for table names, primary or merge keys, and column definitions. 

### Using Pydantic for Schema
You can define schema using Pydantic models, allowing inferred data types and constraints like nullability and unions.

### Data Loading Strategies
- Dispatch to Multiple Tables: The `table_name` argument allows dynamic table dispatch based on data attributes.
- Parallel and Async Resource Handling: Enable parallel extraction by setting `parallelized=True` or use `async` functions.

### Transformer Utilization
Transformers can use output from one resource as input to another. They can modify, filter, or augment data on the fly.

## Advanced Features
### Sampling and Limits
`add_limit` allows sampling of data for testing and exploratory analysis.

### Schema Adjustments
Schema and table names can be adjusted dynamically during data extraction using `apply_hints` or `dlt.mark.with_hints`.

### External File Import
`dlt` supports importing external files in various formats, with optional schema hints or dynamic schema sniffing.

### Resource Customization
- Filter, Transform & Pivot: Apply filters and transformations for data processing.
- Table Nesting Control: Limit nesting levels for clarity and manageability, especially for deeply structured data sources.

### Special Operations
- Resource Duplication: Copy and rename resources for cases like multi-instance generic sources.
- Loader File Format Preference: Opt for specific file formats per resource per destination capabilities.
- Full Data Refresh: Perform full refreshes via settings in the `run` method for complete data regeneration.
"""
    return TextResource(
        text=content,
        name="docs.resource",
        uri="docs://core/resource",
        mime_type="text/markdown",
    )


def source() -> TextResource:
    """Document for @dlt.source"""
    content = """
# Source
## Overview
The `dlt` source represents a logical grouping of API resources, often defined in a separate Python module. It is mainly used to configure API interaction and data extraction.

### Key Features:
- Decoration: A function decorated with `@dlt.source` returns resources (e.g., API endpoints).
- Schema: Optionally define a schema for data organization and optimization.
- Customization: Include data transformations, authentication, pagination, etc.
  
## Declare Sources
Declare sources using `@dlt.source` on a (possibly async) function that yields resources.

### Dynamic Resource Creation
Utilize `dlt.resource` within a source to dynamically create resources from functions.
```python
@dlt.source
def hubspot(api_key=dlt.secrets.value):
    ...
    for endpoint in endpoints:
        yield dlt.resource(get_resource(endpoint), name=endpoint)
```

## Customize Sources
### Access and Load Resources
Access and specify which resources to load:
```python
from hubspot import hubspot

source = hubspot()
print(source.resources.keys())
pipeline.run(source.with_resources("companies", "deals"))
```

### Data Transformation and Filtering
Transform and filter resource data:
```python
source.deals.add_filter(lambda deal: deal["created_at"] > yesterday)
```

### Partial Data Loading
Limit data extraction using `add_limit` for resource testing:
```python
pipeline.run(pipedrive_source().add_limit(10))
```

### Resource Addition
Add custom resources post-creation to a source:
```python
source.resources.add(source.deals | deal_scores)
pipeline.run(source)
```

### Source Renaming
Rename sources and configure them separately:
```python
my_db = sql_database.clone(name="my_db")
```

## Advanced Configuration
### Schema and Nesting
Control table nesting and schema manipulation for clearer data representation:
```python
@dlt.source(max_table_nesting=1)
def mongo_db():
    ...
```

### Full Refresh
Force a full refresh by replacing data:
```python
pipeline.run(merge_source(), write_disposition="replace")
```

## Loading Sources
Load sources into a dataset in `dlt.pipeline`, or decompose a source for parallel processing:
```python
resource_list = sql_source().resources.keys()
for res in resource_list:
    pipeline.run(sql_source().with_resources(res))
```

This documentation provides a detailed but concise explanation of how to use the dlt source feature for effective data loading with potential customizations and advanced configurations.
"""
    return TextResource(
        text=content,
        name="docs.source",
        uri="docs://core/source",
        mime_type="text/markdown",
    )


def destination() -> TextResource:
    content = """
# Destination
## Overview

Destinations in `dlt` are locations where data is loaded and schemas are maintained. They can include databases, data lakes, vector stores, or files.

## Declaring a Destination
- Shorthand Type: Used for built-in destinations.
- Destination Factory Type: Allows use of built-in or custom implementations by declaring a factory type.
- Importing Destination Factory: You can import destination modules, allowing fine-tuned configurations and explicit parameter settings.

### Explicit Configuration and Naming
You can instantiate a destination factory directly for better control and configuration. Naming is crucial for distinguishing between different environments (e.g., dev, staging, production).

## Configuration
### Methods
- Files (TOML): Recommended for setting default configurations.
- Environment Variables: Another method for setting configuration.

### Named Destinations
For named destinations, configurations are structured under the destination's name in the file.

## Credentials
Credentials can be passed explicitly at instance creation, replacing older methods using `credentials` argument in the pipeline.

## Capabilities and Parameters
- Inspecting Capabilities: Understand what a destination supports (e.g. file formats, identifier length) by inspecting its capabilities.
- Configuring Multiple Destinations: Configure credentials in a TOML file for pipelines with multiple destinations.

## Accessing Destinations
`dlt` accesses a destination during the `run`, `sync_destination`, and `load` methods. This ensures the pipeline state aligns with the destination without unnecessary dependencies.

## Naming Conventions
`dlt` maps data source identifiers to destination identifiers using naming conventions to ensure compatibility. Each destination can have default or custom naming conventions set. 

### Case Sensitivity
- Some destinations support case-sensitive identifiers, configurable through the destination factory or configuration files.

## Creating New Destinations
Two methods for implementing a new destination:
1. Sink Function (`@dlt.destination`): For reverse ETL destinations.
2. Full Destination: For detailed control over jobs and schema migration.

This documentation serves as a comprehensive guide for setting up and configuring data destinations within a `dlt` pipeline, ensuring flexibility and control over data management processes.
"""
    return TextResource(
        text=content,
        name="docs.destination",
        uri="docs://core/destination",
        mime_type="text/markdown",
    )


def naming() -> TextResource:
    content = """
# Naming Convention
The `dlt` library translates source identifiers from JSON documents into destination formats like tables and column names. Here's an overview of how naming conventions work within `dlt`, with a focus on the translation and configuration of identifiers. 

## Naming Convention Overview
- Source vs. Destination Identifiers: Identifiers in source data can be diverse, while destination systems have strict naming requirements. `dlt` uses naming conventions to bridge this gap.
- Default Naming Convention: The default convention is `snake_case`, which maps identifiers into a case-insensitive, simplified format.
- Customization: Users can choose among provided naming conventions or create custom ones.

## Default Naming Convention: snake_case
- Converts identifiers to lowercase and replaces unsupported characters with underscores.
- Special character replacements: `+` and `*` to `x`, `-` to `_`, `@` to `a`, `|` to `l`.
- Appends `_` to names starting with numbers and ensures no consecutive underscores.

## Customizing Naming Conventions
### Configuration
- Global and Source-specific Settings: Configure conventions globally using `config.toml` or set per data source.
- Environment Variables: Change globally through `SCHEMA__NAMING`.

### Predefined and User-defined Options
- Available Conventions: Options include `snake_case`, `duck_case`, `direct`, `sql_cs_v1`, `sql_ci_v1`.
- Ignoring Norms for `dataset_name`: Control normalization for dataset names separately, with options to preserve original casing.

### Handling Identifiers
- Identifier Shortening: Occurs during normalization to prevent exceeding destination limits.
- Compound Identifiers: Nested and flattened identifiers use double underscores as path separators.

### Collision Management
- Identifies collisions between naming conventions and existing tables to prevent data corruption.

## Advanced Features
- Case Sensitivity Control: Some destinations handle identifiers differently (e.g., Snowflake uppercase), with conventions to manage this.
- User-defined Conventions: Implement custom conventions by creating a class extending `NamingConvention` and configuring `dlt` accordingly.

By understanding and utilizing these naming conventions, users can streamline their data flows between different source and destination formats efficiently with `dlt`.
"""
    return TextResource(
        text=content,
        name="docs.naming",
        uri="docs://core/naming",
        mime_type="text/markdown",
    )


def state() -> TextResource:
    content = """
# State
## Overview
The dlt pipeline state is a Python dictionary that accompanies your data and allows for persistent storage and retrieval of values across pipeline runs.

## State Management in Resources
### Reading and Writing State
In resources, you can manage state by reading and writing to it. For example, tracking chess game archives to prevent processing duplicates:

```python
@dlt.resource(write_disposition="append")
def players_games(chess_url, player, start_month=None, end_month=None):
    # manage state within the resource
    checked_archives = dlt.current.resource_state().setdefault("archives", [])
    archives = _get_players_archives(chess_url, player)
    for url in archives:
        if url in checked_archives:
            print(f"skipping archive {url}")
            continue
        else:
            print(f"getting archive {url}")
            checked_archives.append(url)
        r = requests.get(url)
        r.raise_for_status()
        yield r.json().get("games", [])
```

### Key Points
- The state is stored locally in the [pipeline working directory](pipeline.md#pipeline-working-directory).
- Data stored must be JSON serializable.

## Sharing State Across Resources
State can also be shared across resources and accessed with `dlt.current.source_state()`. This is useful for shared data like mappings of custom fields.

### Example
Access an example of state sharing in the [pipedrive source](https://github.com/dlt-hub/verified-sources/blob/master/sources/pipedrive/__init__.py#L118).

## Syncing State with Destination
In environments where the file system is not preserved, such as Airflow, dlt can sync state with the destination. The state is stored in the `_dlt_pipeline_state` table.

- Sync Command: `dlt pipeline sync` [retrieve state](../reference/command-line-interface.md#dlt-pipeline-sync).
- Disable Sync: Set `restore_from_destination=false` for persistent working directories.

## When to Use Pipeline State
- For incremental loading of last values.
- Store processed entities if manageable size.
- Track values for custom implementations beyond standard constructs.

## Limitations
Avoid using state for large datasets exceeding millions of records. Alternatives:
- Use external storage like DynamoDB or Redis.
- Use `dlt.current.pipeline()` for accessing data directly from the destination.

### Example
Accessing recent comments for processing:

```python
import dlt

@dlt.resource(name="user_comments")
def comments(user_id: str):
    current_pipeline = dlt.current.pipeline()
    max_id: int = 0
    if not current_pipeline.first_run:
        user_comments = current_pipeline.dataset().user_comments
        max_id_df = user_comments.filter(user_comments.user_id == user_id).select(user_comments["_id"].max()).df()
        max_id = max_id_df[0][0] if len(max_id_df.index) else 0

    yield from [
        {"_id": i, "value": letter, "user_id": user_id}
        for i, letter in zip([1, 2, 3], ["A", "B", "C"])
        if i > max_id
    ]
```

## Inspecting and Resetting Pipeline State
### Inspection
- Use the command: `dlt pipeline -v chess_pipeline info` for state inspection.

### Reset
- Full Reset: Drop the destination dataset, enable `dev_mode`, or use `dlt pipeline drop --drop-all`.
- Partial Reset: Use `dlt pipeline drop <resource_name>` or `dlt pipeline drop --state-paths` for specific state paths.
"""
    return TextResource(
        text=content,
        name="docs.state",
        uri="docs://core/state",
        mime_type="text/markdown",
    )


def schema() -> TextResource:
    content = """
# Schema
## Overview
The schema in the `dlt` library describes the structure of normalized data and provides instructions for data processing and loading. It is generated during normalization and can be customized using hints. Schemas can be exported, imported, and modified directly.

## Schema Components
### Content Hash and Version
- version_hash: Detects manual changes and synchronizes with the destination database schema.
- numeric version: Increases with schema updates for human-readability.

### Naming Convention
- Converts identifiers to snake_case and removes non-ASCII characters.
- Customizable to fit destination requirements.

### Data Normalizer
- Transforms input data into a structure compatible with the destination.
- Configurable to handle nested tables or generate different structures.

### Tables and Columns
- Tables: Contain properties like name, description, columns, and various hints.
- Columns: Include name, data type, and additional properties like precision and nullability.

### Variant Columns
- Created when data cannot be coerced into existing columns.

### Data Types
- Includes various types such as `text`, `double`, `bool`, `timestamp`, etc.
- Supports precision and scale for specific types.

## Table References
### Nested References
- Automatically created from nested data and linked via nested references.

### Table References
- Optional user-defined annotations for downstream processes.

## Configuration
### Schema Settings
- Type autodetectors: Functions to infer data types from values.
- Column hint rules: Apply global hint rules to columns.
- Preferred data types: Set default data types for columns based on name patterns.

### Direct Application
- Apply data types and hints directly using the `@dlt.resource` decorator and `apply_hints`.

## Schema Management
### Export/Import
- Guide available for exporting and importing schema YAML files.

### Attaching Schemas to Sources
- Schemas can be implicitly created or loaded from files.
- Can be modified within the source function body using `dlt.current.source_schema()`.

This structured overview provides a comprehensive understanding of schemas in the `dlt` library, offering insights into configuration, application, and management for efficient data loading processes.
"""
    return TextResource(
        text=content,
        name="docs.schema",
        uri="docs://core/schema",
        mime_type="text/markdown",
    )


def schema_contracts() -> TextResource:
    content = """
# Schema Contracts
`dlt` handles schema evolution at the destination by aligning with the structure and data types of the extracted data. This can be controlled using different schema contract modes.

## Contract Modes
- evolve: Accepts all schema changes.
- freeze: Prevents any schema changes; incompatible data results in exceptions.
- discard_row: Discards rows violating the schema.
- discard_value: Discards non-conforming data values from rows.

### Controlling Schema Entities
Schema entities include:
- tables: Contract is applied when new tables are created.
- columns: Contract is applied when new columns are created.
- data_type: Contract is applied to data type mismatches.

### Setting Schema Contracts
Use the `schema_contract` argument in:
- `dlt.resource()` for individual resources.
- `dlt.source()` for all resources in a source.
- `pipeline.run()` to override existing settings.

### Argument Forms
1. Full: Mapping of schema entities to modes.
2. Shorthand: Single mode applied to all entities.

### Example
```python
@dlt.resource(schema_contract={"tables": "discard_row", "columns": "evolve", "data_type": "freeze"})
def items():
    ...
```

## Pydantic for Data Validation
Pydantic models can define table schemas and validate data. Contracts conform to default Pydantic behavior or can be explicitly defined. 

### Column Mode to Pydantic Mapping
| Column Mode   | Pydantic Extra Mode |
|---------------|---------------------|
| evolve        | allow               |
| freeze        | forbid              |
| discard_value | ignore              |
| discard_row   | forbid              |

## Contract Application on Arrow Tables and Pandas
Schema contracts apply similarly to Arrow tables and pandas frames:
- tables: Work identically irrespective of data item type.
- columns: Allow new columns or raise exceptions as needed.

## Handling Schema Validation Errors
In freeze mode, violations raise `DataValidationError`, accessible via `PipelineStepFailed`.

### Example
```python
try:
    pipeline.run()
except PipelineStepFailed as pip_ex:
    ...
```

## Special Cases
- **New Tables**: Allows new columns if a table is considered new.
- **Manual Adjustments**: If manually adjusted, ensure `evolve` mode initially to avoid exceptions.

## Examples
### Ignoring New Subtables
```python
@dlt.resource(schema_contract={"tables": "discard_row", "columns": "evolve", "data_type": "freeze"})
def items():
    ...
```

### Freezing Schema
```python
pipeline.run(my_source, schema_contract="freeze")
```

### Override Example
```python
@dlt.source(schema_contract={"columns": "freeze", "data_type": "freeze"})
def frozen_source():
  return [items(), other_items()]

pipeline.run(frozen_source())
```
"""
    return TextResource(
        text=content,
        name="docs.schema.contracts",
        uri="docs://core/schema/contracts",
        mime_type="text/markdown",
    )


def schema_evolution() -> TextResource:
    content = """
# Schema Evolution
## Overview
Schema evolution is essential for managing changes in data structure over time. It enables maintainability by separating the technical challenge of "loading" data from the business challenge of "curating" data. This separation allows different stakeholders to manage different stages of data processing.

## Using Schema Evolution in `dlt`
`dlt` automatically infers and evolves schemas as the structure of data changes. This includes handling new columns, datatype changes, and adjusting for removed or renamed columns without slowing down the data processing pipeline.

## Initial Schema Inference
During the initial pipeline run, `dlt` scans data and generates a schema by flattening nested dictionaries and unpacking lists into sub-tables. Here's a sample schema transformation of nested data to a relational format using `dlt`:

```py
data = [{
    "organization": "Tech Innovations Inc.",
    "address": {
        'building': 'r&d',
        "room": 7890,
    },
    "Inventory": [
        {"name": "Plasma ray", "inventory nr": 2411},
        {"name": "Self-aware Roomba", "inventory nr": 268},
        {"name": "Type-inferrer", "inventory nr": 3621}
    ]
}]
```

## Evolving the Schema
As data evolves, `dlt` allows for modifications such as:
- Adding a new column (`CEO`).
- Changing a column type (`inventory nr` from integer to string).
- Removing a column (`room`) or renaming it (`building` to `main_block`).

## Notifying Schema Changes
To keep stakeholders informed about schema updates, use tools like Slack notifications for alerting. This ensures data engineers and analysts can seamlessly handle evolutions without technical impediments.

```py
from dlt.common.runtime.slack import send_slack_message

hook = "https://hooks.slack.com/services/xxx/xxx/xxx"

for package in load_info.load_packages:
    for table_name, table in package.schema_update.items():
        for column_name, column in table["columns"].items():
            send_slack_message(
                hook,
                message=(
                    f"\tTable updated: {table_name}: "
                    f"Column changed: {column_name}: "
                    f"{column['data_type']}"
                )
            )
```

## Controlling Schema Evolution
Control over schema evolution is achievable through schema and data contracts, enabling specification of how schemas should adapt over time. For complete control, refer to the detailed [documentation](./schema-contracts).

## Testing for Removed Columns
To ensure the removal of columns, apply "not null" constraints. Removal can be confirmed when a data validation error occurs due to the constraint's enforcement.

## Data Modifications and Schema Loading
As data changes with additional nested structures, the schema evolution engine adapts by generating appropriate sub-tables, maintaining consistency in data representation.

## Schema and Data Contracts
Utilize schema and data contracts to dictate schema evolution terms. These contracts guide `dlt` on handling entity changes, such as tables and columns, using modes like `evolve`, `freeze`, `discard_rows`, and `discard_columns`.
"""
    return TextResource(
        text=content,
        name="docs.schema.evolution",
        uri="docs://core/schema/evolution",
        mime_type="text/markdown",
    )


def rest_api() -> TextResource:
    content = """
# REST API source
## Overview
The REST API source extracts JSON data from RESTful APIs using declarative configurations. Configure endpoints, pagination, incremental loading, authentication, and data selection in a clear, structured way.

## Quick Start Example

```py
import dlt
from dlt.sources.rest_api import rest_api_source

source = rest_api_source({
    "client": {
        "base_url": "https://api.example.com/",
        "auth": {"token": dlt.secrets["api_token"]},
        "paginator": {"type": "json_link", "next_url_path": "paging.next"},
    },
    "resources": ["posts", {"name": "comments", "endpoint": {"path": "posts/{resources.posts.id}/comments"}}]
})

pipeline = dlt.pipeline(pipeline_name="example", destination="duckdb", dataset_name="api_data")
pipeline.run(source)
```

## Key Configuration Sections
### Client Configuration
Defines connection details to the REST API:
- base_url (str): API root URL.
- headers (dict, optional): Additional HTTP headers.
- auth (dict/object, optional): Authentication details.
- paginator (dict/object, optional): Pagination method.

### Resources
List of API endpoints to load data from. Each resource defines:
- name: Resource/table name.
- endpoint: Endpoint details (path, params, method).
- primary_key (optional): Primary key for merging data.
- write_disposition (optional): Merge/append behavior.
- processing_steps (optional): Data filtering and transformation steps.

### Pagination Methods
The REST API supports common pagination patterns:
- json_link: Next URL from JSON response (next_url_path).
- header_link: Next page URL from HTTP headers.
- offset: Numeric offsets (limit, offset_param).
- page_number: Incremental page numbers (base_page, page_param, total_path).
- cursor: Cursor-based pagination (cursor_path, cursor_param).
- Custom paginators: Extendable for specialized cases.

Custom paginator example:

```py
"paginator": {"type": "page_number", "base_page": 1, "page_param": "page", "total_path": "response.pages"}
```

### Incremental Loading
Load only new/updated data using timestamps or IDs example:

```py
"params": {
    "since": {"type": "incremental", "cursor_path": "updated_at", "initial_value": "2024-01-01T00:00:00Z"}
}
```

### Authentication
Supported methods:
- Bearer Token
- HTTP Basic
- API Key (header/query)
- OAuth2 Client Credentials
- Custom authentication classes

Bearer Token Example:

```py
"auth": {"type": "bearer", "token": dlt.secrets["api_token"]}
```

### Data Selection (JSONPath)
Explicitly specify data locations in JSON responses example:

```py
"endpoint": {"path": "posts", "data_selector": "response.items"}
```

### Resource Relationships
Fetch related resources using placeholders referencing parent fields.

Path Parameter Example:

```py
{"path": "posts/{resources.posts.id}/comments"}
```

Query Parameter Example:

```py
{"params": {"post_id": "{resources.posts.id}"}}
```

### Processing Steps (Filter/Transform)
Apply transformations before loading:

```py
"processing_steps": [
    {"filter": "lambda x: x['id'] < 10"},
    {"map": "lambda x: {**x, 'title': x['title'].lower()}"}
]
```

### Troubleshooting
- Validation Errors: Check resource structure (endpoint paths, params).
- Incorrect Data: Verify JSONPaths (data_selector).
- Pagination Issues: Explicitly set paginator type; check total_path correctness.
- Authentication Issues: Verify credentials; ensure correct auth method.
"""
    return TextResource(
        text=content,
        name="docs.source.rest_api",
        uri="docs://core/source/rest_api",
        mime_type="text/markdown",
    )


# NOTE currently, Continue displays resources by registration order
__resources__ = (
    glossary,
    resource,
    source,
    destination,
    pipeline,
    rest_api,
    state,
    full_loading,
    incremental_loading,
    schema,
    schema_contracts,
    schema_evolution,
    naming,
)
