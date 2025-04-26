import pkg_resources


def get_provider_info():
    return {
        "name": "Monte Carlo",
        "description": "`Monte Carlo <https://www.montecarlodata.com/>`__\n",
        "connection-types": [
            {
                "hook-class-name": "airflow_mcd.hooks.SessionHook",
                "connection-type": "mcd",
            },
            {
                "hook-class-name": "airflow_mcd.hooks.GatewaySessionHook",
                "connection-type": "mcd_gateway",
            },
        ],
        "hook-class-names": [
            "airflow_mcd.hooks.SessionHook",
            "airflow_mcd.hooks.GatewaySessionHook",
        ],
        "package-name": "airflow-mcd",
    }


def _check_airflow_version():
    try:
        airflow_dist = pkg_resources.get_distribution("apache-airflow")
    except pkg_resources.DistributionNotFound:
        raise ImportError(
            "apache-airflow is not installed. Please install a compatible version of Airflow "
            "before using airflow_mcd."
        )
    else:
        # If you still need a minimum version, e.g. >=1.10.14:
        if pkg_resources.parse_version(airflow_dist.version) < pkg_resources.parse_version("1.10.14"):
            raise RuntimeError(
                f"Installed apache-airflow=={airflow_dist.version} is too old. "
                "Please upgrade to apache-airflow>=1.10.14."
            )


_check_airflow_version()
