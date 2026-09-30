"""The platform client: one session, and a live RPC handle off it.

``AnalyticsClient`` answers the routes that are keyed by nothing but themselves -- no
facial-recognition server, no LPR server, just the platform. Its three route groups are
reached as attributes rather than flattened onto the class, so a call site names the
producer that answers it without anyone reading a URL.

**Nine methods, ten endpoints.** All ten are here. Eight of them are one method each --
1, 2, 3, 4, 5, 8, 9 and 13 -- and 6 and 7 are the two routes to a single grant, reached
through :meth:`.applications_api.ApplicationsApi.mint_usecase_download`;
:mod:`.applications_api` says why they are one method and not two. A reader counting
methods should find nine.

Two things this class is careful about, both of which have burned this repository before.

**It never snapshots ``rpc``.** ``session.update()`` builds a *new* RPC and shuts the old
one down, so a handle copied at construction is a handle that stops working the moment
anything re-authenticates. :attr:`AnalyticsClient.rpc` is a property that reads through to
the session every time. That read goes through a property rather than straight to a
slot, so it costs ~105 ns rather than the ~53 ns a bare attribute would -- measured
2026-09-21, and still nothing against the round trip it guards.

**It degrades when the SDK is absent rather than failing three frames later.** Whether there
is a platform SDK to open a session with is :func:`~.bootstrap.attach_session`'s question, not
this class's -- all three clients in this package ask it the same way, and the reasoning about
what makes that guard easy to get wrong lives with the guard.

A client built without a session on a machine with no SDK therefore **constructs
successfully and has no session**. That is the intended outcome: an analytics-only
container should be able to build this object and skip the backend-dependent work, not die
at construction for want of a package it never meant to use.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping, Optional, Sequence, Tuple

from .actions_api import ActionsApi
from .applications_api import ApplicationsApi
from .bootstrap import attach_session, license_key, resolve_action_id
from .identity import (
    APP_DEPLOYMENT_ID_KEYS,
    APPLICATION_ID_KEYS,
    APPLICATION_VERSION_KEYS,
    config_get,
)
from .inference_api import InferenceApi
from .response import CallFailure

logger = logging.getLogger(__name__)


class AnalyticsClient:
    """The platform backend, as ten endpoints in three groups, plus one resolver.

    Args:
        session: An open ``matrice_common`` session to use. Omit it and the client asks
            :func:`~.bootstrap.get_session` for the process's own, building it on first
            use. Pass one when the caller already holds a session, or when a test needs
            the client to make no session of its own.

    Attributes:
        actions: Routes answered by be-actions -- this worker's launch record, and the Redis
            an instance publishes to.
        applications: Routes answered by be-application -- the application catalogue.
        inference: Routes answered by be-inference -- deployments, post-processing configs,
            sites and cameras.
        session: The session this client calls on, or ``None`` when the SDK is absent.
        rpc: The session's *current* RPC handle. Read through every time -- see the
            module docstring.

    The three groups are reached as attributes rather than flattened onto this class::

        client.inference.fetch_location(location_id)

    so a call site names the producer that answers it without anyone opening the file to
    find out. They are split by ``/v1`` prefix, which is both the platform's own division
    and this package's routing boundary -- ``/v1/inference/`` is locally owned and gets one
    base, the other two get the two-base retry.

    **Grouping inside this client is by prefix; ownership ACROSS clients is not.** Three
    ``/v1/actions/`` routes belong to ``FRClient`` and ``LPRClient`` instead, because a route
    belongs to the client that owns the id it is keyed by, and those three are keyed by a
    server id only those clients hold.

    **One method sits on the client itself rather than in a group**, and only one:
    :meth:`resolve_application_identity` reads an action record, then a deployment record,
    then post-processing configs, stopping at the first that answers. No group owns all three,
    and :mod:`.identity` -- which holds the resolution *order* for single-source fields --
    cannot hold this one because it does I/O. A second such method would be a reason to ask
    whether the groups are drawn right; one is the facade doing its job.
    """

    def __init__(self, session: Any = None) -> None:
        self._session = attach_session(session, what="the analytics client's platform session")
        self.actions = ActionsApi(self._require_session)
        self.applications = ApplicationsApi(self._require_session, license_key)
        self.inference = InferenceApi(self._require_session)

    def resolve_application_identity(
        self,
        post_processing_config: Any = None,
        *,
        identity: Optional[Mapping[str, Any]] = None,
        env: Optional[Mapping[str, str]] = None,
        argv: Optional[Sequence[str]] = None,
    ) -> Tuple[Optional[str], Optional[str]]:
        """``(application_id, application_version)`` -- from local data first, then the platform.

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
        extra: Any = identity or {}

        application_id = config_get(post_processing_config, APPLICATION_ID_KEYS) or config_get(
            extra, APPLICATION_ID_KEYS
        )
        application_version = config_get(
            post_processing_config, APPLICATION_VERSION_KEYS
        ) or config_get(extra, APPLICATION_VERSION_KEYS)
        if application_id and application_version:
            return application_id, application_version

        action_id = resolve_action_id(env=env, argv=argv)
        if action_id:
            try:
                params: Mapping[str, Any] = self.actions.get_action_details(action_id).job_params
            except CallFailure as exc:
                logger.debug("action %s gave no jobParams (%s)", action_id, exc)
                params = {}
            application_id = application_id or config_get(params, APPLICATION_ID_KEYS)
            application_version = application_version or config_get(
                params, APPLICATION_VERSION_KEYS
            )
            if application_id and application_version:
                return application_id, application_version

        deployment_id = config_get(post_processing_config, APP_DEPLOYMENT_ID_KEYS) or config_get(
            extra, APP_DEPLOYMENT_ID_KEYS
        )
        if not deployment_id:
            return application_id, application_version

        if not (application_id and application_version):
            try:
                deployment = self.inference.fetch_application_deployment(deployment_id)
            except CallFailure as exc:
                logger.debug("deployment %s gave no appVersion (%s)", deployment_id, exc)
                deployment = None
            if deployment is not None:
                application_id = application_id or deployment.app_id or None
                application_version = application_version or deployment.app_version or None
            if application_id and application_version:
                return application_id, application_version

        if not (application_id and application_version):
            # The post-processing config documents. Reached only when everything above came
            # back empty, and worth the call because it is still the *deployed* answer: these
            # are per-camera deployment config and they carry `_idApplication`. Trying this
            # before the published version is the difference between the right version and a
            # plausible one.
            try:
                documents = self.inference.fetch_post_processing_configs(deployment_id)
            except CallFailure as exc:
                logger.debug(
                    "deployment %s served no post-processing configs (%s)", deployment_id, exc
                )
                documents = []
            for document in documents:
                application_id = application_id or document.application_id or None
                if application_id:
                    break
            if application_id:
                logger.info(
                    "resolved the application id from the deployment's post-processing config "
                    "documents (application_id=%r) -- the deployed answer, after the action and "
                    "app-deployment records had none.",
                    application_id,
                )

        return application_id, application_version

    def _require_session(self) -> Any:
        """The session, or a named refusal -- what every route group is handed.

        A callable rather than the session itself, for the same reason :attr:`rpc` is a
        property: a handle taken once is a handle that goes stale when the session is
        rebuilt.

        It **raises rather than answering ``None``**, and that is the load-bearing part.
        ``bootstrap.get_action_record`` treats ``session=None`` as *"open the process
        session"*, so a group handed a bare ``None`` would quietly build a session the
        caller never asked for and then fail on credentials -- an error about the wrong
        thing, three frames from the missing SDK that actually caused it.

        Raises:
            CallFailure: There is no session; the SDK was absent when this client was built.
        """
        if self._session is None:
            raise CallFailure(
                "This AnalyticsClient has no session, so it cannot reach the platform. "
                "matrice_common was not importable when it was built."
            )
        return self._session

    @property
    def session(self) -> Any:
        """The session this client calls on, or ``None`` when the SDK is absent."""
        return self._session

    @property
    def rpc(self) -> Any:
        """The session's RPC handle, read fresh on every access.

        Not cached, and the distinction is not academic: ``session.update()`` replaces the
        session's RPC and shuts the previous one down. A handle held from construction is
        therefore a handle that works until the first re-authentication and silently stops
        afterwards. All four ``update()`` call sites in this repository are bootstrap-time,
        which is precisely when a client built early would be holding the stale one.

        Raises:
            CallFailure: There is no session -- the SDK was absent at construction, so the
                warning naming that has already been logged.
        """
        return self._require_session().rpc


__all__ = ["AnalyticsClient"]
