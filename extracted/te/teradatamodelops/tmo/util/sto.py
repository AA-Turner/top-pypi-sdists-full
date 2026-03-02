import json
import sys

from teradataml import DataFrame

from tmo.types.exceptions import ConfigurationError
from .connections import execute_sql

DEFAULT_STO_MODELS_TABLE = "vmo_sto_models"


def save_evaluation_metrics(partition_df: DataFrame, metrics: list):
    """
    :param partition_df: teradata dataframe containing at least ["partition_id", "partition_metadata", "num_rows"]
    :param metrics: list of metrics to normalize and report
    :return: None
    """
    total_rows = int(
        partition_df.select(["num_rows"]).sum().to_pandas().iloc[0]["sum_num_rows"]
    )

    metrics_sql = [
        f"SUM(CAST(partition_metadata AS JSON).JSONExtractValue('$.metrics.{metric}') *"
        f" num_rows/{total_rows}) AS {metric}"
        for metric in metrics
    ]
    joined_metrics_sql = ",".join(metrics_sql)
    metrics = DataFrame.from_query(
        f"SELECT {joined_metrics_sql} FROM {partition_df._table_name}"
    ).to_pandas()

    metrics = {metric: "{:.2f}".format(metrics.iloc[0][metric]) for metric in metrics}

    with open("artifacts/output/metrics.json", "w+") as f:
        json.dump(metrics, f, indent=2)


def save_metadata(partition_df: DataFrame):
    """
    create statistic summaries based on the provided dataframe produced via training or evaluation

    partitions.json is {
        "<partition1 key>": <partition1_metadata>,
        "<partition2 key>": <partition2_metadata>,
        ...
    }

    data_stats.json is {
        "num_rows": <num_rows>,
        "num_partitions": <num_partitions>
    }

    :param partition_df: teradata dataframe containing at least ["partition_id", "partition_metadata", "num_rows"]
    :return: None
    """

    total_rows = int(
        partition_df.select(["num_rows"]).sum().to_pandas().iloc[0]["sum_num_rows"]
    )

    metadata_df = partition_df.select(
        ["partition_id", "partition_metadata", "num_rows"]
    ).to_pandas()

    metadata_dict = {
        r["partition_id"]: json.loads(r["partition_metadata"])
        for r in metadata_df.to_dict(orient="records")
    }

    with open("artifacts/output/partitions.json", "w+") as f:
        json.dump(metadata_dict, f, indent=2)

    data_metadata = {
        "num_rows": total_rows,
        "num_partitions": int(metadata_df.shape[0]),
    }

    with open("artifacts/output/data_stats.json", "w+") as f:
        json.dump(data_metadata, f, indent=2)


def cleanup_cli(model_version: str, models_table: str = DEFAULT_STO_MODELS_TABLE):
    """
    cli uses model version of "cli" always. We need to clean up models table between runs.
    A better solution would be for the cli to write to a different table completely and just "recreate" on each run

    :param model_version: the model version being executed
    :param models_table: the models table for cleanup (default is vmo_sto_models)
    :return: None
    """
    if model_version == "cli":
        execute_sql(
            "DELETE FROM {table} WHERE model_version='cli'".format(table=models_table)
        )


def check_sto_version(python_interpreter="tdpython3"):
    """
    Check Python version In-Vantage against the version where this function is running,
    if it's incompatible raise an exception

    :param python_interpreter: path to python interpreter on Vantage node (default is tdpython3)
    :return: None
    """
    version_query = f"""
    SEL DISTINCT ver
    FROM SCRIPT(
        SCRIPT_COMMAND('{python_interpreter} -c "import sys; print(\\".\\".join(map(str, sys.version_info[0:2])))"')
        RETURNS('ver VARCHAR(10)') 
    );
    """
    local_version = ".".join(map(str, sys.version_info[0:2]))
    result = execute_sql(version_query)
    if result.rowcount != 1:
        raise ConfigurationError(
            "Different STO configuration on different nodes, please contact your system"
            " administrator"
        )
    try:
        remote_version = next(iter(result))[0]
    except Exception as err:
        raise ConfigurationError(
            "Different STO configuration on different nodes, please contact your"
            f" system administrator. \nError: {err}"
        )

    if local_version != remote_version:
        raise ConfigurationError(
            "Python versions not matching, local: {local}, In-Vantage: {remote}".format(
                local=local_version, remote=remote_version
            )
        )


