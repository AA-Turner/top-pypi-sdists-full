import gzip
import shutil
from typing import List, Dict, TextIO, Any

from csverve.core import CsverveOutput
from csverve.errors import CsverveInputError


class CsverveOutputFileStream(CsverveOutput):
    def __init__(
            self,
            filepath: str,
            dtypes: Dict[str, str],
            columns: List[str],
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

        super().__init__(
            filepath, dtypes, columns,
            skip_header=skip_header, na_rep=na_rep, sep=sep
        )

    def _write_header_to_file(self, writer: TextIO) -> None:
        """
        Write header.
        @param writer: TextIO.
        @return:
        """
        assert self.columns
        header: str = ','.join(self.columns)
        header = header + '\n'
        writer.write(header)

    def write_data_streams(self, csvfiles: List[str]) -> None:
        """
        Write data streams.
        @param csvfiles: List of CSV files paths.
        @return:
        """
        assert self.columns
        assert self.dtypes
        with gzip.open(self.filepath, 'wt') as writer:

            if not self.skip_header:
                self._write_header_to_file(writer)

            for csvfile in csvfiles:
                with gzip.open(csvfile, 'rt') as data_stream:
                    shutil.copyfileobj(
                        data_stream, writer, length=16 * 1024 * 1024
                    )

        self.write_yaml()

    @staticmethod
    def _file_type(filepath) -> str:
        if filepath.endswith('gz'):
            return 'gzip'
        elif filepath.endswith('csv'):
            return 'plain-text'
        else:
            raise CsverveInputError('Unsupported file type: {}'.format(filepath))

    def rewrite_csv(self, csvfile: str) -> None:
        """
        Rewrite CSV.
        @param csvfile: Filepath of CSV file.
        @return:
        """

        assert self.columns
        assert self.dtypes

        filetype = self._file_type(csvfile)

        opener: Any = gzip.open if filetype == 'gzip' else open

        with gzip.open(self.filepath, 'wt') as writer:
            with opener(csvfile, 'rt') as data_stream:
                shutil.copyfileobj(
                    data_stream, writer, length=16 * 1024 * 1024
                )

        self.write_yaml()
