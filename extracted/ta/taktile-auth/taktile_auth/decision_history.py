import typing as t

from taktile_auth.exceptions import InsufficientRightsException, TaktileAuthException
from taktile_auth.schemas.token import TaktileIdToken


class EnvironmentNotQueryableException(TaktileAuthException):
    """The request named an environment the read cannot express.

    Distinct from a refusal: the caller may well hold the grant, so a consumer
    maps this to "unsupported" rather than "forbidden".
    """


LIVE: t.Final = "live"
SANDBOX: t.Final = "sandbox"
TEST: t.Final = "test"

ALL_ENVIRONMENTS: t.Final = (LIVE, SANDBOX, TEST)
LIVE_AND_SANDBOX: t.Final = (LIVE, SANDBOX)


def _as_tuple(environments: t.Union[str, t.Iterable[str], None]) -> t.Tuple[str, ...]:
    """Normalise a selector, treating a bare string as naming one environment.

    ``str`` is itself an ``Iterable[str]``, so without this a caller passing
    ``LIVE`` is silently iterated into its characters.
    """
    if environments is None:
        return ()
    if isinstance(environments, str):
        return (environments,)
    return tuple(dict.fromkeys(environments))


def environment_permission(organization_id: str, workspace_id: str, environment: str) -> str:
    """The env-scoped Decision History read permission."""
    return f"r:decision_history/{organization_id},{workspace_id},{environment}"


def flat_permission(organization_id: str, workspace_id: str) -> str:
    """The env-unaware Decision History read permission, which entitles every environment."""
    return f"r:workspace_decision_history/{organization_id},{workspace_id}"


class EnvironmentFilter(t.NamedTuple):
    """How a Decision History query must be filtered for the caller.

    ``filter_to is None`` means emit no environment predicate at all, which is not
    the same as naming every environment: an unfiltered query also returns rows in
    environments the selector cannot name.
    """

    filter_to: t.Optional[t.Tuple[str, ...]]

    def as_environment(self) -> t.Optional[str]:
        """The single environment this filter narrows to, ``None`` for more than one.

        ``None`` is "do not narrow" rather than "no environment": a caller entitled
        to several would lose the rest if the query named one.
        """
        if self.filter_to is None or len(self.filter_to) != 1:
            return None
        return self.filter_to[0]

    def covers(self, environments: t.Union[str, t.Iterable[str]]) -> bool:
        """Whether the caller may read every one of these environments.

        For a finished artefact there is nothing to narrow, so the question is
        containment rather than filtering. An unfiltered read reaches every
        environment and so covers any of them.
        """
        return self.filter_to is None or set(_as_tuple(environments)) <= set(self.filter_to)


def authorize_environments(
    token: TaktileIdToken,
    *,
    organization_id: str,
    workspace_id: str,
    environments: t.Union[str, t.Iterable[str], None] = None,
    queryable: t.Collection[str] = ALL_ENVIRONMENTS,
) -> EnvironmentFilter:
    """Authorize a Decision History read and return how to filter it.

    ``environments`` is the request's selector, ``None`` or empty meaning every
    environment, since an un-narrowed query returns them all. Raises when the caller
    is entitled to none of the requested scope; otherwise the result must be applied
    to the query, because a caller entitled to only part of the scope is narrowed
    rather than rejected. ``queryable`` bounds what a narrowed read is
    filtered to: naming an environment outside it raises
    :class:`EnvironmentNotQueryableException`, and narrowing drops it. It does not
    bound the no-narrowing answer — ``filter_to is None`` means emit no predicate,
    which is deliberately not the same as naming every environment, so a fully
    entitled caller still reads whatever the query returns unfiltered.

    The flat legacy grant entitles every environment, so a caller still on it reads
    the full scope unchanged, and only that path logs ``authz-discrepancy``.

    Environment names are the values in :data:`ALL_ENVIRONMENTS`; callers holding
    their own environment type map to them before calling.
    """
    requested = _as_tuple(environments)
    named = bool(requested)
    if not named:
        requested = ALL_ENVIRONMENTS
    if any(environment not in ALL_ENVIRONMENTS for environment in requested):
        # An environment nobody can hold a grant for is a refusal, not a crash.
        raise InsufficientRightsException("insufficient-rights-exception")
    unnarrowed = requested if named else None

    if named:
        unqueryable = [environment for environment in requested if environment not in queryable]
        if unqueryable:
            raise EnvironmentNotQueryableException(unqueryable[0])

    entitled = tuple(
        environment
        for environment in requested
        if token.has_access(environment_permission(organization_id, workspace_id, environment))
    )
    if entitled == requested:
        return EnvironmentFilter(unnarrowed)

    try:
        token.assert_access_with_fallback(
            [environment_permission(organization_id, workspace_id, environment) for environment in requested],
            fallback_permission=flat_permission(organization_id, workspace_id),
        )
    except InsufficientRightsException:
        pass
    else:
        return EnvironmentFilter(unnarrowed)

    narrowed = tuple(environment for environment in entitled if environment in queryable)
    if not narrowed:
        raise InsufficientRightsException("insufficient-rights-exception")
    return EnvironmentFilter(narrowed)


def assert_readable(
    token: TaktileIdToken,
    *,
    organization_id: str,
    workspace_id: str,
    environment: str,
) -> None:
    """Raise unless the caller may read Decision History in ``environment``.

    The request names one environment, so there is nothing to narrow and no filter
    to apply — which is why this returns nothing rather than a filter a caller
    could drop.
    """
    authorize_environments(
        token,
        organization_id=organization_id,
        workspace_id=workspace_id,
        environments=[environment],
    )


def assert_all_readable(
    token: TaktileIdToken,
    *,
    organization_id: str,
    workspace_id: str,
    environments: t.Union[str, t.Iterable[str]],
) -> None:
    """Raise unless the caller may read every one of ``environments``.

    Partial entitlement is a refusal rather than a narrowing, which is what a
    finished artefact needs: it cannot be filtered after the fact the way a query
    can.
    """
    requested = _as_tuple(environments)
    if not requested:
        return
    if not authorize_environments(
        token,
        organization_id=organization_id,
        workspace_id=workspace_id,
        environments=requested,
    ).covers(requested):
        raise InsufficientRightsException("insufficient-rights-exception")


def assert_any_readable(token: TaktileIdToken, *, organization_id: str, workspace_id: str) -> None:
    """Raise unless the caller may read Decision History in some environment.

    For an endpoint whose environment is only knowable from the record it operates
    on, this is what can be checked before the record is loaded: a caller entitled
    to nothing is refused without being told whether the id exists.
    """
    authorize_environments(token, organization_id=organization_id, workspace_id=workspace_id)
