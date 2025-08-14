import pandas as pd

from gable.cli.helpers.data_asset_s3 import NativeS3Converter
from gable.cli.helpers.data_asset_s3.schema_profiler import (
    get_data_asset_field_profiles_for_data_asset,
)
from gable.openapi import (
    ResolvedDataAsset,
    S3SamplingParameters,
    SourceType,
    StructuredDataAssetResourceName,
)


def convert_dataframe_to_recap(path: str, dataframe: pd.DataFrame) -> dict:
    # Check if the dataframe is a Pandas DataFrame
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("Passed dataframe object is not a Pandas DataFrame")

    # Convert the DataFrame to a Recap StructType
    return NativeS3Converter().to_recap(dataframe, event_name=path)


def resolve_dataframe_data_asset(
    data_source: str,
    path: str,
    dataframe: pd.DataFrame,
    skip_profiling: bool = False,
) -> ResolvedDataAsset:
    """
    Get the schema and field profiles for a DataFrame data asset
    """
    # Convert the DataFrame to a Recap StructType
    recap_schema = convert_dataframe_to_recap(path, dataframe)

    # Get the number of fields in the data asset
    num_fields = len(recap_schema["fields"])

    # Generate the data profile if requested (and if there are fields to profile)
    if not skip_profiling and num_fields > 0:
        # Get the number of rows in the Dataframe to use for "sampling"
        num_rows = dataframe.shape[0]

        # Get the field profiles for the data asset
        data_profiles = get_data_asset_field_profiles_for_data_asset(
            recap_schema=recap_schema,
            file_to_obj={path: dataframe},
            event_name=path,
            sampling_params=S3SamplingParameters(rowSampleCount=num_rows),
        )
    else:
        data_profiles = None

    # Return the resolved data asset
    return ResolvedDataAsset(
        source_type=SourceType.dataframe,
        data_asset_resource_name=StructuredDataAssetResourceName(
            source_type=SourceType.dataframe, data_source=data_source, path=path
        ),
        schema=recap_schema,
        fieldNameToDataAssetFieldProfileMap=data_profiles,
    )
