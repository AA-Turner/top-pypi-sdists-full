"""Spaces."""

from __future__ import annotations

import abc
import dataclasses
import uuid
from collections.abc import Iterable, Mapping
from typing import Literal, TypeAlias

import polars as pl
import pyarrow as pa
from typing_extensions import Self, deprecated

from corvic import embed, op_graph, orm, system
from corvic.model._feature_view import FeatureView, FeatureViewEdgeTableMetadata
from corvic.model._source import Source
from corvic.model._wrapped_proto import WrappedProto
from corvic.result import InvalidArgumentError, Ok
from corvic.table import Table
from corvic_generated.algorithm.graph.v1 import graph_pb2
from corvic_generated.model.v1alpha import models_pb2

SpaceID: TypeAlias = orm.SpaceID

_DEFAULT_CONCAT_SEPARATOR = " "


@dataclasses.dataclass(frozen=True)
class Space(WrappedProto[SpaceID, models_pb2.Space]):
    """Spaces apply embedding methods to FeatureViews.

    Example:
    >>> space = Space.node2vec(feature_view, dim=10, walk_length=10, window=10)
    """

    feature_view: FeatureView

    @classmethod
    @abc.abstractmethod
    def create(
        cls, feature_view: FeatureView, client: system.Client | None = None
    ) -> Ok[Self] | InvalidArgumentError: ...

    @abc.abstractmethod
    def embeddings_tables(self) -> Ok[Mapping[str, Table]] | InvalidArgumentError:
        """Generate per-ouput-source embeddings tables for this space."""

    @classmethod
    @deprecated("build a RelationalSpace instead")
    def node2vec(  # noqa: PLR0913
        cls,
        feature_view: FeatureView,
        *,
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
    ) -> embed.Node2Vec:
        """Run Node2Vec on the graph described by the feature view.

        Args:
            feature_view: The feature view to run Node2Vec on
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

        Returns:
            A Space
        """
        if not feature_view.relationships:
            raise InvalidArgumentError("Node2Vec requires some relationships")

        edge_tables = feature_view.output_edge_tables()
        if not edge_tables:
            raise InvalidArgumentError(
                "Node2Vec requires some with_sources to be output=True"
            )

        def edge_generator():
            for table in feature_view.output_edge_tables():
                edge_table_info = table.get_typed_metadata(FeatureViewEdgeTableMetadata)
                for batch in table.to_polars().unwrap_or_raise():
                    yield batch.with_columns(
                        pl.col(edge_table_info.start_source_column_name).alias(
                            "start_id"
                        ),
                        pl.lit(edge_table_info.start_source_name).alias("start_source"),
                        pl.col(edge_table_info.end_source_column_name).alias("end_id"),
                        pl.lit(edge_table_info.end_source_name).alias("end_source"),
                    ).select("start_id", "start_source", "end_id", "end_source")

        n2v_space = embed.Space(
            pl.concat((edge_list for edge_list in edge_generator()), rechunk=False),
            start_id_column_names=("start_id", "start_source"),
            end_id_column_names=("end_id", "end_source"),
            directed=True,
        )
        return embed.Node2Vec(
            space=n2v_space,
            dim=dim,
            walk_length=walk_length,
            window=window,
            p=p,
            q=q,
            alpha=alpha,
            min_alpha=min_alpha,
            negative=negative,
            seed=seed,
            batch_words=batch_words,
            workers=workers,
        )


@dataclasses.dataclass(frozen=True)
class Node2VecParameters:
    dim: int = 10
    walk_length: int = 10
    window: int = 10
    p: float = 1.0
    q: float = 1.0
    alpha: float = 0.025
    min_alpha: float = 0.0001
    negative: int = 5
    epochs: int = 10

    def to_proto(self) -> graph_pb2.Node2VecParameters:
        return graph_pb2.Node2VecParameters(
            ndim=self.dim,
            walk_length=self.walk_length,
            window=self.window,
            p=self.p,
            q=self.q,
            alpha=self.alpha,
            min_alpha=self.min_alpha,
            negative=self.negative,
            epochs=self.epochs,
        )


