from . import (
    circular_algo,
    steady_algo,
    sticky_algo,
    stretched_algo,
    stretchedxtc_algo,
    tilted_algo,
    tiltedxtc_algo,
)
from ._hybrid_algo import hybrid_algo

for algo in (
    hybrid_algo(0, steady_algo, 1, circular_algo, 2),
    hybrid_algo(0, steady_algo, 1, sticky_algo, 2),
    hybrid_algo(0, steady_algo, 1, stretched_algo, 2),
    hybrid_algo(0, steady_algo, 1, stretchedxtc_algo, 2),
    hybrid_algo(0, steady_algo, 1, tilted_algo, 2),
    hybrid_algo(0, steady_algo, 1, tiltedxtc_algo, 2),
    hybrid_algo(0, tilted_algo, 1, circular_algo, 2),
    hybrid_algo(0, tiltedxtc_algo, 1, circular_algo, 2),
    hybrid_algo(0, circular_algo, 2, steady_algo, 3),
    hybrid_algo(0, circular_algo, 2, tilted_algo, 3),
    hybrid_algo(0, steady_algo, 2, tilted_algo, 3),
    hybrid_algo(0, steady_algo, 2, circular_algo, 3),
    hybrid_algo(0, tilted_algo, 2, steady_algo, 3),
    hybrid_algo(0, tilted_algo, 2, circular_algo, 3),
    hybrid_algo(0, steady_algo, 1, tilted_algo, 2, circular_algo, 3),
):
    locals()[algo.__name__] = algo
