from fa_purity import (
    Cmd,
)
from fluidattacks_utils_logger import (
    set_main_log,
)
from fluidattacks_utils_logger.env import (
    current_app_env,
    observes_debug,
)
from fluidattacks_utils_logger.handlers import (
    LoggingConf,
)


def set_logger(root_name: str, version: str) -> Cmd[None]:
    app_env = current_app_env()
    debug = observes_debug()
    conf = app_env.map(
        lambda env: LoggingConf(
            app_name="observes",
            app_type="common",
            app_version=version,
            release_stage=env,
        ),
    )
    return debug.bind(lambda d: conf.bind(lambda c: set_main_log(root_name, c, d)))
