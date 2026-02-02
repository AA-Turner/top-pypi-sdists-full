"""Node2Vec embeddings."""

from __future__ import annotations

import functools
from collections.abc import Hashable, Mapping, Sequence
from typing import Any

import numpy as np
import numpy.typing as npt
import polars as pl
from tqdm.auto import trange
from typing_extensions import deprecated

from corvic import engine
from corvic.result import InvalidArgumentError

_MAX_SENTENCE_LEN = 10000


class KeyedVectors:
    """Vectors whose entries are keyed by an arbitrary value.

    Used to represent embeddings.

    Because struct fields have no natural order, key indexing is performed with
    respect to a tuple constructed from struct fields in key_columns order.
    """

    _vectors: npt.NDArray[np.float32]
    _index_to_key: pl.Series
    _key_field_order: Sequence[str]

    def __init__(
        self, *, dim: int, index_to_key: pl.Series, key_field_order: Sequence[str]
    ):
        """Create keyed vectors.

        Args:
          dim: dimension of vectors
          key_to_index: mapping of key struct to index
          index_to_key: mapping of index to key struct
          key_field_order: order of key struct fields used for index operations
        """
        self.dim = dim
        self._index_to_key = index_to_key
        self._key_field_order = key_field_order
        self._vectors = self._initial_vectors(len(index_to_key), dim)

    @classmethod
    def _initial_vectors(cls, nrows: int, dim: int):
        rng = np.random.default_rng()
        vectors = rng.random((nrows, dim), dtype=np.float32)
        vectors *= 2.0
        vectors -= 1.0
        vectors /= dim
        return vectors

    def __len__(self):
        """Return the number of keys."""
        return self._index_to_key.len()

    @deprecated("use to_polars instead")
    def __getitem__(self, key: Any) -> npt.NDArray[np.float32]:
        """Return vector for key."""
        return self.vectors[self.key_to_index[self.make_key(key)]]  # pyright: ignore[reportDeprecated]

    @deprecated("use to_polars instead")
    def make_key(
        self, obj: dict[str, Hashable] | list[Hashable] | tuple[Hashable] | Hashable
    ) -> Hashable:
        """Return a key appropriate for use with key_to_index."""
        if isinstance(obj, dict):
            return tuple(obj[field_name] for field_name in self._key_field_order)
        if isinstance(obj, list):
            return tuple(elem for elem in obj)
        return (obj,)

    @functools.cached_property
    @deprecated("use to_polars instead")
    def key_to_index(self) -> Mapping[Hashable, int]:
        """Return a mapping from keys to index.

        See make_key to create the expected key object.
        """
        return {
            tuple(names[field_name] for field_name in self._key_field_order): i
            for i, names in enumerate(self._index_to_key)
        }

    @property
    @deprecated("use to_polars instead")
    def index_to_key(self) -> pl.Series:
        """Return a mapping from index to key."""
        return self._index_to_key

    def to_polars(
        self,
        *,
        id_column_name: str = "id",
        embedding_column_name: str = "embedding",
        flatten_single_field: bool = False,
    ) -> pl.DataFrame:
        """Return embedding as a polars DataFrame."""
        if self._vectors.shape[0] == 0:
            polars_df = pl.DataFrame(
                schema={
                    id_column_name: self._index_to_key.dtype,
                    embedding_column_name: pl.List(inner=pl.Float32),
                },
            )
        else:
            polars_df = pl.select(
                self._index_to_key.alias(id_column_name),
                pl.Series(self._vectors, dtype=pl.List(inner=pl.Float32)).alias(
                    embedding_column_name
                ),
            )
        if flatten_single_field and len(self._key_field_order) == 1:
            polars_df = polars_df.unnest(id_column_name).rename(
                {self._key_field_order[0]: id_column_name}
            )
        return polars_df

    @property
    def vectors(self) -> npt.NDArray[np.float32]:
        """Return raw vectors keyed by index space.

        Use to_polars to retrieve vectors by original key.
        """
        return self._vectors


