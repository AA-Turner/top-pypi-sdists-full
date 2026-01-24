from datetime import date
from typing import Optional

general_functions = [
    "BLAKE3",
    "CAST",
    "CHARACTER_LENGTH",
    "CHAR_LENGTH",
    "CRC32",
    "CRC32IEEE",
    "CRC64",
    "DATABASE",
    "DATE",
    "DATE_DIFF",
    "DATE_FORMAT",
    "DATE_TRUNC",
    "DAY",
    "DAYOFMONTH",
    "DAYOFWEEK",
    "DAYOFYEAR",
    "FORMAT_BYTES",
    "FQDN",
    "FROM_BASE64",
    "FROM_DAYS",
    "FROM_UNIXTIME",
    "HOUR",
    "INET6_ATON",
    "INET6_NTOA",
    "INET_ATON",
    "INET_NTOA",
    "IPv4CIDRToRange",
    "IPv4NumToString",
    "IPv4NumToStringClassC",
    "IPv4StringToNum",
    "IPv4StringToNumOrDefault",
    "IPv4StringToNumOrNull",
    "IPv4ToIPv6",
    "IPv6CIDRToRange",
    "IPv6NumToString",
    "IPv6StringToNum",
    "IPv6StringToNumOrDefault",
    "IPv6StringToNumOrNull",
    "JSONArrayLength",
    "JSONExtract",
    "JSONExtractArrayRaw",
    "JSONExtractBool",
    "JSONExtractFloat",
    "JSONExtractInt",
    "JSONExtractKeys",
    "JSONExtractKeysAndValues",
    "JSONExtractKeysAndValuesRaw",
    "JSONExtractRaw",
    "JSONExtractString",
    "JSONExtractUInt",
    "JSONHas",
    "JSONKey",
    "JSONLength",
    "JSONRemoveDynamoDBAnnotations",
    "JSONType",
    "JSON_ARRAY_LENGTH",
    "JSON_EXISTS",
    "JSON_QUERY",
    "JSON_VALUE",
    "L1Distance",
    "L1Norm",
    "L1Normalize",
    "L2Distance",
    "L2Norm",
    "L2Normalize",
    "L2SquaredDistance",
    "L2SquaredNorm",
    "LAST_DAY",
    "LinfDistance",
    "LinfNorm",
    "LinfNormalize",
    "LpDistance",
    "LpNorm",
    "LpNormalize",
    "MACNumToString",
    "MACStringToNum",
    "MACStringToOUI",
    "MAP_FROM_ARRAYS",
    "MD4",
    "MD5",
    "MILLISECOND",
    "MINUTE",
    "MONTH",
    "OCTET_LENGTH",
    "QUARTER",
    "REGEXP_EXTRACT",
    "REGEXP_MATCHES",
    "REGEXP_REPLACE",
    "SCHEMA",
    "SECOND",
    "SHA1",
    "SHA224",
    "SHA256",
    "SHA384",
    "SHA512",
    "SHA512_256",
    "SUBSTRING_INDEX",
    "SVG",
    "TIMESTAMP_DIFF",
    "TO_BASE64",
    "TO_DAYS",
    "TO_UNIXTIME",
    "ULIDStringToDateTime",
    "URLHash",
    "URLHierarchy",
    "URLPathHierarchy",
    "UTCTimestamp",
    "UTC_timestamp",
    "UUIDNumToString",
    "UUIDStringToNum",
    "UUIDToNum",
    "UUIDv7ToDateTime",
    "YEAR",
    "YYYYMMDDToDate",
    "YYYYMMDDToDate32",
    "YYYYMMDDhhmmssToDateTime",
    "YYYYMMDDhhmmssToDateTime64",
]

general_functions_insensitive = [
    "cast",
    "character_length",
    "char_length",
    "crc32",
    "crc32ieee",
    "crc64",
    "database",
    "date",
    "date_format",
    "date_trunc",
    "day",
    "dayofmonth",
    "dayofweek",
    "dayofyear",
    "format_bytes",
    "fqdn",
    "from_base64",
    "from_days",
    "from_unixtime",
    "hour",
    "inet6_aton",
    "inet6_ntoa",
    "inet_aton",
    "inet_ntoa",
    "json_array_length",
    "last_day",
    "millisecond",
    "minute",
    "month",
    "octet_length",
    "quarter",
    "regexp_extract",
    "regexp_matches",
    "regexp_replace",
    "schema",
    "second",
    "substring_index",
    "to_base64",
    "to_days",
    "to_unixtime",
    "utctimestamp",
    "utc_timestamp",
    "year",
]

