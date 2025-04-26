import os

import dask.config
import yaml

fn = os.path.join(os.path.dirname(__file__), "coiled.yaml")

with open(fn) as f:
    defaults = yaml.safe_load(f)

dask.config.update_defaults(defaults)
