"""Tests for the migration Job API (no network; httpx client is stubbed).

Aligned with platform contract 0.2.0. The wire contract is asymmetric —
request bodies and query parameters are snake_case while responses are
camelCase — so these tests assert what is actually put on the wire, not just
what comes back.
"""

import pytest

from novita_sandbox import (
    CancelTooLateError,
    Job,
    JobCancelledError,
    JobFailedError,
    JobPage,
    JobStatus,
    JobType,
    MigrationConflictError,
    MigrationItemStatus,
    MigrationNotSupportedError,
    MigrationStatus,
    ResourceAlreadyMigratingError,
    SharedDependencyError,
    TemplateAliasConflictError,
)
from novita_sandbox.core.exceptions import (
    AuthenticationException,
    InvalidArgumentException,
    NotFoundException,
    RateLimitException,
    SandboxException,
    TimeoutException,
)

JOB_ID = "3f2504e0-4f89-11d3-9a0c-0305e82c3301"


class _FakeResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload
        self.content = b"{}"

    def json(self):
        return self._payload


class _FakeHttpx:
    """Returns queued responses so polling can be exercised.

    When the queue runs dry the last response repeats, so timeout tests do not
    depend on exact poll counts.
    """

    def __init__(self, responses):
        self._responses = list(responses)
        self._last = None
        self.calls = []

    def _next(self):
        if not self._responses:
            return self._last
        self._last = self._responses.pop(0)
        return self._last

    def get(self, path, params=None):
        self.calls.append(("GET", path, params))
        return self._next()

    def post(self, path, json=None):
        self.calls.append(("POST", path, json))
        return self._next()


def _fake_with(monkeypatch, *responses):
    fake = _FakeHttpx(responses)

    class _FakeApiClient:
        def get_httpx_client(self):
            return fake

    monkeypatch.setattr(
        "novita_sandbox.core.job.job_sync.get_api_client",
        lambda config, **kw: _FakeApiClient(),
    )
    return fake


def _status_payload(**overrides):
    """A camelCase status projection with EmitUnpopulated zeros."""
    payload = {
        "jobId": JOB_ID,
        "status": "migrating",
        "items": [],
        "completed": 0,
        "failed": 0,
        "cancelled": 0,
        "total": 1,
    }
    payload.update(overrides)
    return payload


def _item(**overrides):
    """One per-item projection, as a single-job lookup returns it."""
    payload = {
        "itemId": "11111111-2222-3333-4444-555555555555",
        "resourceType": "sandbox",
        "resourceId": "sbx-1",
        "status": "completed",
    }
    payload.update(overrides)
    return payload


def _page(*items, next_cursor=""):
    return {"items": list(items), "nextCursor": next_cursor}


def _error_payload(code, reason, message="boom"):
    return {"code": code, "reason": reason, "message": message, "metadata": None}


# --------------------------------------------------------------------------- #
# create: request encoding
# --------------------------------------------------------------------------- #


def test_migrate_sandbox_sends_resources_body(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))

    out = Job.migrate_sandbox(
        "sbx-1", source_region="us-phx-1", template_alias="my-alias"
    )

    assert fake.calls[0] == (
        "POST",
        "/v1/migrations",
        {
            "resources": [{"id": "sbx-1", "template_alias": "my-alias"}],
            "resource_type": "sandbox",
            "source_region": "us-phx-1",
        },
    )
    # Contract 0.2.0: the accept response carries jobId only, so create
    # returns the plain job id and nothing else.
    assert out == JOB_ID
    assert isinstance(out, str)


def test_template_alias_is_passed_through_verbatim(monkeypatch):
    """The platform does not trim, so the SDK must not either."""
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))

    Job.migrate_sandbox(
        "sbx-1", source_region="us-phx-1", template_alias="  padded  "
    )

    assert fake.calls[0][2]["resources"] == [
        {"id": "sbx-1", "template_alias": "  padded  "}
    ]


def test_blank_alias_rejected_before_request(monkeypatch):
    """An explicitly supplied alias must not be blank."""
    fake = _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException):
        Job.migrate_sandbox("sbx-1", source_region="us-phx-1", template_alias="")

    with pytest.raises(InvalidArgumentException):
        Job.migrate_sandboxes(
            ["sbx-1"], source_region="us-phx-1", template_alias="   "
        )

    assert fake.calls == []


