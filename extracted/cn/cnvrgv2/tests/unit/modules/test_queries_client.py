import pytest

from cnvrgv2.proxy import Proxy
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.queries.query import Query
from cnvrgv2.modules.queries.queries_client import QueriesClient
from cnvrgv2.utils.json_api_format import JAF


class TestQueriesClient:
    def test_init_valid_credentials(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = QueriesClient(empty_cnvrg)
        assert client._context
        assert client._route

    def test_get_with_slug(self, mocker, empty_context, empty_cnvrg):
        slug = "test-slug"

        def mock_call_api(*args, **kwargs):
            response = {
                "data": {
                    "id": "17",
                    "type": "query",
                    "attributes": {
                        "slug": slug,
                        "name": "test-name",
                        "query": "test-query",
                        "commit_sha1": "5b384ce32d8cdef02bc3a139d4cac0a22bb029e8",
                    }
                }
            }
            return JAF(response=response)

        mocked_api_call = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        empty_cnvrg._context = empty_context
        client = QueriesClient(empty_cnvrg)
        model = client.get(slug)

        # The function will not be called on init since its lazy-loading
        assert mocked_api_call.call_count == 0

        # The function will be called when accessing an attribute
        assert model.name == "test-name"
        assert mocked_api_call.call_count > 0

        assert type(model) is Query

    def test_get_with_empty_slug(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = QueriesClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.get("")

    def test_get_with_none_slug(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = QueriesClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.get(None)

    def test_get_with_wrong_type_slug(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = QueriesClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.get({"say": "whaaat??"})

    def test_valid_create(self, mocker, empty_context, empty_cnvrg):
        name = "test-name"
        query = "test-query"

        def mock_call_api(*args, **kwargs):
            response = {
                "data": {
                    "id": "17",
                    "type": "project",
                    "attributes": {
                        "slug": "test-slug",
                        "name": name,
                        "query": query,
                        "commit_sha1": "5b384ce32d8cdef02bc3a139d4cac0a22bb029e8",
                    }
                }
            }
            return JAF(response=response)

        mocked_api_call = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        empty_cnvrg._context = empty_context
        client = QueriesClient(empty_cnvrg)
        model = client.create(name=name, query=query, commit_sha1=None)

        # TODO: add attribute checks. added call_count until decided what to check
        assert type(model) is Query
        assert mocked_api_call.call_count > 0

    def test_create_with_empty_name(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = QueriesClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create(name="", query="test-query")

    def test_create_with_none_name(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = QueriesClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create(name=None, query="test-query")

    def test_create_with_empty_query(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = QueriesClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create(name="test-name", query="")

    def test_create_with_none_query(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = QueriesClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create(name="test-name", query=None)
