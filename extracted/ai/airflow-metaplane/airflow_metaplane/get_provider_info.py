def get_provider_info():
    return {
        "name": "Metaplane",
        "description": "`Metaplane <https://www.metaplane.dev/>`__\n",
        "integrations": [
            {
                "integration-name": "Metaplane",
                "external-doc-url": "https://www.metaplane.dev/",
                "tags": ["service"],
            }
        ],
        "connection-types": [
            {
                "hook-class-name": "airflow_metaplane.hooks.metaplane_hook.MetaplaneHook",
                "connection-type": "metaplane",
            }
        ],
        "hooks": [
            {
                "integration-name": "Metaplane",
                "python-modules": ["airflow_metaplane.hooks.metaplane_hook"],
            }
        ],
        "package-name": "airflow-metaplane",
    }