def test_blank_alias_from_resolver_rejected_before_request(monkeypatch):
    fake = _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException) as excinfo:
        Job.migrate_sandboxes(
            ["sbx-1", "sbx-2"],
            source_region="us-phx-1",
            template_alias=(
                lambda sandbox_id: "ok" if sandbox_id == "sbx-1" else " "
            ),
        )

    assert "sbx-2" in str(excinfo.value)
    assert fake.calls == []


@pytest.mark.parametrize("use_facade", [False, True])
@pytest.mark.parametrize("alias_kwargs", [{}, {"template_alias": None}])
def test_migration_without_alias_omits_field(monkeypatch, use_facade, alias_kwargs):
    from novita_sandbox.core.client import Novita

    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))
    job = Novita(api_key="k").job if use_facade else Job

    assert job.migrate_sandbox(
        "sbx-1", source_region="us-phx-1", **alias_kwargs
    ) == JOB_ID
    assert job.migrate_sandboxes(
        ["sbx-1", "sbx-2"], source_region="us-phx-1", **alias_kwargs
    ) == JOB_ID

    assert fake.calls == [
        ("POST", "/v1/migrations", {
            "resources": resources,
            "resource_type": "sandbox",
            "source_region": "us-phx-1",
        })
        for resources in ([{"id": "sbx-1"}], [{"id": "sbx-1"}, {"id": "sbx-2"}])
    ]


def test_distribution_missing_alias_is_a_type_error(monkeypatch):
    fake = _fake_with(monkeypatch)

    with pytest.raises(TypeError):
        Job.distribute_template("tpl-1", source_region="us-phx-1")
    with pytest.raises(TypeError):
        Job.distribute_templates(["tpl-1", "tpl-2"], source_region="us-phx-1")

    assert fake.calls == []


def test_migrate_sandboxes_is_one_native_request(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))

    out = Job.migrate_sandboxes(
        ["sbx-1", "sbx-2"], source_region="us-phx-1", template_alias="shared"
    )

    # One job covering N items: a single POST with all resources.
    assert len(fake.calls) == 1
    assert fake.calls[0] == (
        "POST",
        "/v1/migrations",
        {
            "resources": [
                {"id": "sbx-1", "template_alias": "shared"},
                {"id": "sbx-2", "template_alias": "shared"},
            ],
            "resource_type": "sandbox",
            "source_region": "us-phx-1",
        },
    )
    assert out == JOB_ID


def test_migrate_sandboxes_fixed_alias_is_allowed_for_shared_base_template(
    monkeypatch,
):
    """N sandboxes sharing one base template passing the same alias is the
    normal case, so a single string alias is applied to every item."""
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))

    Job.migrate_sandboxes(
        ["sbx-1", "sbx-2"], source_region="us-phx-1", template_alias="shared"
    )

    assert fake.calls[0][2]["resources"] == [
        {"id": "sbx-1", "template_alias": "shared"},
        {"id": "sbx-2", "template_alias": "shared"},
    ]


def test_migrate_sandboxes_callable_alias_resolves_per_item(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))

    Job.migrate_sandboxes(
        ["sbx-1", "sbx-2"],
        source_region="us-phx-1",
        template_alias=lambda sandbox_id: f"{sandbox_id}-alias",
    )

    assert fake.calls[0][2]["resources"] == [
        {"id": "sbx-1", "template_alias": "sbx-1-alias"},
        {"id": "sbx-2", "template_alias": "sbx-2-alias"},
    ]


def test_migrate_sandboxes_dedupes_ids_preserving_order(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))

    Job.migrate_sandboxes(
        ["sbx-2", "sbx-1", "sbx-2"], source_region="us-phx-1", template_alias="a"
    )

    assert [item["id"] for item in fake.calls[0][2]["resources"]] == [
        "sbx-2",
        "sbx-1",
    ]


def test_migrate_sandboxes_empty_list_rejected_without_request(monkeypatch):
    fake = _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException):
        Job.migrate_sandboxes([], source_region="us-phx-1", template_alias="a")

    assert fake.calls == []


def test_distribute_template_sends_resources_body(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))

    out = Job.distribute_template(
        "tpl-1", source_region="us-phx-1", template_alias="my-alias"
    )

    assert fake.calls[0] == (
        "POST",
        "/v1/migrations",
        {
            "resources": [{"id": "tpl-1", "template_alias": "my-alias"}],
            "resource_type": "template",
            "source_region": "us-phx-1",
        },
    )
    assert out == JOB_ID


