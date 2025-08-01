import logging
import math
from typing import TYPE_CHECKING, List, Optional, Sequence, Tuple

from _qwak_proto.qwak.ecosystem.v0.ecosystem_pb2 import AuthenticatedUnifiedUserContext
from _qwak_proto.qwak.feature_store.serving.serving_pb2 import (
    BatchFeature as ServingProtoBatchFeature,
    BatchV1Feature as ServingProtoBatchV1Feature,
    EntitiesHeader,
    EntityToFeatures,
    EntityValueRow,
    Feature as ServingProtoFeature,
    RequestedEntitiesMatrix,
    RequestedEntitiesMatrixRequest,
    RequestMetaData,
    StreamingAggregationFeature as ServingProtoStreamingAggregationFeature,
    StreamingFeature as ServingProtoStreamingFeature,
    StreamingV1Feature as ServingProtoStreamingV1Feature,
)
from _qwak_proto.qwak.feature_store.serving.serving_pb2_grpc import ServingServiceStub
from qwak.clients.administration.eco_system.client import EcosystemClient
from qwak.exceptions import QwakException
from qwak.feature_store._common.feature_set_utils import (
    BatchFeature,
    BatchFeatureV1,
    StreamingAggregationFeature,
    StreamingFeature,
    StreamingFeatureV1,
)
from qwak.feature_store.online import endpoint_utils
from qwak.feature_store.online.endpoint_utils import EndpointConfig
from qwak.inner.tool.grpc.grpc_tools import create_grpc_channel
from qwak.model.schema import ModelSchema
from qwak.model.schema_entities import BaseFeature, RequestInput

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    try:
        import pandas as pd
    except ImportError:
        pass


