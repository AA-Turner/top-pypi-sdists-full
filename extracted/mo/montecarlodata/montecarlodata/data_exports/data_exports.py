import os
import urllib.request
from typing import Optional
from urllib.parse import urlparse

import click
import requests
from tabulate import tabulate

from montecarlodata.config import Config
from montecarlodata.data_exports.catalog import DATA_EXPORT_CATALOG
from montecarlodata.data_exports.fields import (
    EXPECTED_GET_DATA_EXPORT_URL,
    FILE_SCHEME,
    LIST_DATA_EXPORTS_HEADERS,
    S3_SCHEME,
    SCHEME_DELIM,
)
from montecarlodata.errors import complain_and_abort, manage_errors
from montecarlodata.fs_utils import mkdirs
from montecarlodata.queries.data_exports import GET_DATA_EXPORT_URL
from montecarlodata.utils import AwsClientWrapper, GqlWrapper


class DataExportService:
    def __init__(
        self,
        config: Config,
        command_name: str,
        request_wrapper: Optional[GqlWrapper] = None,
    ):
        self._abort_on_error = True
        self._command_name = command_name

        self._request_wrapper = request_wrapper or GqlWrapper(
            config,
            command_name=self._command_name,
        )

        self.scheme_handler = {
            FILE_SCHEME: self._save_data_export_to_disk,
            S3_SCHEME: self._save_data_export_to_s3,
        }

    @manage_errors
    def echo_data_exports(
        self,
        headers: str = "firstrow",
        table_format: str = "fancy_grid",
    ) -> None:
        """
        Echo Data Exports as a pretty table
        """
        table = [LIST_DATA_EXPORTS_HEADERS]
        for data_export in DATA_EXPORT_CATALOG:
            table.append(
                [
                    f"{data_export.title} ({data_export.name})",
                    (
                        data_export.description
                        if data_export.description.endswith(".")
                        else f"{data_export.description}."
                    ),
                ]
            )
        click.echo(tabulate(table, headers=headers, tablefmt=table_format, maxcolwidths=100))

    @manage_errors
    def get_data_export(
        self,
        data_export: str,
        destination: str,
        aws_profile: Optional[str] = None,
        dry: bool = False,
    ) -> None:
        """
        Get Data Export, if available, and either persist to S3 or local file system
        """
        parsed_destination = urlparse(destination)
        scheme = parsed_destination.scheme
        if scheme == S3_SCHEME and not aws_profile:
            raise ValueError("Cannot use an s3 destination without specifying an AWS profile.")

        netloc_with_path = parsed_destination.geturl().replace(f"{scheme}{SCHEME_DELIM}", "", 1)

        try:
            handler = self.scheme_handler[scheme]
        except KeyError:
            complain_and_abort("Scheme either missing or not supported.")
        else:
            data_export_url = self._get_data_export_url(data_export=data_export)
            if dry:
                click.echo(data_export_url)
                return
            click.echo(f"Saving data export to '{destination}'.")
            handler(
                data_export_url=data_export_url,
                destination=netloc_with_path,
                aws_profile=aws_profile,
            )
            click.echo("Complete. Have a nice day!")

    def _get_data_export_url(self, data_export: str) -> str:
        """
        Get Data Export URL from the monolith
        """
        resp = self._request_wrapper.make_request_v2(
            query=GET_DATA_EXPORT_URL,
            operation=EXPECTED_GET_DATA_EXPORT_URL,
            service="data_exports_service",
            variables=dict(
                data_export_name=data_export,
            ),
        )
        url = resp.data.url  # type: ignore
        if not url:
            complain_and_abort(
                "Data Export not found. This Data Export might not be available for your account."
            )
        return url

    def _save_data_export_to_disk(self, data_export_url: str, destination: str, **kwargs) -> None:
        """
        Save Data Export to the local filesystem
        """
        if not destination:
            complain_and_abort(
                f"Invalid path. Expected format: '{FILE_SCHEME}{SCHEME_DELIM}folder/file.csv'"
            )
        mkdirs(os.path.dirname(destination))
        urllib.request.urlretrieve(data_export_url, destination)

    def _save_data_export_to_s3(
        self, data_export_url: str, destination: str, aws_profile: Optional[str] = None
    ) -> None:
        """
        Save Data Export to S3
        """
        try:
            bucket, key = destination.split("/", maxsplit=1)
            if not key:
                raise ValueError
        except (ValueError, AttributeError):
            complain_and_abort(
                f"Invalid path. Expected format: '{S3_SCHEME}{SCHEME_DELIM}bucket/key.csv'"
            )
        else:
            AwsClientWrapper(profile_name=aws_profile).upload_stream_to_s3(
                data=requests.get(data_export_url, stream=True).raw, bucket=bucket, key=key
            )