aggregate_functions = [
    "BIT_AND",
    "BIT_OR",
    "BIT_XOR",
    "COVAR_POP",
    "COVAR_SAMP",
    "STD",
    "STDDEV_POP",
    "STDDEV_SAMP",
    "VAR_POP",
    "VAR_SAMP",
    "aggThrow",
    "analysisOfVariance",
    "anova",
    "any",
    "anyHeavy",
    "anyLast",
    "anyLast_respect_nulls",
    "any_respect_nulls",
    "any_value",
    "any_value_respect_nulls",
    "approx_top_count",
    "approx_top_k",
    "approx_top_sum",
    "argMax",
    "argMin",
    "array_agg",
    "array_concat_agg",
    "avg",
    "avgWeighted",
    "boundingRatio",
    "categoricalInformationValue",
    "contingency",
    "corr",
    "corrMatrix",
    "corrStable",
    "count",
    "covarPop",
    "covarPopMatrix",
    "covarPopStable",
    "covarSamp",
    "covarSampMatrix",
    "covarSampStable",
    "cramersV",
    "cramersVBiasCorrected",
    "deltaSum",
    "deltaSumTimestamp",
    "dense_rank",
    "entropy",
    "exponentialMovingAverage",
    "exponentialTimeDecayedAvg",
    "exponentialTimeDecayedCount",
    "exponentialTimeDecayedMax",
    "exponentialTimeDecayedSum",
    "first_value",
    "first_value_respect_nulls",
    "flameGraph",
    "groupArray",
    "groupArrayInsertAt",
    "groupArrayIntersect",
    "groupArrayLast",
    "groupArrayMovingAvg",
    "groupArrayMovingSum",
    "groupArraySample",
    "groupArraySorted",
    "groupBitAnd",
    "groupBitOr",
    "groupBitXor",
    "groupBitmap",
    "groupBitmapAnd",
    "groupBitmapOr",
    "groupBitmapXor",
    "groupUniqArray",
    "histogram",
    "intervalLengthSum",
    "kolmogorovSmirnovTest",
    "kurtPop",
    "kurtSamp",
    "lagInFrame",
    "largestTriangleThreeBuckets",
    "last_value",
    "last_value_respect_nulls",
    "leadInFrame",
    "lttb",
    "mannWhitneyUTest",
    "max",
    "maxIntersections",
    "maxIntersectionsPosition",
    "maxMappedArrays",
    "meanZTest",
    "median",
    "medianBFloat16",
    "medianBFloat16Weighted",
    "medianDD",
    "medianDeterministic",
    "medianExact",
    "medianExactHigh",
    "medianExactLow",
    "medianExactWeighted",
    "medianGK",
    "medianInterpolatedWeighted",
    "medianTDigest",
    "medianTDigestWeighted",
    "medianTiming",
    "medianTimingWeighted",
    "min",
    "minMappedArrays",
    "nonNegativeDerivative",
    "nothing",
    "nothingNull",
    "nothingUInt64",
    "nth_value",
    "ntile",
    "quantile",
    "quantileBFloat16",
    "quantileBFloat16Weighted",
    "quantileDD",
    "quantileDeterministic",
    "quantileExact",
    "quantileExactExclusive",
    "quantileExactHigh",
    "quantileExactInclusive",
    "quantileExactLow",
    "quantileExactWeighted",
    "quantileGK",
    "quantileInterpolatedWeighted",
    "quantileTDigest",
    "quantileTDigestWeighted",
    "quantileTiming",
    "quantileTimingWeighted",
    "quantiles",
    "quantilesBFloat16",
    "quantilesBFloat16Weighted",
    "quantilesDD",
    "quantilesDeterministic",
    "quantilesExact",
    "quantilesExactExclusive",
    "quantilesExactHigh",
    "quantilesExactInclusive",
    "quantilesExactLow",
    "quantilesExactWeighted",
    "quantilesGK",
    "quantilesInterpolatedWeighted",
    "quantilesTDigest",
    "quantilesTDigestWeighted",
    "quantilesTiming",
    "quantilesTimingWeighted",
    "rank",
    "rankCorr",
    "retention",
    "row_number",
    "sequenceCount",
    "sequenceMatch",
    "sequenceNextNode",
    "simpleLinearRegression",
    "singleValueOrNull",
    "skewPop",
    "skewSamp",
    "sparkBar",
    "sparkbar",
    "stddevPop",
    "stddevPopStable",
    "stddevSamp",
    "stddevSampStable",
    "stochasticLinearRegression",
    "stochasticLogisticRegression",
    "studentTTest",
    "sum",
    "sumCount",
    "sumKahan",
    "sumMapFiltered",
    "sumMapFilteredWithOverflow",
    "sumMapWithOverflow",
    "sumMappedArrays",
    "sumWithOverflow",
    "theilsU",
    "topK",
    "topKWeighted",
    "uniq",
    "uniqCombined",
    "uniqCombined64",
    "uniqExact",
    "uniqHLL12",
    "uniqTheta",
    "uniqUpTo",
    "varPop",
    "varPopStable",
    "varSamp",
    "varSampStable",
    "welchTTest",
    "windowFunnel",
]


test_create_prompt = """
You are a Tinybird expert. You will be given a pipe containing different nodes with SQL and Tinybird templating syntax. You will generate URLs to test it with different parameters combinations.
<pipe>
    <name>{name}</name>
    <content>{content}</content>
    <parameters>{parameters}</parameters>
</pipe>

<instructions>
    - Every test name must be unique.
    - The test can have as many parameters as are needed to test the pipe.
    - The parameter within Tinybird templating syntax looks like this one {{String(my_param_name, default_value)}}.
    - If there are no parameters, you can omit parameters and generate a single test.
    - The format of the parameters is the following: ?param1=value1&param2=value2&param3=value3
    - If some parameters are provided by the user and you need to use them, preserve in the same format as they were provided, like case sensitive.
    - If user provides the current test content, use it to generate the new test content.
</instructions>

This is an example of a test with parameters:
<example>
    <test>
        <name>kpis_date_range</name>
        <description>Test specific date range with daily granularity</description>
        <parameters>?date_from=2024-01-01&date_to=2024-01-10</parameters>
    </test>
</example>

Follow the instructions and generate the following response with no additional text:

<response>
    <test>
        <name>[test name here]</name>
        <description>[test description here]</description>
        <parameters>[parameters here]</parameters>
    </test>
</response>
"""


