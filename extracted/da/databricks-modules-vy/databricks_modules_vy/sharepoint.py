import random
import time
import uuid
import warnings
from io import BytesIO, StringIO

import numpy as np
import pandas as pd
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext
from pyspark.dbutils import DBUtils
from pyspark.sql import DataFrame, SparkSession

from .dataframe import snake_headers
from .logging import lp

spark = SparkSession.builder.appName("module").getOrCreate()
dbutils = DBUtils(spark)


def _get_sharepoint_ctx(site_name="VyMasterdata") -> ClientContext:
    sharepoint_url = dbutils.secrets.get("SHAREPOINT", "url")
    site_url = f"{sharepoint_url}/sites/{site_name}"
    client_id = dbutils.secrets.get("SHAREPOINT", "app_id")
    client_secret = dbutils.secrets.get("SHAREPOINT", "app_secret")

    return ClientContext(site_url).with_client_credentials(client_id, client_secret)


def _execute_query_with_backoff(
    ctx, max_attempts=6, base_delay_seconds=1.0, max_delay_seconds=30.0
) -> None:
    """Execute a SharePoint query with simple retry/backoff for transient errors."""
    for attempt in range(1, max_attempts + 1):
        try:
            ctx.execute_query()
            return
        except ClientRequestException as exc:
            status_code = getattr(exc, "status_code", None)
            if status_code not in (429, 503):
                raise

            if attempt == max_attempts:
                raise

            retry_after = None
            response = getattr(exc, "response", None)
            if response is not None:
                retry_after = response.headers.get("Retry-After")

            if retry_after is not None:
                sleep_seconds = float(retry_after)
            else:
                sleep_seconds = min(max_delay_seconds, base_delay_seconds * (2 ** (attempt - 1)))
                sleep_seconds += random.uniform(0.0, 0.5)

            lp(
                f"Sharepoint query failed with status {status_code}."
                f" Retry {attempt}/{max_attempts} in {sleep_seconds:.2f} seconds..."
            )

            time.sleep(sleep_seconds)


def df_from_sharepoint_masterdata(
    list_name, row_limit=5000, site_name="VyMasterdata", internal_name=True
) -> DataFrame:
    # Connect and fetch data
    ctx = _get_sharepoint_ctx(site_name)

    # Get the list and metadata
    s_list = ctx.web.lists.get_by_title(list_name)
    s_list_fields = s_list.fields
    ctx.load(s_list_fields)
    _execute_query_with_backoff(ctx)

    # Create a dictionary to map internal names to display names
    field_map = {field.internal_name: field.title for field in s_list_fields}

    # Set the row limit for the query
    l_items = s_list.get_items().top(row_limit)
    ctx.load(l_items)
    _execute_query_with_backoff(ctx)

    # BUILD PANDAS DF AND CONVERT TO SPARK DF #
    dp = pd.DataFrame()
    for i, item in enumerate(l_items):
        dp_i = pd.DataFrame(item.properties, index=range(1))
        dp = pd.concat([dp, dp_i])

    list_metadata_cols = [
        "FileSystemObjectType",
        "ServerRedirectedEmbedUri",
        "ServerRedirectedEmbedUrl",
        "ContentTypeId",
        "ComplianceAssetId",
        "OData__ColorTag",
        "GUID",
        "OData__UIVersionString",
        "AuthorId",
        "EditorId",
        "Attachments",
        "Id",
        "ParentList",
    ]

    existing_metadata_cols = [col for col in list_metadata_cols if col in dp.columns]
    dp = dp.drop(existing_metadata_cols, axis="columns")

    # Drop columns with only None values
    dp = dp.dropna(axis="columns", how="all")

    # Convert to spark dataframe
    df = spark.createDataFrame(dp)

    if not internal_name:
        for internal_name, field_name in field_map.items():
            df = df.withColumnRenamed(internal_name, field_name)

    df = snake_headers(df)

    # Check if the number of rows in the dataframe is the same as row_limit
    if df.count() == row_limit:
        warnings.warn(
            f"The number of rows in the dataframe ({df.count()}) is equal to the row_limit ({row_limit}). "
            "Some rows might have been lost. Consider increasing the row_limit."
        )
    return df


