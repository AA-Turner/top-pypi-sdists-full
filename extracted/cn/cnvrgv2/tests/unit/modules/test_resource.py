from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.resources.cluster import Cluster
from cnvrgv2.modules.resources.clusters_client import ClustersClient
from cnvrgv2.proxy import Proxy


class MockResponse:
    def __init__(self, status, json):
        self.status_code = status
        self._json = json

    def json(self):
        return self._json


class TestResource:
    def test_create_cluster_raise_onetype_error(self, mocker, empty_context, empty_cnvrg):

        empty_cnvrg._context = empty_context
        mocker.patch.object(Proxy, 'call_api', side_effect=MockResponse(status=200, json={}))
        client = ClustersClient(empty_cnvrg)
        try:
            client.create(build_yaml_path="fake1.yaml", kube_config_yaml_path="fake2.yaml")
        except CnvrgArgumentsError as err:
            assert "The given arguments: build_yaml_path and kube_config_yaml_path cannot be sent together" in str(err)

    def test_update_cluster_raise_NOFILE_error(self, mocker, empty_context, empty_cnvrg):

        empty_cnvrg._context = empty_context
        mocker.patch.object(Proxy, 'call_api', side_effect=MockResponse(status=200, json={}))
        cluster = Cluster(empty_cnvrg, slug="fake")
        try:
            cluster.update(kube_config_yaml_path="fake2.yaml")
        except CnvrgArgumentsError as err:
            assert "Bad arguments: File not found" in str(err)

    def test_delete_cluster_raise_slug_error(self, mocker, empty_context, empty_cnvrg):

        empty_cnvrg._context = empty_context
        client = ClustersClient(empty_cnvrg)
        try:
            client.delete(slug="")
        except CnvrgArgumentsError as err:
            assert "Bad arguments: Cannot get cluster with empty or a non string slug" in str(err)
