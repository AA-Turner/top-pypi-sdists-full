import os
from typing import List, Dict, Union, Any

import pandas as pd  # type: ignore
import yaml
from csverve.errors import CsverveParseError


class CsverveInput(object):
    def __init__(self, filepath: str) -> None:
        """
        CSV file and all related metadata.

        @param filepath: Path of CSV.
        """

        self.filepath: str = filepath

        self._verify_input()

        self._yamldata = self._load_yaml()

    @property
    def header(self) -> bool:
        """
        True if file has header

        @return: header
        """
        return self._yamldata['header']

    @property
    def separator(self) -> str:
        """
        get the separator used

        @return: separator
        """
        return self._yamldata['sep']

    @property
    def columns(self) -> List[str]:
        """
        get the list of columns

        @return: separator
        """
        return [val['name'] for val in self._yamldata['columns']]

    @property
    def dtypes(self) -> Dict[str, str]:
        """
        get the data types

        @return: dtypes
        """
        return {val['name']: val['dtype'] for val in self._yamldata['columns']}

    @property
    def yaml_file(self) -> str:
        """
        Append '.yaml' to CSV path.

        @return: YAML metadata path.
        """
        return self.filepath + '.yaml'

    def _load_yaml(self) -> Dict[str, Any]:
        """
        load the yaml data

        @return: Dict
        """
        with open(self.yaml_file, 'rt') as yamlfile:
            yamldata = yaml.safe_load(yamlfile)
        return yamldata

    def _verify_input(self):
        """
        Verify gzip status and check for yaml

        @return:
        """
        if not self.filepath.endswith('.gz'):
            raise CsverveParseError('input must be gzipped')

        if not os.path.exists(self.yaml_file):
            raise CsverveParseError('yaml file missing')

    def _cast_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cast dataframe dtypes.

        @param df: Pandas DataFrame.
        @return: Pandas DataFrame.
        """
        for column_name in df.columns.values:
            df[column_name] = df[column_name].astype(self.dtypes[column_name])
        return df

    def _verify_data(self, df: pd.DataFrame, columns) -> None:
        """
        Verify columns of DataFrame match those of class property.

        @param df: Pandas DataFrame.
        @return:
        """
        if not set(list(df.columns.values)) == set(columns):
            raise CsverveParseError("metadata mismatch in {}".format(self.filepath))

    def read_csv(self, chunksize: int = None, usecols=None, dtype=None) -> pd.DataFrame:
        """
        Read CSV.

        @param chunksize: Number of rows to read at a time (optional, applies to large datasets).
        @param usecols: Restrict to specific columns (optional).
        @param dtype: Override the dtypes on specific columns (optional).
        @return: pandas DataFrame.
        """

        def return_gen(df_iterator, columns):
            for df in df_iterator:
                self._verify_data(df, columns)
                yield df

        # if header exists then use first line (0) as header
        header: Union[int, None] = 0 if self.header else None
        names: Union[None, List[str]] = None if self.header else self.columns
        columns: List[str] = usecols if usecols else self.columns

        # Override dtypes
        final_dtype = self.dtypes
        if dtype is not None:
            for name, dtype in dtype.items():
                if name in final_dtype:
                    final_dtype[name] = dtype
                else:
                    raise ValueError(f'dtype column {name} not present')

        try:
            data: pd.DataFrame = pd.read_csv(
                self.filepath,
                compression='gzip',
                chunksize=chunksize,
                sep=self.separator,
                header=header,
                names=names,
                dtype=final_dtype,
                usecols=usecols
            )
        except pd.errors.EmptyDataError:
            data = pd.DataFrame(columns=columns)
            data = self._cast_dataframe(data)

        if chunksize:
            return return_gen(data, columns)
        else:
            self._verify_data(data, columns)
            return data