def test_distribute_templates_callable_alias_per_item(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))

    Job.distribute_templates(
        ["tpl-1", "tpl-2"],
        source_region="us-phx-1",
        template_alias=lambda template_id: f"{template_id}-from-us-phx-1",
    )

    assert fake.calls[0][2]["resources"] == [
        {"id": "tpl-1", "template_alias": "tpl-1-from-us-phx-1"},
        {"id": "tpl-2", "template_alias": "tpl-2-from-us-phx-1"},
    ]


def test_distribute_templates_fixed_alias_rejected_locally(monkeypatch):
    """N distinct templates claiming one alias can only collide, and that
    is knowable locally — reject before any request."""
    fake = _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException):
        Job.distribute_templates(
            ["tpl-1", "tpl-2"], source_region="us-phx-1", template_alias="same"
        )

    assert fake.calls == []


def test_create_rejects_bad_alias_argument(monkeypatch):
    _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException):
        Job.migrate_sandboxes(
            ["sbx-1"], source_region="us-phx-1", template_alias=123
        )


def test_create_rejects_empty_source_region(monkeypatch):
    _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException):
        Job.migrate_sandbox("sbx-1", source_region="", template_alias="a")


# --------------------------------------------------------------------------- #
# create: error mapping
# --------------------------------------------------------------------------- #


def test_alias_conflict_maps_to_alias_conflict_error(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(409, _error_payload(409, "MIGRATION_TEMPLATE_ALIAS_CONFLICT")),
    )

    with pytest.raises(TemplateAliasConflictError) as excinfo:
        Job.distribute_template("tpl-1", source_region="us-phx-1", template_alias="a")

    # The base class catches every 409 flavour, and the reason survives.
    assert isinstance(excinfo.value, MigrationConflictError)
    assert excinfo.value.reason == "MIGRATION_TEMPLATE_ALIAS_CONFLICT"


@pytest.mark.parametrize(
    ("reason", "error"),
    [
        ("MIGRATION_RESOURCE_ALREADY_MIGRATING", ResourceAlreadyMigratingError),
        ("MIGRATION_PAST_CANCEL_LINE", CancelTooLateError),
        ("MIGRATION_SHARED_DEPENDENCY", SharedDependencyError),
    ],
)
def test_every_409_reason_maps_to_its_own_error(monkeypatch, reason, error):
    _fake_with(monkeypatch, _FakeResponse(409, _error_payload(409, reason)))

    with pytest.raises(error) as excinfo:
        Job.distribute_template("tpl-1", source_region="us-phx-1", template_alias="a")

    assert isinstance(excinfo.value, MigrationConflictError)
    assert excinfo.value.reason == reason


def test_501_maps_to_not_supported(monkeypatch):
    """A v1 cluster or a deployment with migration switched off answers 501."""
    _fake_with(
        monkeypatch,
        _FakeResponse(501, _error_payload(501, "MIGRATION_NOT_SUPPORTED")),
    )

    with pytest.raises(MigrationNotSupportedError) as excinfo:
        Job.migrate_sandbox("sbx-1", source_region="us-phx-1", template_alias="a")

    assert excinfo.value.reason == "MIGRATION_NOT_SUPPORTED"


def test_bare_501_maps_to_not_supported(monkeypatch):
    _fake_with(monkeypatch, _FakeResponse(501, {}))

    with pytest.raises(MigrationNotSupportedError):
        Job.migrate_sandbox("sbx-1", source_region="us-phx-1", template_alias="a")


def test_409_without_reason_maps_to_generic_conflict(monkeypatch):
    """A 409 with no usable reason is the generic conflict, not an alias clash —
    guessing "alias" would mislabel every other 409."""
    _fake_with(monkeypatch, _FakeResponse(409, {}))

    with pytest.raises(MigrationConflictError) as excinfo:
        Job.distribute_template("tpl-1", source_region="us-phx-1", template_alias="a")

    assert not isinstance(excinfo.value, TemplateAliasConflictError)
    assert excinfo.value.reason == "MIGRATION_CONFLICT"