@dataclasses.dataclass(frozen=True)
class RelationalSpace(Space):
    """Spaces for embeddings that encode relationships."""

    node2vec_params: Node2VecParameters | None = None

    @classmethod
    def create(
        cls, feature_view: FeatureView, client: system.Client | None = None
    ) -> Ok[RelationalSpace] | InvalidArgumentError:
        if not feature_view.relationships:
            return InvalidArgumentError(
                "space will not be useful without at least one relationship"
            )
        if not feature_view.output_sources:
            return InvalidArgumentError(
                "space will not be useful without at least one output source"
            )
        proto_self = models_pb2.Space()
        client = client or feature_view.client

        return Ok(RelationalSpace(client, proto_self, SpaceID(), feature_view))

    def with_node2vec(self, params: Node2VecParameters):
        return dataclasses.replace(self, node2vec_params=params)

    def legacy_embeddings_table(self) -> Ok[Table] | InvalidArgumentError:
        if not self.node2vec_params:
            return InvalidArgumentError("space was not configured")

        def gen_edge_list_tables():
            for edge_table in self.feature_view.output_edge_tables():
                endpoint_metadata = edge_table.get_typed_metadata(
                    FeatureViewEdgeTableMetadata
                )
                yield op_graph.EdgeListTable(
                    table=edge_table.set_metadata({}).op_graph,
                    start_column_name=endpoint_metadata.start_source_column_name,
                    start_entity_name=endpoint_metadata.start_source_name,
                    end_column_name=endpoint_metadata.end_source_column_name,
                    end_entity_name=endpoint_metadata.end_source_name,
                )

        edge_list_tables = list(gen_edge_list_tables())
        if not edge_list_tables:
            return InvalidArgumentError(
                "no relationships given, or those given did not result in edges between"
                + "output sources"
            )
        return Ok(
            Table(
                self.client,
                op_graph.op.embed_node2vec_from_edge_lists(
                    edge_list_tables=edge_list_tables,
                    params=self.node2vec_params.to_proto(),
                ),
            )
        )

    def _split_embedding_table_by_source(
        self, embeddings_table: op_graph.Op
    ) -> Ok[Mapping[str, Table]] | InvalidArgumentError:
        match embeddings_table.unnest_struct("id"):
            case InvalidArgumentError() as err:
                return err
            case Ok(embeddings_table):
                pass
        id_fields = [
            field
            for field in embeddings_table.schema
            if field.name.startswith("column_")
        ]
        id_fields.sort(key=lambda field: int(field.name.removeprefix("column_")))
        source_name_column = id_fields[-1].name
        dtype_to_id_field = {field.dtype: field.name for field in id_fields[:-1]}

        result = dict[str, Table]()
        for source_id in self.feature_view.output_sources:
            source = self.feature_view.source_id_to_feature_view_source[
                source_id
            ].source
            primary_key_field = source.table.schema.get_primary_key()
            if primary_key_field is None:
                return InvalidArgumentError(
                    "source is required to have a primary key to be an output"
                )
            source_id_column = dtype_to_id_field[primary_key_field.dtype]
            table = Table(
                self.client,
                embeddings_table.filter_rows(
                    op_graph.row_filter.eq(source_name_column, source.name, pa.string())
                )
                .select_columns([source_id_column, "embedding"])
                .rename_columns({source_id_column: "entity_id"})
                .add_literal_column(
                    "source_id",
                    str(source_id),
                    pa.string(),
                )
                .unwrap_or_raise(),
            )
            result[source.name] = table

        return Ok(result)

    def embeddings_tables(self) -> Ok[Mapping[str, Table]] | InvalidArgumentError:
        return self.legacy_embeddings_table().and_then(
            lambda t: self._split_embedding_table_by_source(t.op_graph)
        )


@dataclasses.dataclass
class ConcatAndEmbedParameters:
    column_names: list[str]
    model_name: str
    tokenizer_name: str
    expected_vector_length: int
    expected_coordinate_bitwidth: Literal[32, 64] = 32


