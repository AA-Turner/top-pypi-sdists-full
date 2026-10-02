def get_provider_info():
    return {
        "package-name": "apache-airflow-providers-anomalo",
        "name": "Anomalo Provider",
        "description": "An Apache Airflow provider for Anomalo.",
        "versions": ["0.1.7"],
        "connection-types": [
            {
                "hook-class-name": "airflow.providers.anomalo.hooks.anomalo.AnomaloHook",
                "connection-type": "anomalo",
            }
        ],
    }
