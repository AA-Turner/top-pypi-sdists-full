"""Test cases for the probe driver and helpers in `connector_sdk_types.oai.probe`."""

import asyncio

import pytest
from connector_sdk_types.generated import (
    AccountStatus,
    CustomAttributeCustomizedType,
    CustomAttributeSchema,
    CustomAttributeType,
    FoundAccountData,
    FoundEntitlementAssociation,
    FoundEntitlementData,
    ProbeCheck,
    ProbeCheckName,
    ProbeCheckSource,
    ProbeCheckStatus,
    ProbeCoverageStatus,
    ProbeCustomAttributeResult,
    ProbeEntitlementTypeResult,
    ProbeIntegration,
    ProbeIntegrationRequest,
    ProbeSampleAccount,
    ProbeStatus,
)
from connector_sdk_types.oai.probe import (
    ProbeCheckSpec,
    ProbeSession,
    aggregate_probe_status,
    probe_account_label,
    probe_sample_account,
    probe_sample_association,
    probe_sample_entitlement,
    run_probe,
    run_probe_sync,
    skipped_probe_check,
    unsupported_probe_check,
)

APP_ID = "probe_types_test"
_SAMPLE = ProbeSampleAccount(integration_specific_id="user-1")


def _probe(checks: list[ProbeCheckName] | None = None) -> ProbeIntegration:
    return ProbeIntegration(checks=checks)


def _passed(check: ProbeCheckName = ProbeCheckName.ACCOUNTS, count: int = 1) -> ProbeCheck:
    return ProbeCheck(
        check=check,
        status=ProbeCheckStatus.PASSED,
        source=ProbeCheckSource.NATIVE,
        observed_count=count,
        samples=[_SAMPLE] * count,
    )


def _check(
    check: ProbeCheckName = ProbeCheckName.ACCOUNTS,
    status: ProbeCheckStatus = ProbeCheckStatus.PASSED,
    entitlement_types: list[ProbeEntitlementTypeResult] | None = None,
) -> ProbeCheck:
    return ProbeCheck(
        check=check,
        status=status,
        source=ProbeCheckSource.NATIVE,
        observed_count=1,
        samples=[_SAMPLE],
        entitlement_types=entitlement_types,
    )


def _by_check(results, check: ProbeCheckName) -> ProbeCheck:
    return next(result for result in results.checks if result.check is check)


# run_probe


async def test_run_probe_reports_every_check():
    """A caller gets a complete picture whatever it asked for: what ran, what was skipped,
    and what this connector cannot do at all."""

    async def accounts(probe, session) -> ProbeCheck:
        return _passed()

    results = (
        await run_probe(
            _probe(),
            [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts)],
            app_id=APP_ID,
        )
    ).response

    assert {result.check for result in results.checks} == set(ProbeCheckName)
    assert _by_check(results, ProbeCheckName.ACCOUNTS).status is ProbeCheckStatus.PASSED
    for absent in set(ProbeCheckName) - {ProbeCheckName.ACCOUNTS}:
        assert _by_check(results, absent).status is ProbeCheckStatus.UNSUPPORTED
    assert results.status is ProbeStatus.PASSED
    assert results.duration_ms is not None


async def test_run_probe_runs_checks_in_spec_order():
    order: list[ProbeCheckName] = []

    async def record(check: ProbeCheckName):
        async def run(probe, session) -> ProbeCheck:
            order.append(check)
            return _passed(check)

        return run

    specs = [
        ProbeCheckSpec(
            check=ProbeCheckName.ENTITLEMENTS, run=await record(ProbeCheckName.ENTITLEMENTS)
        ),
        ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=await record(ProbeCheckName.ACCOUNTS)),
    ]
    await run_probe(_probe(), specs, app_id=APP_ID)

    assert order == [ProbeCheckName.ENTITLEMENTS, ProbeCheckName.ACCOUNTS]