def create_prompt(existing_resources: str, feedback: str = "", history: str = "") -> str:
    feedback_history = ""
    if feedback and history:
        feedback_history = f"""In case the <feedback> and <history> tags are present and not empty,
it means there was a previous attempt to generate the resources and the user provided feedback and history about previous responses.
Use the following feedback and history to regenerate the response:
Feedback to improve the response:
{feedback}
History of previous results:
{history}"""

    return """
You are a Tinybird expert. You will be given a prompt to generate new or update existing Tinybird resources: datasources and/or pipes.
<existing_resources>{existing_resources}</existing_resources>
{datasource_instructions}
{pipe_instructions}
{sql_instructions}
{datasource_example}
{pipe_example}
{copy_pipe_instructions}
{materialized_pipe_instructions}
{sink_pipe_instructions}
{connection_instructions}
{kafka_connection_example}
{gcs_connection_example}
{gcs_hmac_connection_example}
{s3_connection_example}

{feedback_history}

Use the following format to generate the response and do not wrap it in any other text, including the <response> tag.
<response>
    <resource>
        <type>[datasource or pipe or connection]</type>
        <name>[resource name here]</name>
        <content>[resource content here]</content>
    </resource>
</response>

""".format(
        existing_resources=existing_resources,
        datasource_instructions=datasource_instructions,
        pipe_instructions=pipe_instructions,
        sql_instructions=sql_instructions,
        datasource_example=datasource_example,
        pipe_example=pipe_example,
        copy_pipe_instructions=copy_pipe_instructions,
        materialized_pipe_instructions=materialized_pipe_instructions,
        sink_pipe_instructions=sink_pipe_instructions,
        connection_instructions=connection_instructions,
        kafka_connection_example=kafka_connection_example,
        gcs_connection_example=gcs_connection_example,
        gcs_hmac_connection_example=gcs_hmac_connection_example,
        s3_connection_example=s3_connection_example,
        feedback_history=feedback_history,
    )


def mock_prompt(rows: int, feedback: str = "") -> str:
    today = date.today().isoformat()

    if feedback:
        feedback = f"""In case the <feedback> tag is present and not empty,
it means there was a previous attempt to generate the resources and the system provided feedback about the previous response.
Use the following feedback to regenerate the response:
<feedback>{feedback}</feedback>
"""

    return f"""
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
FROM numbers({rows})
    </example_output>
</example>

<instructions>
- The query MUST return a random sample of data that matches the schema.
- The query MUST return a valid clickhouse sql query.
- The query MUST return a sample of EXACTLY {rows} rows.
- The query MUST be valid for clickhouse and Tinybird.
- FROM numbers({rows}) part is mandatory.
- If json paths are present (e.g. `userAgent` String `json:$.userAgent`), rely on the json paths to generate the sample record.
- If the schema has nested json paths (e.g. `json:$.location.country`), generate nested JSON objects accordingly.
- When working with dates, take into account that the current date is {today}.
- Use recent dates to avoid generating dates that are too far in the past.
- Do NOT include ```clickhouse or ```sql or any other wrapping text to the sql query.
- Do NOT use any of these functions: elementAt
- Do NOT add a semicolon at the end of the query
- Do NOT add any FORMAT at the end of the query, because it will be added later by Tinybird.
- General functions supported are: {general_functions}
- Character insensitive functions supported are: {general_functions_insensitive}
- Aggregate functions supported are: {aggregate_functions}
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
{{
  "order_id": 123456,
  "customer_id": 7890,
  "order_date": "2024-11-30T10:30:00.000Z",
  "total_amount": 150.0,
  "items": ["item1", "item2", "item3"]
}}

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
{{
  "timestamp": "2024-11-30T10:30:00.000Z",
  "location": {{
    "country": "United States",
    "region": "California", 
    "city": "San Francisco",
    "latitude": "37.7749",
    "longitude": "-122.4194"
  }}
}}

### Example SQL output for nested JSON paths:

SELECT
    timestamp,
    CAST(concat('{{
        "country": "', country, '",
        "region": "', region, '",
        "city": "', city, '",
        "latitude": "', latitude, '",
        "longitude": "', longitude, '"
    }}'), 'JSON') AS location
FROM
(
    SELECT
        now() - rand() % 86400 AS timestamp,
        ['United States', 'Canada', 'United Kingdom', 'Germany', 'France'][(rand() % 5) + 1] AS country,
        ['California', 'Texas', 'New York', 'Ontario', 'London'][(rand() % 5) + 1] AS region,
        ['San Francisco', 'Los Angeles', 'New York', 'Toronto', 'London'][(rand() % 5) + 1] AS city,
        toString(round(rand() * 180 - 90, 4)) AS latitude,
        toString(round(rand() * 360 - 180, 4)) AS longitude
    FROM numbers(ROWS)
)
</more_examples>

Follow the instructions and generate the following response with no additional text in the following format:
<response>
    <sql>[raw sql query here]</sql>
</response>

{feedback}

"""


