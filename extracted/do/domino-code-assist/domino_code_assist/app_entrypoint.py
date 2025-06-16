import logging.config

import reacton

from .nb_app import NbApp

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(name)s %(message)s",
            "use_colors": None,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "WARNING", "propagate": False},
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


@reacton.component
def Page(handle_error=True):
    return NbApp(handle_error)


if __name__ == "__main__":
    import reacton

    reacton.render(Page(handle_error=False), handle_error=False)
