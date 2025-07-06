import pytest

from cnvrgv2.errors import CnvrgHttpError


class TestCompute:

    def test_get_create_pytorch_template(self, e2e_cluster):
        templates = e2e_cluster.templates
        new_kube_template = templates.create("pytourch_kube", 2, 2, type="pytorch", worker_num_executors=1,
                                             gpu=2.0, worker_labels="test_1=2,test_2=mock",
                                             worker_taints="test_1=2,cnvrg=kube")

        kube_template = templates.get(new_kube_template.slug)
        assert kube_template.title == "pytourch_kube"
        assert kube_template.cpu == 2
        assert kube_template.memory == 2

    def test_get_create_open_mpi_template(self, e2e_cluster):
        templates = e2e_cluster.templates
        new_kube_template = templates.create("mpi_kube", cpu=2, memory=2, gpu=1,
                                             labels="test_33=2,test_2=22", type="mpi", worker_num_executors=1,
                                             worker_cpu=2.0, worker_memory=2.0, worker_gpu=1, shm=2,
                                             worker_labels="test_1=2,test_2=mock", worker_taints="test_1=2,cnvrg=kube")
        kube_template = templates.get(new_kube_template.slug)
        assert kube_template.title == "mpi_kube"
        assert dict(kube_template.worker)['data']['attributes']['cpu'] == 2
        assert dict(kube_template.worker)['data']['attributes']['labels'] == 'test_1: 2, test_2: mock'
        assert dict(kube_template.worker)['data']['attributes']['gpu'] == 1
        assert dict(kube_template.worker)['data']['attributes']['memory'] == 2
        assert dict(kube_template.worker)['data']['attributes']['num_executors'] == 1
        assert kube_template.labels == "test_33: 2, test_2: 22"
        assert kube_template.cpu == 2
        assert kube_template.memory == 2
        assert kube_template.gpu == 1

    def test_get_create_ray_template(self, e2e_cluster):
        templates = e2e_cluster.templates
        new_kube_template = templates.create("ray_kube", cpu=2, memory=2, gpu=1,
                                             labels="test_33=2,test_2=22", type="ray", worker_num_executors=1,
                                             worker_cpu=2.0, worker_memory=2.0, worker_gpu=1, shm=2,
                                             worker_labels="test_1=2,test_2=mock", worker_taints="test_1=2,cnvrg=kube")
        kube_template = templates.get(new_kube_template.slug)

        assert kube_template.title == "ray_kube"
        assert dict(kube_template.worker)['data']['attributes']['cpu'] == 2
        assert dict(kube_template.worker)['data']['attributes']['labels'] == 'test_1: 2, test_2: mock'
        assert dict(kube_template.worker)['data']['attributes']['gpu'] == 1
        assert dict(kube_template.worker)['data']['attributes']['memory'] == 2
        assert dict(kube_template.worker)['data']['attributes']['num_executors'] == 1
        assert kube_template.labels == "test_33: 2, test_2: 22"
        assert kube_template.cpu == 2
        assert kube_template.memory == 2
        assert kube_template.gpu == 1

    def test_get_create_ray_modin_template(self, e2e_cluster):
        templates = e2e_cluster.templates
        new_kube_template = templates.create("ray_modin_kube", cpu=2, memory=2, gpu=1,
                                             labels="test_33=2,test_2=22", type="ray_modin", worker_num_executors=1,
                                             worker_cpu=2.0, worker_memory=2.0, worker_gpu=1, shm=2,
                                             worker_labels="test_1=2,test_2=mock", worker_taints="test_1=2,cnvrg=kube")
        kube_template = templates.get(new_kube_template.slug)

        assert kube_template.title == "ray_modin_kube"
        assert dict(kube_template.worker)['data']['attributes']['cpu'] == 2
        assert dict(kube_template.worker)['data']['attributes']['labels'] == 'test_1: 2, test_2: mock'
        assert dict(kube_template.worker)['data']['attributes']['gpu'] == 1
        assert dict(kube_template.worker)['data']['attributes']['memory'] == 2
        assert dict(kube_template.worker)['data']['attributes']['num_executors'] == 1
        assert kube_template.labels == "test_33: 2, test_2: 22"
        assert kube_template.cpu == 2
        assert kube_template.memory == 2
        assert kube_template.gpu == 1

    def test_get_create_spark_template(self, e2e_cluster):
        templates = e2e_cluster.templates
        spark_config = "spark.executor.memory=2\nspark.executor.cores=4\nspark.executor.instances=2"
        new_kube_template = templates.create("spark_kube", cpu=2, memory=2, gpu=1,
                                             labels="test_33=2,test_2=22", gaudi=2, huge_pages=500,
                                             type="spark_on_kubernetes",
                                             spark_config=spark_config)

        kube_template = templates.get(new_kube_template.slug)

        assert kube_template.title == "spark_kube"
        assert kube_template.labels == "test_33: 2, test_2: 22"
        assert kube_template.cpu == 2
        assert kube_template.memory == 2
        assert kube_template.gpu == 1
        assert kube_template.gaudi == 2
        assert kube_template.spark_config == spark_config

    def test_list_templates(self, e2e_cluster):
        templates_client = e2e_cluster.templates
        spark_config = "spark.executor.memory=2\nspark.executor.cores=4\nspark.executor.instances=2"
        spark_kube_template = templates_client.create("spark_kube", cpu=2, memory=2, gpu=1,
                                                      labels="test_33=2,test_2=22", gaudi=2, huge_pages=500,
                                                      type="spark_on_kubernetes",
                                                      spark_config=spark_config)

        ray_modin_kube_template = templates_client.create("ray_modin_kube", cpu=2, memory=2, gpu=1,
                                                          labels="test_33=2,test_2=22", type="ray_modin",
                                                          worker_num_executors=1,
                                                          worker_cpu=2.0, worker_memory=2.0, worker_gpu=1, shm=2,
                                                          worker_labels="test_1=2,test_2=mock",
                                                          worker_taints="test_1=2,cnvrg=kube")

        all_templates = [template.title for template in templates_client.list()]

        assert spark_kube_template.title in all_templates
        assert ray_modin_kube_template.title in all_templates

    def test_update_spark_template(self, e2e_cluster):
        templates = e2e_cluster.templates
        spark_config = "spark.executor.memory=2\nspark.executor.cores=4\nspark.executor.instances=2"
        new_spark_template = templates.create("spark_kube", cpu=2, memory=2, gpu=1,
                                              labels="test_33=2,test_2=22", gaudi=2, huge_pages=500,
                                              type="spark_on_kubernetes",
                                              spark_config=spark_config)

        kube_template = templates.get(new_spark_template.slug)
        assert kube_template.title == "spark_kube"
        assert kube_template.labels == "test_33: 2, test_2: 22"
        assert kube_template.cpu == 2
        assert kube_template.memory == 2
        assert kube_template.gpu == 1
        assert kube_template.gaudi == 2
        assert kube_template.spark_config == spark_config

        updated_spark_config = "spark.executor.memory=3\nspark.executor.cores=5\nspark.executor.instances=6"
        kube_template.update(title="spark_kube2", cpu=4, memory=4, gpu=2, labels="test_33=4,test_2=44", gaudi=4,
                             huge_pages=1000,
                             spark_config=updated_spark_config)

        assert kube_template.title == "spark_kube2"
        assert kube_template.labels == "test_33: 4, test_2: 44"
        assert kube_template.cpu == 4
        assert kube_template.memory == 4
        assert kube_template.gpu == 2
        assert kube_template.gaudi == 4
        assert kube_template.spark_config == updated_spark_config

    def test_update_empty_gpu_spark_template(self, e2e_cluster):
        templates = e2e_cluster.templates
        spark_config = "spark.executor.memory=2\nspark.executor.cores=4\nspark.executor.instances=2"
        new_spark_template = templates.create("spark_kube", cpu=2, memory=2, gpu=1,
                                              labels="test_33=2,test_2=22", gaudi=2, huge_pages=500,
                                              type="spark_on_kubernetes",
                                              spark_config=spark_config)

        kube_template = templates.get(new_spark_template.slug)
        assert kube_template.title == "spark_kube"
        assert kube_template.labels == "test_33: 2, test_2: 22"
        assert kube_template.cpu == 2
        assert kube_template.memory == 2
        assert kube_template.gpu == 1
        assert kube_template.gaudi == 2
        assert kube_template.spark_config == spark_config

        kube_template.update(title="spark_kube2", cpu=4, memory=4, gpu=0, labels="", gaudi=4,
                             huge_pages=1000,
                             spark_config="")
        assert kube_template.title == "spark_kube2"
        assert kube_template.labels is None
        assert kube_template.cpu == 4
        assert kube_template.memory == 4
        assert kube_template.gpu == 0
        assert kube_template.gaudi == 4
        assert kube_template.spark_config == ""

    def test_delete_spark_template(self, e2e_cluster):
        templates = e2e_cluster.templates
        spark_config = "spark.executor.memory=2\nspark.executor.cores=4\nspark.executor.instances=2"
        new_spark_template = templates.create("spark_kube", cpu=2, memory=2, gpu=1,
                                              labels="test_33=2,test_2=22", gaudi=2, huge_pages=500,
                                              type="spark_on_kubernetes",
                                              spark_config=spark_config)

        kube_template = templates.get(new_spark_template.slug)
        kube_template.delete()
        with pytest.raises(CnvrgHttpError) as exception_info:
            kube_template.title
        assert "Could not find compute" in str(exception_info.value)
