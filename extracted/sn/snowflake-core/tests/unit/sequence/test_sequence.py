from unittest import mock

import pytest

from snowflake.core import CreateMode, PollingOperation
from snowflake.core.sequence import Sequence, SequenceResource

from ...utils import BASE_URL, extra_params, mock_http_response


@pytest.fixture
def sequences(schema):
    return schema.sequences


@pytest.fixture
def sequence(sequences) -> SequenceResource:
    return sequences["my_sequence"]


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
SEQUENCE = Sequence(name="my_sequence", start=1, increment=1, ordered=True, comment="Test sequence")


def test_create_sequence(fake_root, sequences):
    kwargs = extra_params(
        body={
            "name": "my_sequence",
            "start": 1,
            "increment": 1,
            "ordered": True,
            "comment": "Test sequence",
        },
    )
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/sequences")

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        s_res = sequences.create(SEQUENCE)
        assert isinstance(s_res, SequenceResource)
        assert s_res.name == "my_sequence"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = sequences.create_async(SEQUENCE)
        assert isinstance(op, PollingOperation)
        s_res = op.result()
        assert s_res.name == "my_sequence"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_sequence(fake_root, sequences):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/sequences")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        sequences.iter()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = sequences.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_sequence(fake_root, sequence):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/sequences/my_sequence")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(SEQUENCE.to_json())
        s = sequence.fetch()
        assert s.to_dict() == SEQUENCE.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(SEQUENCE.to_json())
        op = sequence.fetch_async()
        assert isinstance(op, PollingOperation)
        s = op.result()
        assert s.to_dict() == SEQUENCE.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_sequence(fake_root, sequence):
    args = (fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/sequences/my_sequence")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        sequence.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = sequence.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_rename_sequence(fake_root, sequence, sequences):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/sequences/my_sequence:rename?targetName=new_sequence",
    )
    kwargs = extra_params(query_params=[("targetName", "new_sequence")])

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        sequence.rename("new_sequence")
        assert sequence.name == "new_sequence"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        s_res = sequences["another_sequence"]
        op = s_res.rename_async("new_sequence")
        assert isinstance(op, PollingOperation)
        op.result()
        assert s_res.name == "new_sequence"
    args2 = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/sequences/another_sequence:rename?targetName=new_sequence",
    )
    mocked_request.assert_called_once_with(*args2, **kwargs)


def test_rename_sequence_with_options(fake_root, sequence):
    args = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/sequences/my_sequence:rename?ifExists=True&targetDatabase=other_db&targetSchema=other_schema&targetName=new_sequence",
    )
    kwargs = extra_params(
        query_params=[
            ("ifExists", True),
            ("targetDatabase", "other_db"),
            ("targetSchema", "other_schema"),
            ("targetName", "new_sequence"),
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        sequence.rename(
            "new_sequence",
            target_database="other_db",
            target_schema="other_schema",
            if_exists=True,
        )
        assert sequence.name == "new_sequence"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_clone_sequence(fake_root, sequence):
    sequence_clone = Sequence(name="sequence_clone")
    args = (
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/sequences/my_sequence:clone",
    )
    kwargs = extra_params(
        body={
            "name": "sequence_clone",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        sequence.clone(sequence_clone)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = sequence.clone_async(sequence_clone)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_clone_sequence_with_options(fake_root, sequence):
    args = (
        fake_root,
        "POST",
        BASE_URL
        + "/databases/my_db/schemas/my_schema/sequences/my_sequence:clone?createMode=orReplace&targetDatabase=other_db&targetSchema=other_schema",
    )
    kwargs = extra_params(
        query_params=[
            ("createMode", "orReplace"),
            ("targetDatabase", "other_db"),
            ("targetSchema", "other_schema"),
        ],
        body={
            "name": "sequence_clone",
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        sequence.clone(
            Sequence(name="sequence_clone"),
            create_mode=CreateMode.or_replace,
            target_database="other_db",
            target_schema="other_schema",
        )
    mocked_request.assert_called_once_with(*args, **kwargs)
