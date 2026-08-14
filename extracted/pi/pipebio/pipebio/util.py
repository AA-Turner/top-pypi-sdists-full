import csv
import inspect
import logging
import os
import sys
from typing import Any

from Bio.Seq import translate

from requests import HTTPError
from requests.adapters import HTTPAdapter
from requests_toolbelt.sessions import BaseUrlSession
from urllib3 import Retry

from pipebio.models.sequence_document_kind import SequenceDocumentKind

DEFAULT_TIMEOUT = 60  # seconds


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class Util:

    @staticmethod
    def is_aws():
        return 'IS_AWS' in os.environ and os.environ['IS_AWS']=='True'

    # Copied from the google 
    @staticmethod
    def raise_detailed_error(request_object):
        try:

            if request_object.status_code not in [200, 201]:
                print(request_object.text)

            request_object.raise_for_status()
        except HTTPError as e:
            raise HTTPError(e, request_object.text)

    @staticmethod
    def mount_standard_session(session: BaseUrlSession, retry_post=False):
        # Remove previously mounted sessions.
        session.close()
        logging.basicConfig(level=logging.INFO)
        # NOTE: We often use POST for "READ" operations. Can we retry on those specifically?
        methods = ['HEAD', 'GET', 'OPTIONS', 'TRACE', 'PUT', 'PATCH', 'DELETE']
        if retry_post:
            methods.append('POST')

        retries = Retry(total=5,
                        backoff_factor=0,
                        status_forcelist=[
                            100, 101, 102, 103, 104,
                            404, 408, 429,
                            500, 502, 503, 504
                        ],
                        connect=5,
                        read=5,
                        allowed_methods=methods
                        )
        # https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
        session.mount('http://', TimeoutHTTPAdapter(max_retries=retries))
        session.mount('https://', TimeoutHTTPAdapter(max_retries=retries))
        return session

    @staticmethod
    def get_executed_file_location():
        # @see https://stackoverflow.com/a/44592299
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        return os.path.dirname(os.path.abspath(filename))

    @staticmethod
    def get_sequence_kind(sequence: str) -> SequenceDocumentKind:
        try:
            not_an_alignment = sequence.replace('-', '')
            translate(not_an_alignment)
            return SequenceDocumentKind.DNA
        except:
            return SequenceDocumentKind.AA

    @staticmethod
    def split_extension(filename: str) -> tuple[str, str]:
        """Split a filename into (stem, extension), keeping compound extensions.

        Unlike os.path.splitext, 'name.tsv.gz' splits as ('name', '.tsv.gz')
        rather than ('name.tsv', '.gz'), so callers appending an index to the
        stem produce 'name_1.tsv.gz' instead of 'name.tsv_1.gz'.

        The inner suffix must be alphabetic, so a version-like 'v1.2.gz' keeps
        its '.2' in the stem rather than splitting as ('v1', '.2.gz').
        """
        compression_suffixes = {'.gz', '.bz2', '.xz', '.zst', '.zip'}
        stem, extension = os.path.splitext(filename)
        if extension.lower() in compression_suffixes:
            inner_stem, inner_extension = os.path.splitext(stem)
            if inner_extension[1:].isalpha():
                return inner_stem, inner_extension + extension
        return stem, extension

    @staticmethod
    def get_organization_id(user: Any) -> str:
        # Default to first org in list
        return user['org']['id']

    @staticmethod
    def set_csv_field_size_limit():
        """
        Set CSV field size limit with Windows compatibility.
        On Windows, sys.maxsize can be too large for C long, so we find the max that works.
        """
        maxInt = sys.maxsize
        while True:
            try:
                csv.field_size_limit(maxInt)
                break
            except OverflowError:
                maxInt = int(maxInt / 2)
