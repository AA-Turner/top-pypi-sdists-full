from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.service import JobService, Service, ServiceSpecInlineText
from snowflake.core.service._generated import FetchServiceLogs200Response, FetchServiceStatus200Response

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.service._generated.api_client.ApiClient.request"
SERVICE = Service(name="my_service", compute_pool="my_compute_pool", spec=ServiceSpecInlineText(spec_text=""))
JOB_SERVICE = JobService(name="my_service", compute_pool="my_compute_pool", spec=ServiceSpecInlineText(spec_text=""))


@pytest.fixture
def services(schema):
    return schema.services


@pytest.fixture
def service(services):
    return services["my_service"]


def test_create_service(fake_root, services):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/services?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={
            "name": "my_service",
            "compute_pool": "my_compute_pool",
            "spec": {"spec_text": "", "spec_type": "from_inline"},
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        services.create(SERVICE)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = services.create_async(SERVICE)
        assert isinstance(op, PollingOperation)
        service_res = op.result()
        assert service_res.name == "my_service"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_service(fake_root, services):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/services",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        services.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = services.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_execute_job_service(fake_root, services):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/services:execute-job",
    )
    kwargs = extra_params(
        body={
            "name": "my_service",
            "compute_pool": "my_compute_pool",
            "spec": {"spec_text": "", "spec_type": "from_inline"},
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        services.execute_job(JOB_SERVICE)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = services.execute_job_async(JOB_SERVICE)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_create_or_alter_service(fake_root, service):
    args = (
        fake_root,
        "PUT",
        BASE_URL + "/databases/my_db/schemas/my_schema/services/my_service",
    )
    kwargs = extra_params(
        body={
            "name": "my_service",
            "compute_pool": "my_compute_pool",
            "spec": {"spec_text": "", "spec_type": "from_inline"},
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        service.create_or_alter(SERVICE)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = service.create_or_alter_async(SERVICE)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_service(fake_root, service):
    from snowflake.core.service._generated.models import Service as ServiceModel
    from snowflake.core.service._generated.models import ServiceSpecInlineText as ServiceSpecInlineTextModel

    model = ServiceModel(
        name="my_service", compute_pool="my_compute_pool", spec=ServiceSpecInlineTextModel(spec_text=""))
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/services/my_service",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        service.fetch()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = service.fetch_async()
        assert isinstance(op, PollingOperation)
        service = op.result()
        assert service.to_dict() == SERVICE.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_service(fake_root, service):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/services/my_service",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        service.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = service.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_suspend_service(fake_root, service):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/services/my_service:suspend",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        service.suspend()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = service.suspend_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_resume_service(fake_root, service):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/services/my_service:resume",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        service.resume()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = service.resume_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


CUSTOM_METHODS = [
    ("endpoints", "get_endpoints", ()),
    ("containers", "get_containers", ()),
    ("instances", "get_instances", ()),
    ("roles", "get_roles", ()),
    ("roles/my_role/grants-of", "iter_grants_of_service_role", ("my_role",)),
    ("roles/my_role/grants", "iter_grants_to_service_role", ("my_role",)),
]


@pytest.mark.parametrize("method, fn, fn_args", CUSTOM_METHODS)
def test_custom_methods(fake_root, service, method, fn, fn_args):
    args = (
        fake_root,
        "GET",
        BASE_URL + f"/databases/my_db/schemas/my_schema/services/my_service/{method}",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        it = getattr(service, fn)(*fn_args)
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = getattr(service, fn + "_async")(*fn_args)
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_service_status(fake_root, service):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/services/my_service/status?timeout=0",
    )
    kwargs = extra_params(query_params=[("timeout", 0)])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(FetchServiceStatus200Response().to_json())
        service.get_service_status()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(FetchServiceStatus200Response().to_json())
        op = service.get_service_status_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_service_logs(fake_root, service):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/services/my_service/logs?" + \
            "instanceId=1&containerName=my_container",
    )
    kwargs = extra_params(query_params=[("instanceId", 1), ("containerName", "my_container")])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(FetchServiceLogs200Response().to_json())
        service.get_service_logs(1, "my_container")
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(FetchServiceLogs200Response().to_json())
        op = service.get_service_logs_async(1, "my_container")
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
