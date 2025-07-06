
class TestFlowVersion:
    # TODO: Add more tests probably?

    def test_get_flow_version_success(self, e2e_flow, e2e_flow_version):
        title = e2e_flow_version.title
        fv = e2e_flow.flow_versions.get(title)
        assert title == fv.title

    def test_list_flow_versions_success(self, e2e_flow):
        fvs = e2e_flow.flow_versions.list()
        assert len(list(fvs)) > 0

    def test_stop_flow_version_success(self, e2e_flow):
        complete_state = "completed"

        e2e_flow.run()
        fv = next(e2e_flow.flow_versions.list())
        fv.stop()
        fv.reload()

        assert fv.state == complete_state

    def test_info_flow_version_success(self, e2e_flow_version):
        fv_status = 'fv_status'
        info = e2e_flow_version.info()
        assert fv_status in info.keys()
