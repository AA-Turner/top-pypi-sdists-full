import os

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix='worker',
    root_path=os.path.dirname(f"{os.environ['HOME']}/worker/"),
    settings_files=['settings.toml'],
)
