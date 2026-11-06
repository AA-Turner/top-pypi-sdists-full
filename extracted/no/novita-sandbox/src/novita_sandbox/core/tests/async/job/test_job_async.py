"""Tests for the async migration Job API (no network; httpx client is stubbed).

Covers parity with the sync suite on the paths that could plausibly diverge:
request/query encoding, response decoding, the reason-based error mapping and
the polling loop.
"""

import pytest

from novita_sandbox import (
    AsyncJob,
    CancelTooLateError,
    JobCancelledError,
    JobFailedError,
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


class _FakeAsyncHttpx:
    """Returns queued responses; when dry, the last response repeats."""

    def __init__(self, responses):
        self._responses = list(responses)
        self._last = None
        self.calls = []

    def _next(self):
        if not self._responses:
            return self._last
        self._last = self._responses.pop(0)
        return self._last

    async def get(self, path, params=None):
        self.calls.append(("GET", path, params))
        return self._next()

    async def post(self, path, json=None):
        self.calls.append(("POST", path, json))
        return self._next()


def _fake_with(monkeypatch, *responses):
    fake = _FakeAsyncHttpx(responses)

    class _FakeApiClient:
        def get_async_httpx_client(self):
            return fake

    monkeypatch.setattr(
        "novita_sandbox.core.job.job_async.get_api_client",
        lambda config, **kw: _FakeApiClient(),
    )
    return fake


def _status_payload(**overrides):
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


@pytest.mark.asyncio
@pytest.mark.parametrize("alias_kwargs", [{}, {"template_alias": None}])
async def test_migration_without_alias_omits_field(monkeypatch, alias_kwargs):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))

    assert await AsyncJob.migrate_sandbox(
        "sbx-1", source_region="us-phx-1", **alias_kwargs
    ) == JOB_ID
    assert await AsyncJob.migrate_sandboxes(
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


@pytest.mark.asyncio
async def test_distribution_missing_alias_is_a_type_error(monkeypatch):
    fake = _fake_with(monkeypatch)

    with pytest.raises(TypeError):
        await AsyncJob.distribute_template("tpl-1", source_region="us-phx-1")
    with pytest.raises(TypeError):
        await AsyncJob.distribute_templates(["tpl-1", "tpl-2"], source_region="us-phx-1")

    assert fake.calls == []


@pytest.mark.asyncio
async def test_migrate_sandbox_sends_resources_body(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))

    out = await AsyncJob.migrate_sandbox(
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
    assert out == JOB_ID


@pytest.mark.asyncio
async def test_migrate_sandboxes_one_native_request_with_callable_alias(
    monkeypatch,
):
    fake = _fake_with(monkeypatch, _FakeResponse(200, {"jobId": JOB_ID}))

    out = await AsyncJob.migrate_sandboxes(
        ["sbx-1", "sbx-2"],
        source_region="us-phx-1",
        template_alias=lambda sandbox_id: f"{sandbox_id}-alias",
    )

    assert len(fake.calls) == 1
    assert fake.calls[0][2]["resources"] == [
        {"id": "sbx-1", "template_alias": "sbx-1-alias"},
        {"id": "sbx-2", "template_alias": "sbx-2-alias"},
    ]
    assert out == JOB_ID


@pytest.mark.asyncio
async def test_migrate_sandboxes_empty_list_rejected_without_request(monkeypatch):
    fake = _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException):
        await AsyncJob.migrate_sandboxes([], source_region="us-phx-1", template_alias="a")

    assert fake.calls == []


@pytest.mark.asyncio
async def test_distribute_templates_fixed_alias_rejected_locally(monkeypatch):
    fake = _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException):
        await AsyncJob.distribute_templates(
            ["tpl-1", "tpl-2"], source_region="us-phx-1", template_alias="same"
        )

    assert fake.calls == []


@pytest.mark.asyncio
async def test_alias_conflict_maps_to_alias_conflict_error(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(409, _error_payload(409, "MIGRATION_TEMPLATE_ALIAS_CONFLICT")),
    )

    with pytest.raises(TemplateAliasConflictError) as excinfo:
        await AsyncJob.distribute_template(
            "tpl-1", source_region="us-phx-1", template_alias="a"
        )

    assert isinstance(excinfo.value, MigrationConflictError)
    assert excinfo.value.reason == "MIGRATION_TEMPLATE_ALIAS_CONFLICT"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("reason", "error"),
    [
        ("MIGRATION_RESOURCE_ALREADY_MIGRATING", ResourceAlreadyMigratingError),
        ("MIGRATION_PAST_CANCEL_LINE", CancelTooLateError),
        ("MIGRATION_SHARED_DEPENDENCY", SharedDependencyError),
    ],
)
async def test_every_409_reason_maps_to_its_own_error(monkeypatch, reason, error):
    _fake_with(monkeypatch, _FakeResponse(409, _error_payload(409, reason)))

    with pytest.raises(error) as excinfo:
        await AsyncJob.cancel(JOB_ID)

    assert excinfo.value.reason == reason


