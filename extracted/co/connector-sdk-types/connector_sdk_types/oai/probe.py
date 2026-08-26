"""Building blocks for `probe_integration`, usable without the connector SDK."""

from __future__ import annotations

import asyncio
import inspect
import time
import typing as t
from collections.abc import Awaitable, Callable, Collection, Mapping, Sequence
from contextlib import AsyncExitStack, ExitStack

from pydantic import BaseModel, Field, StrictBool, StrictStr
from typing_extensions import Self

# Import directly from modules to avoid a circular import through generated/__init__.py
from connector_sdk_types.generated.models.custom_attribute_schema import (
    CustomAttributeSchema,
)
from connector_sdk_types.generated.models.error import Error
from connector_sdk_types.generated.models.found_account_data import FoundAccountData
from connector_sdk_types.generated.models.found_entitlement_association import (
    FoundEntitlementAssociation,
)
from connector_sdk_types.generated.models.found_entitlement_data import FoundEntitlementData
from connector_sdk_types.generated.models.probe_check import ProbeCheck
from connector_sdk_types.generated.models.probe_check_name import ProbeCheckName
from connector_sdk_types.generated.models.probe_check_source import ProbeCheckSource
from connector_sdk_types.generated.models.probe_check_status import ProbeCheckStatus
from connector_sdk_types.generated.models.probe_coverage_status import ProbeCoverageStatus
from connector_sdk_types.generated.models.probe_integration import ProbeIntegration
from connector_sdk_types.generated.models.probe_integration_request import (
    ProbeIntegrationRequest,
)
from connector_sdk_types.generated.models.probe_integration_response import ProbeIntegrationResponse
from connector_sdk_types.generated.models.probe_results import ProbeResults
from connector_sdk_types.generated.models.probe_sample_account import ProbeSampleAccount
from connector_sdk_types.generated.models.probe_sample_association import ProbeSampleAssociation
from connector_sdk_types.generated.models.probe_sample_custom_attribute import (
    ProbeSampleCustomAttribute,
)
from connector_sdk_types.generated.models.probe_sample_entitlement import ProbeSampleEntitlement
from connector_sdk_types.generated.models.probe_status import ProbeStatus

__all__ = [
    "ProbeCheckCallable",
    "ProbeSession",
    "ProbeCheckSpec",
    "ProbeErrorMapper",
    "aggregate_probe_status",
    "default_probe_error_mapper",
    "elapsed_ms",
    "probe_account_label",
    "probe_failure_message",
    "probe_sample_account",
    "probe_sample_association",
    "probe_sample_custom_attributes",
    "probe_sample_entitlement",
    "run_probe",
    "run_probe_sync",
    "skipped_probe_check",
    "unsupported_probe_check",
]

ResourceT = t.TypeVar("ResourceT")

ProbeCheckCallable: t.TypeAlias = Callable[
    [ProbeIntegration, t.Any],
    "ProbeCheck | Awaitable[ProbeCheck]",
]
"""One check, as a connector implements it.

Receives the capability's own payload, the `ProbeIntegration` and whatever `session` was passed to the driver:
a client, the integration instance itself, etc. May be async or sync.

Credentials and settings are absent:
- An SDK connector already needs a client, so it carries the request on its session
- Non-SDK integration has them on `self`
"""

ProbeErrorMapper: t.TypeAlias = Callable[[ProbeCheckName, Exception], ProbeCheck]
"""Turns an exception raised by a check into a failed check."""


