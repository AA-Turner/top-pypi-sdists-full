# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import argparse
import sys

import contrast_fireball

import contrast
from contrast.configuration.agent_config import AgentConfig
from contrast.configuration.config_option import DEFAULT_VALUE_SRC
from contrast.reporting.fireball import agent_config_to_plain_dict
from contrast.utils.loggers import logger
from contrast_rewriter import log_stderr


def validate_config():
    parser = argparse.ArgumentParser(
        description="Checks the Contrast agent configuration is valid"
    )
    parser.parse_args()
    try:
        exit_status = _validate()
        sys.exit(exit_status)
    except Exception as e:
        _log("Unexpected error while validating agent config:")
        _log(f"{e!r}")
        _log("Unable to validate agent config")
        sys.exit(1)


def _log(msg):
    log_stderr(msg, logger_name="contrast-validate-config")


def _validate():
    """
    Validates the config and returns an appropriate exit status
    """
    _log("Validating Contrast configuration")
    _log("You may see agent logs in structured log format")

    logger.setup_basic_agent_logger()

    if not _check_config():
        return 1

    if not _check_connection():
        return 1

    _log("Connection to Contrast successful")
    return 0


def _valid_proxy(config):
    """
    If proxy use is enabled, verify the proxy url is provided.
    """
    enabled = config.get("api.proxy.enable")
    if not enabled:
        # If proxy isn't enabled then it's "valid"
        _log("Proxy use disabled")
        return True

    url = config.get("api.proxy.url")
    if url:
        # Just check that's a populated string, not that it's a url
        _log("Proxy use enabled")
        return True

    _log("Proxy enabled but no proxy url provided")
    return False


def _valid_cert(config):
    """
    If certificate use is enabled, verify that the three required files are present.
    """
    enabled_config_option = config.get_option("api.certificate.enable")
    enabled = enabled_config_option.value()

    cert_file = config.get("api.certificate.cert_file")
    key_file = config.get("api.certificate.key_file")
    ca_file = config.get("api.certificate.ca_file")

    any_certificate_files_provided = any((ca_file, cert_file, key_file))

    if (
        enabled is True
        and enabled_config_option.source() != DEFAULT_VALUE_SRC
        and not any_certificate_files_provided
    ):
        _log(
            "Certificate configuration is explicitly enabled, but no certificate files are set"
        )
        return False

    if enabled is False or (enabled is True and not any_certificate_files_provided):
        # If certificate use isn't enabled then it's "valid"
        _log("Custom certificate use disabled - using default TLS certificates")
        return True

    if (cert_file and not key_file) or (key_file and not cert_file):
        _log("Certificate PEM file or private key PEM file is missing")
        return False

    _log("Using provided TLS certificates")
    return True


def _check_config():
    _log("Loading config")

    config = AgentConfig()

    _log("Config loaded successfully")

    _log("Checking API configuration")

    missing_values = config.check_for_api_config()
    if missing_values:
        for missing_value in missing_values:
            _log(f"Missing required config value: {missing_value}")
        return False

    return _valid_proxy(config) and _valid_cert(config)


def _check_connection() -> bool:
    from contrast.agent import agent_state

    agent_state.initialize_settings()
    assert (settings := agent_state.get_settings()) is not None
    assert (config := settings.config) is not None

    success = _check_fireball_connection(config)

    _log(f"Fireball reporting client: {'OK' if success else 'ERROR'}")

    return success


def _check_fireball_connection(config) -> bool:
    _log("Checking connection using fireball reporting client")

    try:
        contrast_fireball.connection_test(
            contrast_fireball.ConnectionTestOptions(
                agent_language=contrast_fireball.AgentLanguage.PYTHON,
                agent_version=contrast.__version__,
                config_sources=contrast_fireball.CustomConfigOptions(
                    [
                        contrast_fireball.ConfigValues(
                            values=agent_config_to_plain_dict(config),
                            origin=contrast_fireball.AgentOverride(),
                        )
                    ]
                ),
            )
        )
    except contrast_fireball.Error as e:
        _log(f"Failed to connect to the Contrast UI with fireball: {e}")
        return False

    return True