async def test_run_probe_honours_the_checks_filter():
    ran: list[ProbeCheckName] = []

    async def accounts(probe, session) -> ProbeCheck:
        ran.append(ProbeCheckName.ACCOUNTS)
        return _passed()

    async def entitlements(probe, session) -> ProbeCheck:
        ran.append(ProbeCheckName.ENTITLEMENTS)
        return _passed(ProbeCheckName.ENTITLEMENTS)

    results = (
        await run_probe(
            _probe(checks=[ProbeCheckName.ACCOUNTS]),
            [
                ProbeCheckSpec(
                    check=ProbeCheckName.ACCOUNTS, run=accounts, capability="list_accounts"
                ),
                ProbeCheckSpec(check=ProbeCheckName.ENTITLEMENTS, run=entitlements),
            ],
            app_id=APP_ID,
        )
    ).response

    assert ran == [ProbeCheckName.ACCOUNTS]
    skipped = _by_check(results, ProbeCheckName.ENTITLEMENTS)
    assert skipped.status is ProbeCheckStatus.SKIPPED
    assert skipped.duration_ms is None


async def test_empty_checks_list_runs_nothing():
    """An explicit empty list is not the same as omitting the field."""

    async def accounts(probe, session) -> ProbeCheck:
        raise AssertionError("should not run")

    results = (
        await run_probe(
            _probe(checks=[]),
            [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts)],
            app_id=APP_ID,
        )
    ).response

    assert _by_check(results, ProbeCheckName.ACCOUNTS).status is ProbeCheckStatus.SKIPPED


async def test_run_probe_passes_the_session_and_request_through():
    session = {"client": "mine"}
    seen: dict[str, object] = {}

    async def accounts(probe, given) -> ProbeCheck:
        seen["probe"] = probe
        seen["session"] = given
        return _passed()

    payload = _probe()
    await run_probe(
        payload,
        [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts)],
        app_id=APP_ID,
        session=session,
    )

    assert seen["probe"] is payload
    assert seen["session"] is session


async def test_run_probe_stamps_identity_and_duration():
    async def accounts(probe, session) -> ProbeCheck:
        # Deliberately mislabelled: a check describes findings, the driver owns labels.
        return ProbeCheck(
            check=ProbeCheckName.ENTITLEMENTS,
            status=ProbeCheckStatus.PASSED,
            source=ProbeCheckSource.DEFAULT,
            observed_count=3,
            samples=[_SAMPLE] * 3,
        )

    results = (
        await run_probe(
            _probe(),
            [
                ProbeCheckSpec(
                    check=ProbeCheckName.ACCOUNTS, run=accounts, capability="list_accounts"
                )
            ],
            app_id=APP_ID,
        )
    ).response

    check = _by_check(results, ProbeCheckName.ACCOUNTS)
    assert check.source is ProbeCheckSource.NATIVE
    assert check.capability == "list_accounts"
    assert check.observed_count == 3
    assert check.duration_ms is not None


async def test_a_check_may_name_its_own_capability():
    async def accounts(probe, session) -> ProbeCheck:
        check = _passed()
        check.capability = "list_updated_accounts"
        return check

    results = (
        await run_probe(
            _probe(),
            [
                ProbeCheckSpec(
                    check=ProbeCheckName.ACCOUNTS, run=accounts, capability="list_accounts"
                )
            ],
            app_id=APP_ID,
        )
    ).response

    assert _by_check(results, ProbeCheckName.ACCOUNTS).capability == "list_updated_accounts"


async def test_a_raising_check_fails_only_itself():
    async def accounts(probe, session) -> ProbeCheck:
        raise ValueError("the tenant exploded")

    async def entitlements(probe, session) -> ProbeCheck:
        return _passed(ProbeCheckName.ENTITLEMENTS)

    results = (
        await run_probe(
            _probe(),
            [
                ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts),
                ProbeCheckSpec(check=ProbeCheckName.ENTITLEMENTS, run=entitlements),
            ],
            app_id=APP_ID,
        )
    ).response

    failed = _by_check(results, ProbeCheckName.ACCOUNTS)
    assert failed.status is ProbeCheckStatus.FAILED
    assert failed.error is not None
    assert failed.error.app_id == APP_ID
    assert "exploded" in failed.error.message
    assert _by_check(results, ProbeCheckName.ENTITLEMENTS).status is ProbeCheckStatus.PASSED
    assert results.status is ProbeStatus.FAILED