class ProbeCheckSpec(BaseModel):
    """One check a connector's probe performs.

    check: Which check this describes.
    run: The implementation. `None` asks the SDK to perform the check by exercising the
        connector's standard capabilities.
    capability: The standard capability this check stands in for, e.g. `StandardCapabilityName.LIST_ACCOUNTS`.
        Reported so a caller can tie a result back to what a sync would call.
    required: Whether a failure fails the probe. A failing optional check degrades the run
        to `partial` instead.
    """

    check: ProbeCheckName = Field(description="Which check this describes.")
    run: ProbeCheckCallable | None = Field(
        default=None,
        description=(
            "The implementation. None asks the SDK to perform this check against the "
            "connector's standard capabilities."
        ),
    )
    capability: StrictStr | None = Field(
        default=None,
        description="The standard capability this check stands in for, e.g. `StandardCapabilityName.LIST_ACCOUNTS`.",
    )
    source: ProbeCheckSource = Field(
        default=ProbeCheckSource.NATIVE,
        description=(
            "Who produced this result. `NATIVE` - the connector wrote the check - is the "
            "default. The SDK marks the checks it fills in with `DEFAULT`."
        ),
    )
    required: StrictBool = Field(
        default=True,
        description=(
            "Whether a failure of this check fails the probe as a whole. A failing optional "
            "check degrades the run to `partial` instead."
        ),
    )


class ProbeSession:
    """Base for the object a probe's checks share: clients, settings, any other data

    Subclasses build their resources in `open()` and register anything that needs closing
    with `use()`. The run closes them in reverse order when it ends, including when a check
    raises. Both worlds can inherit from it, ICS connectors as an async context manager,
    synchronous integrations as a plain one.

    ```python
    class GitlabProbeSession(ProbeSession):
        async def open(self) -> None:
            request = self.require_request() # ICS only
            self.settings = get_settings(self.request, GitlabSettings)
            self.client = await self.use(GitlabClient(self.request))

    async with GitlabProbeSession(args) as session:
        return await run_probe(args.request, PROBE_CHECKS, app_id=APP_ID, session=session)
    ```

    A session is optional. A classic integration whose client already lives on `self` can
    pass `session=self` and skip this entirely.
    """

    def __init__(self, request: ProbeIntegrationRequest | None = None) -> None:
        self.request = request
        self._async_stack: AsyncExitStack | None = None
        self._stack: ExitStack | None = None

    def require_request(self) -> ProbeIntegrationRequest:
        """The request this session was built for."""
        if self.request is None:
            raise RuntimeError(
                f"{type(self).__name__} was constructed without a probe request, but needs one."
            )
        return self.request

    async def open(self) -> None:
        """Build what the checks need. Override in an async subclass."""

    def open_sync(self) -> None:
        """Build what the checks need. Override in a synchronous subclass."""

    async def use(self, resource: t.AsyncContextManager[ResourceT]) -> ResourceT:
        """Enter an async context manager and close it when the run ends."""
        if self._async_stack is None:
            raise RuntimeError("use() is only available inside `async with <session>`")
        return await self._async_stack.enter_async_context(resource)

    def use_sync(self, resource: t.ContextManager[ResourceT]) -> ResourceT:
        """Enter a context manager and close it when the run ends."""
        if self._stack is None:
            raise RuntimeError("use_sync() is only available inside `with <session>`")
        return self._stack.enter_context(resource)

    async def __aenter__(self) -> Self:
        self._async_stack = AsyncExitStack()
        await self._async_stack.__aenter__()
        try:
            await self.open()
        except BaseException:
            await self._async_stack.aclose()
            self._async_stack = None
            raise
        return self

    async def __aexit__(self, *exc_info: t.Any) -> None:
        if self._async_stack is not None:
            await self._async_stack.aclose()
            self._async_stack = None

    def __enter__(self) -> Self:
        self._stack = ExitStack()
        self._stack.__enter__()
        try:
            self.open_sync()
        except BaseException:
            self._stack.close()
            self._stack = None
            raise
        return self

    def __exit__(self, *exc_info: t.Any) -> None:
        if self._stack is not None:
            self._stack.close()
            self._stack = None


