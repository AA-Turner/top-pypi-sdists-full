"""Download, upload and import sequence data.

This module wraps the sequence extract/import endpoints used to move tabular
sequence data in and out of PipeBio documents, transparently handling sharded
downloads, AWS Parquet/GCP TSV differences, compression and retries. It is
exposed as :attr:`PipebioClient.sequences`.
"""

import csv
import gzip
import os
import sys
import tempfile
import time
import traceback
import warnings
from multiprocessing.pool import ThreadPool
from pathlib import Path
from subprocess import check_call
from typing import Any, Dict, List, Optional
from urllib.request import urlopen

import requests
from requests_toolbelt.sessions import BaseUrlSession

from pipebio.column import Column
from pipebio.entities import Entities
from pipebio.models.sort import Sort
from pipebio.models.table_column_type import TableColumnType
from pipebio.util import Util

# Set CSV field size limit with Windows compatibility
Util.set_csv_field_size_limit()


class ImportError(Exception):
    """Raised when a sequence import fails irrecoverably."""
    pass


class Sequences:
    """Wraps the sequence extract/import API endpoints.

    Obtain an instance via :attr:`PipebioClient.sequences` rather than
    constructing it directly.
    """

    # Static property used to join entity_id with sequence_id.
    _merge_delimiter = '##@##'
    _is_aws: bool

    def __init__(self, session: BaseUrlSession, is_aws: bool, user: Any = None) -> None:
        """Initialise the service.

        Args:
            session: An authenticated base-url session from the client.
            is_aws: Whether the connected instance is an AWS deployment (affects
                download format handling).
            user: The authenticated user object, forwarded to the internal
                :class:`~pipebio.entities.Entities` service.
        """
        self._session = Util.mount_standard_session(session)
        self._entities = Entities(session, user)
        self._is_aws = is_aws

    def _parallel_download(self, entity_ids: List[str]) -> None:
        print('Download starting')
        entities = {}

        def download(entity_id: str) -> None:
            entities[entity_id] = self.download(entity_id, Sequences._get_filepath_for_entity_id(entity_id))

        list(ThreadPool(8).imap_unordered(download, entity_ids))

    def download_to_memory(self, entity_ids: List[str]) -> Dict[str, Any]:
        """Download several documents and return their sequences in memory.

        Args:
            entity_ids: Ids of the documents to download.

        Returns:
            A map keyed by a compound ``"<entity_id>##@##<sequence_id>"`` id,
            each value containing the parsed id, name, sequence, annotations and
            type.
        """
        self._parallel_download(entity_ids)

        # Build an in memory map that matches this tsv.
        sequence_map = {}

        columns = [
            Column('id', TableColumnType.STRING),
            Column('name', TableColumnType.STRING),
            Column('sequence', TableColumnType.STRING),
            Column('annotations', TableColumnType.STRING),
            Column('type', TableColumnType.STRING),
        ]

        for entity_id in entity_ids:
            sequence_map = self._read_tsv_to_map(
                Sequences._get_filepath_for_entity_id(entity_id),
                str(entity_id),
                columns,
                sequence_map
            )

        return sequence_map

    @staticmethod
    def _read_tsv_to_map(filepath: str,
                         id_prefix: str,
                         columns: List[Column],
                         sequence_map: Dict[str, any] = None) -> Dict[str, any]:

        sequence_map = {} if sequence_map is None else sequence_map

        print(f'read_tsv_to_map::Reading filepath: "{filepath}"')
        # Read the file.
        with open(filepath, 'r') as tsvfile:

            replaced = (x.replace('\0', '') for x in tsvfile)
            reader = csv.DictReader(replaced, dialect='excel-tab')

            for row in reader:
                if 'id' not in row:
                    raise Exception('id not in row')

                row_id = row['id']

                compound_id = f'{id_prefix}{Sequences._merge_delimiter}{row_id}'
                parsed = {}
                for column in columns:
                    name = column.name
                    # Avoid errors like "KeyError: 'type'".
                    parsed[column.name] = column.parse(row[name]) if name in row else column.parse('')

                sequence_map[compound_id] = parsed

        return sequence_map

    def download(self,
                 entity_id: str,
                 destination: str = None,
                 sort: List[Sort] = None,
                 query: str = None,
                 include_cols: Optional[List[str]] = None,
                 exclude_cols: Optional[List[str]] = None,
                 limit: int = None,
                 allow_deleted: bool = True) -> str:
        """Download the sequences of a single document to a local file.

        Args:
            entity_id: Id of the document to download.
            destination: Local path to write the assembled TSV to.
            sort: Deprecated. Will be removed in a future release.
            query: Deprecated. Will be removed in a future release.
            include_cols: Deprecated. Will be removed in a future release.
            exclude_cols: Deprecated. Will be removed in a future release.
            limit: Deprecated. Will be removed in a future release.
            allow_deleted: Whether to include deleted sequences.

        Returns:
            The ``destination`` path that was written.

        .. API reference (generated - do not edit) ::

        **POST** ``/entities/{id}/_extract``

        Extract sequences

        API parameters:
            * ``id`` (path) -- Id of the document to extract rows from.
            * ``sort`` (query) -- Sort expression in the form "columnName:asc" or "columnName:desc".
            * ``pageOffset`` (query) -- Zero-based index of the first row to return.
            * ``pageLimit`` (query) -- Maximum number of rows to return.
            * ``includeCols`` (query) -- Comma-separated list of column names to include in the response.
            * ``excludeCols`` (query) -- Comma-separated list of column names to exclude from the response.
            * ``includeTotalCount`` (query) -- If true, include the total matching row count in the response.
            * ``includeHeaders`` (query) -- If true, include column header metadata in the response.
            * ``includeSortCols`` (query) -- If true, include hidden helper columns used for sorting.
            * ``allowDeleted`` (query) -- If true, also operate on the document when it has been soft-deleted.

        API request body:
            * ``filter`` (optional) -- Query expression, or list of query clauses, selecting matching rows.
            * ``options`` (optional) -- Additional query options.
            * ``selection`` (optional) -- Explicit row ranges to operate on instead of a filter.
            * ``sort`` (optional) -- Sort order to apply to the results.
            * ``jobId`` (optional) -- Id of an existing job to associate the extract with.

        .. end API reference ::
        """
        _deprecated = {'sort': sort, 'query': query, 'include_cols': include_cols,
                       'exclude_cols': exclude_cols, 'limit': limit}
        for name, value in _deprecated.items():
            if value is not None:
                warnings.warn(
                    f'Sequences.download: {name} is deprecated and will be removed in a future release. '
                    f'Use client.export() for filtering, sorting and column selection.',
                    DeprecationWarning,
                    stacklevel=2,
                )

        sort = sort if sort is not None else []
        sort_dicts = [s.to_json() for s in sort]

        # Build query parameters.
        include_sort_cols = True
        maybe_limit = f'pageLimit={limit}' if limit else None
        include_cols_joined = Sequences.get_joined_cols(include_cols, "includeCols")
        exclude_cols_joined = Sequences.get_joined_cols(exclude_cols, "excludeCols")
        maybe_include_sort_cols = f'includeSortCols={str(include_sort_cols).lower()}' if include_sort_cols else None
        allow_deleted_param = f'allowDeleted={str(allow_deleted).lower()}'
        query_string = '&'.join(
            query_param for query_param in
            [maybe_limit, include_cols_joined, exclude_cols_joined, maybe_include_sort_cols, allow_deleted_param]
            if query_param is not None
        )

        query = query if query is not None else ''
        body = {
            'filter': query,
            'sort': sort_dicts,
        }

        file_path = Sequences._get_filepath_for_entity_id(entity_id)
        url = f'entities/{entity_id}/_extract?{query_string}'
        print(f'Downloading shards from "{url}" to "{file_path}".')

        paths = []
        with self._session.post(url, stream=True, timeout=10 * 60, json=body) as response:
            try:
                links = response.json()
                print('links', links)
                if 'statusCode' in links and links['statusCode'] != 200:
                    raise Exception(links['message'])
                elif len(links) == 0:
                    raise Exception(
                        f'Sequences:download - Error; no download links for {entity_id}. Does the table exist?')

                index = 0
                for link in links:
                    path = f'{file_path}-{index}.gz'
                    response = urlopen(link)
                    with open(path, 'wb') as file:
                        file.write(response.read())
                    paths.append(path)
                    index = index + 1

            except Exception as e:
                print('Sequences:download - error:', e)
                raise e

        sorted_paths = self._get_sorted_file_shard_list(entity_id, paths, sort)

        print(f'Unzipping: entity_id={entity_id} to destination={destination}')

        skip_first = False

        if self._is_aws:
            for file_shard in sorted_paths:
                self.convert_parquet_to_tsv(file_shard, destination, skip_header=False)
        else:
            with open(destination, 'wb+') as target_file:
                for file_shard in sorted_paths:
                    with gzip.open(file_shard, 'rb') as g_zip_file:
                        first_line = True
                        for line in g_zip_file:
                            # We skip the first line of every file, except for the very first.
                            if not (first_line and skip_first):
                                line = Sequences._sanitize(line.decode("utf-8"))
                                target_file.write(line.encode("utf-8"))
                            first_line = False
                    # We skip the first line of every file, except for the very first.
                    skip_first = True

        return destination

    @staticmethod
    def get_joined_cols(cols, parameter):
        return f'{parameter}={",".join(cols)}' if cols else None

    @staticmethod
    def _sanitize(line: str) -> str:
        if '"' not in line:
            return line
        else:
            sanitized_line = []
            ending = "\n" if line.endswith("\n") else ""
            splits = line.rstrip("\n").split("\t")
            for split in splits:
                if not split.startswith('"'):
                    sanitized_line.append(split)
                else:
                    sanitized_line.append(split[1:-1].replace('""', '"'))
        return '\t'.join(sanitized_line) + ending

    @staticmethod
    def _get_filepath_for_entity_id(entity_id: any, extension='tsv'):
        file_name = f'{entity_id}.{extension}'
        return os.path.join(tempfile.gettempdir(), file_name)

    def _get_sorted_file_shard_list(self, entity_id: str, file_shard_list: List[str], sort: list):
        """
        Sorts the file_shard_list to ensure that the shards can be stitched back together in the correct order
        This is needed as the response 'chunks' are not necessarily named in the correct order.

        :param entity_id: - document to download
        :param file_shard_list: List[str] - All of the file names of the shards
        :param sort: List[Sort] - list of sorts applied, processed in order, same way SQL does, so order matters
        :return:  List[str] - All of the file names of the shards ordered by the sort
        """

        if sort is None or len(sort) == 0:
            return file_shard_list

        all_fields = self._entities.get_fields(entity_id=entity_id)

        shard_first_data_lines = []

        # get values of sort columns for first data line of each shard
        for file_shard in file_shard_list:
            with gzip.open(file_shard, 'rt') as g_zip_file:
                tsv_reader = csv.reader(g_zip_file, delimiter="\t")
                lines = 2
                header = None
                file_details = {'file_shard': file_shard}

                # reads the first line and headers of each files and pull out
                # all the values we need to sort on
                for i in range(lines):
                    row = next(tsv_reader)
                    if i == 0:
                        header = row
                    else:
                        for sort_column in sort:
                            col_id = sort_column.col_id
                            field = [x for x in all_fields if x.name == col_id][0]
                            col_index = header.index(col_id)
                            # Column.parse returns None for empty string INTEGER/NUMERIC columns,
                            # ideally would change that, but consequences unclear
                            # so overriding that to 0, otherwise take Column.parse output
                            parsed_value = float('-inf') \
                                if (field.kind == TableColumnType.INTEGER or field.kind == TableColumnType.NUMERIC) \
                                   and row[col_index] == '' \
                                else field.parse(row[col_index])
                            file_details[col_id] = parsed_value

            shard_first_data_lines.append(file_details)

        sorted_shard_first_lines = []
        # sort the shards, in reverse order, so last one done is primary sort
        sort.reverse()
        for column_to_sort in sort:
            sorted_shard_first_lines = sorted(shard_first_data_lines,
                                              key=lambda x: x[column_to_sort.col_id],
                                              reverse=column_to_sort.sort == 'desc')

        return list(map(lambda x: x['file_shard'], sorted_shard_first_lines))

    def create_signed_upload(self, entity_id: str, retries: int = 5) -> dict:
        """Create a signed upload slot for sequence data.

        Retries with a short backoff on failure.

        Args:
            entity_id: Id of the document to upload sequences into.
            retries: Number of remaining retry attempts.

        Returns:
            The signed-upload response object.

        .. API reference (generated - do not edit) ::

        **POST** ``/sequences/signed-upload/{entityId}``

        Create a signed upload

        Start a signed upload; Upload sequences in bulk.

        API parameters:
            * ``entityId`` (path) -- Id of the entity the signed upload writes sequences into.
            * ``allowDeleted`` (query) -- If true, also operate on the entity when it has been soft-deleted.

        API request body:
            * ``location`` -- Can help with upload speeds

        .. end API reference ::
        """
        try:
            response = self._session.post(f'sequences/signed-upload/{entity_id}')
            print('Prepare upload: response.text', response.text)
            print('Prepare upload: response.status', response.status_code)
            return response.json()
        except Exception as error:
            print('Prepare upload error: ', error)
            traceback.print_exc()
            if retries > 0:
                print('Prepare upload error, retrying', retries)
                time.sleep(5)
                return self.create_signed_upload(entity_id, retries - 1)
            else:
                raise error

    @staticmethod
    def maybe_compress_file(file_path) -> str:
        key = 'COMPRESS_BIGQUERY_UPLOADS'
        if key in os.environ:
            # Intentional string comparison, environment variables are always strings.
            should_compress = os.environ[key] == 'true'
            print(f'environment variable "{key}"="{should_compress}"')
            if should_compress:
                original_gz_size = Path(file_path).stat().st_size
                print(f'Original size:{original_gz_size}')
                check_call(['gzip', file_path])
                zipped_file_path = file_path + '.gz'
                zipped_gz_size = Path(zipped_file_path).stat().st_size
                print(f'Gzipped size:{zipped_gz_size} ')
                return zipped_file_path
            else:
                pass
        else:
            print(f'environment variable "{key}" not set. Not compressing.')
        return file_path

    def upload(self, url: str, file_path: str, headers: dict = None, retries: int = 5) -> None:
        """Upload a local file to a signed URL, retrying on connection errors.

        Args:
            url: The signed URL to PUT the data to.
            file_path: Path to the local file to upload.
            headers: Optional headers to include (e.g. for server-side
                encryption).
            retries: Number of remaining retry attempts.

        Raises:
            Exception: If the upload times out after exhausting retries.
        """
        if retries == 0:
            raise Exception('Upload has timed out.')

        zipped_file_path = self.maybe_compress_file(file_path)
        with open(zipped_file_path, 'rb') as f:
            try:
                print('upload starting')
                print(f'remaining retries={retries}, uploading to:{url}')
                # Pass headers to the PUT request if provided (for server-side encryption)
                response = requests.put(url, data=f, headers=headers, timeout=10 * 60)
                print('upload: response.text', response.text)
                print('upload: response.status', response.status_code)
                print('upload:ok')
            except requests.exceptions.ConnectionError as e:
                track = traceback.format_exc()
                print(track)
                # RECURSION !!!! - Pass headers in recursive call
                self.upload(url, file_path, headers, retries - 1)

    def import_signed_upload(self,
                             import_details: Dict,
                             allow_deleted_entity: bool = True,
                             remaining_retries: int = 10) -> bool:
        """Trigger import of a previously uploaded file, polling to completion.

        Handles network errors, HTTP errors, rate limits and "already exists"
        responses with exponential backoff.

        Args:
            import_details: The import descriptor returned by the upload step.
            allow_deleted_entity: Whether to allow importing into a deleted
                entity.
            remaining_retries: Number of remaining retry attempts.

        Returns:
            ``True`` when the import succeeds.

        Raises:
            ImportError: If the import finishes in a failed state.
            Exception: On unexpected states or exhausted network retries.

        .. API reference (generated - do not edit) ::

        **POST** ``/sequences/import-signed-upload``

        Import signed upload

        Finish a signed upload; Upload sequences in bulk.

        API parameters:
            * ``allowDeletedEntity`` (query) -- If true, allow referencing an entity that has been soft-deleted.
            * ``format`` (query) -- Format of the uploaded sequence data.

        API request body:
            * ``schema`` -- Column schema describing the uploaded sequence data.
            * ``entityId`` -- Id of the entity the uploaded data is imported into.
            * ``id`` -- Id returned when the signed upload was created.
            * ``location`` -- Can help with upload speeds

        .. end API reference ::
        """
        sleep_seconds = min(5 * (2 ** (10 - remaining_retries)), 1200)

        print(f'Import starting, remaining_retries={remaining_retries}', flush=True)
        query_string = f'?allowDeletedEntity=true' if allow_deleted_entity else ''
        url = f'sequences/import-signed-upload{query_string}'

        try:
            response = self._session.post(url,
                                          json=import_details,
                                          timeout=10 * 60)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            if remaining_retries > 0:
                print(
                    f'Network error: {e}. '
                    f'Sleeping for {sleep_seconds}s before retry '
                    f'(retries left: {remaining_retries})',
                    flush=True
                )
                time.sleep(sleep_seconds)
                return self.import_signed_upload(import_details, allow_deleted_entity, remaining_retries - 1)
            else:
                print(
                    f'Network error: {e}. '
                    f'No retries left. Failing hard.',
                    flush=True
                )
                raise e

        if response.status_code not in [200, 201] and remaining_retries > 0:
            # In case of HTTP error responses
            print(
                f'http error. Response.status_code={response.status_code}'
                f'sleeping for {sleep_seconds}s before retry '
                f'(retries left: {remaining_retries})',
                flush=True
            )
            time.sleep(sleep_seconds)
            # RECURSION!!!
            return self.import_signed_upload(import_details, allow_deleted_entity, remaining_retries - 1)

        response_json = response.json()
        print(f'Import ok, status={response_json}', flush=True)
        print(f'Import response.status={response.status_code}', flush=True)

        state: str = response_json['state']
        errors: List[str] = response_json['errors'] if 'errors' in response_json else []
        running = state in ['RUNNING', 'PENDING']
        done = state in ['DONE', 'SUCCESS']
        failed = done and len(errors) > 0
        success = done and len(errors) == 0

        if success:
            print(f'Import success', flush=True)
            return True
        elif running and remaining_retries > 0:
            print(
                f'state={state}, '
                f'sleeping for {sleep_seconds}s before retry '
                f'(retries left: {remaining_retries})',
                flush=True
            )
            time.sleep(sleep_seconds)
            # RECURSION!!!
            return self.import_signed_upload(import_details, allow_deleted_entity, remaining_retries - 1)
        elif failed:
            print('Errors:', errors, flush=True)

            # If we hit a rate limit then we should wait and try again.
            has_rate_limit_error = any(error.startswith('Exceeded rate limits') for error in errors)
            # If the request has already been submitted but has not completed then we should wait and try again.
            has_already_exists_error = any(error.startswith('Already Exists') for error in errors)

            if (has_rate_limit_error or has_already_exists_error) and remaining_retries > 0:
                print(
                    f'has_rate_limit_error={has_rate_limit_error}, '
                    f'has_already_exists_error={has_already_exists_error}, '
                    f'sleeping for {sleep_seconds}s before retry '
                    f'(retries left: {remaining_retries})',
                    flush=True
                )
                time.sleep(sleep_seconds)
                # RECURSION!!!
                return self.import_signed_upload(import_details, allow_deleted_entity, remaining_retries - 1)
            else:
                raise ImportError('import_signed_upload:error')
        else:
            raise Exception(f'Unexpected state={state}')

    @staticmethod
    def convert_parquet_to_tsv(path_to_parquet_data: str,
                               path_to_tsv_file: str,
                               skip_header: bool = False,
                               chunk_size: int = 10000) -> None:
        """Convert a Parquet shard to TSV, appending to the output file.

        Args:
            path_to_parquet_data: Path to the input Parquet file.
            path_to_tsv_file: Path to the output TSV file (overwritten on the
                first chunk, appended thereafter).
            skip_header: If ``True``, do not write a header row.
            chunk_size: Number of rows to convert per chunk.
        """
        import pyarrow.parquet as pq
        table_data = pq.read_table(path_to_parquet_data)

        if os.path.exists(path_to_tsv_file):
            os.remove(path_to_tsv_file)

        # Convert the table in chunks to CSV format. We convert each chunk to a Pandas dataframe because it allows
        # us to write the data without adding quotes, which the Pyarrow CSV writer does not.
        import csv
        for i in range(0, table_data.num_rows, chunk_size):
            chunk = table_data.slice(i, chunk_size)
            # NOTE: We cast integers with nulls to object because otherwise Pandas will convert them to floats,
            #       which can cause downstream issues, e.g. because 354 becomes 354.0, which BigQuery refuses to
            #       import as an integer.
            chunk_as_df = chunk.to_pandas(integer_object_nulls=True)
            # Convert all boolean columns to lowercase string.
            boolean_columns = list(chunk_as_df.select_dtypes(include='bool').columns)
            for boolean_col in boolean_columns:
                chunk_as_df[boolean_col] = chunk_as_df[boolean_col] \
                    .astype(str) \
                    .apply(lambda x: x.lower() if x is not None and str(x) != 'nan' else '')
            write_header = not skip_header and i == 0
            chunk_as_df.to_csv(
                path_to_tsv_file,
                sep='\t',
                mode='a',
                header=write_header,
                index=False,
                quoting=csv.QUOTE_NONE,
            )
