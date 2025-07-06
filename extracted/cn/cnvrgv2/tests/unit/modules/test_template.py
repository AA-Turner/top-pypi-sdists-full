from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.resources.templates.kube_template import KubeTemplate
from cnvrgv2.proxy import Proxy


class MockResponse:
    def __init__(self, status, json):
        self.status_code = status
        self._json = json

    def json(self):
        return self._json


class TestResource:
    def test_update_template_with_fake_attribute(self, mocker, empty_context, empty_cnvrg):

        empty_cnvrg._context = empty_context
        mocker.patch.object(Proxy, 'call_api', side_effect=MockResponse(status=200, json={}))
        template = KubeTemplate(context=empty_context, slug="slug", attributes={"is_private": False})
        try:
            template.update(fake_attribute=2.0)
        except CnvrgArgumentsError as err:
            assert "Bad arguments: Faulty key fake_attribute" in str(err)
