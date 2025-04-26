import json

# Referenced Data for function mock_connection(dummy_sch)
mock_connection_library_definition = {
    'verifierDefinitions': [
        {
            'verifierClass': 'com.streamsets.pipeline.lib.jdbc.connection.JdbcConnectionVerifier',
            'verifierConnectionFieldName': 'connection',
            'verifierConnectionSelectionFieldName': 'connectionSelection',
            'verifierType': 'STREAMSETS_JDBC',
            'library': 'streamsets-datacollector-sdc-snowflake-lib',
        },
        {
            'verifierClass': 'com.streamsets.pipeline.lib.jdbc.connection.JdbcConnectionVerifier',
            'verifierConnectionFieldName': 'connection',
            'verifierConnectionSelectionFieldName': 'connectionSelection',
            'verifierType': 'STREAMSETS_JDBC',
            'library': 'streamsets-datacollector-jdbc-lib',
        },
    ]
}

CONNECTION_INTERNAL_JSON = {
    'id': 'random-connection-id',
    'sdcId': 'random-sdc-id',
    'libraryDefinition': json.dumps(mock_connection_library_definition),
}