copy_pipe_instructions = """
<copy_pipe_instructions>
- Do not create copy pipes by default, unless the user asks for it.
- Copy pipes should be created in the /copies folder.
- In a .pipe file you can define how to export the result of a Pipe to a Data Source, optionally with a schedule.
- Do not include COPY_SCHEDULE in the .pipe file unless is specifically requested by the user.
- COPY_SCHEDULE is a cron expression that defines the schedule of the copy pipe.
- COPY_SCHEDULE is optional and if not provided, the copy pipe will be executed only once.
- TARGET_DATASOURCE is the name of the Data Source to export the result to.
- TYPE COPY is the type of the pipe and it is mandatory for copy pipes.
- If the copy pipe uses parameters, you must include the % character and a newline on top of every query to be able to use the parameters.
- The content of the .pipe file must follow this format:
DESCRIPTION Copy Pipe to export sales hour every hour to the sales_hour_copy Data Source

NODE daily_sales
SQL >
    %
    SELECT toStartOfDay(starting_date) day, country, sum(sales) as total_sales
    FROM teams
    WHERE
    day BETWEEN toStartOfDay(now()) - interval 1 day AND toStartOfDay(now())
    and country = {{ String(country, 'US')}}
    GROUP BY day, country

TYPE COPY
TARGET_DATASOURCE sales_hour_copy
COPY_SCHEDULE 0 * * * *
</copy_pipe_instructions>
"""

sink_pipe_instructions = """
<sink_pipe_instructions>
- Do not create sink pipes by default, unless the user asks for it.
- Sink pipes should be created in the /sinks folder.
- In a .pipe file you can define how to export the result of a Pipe to an external system, optionally with a schedule.
- Valid external systems are Kafka, S3, GCS.
- Sink pipes depend on a connection, if no connection is provided, search for an existing connection that suits the request. If none, create a new connection.
- Do not include EXPORT_SCHEDULE in the .pipe file unless is specifically requested by the user.
- EXPORT_SCHEDULE is a cron expression that defines the schedule of the sink pipe.
- EXPORT_SCHEDULE is optional and if not provided, the sink pipe will be executed only once.
- EXPORT_CONNECTION_NAME is the name of the connection used to export.
- TYPE SINK is the type of the pipe and it is mandatory for sink pipes.
- If the sink pipe uses parameters, you must include the % character and a newline on top of every query to be able to use the parameters.
- The content of the .pipe file must follow this format:
DESCRIPTION Sink Pipe to export sales hour every hour using my_connection

NODE daily_sales
SQL >
    %
    SELECT toStartOfDay(starting_date) day, country, sum(sales) as total_sales
    FROM teams
    WHERE
    day BETWEEN toStartOfDay(now()) - interval 1 day AND toStartOfDay(now())
    and country = {{ String(country, 'US')}}
    GROUP BY day, country

TYPE sink
EXPORT_CONNECTION_NAME "my_connection"
EXPORT_BUCKET_URI "s3://tinybird-sinks"
EXPORT_FILE_TEMPLATE "daily_prices"
EXPORT_SCHEDULE "*/5 * * * *"
EXPORT_FORMAT "csv"
EXPORT_COMPRESSION "gz"
EXPORT_STRATEGY "truncate"
</sink_pipe_instructions>
"""

materialized_pipe_instructions = """
<materialized_pipe_instructions>
- Do not create materialized pipes by default, unless the user asks for it.
- Materialized pipes should be created in the /materializations folder.
- In a .pipe file you can define how to materialize each row ingested in the earliest Data Source in the Pipe query to a materialized Data Source. Materialization happens at ingest.
- DATASOURCE: Required when TYPE is MATERIALIZED. Sets the target Data Source for materialized nodes.
- TYPE MATERIALIZED is the type of the pipe and it is mandatory for materialized pipes.
- The content of the .pipe file must follow the materialized_pipe_content format.
- Use State modifier for the aggregated columns in the pipe.
</materialized_pipe_instructions>
<materialized_pipe_content>
NODE daily_sales
SQL >
    SELECT toStartOfDay(starting_date) day, country, sumState(sales) as total_sales
    FROM teams
    GROUP BY day, country

TYPE MATERIALIZED
DATASOURCE sales_by_hour
</materialized_pipe_content>
<target_datasource_instructions>
- The target datasource of a materialized pipe must have an AggregatingMergeTree engine.
- Use AggregateFunction for the aggregated columns in the pipe.
- Pipes using a materialized data source must use the Merge modifier in the SQL query for the aggregated columns. Example: sumMerge(total_sales)
- Put all dimensions in the ENGINE_SORTING_KEY, sorted from least to most cardinality.
</target_datasource_instructions>
<target_datasource_content>
SCHEMA >
    `total_sales` AggregateFunction(sum, Float64),
    `sales_count` AggregateFunction(count, UInt64),
    `column_name_2` AggregateFunction(avg, Float64),
    `dimension_1` String,
    `dimension_2` String,
    ...
    `date` DateTime

ENGINE "AggregatingMergeTree"
ENGINE_PARTITION_KEY "toYYYYMM(date)"
ENGINE_SORTING_KEY "date, dimension_1, dimension_2, ..."
</target_datasource_content>
"""

connection_instructions = """
<connection_file_instructions>
    - Content cannot be empty.
    - The connection names must be unique.
    - No indentation is allowed for property names
    - We support kafka, gcs and s3 connections for now
</connection_file_instructions>
"""

