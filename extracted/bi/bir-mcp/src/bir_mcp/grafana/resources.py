import bidict


def get_mcp_resource_uri_functions() -> bidict.bidict[str, callable]:
    functions = bidict.bidict(
        {
            "instruction://flux": get_flux_instruction,
        }
    )
    return functions


def get_flux_instruction() -> str:
    """Provides information about InfluxDB Flux language, such as its data model, syntax, and usage examples."""
    instruction = """
    # Flux 
    Flux is a functional data scripting language designed for querying, analyzing, and acting on time-series data in InfluxDB.

    ## Data model
    Flux organizes data into independent buckets, similar to logical databases in SQL.
    Each bucket contains time series data. A single point is composed of:
    - measurement: The name of the thing you are measuring (e.g., "cpu", "http_requests"), similar to an SQL table or Prometheus metric name.
    - tags: Key-value pairs of metadata that describe the data (e.g., `host="server1"`, `region="us-west"`), similar to Prometheus labels.
    - fields: The actual data values (e.g., `usage_percent=99.5`, `request_count=124`), similar to Prometheus metric value.
    - timestamp: The time of the data point.

    ## Syntax
    Flux queries consist of sequentially executed pipeline of functions, joined by the pipe-forward operator "|>".
    It takes the output of one function and sends it as the input to the next function.

    ### Main Flux functions
    - from() - Specifies the InfluxDB bucket to retrieve data from. It's the starting point for query that fetches time-series data.
    - range() - Filters data based on a time range. Mandatory for time-series queries.
    - filter() - Filters rows based on column values (measurement, field, tags).
    - pivot() - Rotates data from a tall format (one row per timestamp/metric) to a wide format.
    - keep() / drop() - Filters data by column names, allowing you to keep or discard specific columns.
    - limit() - Restricts the number of rows returned.
    - group() - Groups rows together based on common column values for aggregation.
    - aggregateWindow() - Segments data into time windows and applies an aggregate function (mean, sum, etc.).
    - map() - Applies a custom function to each row to modify or add columns.
    - mean(), sum(), count(), last() - Common aggregate functions, often used inside aggregateWindow.
    - highestAverage(), highestMax(), lowestAverage(), top() - Efficient "top-n" results from a group, are significantly more performant for datasets with high tag cardinality
    - yield() - Specifies a result set to be delivered from the query.

    ### Meta functions
    - buckets() - Returns a list of all available buckets.
    - schema.measurements() - Returns a list of all measurements within a bucket.
    - schema.tagKeys() / schema.tagValues() - Returns a list of tag keys or tag values for a given measurement.

    ## Usage
    When using Flux through the Grafana's `/api/ds/query` endpoint, several variables are injected into the query,
    the most important are the `v.timeRangeStart` and `v.timeRangeStop`, which correspond to the `start_time` and `end_time` parameters
    passed to the `/api/ds/query` endpoint. So each query that fetches data from time series should look like this:

    ```flux
    // Specify the bucket name here
    from(bucket: "{bucket}")
        |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
        // Filters, transformations, aggegations, etc.
        |> yield(name: "value")
    ```

    ### Examples

    #### Get all buckets
    ```flux
    buckets()
    ```

    #### Get all measurements in a given bucket
    ```flux
    // Import the schema package to access its functions
    import "influxdata/influxdb/schema"
    // Call the measurements function, specifying which bucket to look in
    schema.measurements(bucket: "{bucket}")
    ```

    #### Get all field keys for a given measurement
    ```flux
    import "influxdata/influxdb/schema"
    schema.measurementFieldKeys(
        bucket: "{bucket}",
        measurement: "{measurement}"
    )
    ```

    #### Get all tag keys for a given measurement
    ```flux
    import "influxdata/influxdb/schema"
    schema.measurementTagKeys(
        bucket: "{bucket}",
        measurement: "{measurement}"
    )
    ```

    #### Get all tag values for a given tag key
    ```flux
    import "influxdata/influxdb/schema"
    schema.measurementTagValues(
        bucket: "{bucket}",
        measurement: "{measurement}",
        tag: "{tag}"
    )
    ```

    #### Filtering and aggregation
    ```flux
    from(bucket: "{bucket}")
        |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
        |> filter(fn: (r) => r._measurement == "{measurement}" and r._field == "{field}")
        // Pivot makes each unique field a new column, with timestamps as rows.
        // This is useful for creating tables or graphs with multiple series.
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        // Group data into 10-minute windows and calculate the mean for each window
        |> aggregateWindow(every: 10m, fn: mean)
        |> yield(name: "mean_{field}_10m")
    ```

    #### Finding lowest average values among groups
    ```flux
    from(bucket: "{bucket}")
        |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
        |> filter(fn: (r) => r._measurement == "{measurement}" and r._field == "{field}")
        |> lowestAverage(n: {n}, groupColumns: ["{tag}"])
    ```
    """
    return instruction
