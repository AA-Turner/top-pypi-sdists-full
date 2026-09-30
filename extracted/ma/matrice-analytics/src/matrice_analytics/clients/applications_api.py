"""Routes answered by **be-application**, reached through the platform gateway.

be-application answers three of the twenty-four endpoints in :mod:`.models` -- 3, 6 and 7 --
and all three belong to ``AnalyticsClient``. All three are here.

``matrice_analytics.runtime.app_bundle`` still holds its own copies of 6 and 7
(``_mint_via_license`` and ``mint_usecase_download_url``) and is still what production
calls. Those are deleted, and their caller repointed here, when the runtime migration
reaches that module; until then the two implementations coexist deliberately, so that
adding these routes changed no behaviour anywhere.

The two download routes are one method
======================================

Endpoints 6 and 7 are two ways to obtain **one** thing -- a presigned URL for a version's
usecase bundle -- so they are one method, :meth:`ApplicationsApi.mint_usecase_download`,
and not two. Exposing them separately would publish a choice no caller is in a position to
make: which route works depends on whether the deployment holds a licence, which the caller
does not know and should not have to ask.

**Neither route can ship alone.** In a deployed container the unlicensed route answers
**404 unauthenticated** -- the gateway's cross-origin redirect drops the auth header -- and
**401 with the container's own token**. The licensed route is the one a container can
actually use, so a lone unlicensed route would read as available and fail everywhere it
matters. A test pins that the two arrive together.

**A synchronous verb that carries headers.** The licensed route sends an ``X-License-Key``
header. ``rpc.get`` has no ``headers`` parameter and drops one with a single warning, so a
call built on it fails as unauthorised rather than as misconfigured;
:func:`~.transport._rpc_sent` does carry headers but is ``async``, and every method here is
synchronous. :func:`~.transport._rpc_headed` is the verb, and it exists for this route.

**One base, the cloud one.** The licensed route is served only by the cloud backend; on an
on-prem box the local nginx does not serve it at all. So it takes
:func:`~.transport.backend_base_url` explicitly and sends once -- the reverse of the two-base
retry the unlicensed route uses.

**The licence is handed in, not read here.** This group resolves nothing, and a test pins it
at zero environment reads. :func:`~.bootstrap.license_key` does the reading, beside
:func:`~.bootstrap.resolve_action_id`, because both answer *what was this container handed at
startup?*; ``AnalyticsClient`` wires it in. A group that read one variable itself would be the exception that ends the rule, and the
rule is what lets every method here be tested with a literal.

**A missing key is not a failure.** Without a licence the licensed route is not attempted at
all and the unlicensed one answers. Raising there would break every unlicensed deployment.
An *attempted* licensed call that fails is a different thing and does raise: falling through
then would report a routing fault as an ordinary unlicensed deployment.

**Two error codes that mean different things.** On the licensed route a 400 means the version
has no usecase bundle attached, which is the ordinary legacy case, and a 401 means the key
was rejected. The message says which.
"""

from __future__ import annotations

from typing import Any, Callable, Mapping, Optional

from .models import Application
from .response import CallFailure, unwrap_platform
from .transport import (
    LICENSE_KEY_HEADER,
    _describe,
    _rpc_data,
    _rpc_headed,
    _rpc_model,
    backend_base_url,
)


