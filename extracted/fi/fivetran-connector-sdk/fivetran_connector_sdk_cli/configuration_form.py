"""The setup form a connector's `configuration_form()` returns, with the tests the platform can run against it."""
from dataclasses import dataclass
from typing import Callable, List, Optional

from fivetran_connector_sdk_cli import wire
from fivetran_connector_sdk_cli.form_field import FormField


@dataclass(frozen=True)
class ConfigurationTest:
    name: str
    label: str


@dataclass(frozen=True)
class ConfigurationFormResponse:
    fields: List[FormField]
    tests: List[ConfigurationTest]


def _varint(number: int) -> bytes:
    out = bytearray()
    while True:
        low = number & 0x7F
        number >>= 7
        out.append(low | 0x80 if number else low)
        if not number:
            return bytes(out)


def _field(number: int, payload: bytes) -> bytes:
    """A length-delimited field of the serialised form."""
    return _varint(number << 3 | 2) + _varint(len(payload)) + payload


def _text(number: int, value: str) -> bytes:
    """A string field of the serialised form: an empty string is not written."""
    return _field(number, value.encode("utf-8")) if value else b""


def _encode_form_field(field: FormField) -> bytes:
    """`common.proto` `FormField`, in field-number order."""
    out = _text(1, field.name) + _text(2, field.label)
    if field.required is not None:
        out += _varint(3 << 3) + (b"\x01" if field.required else b"\x00")
    if field.description is not None:
        out += _field(4, field.description.encode("utf-8"))
    if field.text_field is not None:
        out += _varint(5 << 3) + _varint(field.text_field & 0xFFFFFFFFFFFFFFFF)
    if field.toggle:
        out += _field(7, b"")
    if field.placeholder is not None:
        out += _field(9, field.placeholder.encode("utf-8"))
    if field.dropdown_options is not None:
        options = b"".join(
            _field(1, _text(1, o.value) + _text(2, o.label) + _text(3, o.description)) for o in field.dropdown_options)
        out += _field(12, options)
    return out


class _SerializedForm:
    """What the package carries: the form, serialised the way Fivetran reads it."""

    def __init__(self, response: "ConfigurationFormResponse"):
        self.response = response

    def SerializeToString(self) -> bytes:
        out = b"".join(_field(3, _encode_form_field(f)) for f in self.response.fields)
        out += b"".join(_field(4, _text(1, t.name) + _text(2, t.label)) for t in self.response.tests)
        return out


class ConfigurationForm:
    """Represents the setup form returned by the connector's configuration_form() method.

    Use add_field() to add form fields and add_test() to register setup test functions.
    The platform calls each registered test function by its __name__ when running setup tests.

    Example:
        def configuration_form():
            form = ConfigurationForm()
            form.add_field(form_field.TextField("host", "Host"))
            form.add_field(form_field.TextField("password", "Password", form_field.TextField.password))
            form.add_test(label="Test database connection", func=connection_test)
            return form
    """

    def __init__(self):
        self._fields = []
        self._tests = []  # list of (label: str, func: Callable)

    def add_field(self, field) -> "ConfigurationForm":
        """Adds a form field.

        Args:
            field: A form_field.TextField, DropdownField, or ToggleField instance.

        Returns:
            self, for method chaining.
        """
        if not isinstance(field, FormField):
            raise TypeError(f"field must be a form_field, got {type(field).__name__}: {field!r}")

        self._fields.append(field)
        return self

    def add_test(self, *, label: str, func: Callable) -> "ConfigurationForm":
        """Registers a setup test function.

        The function's __name__ is used as the test identifier sent to the platform.

        Args:
            label: Short human-readable description shown in the setup UI.
            func: The test function to call. Must accept a single configuration dict argument
                and return a Test().success() or Test().failure(...) result.

        Returns:
            self, for method chaining.
        """
        if not label:
            func_name = getattr(func, "__name__", repr(func))
            raise ValueError(f"label must not be empty for test function '{func_name}'")
        if not callable(func):
            raise TypeError("func must be callable")
        if func.__name__ == "<lambda>":
            raise ValueError(
                "anonymous lambda functions cannot be used as test functions; "
                "assign the function to a named variable first"
            )
        if any(f.__name__ == func.__name__ for _, f in self._tests):
            raise ValueError(
                f"a test function named '{func.__name__}' is already registered; "
                "each test function must have a unique name"
            )

        self._tests.append((label, func))
        return self

    def _get_test_function_by_name(self, name: str) -> Optional[Callable]:
        """Returns the registered test function matching the given name, or None."""
        for _, func in self._tests:
            if func.__name__ == name:
                return func
        return None

    def _to_proto(self) -> _SerializedForm:
        """The form as the platform reads it from a package (`SerializeToString()` gives the bytes)."""
        return _SerializedForm(self.to_response())

    def to_response(self) -> ConfigurationFormResponse:
        return ConfigurationFormResponse(
            fields=list(self._fields),
            tests=[
                ConfigurationTest(name=wire.text(func.__name__), label=wire.text(label))
                for label, func in self._tests
            ],
        )
