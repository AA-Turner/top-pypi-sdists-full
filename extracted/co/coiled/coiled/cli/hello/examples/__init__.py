from .exit import exit
from .hello_world import hello_world
from .nyc_parquet import nyc_parquet
from .pytorch import pytorch
from .xarray_nwm import xarray_nwm

examples = {
    "hello-world": hello_world,
    "nyc-parquet": nyc_parquet,
    "xarray-nwm": xarray_nwm,
    "pytorch": pytorch,
    "exit": exit,
}