@dataclasses.dataclass(frozen=True)
class SemanticSpace(Space):
    """Spaces for embedding source properties."""

    output_sources: list[Source]
    concat_and_embed_params: ConcatAndEmbedParameters | None = None

    @classmethod
    def create(
        cls, feature_view: FeatureView, client: system.Client | None = None
    ) -> Ok[SemanticSpace] | InvalidArgumentError:
        client = client or feature_view.client
        if len(feature_view.output_sources) == 0:
            return InvalidArgumentError(
                "feature view must have at least one output source"
            )
        sources = [
            feature_view.source_id_to_feature_view_source[output_source].source
            for output_source in feature_view.output_sources
        ]

        proto_self = models_pb2.Space()
        return Ok(SemanticSpace(client, proto_self, SpaceID(), feature_view, sources))

    def with_concat_and_embed(self, params: ConcatAndEmbedParameters) -> SemanticSpace:
        return dataclasses.replace(self, concat_and_embed_params=params)

    def embeddings_tables(self) -> Ok[Mapping[str, Table]] | InvalidArgumentError:
        if not self.concat_and_embed_params:
            return InvalidArgumentError(
                "space was not configured to produce embeddings"
            )

        params: ConcatAndEmbedParameters = self.concat_and_embed_params
        combined_column_tmp_name = f"__concat-{uuid.uuid4()}"
        embedding_column_tmp_name = f"__embed-{uuid.uuid4()}"

        tables: Mapping[str, Table] = {}

        first_schema = self.output_sources[0].table.schema

        for output_source in self.output_sources:
            pk_field = output_source.table.schema.get_primary_key()
            if pk_field is None:
                return InvalidArgumentError("output source must have a primary key")

            if first_schema != output_source.table.schema:
                return InvalidArgumentError(
                    "schema for all output sources must be the same"
                )

            op = (
                output_source.table.op_graph.concat_string(
                    params.column_names,
                    combined_column_tmp_name,
                    _DEFAULT_CONCAT_SEPARATOR,
                )
                .and_then(
                    lambda t: t.embed_column(
                        combined_column_tmp_name,
                        embedding_column_tmp_name,
                        params.model_name,
                        params.tokenizer_name,
                        params.expected_vector_length,
                        params.expected_coordinate_bitwidth,
                    )
                )
                .and_then(
                    lambda t,
                    pk_field=pk_field,
                    output_source=output_source: t.select_columns(
                        [pk_field.name, embedding_column_tmp_name]
                    )
                    .rename_columns(
                        {
                            pk_field.name: "entity_id",
                            embedding_column_tmp_name: "embedding",
                        }
                    )
                    .add_literal_column(
                        "source_id",
                        str(output_source.id),
                        pa.string(),
                    )
                )
            )

            match op:
                case Ok(table):
                    pass
                case InvalidArgumentError() as err:
                    return err

            tables[output_source.name] = Table(self.client, table)

        return Ok(tables)


@dataclasses.dataclass
class EmbedAndConcatParameters:
    expected_vector_length: int


@dataclasses.dataclass(frozen=True)
class TabularSpace(Space):
    """Spaces for embedding source properties."""

    output_sources: list[Source]
    embed_and_concat_parameters: EmbedAndConcatParameters | None = None

    @classmethod
    def create(
        cls, feature_view: FeatureView, client: system.Client | None = None
    ) -> Ok[Self] | InvalidArgumentError:
        client = client or feature_view.client
        if len(feature_view.output_sources) == 0:
            return InvalidArgumentError(
                "feature view must have at least one output source"
            )
        sources = [
            feature_view.source_id_to_feature_view_source[output_source].source
            for output_source in feature_view.output_sources
        ]

        proto_self = models_pb2.Space()
        return Ok(cls(client, proto_self, SpaceID(), feature_view, sources))

    def with_embed_and_concat(self, params: EmbedAndConcatParameters) -> Self:
        return dataclasses.replace(self, embed_and_concat_parameters=params)

    def embeddings_tables(self) -> Ok[Mapping[str, Table]] | InvalidArgumentError:  # noqa: C901
        if not self.embed_and_concat_parameters:
            return InvalidArgumentError(
                "space was not configured to produce embeddings"
            )
        parameters = self.embed_and_concat_parameters

        tables: Mapping[str, Table] = {}
        first_schema = self.output_sources[0].table.schema

        for output_source in self.output_sources:
            pk_field = output_source.table.schema.get_primary_key()
            if not pk_field:
                return InvalidArgumentError("output source must have a primary key")

            if first_schema != output_source.table.schema:
                return InvalidArgumentError(
                    "schema for all output sources must be the same"
                )

            schema = output_source.table.op_graph.schema
            op = output_source.table.op_graph
            embedding_column_tmp_names: list[str] = []
            for column in schema:
                match column.ftype:
                    case op_graph.feature_type.Numerical():
                        encoded_column_name = f"__encoded-{uuid.uuid4()}"
                        embedding_column_tmp_names.append(encoded_column_name)
                        match op.encode_column(
                            column_name=column.name,
                            encoded_column_name=encoded_column_name,
                            encoder=op_graph.encoder.max_abs_scaler(),
                        ):
                            case Ok(op):
                                pass
                            case InvalidArgumentError() as err:
                                return err
                    case op_graph.feature_type.Categorical():
                        encoded_column_name = f"__encoded-{uuid.uuid4()}"
                        embedding_column_tmp_names.append(encoded_column_name)
                        match op.encode_column(
                            column_name=column.name,
                            encoded_column_name=encoded_column_name,
                            encoder=op_graph.encoder.one_hot_encoder(),
                        ):
                            case Ok(op):
                                pass
                            case InvalidArgumentError() as err:
                                return err

                    case _:
                        continue

            embedding_column_tmp_name = f"__embed-{uuid.uuid4()}"

            op = (
                op.concat_list(
                    column_names=embedding_column_tmp_names,
                    concat_list_column_name=embedding_column_tmp_name,
                )
                .and_then(
                    lambda t,
                    embedding_column_name=embedding_column_tmp_name: op_graph.op.coordinates_from_embedding(  # noqa: E501
                        table=t,
                        embedding_column_name=embedding_column_name,
                        output_dims=parameters.expected_vector_length,
                    )
                )
                .and_then(
                    lambda t,
                    pk_field=pk_field,
                    embedding_column_tmp_name=embedding_column_tmp_name,
                    output_source=output_source: t.select_columns(
                        [pk_field.name, embedding_column_tmp_name]
                    )
                    .update_feature_types(
                        {embedding_column_tmp_name: op_graph.feature_type.embedding()}
                    )
                    .rename_columns(
                        {
                            pk_field.name: "entity_id",
                            embedding_column_tmp_name: "embedding",
                        }
                    )
                    .add_literal_column(
                        "source_id",
                        str(output_source.id),
                        pa.string(),
                    )
                )
            )

            match op:
                case Ok(table):
                    pass
                case InvalidArgumentError() as err:
                    return err

            tables[output_source.name] = Table(self.client, table)

        return Ok(tables)


