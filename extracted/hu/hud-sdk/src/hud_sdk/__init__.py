from .version import version as __version__


print("Hud does not support this platform yet. The SDK has initiated a graceful shutdown. Your application remains unaffected. See the compatibility matrix for details: https://docs.hud.io/docs/hud-sdk-compatibility-matrix-for-python")


def init(*args, **kwargs):
    pass


def set_hook(*args, **kwargs):
    pass


def standby(*args, **kwargs):
    pass


def activate(*args, **kwargs):
    pass


__all__ = ["__version__", "set_hook", "init", "standby", "activate"]
