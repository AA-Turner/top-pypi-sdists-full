try:
    from importlib.metadata import PackageNotFoundError, version as get_version
except Exception:  # Python < 3.8 fallback
    from importlib_metadata import PackageNotFoundError, version as get_version
from packaging.version import parse as parse_version


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
                "connection-type": "mcd-gateway",  # RFC3986 compliant
            },
            # Note: mcd_gateway (legacy with underscore) is supported via code for backward compatibility
            # but not registered here to avoid duplicate entries in the UI dropdown
        ],
        "hook-class-names": [
            "airflow_mcd.hooks.SessionHook",
            "airflow_mcd.hooks.GatewaySessionHook",
        ],
        "package-name": "airflow-mcd",
    }


def _check_airflow_version():
    try:
        airflow_version_str = get_version("apache-airflow")
    except PackageNotFoundError:
        raise ImportError(
            "apache-airflow is not installed. Please install a compatible version of Airflow "
            "before using airflow_mcd."
        )
    else:
        # If you still need a minimum version, e.g. >=1.10.14:
        if parse_version(airflow_version_str) < parse_version("1.10.14"):
            raise RuntimeError(
                f"Installed apache-airflow=={airflow_version_str} is too old. "
                "Please upgrade to apache-airflow>=1.10.14."
            )


def airflow_major_version():
    try:
        import airflow
        return int(airflow.__version__.split('.')[0])
    except Exception:
        return 2  # fallback, assume 2 if unknown