@dataclasses.dataclass
class EmbedImageParameters:
    column_name: str
    model_name: str
    expected_vector_length: int
    expected_coordinate_bitwidth: Literal[32, 64] = 32


@dataclasses.dataclass(frozen=True)
class ImageSpace(Space):
    """Spaces for embedding images."""

    output_source: Source
    embed_image_parameters: EmbedImageParameters | None = None

    def _sub_orm_objects(self, orm_object: orm.Space) -> Iterable[orm.Base]:
        return []

    @classmethod
    def create(
        cls, feature_view: FeatureView, client: system.Client | None = None
    ) -> Ok[Self] | InvalidArgumentError:
        client = client or feature_view.client
        if len(feature_view.output_sources) != 1:
            return InvalidArgumentError(
                "feature view must have exactly one output source"
            )
        source = feature_view.source_id_to_feature_view_source[
            next(iter(feature_view.output_sources))
        ].source

        proto_self = models_pb2.Space()
        return Ok(cls(client, proto_self, SpaceID(), feature_view, source))

    def with_embed_and_image(self, params: EmbedImageParameters) -> Self:
        return dataclasses.replace(self, embed_image_parameters=params)

    def embeddings_tables(self) -> Ok[Mapping[str, Table]] | InvalidArgumentError:
        if not self.embed_image_parameters:
            return InvalidArgumentError(
                "space was not configured to produce embeddings"
            )
        params: EmbedImageParameters = self.embed_image_parameters
        pk_field = self.output_source.table.schema.get_primary_key()
        if not pk_field:
            return InvalidArgumentError("output source must have a primary key")

        embedding_column_tmp_name = f"__embed-{uuid.uuid4()}"

        return (
            self.output_source.table.op_graph.embed_image_column(
                column_name=params.column_name,
                embedding_column_name=embedding_column_tmp_name,
                model_name=params.model_name,
                expected_vector_length=params.expected_vector_length,
                expected_coordinate_bitwidth=params.expected_coordinate_bitwidth,
            )
            .and_then(
                lambda t: t.select_columns([pk_field.name, embedding_column_tmp_name])
                .rename_columns(
                    {pk_field.name: "entity_id", embedding_column_tmp_name: "embedding"}
                )
                .add_literal_column(
                    "source_id",
                    str(self.output_source.id),
                    pa.string(),
                )
            )
            .map(lambda t: {self.output_source.name: Table(self.client, t)})
        )
