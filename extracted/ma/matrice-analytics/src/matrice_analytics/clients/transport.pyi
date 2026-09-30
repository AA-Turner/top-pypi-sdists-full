"""Auto-generated stub for module: transport."""
from typing import Any, Callable, Optional, Tuple

from .response import CallFailure, ConnectionLost, MalformedReply, RateLimited

# Constants
ENV_API_BASE: str
LICENSE_KEY_HEADER: str
LOCAL_AUTHORITY_PREFIXES: Tuple[Any, ...]
POOLED_POST_TIMEOUT_S: float
SERVICE_NAME: str
UPLOAD_TIMEOUT_S: float
logger: Any

# Functions
def backend_base_url(env: Optional[Any[str, str]] = None) -> str:
    """
    The backend's own address, for a route the session's base URL will not serve.
    
        Deployments set ``MATRICE_BASE_URL`` to a local gateway (``http://localhost``). That gateway
        proxies the route prefixes it knows -- ``/v1/inference/*`` among them, which is why
        ``PostProcessingConfigClient`` has always worked -- and 302s anything else out to the real
        backend. ``matrice_common``'s client has ``follow_redirects=True``, and httpx drops the
        ``Authorization`` header when a redirect crosses origin, so a redirected call arrives
        unauthenticated and be-application answers 404. Observed in production on 0.1.428:
        ``http://localhost/v1/applications/.../usecase/download`` -> 302 -> prod -> 404, while the same
        path with a direct base URL returns 200.
    
        Derived the same way ``matrice_common`` derives its own default, so an on-prem or non-prod
        deployment still lands on its own backend; ``$MATRICE_APP_BUNDLE_API_BASE`` overrides it.
    """
    ...

# Classes
class PooledPoster:
    # POST to one host over a **kept-alive** connection pool, and say what went wrong.
    #
    #     The counterpart to :func:`_rpc_sent` for a route that runs often enough that opening a
    #     connection per call is the dominant cost. ``rpc.async_send_request`` opens
    #     ``aiohttp.ClientSession`` inside the call and closes it on the way out, so every request
    #     pays a fresh connection; this holds one session and reuses its connections. Measured on
    #     loopback with a 40 KB body (2026-09-21): 0.68 ms per request against 1.08 ms. The
    #     absolutes are this machine's and drift with it; the ratio is the point, and it is the
    #     shape aiohttp's own documentation describes when it says to hold one session for the
    #     application's lifetime rather than one per request.
    #
    #     **Only for a route that is hot enough to justify it.** A pool is state, and state has to be
    #     closed; :func:`_rpc_sent` stays the right verb everywhere else precisely because it has
    #     none.
    #
    #     **The session is bound to the event loop that first uses it.** aiohttp attaches the
    #     connector to the running loop, so a session created on one loop and used from another
    #     fails at the point of use. It is therefore created lazily, on first send, rather than in
    #     ``__init__`` -- which also keeps construction free of I/O, the property the three clients
    #     in this package share.
    #
    #     **``aiohttp`` is imported inside the send, not at module scope.** It is not a declared
    #     dependency of this package, and importing it costs ~220 ms and ~26 MB against this
    #     module's own ~11 ms -- a cost every importer would pay whether or not it ever posts. Once
    #     ``sys.modules`` is warm the in-function import costs ~120 ns. (All measured
    #     2026-09-21.) When it is absent altogether, :meth:`post` falls back to
    #     ``rpc.async_send_request``, which imports it the same way and fails the same way; a
    #     deployment without aiohttp is no worse off than it is today.
    #
    #     **What this class decides, and what it refuses to decide.** It reconnects once when the
    #     pool hands out a connection the server had already closed, because that request provably
    #     never left and the retry is the first attempt finishing rather than a second one. It does
    #     **not** re-send a request that reached the producer: whether that is safe is the caller's
    #     knowledge, not this class's, and :class:`~.lpr_client.LPRClient` says so in its own words.
    #     A 429 is reported, never slept on -- how long to wait, and whether the payload is still
    #     worth sending when the wait is over, belongs to the caller that owns the queue.

    def __init__(self: Any, session_provider: Callable[[], Any]) -> None:
        """
        Args:
            session_provider: Returns the ``matrice_common`` session to authenticate against,
                read at send time rather than held, because ``session.update()`` replaces the
                session's RPC and shuts the previous one down.
            timeout_s: Total timeout for one request, baked into the pooled session when it is
                created. Changing it afterwards does not reach a session already built.
        """
        ...

    async def aclose(self: Any) -> None:
        """
        Close the pool. Call from the event loop that sent on it.
        
                Idempotent, and free on a poster that never sent: the session is built on the first
                send, so there is nothing to close before it.
        """
        ...

    async def post(self: Any, path: str) -> Any:
        """
        Send one request over the pool and return what ``validate`` makes of the reply.
        
                The signature is :func:`_rpc_sent`'s minus ``method``, because a pool is only worth
                holding for a route that is written to repeatedly, and every such route here is a POST.
        
                Args:
                    path: The path, already filled in and already carrying any query string.
                    what: What is being attempted, phrased to read inside an error message.
                    unwrap: The unwrap belonging to this route's **producer**.
                    validate: Builds the return value from the payload. Not called on an absence.
                    base_url: The host to send to. Required, as for :func:`_rpc_sent`.
                    payload: The request body.
        
                Returns:
                    Whatever ``validate`` builds, or ``None`` when the producer answers with no payload.
        
                Raises:
                    RateLimited: The producer answered 429. Carries ``Retry-After`` when it sent one.
                    ConnectionLost: Two connection attempts failed in a row, so the request never left.
                    CallFailure: Anything else -- no session, no aiohttp *and* no fallback, a non-2xx,
                        or a producer that reported failure in its envelope.
        """
        ...

class Uploader:
    # PUT bytes at a URL that already carries its own authorisation.
    #
    #     **Not a producer route, and deliberately not on a client's route list.** The URL is
    #     handed over at runtime -- a producer answers a write with the storage address it
    #     resolved, and the bytes go there next. There is no path template, no base URL and no
    #     session: a pre-signed URL carries its own credentials in the query string, so adding
    #     an ``Authorization`` header would be wrong, not merely redundant.
    #
    #     It lives here rather than in a usecase because it is transport, and because the
    #     connection pool is this layer's job. The call it replaces opened a fresh
    #     ``httpx.AsyncClient`` per upload; one session is held here and its connections reused,
    #     the same reasoning as :class:`PooledPoster`.
    #
    #     ``aiohttp`` is imported inside the send for the reason the class above gives: ~220 ms
    #     and ~26 MB at module scope, against this module's own ~11 ms.

    def __init__(self: Any) -> None: ...

    async def aclose(self: Any) -> None:
        """
        Close the pool. Free on a putter that never sent -- it opens nothing until then.
        """
        ...

    async def put(self: Any, url: str, content: Any) -> bool:
        """
        Send ``content`` to ``url``. ``True`` when the store accepted it.
        
                Returns ``False`` rather than raising, for every failure: a frame that did not
                reach storage is a lost frame, not a lost request, and the caller's next frame is
                along in milliseconds. The reason is logged once, where it happened.
        
                Reporting is an explicit call rather than a handler for that same reason -- a refusal
                arrives as a status, not as an exception, so there is nothing for a handler to catch.
                Object storage is reached directly, so nothing else in the stack sees these at all.
        """
        ...