async def run_probe(
    probe: ProbeIntegration,
    specs: Sequence[ProbeCheckSpec],
    *,
    app_id: str,
    session: t.Any = None,
    on_error: ProbeErrorMapper | None = None,
    timeout_seconds: float | None = None,
) -> ProbeIntegrationResponse:
    """Run a connector's checks and assemble the report.

    The order of `specs` is the order checks run in, and a check absent from `specs` is one
    this connector cannot perform.

    Args:
        probe: The capability's payload, passed to each check.
        specs: The checks this connector performs, in order.
        app_id: The connector's app id, used when an error has to be built.
        session: Anything the checks need to run - a client or the integration itself.
        on_error: Turns a raised exception into a failed check. Defaults to a plain mapper.
            Connectors that can classify their own errors should pass their own.
        timeout_seconds: Per-check wall-clock budget. `None` means no budget, which a probe
            running while someone waits should avoid.
    """
    _require_implementations(specs)
    map_error = on_error or default_probe_error_mapper(app_id)
    started = time.monotonic()

    checks: list[ProbeCheck] = []
    for spec in specs:
        if _is_excluded(spec, probe):
            checks.append(_skipped_for(spec))
            continue

        check_started = time.monotonic()
        try:
            produced = _invoke(spec, probe, session)
            if not inspect.isawaitable(produced):
                check = t.cast(ProbeCheck, produced)
            elif timeout_seconds is None:
                check = await produced
            else:
                check = await asyncio.wait_for(produced, timeout=timeout_seconds)
        # `asyncio.TimeoutError` is not the builtin `TimeoutError` on Python 3.10, so it has
        # to be caught by name. It can also arrive from inside the check, with no budget of
        # ours to name.
        except asyncio.TimeoutError:
            check = map_error(spec.check, _timeout(spec, timeout_seconds))
        except Exception as exc:
            check = map_error(spec.check, exc)

        checks.append(_labelled(check, spec, check_started))

    return _assemble(checks, specs, started)


def run_probe_sync(
    probe: ProbeIntegration,
    specs: Sequence[ProbeCheckSpec],
    *,
    app_id: str,
    session: t.Any = None,
    on_error: ProbeErrorMapper | None = None,
) -> ProbeIntegrationResponse:
    """`run_probe` for integrations whose capabilities are synchronous.

    Note: there is no per-check time budget here, so sync implementations need
    to be mindful of their run time.

    Raises:
        TypeError: If a check returns an awaitable. Use `run_probe`.
    """
    _require_implementations(specs)
    map_error = on_error or default_probe_error_mapper(app_id)
    started = time.monotonic()

    checks: list[ProbeCheck] = []
    for spec in specs:
        if _is_excluded(spec, probe):
            checks.append(_skipped_for(spec))
            continue

        check_started = time.monotonic()
        try:
            produced = _invoke(spec, probe, session)
            if inspect.isawaitable(produced):
                t.cast(Awaitable[ProbeCheck], produced).close()  # type: ignore[attr-defined]
                raise TypeError(
                    f"Probe check {spec.check.value} is asynchronous. Use `run_probe` rather "
                    "than `run_probe_sync`."
                )
            check = t.cast(ProbeCheck, produced)
        except TypeError:
            raise
        except Exception as exc:
            check = map_error(spec.check, exc)

        checks.append(_labelled(check, spec, check_started))

    return _assemble(checks, specs, started)


def _require_implementations(specs: Sequence[ProbeCheckSpec]) -> None:
    """Fail before running anything, rather than burying it in a check result."""
    missing = [spec.check.value for spec in specs if spec.run is None]
    if missing:
        raise ValueError(f"Probe checks with no implementation: {', '.join(missing)}.")


def _invoke(
    spec: ProbeCheckSpec, probe: ProbeIntegration, session: t.Any
) -> ProbeCheck | Awaitable[ProbeCheck]:
    run = t.cast(ProbeCheckCallable, spec.run)
    return run(probe, session)


def _is_excluded(spec: ProbeCheckSpec, probe: ProbeIntegration) -> bool:
    """Whether the caller asked for a subset that leaves this check out.

    An explicit empty list means "run nothing"; omitting `checks` means "run everything".
    """
    return probe.checks is not None and spec.check not in set(probe.checks)


def _skipped_for(spec: ProbeCheckSpec) -> ProbeCheck:
    return skipped_probe_check(
        spec.check,
        source=spec.source,
        capability=spec.capability,
        message="Not requested in this run.",
    )


