"""Backend HTTP clients for py_analytics.

This package is an **import leaf**. It may import ``matrice_common`` and the
standard library, and nothing else from ``matrice_analytics``. Everything here
is meant to be usable without dragging the rest of the SDK into the import
graph, which is what lets runtime modules depend on it rather than the reverse.

Importing anything from ``matrice_analytics.runtime`` or
``matrice_analytics.post_processing`` here would create an import cycle, because
those modules import this package. The direction is one-way by design:
``runtime`` may import ``clients``; ``clients`` may never import ``runtime``.

Submodules are imported explicitly by their users rather than re-exported here,
so that importing the package costs nothing a caller did not ask for.
"""
