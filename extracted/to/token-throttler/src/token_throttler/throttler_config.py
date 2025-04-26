import warnings
from typing import Any, Dict, Union


class Singleton(type):  # pragma: no cover
    instances: dict = {}

    def __call__(cls, *args, **kwargs) -> None:
        if cls not in cls.instances:
            cls.instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instances[cls]


class ConfigOptions:
    ENABLE_THREAD_LOCK: bool = False
    IDENTIFIER_FAIL_SAFE: bool = False


class ThrottlerConfig(ConfigOptions):
    def __init__(self, config: Union[Dict, None] = None) -> None:
        for key, value in self.__dict__.items():  # pragma: no cover
            if not key.startswith("__") and not key.endswith("__"):
                self.__dict__[key] = value
        if config is not None:
            self.set(config)

    def _configure(self, config: Dict) -> None:
        for key, value in config.items():
            if not hasattr(self, key):
                return
            attr: Any = getattr(self, key)
            if type(attr) is not type(value):
                raise TypeError(f"Invalid type for configuration parameter `{key}`")
            setattr(self, key, value)

    def set(self, config: Dict) -> None:
        if config is None or not config:
            raise ValueError(f"Invalid configuration provided: {config}")
        if not isinstance(config, Dict):
            raise TypeError(
                f"Invalid configuration input. Expected <class 'dict'>, got {type(config)}"
            )
        self._configure(config)
        return


class ThrottlerConfigGlobal(ThrottlerConfig, metaclass=Singleton):
    def __init__(self, config: Union[Dict, None] = None) -> None:
        super().__init__(config)

    def __setattr__(self, name, value):  # pragma: no cover
        if hasattr(self, name):
            warnings.warn(
                f"Modifying attribute '{name}' of {self.__class__.__name__}.",
                RuntimeWarning,
            )
            super().__setattr__(name, value)


default_config: ThrottlerConfigGlobal = ThrottlerConfigGlobal()
