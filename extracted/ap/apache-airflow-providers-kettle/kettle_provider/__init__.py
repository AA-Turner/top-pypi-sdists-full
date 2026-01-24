__version__ = ['1.0.7', '1.0.6', '1.0.5', '1.0.4', '1.0.3', '1.0.2', '1.0.1', '1.0.0']

from typing import Any, Dict


def get_provider_info() -> Dict[str, Any]:
    return {
        "package-name": 'apache-airflow-providers-kettle',
        "name": "Kettle Apache Airflow Provider",
        "description": "A simple Apache Airflow Kettle Operator that can invoke jobs and transformations for Linux based systems.",
        "versions": __version__,
    }