kafka_connection_example = """
<kafka_connection_content>
TYPE kafka
KAFKA_BOOTSTRAP_SERVERS {{ tb_secret("PRODUCTION_KAFKA_SERVERS", "localhost:9092") }}
KAFKA_SECURITY_PROTOCOL SASL_SSL
KAFKA_SASL_MECHANISM PLAIN
KAFKA_KEY {{ tb_secret("PRODUCTION_KAFKA_USERNAME", "") }}
KAFKA_SECRET {{ tb_secret("PRODUCTION_KAFKA_PASSWORD", "") }}
</kafka_connection_content>
"""

gcs_connection_example = """
<gcs_connection_content>
TYPE gcs
GCS_SERVICE_ACCOUNT_CREDENTIALS_JSON {{ tb_secret("PRODUCTION_GCS_SERVICE_ACCOUNT_CREDENTIALS_JSON", "") }}
</gcs_connection_content>
"""

gcs_hmac_connection_example = """
<gcs_hmac_connection_content>
TYPE gcs
GCS_HMAC_ACCESS_ID {{ tb_secret("gcs_hmac_access_id") }}
GCS_HMAC_SECRET {{ tb_secret("gcs_hmac_secret") }}
</gcs_hmac_connection_content>
"""

s3_connection_example = """
<s3_connection_content>
TYPE s3
S3_REGION {{ tb_secret("PRODUCTION_S3_REGION", "") }}
S3_ARN {{ tb_secret("PRODUCTION_S3_ARN", "") }}
</s3_connection_content>
"""

datasource_instructions = """
<datasource_file_instructions>
    - Content cannot be empty.
    - The datasource names must be unique.
    - No indentation is allowed for property names: DESCRIPTION, SCHEMA, ENGINE, ENGINE_PARTITION_KEY, ENGINE_SORTING_KEY, etc.
    - Use MergeTree engine by default.
    - Use AggregatingMergeTree engine when the datasource is the target of a materialized pipe.
    - Use always json paths to define the schema. Example: `user_id` String `json:$.user_id`,
    - Array columns are supported with a special syntax. Example: `items` Array(String) `json:$.items[:]`
    - If the datasource is using an S3 or GCS connection, they need to set IMPORT_CONNECTION_NAME, IMPORT_BUCKET_URI and IMPORT_SCHEDULE (GCS @on-demand only, S3 supports @auto too)
    - If the datasource is using a Kafka connection, they need to set KAFKA_CONNECTION_NAME as the name of the .connection file, KAFKA_TOPIC topic_name and KAFKA_GROUP_ID as the group id for the datasource
    - Unless the user asks for them, do not include ENGINE_PARTITION_KEY and ENGINE_PRIMARY_KEY.
    - DateTime64 type without precision is not supported. Use DateTime64(3) instead.
</datasource_file_instructions>
"""

datasource_example = """
<datasource_content>
DESCRIPTION >
    Some meaningful description of the datasource

SCHEMA >
    `column_name_1` clickhouse_tinybird_compatible_data_type `json:$.column_name_1`,
    `column_name_2` clickhouse_tinybird_compatible_data_type `json:$.column_name_2`,
    ...
    `column_name_n` clickhouse_tinybird_compatible_data_type `json:$.column_name_n`

ENGINE "MergeTree"
ENGINE_PARTITION_KEY "partition_key"
ENGINE_SORTING_KEY "sorting_key_1, sorting_key_2, ..."
</datasource_content>
"""

pipe_example = """
<pipe_content>
DESCRIPTION >
    Some meaningful description of the pipe

NODE node_1
SQL >
    [sql query using clickhouse syntax and tinybird templating syntax and starting always with SELECT or %\nSELECT]
TYPE endpoint

</pipe_content>
"""

pipe_instructions = """
Follow these instructions when creating or updating any type of .pipe file:
<pipe_file_instructions>
    - The pipe names must be unique.
    - Nodes do NOT use the same name as the Pipe they belong to. So if the pipe name is "my_pipe", the nodes must be named different like "my_pipe_node_1", "my_pipe_node_2", etc.
    - Node names MUST be different from the resource names in the project.
    - No indentation is allowed for property names: DESCRIPTION, NODE, SQL, TYPE, etc.
    - Allowed TYPE values are: endpoint, copy, materialized, sink.
    - Add always the output node in the TYPE section or in the last node of the pipe.
</pipe_file_instructions>
"""

