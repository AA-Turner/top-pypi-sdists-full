from .version import version as __version__


print(
    "Hud does not support this platform yet. The SDK has initiated a graceful shutdown. Your application remains unaffected. See the compatibility matrix for details: https://docs.hud.io/docs/hud-sdk-compatibility-matrix-for-python"
)


def init_session(*args, **kwargs):
    pass


def register(*args, **kwargs):
    pass


def init(*args, **kwargs):
    pass


def set_hook(*args, **kwargs):
    pass

def set_failure(*args, **kwargs):
    pass

def set_context(*args, **kwargs):
    pass

class RegisterConfig:
    def __init__(self, *args, **kwargs):
        pass


__all__ = [
    "__version__",
    "RegisterConfig",
    "init_session",
    "register",
    "init",
    "set_hook",
    "set_failure",
    "set_context",
]