class ApplicationsApi:
    """``AnalyticsClient.applications`` -- the application catalogue.

    Args:
        session_provider: Called for the session to ride on each request. A callable rather
            than a session, so a client that rebuilds its session is followed rather than
            outrun.
        license_key_provider: Called for the deployment's licence key, or ``None`` when the
            caller has no licence to offer -- which is the same as holding an empty one and
            takes the unlicensed route. A callable for the same reason as the session: the
            answer is read at call time rather than frozen at construction.
    """

    #: The catalogue entry for one application.
    APPLICATION = "/v1/applications/{application_id}"

    #: Endpoint 6 -- the licensed grant. Guarded by the licence, not by the session.
    #: ``license/`` is a path prefix and ``versions`` is plural: this is the spelling
    #: ``be-application`` serves and the one production has always called.
    USECASE_DOWNLOAD_LICENSE = (
        "/v1/applications/license/{application_id}/versions/{application_version}/usecase/download"
    )

    #: Endpoint 7 -- the same grant, guarded by the session's own credentials.
    USECASE_DOWNLOAD = (
        "/v1/applications/{application_id}/versions/{application_version}/usecase/download"
    )

    def __init__(
        self,
        session_provider: Callable[[], Any],
        license_key_provider: Optional[Callable[[], str]] = None,
    ) -> None:
        self._session_provider = session_provider
        self._license_key_provider = license_key_provider

    def fetch_application(self, application_id: str) -> Optional[Application]:
        """The catalogue entry for one application, or ``None`` if there is no such entry.

        Note that the record's own id field is spelled ``applicationid``, all lowercase, by
        the producer; the model carries the alias so callers read ``application_id``.

        This record knows the **published** version, which is routinely not the version a
        given deployment runs. A caller that wants the deployed one wants endpoint 2.

        Args:
            application_id: The application to read.

        Returns:
            The entry, or ``None`` when the platform reports no such application.

        Raises:
            CallFailure: No base URL produced either an entry or an absence.
        """
        return _rpc_model(
            self._session_provider(),
            self.APPLICATION.format(application_id=application_id),
            what=f"the catalogue entry for application {application_id}",
            unwrap=unwrap_platform,
            validate=Application.model_validate,
        )

    def mint_usecase_download(self, application_id: str, application_version: str) -> str:
        """A fresh presigned URL for this version's usecase bundle.

        Minted on demand rather than read out of config: the URLs be-application issues live
        for five hours, and a deployment's config outlives that by design.

        Two routes answer this, and which one is used is not the caller's business -- see the
        module docstring. With a licence the licensed route is tried; without one it is not
        attempted at all and the unlicensed route answers.

        Args:
            application_id: The application whose bundle is wanted.
            application_version: The version of it.

        Returns:
            The URL. Never ``""`` and never ``None`` -- a caller gets a usable URL or a failure
            naming the application, not an absence to trip over later.

        Raises:
            CallFailure: Neither route produced a URL. The message says which was tried and
                distinguishes a version with no bundle attached from a rejected licence.
        """
        key = "" if self._license_key_provider is None else self._license_key_provider()
        if key:
            return self._mint_licensed(application_id, application_version, key)
        return self._mint_unlicensed(application_id, application_version)

    def _mint_licensed(self, application_id: str, application_version: str, key: str) -> str:
        """Endpoint 6. Raises rather than falling through, and that is the whole point.

        A licence that is present but does not work is not the unlicensed case. Falling through
        here would send the request again on a route a deployed container cannot use, and report
        the resulting 404 as though the deployment simply had no licence -- turning a rejected
        key or a missing bundle into a misleading answer two routes away from the cause.

        The envelope is read here rather than through :func:`~.response.unwrap_platform` for the
        same reason: that unwrap answers ``None`` for a clean 404, which on this route would be
        indistinguishable from "no licence, not attempted".
        """
        path = self.USECASE_DOWNLOAD_LICENSE.format(
            application_id=application_id, application_version=application_version
        )
        what = f"the bundle URL for application {application_id} version {application_version}"
        base = backend_base_url()

        response = _rpc_headed(
            self._session_provider(),
            path,
            what=what,
            headers={LICENSE_KEY_HEADER: key},
            base_url=base,
        )

        # The success flag is checked before the payload, not alongside it: a failed envelope can
        # still carry a `data` object, and reading the URL out of one would turn a refusal into a
        # URL that does not work.
        if isinstance(response, Mapping) and response.get("success"):
            url = self._download_url(response.get("data"))
            if url:
                return url

        raise CallFailure(
            f"GET {base}{path} did not succeed while resolving {what}: {_describe(response)}. "
            f"A 400 here means the version has no usecase bundle attached, which is the ordinary "
            f"legacy case; a 401 means the licence key was rejected."
        )

    def _mint_unlicensed(self, application_id: str, application_version: str) -> str:
        """Endpoint 7, through the two-base retry.

        This route lives on be-application, which the local gateway does not proxy, so it needs
        the same direct-base-url fallback the catalogue lookups get.
        """
        path = self.USECASE_DOWNLOAD.format(
            application_id=application_id, application_version=application_version
        )
        what = f"the bundle URL for application {application_id} version {application_version}"

        try:
            data = _rpc_data(self._session_provider(), path, what=what)
        except CallFailure as exc:
            # By far the commonest failure is "this version has no bundle", which is not a fault.
            # Say so, so nobody reads a routine legacy app as a broken one.
            raise CallFailure(
                f"{exc} A 400 on this route means the version has no usecase bundle attached, "
                f"which is the ordinary legacy case."
            ) from exc

        # No success check here: `_rpc_data` has already made one, and raised if it failed.
        url = self._download_url(data)
        if url:
            return url

        raise CallFailure(
            f"GET {path} succeeded but returned no downloadUrl: {data!r}. A 400 on this route "
            f"means the version has no usecase bundle attached, which is the ordinary legacy case."
        )

    @staticmethod
    def _download_url(data: Any) -> str:
        """The URL out of a route's ``data``, or ``""`` when it carries none.

        Takes the payload rather than the envelope, because the two routes arrive with different
        amounts of envelope already removed and only one of them still needs its success flag
        checked -- keeping that check at the call site is what stops this helper looking like it
        performs one.

        Both spellings are accepted because both are sent: the producer answers ``downloadUrl``
        and some replies carry ``download_url``.
        """
        if not isinstance(data, Mapping):
            return ""
        url = data.get("downloadUrl") or data.get("download_url")
        return url.strip() if isinstance(url, str) else ""


__all__ = ["ApplicationsApi"]
