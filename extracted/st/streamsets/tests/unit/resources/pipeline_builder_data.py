# List of tuples (<config_definition>, <expected default value>)
CONFIG_TYPE_TEST_CASES_JSON = [
    (
        {
            "fieldName": "Dummy",
            "name": "config.dummy",
            "type": "MODEL",
            "defaultValue": None,
            "model": {
                "labels": ["None"],
                "values": ["MANUAL"],
                "modelType": "FIELD_SELECTOR_MULTI_VALUE",
            },
        },
        [],
    ),
    (
        {
            "fieldName": "Dummy",
            "name": "config.dummy",
            "type": "MODEL",
            "defaultValue": None,
            "model": {
                "configDefinitions": [
                    {'name': 'config1', 'type': 'STRING', 'defaultValue': "default1"},
                    # Since there is no default value for config2, we don't expect this key to appear in the default.
                    {'name': 'config2', 'type': 'STRING', 'defaultValue': None},
                ],
                "modelType": "LIST_BEAN",
            },
        },
        [{'config1': 'default1'}],
    ),
    (
        {
            "fieldName": "Dummy",
            "name": "config.dummy",
            "type": "BOOLEAN",
            "defaultValue": None,
        },
        False,
    ),
    (
        {
            "fieldName": "Dummy",
            "name": "config.dummy",
            "type": "LIST",
            "defaultValue": None,
        },
        [],
    ),
    (
        {
            "fieldName": "Dummy",
            "name": "config.dummy",
            "type": "MAP",
            "defaultValue": None,
        },
        [],
    ),
]
