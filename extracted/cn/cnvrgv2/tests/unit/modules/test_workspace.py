from cnvrgv2.modules.workflows.workspace.workspace import Workspace


class TestWorkspace:
    def test_offline_workspace_restart_attribute(self, empty_context):
        try:
            w = Workspace(context=empty_context, slug="end-slug", attributes={'status': 'offline'})
            w.restart()
        except AttributeError as err:
            assert "'Workspace' object has no attribute 'restart'" in str(err)
