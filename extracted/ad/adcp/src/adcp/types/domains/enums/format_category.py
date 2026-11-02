"""Deprecation shim for the removed ``format_category`` submodule.

``FormatCategory`` was replaced by free-form ``FormatId`` strings in
AdCP 3.0. See MIGRATION_v3_to_v4.md for the full migration path.

Importing this module raises :class:`ImportError` with a pointer to the
migration guide — so downstream import sites like::

    from adcp.types.domains.enums.format_category import FormatCategory

get the same pointer as the top-level ``from adcp import FormatCategory``,
instead of a bare ``ModuleNotFoundError``.

This file is restored after every codegen run by
``scripts/post_generate_fixes.py`` (which wipes the generated tree).
"""

raise ImportError(
    "adcp.types.domains.enums.format_category was removed in AdCP 3.0. "
    "Use free-form format-id strings (e.g. 'goog:video_responsive_ad') via "
    "adcp.types.FormatId. See MIGRATION_v3_to_v4.md#creative-format-asset-slots-formataasset-aliases "
    "for details."
)
