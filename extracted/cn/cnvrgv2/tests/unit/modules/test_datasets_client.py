import pytest

from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.dataset import Dataset
from cnvrgv2.modules.datasets_client import DatasetsClient
from cnvrgv2.proxy import Proxy
from cnvrgv2.utils.json_api_format import JAF


class TestDatasetsClient:
    def test_init_no_credentials(self):
        with pytest.raises(CnvrgArgumentsError):
            DatasetsClient(None)

    def test_init_valid_credentials(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        assert client._context
        assert client._route

    def test_get_with_slug(self, mocker, empty_context, empty_cnvrg):
        slug = "test-slug"

        def mock_call_api(*args, **kwargs):
            response = {
                "data": {
                    "id": "17",
                    "type": "dataset",
                    "attributes": {
                        "title": "test-title",
                        "slug": slug,
                    }
                }
            }
            return JAF(response=response)

        mocked_api_call = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        model = client.get(slug)

        # The function will not be called on init since its lazy-loading
        assert mocked_api_call.call_count == 0

        # The function will not be called on init since its lazy-loading
        assert model.title == "test-title"
        assert mocked_api_call.call_count > 0

        assert type(model) is Dataset

    def test_get_with_empty_slug(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.get("")

    def test_get_with_none_slug(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.get(None)

    def test_get_with_wrong_type_slug(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.get({"say": "whaaat??"})

    def test_valid_create(self, mocker, empty_context, empty_cnvrg):
        def mock_call_api(*args, **kwargs):
            response = {
                "data": {
                    "id": "17",
                    "type": "dataset",
                    "attributes": {
                        "title": "test-title",
                        "slug": "test-slug",
                    }
                }
            }
            return JAF(response=response)

        mocked_api_call = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        model_no_cat = client.create("test-title")
        model_with_cat = client.create("test-title", category="images")

        # TODO: add attribute checks. added call_count until decided what to check
        assert type(model_no_cat) is Dataset
        assert type(model_with_cat) is Dataset
        assert mocked_api_call.call_count > 0

    def test_create_with_empty_name(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create("")

    def test_create_with_none_name(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create(None)

    def test_create_with_wrong_type_name(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create({"say": "whaaat??"})

    def test_create_with_empty_category(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create("name", category="")

    def test_create_with_none_category(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create("name", category=None)

    def test_create_with_wrong_type_category(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create("name", category={"say": "whaaat??"})

    def test_create_with_wrong_category_value(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = DatasetsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create("name", category="fake")

    # TODO write this test for CLI
    # def test_verify_datasets(self, mocker, empty_context,empty_cnvrg):
    #     empty_cnvrg._context = empty_context
    #     client = DatasetsClient(empty_cnvrg)
    #     mocker.patch.object(time, "sleep", return_value=None)
    #
    #     with mocker.patch.object(Dataset, "verify", return_value=True):
    #         assert client.verify_datasets(['test1', 'test2'])
    #
    #     with mocker.patch.object(Dataset, "verify", side_effect=[False, False, True, True]):
    #         assert client.verify_datasets(['test1', 'test2'])
    #
    #     with mocker.patch.object(Dataset, "verify", side_effect=[False, False, False, False, True, True]):
    #         assert client.verify_datasets(['test1', 'test2'])
    #
    #     with mocker.patch.object(Dataset, "verify", side_effect=[False, False, False, False]):
    #         mocker.patch.object(DatasetsClient, "seconds_diff", side_effect=[0, 1, 2])
    #         assert client.verify_datasets(['test1', 'test2'], 2) is False
    #
    #     x = mocker.patch.object(Dataset, "verify", side_effect=[False, False, True, False])
    #     mocker.patch.object(DatasetsClient, "seconds_diff", side_effect=[0, 1, 2])
    #     assert client.verify_datasets(['test1', 'test2'], 2) is False
    #     assert x.call_count == 4
    #
    #     with mocker.patch.object(Dataset, "verify", side_effect=[False, False, True, True]):
    #         mocker.patch.object(DatasetsClient, "seconds_diff", side_effect=[0, 1, 2])
    #         assert client.verify_datasets(['test1', 'test2'], 2) is True
