"""`fivetran configuration`: collects a connector's configuration from its setup form, or runs the form's setup tests.

The form is asked for field by field (password and hidden fields without echoing what is typed), the answers are saved to
configuration.json with the password fields encrypted, and the form's setup tests run against what was saved.
"""
import getpass
import json
import os
from typing import Callable, Dict, List

from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_cli import form_field
from fivetran_connector_sdk_cli.configuration_decryption import (
    decrypt_configuration_values, encrypt_value, get_or_create_key)
from fivetran_connector_sdk_common.constants import (
    DROPDOWN_LABEL, ENCRYPTED_VALUE_PREFIX, REQUIRED_INPUT_MESSAGE, TOGGLE_LABEL)
from fivetran_connector_sdk_cli.form_field import HIDDEN, FormField

TEXT_KIND_NAMES = {form_field.PLAIN_TEXT: "PlainText", form_field.PASSWORD: "Password", HIDDEN: "Hidden"}


class ConfigurationError(Exception):
    """The form cannot be used: a duplicate field name, a dropdown with no options, a field of an unsupported kind."""


def validate_form(fields: List[FormField]):
    """Field names must be unique, and a dropdown must have at least one option and no repeated value."""
    seen = set()
    for field in fields:
        if field.name.strip() and field.name in seen:
            raise ConfigurationError(f"Duplicate configuration field name '{field.name}'.")
        seen.add(field.name)
    print_library_log("Validating configuration form dropdown fields")
    for field in fields:
        if field.dropdown_options is not None:
            values = [option.value for option in field.dropdown_options]
            if not values:
                raise ConfigurationError(f"Dropdown field '{field.name}' must define at least one option.")
            repeated = next((v for i, v in enumerate(values) if v in values[:i]), None)
            if repeated is not None:
                raise ConfigurationError(f"Duplicate dropdown value '{repeated}' in field '{field.name}'.")
    print_library_log("Configuration form dropdown field validation completed")


def _required(field: FormField) -> bool:
    return bool(field.required)


def _blank(value: str) -> bool:
    return not value.strip()


def _ask(label: str, input_fn: Callable[[str], str]) -> str:
    return input_fn(f"{label}: ")


def _prompt_required(field: FormField, ask_fn) -> str:
    while True:
        value = _ask(field.label, ask_fn)
        if not (_required(field) and _blank(value)):
            return value
        print(REQUIRED_INPUT_MESSAGE)


def _prompt_allowed(field: FormField, allowed: List[str], input_fn) -> str:
    while True:
        value = _ask(field.label, input_fn)
        if _required(field) and _blank(value):
            print(REQUIRED_INPUT_MESSAGE)
            continue
        if _blank(value):
            return ""
        if value in allowed:
            return value
        print(f"Invalid value: {value}")


def _prompt_toggle(field: FormField, input_fn) -> str:
    while True:
        value = _ask(field.label, input_fn).lower()
        if _required(field) and _blank(value):
            print(REQUIRED_INPUT_MESSAGE)
            continue
        if _blank(value):
            return ""
        if value in ("true", "false"):
            return value
        print(f"Invalid value: {value}")


def _describe_option(option) -> str:
    label, value, description = option.label, option.value, option.description
    if not label.strip():
        return value if not description.strip() else f"{value} - {description}"
    return f"{label}: {value}" if not description.strip() else f"{label}: {value} - {description}"


def prompt_for_configuration(fields: List[FormField], input_fn: Callable[[str], str] = input,
                             secret_fn: Callable[[str], str] = getpass.getpass) -> Dict[str, str]:
    print("\nEnter configuration values")
    config: Dict[str, str] = {}
    for field in fields:
        print()
        required = "REQUIRED" if _required(field) else ""
        description = field.description if field.description is not None else ""
        if field.dropdown_options is not None:
            print(f"<{field.name} [{DROPDOWN_LABEL}] [{description}] {required}>")
            for option in field.dropdown_options:
                print(_describe_option(option))
            config[field.name] = _prompt_allowed(field, [o.value for o in field.dropdown_options], input_fn)
        elif field.toggle:
            print(f"<{field.name} [{TOGGLE_LABEL}] [true, false] [{description}] {required}>")
            config[field.name] = _prompt_toggle(field, input_fn)
        elif field.text_field is not None:
            kind = TEXT_KIND_NAMES.get(field.text_field, str(field.text_field))
            if field.text_field == HIDDEN:
                print(f"{field.name} [Hidden Field]")
            else:
                placeholder = field.placeholder if field.placeholder is not None else ""
                print(f"<{field.name} [{kind}] [Placeholder: {placeholder}] [{description}] {required}>")
            secret = field.text_field in (form_field.PASSWORD, HIDDEN)
            config[field.name] = _prompt_required(field, secret_fn if secret else input_fn)
        else:
            raise ConfigurationError(f"Unsupported form parentFormField type: {field.name}")
    return config