def test_unknown_409_reason_is_preserved_on_the_generic_conflict(monkeypatch):
    _fake_with(monkeypatch, _FakeResponse(409, _error_payload(409, "SOMETHING_NEW")))

    with pytest.raises(MigrationConflictError) as excinfo:
        Job.cancel(JOB_ID)

    assert excinfo.value.reason == "SOMETHING_NEW"
    assert not isinstance(excinfo.value, TemplateAliasConflictError)


def test_400_validator_param_maps_to_invalid_argument(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(400, _error_payload(400, "VALIDATOR_PARAM")),
    )

    with pytest.raises(InvalidArgumentException):
        Job.migrate_sandbox("sbx-1", source_region="us-phx-1", template_alias="a")


def test_400_resource_not_found_maps_to_not_found(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(400, _error_payload(400, "RESOURCE_NOT_FOUND")),
    )

    with pytest.raises(NotFoundException):
        Job.get("no-such-job")


def test_401_maps_to_authentication(monkeypatch):
    _fake_with(monkeypatch, _FakeResponse(401, _error_payload(401, "UNAUTHORIZED")))

    with pytest.raises(AuthenticationException):
        Job.migrate_sandbox("sbx-1", source_region="us-phx-1", template_alias="a")


def test_429_maps_to_rate_limit_without_retry(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(429, _error_payload(429, "UNKNOWN")))

    with pytest.raises(RateLimitException):
        Job.migrate_sandbox("sbx-1", source_region="us-phx-1", template_alias="a")

    # The SDK never retries on its own.
    assert len(fake.calls) == 1


def test_500_maps_to_sandbox_exception_keeping_reason(monkeypatch):
    _fake_with(monkeypatch, _FakeResponse(500, _error_payload(500, "UNKNOWN")))

    with pytest.raises(SandboxException) as excinfo:
        Job.migrate_sandbox("sbx-1", source_region="us-phx-1", template_alias="a")

    assert "UNKNOWN" in str(excinfo.value)


# --------------------------------------------------------------------------- #
# query
# --------------------------------------------------------------------------- #


def test_get_uses_list_route_with_job_id_query(monkeypatch):
    fake = _fake_with(
        monkeypatch,
        _FakeResponse(
            200,
            _page(
                _status_payload(
                    status="migrating", total=3, items=[_item(status="migrating")]
                )
            ),
        ),
    )

    out = Job.get(JOB_ID)

    assert fake.calls[0] == ("GET", "/v1/migrations", {"job_id": JOB_ID})
    assert out == MigrationStatus(
        job_id=JOB_ID,
        status=JobStatus.MIGRATING,
        completed=0,
        failed=0,
        cancelled=0,
        total=3,
        items=[MigrationItemStatus("11111111-2222-3333-4444-555555555555", "sandbox", "sbx-1", JobStatus.MIGRATING)],
    )


def test_get_parses_the_per_item_breakdown(monkeypatch):
    """0.2.0 puts the per-item projection on single-job lookups only."""
    _fake_with(
        monkeypatch,
        _FakeResponse(
            200,
            _page(
                _status_payload(
                    status="migrating",
                    total=2,
                    items=[
                        _item(
                            resourceType="base",
                            resourceId="tpl-base",
                            status="migrating",
                        ),
                        _item(
                            itemId="99999999-2222-3333-4444-555555555555",
                            resourceType="template",
                            resourceId="tpl-1",
                            status="failed",
                        ),
                    ],
                )
            ),
        ),
    )

    out = Job.get(JOB_ID)

    assert [item.resource_type for item in out.items] == ["base", "template"]
    assert [item.resource_id for item in out.items] == ["tpl-base", "tpl-1"]
    assert [item.status for item in out.items] == [
        JobStatus.MIGRATING,
        JobStatus.FAILED,
    ]


def test_base_item_is_not_counted_in_total(monkeypatch):
    """The base template a sandbox drags along is reported but not counted."""
    _fake_with(
        monkeypatch,
        _FakeResponse(
            200,
            _page(
                _status_payload(
                    status="completed",
                    completed=1,
                    total=1,
                    items=[_item(resourceType="base"), _item(status="completed")],
                )
            ),
        ),
    )

    out = Job.get(JOB_ID)

    assert len(out.items) == 2
    assert out.total == 1
    assert out.completed == 1


def test_list_pages_carry_no_items(monkeypatch):
    """List rows are counter-only: items is [] even when the job has them."""
    _fake_with(monkeypatch, _FakeResponse(200, _page(_status_payload(status="migrating"))))

    page = Job.list()

    assert page.items[0].items == []


