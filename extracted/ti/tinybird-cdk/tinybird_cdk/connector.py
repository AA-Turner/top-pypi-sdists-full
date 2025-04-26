import csv
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import ndjson

from . import errors, logger, tinybird
from .export import URL, CloudDir, CloudFile, Data, LocalFile

@dataclass(frozen=True)
class Scope:
    name: str
    value: str

@dataclass(frozen=True)
class Table(Scope):
    num_rows: Optional[int]=None
    size: Optional[int]=None

class Connector:
    '''
    Abstract class with common API all connectors must implement.

    In particular, all concrete classes are context managers and should be used
    as such. That way, unexpected errors are still reported.
    '''
    def __init__(self):
        self.tb = tinybird.Client() # pylint: disable=invalid-name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, _exc_tb):
        if exc_type:
            logger.error(f'Exception raised: {exc_val!r}')
            if not issubclass(exc_type, errors.Error):
                # exc_val.message may not exist, just call str().
                raise errors.Error(str(exc_val)) from exc_val
        return False

    def query_tb(self, sql, pipe=None, scalar=False):
        return self.tb.query(sql, pipe=pipe, scalar=scalar)

class SQLConnector(Connector, ABC):
    '''
    Abstract class for connectors for SQL databases like MySQL or Snowflake.

    SQL connectors only have to implement ``_export()`` which is an internal
    method. They inherit the public API for end-users.
    '''

    SAMPLE_SIZE = 10

    # --- Abstract interface ----------------------------------------------------------------------

    @abstractmethod
    def get_scopes(self):
        '''Returns a tuple of scope codes and names, top first.'''

    @abstractmethod
    def list_scope(self, parents={}):
        '''Returns a list with the resources scoped to the given parents.'''

    @abstractmethod
    def suggest_schema(self, scopes):
        '''Returns a ClickHouse schema for the given table.'''

    # @abstractmethod
    # def ingest_query(self, schema, column_names):
    #     '''Returns the SQL query to be executed for data ingestion.'''

    @abstractmethod
    def _export(self, query: str, fmt: str, row_limit: int):
        '''Export the given query, and return an export object.'''

    @abstractmethod
    def _query(self, sql):
        '''Execute a query against the database and return the result set as list of dictionaries.'''

    #
    # --- Sample ----------------------------------------------------------------------------------
    #

    def sample(self, schema, column_names):
        query = self.ingest_query(schema, column_names)
        return self.query_db(f'{query} LIMIT {self.SAMPLE_SIZE}')

    # --- Query this connector's database ---------------------------------------------------------

    def query_db(self, sql, scalar=False):
        data = self._query(sql)
        if scalar:
            return list(data[0].values())[0] if data else None
        return data

    # --- Append ----------------------------------------------------------------------------------

    def append(self, query, data_source, fmt, row_limit: Optional[int]=None):
        export = self._export(query, fmt, row_limit)
        return self._append_export(export, data_source, fmt)

    def _append_export(self, export, data_source, fmt):
        try:
            if isinstance(export, Data):
                return self.tb.append_data(export.data, data_source, fmt)
            if isinstance(export, URL):
                return self.tb.append_url(export.url, data_source, fmt)
            if isinstance(export, LocalFile):
                return self.tb.append_file(export.path, data_source, fmt)
            if isinstance(export, CloudFile):
                url = export.client.public_url(export.bucket, export.key)
                return self.tb.append_url(url, data_source, fmt)
            if isinstance(export, CloudDir):
                if cat_key := export.client.cat(export.bucket, export.directory):
                    url = export.client.public_url(export.bucket, cat_key)
                    return self.tb.append_url(url, data_source, fmt)
                logger.info('No files found in directory, skipping append')
                return None
            raise Exception(f'Unknown export type {export!r}')
        finally:
            export.cleanup()

    # --- Replace ---------------------------------------------------------------------------------

    def replace(self, query: str, data_source: str, fmt, replace_condition=None, row_limit=None):
        export = self._export(query, fmt, row_limit=row_limit)
        logger.info("Query completed. Starting upload...")
        return self._replace_export(export, data_source, fmt, replace_condition)


    def _replace_export(self, export, data_source, fmt, replace_condition):
        try:
            if isinstance(export, Data):
                return self.tb.replace_data(export.data, data_source, fmt, replace_condition)
            if isinstance(export, URL):
                return self.tb.replace_url(export.url, data_source, fmt, replace_condition)
            if isinstance(export, LocalFile):   
                return self.tb.replace_file(export.path, data_source, fmt, replace_condition)
            if isinstance(export, CloudFile):
                url = export.client.public_url(export.bucket, export.key)
                return self.tb.replace_url(url, data_source, fmt, replace_condition)
            if isinstance(export, CloudDir):
                if cat_key := export.client.cat(export.bucket, export.directory):
                    url = export.client.public_url(export.bucket, cat_key)
                    return self.tb.replace_url(url, data_source, fmt, replace_condition)
                logger.info('No files found in directory, skipping replace')
                return None
            raise Exception(f'Unknown export type {export!r}')
        finally:
            export.cleanup()

    # --- Helpers ---------------------------------------------------------------------------------

    @staticmethod
    def _binary_tempfile(extension):
        return tempfile.NamedTemporaryFile(mode='wb', suffix=f'.{extension}', delete=False)

    @staticmethod
    def _text_tempfile(extension):
        return tempfile.NamedTemporaryFile(mode='wt', suffix=f'.{extension}', delete=False)

    def _to_csv_tempfile(self, rows):
        tmp = self._text_tempfile(extension='csv')
        csv.writer(tmp).writerows(rows)
        tmp.close()
        return tmp.name

    def _to_ndjson_tempfile(self, rows):
        tmp = self._text_tempfile(extension='ndjson')
        ndjson.dump(rows, tmp, default=str)
        tmp.close()
        return tmp.name

class CloudConnector(Connector):
    '''
    Superclass of connectors for cloud storage services.

    Subclasses are expected to have a ``client`` attribute with one of the
    standardized clients in ``tinybird_cdk.cloud``.
    '''
    def append(self, bucket, key, data_source, fmt):
        url = self.client.public_url(bucket, key)
        return self.tb.append_url(url, data_source, fmt)

    def replace(self, bucket, key, data_source, fmt, replace_condition=None):
        url = self.client.public_url(bucket, key)
        return self.tb.replace_url(url, data_source, fmt, replace_condition)

class StreamingConnector(Connector):
    '''
    Abstract class for all streaming connectors.

    Streaming connectors are expected to be used as context managers like the
    rest. They only need to implement a ``stream()`` method, which tipically
    runs their infinite loop.
    '''
    @abstractmethod
    def stream(self, stream_name, data_source):
        pass