async def test_a_check_may_overrun_its_budget():
    async def accounts(probe, session) -> ProbeCheck:
        await asyncio.sleep(0.2)
        raise AssertionError("should have been cancelled")

    results = (
        await run_probe(
            _probe(),
            [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts)],
            app_id=APP_ID,
            timeout_seconds=0.01,
        )
    ).response

    check = _by_check(results, ProbeCheckName.ACCOUNTS)
    assert check.status is ProbeCheckStatus.FAILED
    assert check.error is not None
    assert check.error.error_code == "request_timeout"
    assert "0.01s" in (check.message or "")


async def test_a_timeout_without_a_budget_is_still_a_failed_check():
    async def accounts(probe, session) -> ProbeCheck:
        raise asyncio.TimeoutError

    results = (
        await run_probe(
            _probe(),
            [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts)],
            app_id=APP_ID,
        )
    ).response

    check = _by_check(results, ProbeCheckName.ACCOUNTS)
    assert check.status is ProbeCheckStatus.FAILED
    assert "too long" in (check.message or "")


async def test_a_sync_check_is_accepted():
    def accounts(probe, session) -> ProbeCheck:
        return _passed()

    results = (
        await run_probe(
            _probe(),
            [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts)],
            app_id=APP_ID,
            timeout_seconds=5,
        )
    ).response

    assert _by_check(results, ProbeCheckName.ACCOUNTS).status is ProbeCheckStatus.PASSED


async def test_a_custom_error_mapper_is_used():
    async def accounts(probe, session) -> ProbeCheck:
        raise ValueError("boom")

    def on_error(check: ProbeCheckName, exc: Exception) -> ProbeCheck:
        return ProbeCheck(
            check=check,
            status=ProbeCheckStatus.FAILED,
            source=ProbeCheckSource.NATIVE,
            observed_count=0,
            samples=[],
            message="mapped by the connector",
        )

    results = (
        await run_probe(
            _probe(),
            [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts)],
            app_id=APP_ID,
            on_error=on_error,
        )
    ).response

    assert _by_check(results, ProbeCheckName.ACCOUNTS).message == "mapped by the connector"


async def test_an_optional_check_only_degrades_the_run():
    async def accounts(probe, session) -> ProbeCheck:
        raise ValueError("boom")

    results = (
        await run_probe(
            _probe(),
            [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts, required=False)],
            app_id=APP_ID,
        )
    ).response

    assert results.status is ProbeStatus.PARTIAL


async def test_a_spec_without_an_implementation_is_a_programming_error():
    """Only ProbeSettings may leave `run` unset, for the SDK to fill in."""
    with pytest.raises(ValueError, match="no implementation"):
        await run_probe(
            _probe(),
            [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS)],
            app_id=APP_ID,
        )


# run_probe_sync, for integrations whose capabilities are synchronous (classic and maybe some ICS ones)


def test_sync_driver_reports_every_check():
    def accounts(probe, session) -> ProbeCheck:
        return _passed()

    results = run_probe_sync(
        _probe(),
        [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts, capability="list_accounts")],
        app_id=APP_ID,
    ).response

    assert {result.check for result in results.checks} == set(ProbeCheckName)
    check = _by_check(results, ProbeCheckName.ACCOUNTS)
    assert check.status is ProbeCheckStatus.PASSED
    assert check.capability == "list_accounts"
    assert check.duration_ms is not None
    assert results.status is ProbeStatus.PASSED


def test_sync_driver_passes_the_session_through():
    """Classic integrations hand in `self`, so this is their whole client and auth."""
    session = object()
    seen = []

    def accounts(probe, given) -> ProbeCheck:
        seen.append(given)
        return _passed()

    run_probe_sync(
        _probe(),
        [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts)],
        app_id=APP_ID,
        session=session,
    )

    assert seen == [session]


def test_sync_driver_honours_the_checks_filter():
    def accounts(probe, session) -> ProbeCheck:
        raise AssertionError("should not run")

    results = run_probe_sync(
        _probe(checks=[ProbeCheckName.ENTITLEMENTS]),
        [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts)],
        app_id=APP_ID,
    ).response

    assert _by_check(results, ProbeCheckName.ACCOUNTS).status is ProbeCheckStatus.SKIPPED


