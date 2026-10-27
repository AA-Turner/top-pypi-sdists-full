"""The fields of a connector's setup form: `TextField`, `DropdownField` and `ToggleField`.

Each builds a `FormField`, failing as it does on Fivetran for values that are rejected (a non-string label, a lone
surrogate, a required flag that is not an integer).
"""
from dataclasses import dataclass
from typing import List, Optional

from fivetran_connector_sdk_cli import wire

PLAIN_TEXT = 0
PASSWORD = 1
HIDDEN = 2
_TEXT_FIELD_NAMES = {"PlainText": PLAIN_TEXT, "Password": PASSWORD, "Hidden": HIDDEN}


@dataclass
class DropdownFieldParam:
    """Represents one selectable option in a DropdownField.

    Use `value` for the configuration value that should be saved and passed to your
    connector code. Use `label` and `description` only to control how the option is
    displayed in the setup form.

    Example:
        form_field.DropdownFieldParam(
            value="syncAll",
            label="Sync all accounts",
            description="Automatically sync all accounts you have access to.",
        )

    Args:
        value: Required option value. Converted to a string, stored in `configuration.json`,
            and passed to connector code when selected.
        label: Optional display name for this option. Defaults to `str(value)`.
        description: Optional help text shown with this option. Defaults to an empty string.
    """

    value: object
    label: Optional[str] = None
    description: Optional[str] = None


@dataclass(frozen=True)
class DropdownOption:
    value: str
    label: str
    description: str


@dataclass
class FormField:
    """One field of the setup form. At most one of `text_field`, `dropdown_options` and `toggle` says what kind it is."""
    name: str
    label: str
    required: Optional[bool] = None
    description: Optional[str] = None
    placeholder: Optional[str] = None
    text_field: Optional[int] = None
    dropdown_options: Optional[List[DropdownOption]] = None
    toggle: bool = False


class TextField:
    """Represents a text input form field.

    Use the class constants to specify the field type:
      - TextField.plain_text: visible plain-text input
      - TextField.password: masked password input

    Args:
        name: Unique identifier for this field, used as the configuration key.
        label: Human-readable label shown in the UI.
        field_type: One of TextField.plain_text or TextField.password.
            Defaults to TextField.plain_text.
        description: Optional help text displayed below the field.
        required: Whether the field must be filled before saving. Defaults to False.
        placeholder: Optional placeholder text shown when the field is empty.
    """

    plain_text = PLAIN_TEXT
    password = PASSWORD

    def __new__(
        cls,
        name: str,
        label: str,
        field_type: int = PLAIN_TEXT,
        *,
        description: Optional[str] = None,
        required: bool = False,
        placeholder: Optional[str] = None,
    ) -> FormField:
        field = FormField(
            name=wire.text(name),
            label=wire.text(label),
            text_field=None if field_type is None else wire.enum(field_type, _TEXT_FIELD_NAMES),
            required=wire.boolean(required),
        )
        if description is not None:
            field.description = wire.text(description, unset_if_none=False)
        if placeholder is not None:
            field.placeholder = wire.text(placeholder, unset_if_none=False)
        return field


class DropdownField:
    """Represents a dropdown selection form field.

    Args:
        name: Unique identifier for this field, used as the configuration key.
        label: Human-readable label shown in the UI.
        fields: List of DropdownFieldParam options. If every option only has a value, a simple
            dropdown is created. If a label or description is provided for an option, a rich UI dropdown will be created.
        description: Optional help text displayed below the field.
        required: Whether the field must be filled before saving. Defaults to False.
        placeholder: Optional placeholder text shown when no option is selected.

    Examples:
        form_field.DropdownField(
            name="namedRange",
            label="Named Range",
            fields=[
                form_field.DropdownFieldParam(value="TrustPilot_CurrentDate"),
                form_field.DropdownFieldParam(value="TrustPilot_History"),
            ]
        )

        form_field.DropdownField(
            name="accountSyncMode",
            label="Account sync mode",
            fields=[
                form_field.DropdownFieldParam(
                    value="syncAll",
                    label="Sync all accounts",
                    description="Automatically sync all accounts you access to.",
                ),
            ]
        )
    """

    def __new__(
        cls,
        name: str,
        label: str,
        *,
        fields: List[DropdownFieldParam],
        description: Optional[str] = None,
        required: bool = False,
        placeholder: Optional[str] = None,
    ) -> FormField:
        if not fields:
            raise ValueError(f"DropdownField '{name}' must define at least one option in 'fields'.")
        # The options are built before the field, as production builds its nested messages before the outer one.
        options = [
            DropdownOption(
                value=wire.text(str(item.value)),
                label=wire.text(str(item.label if item.label is not None else item.value)),
                description=wire.text("" if item.description is None else str(item.description)),
            )
            for item in fields
        ]
        field = FormField(
            name=wire.text(name),
            label=wire.text(label),
            dropdown_options=options,
            required=wire.boolean(required),
        )
        if description is not None:
            field.description = wire.text(description, unset_if_none=False)
        if placeholder is not None:
            field.placeholder = wire.text(placeholder, unset_if_none=False)
        return field


class ToggleField:
    """Represents a boolean toggle form field.

    Args:
        name: Unique identifier for this field, used as the configuration key.
        label: Human-readable label shown in the UI.
        description: Optional help text displayed below the field.
        required: Whether the field must be filled before saving. Defaults to False.
    """

    def __new__(
        cls,
        name: str,
        label: str,
        *,
        description: Optional[str] = None,
        required: bool = False,
    ) -> FormField:
        field = FormField(
            name=wire.text(name),
            label=wire.text(label),
            toggle=True,
            required=wire.boolean(required),
        )
        if description is not None:
            field.description = wire.text(description, unset_if_none=False)
        return field
