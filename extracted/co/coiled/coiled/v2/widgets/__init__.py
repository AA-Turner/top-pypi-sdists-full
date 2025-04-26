"""Status display widgets for Coiled cluster instances.

Each widget implementation must have an ``update()`` instance method that takes two
arguments. The first argument is the JSON response from the declarative
``/api/v2/clusters/account/{account}/id/{cluster_id}`` endpoint, parsed into a
dictionary. The second argument is a list of `coiled.v2.states.State` instances
that contain the state changes of the cluster, scheduler, and workers.

The widget implementation is then responsible for drawing itself to the environment.
Current implementations support Jupyter Notebook-like contexts and IPython console
contexts via the ``_ipython_display_`` and ``_repr_mimebundle_`` methods.

Please avoid adding unconditional dependencies on rendering or widget libraries, so
that people who only want to work in scripts don't have to install lots of packages
they won't need.
"""

from .interface import ClusterWidget
from .util import EXECUTION_CONTEXT

__all__ = ["EXECUTION_CONTEXT"]