def test_sync_driver_traps_a_raising_check():
    def accounts(probe, session) -> ProbeCheck:
        raise PermissionError("Directory.Read.All is not granted")

    results = run_probe_sync(
        _probe(),
        [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts)],
        app_id=APP_ID,
    ).response

    check = _by_check(results, ProbeCheckName.ACCOUNTS)
    assert check.status is ProbeCheckStatus.FAILED
    assert check.error is not None
    assert "Directory.Read.All" in check.error.message


def test_sync_driver_rejects_an_async_check():
    """Silently never awaiting it would report a passing check that never ran."""

    async def accounts(probe, session) -> ProbeCheck:
        return _passed()

    with pytest.raises(TypeError, match="asynchronous"):
        run_probe_sync(
            _probe(),
            [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=accounts)],
            app_id=APP_ID,
        )


def test_sync_driver_requires_implementations():
    with pytest.raises(ValueError, match="no implementation"):
        run_probe_sync(_probe(), [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS)], app_id=APP_ID)


# The sample union


def test_samples_survive_a_round_trip_as_their_own_kinds():
    """Samples are a union discriminated by `kind`, but the generated models type it as a
    plain string, so pydantic tells the variants apart by their fields. A new sample type
    whose required fields are a subset of another's would break that silently, this test is
    what makes it fail loudly instead.
    """
    check = ProbeCheck(
        check=ProbeCheckName.ENTITLEMENTS,
        status=ProbeCheckStatus.PASSED,
        source=ProbeCheckSource.NATIVE,
        observed_count=3,
        samples=[
            probe_sample_account(FoundAccountData(integration_specific_id="user-1")),
            probe_sample_entitlement(
                FoundEntitlementData(
                    entitlement_type="role",
                    integration_specific_id="admin",
                    integration_specific_resource_id="",
                    label="Admin",
                )
            ),
            probe_sample_association(
                FoundEntitlementAssociation(
                    account_id="user-1",
                    integration_specific_entitlement_id="admin",
                    integration_specific_resource_id="",
                ),
                linked_to_sampled_account=True,
            ),
        ],
    )

    restored = ProbeCheck.model_validate_json(check.model_dump_json())

    assert [type(sample).__name__ for sample in restored.samples] == [
        "ProbeSampleAccount",
        "ProbeSampleEntitlement",
        "ProbeSampleAssociation",
    ]
    assert [sample.kind for sample in restored.samples] == [
        "account",
        "entitlement",
        "association",
    ]


def test_generated_from_dict_helpers_accept_samples():
    """`from_dict` / `from_json` are generated before the annotation is rewritten to a real
    union, so they used to rebuild the discarded `ProbeSample` wrapper and raise on every
    payload carrying samples. The codegen now passes those values through untouched.
    """
    check = ProbeCheck(
        check=ProbeCheckName.ACCOUNTS,
        status=ProbeCheckStatus.PASSED,
        source=ProbeCheckSource.NATIVE,
        observed_count=1,
        samples=[probe_sample_account(FoundAccountData(integration_specific_id="user-1"))],
    )
    payload = check.model_dump(mode="json")

    for restored in (ProbeCheck.from_dict(payload), ProbeCheck.from_json(check.model_dump_json())):
        assert restored is not None
        assert [type(sample).__name__ for sample in restored.samples] == ["ProbeSampleAccount"]


# aggregate_probe_status


def test_all_passing_checks_pass_the_run():
    assert aggregate_probe_status([_check(), _check(ProbeCheckName.ENTITLEMENTS)]) is (
        ProbeStatus.PASSED
    )


def test_failed_required_check_fails_the_run():
    assert aggregate_probe_status([_check(status=ProbeCheckStatus.FAILED)]) is ProbeStatus.FAILED


def test_a_required_failure_outweighs_an_optional_one():
    checks = [
        _check(ProbeCheckName.ENTITLEMENT_ASSOCIATIONS, ProbeCheckStatus.FAILED),
        _check(ProbeCheckName.ACCOUNTS, ProbeCheckStatus.FAILED),
    ]
    assert (
        aggregate_probe_status(checks, optional_checks=[ProbeCheckName.ENTITLEMENT_ASSOCIATIONS])
        is ProbeStatus.FAILED
    )


