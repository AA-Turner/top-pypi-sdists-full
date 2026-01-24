from typing import List, Dict

import pandas as pd  # type: ignore
from csverve.core import CsverveOutput
from csverve.errors import CsverveWriterError


class CsverveOutputDataFrame(CsverveOutput):
    def __init__(
            self,
            df: pd.DataFrame,
            filepath: str,
            dtypes: Dict[str, str],
            skip_header: bool = False,
            na_rep: str = 'NaN',
            sep: str = ',',
    ) -> None:
        """
        CSV file and all related metadata.

        @param filepath: CSV file path.
        @param dtypes: Dictionary of pandas dtypes, where key = column name, value = dtype.
        @param header: boolean, True = write header, False = don't write header.
        @param na_rep: replace NaN with this value.
        @param columns: List of column names.
        """
        self.df = df
        columns: List[str] = list(self.df.columns.values)

        super().__init__(
            filepath, dtypes, columns,
            skip_header=skip_header, na_rep=na_rep, sep=sep
        )

        self._cast_df()

    def _cast_df(self):
        """
        Cast dataframe dtypes.

        @return:
        """

        for column_name in self.df.columns.values:
            try:
                self.df[column_name] = self.df[column_name].astype(self.dtypes[column_name])
            except ValueError:
                raise CsverveWriterError(
                    'Unable to cast the column {} to {}'.format(column_name, self.dtypes[column_name])
                )

    def write_df(self) -> None:
        """
        Write out dataframe to CSV.

        @param df: Pandas DataFrames.
        @param chunks: bool.
        @return:
        """

        if isinstance(self.df, pd.io.parsers.TextFileReader):
            for i, data in enumerate(self.df):
                if i == 0:
                    data.to_csv(
                        self.filepath, sep=self.sep, na_rep=self.na_rep,
                        index=False, compression='gzip', header=(not self.skip_header), mode='w'
                    )
                else:
                    data.to_csv(
                        self.filepath, sep=self.sep, na_rep=self.na_rep,
                        index=False, compression='gzip', header=False, mode='a'
                    )
        elif isinstance(self.df, pd.DataFrame):
            self.df.to_csv(
                self.filepath, sep=self.sep, na_rep=self.na_rep,
                index=False, compression='gzip', header=(not self.skip_header)
            )
        else:
            raise CsverveWriterError('Invalid df provided as input')

        self.write_yaml()
