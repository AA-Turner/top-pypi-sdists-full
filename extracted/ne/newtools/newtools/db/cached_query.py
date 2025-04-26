# (c) Deductive 2012-2020, all rights reserved
# This code is licensed under MIT license (see license.txt for details)
"""


These classes provide functionality to cache database results locally or on S3 and only re-execute the database query if the query SQL or parameters have changed.

Cache structure
---------------

Each query is cached to the path specified in cache_path with a generated filename that uniquely represents the querythat has been run, for example:

``s3://cache_bucket/cache_prefix/get_results_5e5920011161b3081937572d25140237_ba98cb6452cf711ae0cec5c2dadc2585.csv.gz``

This is made up as follows:

* **s3://cache_bucket/cache_prefix/** - The path provided in the cache_path parameter when instantiating the class
* **get_results** - The first part of the file name represents the name of the query run, e.g. get_tune_in_outcomes.sql
* **5e5920011161b3081937572d25140237** - This is a unique hash calculated from the contents of the SQL file. When a new version of the file is created, a new hash will also be created.
* **ba98cb6452cf711ae0cec5c2dadc2585** - This is a unique hash calculated from the parameters passed to the SQL file. A new file is created for each set of parameters passed to the file
* **.csv.gz** - A fixed prefix, always set to “.csv.gz”

Caches can optionally be set to expiree very n seconds in which case the cache will appear as follows:
``s3://cache_bucket/cache_prefix/get_results_5e5920011161b3081937572d25140237_ba98cb6452cf711ae0cec5c2dadc2585_1616518700.csv.gz``

In this case 1616518700 refers to the epoch time, at which the n seconds starts for which this cache is valid. For example, if you set for the cache to be valid for 60 seconds then a
new cache will be created each minute

Hash collisions
---------------

The hash is designed to be unique for each execution of the SQL file but there is about a 1 in a million chance that we’ll get the same hash for two different SQL files. If this occurs then the campaign results should look like total garbage so please double check the QA reports before sending to a customer.

Archive queries
---------------

Each query that is run can be saved to an optionally specified sql_archive_path. In this location the full text of every executed query with the timestamp will be saved.

Params
------

When creating a CachedQuery class you specify a set of parameters that are used across all queries executed using the class. This can be used to store common parameters for queries such as access tokens and secrets.

Running multiple clients
------------------------

Before running the query, the client attempts to lock the file. This is either done by creating a .lock file with a similar name
or by creating a row in DynamoDB to lock the file. The table in DynamoDB is "newtools.dynamo.doggo.lock" in us-east-1 and contains one entry per locked files. Entries are typically deleted after the lock is released.

"""

import datetime
import hashlib
import json
import logging
import os
import re
import shutil
import time
from typing import Optional, List, Tuple, Iterator, Union, Any, Type

from newtools.aws import S3Location
from newtools.db.athena import AthenaClient
from newtools.db.sql_client import SqlClient
from newtools.doggo import DoggoLock, DoggoFileSystem, DynamoDogLock, FileDoggo, PandasDoggo

# Set S3fsMixin for backwards compatibility
S3fsMixin = DoggoFileSystem
Path = Union[str, S3Location]
DataFrame = Type['pd.DataFrame']
BotoSession = Type['boto3.Session']


class UselessLock:
    """
    Class to allow the use of a lock to be optional.
    """
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger("newtools.cached_query.UselessLock")

    def __enter__(self):
        self.logger.info("Acquiring useless lock")
        return self

    def __exit__(self, *_):
        self.logger.info("Releasing useless lock")