def test_get_empty_items_raises_not_found(monkeypatch):
    _fake_with(monkeypatch, _FakeResponse(200, _page()))

    with pytest.raises(NotFoundException):
        Job.get(JOB_ID)


def test_list_sends_contract_query_keys(monkeypatch):
    fake = _fake_with(
        monkeypatch,
        _FakeResponse(200, _page(_status_payload())),
    )

    Job.list(
        resource_id="sbx-1",
        job_type=JobType.SANDBOX_BATCH,
        status=JobStatus.COMPLETED,
        source_region="us-phx-1",
        target_region="us-01",
        limit=5,
        cursor="c-1",
    )

    # 0.2.0 renamed the filters: type / status, not resource_type / state.
    assert fake.calls[0] == (
        "GET",
        "/v1/migrations",
        {
            "resource_id": "sbx-1",
            "type": "sandbox_batch",
            "status": "completed",
            "source_region": "us-phx-1",
            "target_region": "us-01",
            "limit": 5,
            "cursor": "c-1",
        },
    )


def test_list_region_filters_are_optional(monkeypatch):
    """The region filters are new in 0.2.0 and must stay omitted when unset."""
    fake = _fake_with(monkeypatch, _FakeResponse(200, _page()))

    Job.list(source_region="us-phx-1")

    assert fake.calls[0][2] == {"source_region": "us-phx-1"}


def test_list_omits_unset_params(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, _page()))

    Job.list()

    assert fake.calls[0] == ("GET", "/v1/migrations", {})


def test_list_parses_page_and_normalizes_empty_cursor(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(
            200,
            _page(_status_payload(status="completed"), next_cursor=""),
        ),
    )

    page = Job.list()

    assert isinstance(page, JobPage)
    assert page.next_cursor is None
    assert page.items[0].status is JobStatus.COMPLETED


def test_list_accepts_raw_string_filters(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, _page()))

    Job.list(job_type="template", status="failed")

    assert fake.calls[0][2] == {"type": "template", "status": "failed"}


def test_counters_zero_is_a_value_not_unset(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(200, _page(_status_payload(status="completed", total=0))),
    )

    out = Job.get(JOB_ID)

    # EmitUnpopulated sends 0 for unset int32 counters; a zero must survive.
    assert out.completed == 0
    assert out.failed == 0
    assert out.total == 0


def test_status_unknown_status_passes_through(monkeypatch):
    """A status this SDK predates is kept as-is rather than coerced."""
    _fake_with(
        monkeypatch,
        _FakeResponse(
            200,
            _page(
                _status_payload(
                    status="brand-new-state",
                    items=[_item(status="brand-new-state")],
                )
            ),
        ),
    )

    out = Job.get(JOB_ID)

    assert out.status == "brand-new-state"
    assert out.items[0].status == "brand-new-state"


# --------------------------------------------------------------------------- #
# cancel
# --------------------------------------------------------------------------- #


def test_cancel_posts_job_id_and_returns_reverting_snapshot(monkeypatch):
    fake = _fake_with(
        monkeypatch,
        _FakeResponse(
            200,
            _status_payload(
                status="reverting", total=3, items=[_item(status="cancelled")]
            ),
        ),
    )

    out = Job.cancel(JOB_ID)

    assert fake.calls[0] == (
        "POST",
        "/v1/migrations/cancel",
        {"job_id": JOB_ID},
    )
    assert out.status is JobStatus.REVERTING
    assert out.total == 3
    # The cancel response carries the same per-item breakdown as get().
    assert [item.status for item in out.items] == [JobStatus.CANCELLED]


def test_cancel_too_late_maps_to_its_own_error(monkeypatch):
    """Past the point of no return the job has to run to completion."""
    _fake_with(
        monkeypatch,
        _FakeResponse(
            409, _error_payload(409, "MIGRATION_PAST_CANCEL_LINE")
        ),
    )

    with pytest.raises(CancelTooLateError):
        Job.cancel(JOB_ID)


def test_cancel_terminal_job_maps_to_not_found(monkeypatch):
    """0.2.0 makes "no such job / all terminal / not yours" indistinguishable
    (anti-probing), so all three surface as NotFoundException."""
    _fake_with(
        monkeypatch,
        _FakeResponse(400, _error_payload(400, "RESOURCE_NOT_FOUND")),
    )

    with pytest.raises(NotFoundException):
        Job.cancel(JOB_ID)


