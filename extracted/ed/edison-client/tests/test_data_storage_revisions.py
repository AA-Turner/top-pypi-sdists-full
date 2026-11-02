import inspect
import json
from uuid import UUID, uuid4

import httpx
import pytest
from pydantic import ValidationError

from edison_client.clients.data_storage_methods import (
    DataStorageError,
    DataStorageMethods,
)
from edison_client.clients.exceptions import (
    DataStorageConflictError,
    DataStorageNotFoundError,
    DataStoragePermissionError,
    DataStorageValidationError,
)
from edison_client.models.data_storage_methods import DataStorageRevisionUpdate


async def invoke(method, *args, **kwargs):
    result = method(*args, **kwargs)
    return await result if inspect.isawaitable(result) else result


class StorageClient(DataStorageMethods):
    def __init__(self, client, async_client):
        self._client = client
        self._async_client = async_client

    @property
    def client(self):
        return self._client

    @property
    def async_client(self):
        return self._async_client


@pytest.fixture(name="entry_response")
def fixture_entry_response():
    entry_id, revision_id = str(uuid4()), str(uuid4())
    return {
        "data_storage": {
            "id": entry_id,
            "name": "report.txt",
            "content": "",
            "status": "active",
            "share_status": "private",
            "user_id": "owner",
            "created_at": "2026-09-10T00:00:00Z",
            "modified_at": "2026-09-10T00:00:00Z",
        },
        "storage_locations": [
            {
                "id": str(uuid4()),
                "data_storage_id": entry_id,
                "created_at": "2026-09-10T00:00:00Z",
                "storage_config": {
                    "storage_type": "raw_content",
                    "content_type": "text",
                },
            }
        ],
        "content": "",
        "revision_id": revision_id,
        "version": 2,
        "current_revision_id": str(uuid4()),
        "revision_generation": 3,
    }


@pytest.fixture(name="storage_client")
async def fixture_storage_client():
    clients = []

    def create(handler):
        transport = httpx.MockTransport(handler)
        client = httpx.Client(transport=transport, base_url="https://storage.test")
        async_client = httpx.AsyncClient(
            transport=transport, base_url="https://storage.test"
        )
        clients.append((client, async_client))
        return StorageClient(client, async_client)

    yield create
    for client, async_client in clients:
        client.close()
        await async_client.aclose()


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("fetch", [False, True])
@pytest.mark.parametrize("selector", ["latest", "version", "revision_id"])
async def test_exact_reads_preserve_selectors_and_empty_content(
    storage_client, entry_response, asynchronous, fetch, selector
):
    selectors: dict[str, int | UUID] = {}
    if selector == "version":
        selectors[selector] = 0
    elif selector == "revision_id":
        selectors[selector] = uuid4()

    def handle(request):
        assert request.url.path == "/v0.1/data-storage/data-entries/report-alias"
        assert dict(request.url.params) == {k: str(v) for k, v in selectors.items()}
        return httpx.Response(200, json=entry_response)

    client = storage_client(handle)
    name = "fetch_data_from_storage" if fetch else "get_data_storage_entry"
    method = getattr(client, f"a{name}" if asynchronous else name)
    result = method("report-alias", **selectors)
    if asynchronous:
        result = await result
    assert result.content == ""  # noqa: PLC1901
    if not fetch:
        assert str(result.revision_id) == entry_response["revision_id"]
        assert str(result.current_revision_id) == entry_response["current_revision_id"]
        assert result.version == 2
        assert result.revision_generation == 3
    await client.async_client.aclose()


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("fetch", [False, True])
async def test_missing_exact_read_fails(storage_client, asynchronous, fetch):
    client = storage_client(
        lambda _: httpx.Response(404, json={"detail": "Missing revision"})
    )
    name = "fetch_data_from_storage" if fetch else "get_data_storage_entry"
    method = getattr(client, f"a{name}" if asynchronous else name)
    with pytest.raises(DataStorageNotFoundError, match="404"):
        await invoke(method, "report-alias", version=99)
    await client.async_client.aclose()


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("description", [None, "Corrected results", ""])
async def test_update_retries_same_revision_and_does_not_retry_conflicts(
    storage_client, entry_response, asynchronous, description
):
    bodies = []
    payload = DataStorageRevisionUpdate(
        revision_id=uuid4(),
        base_revision_id=uuid4(),
        content="",
        publish=False,
        description=description,
    )

    def handle(request):
        assert request.method == "PATCH"
        bodies.append(json.loads(request.content))
        if description is None:
            assert "description" not in bodies[-1]
        else:
            assert bodies[-1]["description"] == description
        if len(bodies) == 1:
            raise httpx.ReadTimeout("Response lost", request=request)
        if len(bodies) == 2:
            return httpx.Response(200, json=entry_response)
        return httpx.Response(409, json={"detail": "Newer revision exists"})

    client = storage_client(handle)
    method = (
        client.aupdate_data_storage_entry
        if asynchronous
        else client.update_data_storage_entry
    )
    result = method("report-alias", payload)
    if asynchronous:
        result = await result
    assert result.version == 2
    assert bodies == [payload.model_dump(mode="json", exclude_none=True)] * 2
    with pytest.raises(DataStorageConflictError, match="409") as exc:
        await invoke(method, "report-alias", payload)
    assert isinstance(exc.value.__cause__, httpx.HTTPStatusError)
    assert exc.value.__cause__.response.status_code == 409
    assert len(bodies) == 3
    await client.async_client.aclose()