def _timeout(spec: ProbeCheckSpec, timeout_seconds: float | None) -> TimeoutError:
    overran = f"longer than {timeout_seconds:g}s" if timeout_seconds is not None else "too long"
    return TimeoutError(f"Probing {spec.check.value} took {overran} and was stopped.")


def _labelled(check: ProbeCheck, spec: ProbeCheckSpec, started: float) -> ProbeCheck:
    """A check describes what it found. The driver owns how it is labelled."""
    check.check = spec.check
    check.source = spec.source
    if check.capability is None:
        check.capability = spec.capability
    if check.duration_ms is None:
        check.duration_ms = elapsed_ms(started)
    return check


def _assemble(
    checks: list[ProbeCheck], specs: Sequence[ProbeCheckSpec], started: float
) -> ProbeIntegrationResponse:
    described = {spec.check for spec in specs}
    for check in ProbeCheckName:
        if check not in described:
            checks.append(
                unsupported_probe_check(
                    check,
                    source=ProbeCheckSource.NATIVE,
                    message="This connector does not probe this check.",
                )
            )

    return ProbeIntegrationResponse(
        response=ProbeResults(
            status=aggregate_probe_status(
                checks,
                optional_checks=[spec.check for spec in specs if not spec.required],
            ),
            checks=checks,
            duration_ms=elapsed_ms(started),
        )
    )


def default_probe_error_mapper(app_id: str) -> ProbeErrorMapper:
    """Map an exception to a failed check without any connector-specific knowledge."""
    from connector_sdk_types.errors.codes import ConnectorErrorCode
    from connector_sdk_types.errors.metadata import build_metadata

    def map_error(check: ProbeCheckName, exc: Exception) -> ProbeCheck:
        code = (
            ConnectorErrorCode.REQUEST_TIMEOUT
            if isinstance(exc, TimeoutError)
            else ConnectorErrorCode.INTERNAL_ERROR
        )
        error = Error(
            message=str(exc),
            error_code=code,
            app_id=app_id,
            raised_by=type(exc).__name__,
            error_metadata=build_metadata(code),
        )
        return ProbeCheck(
            check=check,
            status=ProbeCheckStatus.FAILED,
            source=ProbeCheckSource.NATIVE,
            observed_count=0,
            samples=[],
            message=probe_failure_message(error),
            error=error,
        )

    return map_error


def skipped_probe_check(
    check: ProbeCheckName,
    *,
    source: ProbeCheckSource,
    message: str,
    capability: str | None = None,
) -> ProbeCheck:
    """A check that was not attempted: excluded by the request, or missing a prerequisite."""
    return ProbeCheck(
        check=check,
        status=ProbeCheckStatus.SKIPPED,
        source=source,
        capability=capability,
        observed_count=0,
        samples=[],
        message=message,
    )


def unsupported_probe_check(
    check: ProbeCheckName,
    *,
    source: ProbeCheckSource,
    message: str,
    capability: str | None = None,
) -> ProbeCheck:
    """A check this connector cannot perform."""
    return ProbeCheck(
        check=check,
        status=ProbeCheckStatus.UNSUPPORTED,
        source=source,
        capability=capability,
        observed_count=0,
        samples=[],
        message=message,
    )


