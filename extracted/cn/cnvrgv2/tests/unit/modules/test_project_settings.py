from cnvrgv2.proxy import Proxy
from cnvrgv2.modules.project import Project
from cnvrgv2.modules.project_settings import ProjectSettings


class TestProjectSettings:

    def test_save_project_settings(self, mocker, empty_context):
        project = Project(context=empty_context, slug="fake-slug")
        project_settings = ProjectSettings(project=project)

        mocked_save = mocker.patch.object(Proxy, 'call_api')
        project_settings.save()
        assert mocked_save.call_count == 1
