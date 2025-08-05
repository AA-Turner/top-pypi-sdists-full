from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.client_request_exception import ClientRequestException
import pandas as pd
from pyspark.sql import DataFrame, SparkSession
from pyspark.dbutils import DBUtils
from .dataframe import snake_headers
from io import StringIO, BytesIO
import numpy as np
import uuid
import warnings

spark = SparkSession.builder.appName("module").getOrCreate()
dbutils = DBUtils(spark)


def df_from_sharepoint_masterdata(list_name, row_limit=5000, site_name="VyMasterdata"):
    # Connect and fetch data
    sharepoint_url = dbutils.secrets.get("SHAREPOINT", "url")
    site_url = f"{sharepoint_url}/sites/{site_name}"
    client_id = dbutils.secrets.get("SHAREPOINT", "app_id")
    client_secret = dbutils.secrets.get("SHAREPOINT", "app_secret")

    ctx = ClientContext(site_url).with_credentials(ClientCredential(client_id, client_secret))
    sp_lists = ctx.web.lists
    s_list = sp_lists.get_by_title(list_name)

    # Set the row limit for the query
    l_items = s_list.get_items().top(row_limit)
    ctx.load(l_items)
    ctx.execute_query()

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
    ]

    dp = dp.drop(list_metadata_cols, axis="columns")

    # Drop columns with only None values
    dp = dp.dropna(axis="columns", how="all")

    # Convert to spark dataframe
    df = spark.createDataFrame(dp)
    df = snake_headers(df)

    # Check if the number of rows in the dataframe is the same as row_limit
    if df.count() == row_limit:
        warnings.warn(
            f"The number of rows in the dataframe ({df.count()}) is equal to the row_limit ({row_limit}). "
            "Some rows might have been lost. Consider increasing the row_limit."
        )
    return df


def authenticate_sharepoint(site_url, client_id, client_secret):
    """Authenticate with SharePoint using username and password"""

    ctx = ClientContext(site_url).with_credentials(ClientCredential(client_id, client_secret))
    return ctx


def _get_file_bytes_from_sharepoint(item_path, site_name="VyMasterdata"):
    """Fetches the file at the provided location in item_path. Raises exception if no file is found.

    Args:
        item_path (str) : path relative to the site the csv is located. Initiate the path with \'/\'
        site_name (str) : name of site to fetch csv

    Returns:
        (sharepoint.File) file-object from sharepoint-lib
    """
    sharepoint_url = dbutils.secrets.get("SHAREPOINT", "url")
    site_url = f"{sharepoint_url}/sites/{site_name}"
    csv_url = f"/sites/{site_name}" + item_path

    client_id = dbutils.secrets.get("SHAREPOINT", "app_id")
    client_secret = dbutils.secrets.get("SHAREPOINT", "app_secret")

    ctx = authenticate_sharepoint(site_url, client_id, client_secret)

    file_ = ctx.web.get_file_by_server_relative_url(csv_url)
    ctx.load(file_)
    ctx.execute_query()

    # Download the file-contents
    file_bytesio = BytesIO()
    file_.download(file_bytesio)
    ctx.execute_query()

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
):
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
):
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

    # Setting up context to site with credentials
    sharepoint_url = dbutils.secrets.get("SHAREPOINT", "url")
    site_url = f"{sharepoint_url}/sites/{site_name}"
    client_id = dbutils.secrets.get("SHAREPOINT", "app_id")
    client_secret = dbutils.secrets.get("SHAREPOINT", "app_secret")

    ctx = authenticate_sharepoint(site_url, client_id, client_secret)

    # Set up query and execute it
    folder = ctx.web.get_folder_by_server_relative_url(relative_path_to_folder)
    files = folder.files
    ctx.load(files)
    ctx.execute_query()

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
        # Setting up context to site with credentials
        sharepoint_url = dbutils.secrets.get("SHAREPOINT", "url")
        site_url = f"{sharepoint_url}/sites/{site_name}"
        client_id = dbutils.secrets.get("SHAREPOINT", "app_id")
        client_secret = dbutils.secrets.get("SHAREPOINT", "app_secret")

        ctx = authenticate_sharepoint(site_url, client_id, client_secret)

    # Set up query and execute it
    folder = ctx.web.get_folder_by_server_relative_url(relative_path_to_folder)
    files = folder.files
    ctx.load(files)
    ctx.execute_query()

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
        # Setting up context to site with credentials
        sharepoint_url = dbutils.secrets.get("SHAREPOINT", "url")
        site_url = f"{sharepoint_url}/sites/{site_name}"
        client_id = dbutils.secrets.get("SHAREPOINT", "app_id")
        client_secret = dbutils.secrets.get("SHAREPOINT", "app_secret")

        ctx = authenticate_sharepoint(site_url, client_id, client_secret)

    # Set up query and execute it
    folder = ctx.web.get_folder_by_server_relative_url(relative_path_to_folder)
    subfolders = folder.folders
    ctx.load(subfolders)
    ctx.execute_query()

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
        # Setting up context to site with credentials
        sharepoint_url = dbutils.secrets.get("SHAREPOINT", "url")
        site_url = f"{sharepoint_url}/sites/{site_name}"
        client_id = dbutils.secrets.get("SHAREPOINT", "app_id")
        client_secret = dbutils.secrets.get("SHAREPOINT", "app_secret")

        ctx = authenticate_sharepoint(site_url, client_id, client_secret)

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
