import mimetypes
import os
from contextlib import suppress
from datetime import datetime
from io import BytesIO
from typing import Generator, Optional

import magic
import requests
from wbcore.contrib.io.backends.abstract import AbstractDataBackend
from wbcore.contrib.io.backends.utils import register


@register("Default Stream", save_data_in_import_source=True)
class DataBackend(AbstractDataBackend):
    """
    DataBackend for stream based import
    """

    def __init__(
        self,
        url: Optional[str] = None,
        **kwargs,
    ):
        """
        Args:
            url: URL to fetch the stream from
            **kwargs:
        Raises:
            ValueError: If url not found in the keywords argument
        """
        if not url:
            raise ValueError("This backend needs a valid url")

        self.url = url

    @classmethod
    def _check_content_type(cls, output: BytesIO, filename: str) -> bool:
        """
        Check if given bytes stream matches the corresponding filename extension

        Args:
            output: The file bytes stream
            filename: The file name (with extension)

        Returns:
            True if the contents matches

        Raises:
            MagicException: If error happens while extracting content type
        """
        try:
            buffer_content_type = magic.from_buffer(output.read(1024), mime=True)
            guess_extensions = mimetypes.guess_extension(buffer_content_type)
            return guess_extensions == os.path.splitext(filename)[1]
        except magic.MagicException:
            return False

    def get_files(
        self,
        execution_time: datetime,
        base_filename: Optional[str] = "default_stream",
        extension: Optional[str] = "xml",
        validate_content_type: Optional[bool] = True,
        **kwargs,
    ) -> Generator[tuple[str, BytesIO], None, None]:
        """
        Connect to file stream and download its content as bytes stream

        Args:
            execution_time: When the import is executed.
            base_filename: The resulting filename. Defaults to "default_stream".
            extension: The resulting file extension. Defaults to ".xml".
            validate_content_type: If true, will sanitize file content with its given extension. Defaults to True.
            **kwargs:

        Returns:
            A generator of tuple of filename and bytes stream

        """
        with suppress(requests.ConnectionError):
            headers = kwargs.get("headers", {})
            r = requests.get(self.url, headers=headers, timeout=10)
            if r.ok and (content := r.content):
                content_file = BytesIO()
                content_file.write(content)
                content_file.seek(0)
                file_name = f"{base_filename}_{datetime.timestamp(execution_time)}.{extension}"
                if not validate_content_type or (
                    validate_content_type and self._check_content_type(content_file, file_name)
                ):
                    yield file_name, content_file
