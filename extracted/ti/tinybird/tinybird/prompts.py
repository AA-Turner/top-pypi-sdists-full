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


sql_instructions = f"""
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
    - When you use defined function with a parameter inside, do NOT add quotes around the parameter:
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
