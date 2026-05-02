import os


class ClusterConfig:
    def __init__(self):
        self.cluster_name = None
        self.is_cluster = False
        self.__get_cluster_setting()

    def __get_cluster_setting(self):
        cluster_name = os.getenv("DAISY_CLUSTER_NAME", "")
        is_cluster = True if cluster_name else False

        self.cluster_name = cluster_name
        self.is_cluster = is_cluster


class PlatoConfig(object):
    def __init__(self):
        self.plato_install_path = os.getenv("PLATO_PATH", "")


plato_config = PlatoConfig()
