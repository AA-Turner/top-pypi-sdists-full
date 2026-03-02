import itertools as it
import sys

from . import circular_algo  # noqa: F401
from . import compressing_algo  # noqa: F401
from . import steady_algo  # noqa: F401
from . import sticky_algo  # noqa: F401
from . import stretched_algo  # noqa: F401
from . import stretchedxtc_algo  # noqa: F401
from . import tilted_algo  # noqa: F401
from . import tiltedxtc_algo  # noqa: F401
from ._hybrid_algo_prefab import (  # noqa: F401
    hybrid_0_steady_1_stretched_2_algo,
    hybrid_0_steady_1_stretchedxtc_2_algo,
    hybrid_0_steady_1_tiltedxtc_2_algo,
)
from ._hybrid_algo_prefab import hybrid_0_steady_1_tilted_2_algo  # noqa: F401
from ._primed_algo import primed_algo

# adapted from https://stackoverflow.com/a/4860414
this_module = sys.modules[__name__]
for pad, algo_name in it.product(
    (0, *map((1).__lshift__, range(2, 6))),
    (
        "circular_algo",
        "compressing_algo",
        "hybrid_0_steady_1_stretched_2_algo",
        "hybrid_0_steady_1_stretchedxtc_2_algo",
        "hybrid_0_steady_1_tilted_2_algo",
        "hybrid_0_steady_1_tiltedxtc_2_algo",
        "steady_algo",
        "sticky_algo",
        "stretched_algo",
        "stretchedxtc_algo",
        "tilted_algo",
        "tiltedxtc_algo",
    ),
):
    for lpad, rpad in set([(0, pad), (pad, 0)]):
        setattr(
            this_module,
            f"primed_{lpad}pad{rpad}_{algo_name}",
            primed_algo(
                algo=locals()[algo_name],
                lpad=lpad,
                rpad=rpad,
            ),
        )
