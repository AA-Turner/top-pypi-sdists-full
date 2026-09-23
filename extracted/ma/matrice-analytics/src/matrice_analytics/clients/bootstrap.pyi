"""Auto-generated stub for module: bootstrap."""
from typing import Any, Optional

from .response import CallFailure

# Constants
ENV_ACTION_ID: str
ENV_ACTION_ID_BARE: str

# Functions
def get_session(what: str = 'the platform session') -> Any:
    """
    The process's one ``matrice_common`` session, built on first use.
    
        Lazy because a container that never needs the platform should never pay for a session, and
        should not fail at import time for want of credentials it does not use. Memoised per
        *process*, not per caller: sessions are built from the same two environment variables
        wherever they are opened, so a second one is the same handle at the cost of another
        credential exchange.
    
        Thread-safe under the double-checked pattern -- the fast path is a bare read once the
        session exists, and the lock is taken only while the process is still cold.
    
        A failure is **not** memoised: ``_SESSION`` is assigned only on success, so a container that
        starts before its credentials are mounted recovers on the next call instead of being stuck
        with the first error for its lifetime.
    """
    ...
def open_session(what: str) -> Any:
    """
    A ``matrice_common`` session from the container's own credentials.
    
        Imported lazily, exactly as ``PostProcessingConfigClient.__init__`` does, so this module stays
        importable in an image with no platform SDK.
    
        Opens a **new** session every call. Callers that want one session for the life of the process
        use :func:`get_session` instead; this one stays uncached so that a caller who needs a session
        independent of anyone else's -- or a test that needs two -- can still get one.
    
        Credentials come from ``matrice_common.resolve_credentials``, which is the same three-tier
        order ``Session.__init__`` itself applies: an explicit argument, then the SDK's in-process
        registry, then the environment. Reading ``os.environ`` directly -- as this did until now --
        sees only the last of the three, so a container whose credentials were published to the
        registry by an SDK entry point was refused for want of variables it never needed to export.
        That is reachable rather than theoretical: ``Session`` used to copy explicit keys back into
        ``os.environ`` and deliberately stopped, because the environment is inherited by every
        subprocess and captured by most crash reporters.
    """
    ...
def resolve_action_id(env: Optional[Any[str, str]] = None, argv: Optional[Any[str]] = None) -> Optional[str]:
    """
    The action record id for this worker, if it can be determined locally.
    
        Three sources, no I/O. ``$MATRICE_ACTION_ID`` first, because an operator setting it means it,
        then ``$ACTION_ID`` -- the bare name the Go services and the ENV_ID_ACTIONS images read, and the
        only one some py_compute launch paths emitted. Then ``sys.argv``: py_compute launches every
        action container as ``python3 <entrypoint>.py <action_record_id> <port>``, so the id is the
        first argument that looks like an ObjectId. Matching on shape rather than position keeps this
        from mistaking a port or a flag for an id.
    
        A malformed value in either env var falls through rather than erroring, so a truncated id does
        not mask a good one in argv.
    """
    ...