@pytest.mark.parametrize("asynchronous", [False, True])
async def test_history_pagination_and_draft_publication(
    storage_client, entry_response, asynchronous
):
    revision_id, base_id = uuid4(), uuid4()

    def handle(request):
        if request.method == "PATCH":
            assert json.loads(request.content) == {
                "revision_id": str(revision_id),
                "base_revision_id": str(base_id),
                "publish": True,
            }
            return httpx.Response(200, json=entry_response)
        assert request.url.path.endswith("/report-alias/revisions")
        assert dict(request.url.params) == {
            "limit": "10",
            "offset": "20",
            "include_unpublished": "true",
        }
        return httpx.Response(
            200,
            json={
                "entry_id": entry_response["data_storage"]["id"],
                "current_revision_id": entry_response["current_revision_id"],
                "revisions": [
                    {
                        "id": str(revision_id),
                        "entry_id": entry_response["data_storage"]["id"],
                        "version": 4,
                        "parent_revision_id": str(base_id),
                        "snapshot": {
                            "name": "report.txt",
                            "content": "draft",
                            "embedding": [1.0, 0.0],
                        },
                        "created_by": "owner",
                        "trajectory_id": None,
                        "created_at": "2026-09-10T00:00:00Z",
                        "published_at": None,
                    }
                ],
            },
        )

    client = storage_client(handle)
    method = (
        client.alist_data_storage_revisions
        if asynchronous
        else client.list_data_storage_revisions
    )
    history = method("report-alias", limit=10, offset=20, include_unpublished=True)
    if asynchronous:
        history = await history
    assert history.revisions[0].snapshot.content == "draft"
    assert history.revisions[0].snapshot.embedding == [1.0, 0.0]
    assert history.revisions[0].published_at is None
    update = (
        client.aupdate_data_storage_entry
        if asynchronous
        else client.update_data_storage_entry
    )
    result = update(
        "report-alias",
        DataStorageRevisionUpdate(revision_id=revision_id, base_revision_id=base_id),
    )
    if asynchronous:
        await result
    await client.async_client.aclose()


@pytest.mark.parametrize(
    "fields",
    [
        {"content": "", "source_entry_id": uuid4()},
        {"publish": False},
        {"name": "renamed"},
    ],
)
def test_invalid_updates_fail_locally(fields):
    with pytest.raises(ValidationError) as exc:
        DataStorageRevisionUpdate(
            revision_id=uuid4(), base_revision_id=uuid4(), **fields
        )
    assert isinstance(exc.value.errors()[0]["ctx"]["error"], DataStorageValidationError)


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("fetch", [False, True])
@pytest.mark.parametrize(
    "selectors", [{"version": -1}, {"version": 0, "revision_id": uuid4()}]
)
async def test_invalid_read_selectors_fail_before_http(
    storage_client, asynchronous, fetch, selectors
):
    def handle(_):
        pytest.fail("Invalid selectors must not make an HTTP request")

    client = storage_client(handle)
    name = "fetch_data_from_storage" if fetch else "get_data_storage_entry"
    method = getattr(client, f"a{name}" if asynchronous else name)
    with pytest.raises(DataStorageValidationError):
        await invoke(method, "report-alias", **selectors)
    await client.async_client.aclose()


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize(
    ("status_code", "error_type"),
    [
        (403, DataStoragePermissionError),
        (404, DataStorageNotFoundError),
        (409, DataStorageConflictError),
        (422, DataStorageValidationError),
    ],
)
async def test_storage_http_errors_preserve_specific_type_and_cause(
    storage_client, asynchronous, status_code, error_type
):
    client = storage_client(
        lambda _: httpx.Response(status_code, json={"detail": "Rejected"})
    )
    method = (
        client.aupdate_data_storage_entry
        if asynchronous
        else client.update_data_storage_entry
    )
    payload = DataStorageRevisionUpdate(
        revision_id=uuid4(), base_revision_id=uuid4(), content="new"
    )
    with pytest.raises(error_type) as exc:
        await invoke(method, "report-alias", payload)
    assert isinstance(exc.value, DataStorageError)
    assert isinstance(exc.value.__cause__, httpx.HTTPStatusError)
    assert exc.value.__cause__.response.status_code == status_code


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("params", [{"limit": 0}, {"limit": 101}, {"offset": -1}])
async def test_invalid_history_pagination_raises_validation_error(
    storage_client, asynchronous, params
):
    def unexpected_request(_):
        pytest.fail("Invalid pagination must fail before HTTP")

    client = storage_client(unexpected_request)
    method = (
        client.alist_data_storage_revisions
        if asynchronous
        else client.list_data_storage_revisions
    )
    with pytest.raises(DataStorageValidationError):
        await invoke(method, "report-alias", **params)