class BaseCachedClass:
    validation_mode = False
    _expiry_seconds = 0

    def __init__(
        self,
        cache_path,
        logger=logging.getLogger("newtools.cached_query"),
        expiry_seconds=0,
        boto_session: Optional[BotoSession] = None
    ) -> None:
        self.cache_path = cache_path
        self.dfs = DoggoFileSystem(boto3_session=boto_session) if boto_session else DoggoFileSystem()
        self._logger = logger
        self._expiry_seconds = expiry_seconds

    def _exists(self, path):
        """
        Checks whether a path exists locally or on S3

        :param path: the path to check
        :return: True if the path exists
        """
        if self.validation_mode:
            return True
        else:
            return self.dfs.exists(path)

    @staticmethod
    def _get_file_hash(files):
        """
        Returns a hash based on the file contents

        :param files: a list the file to hash
        :return: an MD5 hex digest
        """

        hasher = hashlib.md5()
        for file in files:
            with open(file, 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
        return hasher.hexdigest()

    @staticmethod
    def _get_dict_hash(*my_dicts):
        """
        Returns a hash based on a dictionary

        :param my_dicts: the dictionary/ies to hash
        :return: an MD5 hex digest
        """

        return hashlib.md5("".join([json.dumps(d, sort_keys=True) for d in my_dicts if d is not None])
                           .encode('utf-8')).hexdigest()

    def get_cache_path(self, prefix, files_to_hash, data_hash="", suffix=""):
        """
        Returns the location to cache the output to

        :param prefix: the name of the file
        :param files_to_hash: the name of the file to hash in the output name
        :param data_hash: an additional hash to add to the string
        :param suffix: a suffix to add to the end

        :return: the full path to cache to
        """

        data_hash = [] if data_hash == "" else [data_hash]

        hash_list = [prefix, self._get_file_hash(files_to_hash)] + data_hash

        if self._expiry_seconds > 0:
            # Truncate the epoch to the expiry seconds and add to the hash list
            # For example, if the epoch is 1616681824 and we are expiring every 100 seconds
            # the expiry time in the hash will be to set to 1616681800.
            #
            # This means than any query run before 1616681900 will use the same expiry hash
            # and pick up the cached version.
            epoch = int(int(time.time()))
            hash_list.append(str(epoch - epoch % self._expiry_seconds))

        file_format = self.get_cache_file_format(suffix)
        file_loc = "_".join(hash_list) + file_format

        if self.cache_path.startswith("s3://"):
            return S3Location(self.cache_path).join(file_loc)
        else:
            return os.path.join(self.cache_path, file_loc)

    @staticmethod
    def get_cache_file_format(
        suffix: str
    ) -> str:
        """
        Return the file format for the cache path.
        """
        return ".csv" + suffix


class BaseCachedQuery(BaseCachedClass):
    _archive_path = None
    _redshift_checks = False

    wait_period = 30
    time_out_seconds = 1800
    maximum_age = 3600

    def __init__(self, params=None, cache_path="", sql_archive_path=None, sql_paths=None, gzip=True,
                 dynamodb_lock=True, logger=logging.getLogger("newtools.cached_query"), expiry_seconds=0,
                 use_lock: Optional[bool] = True, boto_session: Optional[BotoSession] = None):
        """
        Cached query class

        :param params: a dictionary of parameters passed to each query
        :param cache_path: the path locally or on S3 to cache query results
        :param sql_archive_path: the path locally or on S3 to store archive SQL queries
        :param sql_paths: path or a list of paths to search for SQL queries
        :param gzip: if set, then results will be compression
        :param dynamodb_lock: defaults to True, using Dynamo DB for locking in S3
        :param logger: the logger to use for this class and any newtools classes created by this class
        :param expiry_seconds: if set, caches files we expire every expiry_seconds seconds.
        :param use_lock: whether to use a lock to prevent concurrent s3 access
            if set to False, dynamodb_lock parameter wll be ignored
        :param boto_session: a specific boto3 session to be used
        """
        super().__init__(cache_path, logger, expiry_seconds, boto_session=boto_session)

        self._logger = logger
        self._gzip = gzip
        self._args = self._validate_args(params)

        self._sql_paths = ['sql', os.path.join(os.path.split(__file__)[0], 'sql')]
        if sql_paths is not None:
            if not isinstance(sql_paths, list):
                sql_paths = [sql_paths]
            self._sql_paths = sql_paths + self._sql_paths

        self._archive_path = sql_archive_path

        if not use_lock:
            self._aws_lock = UselessLock
        elif dynamodb_lock:
            self._aws_lock = DynamoDogLock
        else:
            self._aws_lock = DoggoLock

    def _get_lock(self, path):
        if path.startswith("s3://"):
            return self._aws_lock(path,
                                  wait_period=self.wait_period,
                                  time_out_seconds=self.time_out_seconds,
                                  maximum_age=self.maximum_age,
                                  logger=self._logger
                                  )
        else:
            # short time outs for local file system
            return DoggoLock(path,
                             wait_period=self.wait_period,
                             time_out_seconds=self.time_out_seconds,
                             maximum_age=self.maximum_age,
                             logger=self._logger
                             )

    def _validate_args(self, args):
        """
        Validated passed parameters and creates the arguments

        :param args: a dictionary of parameters
        """
        if args is not None:
            # create the S3 credentials
            try:
                args["s3_credentials"] = "aws_access_key_id={0};aws_secret_access_key={1}".format(
                    args["aws_access_key_id"],
                    args["aws_secret_access_key"])
            except KeyError:
                pass

            # now log out all the parameters
            self._log_parameters(args)

            return args
        else:
            return dict()

    def archive_path(self, file_path):
        """
        Calculates the archive path for the SQL queries

        :param: the path of the SQL files

        :return: the location to save the archived SQL file
        """
        if self._archive_path is None:
            return None
        else:
            return os.path.join(self._archive_path, os.path.split(file_path)[1])

    def get_sql_file(self, file):
        """
        Search SQL paths for the named query

        :param file: the SQL file to get
        :return: a full path to the SQL file
        """
        for p in self._sql_paths:
            f = os.path.join(p, file)
            if os.path.exists(f):
                return f

        raise ValueError("SQL file {0} not found in {1}".format(
            file,
            ",".join(self._sql_paths)
        ))

    @staticmethod
    def _clean_dict(d):
        """
        Removes any secret terms from a dictionary, for logging

        :param d: the dictionary to search
        :return: a clean dictionary
        """
        block_words = ["secret", "password", "credentials"]
        clean = {}
        for param in d:
            if any(x.lower() in param.lower() for x in block_words):
                clean[param] = "*" * len(d[param])
            else:
                clean[param] = d[param]

        return clean

    def _log_parameters(self, params):
        """
        Logs SQL parameters excluding any secret terms

        :param params: a dict of parameters
        """
        if params is not None:
            clean = self._clean_dict(params)
            for param in clean:
                self._logger.info("{0} = {1}".format(param, clean[param]))

    @staticmethod
    def __format_list(the_listl):

        if len(the_listl) == 1:
            the_listl = the_listl + ["There is really no chance that this will be a match in the database"]

        return tuple(the_listl)

    def clear_cache(self,
                    sql_file,
                    output_prefix,
                    params=None,
                    replacement_dict=None):
        """
        Clears the cache of the specified SQL file

        :param sql_file: the SQL file to delete the cachec
        :param output_prefix: the output path to use for the cache
        :param params: the parameters to use in the cache
        :param replacement_dict: and replacement to be made in the query's text
        :return:
        """
        # set the path
        path = self.get_cache_path(
            prefix=output_prefix,
            files_to_hash=[self.get_sql_file(sql_file)],
            data_hash=self._get_dict_hash(params, replacement_dict),
            suffix=".gz" if self._gzip else "")

        with self._get_lock(path):
            if self._exists(path):
                self.dfs.rm(path)

    @staticmethod
    def _validate_sql(sql_file):
        """
        Implemented by the child class and raise an exception if it's not valid

        :param sql_file: the SQL file to validate
        """
        pass

    def get_query_params(
        self,
        params: Optional[dict],
        ignore_list: List[str]
    ) -> dict:
        """
        Get a set of query parameters, with passed arguments taking precedence.
        Also formats any list parameters as per __format_list().

        :param ignore_list: any parameters to ignore from list formatting
        """
        query_parameters = dict(self._args)
        if params is not None:
            query_parameters.update(params)

        for arg in query_parameters:
            if type(query_parameters[arg]) == list and arg not in ignore_list:
                query_parameters[arg] = self.__format_list(query_parameters[arg])

        return query_parameters

    def check_exists(
        self,
        output_file: str,
        refresh_cache: bool
    ) -> Optional[str]:
        """
        Function to check if the output file already exists in S3.
        If so, return the file location or remove the file if opting to refresh the cache.
        """
        if self._exists(output_file):
            if refresh_cache:
                self._logger.info("Refreshing cache at {0}".format(output_file))
                with self._get_lock(output_file):
                    self.dfs.rm(output_file, recursive=True)
            else:
                self._logger.info("Loading query from {0}".format(output_file))
                return output_file

    def lock_and_execute(
        self,
        output_file: str,
        file_path: str,
        query_parameters: dict,
        replacement_dict: dict
    ) -> None:
        """
        Function to obtain the lock on the output file path and execute the query.
        """
        with self._get_lock(output_file):
            if not self._exists(output_file):
                # clean up any S3 files with the same prefix
                for file in self.dfs.glob(output_file + "**"):  # pragma: nocover
                    self.dfs.rm(file)

                self._logger.info("Executing query to {0}".format(output_file))
                self._execute_query(
                    query_file=file_path,
                    output_file=output_file,
                    query_parameters=query_parameters,
                    replacement_dict={} if replacement_dict is None else replacement_dict
                )

                # In the S3 case, redshift files are saved with a prefix and need to be renamed
                if self._redshift_checks and output_file.startswith("s3://"):
                    if not self.dfs.exists(output_file):
                        files = self.dfs.glob(output_file + "**")
                        self._concatenate_files(output_file=output_file, files=files)

    def get_results(
        self,
        sql_file: str,
        output_prefix: str,
        params: Optional[dict] = None,
        replacement_dict: Optional[dict] = None,
        refresh_cache: Optional[bool] = False,
        ignore_list: Optional[List[str]] = None
    ) -> str:
        """
        Runs the specified SQL file

        :param sql_file: the SQL file to run
        :param output_prefix: the output path to use for this query
        :param params: the parameters to use in the query
        :param replacement_dict: and replacement to be made in the query's text
        :param refresh_cache: if set, then the cache for this query is refreshed when it is run
        :param ignore_list: any parameters we do not want to __format_list on
        """
        ignore_list = ignore_list if ignore_list else []
        query_parameters = self.get_query_params(params, ignore_list)

        file_path = self.get_sql_file(sql_file)
        self._validate_sql(file_path)

        output_file = self.get_cache_path(
            prefix=output_prefix,
            files_to_hash=[file_path],
            data_hash=self._get_dict_hash(params, replacement_dict),
            suffix=".gz" if self._gzip else ""
        )

        self._log_parameters(params)

        cached_loc = self.check_exists(output_file, refresh_cache)
        output_file = cached_loc if cached_loc else output_file

        self.lock_and_execute(
            output_file=output_file,
            file_path=file_path,
            query_parameters=query_parameters,
            replacement_dict=replacement_dict
        )

        return output_file

    def _concatenate_files(self, output_file, files, deleting_files=True):
        if len(files) == 0:
            raise ValueError("No file returned by the query. Does it contain an UNLOAD command?")
        elif len(files) > 1:
            self._logger.info(f"Concatenating {','.join([f for f in files])}")
            with FileDoggo(output_file, 'wb', compression="gzip" if self._gzip else None) as outfile:
                # Open each file to concatenate
                for file_number, file in enumerate(files):
                    # Write each line to the output file
                    with FileDoggo(file, 'rb', compression="gzip" if self._gzip else None) as infile:
                        if file_number != 0:  # Skip first line for the rest of files
                            _ = infile.readline()
                        shutil.copyfileobj(infile, outfile)
            if deleting_files:
                for file in files:
                    self.dfs.rm(file)
            else:
                self._logger.info("Keeping the local file for unit test")
        else:
            self.dfs.mv(files[0], output_file)

    def _execute_query(self, **params):
        # Implemented by child
        raise NotImplementedError("BaseCachedClass cannot execute queries")


class CachedPep249Query(BaseCachedQuery):
    """
    A CachedQuery class compatible with PEP249 classes.


    The PEP249 query takes an additional argument containing any PEP249 compliant connection object.

    Use the CachedPep249Query class with any PEP249 compliant database connector, like this:

    .. code-block:: python

        import pandas as pd
        import sqlite3
        from newtools import CachedPep249Query

        pep_249_obj =  sqlite3.connect("mydb.sqlite")

        q = CachedPep249Query(pep_249_obj,
                              cache_path="s3://here-is-my-cache/",
                              sql_paths=["local/path/with/sql/file", "another/local/path"],
                              gzip=True)

        results = q.get_results(sql_file="my_query.sql",
                      output_prefix="test_query"
                      )

        df = pd.load_df(results, compression="gzip")

    """
    __sql = None
    _redshift_checks = True

    def __init__(self, pep_249_obj, params=None, cache_path="", sql_archive_path=None, sql_paths=None, gzip=True,
                 dynamodb_lock=True, logger=logging.getLogger("newtools.cached_query"), expiry_seconds=0,
                 boto_session: Optional[BotoSession] = None):
        super().__init__(params, cache_path, sql_archive_path, sql_paths, gzip, dynamodb_lock, logger, expiry_seconds,
                         boto_session=boto_session)

        self._sql = SqlClient(pep_249_obj,
                              logger=logger,
                              logging_level=logging.INFO)

    @staticmethod
    def _validate_sql(sql_file):
        """
        Checks for unescape % signs in the SQL file which doesn't work for Parameters

        Raise an exception if it's not valid

        :param sql_file: the SQL file to validate
        """
        with open(sql_file, 'rt') as f:
            sql = f.read()
            # check for unescaped %
            if re.search("%[^%]", sql):
                raise ValueError("SQL file {0} contains unescaped % signs that will not run".format(sql_file))

    def _execute_query(self,
                       query_file,
                       output_file,
                       query_parameters,
                       replacement_dict):
        """
        Executes the query

        :param query_file: the query to run
        :param output_file: the location to store the output
        :param query_parameters: the full set of query parameters to use
        :param replacement_dict: any items to replace directly in the SQL code
        :return:
        """

        if '{s3_path' in open(query_file).read():
            # many of our queries include an UNLOAD to S3 path statement and require s3_path
            query_parameters["s3_path"] = output_file

            self._sql.execute_query(query=query_file,
                                    parameters=query_parameters,
                                    replace=replacement_dict,
                                    archive_query=self.archive_path(query_file))
        else:
            # otherwise run and save directly to CSV
            self._sql.execute_query_to_csv(query=query_file,
                                           csvfile=output_file,
                                           parameters=query_parameters,
                                           replace=replacement_dict,
                                           archive_query=self.archive_path(query_file))


class CachedAthenaQuery(BaseCachedQuery):
    """
    The cached AthenaQuery will execute queries against AWS Athena and cache results in csv.gz format.

    It takes single additional arguments, queue_queries, which defaults to False but will queue the queries
    before executing them if set to true.

    Two special parameters must be passed to connect to Athena:

    * **aws_region** - the AWS region
    * **athena_db** - the Athena database to use

    The Athena connection is created using Boto and uses the current AWS profile or AWS access keys and tokens.

    Use the class as follows

    .. code-block:: python

        import pandas as pd
        from newtools import CachedAthenaQuery

        q = CachedAthenaQuery(cache_path="s3://here-is-my-cache/",
                              sql_paths=["local/path/with/sql/file", "another/local/path"],
                              params={"aws_region": "us-east-1",
                                      "athena_db": "my_db"},
                              gzip=True)


        results = q.get_results(sql_file="my_query.sql",
                      output_prefix="test_query"
                      )

        df = pd.load_df(results, compression="gzip")

    """
    __ac = None

    def __init__(self, params=None, cache_path="", sql_archive_path=None, sql_paths=None, gzip=True,
                 dynamodb_lock=True, logger=logging.getLogger("newtools.cached_query"),
                 queue_queries=False, expiry_seconds=0, use_lock: Optional[bool] = True,
                 boto_session: Optional[BotoSession] = None):
        super().__init__(
            params=params,
            cache_path=cache_path,
            sql_archive_path=sql_archive_path,
            sql_paths=sql_paths,
            gzip=gzip,
            dynamodb_lock=dynamodb_lock,
            logger=logger,
            expiry_seconds=expiry_seconds,
            use_lock=use_lock,
            boto_session=boto_session
        )

        self._results = dict()
        self.queue_queries = queue_queries

    @property
    def _ac(self):
        """

        :return: the AthenaClient class to use
        """
        if self.__ac is None:
            self.__ac = AthenaClient(region=self._args.get('aws_region', 'us-east-1'),
                                     db=self._args['athena_db'],
                                     workgroup=self._args.get('workgroup', None))

        return self.__ac

    def _archive_query(self, logged_query, parameters, file):
        """
        Logs the query to the archive location

        :param logged_query: the text of the query
        :param parameters: the parameters to apply
        :param file: the archive file path
        """
        file_hash = file.replace('.sql', '') + f'_{int(time.time())}'
        with self.dfs.open(f'{file_hash}.sql', 'wb') as f:  # FileDoggo does not support "wt" for S3 files
            f.write('-- Ran query on: {:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now()).encode('UTF-8'))
            f.write('-- Parameters: {0}\n'.format(self._clean_dict(parameters)).encode('UTF-8'))
            f.write((logged_query + ';\n').encode('UTF-8'))

    @staticmethod
    def get_query_body(
        query_file: str,
        query_parameters: dict,
        replacement_dict: dict
    ) -> str:
        """
        Function to open the query and format with the specified parameters.
        """
        with open(query_file) as f:
            actual_query = f.read()

        for key in replacement_dict:
            actual_query = actual_query.replace(key, replacement_dict[key])

        return actual_query.format(**query_parameters)

    def _execute_query(
        self,
        query_file: str,
        output_file: str,
        query_parameters: dict,
        replacement_dict: dict
    ) -> None:
        """
        Executes the query

        :param query_file: the query to run
        :param output_file: the location to store the output
        :param query_parameters: the full set of query parameters to use
        :param replacement_dict: any items to replace directly in the SQL code
        """
        actual_query = self.get_query_body(query_file, query_parameters, replacement_dict)

        # Save an archive copy of the query
        archive_query_path = self.archive_path(query_file)
        if archive_query_path is not None:
            self._archive_query(actual_query, query_parameters, archive_query_path)

        # Now run the query on Athena
        self._results[output_file] = self._ac.add_query(
            sql=actual_query,
            name="unload {}".format(output_file),
            output_location=self.cache_path)

        if not self.queue_queries:
            self.wait_for_completion()

    def wait_for_completion(self):

        self._ac.wait_for_completion()

        compression = 'gzip' if self._gzip else None

        for output_file in set(self._results.keys()):
            res = self._results.pop(output_file)
            actual_file = S3Location(self.cache_path).join(res.id + '.csv')

            with self.dfs.open(actual_file, 'rb') as f_in:
                with self.dfs.open(output_file, 'wb', compression=compression) as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # delete the metadata file
            self.dfs.rm(actual_file)
            self.dfs.rm(actual_file + '.metadata')


class CachedCTASQuery(CachedAthenaQuery):
    """
    Class allowing functionality to run Athena queries using the CTAS operation.
    """
    def __init__(
        self,
        params: Optional[dict] = None,
        cache_path: Optional[Path] = '',
        sql_archive_path: Optional[str] = None,
        sql_paths: Optional[Union[str, List[str]]] = None,
        dynamodb_lock: Optional[bool] = True,
        use_lock: Optional[bool] = True,
        logger: Optional[logging.Logger] = logging.getLogger(__name__),
        expiry_seconds: Optional[int] = 0,
        queue_queries: Optional[bool] = False,
        return_meta: Optional[bool] = False,
        boto_session: Optional[BotoSession] = None
    ) -> None:
        """
        :param use_lock: whether to use a lock to prevent concurrent s3 access
            if set to False, dynamodb_lock parameter wll be ignored
        :param return_meta: whether to return the metadata of the query (e.g. count(1) of the results)
            this functionality will only work if queue_queries is set to False
        """
        if cache_path and not cache_path.startswith('s3://'):
            raise AssertionError(f"CTAS queries can only output to S3; current cache path: {cache_path}")

        self.query_meta = {}

        super().__init__(
            params=params,
            cache_path=cache_path,
            sql_archive_path=sql_archive_path,
            sql_paths=sql_paths,
            dynamodb_lock=dynamodb_lock,
            logger=logger,
            expiry_seconds=expiry_seconds,
            use_lock=use_lock
        )

        self.return_meta = return_meta
        self.queue_queries = queue_queries

        self.doggo = PandasDoggo(boto_session=boto_session) if boto_session else PandasDoggo()

    @classmethod
    def get_query_header(
        cls,
        database: str,
        table_name: str,
        external_location: Path,
        output_format: Optional[str] = None,
        output_compression: Optional[str] = None,
        partition_columns: Optional[Union[str, List[str]]] = None,
        bucket_info: Optional[Tuple[str, int]] = None
    ) -> str:
        """
        Function to calculate the CTAS header for the query to run.

        :param database: the database to CTAS from
        :param table_name: the name of the CTAS temporary table
        :param external_location: where to save the CTAS contents to in S3
        :param output_format: the format of the output data, which is PARQUET by default
        :param output_compression: the compression of the output data
            https://docs.aws.amazon.com/athena/latest/ug/compression-formats.html
        :param partition_columns: the columns to partition by
            must ensure the partition columns are the last columns of the SELECT statement in the query
            moreover, if multiple partition columns are specified, their ordering must be as in the query
        :param bucket_info: a tuple containing the column to bucket on and the bucket count
        """
        base_template = "CREATE TABLE {db}.{table} WITH({query_prop}) AS"

        properties = {
            "format": f"'{output_format if output_format else 'PARQUET'}'",
            "write_compression": f"'{output_compression if output_compression else 'SNAPPY'}'",
            "external_location": f"'{external_location}'"
        }

        if partition_columns:
            if isinstance(partition_columns, str):
                partition_columns = [partition_columns]
            properties["partitioned_by"] = "ARRAY{}".format(partition_columns)
        if bucket_info:
            column, count = bucket_info
            properties["bucketed_by"] = "ARRAY{}".format([column])
            properties["bucket_count"] = int(count)

        str_properties = ", ".join([f"{key} = {properties[key]}" for key in properties])

        return base_template.format(
            db=database,
            table=table_name,
            query_prop=str_properties
        )

    def get_results(
        self,
        sql_file: str,
        output_prefix: str,
        params: Optional[dict] = None,
        replacement_dict: Optional[dict] = None,
        refresh_cache: Optional[bool] = False,
        **kwargs
    ) -> Union[str, dict]:
        """
        Function to run the specified query and return the output path(/directory) to the data.
        If return_meta is set to True, will return a dictionary containing the output path and the metadata.
        The query metadata is refreshed on get_results() call.
        """
        self.query_meta = {}

        output_path = super().get_results(
            sql_file=sql_file,
            output_prefix=output_prefix,
            params=params,
            replacement_dict=replacement_dict,
            refresh_cache=refresh_cache,
            ignore_list=['partition_columns']
        )

        if self.return_meta:
            return {
                'output_path': output_path,
                **self.query_meta
            }
        else:
            return output_path

    @staticmethod
    def get_cache_file_format(*args, **kwargs) -> str:
        """
        Return the file format for the cache path for CTAS.
        """
        return "/"

    def _execute_query(
        self,
        query_file: str,
        output_file: str,
        query_parameters: dict,
        replacement_dict: dict
    ) -> None:
        """
        Function to execute the query under CTAS.
        """
        self.validate_ctas_params(query_parameters)
        ctas_params = self.extract_ctas_parameters(query_parameters, output_file)
        ctas_header = self.get_query_header(**ctas_params)

        query_body = self.get_query_body(query_file, query_parameters, replacement_dict)

        actual_query = f"{ctas_header}\n{query_body}"

        # Save an archive copy of the query
        archive_query_path = self.archive_path(query_file)
        if archive_query_path is not None:
            self._archive_query(actual_query, query_parameters, archive_query_path)

        # Run the query on Athena
        self._ac.add_query(
            sql=actual_query,
            name="CTAS {}".format(output_file),
            output_location=self.cache_path
        )

        if not self.queue_queries:
            self._ac.wait_for_completion()

            if self.return_meta:
                self.get_query_metadata(
                    database=ctas_params.get('database'),
                    table_name=ctas_params.get('table_name'),
                    partition_columns=ctas_params.get('partition_columns')
                )

            # If CTAS has no results, no files are saved to S3 - so we do so for caching purposes
            if not self.dfs.exists(output_file):
                self.dfs.s3_client.put_object(
                    Bucket=S3Location(output_file).bucket,
                    Key=S3Location(output_file).join('EMPTY').key,
                    Body=b''
                )

            # Drop the CTAS table
            self._ac.add_query(
                sql=f"DROP TABLE IF EXISTS {ctas_params['database']}.{ctas_params['table_name']}",
                name="DROP CTAS {}".format(output_file),
                output_location=self.cache_path
            )
            self._ac.wait_for_completion()

    def get_query_metadata(
        self,
        database: str,
        table_name: str,
        partition_columns: Optional[Union[str, list]] = None
    ) -> None:
        """
        Function to run queries to get metadata about the results of the query from CTAS.

        :param database: the database the table is stored in
        :param table_name: the name of the CTAS table
        :param partition_columns: the partitions columns used in the query (if any)
        """
        base_query = """SELECT {columns} COUNT(1) FROM {database}.{table_name} {group_by}"""
        columns = group_by = ""

        if partition_columns:
            partition_columns = partition_columns if isinstance(partition_columns, list) else [partition_columns]
            columns = ", ".join(partition_columns) + ","
            group_by = f"GROUP BY {', '.join(str(i) for i in range(1, len(partition_columns) + 1))}"

        query = base_query.format(
            columns=columns,
            database=database,
            table_name=table_name,
            group_by=group_by
        )

        query_id = self._ac.add_query(query, output_location=self.cache_path)
        self._ac.wait_for_completion()
        results = self._ac.get_query_result(query_id)

        self.query_meta['size'] = self.format_df_to_dict(results, index_cols=partition_columns)

    @staticmethod
    def format_df_to_dict(
        df: DataFrame,
        index_cols: Optional[List[str]] = None
    ) -> dict:
        """
        Function to format a dataframe into a dictionary of values.

        :param df: the dataframe to format
        :param index_cols: the columns to set as the index
        """
        col_name = df.columns[-1]
        if index_cols:
            return df.set_index(index_cols).to_dict()[col_name]
        else:
            return {'total': int(df.loc[0, col_name])}

    @staticmethod
    def validate_ctas_params(
        parameters: dict
    ) -> None:
        """
        Function to check the required parameters for CTAS are specified in the parameters.
        """
        required_params = ["ctas_athena_db"]

        for param in required_params:
            assert param in parameters, f"Required CTAS parameter '{param}' has not been specified"

    @staticmethod
    def extract_ctas_parameters(
        params: dict,
        output_file: str
    ) -> dict:
        """
        Function to extract the CTAS parameters from the query parameters.

        :param params: the query parameters and generic SQL parameters
        :param output_file: the external location for CTAS, of the form {cache_path}/{sql_hash}/
        """
        return {
            "database": params.get("ctas_athena_db"),
            "table_name": re.sub(r'\W', '', output_file.split('/')[-2]),
            "external_location": output_file,
            "output_format": params.get("output_format"),
            "output_compression": params.get("output_compression"),
            "partition_columns": params.get("partition_columns"),
            "bucket_info": params.get("bucket_info")
        }

    def load_dir_iter(
        self,
        load_path: Path,
        file_format: Optional[str] = None
    ) -> Iterator[DataFrame]:
        """
        Function to return a generator of the output CTAS data.

        :param load_path: the directory containing the CTAS data in S3
        :param file_format: the format of the save files, e.g. PARQUET or CSV
        """
        yield from self.doggo.load_dir_iter(load_path, file_format)

    def load_dir(
        self,
        load_path: Path,
        file_format: Optional[str] = None
    ) -> DataFrame:
        """
        Function to load in the CTAS output and return one unified dataframe.

        :param load_path: the directory containing the CTAS data in S3
        :param file_format: the format of the save files, e.g. PARQUET or CSV
        """
        return self.doggo.load_dir(load_path, file_format)

    def get_partitions(
        self,
        load_path: Path
    ) -> List[Tuple[Any]]:
        """
        Function to load all partitions under the load_path into a list of tuples of the form:
            ('partition_col1=partition_val1', 'partition_col2=partition_val2', ..., '{path_to_data}')

        :param load_path: the directory containing the CTAS data in S3
        """
        output: List[tuple] = []

        for file_name in self.dfs.ls(location=load_path, recursive=True):
            partitions = tuple(ele for ele in file_name.split('/') if "=" in ele)
            external_location = re.search('(.*=.*/).*', file_name).group(1)
            output.append(partitions + (external_location, ))

        return list(set(output))