def test_skipped_never_fails_a_run():
    """What the caller left out is not a problem with the connector."""
    assert aggregate_probe_status([_check(status=ProbeCheckStatus.SKIPPED)]) is ProbeStatus.PASSED


def test_a_run_that_proved_nothing_fails():
    """Every check unsupported means nothing was shown to be reachable. Reporting that as
    `passed` would tell a customer their credentials are fine on no evidence at all."""
    unsupported = [
        _check(check=name, status=ProbeCheckStatus.UNSUPPORTED) for name in ProbeCheckName
    ]
    assert aggregate_probe_status(unsupported) is ProbeStatus.FAILED


def test_unsupported_alongside_something_proven_does_not_fail_the_run():
    checks = [
        _check(check=ProbeCheckName.ACCOUNTS, status=ProbeCheckStatus.PASSED),
        _check(check=ProbeCheckName.ENTITLEMENTS, status=ProbeCheckStatus.UNSUPPORTED),
    ]
    assert aggregate_probe_status(checks) is ProbeStatus.PASSED


def test_unsupported_with_only_skipped_beside_it_fails():
    """The caller asked for one check and the connector cannot perform it."""
    checks = [
        _check(check=ProbeCheckName.ACCOUNTS, status=ProbeCheckStatus.UNSUPPORTED),
        _check(check=ProbeCheckName.ENTITLEMENTS, status=ProbeCheckStatus.SKIPPED),
    ]
    assert aggregate_probe_status(checks) is ProbeStatus.FAILED


def test_a_failed_optional_check_still_only_degrades_beside_unsupported_ones():
    """`required=False` is the connector's call and outranks the proved-nothing rule: a check
    that ran and failed is a different report from one that was never attempted."""
    checks = [
        _check(check=ProbeCheckName.ACCOUNTS, status=ProbeCheckStatus.FAILED),
        _check(check=ProbeCheckName.ENTITLEMENTS, status=ProbeCheckStatus.UNSUPPORTED),
    ]
    assert (
        aggregate_probe_status(checks, optional_checks=[ProbeCheckName.ACCOUNTS])
        is ProbeStatus.PARTIAL
    )


def test_incomplete_entitlement_type_coverage_degrades_a_passing_check():
    checks = [
        _check(
            ProbeCheckName.ENTITLEMENTS,
            entitlement_types=[
                ProbeEntitlementTypeResult(
                    entitlement_type="role", status=ProbeCoverageStatus.FOUND
                ),
                ProbeEntitlementTypeResult(
                    entitlement_type="license", status=ProbeCoverageStatus.NOT_FOUND
                ),
            ],
        )
    ]
    assert aggregate_probe_status(checks) is ProbeStatus.PARTIAL


def test_unpopulated_custom_attribute_degrades_a_passing_check():
    """A declared attribute nothing carries a value for means attributes would sync empty."""
    checks = [
        ProbeCheck(
            check=ProbeCheckName.ACCOUNTS,
            status=ProbeCheckStatus.PASSED,
            source=ProbeCheckSource.DEFAULT,
            observed_count=1,
            samples=[_SAMPLE],
            custom_attributes=[
                ProbeCustomAttributeResult(name="department", status=ProbeCoverageStatus.FOUND),
                ProbeCustomAttributeResult(
                    name="cost_center", status=ProbeCoverageStatus.NOT_FOUND
                ),
            ],
        )
    ]
    assert aggregate_probe_status(checks) is ProbeStatus.PARTIAL


def test_no_checks_passes():
    """A run that asked for nothing did not fail."""
    assert aggregate_probe_status([]) is ProbeStatus.PASSED


# Builders


def test_skipped_check_shape():
    check = skipped_probe_check(
        ProbeCheckName.ENTITLEMENTS, source=ProbeCheckSource.NATIVE, message="Not requested."
    )

    assert check.status is ProbeCheckStatus.SKIPPED
    assert check.observed_count == 0