# --------------------------------------------------------------------------- #
# wait
# --------------------------------------------------------------------------- #


def test_wait_polls_until_completed(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(200, _page(_status_payload(status="migrating", total=2))),
        _FakeResponse(
            200, _page(_status_payload(status="migrating", completed=1, total=2))
        ),
        _FakeResponse(
            200, _page(_status_payload(status="completed", completed=2, total=2))
        ),
    )

    seen = []
    out = Job.wait(
        JOB_ID, poll_interval=0.001, on_progress=seen.append
    )

    assert out.status is JobStatus.COMPLETED
    assert out.completed == 2
    # on_progress fires once per poll, including the terminal one.
    assert [s.status for s in seen] == [
        JobStatus.MIGRATING,
        JobStatus.MIGRATING,
        JobStatus.COMPLETED,
    ]


def test_wait_failed_raises_with_counters(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(200, _page(_status_payload(status="migrating", total=5))),
        _FakeResponse(
            200,
            _page(
                _status_payload(
                    status="failed", completed=3, failed=2, total=5
                )
            ),
        ),
    )

    with pytest.raises(JobFailedError) as excinfo:
        Job.wait(JOB_ID, poll_interval=0.001)

    assert excinfo.value.status.failed == 2
    assert excinfo.value.status.total == 5
    assert JOB_ID in str(excinfo.value)


def test_wait_cancelled_raises(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(200, _page(_status_payload(status="cancelled", total=1))),
    )

    with pytest.raises(JobCancelledError) as excinfo:
        Job.wait(JOB_ID, poll_interval=0.001)

    assert excinfo.value.status.status is JobStatus.CANCELLED


def test_wait_treats_reverting_as_non_terminal(monkeypatch):
    """Cancel rolls the job back, so reverting is not a terminal state."""
    fake = _fake_with(
        monkeypatch,
        _FakeResponse(200, _page(_status_payload(status="reverting", total=1))),
        _FakeResponse(200, _page(_status_payload(status="cancelled", total=1))),
    )

    with pytest.raises(JobCancelledError):
        Job.wait(JOB_ID, poll_interval=0.001)

    assert len(fake.calls) == 2


def test_wait_timeout_reports_last_counters(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(
            200, _page(_status_payload(status="migrating", completed=1, total=4))
        ),
        _FakeResponse(
            200, _page(_status_payload(status="migrating", completed=1, total=4))
        ),
        _FakeResponse(
            200, _page(_status_payload(status="migrating", completed=1, total=4))
        ),
    )

    with pytest.raises(TimeoutException) as excinfo:
        Job.wait(JOB_ID, timeout=0.05, poll_interval=0.02)

    assert "migrating" in str(excinfo.value)
    assert "completed=1" in str(excinfo.value)


def test_wait_validates_arguments(monkeypatch):
    _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException):
        Job.wait(JOB_ID, timeout=-1, poll_interval=1)
    with pytest.raises(InvalidArgumentException):
        Job.wait(JOB_ID, poll_interval=0)


def test_wait_returns_completed_even_with_failed_items(monkeypatch):
    """The contract defines no aggregation rule for mixed outcomes, so a
    completed projection is returned as-is and the caller checks counters."""
    _fake_with(
        monkeypatch,
        _FakeResponse(
            200,
            _page(
                _status_payload(
                    status="completed", completed=3, failed=2, total=5
                )
            ),
        ),
    )

    out = Job.wait(JOB_ID, poll_interval=0.001)

    assert out.status is JobStatus.COMPLETED
    assert out.failed == 2


# --------------------------------------------------------------------------- #
# facade
# --------------------------------------------------------------------------- #


def test_wait_progress_carries_items(monkeypatch):
    """Every wait() poll is a single-job lookup, so items is populated."""
    _fake_with(
        monkeypatch,
        _FakeResponse(
            200,
            _page(
                _status_payload(
                    status="migrating",
                    total=2,
                    items=[_item(status="migrating")],
                )
            ),
        ),
        _FakeResponse(
            200,
            _page(
                _status_payload(
                    status="completed",
                    completed=2,
                    total=2,
                    items=[_item(status="completed")],
                )
            ),
        ),
    )

    seen = []
    Job.wait(JOB_ID, poll_interval=0.001, on_progress=seen.append)

    assert len(seen[0].items) == 1
    assert seen[0].items[0].resource_type == "sandbox"
    assert seen[1].items[0].status is JobStatus.COMPLETED


