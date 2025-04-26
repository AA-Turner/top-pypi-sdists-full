# (c) 2012-2020 Deductive, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

from io import BytesIO
import os
from csv import Sniffer, Error
from newtools.optional_imports import UniversalDetector, pandas as pd


from .doggo import PandasDoggo
from .fs import DoggoFileSystem


class CSVDoggo:
    """
    Loads and saves CSV files from pandas DataFrames. Supports GZIP, Parquet, S3, local file system interchangably

    """
    _load_map = {'line_terminator': 'lineterminator',
                 'force_dtype': 'dtype',
                 'nan_values': "na_values"}

    _save_map = {'delimiter': 'sep',
                 'force_dtype': 'dtype',
                 'nan_values': 'na_rep'}

    SAMPLE_SIZE = 1024 * 1024

    def __init__(self, base_path="", detect_parameters=False, *args, **kwargs):
        """

        :param base_path: the base path to use for subsequent save and load operations
        :param args: args to pass to save and load functions
        :param kwargs: kwargs to pass to save and load functions
        """
        self._base_path = base_path
        self._doggo = PandasDoggo()
        self._args = args
        self._kwargs = kwargs

        self.detect_parameters = detect_parameters

    def _get_file(self, file):
        return os.path.join(self._base_path, file)

    @staticmethod
    def _get_encoding(sample):
        detector = UniversalDetector()
        for line in BytesIO(sample).readlines():
            detector.feed(line)
            if detector.done:  # pragma: no cover
                break
        detector.close()
        return detector.result["encoding"]

    def _sniff_parameters(self, file):
        """
        sets instance variable with detected parameters from file
        :param file: name of file to be considered (relative to self.base_path)
        :return: True if able to detect parameters
        """
        # if we are using the default parameters, then attempt to guess them

        # create a sample...
        full_path = self._get_file(file)
        with DoggoFileSystem().open(full_path, mode="rb") as f:
            sample = f.read(self.SAMPLE_SIZE)

        # get the encoding...
        encoding = self._get_encoding(sample)
        if encoding is None:
            encoding = 'windows-1252'

        # now decode the sample
        try:
            sample = sample.decode(encoding)
        except UnicodeDecodeError:
            encoding = "windows-1252"
            try:
                sample = sample.decode(encoding)
            except UnicodeDecodeError as e:
                raise ValueError(str(e))

        # use the sniffer to detect the parameters...
        sniffer = Sniffer()
        dialect = sniffer.sniff(sample)
        delimiter = dialect.delimiter
        # the detector always seems to find a header... below line is in case it does not
        header = 0 if sniffer.has_header(sample) else -1
        quotechar = dialect.quotechar

        return {
            "encoding": encoding,
            "delimiter": delimiter,
            "header": header,
            "quotechar": quotechar
        }

    def _get_args(self, args):
        return args + self._args

    def _get_kwargs(self, kwargs, field_map):
        kw = self._kwargs.copy()
        kw.update(kwargs)
        for key in list(kw.keys()):
            if key in field_map:
                kw[field_map[key]] = kw.pop(key)
            elif key.startswith("csv_"):
                kw[key[4:]] = kw.pop(key)

        if kw.get("header", 0) == -1:
            kw.pop("header")

        if 'na_rep' in kw:
            kw['na_rep'] = kw['na_rep'][0]

        return kw

    def _get_path(self, file):
        return os.path.join(self._base_path, file)

    def load_df(self, file, *args, **kwargs):
        """
        Loads a data frame

        :param file: the file to load
        :param args: any args to use
        :param kwargs: any keyword args to use
        :return: a pandas data frame
        """

        try:
            return self._doggo.load_csv(self._get_path(file),
                                        *self._get_args(args),
                                        **self._get_kwargs(kwargs, self._load_map))
        except (UnicodeError, UnicodeDecodeError, pd.errors.ParserError) as e:
            err_msg = str(e)
            if self.detect_parameters:
                kwargs.update(self._sniff_parameters(file))
                return self._doggo.load_csv(self._get_path(file),
                                            *self._get_args(args),
                                            **self._get_kwargs(kwargs, self._load_map))
            raise ValueError(err_msg)

    def save_df(self, df, file, *args, **kwargs):
        """
        Saves a data frame

        :param df: the data frame to save
        :param file: the path to save to
        :param args: any args to use
        :param kwargs: any keyword args to use
        """
        if 'index' not in kwargs:
            kwargs['index'] = False
        return self._doggo.save_csv(df, self._get_path(file), *self._get_args(args),
                                    **self._get_kwargs(kwargs, self._save_map))

    def df_to_string(self, df, *args, **kwargs):
        """
        Returns a formatted string from a dataframe using the specified
        configuration for the class

        :param df: the data frame to cast to string
        """

        return df.to_csv(*self._get_args(args), **self._get_kwargs(kwargs, self._save_map))
