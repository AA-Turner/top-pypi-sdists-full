import pytest

from cnvrgv2.errors import CnvrgHttpError


class TestResources:
    def test_create_cluster_success(self, random_name, e2e_client):
        cluster_name = random_name(5)
        attributes = {
            "domain": "test-domain.cicd.cnvrg.me",
            "scheduler": "cnvrg_scheduler",
            "namespace": "test-namespace"
        }
        cluster = e2e_client.clusters.create(
            kube_config_yaml_path="assets/kube_config.yaml",
            resource_name=cluster_name,
            domain=attributes["domain"],
            scheduler=attributes["scheduler"],
            namespace=attributes["namespace"],
            https_scheme=True,
            persistent_volumes=True,
            gaudi_enabled=True
        )

        assert cluster.title == cluster_name
        assert cluster.domain == attributes["domain"]
        assert cluster.scheduler == attributes["scheduler"]
        assert cluster.namespace == attributes["namespace"]
        assert cluster.https_scheme is True
        assert cluster.persistent_volumes is True

    def test_update_cluster_success(self, random_name, e2e_client, e2e_cluster):
        cluster_name = random_name(5)
        attributes = {"domain": "test-domain.cicd.cnvrg.me",
                      "scheduler": "volcano",
                      "namespace": "test-namespace-new"}
        e2e_cluster.update(domain=attributes["domain"])
        e2e_cluster.reload()
        assert e2e_cluster.domain == attributes["domain"]

        e2e_cluster.update(resource_name=cluster_name, scheduler=attributes["scheduler"],
                           namespace=attributes["namespace"])
        e2e_cluster.reload()
        assert e2e_cluster.title == cluster_name
        assert e2e_cluster.scheduler == attributes["scheduler"]
        assert e2e_cluster.namespace == attributes["namespace"]

        e2e_cluster.update(https_scheme=True, persistent_volumes=True)
        e2e_cluster.reload()
        assert e2e_cluster.https_scheme is True
        assert e2e_cluster.persistent_volumes is True

    def test_delete_cluster_success(self, random_name, e2e_client, e2e_cluster):
        slug = e2e_cluster.slug
        e2e_cluster.delete()
        cluster = e2e_client.clusters.get(slug)
        with pytest.raises(CnvrgHttpError) as exception_info:
            cluster.title
        assert "The requested resource could not be found" in str(exception_info.value)
