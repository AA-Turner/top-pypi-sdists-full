# Redis Connection Utility
#
# This module contains a class used to get Redis Connection

from rediscluster import StrictRedisCluster


class RedisUtil:

    def __init__(self, host, port, password=None):
        self.redis_host = host
        self.redis_port = port
        self.redis_password = password
        self.connection = None

    def get_connection(self):

        if self.connection is None:

            startup_nodes = [{"host": self.redis_host, "port": self.redis_port}]

            conn_config = {"startup_nodes": startup_nodes,
                           "decode_responses": True,
                           "skip_full_coverage_check": True,
                           }

            if self.redis_password is not None:
                conn_config.update(ssl=True, password=self.redis_password)

            self.connection = StrictRedisCluster(**conn_config)

        return self.connection
