import abc


class Env(abc.ABC):
    @abc.abstractmethod
    def step(self, action):
        pass

    @abc.abstractmethod
    def reset(self, seed: int | None = None):
        pass
