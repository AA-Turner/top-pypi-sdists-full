"""Auto-generated stub for module: analytics_client."""
from typing import Any, Optional, Tuple

from .actions_api import ActionsApi
from .applications_api import ApplicationsApi
from .bootstrap import attach_session, license_key, resolve_action_id
from .identity import APP_DEPLOYMENT_ID_KEYS, APPLICATION_ID_KEYS, APPLICATION_VERSION_KEYS, config_get
from .inference_api import InferenceApi
from .response import CallFailure

# Constants
logger: Any

# Classes
class AnalyticsClient:
    # The platform backend, as ten endpoints in three groups, plus one resolver.
    #
    #     Args:
    #         session: An open ``matrice_common`` session to use. Omit it and the client asks
    #             :func:`~.bootstrap.get_session` for the process's own, building it on first
    #             use. Pass one when the caller already holds a session, or when a test needs
    #             the client to make no session of its own.
    #
    #     Attributes:
    #         actions: Routes answered by be-actions -- this worker's launch record, and the Redis
    #             an instance publishes to.
    #         applications: Routes answered by be-application -- the application catalogue.
    #         inference: Routes answered by be-inference -- deployments, post-processing configs,
    #             sites and cameras.
    #         session: The session this client calls on, or ``None`` when the SDK is absent.
    #         rpc: The session's *current* RPC handle. Read through every time -- see the
    #             module docstring.
    #
    #     The three groups are reached as attributes rather than flattened onto this class::
    #
    #         client.inference.fetch_location(location_id)
    #
    #     so a call site names the producer that answers it without anyone opening the file to
    #     find out. They are split by ``/v1`` prefix, which is both the platform's own division
    #     and this package's routing boundary -- ``/v1/inference/`` is locally owned and gets one
    #     base, the other two get the two-base retry.
    #
    #     **Grouping inside this client is by prefix; ownership ACROSS clients is not.** Three
    #     ``/v1/actions/`` routes belong to ``FRClient`` and ``LPRClient`` instead, because a route
    #     belongs to the client that owns the id it is keyed by, and those three are keyed by a
    #     server id only those clients hold.
    #
    #     **One method sits on the client itself rather than in a group**, and only one:
    #     :meth:`resolve_application_identity` reads an action record, then a deployment record,
    #     then post-processing configs, stopping at the first that answers. No group owns all three,
    #     and :mod:`.identity` -- which holds the resolution *order* for single-source fields --
    #     cannot hold this one because it does I/O. A second such method would be a reason to ask
    #     whether the groups are drawn right; one is the facade doing its job.

    def __init__(self: Any, session: Any = None) -> None: ...

    def resolve_application_identity(self: Any, post_processing_config: Any = None) -> Tuple[Optional[str], Optional[str]]:
        """
        ``(application_id, application_version)`` -- from local data first, then the platform.
        
                The one method here that is not a single route. It reads three of them, in a fixed
                order, stopping at the first that answers both halves -- which is why it lives on the
                client rather than in a route group: no group owns all three, and
                :mod:`.identity` cannot hold it because that module does no I/O by contract.
        
                Order, cheapest and most local first. **Every step reports the version this deployment
                actually runs**; the published version is not among them and never resolves here --
                :meth:`.applications_api.ApplicationsApi.fetch_application` answers that different
                question.
        
                1. what the caller already holds -- ``post_processing_config``, then ``identity``,
                   which on the worker path is ``stream_info``. No I/O at all;
                2. this worker's own action record -- a ``deploy_add`` launch carries both halves in
                   ``jobParams``;
                3. the app-deployment record, which answers with the id **and** the version at once;
                4. the deployment's post-processing config documents, which carry ``_idApplication``.
                   Last because it is the only step that can return several documents, but still a
                   *deployed*-scope answer, so it belongs ahead of any published-version guess.
        
                Step 4 can only ever supply the **id**. The producer's
                ``PostProcessingConfigResponse`` sends seven fields and no version among them, so the
                version half of that step was unreachable before this method was typed and is absent
                now rather than silently failing.
        
                Every step's failure is swallowed to a debug line and the search continues: a record
                that cannot be read is a miss, not a fault, because a later source may still answer and
                the caller's own fallback is better than an exception from four routes down.
        
                Args:
                    post_processing_config: The caller's config, raw dict or parsed object -- both are
                        read, by key and by attribute respectively.
                    identity: Any other mapping that may carry these fields; ``stream_info`` on the
                        worker path.
                    env: Environment to resolve the action id from. Defaults to the process's own.
                    argv: Command line to resolve the action id from. Defaults to the process's own.
        
                Returns:
                    The pair, either half of which may be ``None``. ``None`` means *no source knew* and
                    is a refusal rather than a value; this method never invents one.
        """
        ...

    def rpc(self: Any) -> Any:
        """
        The session's RPC handle, read fresh on every access.
        
                Not cached, and the distinction is not academic: ``session.update()`` replaces the
                session's RPC and shuts the previous one down. A handle held from construction is
                therefore a handle that works until the first re-authentication and silently stops
                afterwards. All four ``update()`` call sites in this repository are bootstrap-time,
                which is precisely when a client built early would be holding the stale one.
        
                Raises:
                    CallFailure: There is no session -- the SDK was absent at construction, so the
                        warning naming that has already been logged.
        """
        ...

    def session(self: Any) -> Any:
        """
        The session this client calls on, or ``None`` when the SDK is absent.
        """
        ...