class OnlineClient:
    """
    Online Feature Serving client
    """

    def __init__(
        self,
        enable_ssl=True,
        endpoint_url: Optional[str] = None,
        metadata: Optional[Sequence[Tuple[str]]] = None,
    ):
        self._metadata = metadata
        self._enable_ssl = enable_ssl
        self._endpoint_url = endpoint_url

        options = (
            ("grpc.keepalive_timeout_ms", 1500),
            ("grpc.client_idle_timeout_ms", 60 * 1000),
        )

        if endpoint_url is None:
            user_context: AuthenticatedUnifiedUserContext = (
                EcosystemClient().get_authenticated_user_context().user
            )
            conf: EndpointConfig = endpoint_utils.get_config_by_account_type(
                user_context
            )
            endpoint_url = conf.endpoint_url
            if conf.enable_ssl is not None:
                enable_ssl = conf.enable_ssl

            if conf.metadata is not None:
                self._metadata = conf.metadata

        channel = create_grpc_channel(
            url=endpoint_url, enable_ssl=enable_ssl, options=options
        )

        self._serving_client: ServingServiceStub = ServingServiceStub(channel)

    @staticmethod
    def to_string_entities_values(values) -> List[str]:
        return [str(value) for value in values]

    def get_feature_values(
        self,
        schema: ModelSchema,
        df: "pd.DataFrame",
        model_name: str = "no-model",
        *,
        max_keys_per_request: int = 500,
    ) -> "pd.DataFrame":
        """
        :param schema: a ModelSchema object - defines the entities, features and prediction (irelevant in this case).
        :param df: a pandas data-frame with a column for each explicit feature needed
                         and a column for each entity key defined in the schema.
        :param model_name: the name of the model to retrieve the features for.
        :param max_keys_per_request: the maximum number of keys per request to the backend
        :return: a pandas data-frame - the feature values defined in the schema
                                       of the requested entities in the df.

        each row in the returned data-frame is constructed by retrieving the most recent requested feature values
        of the entity key(s) for the specific entity value(s) defined in the df.

        TODO: fix imports and align example
        Examples:
        >>> import pandas as pd
        >>> from qwak.feature_store import OnlineClient
        >>> from qwak.model.schema import (
        >>>     ModelSchema, FeatureStoreInput
        >>> )
        >>>
        >>> user_id = Entity(name='uuid', type=str)
        >>>
        >>> model_schema = ModelSchema(
        >>>     entities=[
        >>>         user_id
        >>>     ],
        >>>     inputs=[
        >>>         FeatureStoreInput(entity=user_id, name='user_purchases.number_of_purchases'),
        >>>         FeatureStoreInput(entity=user_id, name='user_purchases.avg_purchase_amount'),
        >>>     ],
        >>>     outputs=[
        >>>         InferenceOutput(name="score", type=float)
        >>>     ])
        >>>
        >>> online_client = OnlineClient()
        >>>
        >>> df = pd.DataFrame(columns=  ['uuid', 'explicit_feature_purchase_price'],
        >>>                   data   =  [ '1'  ,                22                ])
        >>>
        >>> user_features = online_client.get_feature_values(
        >>>                     model_schema,
        >>>                     df)
        >>>
        >>> print(user_features.head())
        >>>	#       user_purchases.number_of_purchases	user_purchases.avg_purchase_amount    otf_quad_price
        >>> # 0	                    76	                              4.796842                     484
        """
        try:
            import pandas as pd
        except ImportError:
            raise QwakException(
                "Missing Pandas dependency required for querying the online feature store"
            )

        (
            entity_features_compounds,
            entities_with_index,
            feature_set_names,
        ) = self._create_entity_and_features_sets(
            schema, pd.DataFrame(df.iloc[0]).transpose()
        )

        if not entity_features_compounds:
            df_result = pd.DataFrame(
                columns=[
                    input_field.name
                    for input_field in schema._inputs
                    if isinstance(input_field, BaseFeature)
                ]
            )

            return pd.concat([df, df_result], axis=1, join="inner")

        entities_to_features = []
        for entity_features_compound in entity_features_compounds.values():
            entities_to_features.append(
                EntityToFeatures(
                    features=entity_features_compound.features,
                    entity_name=entity_features_compound.entity_name,
                )
            )

        ordered_entities_tuple = sorted(
            entities_with_index, key=lambda entity: entity[1]
        )
        ordered_entities = [entity[0] for entity in ordered_entities_tuple]

        request_chunks: List[Tuple[RequestedEntitiesMatrix, pd.DataFrame]] = (
            OnlineClient._split_entities(
                entity_names=ordered_entities,
                population_df=df,
                max_entities_per_split=max_keys_per_request,
            )
        )

        results: List[pd.DataFrame] = []
        for matrix, population_df in request_chunks:
            request = RequestedEntitiesMatrixRequest(
                entity_values_matrix=matrix,
                entities_to_features=entities_to_features,
                request_meta_data=RequestMetaData(
                    model_name=model_name,
                    feature_set_names=list(feature_set_names),
                    num_keys=len(population_df),
                ),
            )
            try:
                response_df_json, _ = self._serving_client.GetMultiFeatures.with_call(
                    request, metadata=self._metadata
                )
                try:
                    # Try orjson first (fastest - 6x speedup)
                    import orjson

                    parsed_data = orjson.loads(response_df_json.pandas_df_as_json)
                    features_df: pd.DataFrame = pd.DataFrame(
                        data=parsed_data["data"],
                        columns=parsed_data["columns"],
                        index=parsed_data["index"],
                    )
                except ImportError:
                    # Fallback: Direct json.loads + DataFrame (2x speedup, no deps)
                    import json

                    parsed_data = json.loads(response_df_json.pandas_df_as_json)
                    features_df: pd.DataFrame = pd.DataFrame(
                        data=parsed_data["data"],
                        columns=parsed_data["columns"],
                        index=parsed_data["index"],
                    )
                results.append(
                    pd.concat(
                        [population_df.reset_index(drop=True), features_df],
                        axis=1,
                        join="inner",
                    )
                )
            except Exception as e:
                raise QwakException(
                    f"Failed to retrieve online feature values, got {repr(e)}"
                )

        res = pd.concat(results, axis=0)
        res.index = df.index
        return res

    @staticmethod
    def _split_entities(
        entity_names: List[str],
        population_df: "pd.DataFrame",
        max_entities_per_split: int,
    ) -> List[Tuple[RequestedEntitiesMatrix, "pd.DataFrame"]]:
        entity_values: List[List[str]] = population_df[entity_names].values.tolist()

        num_batches: int = math.ceil(len(entity_values) / max_entities_per_split)

        res: List[Tuple[RequestedEntitiesMatrix, pd.DataFrame]] = []
        for i in range(num_batches):
            curr_entities: List[List[str]] = entity_values[
                i * max_entities_per_split : (i + 1) * max_entities_per_split
            ]
            curr_population_df = population_df[
                i * max_entities_per_split : (i + 1) * max_entities_per_split
            ]
            curr_entity_rows: List[EntityValueRow] = [
                EntityValueRow(
                    index=idx, entity_values=OnlineClient.to_string_entities_values(v)
                )
                for idx, v in enumerate(curr_entities)
            ]

            res.append(
                (
                    RequestedEntitiesMatrix(
                        header=EntitiesHeader(entity_names=entity_names),
                        rows=curr_entity_rows,
                    ),
                    curr_population_df,
                )
            )
        return res

    @staticmethod
    def _create_entity_and_features_sets(schema: ModelSchema, df: "pd.DataFrame"):
        entity_features_compounds = {}
        list_of_df_columns = df.columns.to_list()
        entities_and_indexes = []
        feature_set_names = set()
        for entity in schema._entities:
            if entity.name not in df:
                logger.error(
                    f"Schema entity key '{entity.name}' does not exist in the request DataFrame"
                )
            else:
                entity_features_compounds[entity.name] = EntityFeaturesCompound(
                    entity.name, df[entity.name]
                )
                entities_and_indexes.append(
                    (entity.name, list_of_df_columns.index(entity.name))
                )

        for feature in [
            feature
            for feature in schema._inputs
            if not isinstance(feature, RequestInput)
        ]:
            if feature.entity.name not in entity_features_compounds:
                logger.info(
                    f"The entity: {feature.entity.name} of the Feature: {feature} does not exist in the entities list"
                )

            else:
                if isinstance(feature, BatchFeatureV1):
                    feature_proto = ServingProtoFeature(
                        batch_v1_feature=ServingProtoBatchV1Feature(name=feature.name)
                    )
                elif isinstance(feature, BatchFeature):
                    feature_proto = ServingProtoFeature(
                        batch_feature=ServingProtoBatchFeature(name=feature.name)
                    )
                elif isinstance(feature, StreamingFeature):
                    feature_proto = ServingProtoFeature(
                        streaming_feature=ServingProtoStreamingFeature(
                            name=feature.name
                        )
                    )
                elif isinstance(feature, StreamingFeatureV1):
                    feature_proto = ServingProtoFeature(
                        streaming_v1_feature=ServingProtoStreamingV1Feature(
                            name=feature.name
                        )
                    )
                elif isinstance(feature, StreamingAggregationFeature):
                    feature_proto = ServingProtoFeature(
                        streaming_aggregation=ServingProtoStreamingAggregationFeature(
                            name=feature.name
                        )
                    )
                else:
                    raise ValueError(
                        f"Not support type for feature extraction - {type(feature)}"
                    )

                entity_features_compounds[feature.entity.name].add_feature(
                    feature_proto
                )
                feature_set_names.add(feature.name.split(".")[0])

        return entity_features_compounds, entities_and_indexes, feature_set_names


class EntityFeaturesCompound:
    def __init__(self, entity_name, entity_value):
        self.entity_name = entity_name
        self.entity_value = entity_value
        self.features = []

    def add_feature(self, feature):
        self.features.append(feature)