def _password_fields(fields: List[FormField]) -> List[FormField]:
    return [f for f in fields if f.text_field == form_field.PASSWORD]


def _encrypt_passwords(config: Dict[str, str], fields: List[FormField], disable: bool) -> Dict[str, str]:
    if disable or not _password_fields(fields):
        return config
    key = get_or_create_key()
    encrypted = dict(config)
    for field in _password_fields(fields):
        value = config.get(field.name)
        if value is not None and value.strip() and not value.startswith(ENCRYPTED_VALUE_PREFIX):
            encrypted[field.name] = encrypt_value(value, field.name, key)
    return encrypted


def run_configuration_form(form, config_path: str, disable_encryption: bool, input_fn=input,
                           secret_fn=getpass.getpass) -> int:
    """Asks for each field of `form`, then writes the answers (passwords encrypted) to `config_path`."""
    validate_form(form.fields)
    if not form.fields:
        print_library_log("Your connector's configuration_form() method defines no fields. Please add at least one field and"
                          " re-run.", Logging.Level.SEVERE)
        return 1
    config = prompt_for_configuration(form.fields, input_fn, secret_fn)
    if disable_encryption:
        print_library_log("Encryption is disabled. Sensitive field values will be stored as plain text in"
                          " configuration.json. This is not recommended when working with AI or in shared environments.",
                          Logging.Level.WARNING, log_icon=Logging.LogIcon.INFO)
    config = _encrypt_passwords(config, form.fields, disable_encryption)
    fd = os.open(config_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)  # it may hold secrets, so only the owner reads it
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(json.dumps(config, ensure_ascii=False, separators=(",", ":")))
    os.chmod(config_path, 0o600)
    print_library_log(f"Configuration saved to: {config_path}", log_icon=Logging.LogIcon.INFO)
    masked = {k: ("****" if k in {f.name for f in _password_fields(form.fields)} else v) for k, v in config.items()}
    keys = ", ".join(masked)
    print_library_log(f"Configuration saved (values redacted). Keys: [{keys}]", log_icon=Logging.LogIcon.INFO)
    return 0


def _read_configuration(config_path: str):
    """The parsed `configuration.json`; raises `ConfigurationError`, with no traceback to show, if it cannot be read as JSON."""
    try:
        with open(config_path, encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError) as e:
        raise ConfigurationError(f"Cannot read configuration.json at {config_path}: {getattr(e, 'strerror', None) or e}") from e
    if not text.strip():
        raise ConfigurationError("configuration.json is empty.")
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ConfigurationError(f"configuration.json is not valid JSON: {e.msg}: line {e.lineno}, column {e.colno}.") from e


def run_configuration_tests(connector, form, config_path: str) -> int:
    """Runs each setup test of `form` against the configuration in `config_path`, stopping at the first failure."""
    validate_form(form.fields)
    if not form.tests:
        print_library_log("Your connector's configuration_form() method defines no tests to run.")
        return 0
    if not os.path.exists(config_path):
        print_library_log("No configuration.json found. Run 'fivetran configuration' first to generate one.",
                          Logging.Level.SEVERE, log_icon=Logging.LogIcon.FAILURE)
        return 1
    print_library_log(f"Reading configuration from: {config_path}", log_icon=Logging.LogIcon.INFO)
    configuration = _read_configuration(config_path)
    if not isinstance(configuration, dict):
        print_library_log("configuration.json must be a JSON object of key-value pairs.", Logging.Level.SEVERE,
                          log_icon=Logging.LogIcon.FAILURE)
        return 1
    password_names = {f.name for f in _password_fields(form.fields)}
    if any(isinstance(configuration.get(n), str) and configuration[n].strip()
           and not configuration[n].startswith(ENCRYPTED_VALUE_PREFIX) for n in password_names):
        print_library_log("Configuration contains plain-text password field values. "
                          "Re-run 'fivetran configuration' without --disable-encryption to encrypt them.",
                          Logging.Level.WARNING, log_icon=Logging.LogIcon.INFO)
    configuration = decrypt_configuration_values(configuration)
    print_library_log("Running setup tests...")
    for test in form.tests:
        response = connector.run_test(test.name, configuration)
        failure = response.failure
        print_library_log(f"[{test.name} - {test.label}]: {failure if failure is not None else 'PASSED'}")
        if failure is not None:
            print_library_log("Exiting due to test failure. Remaining tests skipped.", Logging.Level.SEVERE)
            return 1
    print_library_log("All tests passed!")
    return 0