@pytest.mark.asyncio
async def test_501_maps_to_not_supported(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(501, _error_payload(501, "MIGRATION_NOT_SUPPORTED")),
    )

    with pytest.raises(MigrationNotSupportedError):
        await AsyncJob.migrate_sandbox(
            "sbx-1", source_region="us-phx-1", template_alias="a"
        )


@pytest.mark.asyncio
async def test_409_without_reason_maps_to_generic_conflict(monkeypatch):
    _fake_with(monkeypatch, _FakeResponse(409, {}))

    with pytest.raises(MigrationConflictError) as excinfo:
        await AsyncJob.cancel(JOB_ID)

    assert not isinstance(excinfo.value, TemplateAliasConflictError)


@pytest.mark.asyncio
async def test_400_resource_not_found_maps_to_not_found(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(400, _error_payload(400, "RESOURCE_NOT_FOUND")),
    )

    with pytest.raises(NotFoundException):
        await AsyncJob.get("no-such-job")


@pytest.mark.asyncio
async def test_401_maps_to_authentication(monkeypatch):
    _fake_with(monkeypatch, _FakeResponse(401, _error_payload(401, "UNAUTHORIZED")))

    with pytest.raises(AuthenticationException):
        await AsyncJob.migrate_sandbox(
            "sbx-1", source_region="us-phx-1", template_alias="a"
        )


@pytest.mark.asyncio
async def test_500_maps_to_sandbox_exception_keeping_reason(monkeypatch):
    _fake_with(monkeypatch, _FakeResponse(500, _error_payload(500, "UNKNOWN")))

    with pytest.raises(SandboxException) as excinfo:
        await AsyncJob.migrate_sandbox(
            "sbx-1", source_region="us-phx-1", template_alias="a"
        )

    assert "UNKNOWN" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_uses_list_route_with_job_id_query(monkeypatch):
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

    out = await AsyncJob.get(JOB_ID)

    assert fake.calls[0] == ("GET", "/v1/migrations", {"job_id": JOB_ID})
    assert out == MigrationStatus(
        job_id=JOB_ID,
        status=JobStatus.MIGRATING,
        completed=0,
        failed=0,
        cancelled=0,
        total=3,
        items=[
            MigrationItemStatus(
                "11111111-2222-3333-4444-555555555555",
                "sandbox",
                "sbx-1",
                JobStatus.MIGRATING,
            )
        ],
    )


@pytest.mark.asyncio
async def test_list_sends_contract_query_keys(monkeypatch):
    fake = _fake_with(monkeypatch, _FakeResponse(200, _page()))

    await AsyncJob.list(
        resource_id="sbx-1",
        job_type=JobType.TEMPLATE,
        status=JobStatus.FAILED,
        source_region="us-phx-1",
        target_region="us-01",
        limit=5,
        cursor="c-1",
    )

    assert fake.calls[0] == (
        "GET",
        "/v1/migrations",
        {
            "resource_id": "sbx-1",
            "type": "template",
            "status": "failed",
            "source_region": "us-phx-1",
            "target_region": "us-01",
            "limit": 5,
            "cursor": "c-1",
        },
    )


@pytest.mark.asyncio
async def test_list_parses_page_and_normalizes_empty_cursor(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(
            200, _page(_status_payload(status="completed"), next_cursor="")
        ),
    )

    page = await AsyncJob.list()

    assert page.next_cursor is None
    assert page.items[0].status is JobStatus.COMPLETED


@pytest.mark.asyncio
async def test_cancel_posts_job_id_and_returns_reverting_snapshot(monkeypatch):
    fake = _fake_with(
        monkeypatch,
        _FakeResponse(
            200,
            _status_payload(
                status="reverting", total=3, items=[_item(status="cancelled")]
            ),
        ),
    )

    out = await AsyncJob.cancel(JOB_ID)

    assert fake.calls[0] == (
        "POST",
        "/v1/migrations/cancel",
        {"job_id": JOB_ID},
    )
    assert out.status is JobStatus.REVERTING
    assert [item.status for item in out.items] == [JobStatus.CANCELLED]


