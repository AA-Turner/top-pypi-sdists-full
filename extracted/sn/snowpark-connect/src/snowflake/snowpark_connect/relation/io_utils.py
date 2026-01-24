#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from urllib.parse import urlparse

from pyspark.errors.exceptions.base import AnalysisException

from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code

CLOUD_PREFIX_TO_CLOUD = {
    "abfss": "azure",
    "wasbs": "azure",
    "gcs": "gcp",
    "gs": "gcp",
}

SUPPORTED_COMPRESSION_PER_FORMAT = {
    "csv": {
        "GZIP",
        "BZ2",
        "BROTLI",
        "ZSTD",
        "DEFLATE",
        "RAW_DEFLATE",
        "NONE",
        "UNCOMPRESSED",
    },
    "json": {
        "GZIP",
        "BZ2",
        "BROTLI",
        "ZSTD",
        "DEFLATE",
        "RAW_DEFLATE",
        "NONE",
        "UNCOMPRESSED",
    },
    "parquet": {"LZO", "SNAPPY", "NONE", "UNCOMPRESSED"},
    "text": {"NONE", "UNCOMPRESSED"},
}


def supported_compressions_for_format(format: str) -> set[str]:
    return SUPPORTED_COMPRESSION_PER_FORMAT.get(format, set())


def is_supported_compression(format: str, compression: str | None) -> bool:
    if compression is None:
        return True
    return compression in supported_compressions_for_format(format)


def get_compression_for_source_and_options(
    source: str, options: dict[str, str], from_read: bool = False
) -> str | None:
    """
    Determines the compression type to use for a given data source and options.
    Args:
        source (str): The data source format (e.g., "csv", "json", "parquet", "text").
        options (dict[str, str]): A dictionary of options that may include a "compression" key.
    Returns:
        str: The compression type to use (e.g., "GZIP", "SNAPPY", "NONE").
    Raises:
        AnalysisException: If the specified compression is not supported for the given source format.
    """
    # From read, we don't have a default compression
    if from_read and "compression" not in options:
        return None

    # Get compression from options for proper filename generation
    default_compression = "NONE" if source != "parquet" else "snappy"
    compression = options.get("compression", default_compression).upper()
    if compression == "UNCOMPRESSED":
        compression = "NONE"

    if not is_supported_compression(source, compression):
        supported_compressions = supported_compressions_for_format(source)
        exception = AnalysisException(
            f"Compression {compression} is not supported for {source} format. "
            + (
                f"Supported compressions: {sorted(supported_compressions)}"
                if supported_compressions
                else "None compression supported for this format."
            )
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    return compression


def get_cloud_from_url(
    url: str,
):
    """
    Google Cloud Storage : 'gcs://<bucket>[/<path>/]'
    Microsoft Azure : 'azure://<account>.blob.core.windows.net/<container>[/<path>/]'
    """
    url_parts = url.split("://")
    if len(url_parts) < 2:
        return None

    cloud_domain = url_parts[0].lower()
    return CLOUD_PREFIX_TO_CLOUD.get(cloud_domain, cloud_domain)


def split_url_paths(url):
    return url.split("://")[1].split("/")


def parse_gcp_url(url: str):
    """

    Args:
        url: 'gcs://<bucket>[/<path>/]'

    """
    path_parts = split_url_paths(url)
    bucket_name = path_parts[0]
    path = "/".join(path_parts[1:])
    return bucket_name, path


def parse_azure_url(url: str):
    """
    Args:
        url: 'azure://<account>.blob.core.windows.net/<container>[/<path_to_data>/]'
        url: 'abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<path_to_data>'
        url: 'wasbs://<container name>@<storage account name>.blob.core.windows.net/<path_to_data>'
    """
    path_parts = split_url_paths(url)

    # Check if it's azure:// scheme (different format)
    if url.startswith("azure://"):
        # For azure://, format is: azure://<account>.blob.core.windows.net/<container>/<path>
        if len(path_parts) < 2:
            exception = AnalysisException(
                f"Malformed Azure URL: expected format 'azure://<account>.blob.core.windows.net/<container>[/<path>]', got '{url}'."
            )
            attach_custom_error_code(
                exception,
                ErrorCodes.INVALID_INPUT,
            )
            raise exception
        account = path_parts[0].split(".")[0]
        container = path_parts[1]
        path = "/".join(path_parts[2:])
    else:
        # For abfss:// and wasbs://, format is: scheme://<container>@<account>.domain/<path>
        prefix = path_parts[0].split(".")[0].split("@")
        account = prefix[1]
        container = prefix[0]
        path = "/".join(path_parts[1:])

    return account, container, path


def is_cloud_path(path: str) -> bool:
    return (
        path.startswith("@")  # Snowflake Stage
        or path.startswith("s3://")
        or path.startswith("s3a://")  # AWS S3
        or path.startswith("azure://")
        or path.startswith("abfss://")
        or path.startswith("wasbs://")  # Azure
        or path.startswith("gcs://")
        or path.startswith("gs://")  # GCP
    )


def convert_file_prefix_path(path: str) -> str:
    if path.startswith("file:/"):
        return urlparse(path).path
    return path
