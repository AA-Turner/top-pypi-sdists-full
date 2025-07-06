from cnvrgv2.context import Context


class MockResponse:
    def __init__(self, status, json):
        self.status_code = status
        self._json = json

    def json(self):
        return self._json


class TestCnvrg:
    def test_set_organization(self, mocker, empty_cnvrg):
        new_org = "new-org"
        mocker.patch.object(Context, "set_scope")

        assert empty_cnvrg._organization != new_org
        empty_cnvrg.set_organization(new_org)
        assert empty_cnvrg._organization == new_org