sql_instructions = """
<sql_instructions>
    - The SQL query must be a valid ClickHouse SQL query that mixes ClickHouse syntax and Tinybird templating syntax (Tornado templating language under the hood).
    - SQL queries with parameters must start with "%" character and a newline on top of every query to be able to use the parameters. Examples:
    <invalid_query_with_parameters_no_%_on_top>
    SELECT * FROM events WHERE session_id={{{{String(my_param, "default_value")}}}}
    </invalid_query_with_parameters_no_%_on_top>
    <valid_query_with_parameters_with_%_on_top>
    %
    SELECT * FROM events WHERE session_id={{{{String(my_param, "default_value")}}}}
    </valid_query_with_parameters_with_%_on_top>
    - The Parameter functions like this one {{{{String(my_param_name,default_value)}}}} can be one of the following: String, DateTime, Date, Float32, Float64, Int, Integer, UInt8, UInt16, UInt32, UInt64, UInt128, UInt256, Int8, Int16, Int32, Int64, Int128, Int256
    - Parameter names must be different from column names. Pass always the param name and a default value to the function.
    - Use ALWAYS hardcoded values for default values for parameters.
    - Code inside the template {{{{template_expression}}}} follows the rules of Tornado templating language so no module is allowed to be imported. So for example you can't use now() as default value for a DateTime parameter. You need an if else block like this:
    <invalid_condition_with_now>
    AND timestamp BETWEEN {{DateTime(start_date, now() - interval 30 day)}} AND {{DateTime(end_date, now())}}
    </invalid_condition_with_now>
    <valid_condition_without_now>
    {{%if not defined(start_date)%}}
    timestamp BETWEEN now() - interval 30 day
    {{%else%}}
    timestamp BETWEEN {{{{DateTime(start_date)}}}}
    {{%end%}}
    {{%if not defined(end_date)%}}
    AND now()
    {{%else%}}
    AND {{{{DateTime(end_date)}}}}
    {{%end%}}
    </valid_condition_without_now>
    - Parameters must not be quoted.
    - When you use defined function with a paremeter inside, do NOT add quotes around the parameter:
    <invalid_defined_function_with_parameter>{{% if defined('my_param') %}}</invalid_defined_function_with_parameter>
    <valid_defined_function_without_parameter>{{% if defined(my_param) %}}</valid_defined_function_without_parameter>
    - Use datasource names as table names when doing SELECT statements.
    - Do not use pipe names as table names.
    - The available datasource names to use in the SQL are the ones present in the existing_resources section or the ones you will create.
    - Use node names as table names only when nodes are present in the same file.
    - Do not reference the current node name in the SQL.
    - SQL queries only accept SELECT statements with conditions, aggregations, joins, etc.
    - Do NOT use CREATE TABLE, INSERT INTO, CREATE DATABASE, etc.
    - Use ONLY SELECT statements in the SQL section.
    - INSERT INTO is not supported in SQL section.
    - ClickHouse functions supported are:
        - General functions supported are: {general_functions}
        - Character insensitive functions supported are: {general_functions_insensitive}
        - Aggregate functions supported are: {aggregate_functions}
    - How to use ClickHouse supported functions:
        - When using functions try always ClickHouse functions first, then SQL functions.
        - Do not use any ClickHouse function that is not present in the list of general functions, character insensitive functions and aggregate functions.
        - If the function is not present in the list, the sql query will fail, so avoid at all costs to use any function that is not present in the list.
        - When aliasing a column, use first the column name and then the alias.
        - General functions and aggregate functions are case sensitive.
        - Character insensitive functions are case insensitive.
    - Parameters are never quoted in any case.
    - Use the following syntax in the SQL section for the iceberg table function: iceberg('s3://bucket/path/to/table', {{{{tb_secret('aws_access_key_id')}}}}, {{{{tb_secret('aws_secret_access_key')}}}})
    - Use the following syntax in the SQL section for the postgres table function: postgresql('host:port', 'database', 'table', {{{{tb_secret('db_username')}}}}, {{{{tb_secret('db_password')}}}}), 'schema')
</sql_instructions>
""".format(
    general_functions=general_functions,
    general_functions_insensitive=general_functions_insensitive,
    aggregate_functions=aggregate_functions,
)


def rules_prompt(source: Optional[str] = None) -> str:
    base_command = source or "tb"
    return """
You are an expert in SQL and Tinybird. Follow these instructions when working with .datasource and .pipe files:

<command_calling>
You have commands at your disposal to develop a tinybird project:
- {base_command} build: to build the project locally and check it works.
- {base_command} deployment create --wait --auto: to create a deployment and promote it automatically
- {base_command} test run: to run existing tests
- {base_command} endpoint url <pipe_name>: to get the url of an endpoint, token included.
- {base_command} endpoint data <pipe_name>: to get the data of an endpoint. You can pass parameters to the endpoint like this: {base_command} endpoint data <pipe_name> --param1 value1 --param2 value2
- {base_command}  token ls: to list all the tokens
There are other commands that you can use, but these are the most common ones. Run `{base_command} -h` to see all the commands if needed.
When you need to work with resources or data in cloud, add always the --cloud flag before the command. Example: {base_command} --cloud datasource ls
</command_calling>
<development_instructions>
- When asking to create a tinybird data project, if the needed folders are not already created, use the following structure:
├── connections
├── copies
├── sinks
├── datasources
├── endpoints
├── fixtures
├── materializations
├── pipes
└── tests
- The local development server will be available at http://localhost:7181. Even if some response uses another base url, use always http://localhost:7181.
- After every change in your .datasource, .pipe or .ndjson files, run `{base_command} build` to build the project locally.
- When you need to ingest data locally in a datasource, create a .ndjson file with the same name of the datasource and the data you want and run `{base_command} build` so the data is ingested.
- The format of the generated api endpoint urls is: http://localhost:7181/v0/pipe/<pipe_name>.json?token=<token>
- Before running the tests, remember to have the project built with `{base_command} build` with the latest changes.
</development_instructions>
When asking for ingesting data, adding data or appending data do the following depending on the environment you want to work with:
<ingest_data_instructions>
- When building locally, create a .ndjson file with the data you want to ingest and do `{base_command} build` to ingest the data in the build env.
- We call `cloud` the production environment.
- When appending data in cloud, use `{base_command} --cloud datasource append <datasource_name> <file_name>`
- When you have a response that says “there are rows in quarantine”, do `{base_command} [--cloud] datasource data <datasource_name>_quarantine` to understand what is the problem.
</ingest_data_instructions>
<datasource_file_instructions>
Follow these instructions when creating or updating .datasource files:
{datasource_instructions}
</datasource_file_instructions>

<pipe_file_instructions>
Follow these instructions when creating or updating .pipe files:
{pipe_instructions}
{sql_instructions}
{datasource_example}
{pipe_example}
{copy_pipe_instructions}
{materialized_pipe_instructions}
{sink_pipe_instructions}
{connection_instructions}
{kafka_connection_example}
{gcs_connection_example}
{gcs_hmac_connection_example}
{s3_connection_example}
</pipe_file_instructions>
<test_file_instructions>
Follow these instructions when creating or updating .yaml files for tests:
{test_instructions}
</test_file_instructions>
<deployment_instruction>
Follow these instructions when evolving a datasource schema:
{deployment_instructions}
</deployment_instruction>
""".format(
        base_command=base_command,
        datasource_instructions=datasource_instructions,
        pipe_instructions=pipe_instructions,
        sql_instructions=sql_instructions,
        datasource_example=datasource_example,
        pipe_example=pipe_example,
        copy_pipe_instructions=copy_pipe_instructions,
        materialized_pipe_instructions=materialized_pipe_instructions,
        sink_pipe_instructions=sink_pipe_instructions,
        test_instructions=test_instructions,
        deployment_instructions=deployment_instructions,
        connection_instructions=connection_instructions,
        kafka_connection_example=kafka_connection_example,
        gcs_connection_example=gcs_connection_example,
        gcs_hmac_connection_example=gcs_hmac_connection_example,
        s3_connection_example=s3_connection_example,
    )


