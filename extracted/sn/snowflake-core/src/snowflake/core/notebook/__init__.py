"""Manages Snowflake Notebooks.

``snowflake.core.notebook`` is deprecated. Snowflake is disabling creation of new
Legacy Notebooks, starting September 1, 2026. A later change, planned for
November 2026, forbids editing and executing existing Legacy Notebooks as well.
Importing this package emits a ``DeprecationWarning``.

Examples:
    >>> notebooks: NotebookCollection = root.databases["my_db"].schemas["my_schema"].notebooks
    >>> my_notebook = notebooks.create(Notebook("my_notebook"))
    >>> notebook_iter = notebooks.iter(like="my%")
    >>> notebook = notebooks["my_notebook"]
    >>> an_existing_notebook = notebooks["an_existing_notebook"]

Refer to :class:`snowflake.core.Root` to create the ``root``.
"""

import warnings

from ._notebook import Notebook, NotebookCollection, NotebookResource, VersionDetails


warnings.warn(
    "snowflake.core.notebook is deprecated. Snowflake is disabling creation of new "
    "Legacy Notebooks, starting September 1, 2026. A later change, planned for "
    "November 2026, forbids editing and executing existing Legacy Notebooks as well. "
    "See https://docs.snowflake.com/en/release-notes/bcr-bundles/un-bundled/bcr-disable-legacy-notebooks.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["Notebook", "NotebookCollection", "NotebookResource", "VersionDetails"]