def test_facade_exposes_types_and_errors():
    from novita_sandbox.core.client import Novita

    client = Novita(api_key="k")

    assert client.job.Job is Job
    assert client.job.JobStatus is JobStatus
    assert client.job.JobType is JobType
    assert client.job.MigrationStatus is MigrationStatus
    assert client.job.MigrationItemStatus is MigrationItemStatus
    assert client.job.MigrationConflictError is MigrationConflictError
    assert (
        client.job.MigrationNotSupportedError is MigrationNotSupportedError
    )
    assert client.job.TemplateAliasConflictError is TemplateAliasConflictError
    assert client.job.ResourceAlreadyMigratingError is ResourceAlreadyMigratingError
    assert client.job.CancelTooLateError is CancelTooLateError
    assert client.job.SharedDependencyError is SharedDependencyError
    assert client.job.JobFailedError is JobFailedError
    assert client.job.JobCancelledError is JobCancelledError


def test_facade_methods_hit_the_wire(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))

    from novita_sandbox.core.client import Novita

    client = Novita(api_key="k")
    out = client.job.migrate_sandboxes(
        ["sbx-1", "sbx-2"], source_region="us-phx-1", template_alias="a"
    )

    assert out == JOB_ID
    assert fake.calls[0][0] == "POST"
    assert fake.calls[0][2]["resource_type"] == "sandbox"
    assert all(
        item["template_alias"] == "a" for item in fake.calls[0][2]["resources"]
    )


# --------------------------------------------------------------------------- #
# connection opts, legacy domains, and edge cases
# --------------------------------------------------------------------------- #


def test_connection_opts_flow_into_config():
    """Connection kwargs pass through verbatim, like every other resource API."""
    from novita_sandbox.core.job.job_sync import _connection_config

    config = _connection_config(
        {"api_url": "http://configured", "request_timeout": 7}, "Job.get"
    )

    assert config.api_url == "http://configured"
    assert config.request_timeout == 7


def test_legacy_domain_rejected_before_any_request(monkeypatch):
    fake = _fake_with(monkeypatch)

    with pytest.raises(NotImplementedError):
        Job.list(domain="us-01.sandbox.novita.ai")

    assert fake.calls == []


def test_string_ids_rejected_without_request(monkeypatch):
    fake = _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException):
        Job.migrate_sandboxes("sbx-1", source_region="us-phx-1", template_alias="a")

    assert fake.calls == []


def test_one_shared_alias_for_several_templates_is_rejected(monkeypatch):
    """N templates under one alias can only collide, and that is local."""
    fake = _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException) as excinfo:
        Job.distribute_templates(
            ["tpl-1", "tpl-2"], source_region="us-phx-1", template_alias="shared"
        )

    assert "per-template function" in str(excinfo.value)
    assert fake.calls == []


def test_blank_alias_wins_over_the_shared_template_check(monkeypatch):
    """A blank alias is a different mistake, so it gets its own message."""
    fake = _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException) as excinfo:
        Job.distribute_templates(
            ["tpl-1", "tpl-2"], source_region="us-phx-1", template_alias="  "
        )

    assert "must not be blank" in str(excinfo.value)
    assert fake.calls == []


def test_create_response_without_job_id_raises(monkeypatch):
    _fake_with(monkeypatch, _FakeResponse(200, {"jobId": ""}))

    with pytest.raises(SandboxException):
        Job.migrate_sandbox("sbx-1", source_region="us-phx-1", template_alias="a")


def test_empty_cursor_omitted_from_query(monkeypatch):
    fake = _fake_with(
        monkeypatch, _FakeResponse(200, {"items": [], "nextCursor": ""})
    )

    Job.list(cursor="")

    assert "cursor" not in fake.calls[0][2]


def test_reason_wins_over_conflicting_status(monkeypatch):
    """A 409 envelope carrying RESOURCE_NOT_FOUND honors its reason."""
    _fake_with(
        monkeypatch,
        _FakeResponse(
            409,
            {"code": 409, "reason": "RESOURCE_NOT_FOUND", "message": "no such job"},
        ),
    )

    with pytest.raises(NotFoundException):
        Job.get(JOB_ID)
