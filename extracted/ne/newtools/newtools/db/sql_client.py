import logging
import os
import csv
import datetime
from importlib import import_module
from io import BytesIO

from newtools.aws import S3Location
from newtools.optional_imports import boto3, pandas as pd, sqlparse


def _clean_dict(d):
    block_words = ["secret", "password"]
    clean = dict()
    for param in d:
        if any(x.lower() in param.lower() for x in block_words):
            clean[param] = "*" * len(d[param])
        else:
            clean[param] = d[param]

    return clean


class QueryArchiver:
    _archive = None

    def __init__(self, file):
        self._file = file
        self._archive = BytesIO()

    @property
    def is_s3(self):
        return self._file.startswith('s3://')

    @property
    def am_archiving(self):
        return self._file is not None

    def __enter__(self):
        if self.am_archiving and not self.is_s3:
            os.makedirs(os.path.dirname(self._file), exist_ok=True)

            # clear the file
            open(self._file, 'w').close()

        return self

    def log(self, logged_query, parameters):
        if self.am_archiving:
            self._archive.write(
                '-- Ran query on: {:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now()).encode('utf-8'))
            self._archive.write('-- Parameters: {0}\n'.format(_clean_dict(parameters)).encode('utf-8'))
            self._archive.write(logged_query.encode('utf-8') + b';\n')

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self.am_archiving:
            self._archive.seek(0)
            if self.is_s3:
                s3_path = S3Location(self._file)
                s3 = boto3.client('s3')
                _ = self._archive.read()  # boto closes this, but i want to keep it just in case
                self._archive.seek(0)
                s3.upload_fileobj(self._archive, s3_path.bucket, s3_path.key)
            else:
                with open(self._file, 'wb') as f:
                    f.write(self._archive.read())


class ParamParser:
    """
    Class to parse SQL parameters into a common format
    """

    named_styles = {
        'named': ':{name}',
        'pyformat': '%({name}){type}'
    }

    sequence_styles = {
        'qmark': '?',
        'numeric': ':{index}',
        'format': '%{type}',
    }

    styles = {**named_styles, **sequence_styles}

    index = 0

    def _get_param(self, param):
        self.index = self.index + 1
        return self.styles[self.paramstyle].format(name=param, type="s", sequence=self.index)

    def __init__(self, paramstyle, logger):
        self.paramstyle = paramstyle
        logger.debug("Queries will use paramstyle = {0}".format(paramstyle))
        if paramstyle not in ('pyformat', 'qmark'):  # pragma: nocover
            logger.warning("The paramstyle {0} has not been tested and may not work".format(paramstyle))

    @staticmethod
    def parse_for_logging(sql, params):

        return sql.format(**_clean_dict(params))

    def parse_sql_params(self, sql, params):

        # validate
        self.parse_for_logging(sql, params)
        if len(params) > 0:
            self.index = 0
            new_sql = ""
            new_params = []
            for segment in sql.replace("'{", "{").replace("}'", "}").replace("{", "}").split("}"):
                if segment in params:
                    new_sql = new_sql + self._get_param(segment)
                    new_params.append(params[segment])
                else:
                    new_sql = new_sql + segment

            if self.paramstyle in self.named_styles:  # pragma: nocover
                # this is not tested because we only have sql lite client for testing which does not support
                # named params.
                return new_sql, params
            else:
                return new_sql, new_params
        else:
            return sql, params


class SqlClient:
    """
    A wrapper for PEP249 connection objects to provide additional logging and simple execution
    of queries and optional writing out of results to DataFrames or CSV

    The client runs multi-statement SQL queries from file or from strings and can return the
    result of the final SQL statement in either a DataFrame or as a CSV.

    Archives the text of the executed queries to an optionally specified location.

    Parameters:
    - db_connection - a connection object from a PEP249 compliant class
    """

    def __init__(self,
                 db_connection,
                 logging_level=logging.DEBUG,
                 log_query_text=False,
                 logger=logging.getLogger("newtools.sql_client")):

        self._logger = logger
        self.connection = db_connection
        self.cursor = self.connection.cursor()
        paramstyle = import_module(db_connection.__class__.__module__.split(".")[0]).paramstyle
        self.parser = ParamParser(paramstyle, self._logger)
        self.logging_level = logging_level
        self._counter = 0
        self._log_query_text = log_query_text

    def _log_query(self, query, parameters):
        self._logger.log(self.logging_level, "Executing part {0}: {1}".format(self._counter, query.split("\n")[0]))
        self._logger.debug("Parameters {0}".format(_clean_dict(parameters)))

        if self._log_query_text:
            for line in query.split("\n"):
                self._logger.log(self.logging_level, "{0:03} {1}".format(self._counter, line))
                self._increment_counter()

    def _report_rowcount(self, execution_time):
        if self.cursor.rowcount >= 0:
            self._logger.log(self.logging_level, "Completed in {0}s. {1} rows affected".format(
                execution_time.seconds,
                self.cursor.rowcount))
        else:
            self._logger.log(self.logging_level, "Completed in {0}s".format(execution_time.seconds))

    def _get_queries(self, query_file, replace):
        replace = dict() if replace is None else replace
        if query_file[-4:] == ".sql":
            if os.path.isfile(query_file):
                self._logger.log(self.logging_level, "Loading query from {0}".format(query_file))
                f = open(query_file, "r")
                text = f.read()
                f.close()
            else:
                self._logger.error("File {0} does not exist".format(query_file))
                raise OSError("File {0} does not exist".format(query_file))
        else:
            text = query_file

        for key in replace:
            text = text.replace(key, replace[key])

        # split into multiple commands....
        if ';' in text:
            # use sql parse if installed, otherwise split on every ;
            generator = sqlparse.split(text)

            # split into multiple commands....
            for command in generator:
                if command.strip() not in ["", "';'"]:
                    yield command.strip()
        else:
            yield text.strip()

    def _run_and_log_sql(self, command, parameters, query_archiver, pandas=False, dry_run=False):
        parameters = dict() if parameters is None else parameters

        sql, params = self.parser.parse_sql_params(command, parameters)

        df = None

        if command != '':
            self._log_query(command, parameters)
            query_archiver.log(self.parser.parse_for_logging(command, parameters), parameters)
            start_time = datetime.datetime.now()
            if not dry_run:
                if pandas:
                    df = pd.read_sql(sql,
                                     self.connection,
                                     params=params)
                else:
                    self.cursor.execute(sql, params)

                self._report_rowcount(datetime.datetime.now() - start_time)

        return df

    def _reset_counter(self):
        self._counter = 1

    def _increment_counter(self):
        self._counter = self._counter + 1

    def _execute_queries(self, queries, parameters, first_to_run, query_archiver, dry_run):
        self._reset_counter()
        for command in queries:
            if self._counter >= first_to_run:
                self._run_and_log_sql(command=command,
                                      parameters=parameters,
                                      pandas=False,
                                      query_archiver=query_archiver,
                                      dry_run=dry_run
                                      )
            self._increment_counter()

    def execute_query(self, query, parameters=None, replace=None, first_to_run=1, archive_query=None, dry_run=False):
        """
        Runs a query and ignores any output

        Parameters:
        - query - the query to run, either a SQL file or a SQL query
        - parameters - a dict of parameters to substitute in the query
        - replace - a dict or items to be replaced in the SQL text
        - first_to_run - the index of the first query in a multi-command query to be executed
        - archive_query - save the query that is run to file. Default=False,

        """
        with QueryArchiver(archive_query) as archiver:
            self._execute_queries(queries=self._get_queries(query, replace),
                                  parameters=parameters,
                                  first_to_run=first_to_run,
                                  query_archiver=archiver,
                                  dry_run=dry_run)

        self.connection.commit()

    def execute_query_to_df(self, query, parameters=None, replace=None, first_to_run=1, dry_run=False,
                            archive_query=None):
        """
        Runs a query and returns the output of the final statement in a DataFrame.

        Parameters:
        - query - the query to run, either a SQL file or a SQL query
        - parameters - a dict of parameters to substitute in the query
        - replace - a dict or items to be replaced in the SQL text
        - first_to_run - the index of the first query in a multi-command query to be executed
        - archive_query - save the query that is run to file. Default=False,

        """

        commands = [command for command in self._get_queries(query, replace)]

        with QueryArchiver(archive_query) as archiver:
            self._execute_queries(queries=commands[:-1],
                                  parameters=parameters,
                                  first_to_run=first_to_run,
                                  query_archiver=archiver,
                                  dry_run=dry_run)

            # now run the last one as a select
            df = self._run_and_log_sql(command=commands[-1],
                                       parameters=parameters,
                                       pandas=True,
                                       dry_run=dry_run,
                                       query_archiver=archiver)

        self.connection.commit()

        if not dry_run and len(df) == 0:
            self._logger.info("No results returned")
            return pd.DataFrame()
        else:
            return df

    def execute_query_to_csv(self,
                             query,
                             csvfile,
                             parameters=None,
                             replace=None,
                             append=False,
                             first_to_run=1,
                             archive_query=None,
                             dry_run=False):
        """
        Runs a query and writes the output of the final statement to a CSV file.

        Parameters:
        - query - the query to run, either a SQL file or a SQL query
        - csvfile - the file name to save the query results to
        - parameters - a dict of parameters to substitute in the query
        - replace - a dict or items to be replaced in the SQL text
        - first_to_run - the index of the first query in a multi-command query to be executed
        """
        with QueryArchiver(archive_query) as archiver:
            self._execute_queries(queries=self._get_queries(query, replace),
                                  parameters=parameters,
                                  first_to_run=first_to_run,
                                  query_archiver=archiver,
                                  dry_run=dry_run)

        if not dry_run:
            # delete an existing file if we are not appending
            if os.path.exists(csvfile) and append:
                file_mode = 'a'
            else:
                file_mode = 'w'

            # now get the data
            with open(csvfile, file_mode) as f:
                writer = csv.writer(f, delimiter=',')

                # write the header if we are writing to the beginning of the file
                if file_mode == 'w':
                    writer.writerow([desc[0] for desc in self.cursor.description])

                for row in self.cursor:
                    writer.writerow(row)
