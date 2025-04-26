# (c) 2012-2020 Deductive, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)


import gzip
import json
import logging
import os
from datetime import datetime
from typing import Optional, Union, Type, Iterator
from newtools.aws import S3Location
from .fs import DoggoFileSystem, FileDoggo

from newtools.optional_imports import pandas as pd

Path = Union[str, S3Location]
DataFrame = Type['pd.DataFrame']


class PandasDoggo:
    """
    Is a Panda a doggo?

    .. parsed-literal::

        ░░░░░░░░▄██▄░░░░░░▄▄░░
        ░░░░░░░▐███▀░░░░░▄███▌
        ░░▄▀░░▄█▀▀░░░░░░░░▀██░
        ░█░░░██░░░░░░░░░░░░░░░
        █▌░░▐██░░▄██▌░░▄▄▄░░░▄
        ██░░▐██▄░▀█▀░░░▀██░░▐▌
        ██▄░▐███▄▄░░▄▄▄░▀▀░▄██
        ▐███▄██████▄░▀░▄█████▌
        ▐████████████▀▀██████░
        ░▐████▀██████░░█████░░
        ░░░▀▀▀░░█████▌░████▀░░
        ░░░░░░░░░▀▀███░▀▀▀░░░░


    A class designed to simplify file IO operation to and from local or s3 files, with specific functionality for csv and parquet file formats

    Key features
    ------------

    - read / write csv and parquet files
    - read and write both locally and to s3
    - support gzip, snappy and zip compression
    - sensible s3 handling of different profiles / credentials

    Usage
    -----

    .. code-block:: python

        from newtools import PandasDoggo

        fh = PandasDoggo()

        df = fh.load('filename.ext')

        fh.save(df, 'path/to/new_file/ext')

    """

    def __init__(self,
                 boto_session=None,
                 logger=logging.getLogger("newtools.pandas_doggo")):
        """

        :param boto_session: optional boto3 session to use for
        :type boto_session: boto3.Session
        :param logger: the logger to use
        """

        if boto_session:
            self.s3_client = boto_session.client('s3')
        else:
            self.s3_client = None

        self.dfs = DoggoFileSystem(boto3_session=boto_session)
        self._logger = logger

    @staticmethod
    def _extract_file_format(path):

        for part in reversed(path.split(".")[-2:]):
            if part in ('csv', 'parquet', 'pq'):
                return part

        raise ValueError(f'could not determine format of path: {path}, use file_format param to specify')

    @staticmethod
    def _extract_compression(path):
        # extend for other compression

        if path.endswith('.gzip') or path.endswith('.gz'):
            return 'gzip'
        if ('.snappy' in path) or path.endswith('.sz'):
            return 'snappy'
        if path.endswith('.zip'):
            return 'zip'

    def load(self, path, file_format=None, compression=None, request_payer='bucketowner', *args, **kwargs):
        """Load a file into a Pandas.DataFrame from local or s3 locations.

        :param path: required. Can be s3 or local s3 must be in `s3://` format - accepts `S3Location`
        :type path: str
        :param file_format: None. Autodetects from path, can be set to `csv` or `parquet` to explicitly force a format
        :param compression: optional, 'gzip', 'snappy' or None. Autodetects from path if path ends in `.gz`, `.gzip` or contains `.snappy`
        :param request_payer: either 'bucketowner' (default) or 'requester' - who incurs the cost of said operation
        :param args: args to pass to the panda to load the file
        :param kwargs: kwargs to pass to the panda to load the file eg columns=['subset', 'of', 'columns']
        :return: Pandas.DataFrame
        """

        file_format = file_format or self._extract_file_format(path)

        if file_format not in ('csv', 'parquet', 'pq'):
            raise ValueError(f'detected format:{format} is not recognized file format for load')

        if file_format == 'csv':
            return self.load_csv(path, compression=compression, request_payer=request_payer, *args, **kwargs)

        elif file_format in ('parquet', 'pq'):
            return self.load_parquet(path, compression=compression, request_payer=request_payer, *args, **kwargs)

    def load_csv(self, path, compression=None, request_payer='bucketowner', *args, **kwargs):
        """alias for .load(path, format='csv')"""
        if 'chunksize' in kwargs:
            raise NotImplementedError("PandasDoggo does not support chunksize for loading data frames")

        compression = compression or self._extract_compression(path)
        fm = FileDoggo(path, mode='rb', client=self.s3_client, compression=compression, request_payer=request_payer)
        with fm as f:
            df = pd.read_csv(f, *args, **kwargs)

        return df

    def load_parquet(self, path, compression=None, request_payer='bucketowner', *args, **kwargs):
        """alias for .load(path, format='parquet')"""

        compression = compression or self._extract_compression(path)
        fm = FileDoggo(path, mode='rb', client=self.s3_client, compression=compression, request_payer=request_payer)
        with fm as f:
            df = pd.read_parquet(f, engine='pyarrow', *args, **kwargs)

        return df

    def save(self, df, path, file_format=None, compression=None, request_payer='bucketowner', *args, **kwargs):
        """Save a file into a Pandas.DataFrame from local or s3 locations.

        :param df: Data frame
        :type df: Pandas.DataFrame
        :param path: required. Can be s3 or local s3 must be in `s3://` format - accepts `S3Location`
        :type path: str
        :param file_format: 'None. Autodetects from path, can be set to `csv` or `parquet` to explicitly force a format
        :param compression: None. Supports gzip and snappy, autodetects from path if path ends in `.gz`, `.gzip` or contains `.snappy`
        :param request_payer: either 'bucketowner' (default) or 'requester' - who incurs the cost of said operation
        :param args: args to pass to the panda to save the file
        :param kwargs: kwargs to pass to the panda to save the file eg index=None
        """

        file_format = file_format or self._extract_file_format(path)

        if file_format == 'csv':
            return self.save_csv(df, path, compression=compression, request_payer=request_payer, *args, **kwargs)

        elif file_format in ('parquet', 'pq'):
            return self.save_parquet(df, path, compression=compression, request_payer=request_payer, *args, **kwargs)

    def save_csv(self, df, path, compression=None, request_payer='bucketowner', *args, **kwargs):
        """Alias for .save(df, format='csv')"""
        compression = compression or self._extract_compression(path)
        fm = FileDoggo(path, mode='wb', client=self.s3_client, compression=compression, request_payer=request_payer)
        with fm as f:
            f.write(df.to_csv(None, *args, **kwargs).encode('utf-8'))

    def save_parquet(self, df, path, compression=None, request_payer='bucketowner', *args, **kwargs):
        """Alias for .save(df, format='parquet')"""

        compression = compression or self._extract_compression(path)
        fm = FileDoggo(path, mode='wb', client=self.s3_client, compression=compression, request_payer=request_payer)
        with fm as f:
            df.to_parquet(f, *args, **kwargs)

    def save_partitioned(self,
                         df,
                         base_path,
                         name,
                         suffix,
                         partition_columns,
                         partition_string="",
                         date_time_format="%Y-%m-%d_%H%M%S.%f",
                         compression=None,
                         request_payer='bucketowner', *args, **kwargs):
        """Save a data frame into multiple files, partitioned by the specified columns. The base path can be
        local file system, or S3.

        Based on athena_partition from old tools. Notable differences are as follows:
        * PandasDoggo saves the index as default so pass index=False for comparable behavior
        * base_path - new parameter that was previously taken from the passed file_handler
        * partition_columns - replaces partition_categories
        * partition_dtypes - not supported so please apply any changes to dtype before passing using df.astype(dict(zip(["col1", "col7"], [int, int])
        * columns_to_keep - not supported, please only send a slice of the data frame with the columns you want to partition or save
        * file_handler - not supported, uses the PandasDoggo class.

        :param df: The data frame to be partitioned
        :param base_path: The base path to save the files to
        :param name: If provided all files filename will start with this
        :param suffix: The extension the file should be saved with, .csv for csv, and .parquet for parquet
        :param partition_columns: The columns to partition the data on
        :param partition_string: Allows formatting folder names, will be dependant on how many partition categories there
                are, defaults to creating hive-format folders and sub folders in order of partitioning
        :param date_time_format: To minimise chances of overwrite the saved files contain the date time of when this
                function was called, this param specifies the format of the date time
        :param compression: None. Supports gzip and snappy, autodetects from suffix if it ends in `.gz`, `.gzip` or contains `.snappy`
        :param request_payer: either 'bucketowner' (default) or 'requester' - who incurs the cost of said operation
        :param args: args to pass to the panda to save the file
        :param kwargs: kwargs to pass to the panda to save the file eg index=None
        :return: Returns a full list of all file paths created, doesnt return base path as part of this
        """

        if any(df[partition_columns].isna().any()) or any((df[partition_columns] == "").any()):  # pragma: no cover
            raise ValueError('The partition columns contain NaN values')

        # Set up the default partition string
        if not partition_string:
            partition_string = "/".join([col + "={}" for col in partition_columns])

        paths = list()

        # Create each partition file
        for partition_values, group_df in df.groupby(partition_columns, sort=False):

            # Format the partitions
            if len(partition_columns) == 1:
                partition_values = [partition_values]
            partitions = partition_string.format(*partition_values)

            # Get the time
            time = datetime.now().strftime(date_time_format)
            self._logger.info("time is {}".format(time))

            # Get the file
            file = f"{base_path}/{partitions}/{name}{datetime.now().strftime(date_time_format)}{suffix}"
            self._logger.info(json.dumps({"message": "Saving parquet to location {}".format(file)}))

            # Create the path if it doesn't exist...
            if file.startswith("/"):
                try:
                    os.makedirs(os.path.dirname(file))
                except FileExistsError:  # pragma: no cover
                    pass

            # Save the dataframe
            self.save(group_df[[col for col in df.columns if col not in partition_columns]],
                      file, compression=compression, request_payer=request_payer, *args, **kwargs)

            # Add to the list to return
            paths.append(file)

        return paths

    def load_dir_iter(
        self,
        load_path: Path,
        file_format: Optional[str] = None
    ) -> Iterator[DataFrame]:
        """
        Function to return a generator of the output under the given directory.

        :param load_path: the directory containing the data in S3
        :param file_format: the format of the save files, e.g. PARQUET or CSV
        """
        file_format = file_format.upper() if file_format else 'PARQUET'

        if file_format == 'PARQUET':
            load_func = self.load_parquet
        elif file_format == 'CSV':
            load_func = self.load_csv
        else:
            raise NotImplementedError(
                f"{self.__class__.__name__}.load_dir_iter only supports loading CSV or PARQUET files, not {file_format}"
            )

        for file_name in self.dfs.ls(location=load_path, recursive=True):
            yield load_func(file_name)

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
        file_format = file_format.upper() if file_format else 'PARQUET'
        return pd.concat(df for df in self.load_dir_iter(load_path, file_format))


