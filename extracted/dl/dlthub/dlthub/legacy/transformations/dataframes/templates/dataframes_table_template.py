

# staging view for table {{ table_name }}
@transformation(table_name="{{ stg_table_name }}", materialization="view")
def {{ stg_table_name_func }}(
    connection: duckdb.DuckDBPyConnection,
    utils: TransformationUtils
) -> str:

    input_table = utils.make_qualified_input_table_name("{{ table_name }}")
    active_load_id_table = utils.make_qualified_output_table_name(ACTIVE_LOADS_ID_TABLE)

    return f"SELECT * FROM {input_table} WHERE _dlt_load_id IN (SELECT load_id FROM {active_load_id_table})"


# final table for table {{ table_name }}
@transformation(table_name="{{ table_name }}", materialization="table")
def {{ table_name_func }}(
    connection: duckdb.DuckDBPyConnection,
    utils: TransformationUtils
) -> Generator[Any, None, None]:

    stg_table_name = utils.make_qualified_output_table_name("{{ stg_table_name }}")

    # move data from staging table to output table
    for batch in connection.execute(f"SELECT * FROM {stg_table_name}").fetch_record_batch(DEFAULT_CHUNKSIZE):
        # TODO: do your transformations here
        # ...
        yield batch