def claude_rules_prompt(source: Optional[str] = None) -> str:
    base_command = source or "tb"
    return """
# Tinybird CLI rules

## Commands
You have commands at your disposal to develop a tinybird project:
- {base_command} build: to build the project locally and check it works.
- {base_command} deployment create --wait --auto: to create a deployment and promote it automatically
- {base_command} test run: to run existing tests
- {base_command} endpoint url <pipe_name>: to get the url of an endpoint, token included.
- {base_command} endpoint data <pipe_name>: to get the data of an endpoint. You can pass parameters to the endpoint like this: {base_command} endpoint data <pipe_name> --param1 value1 --param2 value2
- {base_command}  token ls: to list all the tokens
There are other commands that you can use, but these are the most common ones. Run `{base_command} -h` to see all the commands if needed.
When you need to work with resources or data in cloud, add always the --cloud flag before the command. Example: {base_command} --cloud datasource ls

## Development instructions
- When asking to create a tinybird data project, if the needed folders are not already created, use the following structure:
├── connections
├── copies
├── sinks
├── datasources
├── endpoints
├── fixtures
├── materializations
├── pipes
└── tests
- The local development server will be available at http://localhost:7181. Even if some response uses another base url, use always http://localhost:7181.
- After every change in your .datasource, .pipe or .ndjson files, run `{base_command} build` to build the project locally.
- When you need to ingest data locally in a datasource, create a .ndjson file with the same name of the datasource and the data you want and run `{base_command} build` so the data is ingested.
- The format of the generated api endpoint urls is: http://localhost:7181/v0/pipe/<pipe_name>.json?token=<token>
- Before running the tests, remember to have the project built with `{base_command} build` with the latest changes.
</development_instructions>
When asking for ingesting data, adding data or appending data do the following depending on the environment you want to work with:

## Ingestion instructions
- When building locally, create a .ndjson file with the data you want to ingest and do `{base_command} build` to ingest the data in the build env.
- We call `cloud` the production environment.
- When appending data in cloud, use `{base_command} --cloud datasource append <datasource_name> <file_name>`
- When you have a response that says “there are rows in quarantine”, do `{base_command} [--cloud] datasource data <datasource_name>_quarantine` to understand what is the problem.

## .datasource file instructions
Follow these instructions when creating or updating .datasource files:
{datasource_instructions}

## .pipe file instructions
Follow these instructions when creating or updating .pipe files:
{pipe_instructions}
{sql_instructions}
{datasource_example}
{pipe_example}
{copy_pipe_instructions}
{materialized_pipe_instructions}
{sink_pipe_instructions}
{connection_instructions}
{kafka_connection_example}
{gcs_connection_example}
{gcs_hmac_connection_example}
{s3_connection_example}

## .test file instructions
Follow these instructions when creating or updating .yaml files for tests:
{test_instructions}

## Deployment instructions
Follow these instructions when evolving a datasource schema:
{deployment_instructions}
""".format(
        base_command=base_command,
        datasource_instructions=datasource_instructions,
        pipe_instructions=pipe_instructions,
        sql_instructions=sql_instructions,
        datasource_example=datasource_example,
        pipe_example=pipe_example,
        copy_pipe_instructions=copy_pipe_instructions,
        materialized_pipe_instructions=materialized_pipe_instructions,
        sink_pipe_instructions=sink_pipe_instructions,
        test_instructions=test_instructions,
        deployment_instructions=deployment_instructions,
        connection_instructions=connection_instructions,
        kafka_connection_example=kafka_connection_example,
        gcs_connection_example=gcs_connection_example,
        gcs_hmac_connection_example=gcs_hmac_connection_example,
        s3_connection_example=s3_connection_example,
    )