def collect_sto_versions(
    raise_diff_config_exception=True, python_interpreter="tdpython3"
):
    """
    Collects Python and packages information from In-Vantage installation

    :param python_interpreter: path to python interpreter on Vantage node (default is tdpython3)
    :param raise_diff_config_exception: whether raise an exception if different Python versions are detected on different AMPs of Vantage system
    :return: Dict with python_version and packages versions
    """
    python_version_query = f"""
    SEL DISTINCT ver
    FROM SCRIPT(
        SCRIPT_COMMAND('{python_interpreter} -c "import sys; print(sys.version.replace(\\"\\n\\",\\" \\"))"')
        RETURNS('ver VARCHAR(100)') 
    );
    """
    result = execute_sql(python_version_query)
    if result.rowcount != 1 and raise_diff_config_exception:
        raise ConfigurationError(
            "Different STO configuration on different nodes, please contact your system"
            " administrator"
        )
    try:
        python_version = next(iter(result))[0]
    except Exception as err:
        raise ConfigurationError(
            "Different STO configuration on different nodes, please contact your"
            f" system administrator. \nError: {err}"
        )

    packages_version_query = f"""
    SEL DISTINCT pkg
    FROM SCRIPT(
        SCRIPT_COMMAND('{python_interpreter} -c "import pkg_resources; [print(pkg) for pkg in pkg_resources.working_set]"')
        RETURNS('pkg VARCHAR(100)') 
    );
    """
    result = execute_sql(packages_version_query)
    packages = {}
    for row in result:
        pair = row[0].split(" ")
        packages[pair[0]] = pair[1]

    return {"python_version": python_version, "packages": packages}


def get_joined_models_df(
    data_table: str,
    model_artefacts_table: str,
    model_version: str,
    partition_id: str = "partition_id",
):
    """
    Joins the dataset which is to be used for scoring/evaluation with the model artefacts and appends the model_artefact
    to the first row with the column name 'model'.

    Args:
        data_table: the table/view of the dataset to join
        model_artefacts_table: the model artefacts table where the model artefacts are stored
        model_version: the model version to use from the model artefacts
        partition_id: the dataset partition_id

    Returns:
        DataFrame
    """
    query = f"""
    SELECT d.*, CASE WHEN n_row=1 THEN m.model ELSE null END AS model 
        FROM (SELECT x.*, ROW_NUMBER() OVER (PARTITION BY x.{partition_id} ORDER BY x.{partition_id}) AS n_row FROM {data_table} x) AS d
        LEFT JOIN {model_artefacts_table} m
        ON d.{partition_id} = m.partition_id
        WHERE m.model_version = '{model_version}'
    """

    return DataFrame.from_query(query)


def get_joined_single_model_df(
    data_table: str,
    model_version: str,
    model_artefacts_table: str = DEFAULT_STO_MODELS_TABLE,
    partition_id: str = "partition_id",
):
    """
    Joins the dataset which is to be used for scoring/evaluation with a single model artefact and appends that artefact
    to the first row of each partition with the column name 'model'.
    If there's more than one artefact corresponding to 'model_version' then the random first one is taken.


    Args:
        data_table: the table/view of the dataset to join
        model_version: the model version to use from the model artefacts
        model_artefacts_table: the model artefacts table where the model artefacts are stored (defaults to vmo_sto_models)
        partition_id: the dataset partition_id

    Returns:
        DataFrame
    """
    query = f"""
    SELECT d.*, CASE WHEN n_row=1 THEN m.model ELSE null END AS model 
        FROM (SEL x.*, ROW_NUMBER() OVER (PARTITION BY x.{partition_id} ORDER BY x.{partition_id}) AS n_row FROM {data_table} x) AS d
        CROSS JOIN (SEL * FROM {model_artefacts_table} WHERE model_version = '{model_version}' QUALIFY CSUM(1,1) = 1) m
    """

    return DataFrame.from_query(query)


def get_joined_partitioned_models_df(
    data_table: str,
    model_version: str,
    model_artefacts_table: str = DEFAULT_STO_MODELS_TABLE,
    partition_id: str = "partition_id",
):
    """
    Joins the dataset which is to be used for scoring/evaluation with the model artefacts and appends the artefact
    to the first row with the column name 'model'.

    Args:
        data_table: the table/view of the dataset to join
        model_version: the model version to use from the model artefacts
        model_artefacts_table: the model artefacts table where the model artefacts are stored (defaults to vmo_sto_models)
        partition_id: the dataset partition_id

    Returns:
        DataFrame
    """
    return get_joined_models_df(
        data_table, model_artefacts_table, model_version, partition_id
    )
