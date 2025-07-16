"""Deprecated. Install `copier-template-extensions` instead."""

import warnings

from copier_template_extensions import ContextHook, TemplateExtensionLoader

__all__: list[str] = ["ContextHook", "TemplateExtensionLoader"]

warnings.warn(
    "This package is deprecated and renamed to `copier-template-extensions`. "
    "Please install `copier-template-extensions` instead, and replace every occurrence "
    "of `copier-templates-extensions` and `copier_templates_extensions` in your template with "
    "`copier-template-extensions` and `copier_template_extensions` respectively.",
    DeprecationWarning,
    stacklevel=2,
)