def aggregate_probe_status(
    checks: Sequence[ProbeCheck],
    *,
    optional_checks: Collection[ProbeCheckName] = (),
) -> ProbeStatus:
    """Reduce checks to the outcome of the run.

    - a failed required check makes the run `failed`
    - a failed optional check, or a passing check that left something it declared
      unaccounted for - an entitlement type with no entitlement, a custom attribute no
      account populated - makes it `partial`
    - a run where nothing was attempted and something was `unsupported` is `failed`: it
      proved nothing, so it cannot report otherwise
    - `skipped` never fails a run, and `unsupported` beside a check that ran does not either
    """
    outcomes = {check.status for check in checks}
    if ProbeCheckStatus.UNSUPPORTED in outcomes and not (
        outcomes & {ProbeCheckStatus.PASSED, ProbeCheckStatus.FAILED}
    ):
        return ProbeStatus.FAILED

    status = ProbeStatus.PASSED
    for check in checks:
        if check.status is ProbeCheckStatus.FAILED:
            if check.check in optional_checks:
                status = ProbeStatus.PARTIAL
                continue
            return ProbeStatus.FAILED

        # Coverage is a lesser requirement than fetching the records at all, every
        # entitlement type, every declared custom attribute, so a gap degrades the run
        # rather than failing it.
        covered = [result.status for result in check.entitlement_types or []]
        covered += [result.status for result in check.custom_attributes or []]
        if any(reported is not ProbeCoverageStatus.FOUND for reported in covered):
            status = ProbeStatus.PARTIAL
    return status


def probe_sample_account(
    account: FoundAccountData,
    *,
    custom_attributes: Sequence[str] | None = None,
    schemas: Sequence[CustomAttributeSchema] | None = None,
) -> ProbeSampleAccount:
    """Reduce an account to identifying fields, plus the attributes that were asked for.

    Args:
        account: The account a check fetched.
        custom_attributes: The names from `ProbeIntegration.custom_attributes`. Every one
            appears on the sample, valued when this account has a value, so a consumer can
            tell "the connector cannot see this attribute" from "this account has none".
        schemas: The connector's attribute schema, when it has one, used to type what it
            reports.
    """
    return ProbeSampleAccount(
        integration_specific_id=account.integration_specific_id,
        email=account.email,
        username=account.username,
        user_status=account.user_status,
        custom_attributes=(
            probe_sample_custom_attributes(
                custom_attributes, values=account.custom_attributes, schemas=schemas
            )
            if custom_attributes
            else None
        ),
    )


def probe_sample_custom_attributes(
    names: Sequence[str],
    *,
    values: Mapping[str, str] | None = None,
    schemas: Sequence[CustomAttributeSchema] | None = None,
) -> list[ProbeSampleCustomAttribute]:
    """
    One entry per requested attribute, valued where the record has a value.
    A requested attribute with no value is kept rather than dropped.
    """
    by_name = {schema.name: schema for schema in schemas or []}
    resolved = values or {}
    return [
        ProbeSampleCustomAttribute(
            name=name,
            value=resolved.get(name) or None,
            customized_type=by_name[name].customized_type if name in by_name else None,
            attribute_type=by_name[name].attribute_type if name in by_name else None,
        )
        for name in names
    ]


def probe_sample_entitlement(entitlement: FoundEntitlementData) -> ProbeSampleEntitlement:
    """Reduce an entitlement to identifying fields."""
    return ProbeSampleEntitlement(
        integration_specific_id=entitlement.integration_specific_id,
        integration_specific_resource_id=entitlement.integration_specific_resource_id,
        entitlement_type=entitlement.entitlement_type,
        label=entitlement.label,
    )


def probe_sample_association(
    association: FoundEntitlementAssociation,
    *,
    linked_to_sampled_account: bool,
) -> ProbeSampleAssociation:
    """Reduce an association to identifying fields.

    Pass `linked_to_sampled_account=True` only when the association demonstrably belongs to
    an account the probe fetched.
    """
    return ProbeSampleAssociation(
        account_id=association.account_id,
        integration_specific_entitlement_id=association.integration_specific_entitlement_id,
        integration_specific_resource_id=association.integration_specific_resource_id,
        linked_to_sampled_account=linked_to_sampled_account,
    )


def probe_account_label(account: FoundAccountData) -> str:
    """The most recognizable identifier an account carries, for check messages."""
    return account.email or account.username or account.integration_specific_id


def probe_failure_message(error: Error) -> str:
    """What to show for a failed check: the remediation hint, else the error's message."""
    hint = error.error_metadata.hint if error.error_metadata else None
    return hint or error.message


def elapsed_ms(started: float) -> int:
    """Milliseconds since a `time.monotonic()` reading."""
    return int((time.monotonic() - started) * 1000)