@pytest.mark.asyncio
async def test_wait_polls_until_completed(monkeypatch):
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
    out = await AsyncJob.wait(
        JOB_ID, poll_interval=0.001, on_progress=seen.append
    )

    assert out.status is JobStatus.COMPLETED
    assert [s.status for s in seen] == [
        JobStatus.MIGRATING,
        JobStatus.MIGRATING,
        JobStatus.COMPLETED,
    ]


@pytest.mark.asyncio
async def test_wait_failed_raises_with_counters(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(
            200,
            _page(_status_payload(status="failed", completed=3, failed=2, total=5)),
        ),
    )

    with pytest.raises(JobFailedError) as excinfo:
        await AsyncJob.wait(JOB_ID, poll_interval=0.001)

    assert excinfo.value.status.failed == 2
    assert excinfo.value.status.total == 5


@pytest.mark.asyncio
async def test_wait_cancelled_raises(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(200, _page(_status_payload(status="cancelled", total=1))),
    )

    with pytest.raises(JobCancelledError):
        await AsyncJob.wait(JOB_ID, poll_interval=0.001)


@pytest.mark.asyncio
async def test_wait_treats_reverting_as_non_terminal(monkeypatch):
    fake = _fake_with(
        monkeypatch,
        _FakeResponse(200, _page(_status_payload(status="reverting", total=1))),
        _FakeResponse(200, _page(_status_payload(status="cancelled", total=1))),
    )

    with pytest.raises(JobCancelledError):
        await AsyncJob.wait(JOB_ID, poll_interval=0.001)

    assert len(fake.calls) == 2


@pytest.mark.asyncio
async def test_wait_timeout_reports_last_counters(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(
            200, _page(_status_payload(status="migrating", completed=1, total=4))
        ),
    )

    with pytest.raises(TimeoutException) as excinfo:
        await AsyncJob.wait(JOB_ID, timeout=0.05, poll_interval=0.02)

    assert "migrating" in str(excinfo.value)
    assert "completed=1" in str(excinfo.value)


@pytest.mark.asyncio
async def test_wait_validates_arguments(monkeypatch):
    _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException):
        await AsyncJob.wait(JOB_ID, timeout=-1, poll_interval=1)
    with pytest.raises(InvalidArgumentException):
        await AsyncJob.wait(JOB_ID, poll_interval=0)


# --------------------------------------------------------------------------- #
# connection opts, legacy domains, and edge cases
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_legacy_domain_rejected_before_any_request(monkeypatch):
    fake = _fake_with(monkeypatch)

    with pytest.raises(NotImplementedError):
        await AsyncJob.list(domain="us-01.sandbox.novita.ai")

    assert fake.calls == []


@pytest.mark.asyncio
async def test_string_ids_rejected_without_request(monkeypatch):
    fake = _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException):
        await AsyncJob.migrate_sandboxes(
            "sbx-1", source_region="us-phx-1", template_alias="a"
        )

    assert fake.calls == []


@pytest.mark.asyncio
async def test_blank_alias_rejected_before_request(monkeypatch):
    fake = _fake_with(monkeypatch)

    with pytest.raises(InvalidArgumentException):
        await AsyncJob.migrate_sandboxes(
            ["sbx-1", "sbx-2"], source_region="us-phx-1", template_alias="  "
        )

    assert fake.calls == []


@pytest.mark.asyncio
async def test_create_response_without_job_id_raises(monkeypatch):
    _fake_with(monkeypatch, _FakeResponse(200, {}))

    with pytest.raises(SandboxException):
        await AsyncJob.migrate_sandbox(
            "sbx-1", source_region="us-phx-1", template_alias="a"
        )


@pytest.mark.asyncio
async def test_empty_cursor_omitted_from_query(monkeypatch):
    fake = _fake_with(
        monkeypatch, _FakeResponse(200, {"items": [], "nextCursor": ""})
    )

    await AsyncJob.list(cursor="")

    assert "cursor" not in fake.calls[0][2]


@pytest.mark.asyncio
async def test_reason_wins_over_conflicting_status(monkeypatch):
    _fake_with(
        monkeypatch,
        _FakeResponse(
            409,
            {"code": 409, "reason": "RESOURCE_NOT_FOUND", "message": "no such job"},
        ),
    )

    with pytest.raises(NotFoundException):
        await AsyncJob.get(JOB_ID)
