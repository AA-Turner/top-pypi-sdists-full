from base64 import b64encode
from typing import Any
from typing import Iterable
from typing import List
from typing import Union
from urllib.parse import urlencode

import pandas
from pyspark import sql as pyspark_sql

from tecton._internals import errors
from tecton._internals import ingest_utils
from tecton._internals import metadata_service
from tecton_core import feature_definition_wrapper
from tecton_core import id_helper
from tecton_core.conf import tecton_url
from tecton_core.errors import SCHEMA_VALIDATION_COLUMN_TYPE_MISMATCH_ERROR
from tecton_core.schema import Schema
from tecton_core.spark_type_annotations import is_pyspark_df
from tecton_proto.common import fco_locator__client_pb2 as fco_locator_pb2
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2
from tecton_proto.online_store import feature_value__client_pb2 as feature_value_pb2
from tecton_spark.schema_spark_utils import schema_from_spark


KEY_DELETION_MAX = 500000


def delete_keys(
    online: bool,
    offline: bool,
    keys: Union[pyspark_sql.DataFrame, pandas.DataFrame],
    feature_definition: feature_definition_wrapper.FeatureDefinitionWrapper,
) -> List[str]:
    if not offline and not online:
        raise errors.NO_STORE_SELECTED

    materialization_state_transitions = feature_definition.fv_spec.materialization_state_transitions
    if offline and any(transition.offline_enabled for transition in materialization_state_transitions):
        if not feature_definition.offline_store_config.HasField("delta"):
            raise errors.OFFLINE_STORE_NOT_SUPPORTED

    if online and all(not transition.online_enabled for transition in materialization_state_transitions):
        print("Online materialization was never enabled. No data to be deleted in online store.")
        online = False

    if offline and all(not transition.offline_enabled for transition in materialization_state_transitions):
        print("Offline materialization was never enabled. No data to be deleted in offline store.")
        offline = False

    if not (offline or online):
        return None

    if not (is_pyspark_df(keys) or isinstance(keys, pandas.DataFrame)):
        raise errors.INVALID_JOIN_KEY_TYPE(type(keys))
    _validate_entity_deletion_keys_dataframe(
        df=keys, join_keys=feature_definition.join_keys, view_schema=feature_definition.view_schema
    )

    keys = keys if isinstance(keys, pandas.DataFrame) else keys.toPandas()
    keys = keys.drop_duplicates()
    info_response = _get_delete_entities_info(feature_definition.id)
    s3_path = info_response.df_path
    offline_join_keys_path = s3_path + "/offline"
    online_join_keys_path = s3_path + "/online"
    # TODO(TEC-17028): Only upload entity keys once.
    if online:
        join_key_df = _serialize_join_keys(keys, feature_definition.join_keys)
        ingest_utils.upload_df_pandas(info_response.signed_url_for_df_upload_online, join_key_df, parquet=False)
    if offline:
        ingest_utils.upload_df_pandas(info_response.signed_url_for_df_upload_offline, keys)

    return _send_deletion_request(feature_definition, online, offline, online_join_keys_path, offline_join_keys_path)


def _send_deletion_request(
    feature_definition: feature_definition_wrapper.FeatureDefinitionWrapper,
    online: bool,
    offline: bool,
    online_join_keys_path: str,
    offline_join_keys_path: str,
) -> List[str]:
    deletion_request = metadata_service_pb2.DeleteEntitiesRequest(
        fco_locator=fco_locator_pb2.FcoLocator(
            id=id_helper.IdHelper.from_string(feature_definition.id), workspace=feature_definition.workspace
        ),
        online=online,
        offline=offline,
        online_join_keys_full_path=online_join_keys_path,
        offline_join_keys_path=offline_join_keys_path,
    )
    delete_entities_response = metadata_service.instance().DeleteEntities(deletion_request)
    url = f"{tecton_url()}/app/jobs?" + urlencode(
        {
            "workspaces": feature_definition.workspace,
            "task_type": "Deletion",
            "feature_views": feature_definition.name,
        }
    )
    print(f"Deletion occurs asynchronously. View the status of the completion job at {url}")
    return list(delete_entities_response.job_ids)


def _get_delete_entities_info(string_id: str) -> metadata_service_pb2.GetDeleteEntitiesInfoResponse:
    info_request = metadata_service_pb2.GetDeleteEntitiesInfoRequest(
        feature_definition_id=id_helper.IdHelper.from_string(string_id),
    )
    return metadata_service.instance().GetDeleteEntitiesInfo(info_request)


def _serialize_join_keys(join_keys_df: pandas.DataFrame, join_keys: List[str]) -> pandas.DataFrame:
    def _serialize_fn(items: Iterable[Any]) -> str:
        ret = feature_value_pb2.FeatureValueList()
        for item in items:
            if isinstance(item, int):
                ret.feature_values.add().int64_value = item
            elif isinstance(item, str):
                ret.feature_values.add().string_value = item
            elif item is None:
                ret.feature_values.add().null_value.CopyFrom(feature_value_pb2.NullValue())
            else:
                msg = f"Unknown type: {type(item)}"
                raise Exception(msg)
        return b64encode(ret.SerializeToString()).decode()

    keys_df = join_keys_df[join_keys]
    return keys_df.apply(lambda row: _serialize_fn(tuple(row)), axis=1).to_frame(name="join_keys_array")


def _validate_entity_deletion_keys_dataframe(
    df: Union[pyspark_sql.DataFrame, pandas.DataFrame], join_keys: List[str], view_schema: Schema
) -> None:
    if len(set(df.columns)) != len(df.columns):
        raise errors.DUPLICATED_COLS_IN_KEYS(", ".join(list(df.columns)))

    row_count = df.count() if is_pyspark_df(df) else len(df)
    if row_count > KEY_DELETION_MAX:
        raise errors.TOO_MANY_KEYS(KEY_DELETION_MAX)
    if row_count == 0:
        msg = "keys"
        raise errors.EMPTY_ARGUMENT(msg)

    if set(df.columns) != set(join_keys):
        raise errors.INCORRECT_KEYS(", ".join(list(df.columns)), ", ".join(join_keys))

    # We skip schema validation for Pandas DataFrames since there is no reliable way to map Pandas types to Tecton types yet.
    if is_pyspark_df(df):
        df_columns = schema_from_spark(df.schema).column_name_and_data_types()
        fv_columns = view_schema.column_name_and_data_types()
        for df_column in df_columns:
            if df_column not in fv_columns:
                raise SCHEMA_VALIDATION_COLUMN_TYPE_MISMATCH_ERROR(
                    [(df_column[0], next(x for x in fv_columns if x[0] == df_column[0])[1], df_column[1])]
                )