class Space:
    """A feature space, i.e., a graph."""

    graph: engine.CSRGraph
    _index_to_key: pl.Series
    _node_ids: list[str]

    def __init__(
        self,
        edges: pl.DataFrame,
        *,
        start_id_column_names: Sequence[str] | None = None,
        end_id_column_names: Sequence[str] | None = None,
        directed: bool = True,
    ):
        """Create a space from a table of edges.

        By default, assume that the first column is the start id (source) of an edge
        and the second column is the end id (destination) of an edge.

        If the start or end of an edge is identified by a combination of columns,
        use start_id_column_names and end_id_column_names.

        Args:
          edges: table of edges where each row is an edge
          start_id_column_names: names of columns in edges table corresponding
            to start (or source) of an edge.
          end_id_column_names: names of columns in edges table corresponding
            to end (or destination) of an edge
          directed: if edges should be considered directeds
        """
        if len(edges.columns) < 2:  # noqa: PLR2004
            raise InvalidArgumentError("edges should have at least two columns")

        start_id_column_names = start_id_column_names or [edges.columns[0]]
        end_id_column_names = end_id_column_names or [edges.columns[1]]
        if len(start_id_column_names) != len(end_id_column_names):
            raise InvalidArgumentError("unequal number of id columns")

        edge_starts = edges.select(pl.col(start_id_column_names))
        edge_ends = edges.select(pl.col(end_id_column_names))

        self._node_ids = [f"column_{idx}" for idx in range(len(start_id_column_names))]
        edge_starts_by_node_id = (
            edge_starts.with_columns(
                pl.col(name).alias(f"column_{idx}")
                for idx, name in enumerate(start_id_column_names)
            )
            .select(self._node_ids)
            .with_row_index("index")
            .with_columns(pl.lit(0).alias("side"))
        )
        edge_ends_by_node_id = (
            edge_ends.with_columns(
                pl.col(name).alias(f"column_{idx}")
                for idx, name in enumerate(end_id_column_names)
            )
            .select(self._node_ids)
            .with_row_index("index")
            .with_columns(pl.lit(1).alias("side"))
        )

        # Not strictly necessary, but preserve locality of ID space by following
        # edge "iteration" order
        endpoints = (
            pl.concat([edge_starts_by_node_id, edge_ends_by_node_id], rechunk=False)
            .sort(["index", "side"])
            .select(self._node_ids)
            .unique(maintain_order=True, keep="first")
        )

        nodes = endpoints.with_row_index(name="index").with_columns(
            pl.col("index").cast(pl.UInt32), pl.struct(self._node_ids).alias("id")
        )

        if len(edges):
            edge_starts_by_index = (
                edge_starts.join(
                    nodes,
                    left_on=start_id_column_names,
                    right_on=self._node_ids,
                    how="left",
                    join_nulls=True,
                )
                .select(["index"])
                .rename({"index": "start"})
            )
            edge_ends_by_index = (
                edge_ends.join(
                    nodes,
                    left_on=end_id_column_names,
                    right_on=self._node_ids,
                    how="left",
                    join_nulls=True,
                )
                .select(["index"])
                .rename({"index": "end"})
            )
            edge_array = pl.concat(
                [edge_starts_by_index, edge_ends_by_index], how="horizontal"
            ).to_numpy()
        else:
            edge_array = np.empty((0, 2), dtype=np.uint32)

        self.directed = directed
        self.graph = engine.csr_from_edges(edges=edge_array, directed=directed)
        self._index_to_key = nodes["id"]

    def make_keyed_vectors(self, dim: int) -> KeyedVectors:
        """Make keyed vectors appropriate to the space."""
        return KeyedVectors(
            dim=dim, index_to_key=self._index_to_key, key_field_order=self._node_ids
        )


class Node2Vec:
    """Node to vector algorithm."""

    _params: engine.Node2VecParams
    _keyed_vectors: KeyedVectors
    _space: Space
    # TODO(ddn): Use seed
    _seed: int | None

    _syn1neg: npt.NDArray[np.float32] | None

    def __init__(  # noqa: PLR0913
        self,
        space: Space,
        dim: int,
        walk_length: int,
        window: int,
        p: float = 1.0,
        q: float = 1.0,
        batch_words: int | None = None,
        alpha: float = 0.025,
        seed: int | None = None,
        workers: int | None = None,
        min_alpha: float = 0.0001,
        negative: int = 5,
    ):
        """Create a new instance of Node2Vec.

        Args:
            space: Graph object whose nodes are to be embedded.
            dim: The dimensionality of the embedding
            walk_length: Length of the random walk to be computed
            window: Size of the window. This is half of the context,
                as the context is all nodes before `window` and
                after `window`.
            p: The higher the value, the lower the probability to return to
                the previous node during a walk.
            q: The higher the value, the lower the probability to return to
                a node connected to a previous node during a walk.
            alpha: Initial learning rate
            min_alpha: Final learning rate
            negative: Number of negative samples
            seed: Random seed
            batch_words: Target size (in nodes) for batches of examples passed
                to worker threads
            workers: Number of threads to use. Default is to select number of threads
                as needed. Setting this to a non-default value incurs additional
                thread pool creation overhead.
        """
        batch_words = batch_words or _MAX_SENTENCE_LEN
        self._params = engine.Node2VecParams(
            p=p,
            q=q,
            start_alpha=alpha,
            end_alpha=min_alpha,
            window=window,
            batch_size=batch_words // (walk_length or 1),
            num_negative=negative,
            max_walk_length=walk_length,
            workers=workers,
        )

        self._space = space
        self._keyed_vectors = space.make_keyed_vectors(dim)

        self._seed = seed
        self._layer1_size = dim

        self._syn1neg = None

        self._syn1neg = np.zeros(
            (len(self._keyed_vectors), self._layer1_size), dtype=np.float32
        )

    def train(
        self,
        *,
        epochs: int,
        verbose: bool = True,
    ):
        """Train the model and compute the node embedding.

        Args:
            epochs: Number of epochs to train the model for.
            verbose: Whether to show loading bar.
        """
        assert self._syn1neg is not None

        for _ in trange(
            epochs,
            dynamic_ncols=True,
            desc="Epochs",
            leave=False,
            disable=not verbose,
        ):
            gen = np.random.Generator(np.random.get_bit_generator())
            next_random = gen.integers(  # pyright: ignore[reportUnknownMemberType]
                np.int32(2**31 - 1), dtype=np.int32
            )
            engine.train_node2vec_epoch(
                graph=self._space.graph,
                params=self._params,
                embeddings=self._keyed_vectors.vectors,
                hidden_layer=self._syn1neg,
                next_random=np.uint64(next_random),
            )

    @property
    def wv(self) -> KeyedVectors:
        """Return computed embeddings."""
        return self._keyed_vectors
