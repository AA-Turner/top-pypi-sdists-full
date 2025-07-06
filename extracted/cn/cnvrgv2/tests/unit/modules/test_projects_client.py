import pytest

from cnvrgv2.proxy import Proxy
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.project import Project
from cnvrgv2.modules.projects_client import ProjectsClient
from cnvrgv2.utils.json_api_format import JAF


class TestProjectsClient:
    def test_init_no_credentials(self):
        with pytest.raises(CnvrgArgumentsError):
            ProjectsClient(None)

    def test_init_valid_credentials(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = ProjectsClient(empty_cnvrg)
        assert client._context
        assert client._route

    def test_get_with_slug(self, mocker, empty_context, empty_cnvrg):
        slug = "test-slug"

        def mock_call_api(*args, **kwargs):
            response = {
                "data": {
                    "id": "17",
                    "type": "project",
                    "attributes": {
                        "title": "test-title",
                        "slug": slug,
                        "git": False,
                        "start_commit": "b6692ea5df920cad691c20319a6fffd7a4a766b8",
                        "commit": "5b384ce32d8cdef02bc3a139d4cac0a22bb029e8"
                    }
                }
            }
            return JAF(response=response)

        mocked_api_call = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        empty_cnvrg._context = empty_context
        client = ProjectsClient(empty_cnvrg)
        model = client.get(slug)

        # The function will not be called on init since its lazy-loading
        assert mocked_api_call.call_count == 0

        # The function will not be called on init since its lazy-loading
        assert model.title == "test-title"
        assert mocked_api_call.call_count > 0

        assert type(model) is Project

    def test_get_with_empty_slug(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = ProjectsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.get("")

    def test_get_with_none_slug(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = ProjectsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.get(None)

    def test_get_with_wrong_type_slug(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = ProjectsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.get({"say": "whaaat??"})

    def test_valid_create(self, mocker, empty_context, empty_cnvrg):
        def mock_call_api(*args, **kwargs):
            response = {
                "data": {
                    "id": "17",
                    "type": "project",
                    "attributes": {
                        "title": "test-title",
                        "slug": "test-slug",
                        "git": False,
                        "start_commit": "b6692ea5df920cad691c20319a6fffd7a4a766b8",
                        "commit": "5b384ce32d8cdef02bc3a139d4cac0a22bb029e8"
                    }
                }
            }
            return JAF(response=response)

        mocked_api_call = mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        empty_cnvrg._context = empty_context
        client = ProjectsClient(empty_cnvrg)
        model = client.create("test-title")

        # TODO: add attribute checks. added call_count until decided what to check
        assert type(model) is Project
        assert mocked_api_call.call_count > 0

    def test_create_with_empty_name(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = ProjectsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create("")

    def test_create_with_none_name(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = ProjectsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create(None)

    def test_create_with_wrong_type_name(self, empty_context, empty_cnvrg):
        empty_cnvrg._context = empty_context
        client = ProjectsClient(empty_cnvrg)
        with pytest.raises(CnvrgArgumentsError):
            client.create({"say": "whaaat??"})
