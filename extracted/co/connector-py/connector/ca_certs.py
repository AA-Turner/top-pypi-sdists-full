import logging
import platform

logger = logging.getLogger(__name__)


def set_python_to_use_system_ca_certificates() -> None:
    """
    Set python to use the system CA certificates on Windows.
    """
    # Ignore the missing import error because this library only used on Windows.
    import pip_system_certs.wrapt_requests  # type: ignore

    pip_system_certs.wrapt_requests.inject_truststore()

    logger.info("Connector is now using the system CA certificates")


def is_windows() -> bool:
    """
    Check if the current platform is Windows.
    """
    return platform.system() == "Windows"
