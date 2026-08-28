"""Auto-generated stub for module: routing."""
from typing import Any

from .manifest.loader import redact_url

# Constants
Engine: Any
FlowMode: Any
logger: Any

# Functions
def normalise_app_name(name: str) -> str:
    """
    A deployment's ``app_name`` as an app id.
    
        The same normalisation the legacy resolver's display-name index used
        (``flow.py:_normalize``): lower-cased, with spaces and hyphens folded to underscores, so a
        deployment carrying ``"People Counting"`` resolves ``people_counting``.  Kept because that
        join is real -- ``app_name`` is a display string in some deployment records and an id in
        others.
    """
    ...
def resolve_flow_mode(env: Any[str, str] | None = None) -> Any:
    """
    Read ``MATRICE_ANALYTICS_FLOW``.
    
        Args:
            env: Environment to read.  Defaults to :data:`os.environ`; injectable so a test does
                not have to mutate process state.
    
        Returns:
            ``"auto"`` (the default), ``"old"`` or ``"new"``.
    
        Raises:
            RoutingError: The variable is set to something else.  Deliberately fatal: the legacy
                resolver lower-cased the value and fell through to ``auto``, so
                ``MATRICE_ANALYTICS_FLOW=newx`` meant "auto" and an operator who thought they had
                switched engines had not.  A typo in a routing switch must not be a silent no-op.
    """
    ...
def route_app(app: str | Any.Any[str] | None) -> Any:
    """
    Decide which engine runs ``app``.
    
        Args:
            app: What the deployment knows the app as -- a bare id (``people_counting``), a display
                name (``"People Counting"``), an app folder path, or a zip URL.  ``None`` or empty
                routes to legacy: an unnamed app cannot have a manifest.
            mode: Override the env var, for a caller that already has a policy.
            env: Environment to read ``MATRICE_ANALYTICS_FLOW`` from.  Injectable for tests.
            loader: The app loader.  Injectable so a caller can supply a cached or pre-warmed one;
                defaults to :func:`~matrice_analytics.engine.manifest.loader.load_app_bundle`,
                which resolves paths, URLs and bare ids and validates the manifest.
    
        Returns:
            The :class:`RoutingDecision`.  When ``engine == "new"`` it carries the already-loaded
            bundle, so the caller runs exactly the app that was approved.
    
        Raises:
            RoutingError: ``mode``/``MATRICE_ANALYTICS_FLOW`` is ``new`` and the app cannot run on
                the new engine, or the env var holds an unknown value.
    """
    ...
def unrunnable_primitives(manifest: Any, loaded: Any | None = None) -> tuple[str, ...]:
    """
    Every reason this build cannot run ``manifest``'s pipeline, one string each.
    
        Three conditions, all of which the runtime would otherwise discover at session start:
    
        * a primitive the manifest schema knows but the engine has not built
          (``IMPLEMENTED = False`` -- the schema deliberately validates apps ahead of the runtime,
          ``08`` §2);
        * a primitive with no entry in :data:`~matrice_analytics.engine.primitives.REGISTRY` --
          possible when a build ships a partial primitive set;
        * a ``custom`` stage whose implementation was not imported.  Only the loader imports an
          app's Python, so this is really "you were handed a manifest, not a bundle".
    
        Args:
            manifest: The validated manifest.
            loaded: The bundle it came from, when there is one.  Without it, ``custom`` stages
                cannot be checked and are reported as such.
    
        Returns:
            Human-readable problems, each naming the offending stage and primitive.  Empty means
            the pipeline is runnable.
    """
    ...

# Classes
class RoutingDecision:
    # Which engine runs, and the reason -- in words a log line can carry verbatim.

    def use_new_engine(self: Any) -> bool: ...

class RoutingError:
    # The new engine was explicitly requested and cannot run this app.
    #
    #     Raised only under ``MATRICE_ANALYTICS_FLOW=new``.  In ``auto`` the same condition returns a
    #     ``legacy`` :class:`RoutingDecision` whose ``reason`` names the cause -- an override,
    #     though, is an operator saying "use the new engine", and answering that with a silent legacy
    #     run is the failure mode this whole engine exists to remove.

    ...