test_instructions = """
- The test file name must match the name of the pipe it is testing.
- Every scenario name must be unique inside the test file.
- When looking for the parameters available, you will find them in the pipes in the following format: {{{{String(my_param_name, default_value)}}}}.
- If there are no parameters, you can omit parameters and generate a single test.
- The format of the parameters is the following: param1=value1&param2=value2&param3=value3
- If some parameters are provided by the user and you need to use them, preserve in the same format as they were provided, like case sensitive
- Test as many scenarios as possible.
- The format of the test file is the following:
<test_file_format>
- name: kpis_single_day
  description: Test hourly granularity for a single day
  parameters: date_from=2024-01-01&date_to=2024-01-01
  expected_result: |
    {"date":"2024-01-01 00:00:00","visits":0,"pageviews":0,"bounce_rate":null,"avg_session_sec":0}
    {"date":"2024-01-01 01:00:00","visits":0,"pageviews":0,"bounce_rate":null,"avg_session_sec":0}

- name: kpis_date_range
  description: Test daily granularity for a date range
  parameters: date_from=2024-01-01&date_to=2024-01-31
  expected_result: |
    {"date":"2024-01-01","visits":0,"pageviews":0,"bounce_rate":null,"avg_session_sec":0}
    {"date":"2024-01-02","visits":0,"pageviews":0,"bounce_rate":null,"avg_session_sec":0}

- name: kpis_default_range
  description: Test default behavior without date parameters (last 7 days)
  parameters: ''
  expected_result: |
    {"date":"2025-01-10","visits":0,"pageviews":0,"bounce_rate":null,"avg_session_sec":0}
    {"date":"2025-01-11","visits":0,"pageviews":0,"bounce_rate":null,"avg_session_sec":0}

- name: kpis_fixed_time
  description: Test with fixed timestamp for consistent testing
  parameters: fixed_time=2024-01-15T12:00:00
  expected_result: ''

- name: kpis_single_day
  description: Test single day with hourly granularity
  parameters: date_from=2024-01-01&date_to=2024-01-01
  expected_result: |
    {"date":"2024-01-01 00:00:00","visits":0,"pageviews":0,"bounce_rate":null,"avg_session_sec":0}
    {"date":"2024-01-01 01:00:00","visits":0,"pageviews":0,"bounce_rate":null,"avg_session_sec":0}

</test_file_format>
"""

deployment_instructions = """
- When you make schema changes that are incompatible with the old schema, you must use a forward query in your data source. Forward queries are necessary when introducing breaking changes. Otherwise, your deployment will fail due to a schema mismatch.
- Forward queries translate the old schema to a new one that you define in the .datasource file. This helps you evolve your schema while continuing to ingest data.
Follow these steps to evolve your schema using a forward query:
- Edit the .datasource file to add a forward query.
- Run tb deploy --check to validate the deployment before creating it.
- Deploy and promote your changes in Tinybird Cloud using {base_command} --cloud deploy.
    <forward_query_example>
SCHEMA >
    `timestamp` DateTime `json:$.timestamp`,
    `session_id` UUID `json:$.session_id`,
    `action` String `json:$.action`,
    `version` String `json:$.version`,
    `payload` String `json:$.payload`

FORWARD_QUERY >
    select timestamp, toUUID(session_id) as session_id, action, version, payload
    </forward_query_example>
</deployment_instruction>
"""


def readme_prompt(readme: str, host: str, token: str, resources_xml: str) -> str:
    return f"""
You are an expert in SQL and Tinybird. Follow these instructions to generate a new README.md file for a tinybird project:
Current README.md file:
<current_resources_xml>
{resources_xml}
</current_resources_xml>
<readme>{readme}</readme>
<readme_instructions>
- If it is not present in the current readme, generate a new ## Tinybird section with the following content:
    - ### Overview section:
        - Explaining the purpose of the project.
    - ### Data sources section:
        - Explaining the purpose of each datasource.
        - Add a snippet of how to ingest data into each datasource like the following (where the payload example matches the datasource schema respecting non-nullable types):
        curl -X POST "{host}/v0/events?name=events" \
    -H "Authorization: Bearer {token}" \
    -d '{{"date":"2025-01-31","id":"123","user_id":"abc"}}'
    - ### Endpoints section:
        - Explaining the purpose of each endpoint.
        - Add a snippet of how to use each endpoint like the following:
        curl -X GET "{host}/v0/pipes/pipe_name.json?token={token}"
        - DateTime parameters must be formatted as YYYY-MM-DD HH:MM:SS, or else will fail.
- Do not include any other extra info related to Tinybird just maintain the existing one in the <readme> tag.
- Make sure the API host is correct, {host}.
- It is mandatory to return a <resource> tag with type "readme" in the response.
- The response must follow the following format:
<readme>[readme content here]</readme>
</readme_instructions>
"""


def quarantine_prompt(datasource_definition: str) -> str:
    return f"""
- You are an expert in Tinybird.
- You are given a list of rows that went to quarantine during ingestion because of data quality issues.
- Return the errors in a human readable format so the user can understand what is the problem and fix it.
- Be concise and to the point.
- Do not mention clickhouse tables. Refer to data sources instead.
- The possible fixes recommended fixes are:
    - Changing a column type in the datasource definition: tell the user what to change in the datasource file, then build again before appending the data.
    - Changing the data because of the wrong data type: tell the user what to change in the data file, then append the data again.
- The format of the response always inside the tag <quarantine_errors>[response]</quarantine_errors>
- Do not use markdown format in the response, because it is a CLI output.
- The datasource definition is the following:
<datasource_definition>
{datasource_definition}
</datasource_definition>
"""
