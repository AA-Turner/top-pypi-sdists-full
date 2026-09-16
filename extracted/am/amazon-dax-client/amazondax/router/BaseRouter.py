from abc import ABC, abstractmethod


class BaseRouter(ABC):
    ''' Abstract class that determines how the cluster routes requests. '''
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self, service_endpoints):
        pass

    @abstractmethod
    def wait_for_routes(self, min_healthy=1, leader_min=1, timeout=None):
        pass

    @abstractmethod
    def next_leader(self, prev_client):
        pass

    @abstractmethod
    def next_any(self, prev_client):
        pass
