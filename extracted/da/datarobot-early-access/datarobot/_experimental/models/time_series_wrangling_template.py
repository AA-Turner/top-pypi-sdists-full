from typing import Optional
import uuid

import datarobot as dr
from datarobot import DataStore, UseCase
from datarobot._experimental.models.time_series_transformation_plan import (
    InputParameters,
    TimeSeriesTransformationPlan,
)
from datarobot.enums import DataWranglingDataSourceTypes, DataWranglingDialect
from datarobot.models.dataset import Dataset
from datarobot.models.recipe import DatasetInput, DataSourceInput, Recipe
from datarobot.models.recipe_operation import (
    DatetimeSamplingOperation,
    RandomSamplingOperation,
    TimeSeriesOperation,
)
from datarobot.rest import RESTClientObject


def associate_credentials_with_data_store(
    client: RESTClientObject, data_store: DataStore, credentials: Optional[dr.Credential] = None
) -> DataStore:
    """If database connection requires credentials, associate credentials with a data store, so that a
    recipe can find them and apply automatically
    """
    if credentials:
        r = client.put(
            f"credentials/{credentials.credential_id}/associations/dataconnection:{data_store.id}/",
            json={"isDefault": True},
        )
        assert r.status_code in {200, 201}

    return data_store


def create_recipe_from_dataset(use_case_id: str) -> Recipe:
    """Create a recipe from dataset."""
    # get dataset id you plan to use
    dataset = Dataset.get("DATASET_ID")
    dataset_input = DatasetInput(sampling=RandomSamplingOperation(rows=2000, seed=1))
    recipe = Recipe.from_dataset(
        UseCase.get(use_case_id),
        dataset,
        DataWranglingDialect.SPARK,
        [dataset_input],
    )
    return recipe


def create_recipe_from_datasource(client: RESTClientObject, use_case_id: str) -> Recipe:
    """Create a recipe from data source."""
    driver = [
        driver
        for driver in dr.DataDriver.list(dr.enums.DataDriverListTypes.JDBC)
        if driver.class_name == "net.snowflake.client.jdbc.SnowflakeDriver"
        and driver.version == "3.9.2"
    ][0]

    data_store = DataStore.create(
        data_store_type=dr.enums.DataStoreTypes.JDBC,
        canonical_name=f"Canonical_name_{uuid.uuid4().hex.upper()}",
        driver_id=driver.id,
        jdbc_url="jdbc_url",
    )
    credentials = [cred for cred in dr.Credential.list() if cred.name == "CREDENTIALS_NAME"][0]
    associate_credentials_with_data_store(client, data_store, credentials)

    data_source_input = DataSourceInput(
        f"snowflake_input-{uuid.uuid4().hex.upper()}",
        table="TABLE_NAME",
        schema="SCHEMA_NAME",
        catalog="CATALOG_NAME",
        sampling=RandomSamplingOperation(rows=2000, seed=1),
    )

    recipe = Recipe.from_data_store(
        UseCase.get(use_case_id),
        data_store,
        DataWranglingDataSourceTypes.JDBC,
        DataWranglingDialect.SNOWFLAKE,
        [data_source_input],
    )
    return recipe


def user_flow_template(client: RESTClientObject) -> None:
    """Example of the user flow."""
    # If there is no defined data store, define it. For example, for snowflake:
    use_case_id = "USE_CASE_ID"
    # for relational databases as sources
    recipe = create_recipe_from_datasource(client, use_case_id)
    # or for static datasets as sources
    recipe = create_recipe_from_dataset(use_case_id)
    # resample for time series purposes
    multiseries_id_column = "SERIES_COLUMN_NAME"
    selected_series = ["SERIES_A", "SERIES_B"]
    datetime_partition_column = "DATE_COLUMN_NAME"
    number_of_rows = 2000
    datetime_sampling = DatetimeSamplingOperation(
        datetime_partition_column,
        rows=number_of_rows,
        # "Earliest" row selection is recommended, in case timeseriesTransformationPlan is requested.
        # Recommendations are provided based on fearures important for a trained model with the provided target,
        # therefore so it s important to not include any data from sample into future validation or
        # holdout partitioning fold.
        strategy="earliest",
        multiseries_id_column=multiseries_id_column,
        # select couple of representative series in case of multiseries dataset
        selected_series=selected_series,
    )
    recipe.inputs[0].sampling = datetime_sampling
    Recipe.set_inputs(recipe.id, recipe.inputs)

    # check the data, compute the preview and insights
    recipe.retrieve_preview()
    recipe.retrieve_insights()

    # Either create a time series plan manually or get a suggestion in a form of timeseriesTransformationPlan, latter is
    # available behind Enable AutoTS feature flag,
    # dataset is multiplied n forecast_distances_times, how much rows to predict ahead
    forecast_distances = [1, 2, 3]
    # which windows to use for derivation, in terms of rows.
    feature_derivation_windows = [7]
    target_column = "TARGET_COLUMN_NAME"
    input_parameters = InputParameters(
        forecast_distances=forecast_distances,
        feature_derivation_windows=feature_derivation_windows,
        target_column=target_column,
        datetime_partition_column=datetime_partition_column,
        multiseries_id_column=multiseries_id_column,
    )
    plan = TimeSeriesTransformationPlan.compute(recipe.id, input_parameters)

    # review the plan and adjust it if needed.
    assert plan.suggested_operations

    # For performance reasons it s important to create user defined functions (UDFs) on database side and use them for
    # rolling median and rolling most frequent features generation.
    # Check out https://github.com/datarobot-community/wrangling_helpers/.
    # Not applicable for Spark.
    rolling_median_udf = "path_to_added_rolling_median_udf"
    rolling_most_frequent_udf = "path_to_added_most_frequent_udf"

    # Apply the result to the recipe.
    ts_operation = TimeSeriesOperation(
        **plan.suggested_operations[0]["arguments"],
        rolling_median_udf=rolling_median_udf,
        rolling_most_frequent_udf=rolling_most_frequent_udf,
    )
    Recipe.set_operations(recipe.id, [ts_operation])

    # verify output
    preview = recipe.retrieve_preview()
    insights = recipe.retrieve_insights()
    assert preview
    assert insights

    # publish dataset to AI catalog or back to the data source.
    dataset_name = "published_dataset"
    max_wait = 600
    dataset = Dataset.create_from_recipe(
        recipe, dataset_name, use_cases=[use_case_id], max_wait=max_wait
    )
    assert dataset


if __name__ == "__main__":
    client = dr.Client(
        token="TOKEN",
        endpoint="endpoint",
    )

    user_flow_template(client)
