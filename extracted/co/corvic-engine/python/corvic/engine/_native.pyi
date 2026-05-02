from typing import TypeAlias

import numpy as np
import numpy.typing as npt

NodeT: TypeAlias = np.uint32
NodeLikeT: TypeAlias = NodeT | int

class CSRGraph:
    def num_nodes(self) -> int: ...
    def has_edge(self, src: NodeLikeT, dst: NodeLikeT) -> bool: ...

def csr_from_edges(*, edges: npt.NDArray[NodeT], directed: bool) -> CSRGraph: ...

class Node2VecParams:
    def __init__(  # noqa: PLR0913
        self,
        *,
        p: float,
        q: float,
        start_alpha: float,
        end_alpha: float,
        window: int,
        batch_size: int,
        max_walk_length: int,
        num_negative: int,
        workers: int | None,
    ) -> None: ...
    @property
    def p(self) -> float: ...
    @property
    def q(self) -> float: ...
    @property
    def start_alpha(self) -> float: ...
    @property
    def end_alpha(self) -> float: ...
    @property
    def window(self) -> int: ...
    @property
    def batch_size(self) -> int: ...
    @property
    def max_walk_length(self) -> int: ...
    @property
    def num_negative(self) -> int: ...
    @property
    def workers(self) -> int | None: ...

def train_node2vec_epoch(
    *,
    graph: CSRGraph,
    params: Node2VecParams,
    embeddings: npt.NDArray[np.float32],
    hidden_layer: npt.NDArray[np.float32],
    next_random: np.uint64,
) -> None: ...
