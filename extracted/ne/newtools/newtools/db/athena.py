# (c) 2012-2018 Deductive, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)
import logging
import os
from typing import Optional

from newtools.aws import S3Location
from newtools.doggo import CSVDoggo
from newtools.optional_imports import boto3, AWSRetry
from newtools.queue import TaskQueue
from newtools.db.data_types import ALL_TYPES


class AthenaClient(TaskQueue):
    """
    A client for AWS Athena that runs queries against Athena.
    Includes queuing functionality to run multiple queries and wait until they have completed.

    We can generate a CREATE TABLE Athena query using the .get_ct_query() function.
    To use this class, we have the following example:

    .. code-block:: python

        from newtools import AthenaClient
        from newtools.db.data_types import StringType, TimestampType

        ac = AthenaClient(**kwargs)
        query = ac.get_ct_query(
            table_name='test_table',
            s3_location='s3://test-bucket/test_prefix',
            column_schema={
                'COL1': StringType(),
                'COL2': TimestampType(),
            },
            partition_columns={
                'COL3': StringType()
            },
            partition_projection={
                'COL3': {
                    'type': 'date',
                    'lookback': '2MONTHS'
                }
            }
        )
    """

    def __init__(self, region, db, max_queries=3, max_retries=3, query_terminating=True,
                 df_handler=None, workgroup=None, logger=logging.getLogger("newtools.athena")):
        """
        Create an AthenaClient

        :param region: the AWS region to create the object, e.g. us-east-2
        :param max_queries: the maximum number of queries to run at any one time, defaults to three
        :type max_queries: int
        :param max_retries: the maximum number of times execution of the query will be retried on failure
        :type max_retries: int
        :param query_terminating: whether to terminate all queries when deleting the class
        :type query_terminating bool
        :param workgroup: optional workgroup for AWS Athena
        :type workgroup string
        :param logger: the logger to use for this class and any newtools classes created by this class
        """
        self.df_handler = CSVDoggo() if df_handler is None else df_handler
        self.athena = boto3.client(service_name='athena', region_name=region)
        self.db_name = db
        self.aws_region = region
        self.query_terminating = query_terminating
        self._workgroup = workgroup
        self._logger = logger
        self.sql_dir = os.path.join(os.path.dirname(__file__), 'sql')

        super(AthenaClient, self).__init__(max_queries, max_retries)

    def __del__(self):
        """
        when deleting the instance, ensure that all associated tasks are stopped and do not enter the queue
        """
        if self.query_terminating:
            self.stop_and_delete_all_tasks()

    @AWSRetry.backoff(added_exceptions=["ThrottlingException"])
    def _update_task_status(self, task):
        """
        Gets the status of the query, and updates its status in the queue.
        Any queries that fail are reset to pending so they will be run a second time
        """

        if task.id is not None:
            self._logger.debug(
                "...checking status of query {0} to {1}".format(task.name, task.arguments["output_location"]))
            status = self.athena.get_query_execution(QueryExecutionId=task.id)["QueryExecution"]["Status"]

            if status["State"] in ("RUNNING", "QUEUED"):
                task.is_complete = False
            elif status["State"] == "SUCCEEDED":
                task.is_complete = True
            else:
                task.error = status.get("StateChangeReason", status["State"])
        else:
            task.is_complete = True

    def _trigger_task(self, task):
        """
        Runs a query in Athena
        """

        self._logger.info("Starting query {0}, remaining {2}, output to to {1},".format(
            task.name,
            task.arguments["output_location"],
            self.time_remaining))

        # Set up the kwargs, excluding any None values
        kwargs = {k: v for (k, v) in {
            "QueryString": task.arguments["sql"],
            "QueryExecutionContext": {'Database': self.db_name},
            "ResultConfiguration": {'OutputLocation': task.arguments["output_location"]},
            "WorkGroup": self._workgroup,
            "ResultReuseConfiguration": task.arguments['caching']
        }.items() if v is not None}

        task.id = self.athena.start_query_execution(**kwargs)["QueryExecutionId"]

    def add_query(self, sql, name=None, output_location=None, caching=0):
        """
        Adds a query to Athena. Respects the maximum number of queries specified when the module was created.
        Retries queries when they fail so only use when you are sure your syntax is correct!
        Returns a query object
        :param sql: the SQL query to run
        :param name: an optional name which will be logged when running this query
        :param output_location: the S3 prefix where you want the results stored (required if workgroup is not specified)
        :param caching: if greater than 0 represents the max age in minutes a query can be to reuse the result Athena3
        :return: a unique identified for this query
        """
        return self.add_task(
            name=sql[:255] if name is None else name,
            args={"sql": sql,
                  "output_location": None if output_location is None else S3Location(output_location).s3_url,
                  "caching": None if caching <= 0 else {'ResultReuseByAgeConfiguration': {'Enabled': True,
                                                                                          'MaxAgeInMinutes': caching}}})

    def wait_for_completion(self):
        """
        Check if jobs have failed, if so trigger deletion event for AthenaClient,
        else wait for completion of any queries .
        Will automatically remove all pending and stop all active queries upon completion.
        """
        try:
            super(AthenaClient, self).wait_for_completion()
        except Exception as e:
            raise e
        finally:
            self.stop_and_delete_all_tasks()

    def get_query_result(self, query):
        """
        Returns Pandas DataFrame containing query result if query has completed
        :param query: the query ID returned from add_query()
        """
        self._update_task_status(query)

        if query.is_complete:
            response = self.athena.get_query_execution(QueryExecutionId=query.id)
            filepath = response['QueryExecution']['ResultConfiguration']['OutputLocation']
            self._logger.info("Fetching results from {}".format(filepath))
            df = self.df_handler.load_df(filepath)
            return df
        else:
            raise ValueError("Cannot fetch results since query hasn't completed")

    def _stop_all_active_tasks(self):
        """
        iterates through active queue and stops all queries from executing
        :return: None
        """
        while self.active_queue:
            task = self.active_queue.pop()
            if task.id is not None:
                self._logger.info("Response while stop_query_execution with following QueryExecutionId {}; {}"
                                  .format(task.id, self.athena.stop_query_execution(QueryExecutionId=task.id)))

    def stop_and_delete_all_tasks(self):
        """
        stops active tasks and removes pending tasks for a given client
        :return: None
        """
        self._empty_pending_queue()
        self._stop_all_active_tasks()

    @staticmethod
    def get_sql(
        sql_loc: str
    ) -> str:
        """
        Function to return the SQL file as an un-formatted string.

        :param sql_loc: the location of the sql to load
        """
        with open(sql_loc) as f:
            return f.read()

    def get_ct_query(
        self,
        table_name: str,
        s3_location: S3Location,
        column_schema: dict,
        partition_columns: Optional[dict] = None,
        partition_projection: Optional[dict] = None,
        db_name: Optional[str] = None,
        file_format: Optional[str] = 'PARQUET'
    ) -> str:
        """
        Function to generate a CREATE TABLE query for Athena.

        :param table_name: the name for the table
        :param s3_location: the s3 location where the data is stored
        :param column_schema: a dictionary of column names along with data types
        :param partition_columns: a dictionary of column names along with data types specifically for partition columns
        :param partition_projection: a dictionary with information about the partition columns for the projection
            for example,
                {
                    'column_name_1': {
                        'type': 'date'
                    },
                    'column_name_2': {
                        'type': 'enum',
                        'values': ['val1', 'val2']
                    },
                    'column_name_3': {
                        'type': 'date',
                        'lookback': '1MONTH'
                    }
                }
            see here for more information on formats for specific variables:
            https://docs.aws.amazon.com/athena/latest/ug/partition-projection-supported-types.html
        :param db_name: the database to create the table in (will default to db from __init__ if not provided)
        :param file_format: one of 'PARQUET' or 'CSV'
        """
        file_format = file_format.upper()
        assert file_format in ['PARQUET', 'CSV'], f"The file format must be one of CSV or PARQUET, not {file_format}"

        self._logger.info("Loading CREATE TABLE query template")
        query = self.get_sql(sql_loc=os.path.join(self.sql_dir, 'create_table.sql'))
        db_name = db_name if db_name else self.db_name

        partitioned_by = ''
        if partition_columns:
            partitioned_by = f'PARTITIONED BY (\n  {self.get_column_schema(partition_columns)}\n)'

        if partition_projection:
            # ensure all partition columns have a projection
            missing_part_cols = set(partition_columns.keys()).difference(partition_projection.keys())
            assert not missing_part_cols, f"Columns {missing_part_cols} do not projection information"

        self._logger.info("Generating CREATE TABLE query")
        return query.format(
            database_name=db_name.lower(),
            table_name=table_name.lower(),
            columns=self.get_column_schema(column_schema),
            partitioned_by=partitioned_by,
            row_format_serde=self.get_rfs(file_format),
            external_location=s3_location,
            tbl_properties=self.get_tbl_props(file_format, partition_projection)
        )

    @staticmethod
    def get_column_schema(
        column_schema: dict
    ) -> str:
        """
        Function to return a string of the column schema for CREATE TABLE Athena queries.
        """
        errors = []
        for type_ in column_schema.values():
            if not any(isinstance(type_, ele) for ele in ALL_TYPES):
                errors.append(type_)

        if errors:
            raise AssertionError(
                f"Column types "
                f"{errors} "
                f"must be one of the supported types: "
                f"{[i.__name__ for i in ALL_TYPES]}"
            )

        return ",\n  ".join([f"{column} {type_.ATHENA_TYPE}" for column, type_ in column_schema.items()])

    @staticmethod
    def get_rfs(
        file_format: str
    ) -> str:
        """
        Return the ROW FORMAT SERDE property for the Athena table depending on the file format.

        :param file_format: either 'PARQUET' or 'CSV'
        """
        if file_format == 'PARQUET':
            hive_format = 'ql.io.parquet.serde.ParquetHiveSerDe'
        else:
            hive_format = 'serde2.OpenCSVSerde'

        return f'org.apache.hadoop.hive.{hive_format}'

    def get_tbl_props(
        self,
        file_format: str,
        partition_proj: Optional[dict] = None
    ) -> str:
        """
        Get the TBLPROPERTIES property for the Athena table.

        :param file_format: either 'PARQUET' or 'CSV'
        :param partition_proj: a dictionary with information about the partition columns for the projection
        """
        if file_format == 'PARQUET':
            tbl_props = {
                'classification': 'parquet',
                'compressionType': 'snappy'
            }
        else:
            tbl_props = {
                'skip.header.line.count': '1'
            }

        if partition_proj:
            tbl_props.update({'projection.enabled': 'TRUE'})
            for column in partition_proj:
                tbl_props.update(self.get_partition_projection_props(column, partition_proj[column]))

        return ",\n  ".join(f"'{k}' = '{v}'" for k, v in tbl_props.items())

    @staticmethod
    def get_partition_projection_props(
        column: str,
        metadata: dict
    ) -> dict:
        """
        Function to return the TBLPROPERTIES for the partition projection for the given column.

        :param column: the colum name
        :param metadata: metadata for the properties
        """
        if metadata.get('type') == 'date':
            lookback_window = metadata.get('lookback') if 'lookback' in metadata else '2YEARS'

            return {
                f'projection.{column}.format': 'yyyy-MM-dd',
                f'projection.{column}.interval': '1',
                f'projection.{column}.interval.unit': 'DAYS',
                f'projection.{column}.range': f'NOW-{lookback_window},NOW',
                f'projection.{column}.type': 'date'
            }

        elif metadata.get('type') == 'enum':
            enum_values = metadata.get('values')
            assert enum_values, f"No enum values have been provided for partition projection on column: {column}"
            assert isinstance(enum_values, list), "The values for an enum partition projection must be a LIST"

            return {
                f'projection.{column}.values': ','.join(enum_values),
                f'projection.{column}.type': 'enum'
            }

        else:
            raise ValueError(f"Partition projection type {metadata.get('type')} is not supported")