def test_unsupported_check_shape():
    check = unsupported_probe_check(
        ProbeCheckName.ENTITLEMENT_ASSOCIATIONS,
        source=ProbeCheckSource.NATIVE,
        message="Not offered by this connector.",
        capability="find_entitlement_associations",
    )

    assert check.status is ProbeCheckStatus.UNSUPPORTED
    assert check.capability == "find_entitlement_associations"


ACCOUNT_WITH_ATTRIBUTES = FoundAccountData(
    integration_specific_id="user-1",
    email="jane@acme.com",
    username="jane",
    user_status=AccountStatus.ACTIVE,
    custom_attributes={"department": "Engineering", "title": "Staff"},
    extra_data={"internal_note": "not for display"},
)


def test_account_sample_carries_identifying_fields_only():
    """No attributes were asked for, so none are reported - and never `extra_data`."""
    assert probe_sample_account(ACCOUNT_WITH_ATTRIBUTES).model_dump() == {
        "kind": "account",
        "integration_specific_id": "user-1",
        "email": "jane@acme.com",
        "username": "jane",
        "user_status": AccountStatus.ACTIVE,
        "custom_attributes": None,
    }


def test_account_sample_reports_requested_attributes_with_values():
    sample = probe_sample_account(
        ACCOUNT_WITH_ATTRIBUTES, custom_attributes=["department", "cost_center"]
    )

    assert sample.custom_attributes is not None
    assert [(a.name, a.value) for a in sample.custom_attributes] == [
        ("department", "Engineering"),
        # Requested but unset: kept, so a consumer can see the attribute exists and is empty.
        ("cost_center", None),
    ]
    # Not requested, so not reported, even though the account carries it.
    assert "title" not in [a.name for a in sample.custom_attributes]


def test_attribute_samples_are_typed_when_a_schema_is_available():
    schemas = [
        CustomAttributeSchema(
            customized_type=CustomAttributeCustomizedType.ACCOUNT,
            name="department",
            attribute_type=CustomAttributeType.STRING,
        )
    ]
    sample = probe_sample_account(
        ACCOUNT_WITH_ATTRIBUTES, custom_attributes=["department", "cost_center"], schemas=schemas
    )

    assert sample.custom_attributes is not None
    typed, untyped = sample.custom_attributes
    assert typed.attribute_type is CustomAttributeType.STRING
    assert typed.customized_type is CustomAttributeCustomizedType.ACCOUNT
    # No schema entry, so the type is simply unknown rather than guessed.
    assert untyped.attribute_type is None


def test_entitlement_sample_carries_identifying_fields_only():
    entitlement = FoundEntitlementData(
        entitlement_type="role",
        integration_specific_id="admin",
        integration_specific_resource_id="org-1",
        label="Admin",
        extra_data={"internal_note": "not for display"},
        custom_attributes={"tier": "gold"},
    )

    assert probe_sample_entitlement(entitlement).model_dump() == {
        "kind": "entitlement",
        "integration_specific_id": "admin",
        "integration_specific_resource_id": "org-1",
        "entitlement_type": "role",
        "label": "Admin",
    }


@pytest.mark.parametrize("linked", [True, False])
def test_association_sample_records_linkage(linked: bool):
    association = FoundEntitlementAssociation(
        account_id="user-1",
        integration_specific_entitlement_id="admin",
        integration_specific_resource_id="",
    )
    sample = probe_sample_association(association, linked_to_sampled_account=linked)

    assert sample.account_id == "user-1"
    assert sample.linked_to_sampled_account is linked


@pytest.mark.parametrize(
    ("account", "expected"),
    [
        (FoundAccountData(integration_specific_id="1", email="a@b.c", username="ab"), "a@b.c"),
        (FoundAccountData(integration_specific_id="1", username="ab"), "ab"),
        (FoundAccountData(integration_specific_id="1"), "1"),
    ],
)
def test_account_label_prefers_the_most_recognizable_identifier(
    account: FoundAccountData, expected: str
):
    assert probe_account_label(account) == expected


# ProbeSession, the base both the SDK and classic integrations build their sessions on


class _Resource:
    """A context manager that records whether it was closed."""

    def __init__(self) -> None:
        self.closed = False

    async def __aenter__(self) -> "_Resource":
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        self.closed = True

    def __enter__(self) -> "_Resource":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.closed = True


