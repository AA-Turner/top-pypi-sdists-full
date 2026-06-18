# SPDX-FileCopyrightText: 2021 TU Wien.
# SPDX-FileCopyrightText: 2021 CERN.
# SPDX-License-Identifier: MIT

"""Type registry for looking up registered types per id.

The interface requires that the registered type have at least the property
``type_id`` defined:

.. code-block:: python

    class MyType(BaseType):
        type_id = "my-id"

Afterwards you can lookup types:

.. code-block:: python

    registry.lookup("my-id")
    for t in registry:
        # do something
"""


class TypeRegistry:
    """Registry for looking up registered types per id/name."""

    def __init__(self, types):
        """Constructor."""
        self._registered_types = {}
        for t in types:
            self.register_type(t)

    def register_type(self, type_, force=False):
        """Register the specified request_type."""
        type_id = type_.type_id

        if force:
            self._registered_types[type_id] = type_
        else:
            self._registered_types.setdefault(type_id, type_)

    def lookup(self, type_id, quiet=False, default=None):
        """Look up a registered type by its id."""
        if not quiet:
            return self._registered_types[type_id]

        return self._registered_types.get(type_id, default)

    def __iter__(self):
        """Iterate over all types."""
        for t in self._registered_types.values():
            yield t