def _get_file_bytes_from_sharepoint(item_path, site_name="VyMasterdata"):
    """Fetches the file at the provided location in item_path. Raises exception if no file is found.

    Args:
        item_path (str) : path relative to the site the csv is located. Initiate the path with '/'
        site_name (str) : name of site to fetch csv

    Returns:
        (sharepoint.File) file-object from sharepoint-lib
    """
    csv_url = f"/sites/{site_name}" + item_path
    ctx = _get_sharepoint_ctx(site_name)

    file_ = ctx.web.get_file_by_server_relative_url(csv_url)
    ctx.load(file_)
    _execute_query_with_backoff(ctx)

    # Download the file-contents
    file_bytesio = BytesIO()
    file_.download(file_bytesio)
    _execute_query_with_backoff(ctx)

    return file_bytesio


def get_file_exists(relative_url, site_name):
    """Checks if the provided path to a file exists at the provided site. Raises Exception if file is not found

    Args:
        relative_url (str) : path relative to the site the csv is located. Initiate the path with \'/\'
        site_name (str) : name of site the file belongs to
    """

    _get_file_bytes_from_sharepoint(relative_url, site_name)


def df_from_sharepoint_csv(
    item_path,
    site_name="VyMasterdata",
    delimiter=";",
    header=False,
    col_names=None,
    include_row_num=False,
    row_num_type=int,
    pd_dtype=object,
) -> DataFrame:
    """Gets the bytes from a csv-file in sharepoint and converts it to a spark dataframe

    Args:
        item_path (str)         : path relative to the site the csv is located. Initiate the path with \'/\'
        site_name (str)         : name of site to fetch csv
        delimiter (str)         : delimiter used by the csv-file
        header (bool)           : uses header from csv-file if left True. Sets column names to c_0, c_1, ... if left False
        include_row_num (bool)  : adds the row-number of the csv as an additional column

    Returns:
        (spark.DataFrame) dataframe of the csv

    """
    # ######## CONNECT AND FETCH DATA #########
    file_bytesio = _get_file_bytes_from_sharepoint(item_path, site_name)

    if header:
        dp = pd.read_csv(
            StringIO(file_bytesio.getvalue().decode("latin-1")),
            delimiter=delimiter,
            names=col_names,
            dtype=pd_dtype,
        )
    else:
        dp = pd.read_csv(
            StringIO(file_bytesio.getvalue().decode("latin-1")),
            delimiter=delimiter,
            header=None,
            names=col_names,
            dtype=pd_dtype,
        )
        dp = dp.rename(columns={i: f"c_{i}" for i in range(dp.shape[1])})

    dp = dp.replace([np.nan], [None])

    if include_row_num:
        dp["row_num"] = dp.reset_index().index + 1
        dp["row_num"] = dp["row_num"].astype(row_num_type)

    df = spark.createDataFrame(dp)

    return df


def df_from_sharepoint_csv_utf8(
    item_path,
    site_name="VyMasterdata",
    delimiter=";",
    header=False,
    col_names=None,
    include_row_num=False,
    row_num_type=int,
    pd_dtype=object,
    comment=None,
) -> DataFrame:
    """Gets the bytes from a csv-file in sharepoint and converts it to a spark dataframe

    Args:
        item_path (str)         : path relative to the site the csv is located. Initiate the path with \'/\'
        site_name (str)         : name of site to fetch csv
        delimiter (str)         : delimiter used by the csv-file
        header (bool)           : uses header from csv-file if left True. Sets column names to c_0, c_1, ... if left False
        include_row_num (bool)  : adds the row-number of the csv as an additional column
        comment (str)           : character that indicates a comment

    Returns:
        (spark.DataFrame) dataframe of the csv

    """
    # ######## CONNECT AND FETCH DATA #########
    file_bytesio = _get_file_bytes_from_sharepoint(item_path, site_name)

    if header:
        dp = pd.read_csv(
            StringIO(file_bytesio.getvalue().decode("utf-8")),
            delimiter=delimiter,
            names=col_names,
            dtype=pd_dtype,
            comment=comment,
        )
    else:
        dp = pd.read_csv(
            StringIO(file_bytesio.getvalue().decode("utf-8")),
            delimiter=delimiter,
            header=None,
            names=col_names,
            dtype=pd_dtype,
            comment=comment,
        )
        dp = dp.rename(columns={i: f"c_{i}" for i in range(dp.shape[1])})

    dp = dp.replace([np.nan], [None])

    if include_row_num:
        dp["row_num"] = dp.reset_index().index + 1
        dp["row_num"] = dp["row_num"].astype(row_num_type)

    df = spark.createDataFrame(dp)

    return df