class _AsyncSession(ProbeSession):
    """Opens one resource, the shape a connector's session takes."""

    def __init__(self, request=None, *, fail: bool = False) -> None:
        super().__init__(request)
        self.fail = fail
        self.resource = _Resource()

    async def open(self) -> None:
        await self.use(self.resource)
        if self.fail:
            raise RuntimeError("client could not be built")


class _SyncSession(ProbeSession):
    def __init__(self, request=None, *, fail: bool = False) -> None:
        super().__init__(request)
        self.fail = fail
        self.resource = _Resource()

    def open_sync(self) -> None:
        self.use_sync(self.resource)
        if self.fail:
            raise RuntimeError("client could not be built")


async def test_session_closes_what_it_opened():
    async with _AsyncSession() as session:
        assert session.resource.closed is False
    assert session.resource.closed is True


async def test_session_closes_what_it_opened_when_a_check_raises():
    """A failing check must not leak the client: probes run while a customer waits."""
    session = _AsyncSession()
    with pytest.raises(ValueError):
        async with session:
            raise ValueError("a check blew up")
    assert session.resource.closed is True


async def test_session_closes_what_it_opened_when_open_fails():
    """Half-built is still built: whatever `open()` managed to register is closed."""
    session = _AsyncSession(fail=True)
    with pytest.raises(RuntimeError, match="client could not be built"):
        async with session:
            pass
    assert session.resource.closed is True


async def test_session_can_be_reopened_after_a_failed_open():
    """The failed attempt leaves no stack behind, so a retry is not poisoned by it."""
    session = _AsyncSession(fail=True)
    with pytest.raises(RuntimeError):
        async with session:
            pass

    session.fail = False
    session.resource = _Resource()
    async with session:
        assert session.resource.closed is False
    assert session.resource.closed is True


def test_sync_session_closes_what_it_opened():
    with _SyncSession() as session:
        assert session.resource.closed is False
    assert session.resource.closed is True


def test_sync_session_closes_what_it_opened_when_open_fails():
    session = _SyncSession(fail=True)
    with pytest.raises(RuntimeError, match="client could not be built"):
        with session:
            pass
    assert session.resource.closed is True


async def test_use_outside_the_context_manager_is_a_programming_error():
    """`use()` only means something once there is a stack to close things onto."""
    session = ProbeSession()
    with pytest.raises(RuntimeError, match="only available inside"):
        await session.use(_Resource())


def test_use_sync_outside_the_context_manager_is_a_programming_error():
    session = ProbeSession()
    with pytest.raises(RuntimeError, match="only available inside"):
        session.use_sync(_Resource())


def test_require_request_returns_the_request_it_was_built_for():
    request = ProbeIntegrationRequest(request=_probe())
    assert ProbeSession(request).require_request() is request


def test_require_request_names_the_session_that_lacks_one():
    """A session built without a request cannot read settings - say which class it was."""
    with pytest.raises(RuntimeError, match="_AsyncSession was constructed without"):
        _AsyncSession().require_request()


async def test_base_session_needs_no_overrides():
    """`session=self` is supported, so the base must be usable as-is."""
    async with ProbeSession() as session:
        assert session.request is None
    with ProbeSession() as session:
        assert session.request is None


# Labelling: the driver stamps what it owns, and leaves what the check reported


async def test_a_check_keeps_the_duration_it_measured_itself():
    """A check that times its own work - a classic integration wrapping a blocking call -
    keeps that number rather than having the driver's wall-clock overwrite it."""

    async def run(probe, session):
        check = _passed()
        check.duration_ms = 7
        return check

    response = await run_probe(
        _probe(),
        [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=run)],
        app_id=APP_ID,
    )

    assert _by_check(response.response, ProbeCheckName.ACCOUNTS).duration_ms == 7


async def test_a_check_that_did_not_time_itself_is_timed_by_the_driver():
    response = await run_probe(
        _probe(),
        [ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=lambda probe, session: _passed())],
        app_id=APP_ID,
    )

    assert _by_check(response.response, ProbeCheckName.ACCOUNTS).duration_ms is not None
