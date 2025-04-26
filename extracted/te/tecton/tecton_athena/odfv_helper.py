import logging
from typing import Dict
from typing import List

import pandas

from tecton_core import feature_set_config
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.query.pandas import pipeline_helper
from tecton_proto.args.transformation__client_pb2 import TransformationMode


logger = logging.getLogger(__name__)

# Staging all of the following for deletion once Athena migration to querytree is complete


def get_odfvs_from_feature_set_config(feature_set_config: FeatureSetConfig):
    feature_set_items = feature_set_config.definitions_and_configs
    odfvs = [fd.feature_definition for fd in feature_set_items if fd.feature_definition.is_rtfv]
    return odfvs


def _extract_inputs_for_odfv_from_data(
    data_df: pandas.DataFrame, odfv: FeatureDefinitionWrapper
) -> Dict[str, pandas.DataFrame]:
    odfv_invocation_inputs = {}

    odfv_transformation_node = odfv.pipeline.root.transformation_node

    for input in odfv_transformation_node.inputs:
        input_name = input.arg_name
        input_df = None

        if input.node.HasField("request_data_source_node"):
            request_context_schema = input.node.request_data_source_node.request_context.tecton_schema
            request_context_fields = [c.name for c in request_context_schema.columns]

            for f in request_context_fields:
                if f not in data_df.columns:
                    msg = f"ODFV {odfv.name} has a dependency on the Request Data Source named '{input_name}'. Field {f} of this Request Data Source is not found in the spine. Available columns: {list(data_df.columns)}"
                    raise TectonValidationError(msg)

            input_df = data_df[request_context_fields]
        elif input.node.HasField("feature_view_node"):
            fv_features = feature_set_config.find_dependent_feature_set_items(
                odfv.fco_container, input.node, {}, odfv.id
            )[0]
            select_columns_and_rename_map = {}
            for f in fv_features.features:
                column_name = f"{fv_features.namespace}__{f}"
                mapped_name = f
                select_columns_and_rename_map[column_name] = mapped_name

            for f in select_columns_and_rename_map.keys():
                if f not in data_df.columns:
                    msg = f"ODFV {odfv.name} has a dependency on the Feature View '{input_name}'. Feature {f} of this Feature View is not found in the retrieved historical data. Available columns: {list(data_df.columns)}"
                    raise TectonValidationError(msg)
            # Let's select all of the features of the input FV from data_df
            input_df = data_df.rename(columns=select_columns_and_rename_map)[[*select_columns_and_rename_map.values()]]
        else:
            msg = f"Unexpected input found ({input_name}) on ODFV {odfv.name}"
            raise Exception(msg)

        odfv_invocation_inputs[input_name] = input_df

    return odfv_invocation_inputs


def _run_odfv(data_df: pandas.DataFrame, odfv: FeatureDefinitionWrapper) -> pandas.DataFrame:
    odfv_pipeline = pipeline_helper.build_odfv_execution_pipeline(
        pipeline=odfv.pipeline, transformations=odfv.transformations, name=odfv.name
    )
    if odfv.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PANDAS:
        odfv_inputs = _extract_inputs_for_odfv_from_data(data_df, odfv)
        odfv_result_df = odfv_pipeline.execute_with_inputs(odfv_inputs)
        return odfv_result_df
    elif odfv.transformation_mode == TransformationMode.TRANSFORMATION_MODE_PYTHON:
        odfv_inputs = _extract_inputs_for_odfv_from_data(data_df, odfv)

        # The inputs are currently a mapping of input_name to pandas DF
        # We need turn the ODFV inputs from a pandas DF to a list of dictionaries
        # Then we need to iterate through all rows of the input data set, pass the input dicts into the ODFV
        # And finally convert the resulting list of dicts into a pandas DF
        for input_name in odfv_inputs.keys():
            # Map pandas DFs to List of dicts (one dict per row)
            odfv_inputs[input_name] = odfv_inputs[input_name].to_dict("records")

        odfv_result_list = []

        num_rows = len(data_df)
        if num_rows > 100:
            logger.warn(
                f"Executing ODFV {odfv.name} for {len(data_df)} rows. The ODFV will be executed row by row and may take a while to complete..."
            )

        for row_index in range(num_rows):
            # Iterate through all rows of the data and invoke the ODFV
            row_odfv_inputs = {}
            for input_name in odfv_inputs.keys():
                row_odfv_inputs[input_name] = odfv_inputs[input_name][row_index]

            odfv_result_dict = odfv_pipeline.execute_with_inputs(row_odfv_inputs)
            odfv_result_list.append(odfv_result_dict)
        return pandas.DataFrame.from_dict(odfv_result_list)
    else:
        msg = f"ODFV {odfv.name} has an unexpected transformation mode: {odfv.transformation_mode}"
        raise TectonValidationError(msg)


def run_and_append_on_demand_features_to_historical_data(
    data_df: pandas.DataFrame, odfvs: List[FeatureDefinitionWrapper]
):
    for odfv in odfvs:
        odfv_result_df = _run_odfv(data_df, odfv)
        # We're performing an index based merge between the historical data and the ODFV results
        # That's safe to do because the ODFV function isn't expected to change the order of rows
        data_df = data_df.merge(odfv_result_df, left_index=True, right_index=True)
    return data_df
