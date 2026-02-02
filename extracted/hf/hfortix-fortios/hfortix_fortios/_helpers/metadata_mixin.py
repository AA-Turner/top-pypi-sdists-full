"""
Metadata Mixin for FortiOS API Endpoints

Provides common metadata helper methods for all endpoint classes.
Each endpoint class inherits these methods and imports from their own
_helpers.<endpoint_name> module for endpoint-specific data.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from types import ModuleType


class MetadataMixin:
    """
    Mixin providing metadata helper methods for FortiOS API endpoint classes.

    This mixin provides a standardized interface for accessing schema metadata,
    field information, validation, and other introspection capabilities.

    Each endpoint class that inherits this mixin must define a class attribute:
        _helper_module_name: str  # Name of the helper module (e.g., "settings")

    The corresponding helper module at `_helpers.<endpoint_name>` must provide:
    - get_schema_info()
    - get_field_metadata(field_name)
    - get_all_fields()
    - validate_field_value(field_name, value)
    - REQUIRED_FIELDS
    - FIELDS_WITH_DEFAULTS
    - DEPRECATED_FIELDS (optional)
    """

    # Subclasses must define this
    _helper_module_name: str = ""

    @classmethod
    def _get_helper_module(cls) -> ModuleType:
        """Get the helper module for this endpoint class."""
        from importlib import import_module

        if not cls._helper_module_name:
            raise NotImplementedError(
                f"{cls.__name__} must define _helper_module_name class attribute"
            )

        # Determine the package based on the class's module
        package = cls.__module__.rsplit(".", 1)[0]
        return import_module(
            f"._helpers.{cls._helper_module_name}", package=package
        )

    @classmethod
    def help(
        cls, field_name: str | None = None, show_fields: bool = False
    ) -> None:
        """
        Display interactive help for this endpoint or specific field.

        Args:
            field_name: Optional field name to get help for. If None, shows full endpoint help.
            show_fields: Ignored (kept for compatibility, field list removed)

        Examples:
            >>> # Get comprehensive endpoint help
            >>> Address.help()

            >>> # Get field information
            >>> Address.help("name")

            >>> # Or use as instance method
            >>> fgt.api.cmdb.firewall.address.help()
        """
        if field_name is not None:
            # Show field-specific help
            helper_module = cls._get_helper_module()
            get_field_metadata = getattr(helper_module, "get_field_metadata")

            meta = get_field_metadata(field_name)
            if meta is None:
                print(f"\n❌ Unknown field: {field_name}\n")
                return

            print(f"\n{'=' * 80}")
            print(f"FIELD: {meta['name']}")
            print("=" * 80)
            print(f"Type: {meta['type']}")
            if "description" in meta:
                print(f"Description: {meta['description']}")
            print(
                f"Required: {'Yes' if meta.get('required', False) else 'No'}"
            )
            if "default" in meta:
                print(f"Default: {meta['default']}")
            if "options" in meta:
                print(f"Options: {', '.join(meta['options'])}")
            if "constraints" in meta:
                constraints = meta["constraints"]
                if "min" in constraints or "max" in constraints:
                    min_val = constraints.get("min", "?")
                    max_val = constraints.get("max", "?")
                    print(f"Range: {min_val} - {max_val}")
                if "max_length" in constraints:
                    print(f"Max Length: {constraints['max_length']}")
            print("=" * 80 + "\n")
            return

        # Show full endpoint help using the interactive help function
        from ..help import help as interactive_help

        interactive_help(cls)

    @classmethod
    def fields(
        cls, detailed: bool = False
    ) -> Union[dict[str, Any], list[str]]:
        """
        Get field information as dict with JSON intent.

        Args:
            detailed: If True, return dict with field metadata (default: False)

        Returns:
            Dict with field metadata if detailed=True, otherwise simple list of field names.
            All return values are JSON-serializable.

        Examples:
            >>> # Simple list
            >>> fields = Settings.fields()
            >>> print(f"Available fields: {len(fields)}")

            >>> # Detailed dict with metadata (JSON intent)
            >>> from hfortix_fortios.formatting import to_json
            >>> print(to_json(Settings.fields(detailed=True)))
        """
        helper_module = cls._get_helper_module()
        get_all_fields = getattr(helper_module, "get_all_fields")
        get_field_metadata = getattr(helper_module, "get_field_metadata")

        field_names = get_all_fields()

        if not detailed:
            return field_names

        # Build detailed dict - JSON serializable
        detailed_fields = {}
        for fname in field_names:
            meta = get_field_metadata(fname)
            if meta:
                detailed_fields[fname] = meta

        return detailed_fields

    @classmethod
    def field_info(cls, field_name: str) -> dict[str, Any] | None:
        """
        Get complete metadata for a specific field.

        Args:
            field_name: Name of the field

        Returns:
            Field metadata dict or None if field doesn't exist

        Examples:
            >>> info = Settings.field_info("machine-learning-detection")
            >>> print(f"Type: {info['type']}")
            >>> if 'options' in info:
            ...     print(f"Options: {info['options']}")
        """
        helper_module = cls._get_helper_module()
        get_field_metadata = getattr(helper_module, "get_field_metadata")

        return get_field_metadata(field_name)

    @classmethod
    def validate_field(
        cls, field_name: str, value: Any
    ) -> tuple[bool, str | None]:
        """
        Validate a field value against its constraints.

        Args:
            field_name: Name of the field
            value: Value to validate

        Returns:
            Tuple of (is_valid, error_message)

        Examples:
            >>> is_valid, error = Settings.validate_field("machine-learning-detection", "test")
            >>> if not is_valid:
            ...     print(f"Validation error: {error}")
        """
        helper_module = cls._get_helper_module()
        validate_field_value = getattr(helper_module, "validate_field_value")

        return validate_field_value(field_name, value)

    @classmethod
    def required_fields(cls) -> list[str]:
        """
        Get list of required field names.

        Note: Due to FortiOS schema quirks, some fields may be conditionally required.
        Always test with the actual API for authoritative requirements.

        Returns:
            List of required field names

        Examples:
            >>> required = Settings.required_fields()
            >>> print(f"Required fields: {', '.join(required)}")
        """
        helper_module = cls._get_helper_module()
        REQUIRED_FIELDS = getattr(helper_module, "REQUIRED_FIELDS")

        return REQUIRED_FIELDS.copy()

    @classmethod
    def defaults(cls) -> dict[str, Any]:
        """
        Get all fields with default values as dict with JSON intent.

        Returns dict regardless of client return_mode.
        Dict is JSON-serializable for easy conversion.

        Returns:
            Dict with field default values (JSON-serializable)

        Examples:
            >>> defaults = Settings.defaults()
            >>> payload = defaults.copy()
            >>> payload['name'] = 'my-custom-name'

            >>> # Print as formatted JSON
            >>> from hfortix_fortios.formatting import to_json
            >>> print(to_json(Settings.defaults()))
        """
        helper_module = cls._get_helper_module()
        FIELDS_WITH_DEFAULTS = getattr(helper_module, "FIELDS_WITH_DEFAULTS")

        return FIELDS_WITH_DEFAULTS.copy()

    @classmethod
    def schema(cls) -> dict[str, Any]:
        """
        Get complete schema information as dict with JSON intent.

        Returns dict regardless of client return_mode.
        Dict is JSON-serializable for easy conversion.

        Returns:
            Dict with schema metadata (JSON-serializable)

        Examples:
            >>> schema = Settings.schema()
            >>> print(f"Endpoint: {schema['endpoint']}")
            >>> print(f"Total fields: {schema['total_fields']}")

            >>> # Print as formatted JSON
            >>> from hfortix_fortios.formatting import to_json
            >>> print(to_json(Settings.schema()))
        """
        helper_module = cls._get_helper_module()
        get_schema_info = getattr(helper_module, "get_schema_info")

        return get_schema_info()