# # Functions for traversing and extracting files and folders from a site # #
def get_files_in_folder(relative_path_to_folder, site_name="VyMasterdata"):
    """
    Returns the name of a folder within a site at the passed location relative to the site

    Args:
        relative_url (str) : path relative to the site the csv is located. Initiate the path with \'/\'
        site_name (str) : name of site the file belongs to

    Returns (Array<str>): Array of files present at the folder provided
    """

    ctx = _get_sharepoint_ctx(site_name)

    # Set up query and execute it
    folder = ctx.web.get_folder_by_server_relative_url(relative_path_to_folder)
    files = folder.files
    ctx.load(files)
    _execute_query_with_backoff(ctx)

    # Return result of query
    return [file.properties["Name"] for file in files]


def get_filepaths_in_folder(relative_path_to_folder, site_name="VyMasterdata", ctx=None):
    """
    Returns relative filepaths within folder of a site at the passed relative location

    Args:
        relative_url (str) : path relative to the site the csv is located. Initiate the path with \'/\'
        site_name (str) : name of site the file belongs to

    Returns (Array<str>): Array of files present at the folder provided
    """

    if ctx is None:
        ctx = _get_sharepoint_ctx(site_name)

    # Set up query and execute it
    folder = ctx.web.get_folder_by_server_relative_url(relative_path_to_folder)
    files = folder.files
    ctx.load(files)
    _execute_query_with_backoff(ctx)

    # Return result of query
    return [file.properties["ServerRelativeUrl"] for file in files]


def get_subfolders(relative_path_to_folder, site_name="VyMasterdata", ctx=None):
    """
    Returns subfolders found at the passed relative location in a sharepoint-site

    Args:
        relative_url (str) : path relative to the site the csv is located. Initiate the path with \'/\'
        site_name (str) : name of site the file belongs to

    Returns (Array<str>): Array of files present at the folder provided
    """

    if ctx is None:
        ctx = _get_sharepoint_ctx(site_name)

    # Set up query and execute it
    folder = ctx.web.get_folder_by_server_relative_url(relative_path_to_folder)
    subfolders = folder.folders
    ctx.load(subfolders)
    _execute_query_with_backoff(ctx)

    # Return result of query
    return [x.properties["Name"] for x in subfolders]


def get_items_at_folder(relative_path_to_folder, site_name="VyMasterdata", ctx=None):
    """
    Recursively iterates through tree of sharepoint site-folder and collects the items located at them

    Args:
        relative_url (str) : path relative to the site the csv is located. Initiate the path with \'/\'
        site_name (str) : name of site the file belongs to

    Returns (Array<str>): Array of files present at the folder provided
    """

    if ctx is None:
        ctx = _get_sharepoint_ctx(site_name)

    # Set up array to store result
    result = []

    # Get subfolders at current location
    subfolders = get_subfolders(relative_path_to_folder, site_name, ctx)

    # Base-condition
    if not subfolders:
        return get_filepaths_in_folder(relative_path_to_folder, site_name, ctx)

    # Recursion
    for subfolder in subfolders:
        result += get_filepaths_in_folder(relative_path_to_folder, site_name, ctx)
        result += get_items_at_folder(relative_path_to_folder + f"/{subfolder}", site_name, ctx)

    return result
