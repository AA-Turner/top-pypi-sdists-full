import os
from pathlib import Path

import yaml
from donfig import Config

new_user_config_dir = Path("~/.config/arraylake").expanduser()

user_config_dir = Path(os.getenv("ARRAYLAKE_CONFIG", new_user_config_dir)).expanduser()
user_config_file = user_config_dir / "config.yaml"

fn = Path(__file__).resolve().parent / "config.yaml"
with fn.open() as f:
    defaults = yaml.safe_load(f)
config = Config("arraylake", paths=[user_config_dir], defaults=[defaults])

# maybe move a copy of the defaults to the user config space
config.ensure_file(
    source=fn,
    comment=True,
)


def default_service_uri() -> str:
    # default to using production service if service URI is not specified anywhere
    return config.get("service.uri", "https://api.earthmover.io")
