import os
from typing import List, Dict, Union
from warnings import warn

import csverve.utils as utils
import pandas as pd  # type: ignore
from csverve.core import CsverveInput
from csverve.core import CsverveOutputDataFrame
from csverve.core import CsverveOutputFileStream
from csverve.core import IrregularCsverveInput
from csverve.errors import CsverveConcatException


def concatenate_csv_files_pandas(
        in_filenames: Union[List[str], Dict[str, str]],
        out_filename: str,
        dtypes: Dict[str, str],
        skip_header: bool = False,
        drop_duplicates: bool = False,
        **kwargs
) -> None:
    """
    Concatenate gzipped CSV files.

    @param in_filenames: List of gzipped CSV file paths, or a dictionary where the keys are file paths.
    @param out_filename: Path of resulting concatenated gzipped CSV file and meta YAML.
    @param dtypes: Dictionary of pandas dtypes, where key = column name, value = dtype.
    @param skip_header: boolean, True = write header, False = don't write header.
    @return:
    """

    if kwargs.get('write_header') is not None:
        raise DeprecationWarning('write_header has been deprecated and will be ignored, please use skip_header instead')

    if isinstance(in_filenames, dict):
        in_filenames = list(in_filenames.values())

    data: List[CsverveInput] = [
        CsverveInput(in_filename).read_csv() for in_filename in in_filenames
    ]
    concat_data: pd.DataFrame = pd.concat(data, ignore_index=True)
    if drop_duplicates:
        concat_data = concat_data.drop_duplicates()
    csvoutput: CsverveOutputDataFrame = CsverveOutputDataFrame(
        concat_data, out_filename, dtypes, skip_header=skip_header
    )
    csvoutput.write_df()


def concatenate_csv_files_quick_lowmem(
        inputfiles: List[str],
        output: str,
        dtypes: Dict[str, str],
        columns: List[str],
        skip_header: bool = False,
        **kwargs
) -> None:
    """
    Concatenate gzipped CSV files.

    @param inputfiles: List of gzipped CSV file paths.
    @param output: Path of resulting concatenated gzipped CSV file and meta YAML.
    @param dtypes: Dictionary of pandas dtypes, where key = column name, value = dtype.
    @param columns: List of column names for newly concatenated gzipped CSV file.
    @param skip_header: boolean, True = write header, False = don't write header.
    @return:
    """
    if kwargs.get('write_header') is not None:
        raise DeprecationWarning('write_header has been deprecated and will be ignored, please use skip_header instead')

    csvoutput: CsverveOutputFileStream = CsverveOutputFileStream(
        output, dtypes, skip_header=skip_header, columns=columns
    )
    csvoutput.write_data_streams(inputfiles)


def get_columns(infile):
    return CsverveInput(infile).columns


def get_dtypes(infile):
    return CsverveInput(infile).dtypes


def rewrite_csv_file(
        filepath: str,
        outputfile: str,
        skip_header: bool = False,
        dtypes: Dict[str, str] = None,
        **kwargs
) -> None:
    """
    Generate header less csv files.

    @param filepath: File path of CSV.
    @param outputfile: File path of header less CSV to be generated.
    @param skip_header: boolean, True = write header, False = don't write header.
    @param dtypes: Dictionary of pandas dtypes, where key = column name, value = dtype.
    @return:
    """
    if kwargs.get('write_header') is not None:
        warn('write_header has been deprecated and will be ignored, please use skip_header instead', DeprecationWarning)

    if os.path.exists(filepath + '.yaml'):
        csvinput: Union[CsverveInput, IrregularCsverveInput] = CsverveInput(filepath)
        df = csvinput.read_csv()

        csvoutput_df = CsverveOutputDataFrame(
            df, outputfile, skip_header=skip_header,
            dtypes=csvinput.dtypes
        )
        csvoutput_df.write_df()
    else:
        assert dtypes
        csvinput = IrregularCsverveInput(filepath, dtypes)

        csvoutput_fs = CsverveOutputFileStream(
            outputfile, skip_header=skip_header, columns=csvinput.columns,
            dtypes=csvinput.dtypes
        )
        csvoutput_fs.rewrite_csv(filepath)


def merge_csv(
        in_filenames: Union[List[str], Dict[str, str]],
        out_filename: str,
        how: str,
        on: List[str],
        skip_header: bool = False,
        lenient: bool = False,
        **kwargs
) -> None:
    """
    Create one gzipped CSV out of multiple gzipped CSVs.

    @param in_filenames: Dictionary containing file paths as keys
    @param out_filename: Path to newly merged CSV
    @param how: How to join DataFrames (inner, outer, left, right).
    @param on: Column(s) to join on, comma separated if multiple.
    @param skip_header: boolean, True = write header, False = don't write header
    @return:
    """
    if kwargs.get('write_header') is not None:
        warn('write_header has been deprecated and will be ignored, please use skip_header instead', DeprecationWarning)

    if isinstance(in_filenames, dict):
        in_filenames = list(in_filenames.values())

    data: List[CsverveInput] = [CsverveInput(infile) for infile in in_filenames]

    dfs: List[str] = [csvinput.read_csv() for csvinput in data]

    dtypes: List[Dict[str, str]] = [csvinput.dtypes for csvinput in data]

    merged_data: pd.DataFrame = utils.merge_frames(dfs, how, on, lenient=lenient)

    dtypes_: Dict[str, str] = utils.merge_dtypes(dtypes)

    csvoutput: CsverveOutputDataFrame = CsverveOutputDataFrame(
        merged_data, out_filename, dtypes_, skip_header=skip_header
    )
    csvoutput.write_df()


def concatenate_csv(inputfiles: List[str], output: str, skip_header: bool = False,
                    drop_duplicates: bool = False, **kwargs) -> None:
    """
    Concatenate gzipped CSV files, dtypes in meta YAML files must be the same.

    @param inputfiles: List of gzipped CSV file paths, or a dictionary where the keys are file paths.
    @param output: Path of resulting concatenated gzipped CSV file and meta YAML.
    @param skip_header: boolean, True = write header, False = don't write header.
    @return:
    """
    if kwargs.get('write_header') is not None:
        warn('write_header has been deprecated and will be ignored, please use skip_header instead', DeprecationWarning)

    if isinstance(inputfiles, dict):
        inputfiles = list(inputfiles.values())

    if inputfiles == []:
        raise CsverveConcatException("nothing provided to concat")

    inputs: List[CsverveInput] = [CsverveInput(infile) for infile in inputfiles]

    dtypes: Dict[str, str] = utils.merge_dtypes([csvinput.dtypes for csvinput in inputs])

    headers: List[bool] = [csvinput.header for csvinput in inputs]

    columns: List[List[str]] = [csvinput.columns for csvinput in inputs]

    low_memory: bool = True
    if any(headers):
        low_memory = False

    if not all(columns[0] == elem for elem in columns):
        low_memory = False

    if drop_duplicates:
        low_memory = False

    if low_memory:
        concatenate_csv_files_quick_lowmem(inputfiles, output, dtypes, columns[0], skip_header=skip_header)
    else:
        concatenate_csv_files_pandas(inputfiles, output, dtypes, skip_header=skip_header,
                                     drop_duplicates=drop_duplicates)


def annotate_csv(
        infile: str,
        annotation_df: pd.DataFrame,
        outfile,
        annotation_dtypes,
        on="cell_id",
        skip_header: bool = False,
        **kwargs
):
    """
    TODO: fill this in
    @param infile:
    @param annotation_df:
    @param outfile:
    @param annotation_dtypes:
    @param on:
    @param skip_header:
    @return:
    """

    if kwargs.get('write_header') is not None:
        warn('write_header has been deprecated and will be ignored, please use skip_header instead', DeprecationWarning)

    csvinput = CsverveInput(infile)
    metrics_df = csvinput.read_csv()

    # get annotation rows that correspond to rows in on
    reformed_annotation = annotation_df[annotation_df[on].isin(metrics_df[on])]

    # do nothing if the annotation df is empty
    if reformed_annotation.empty:  # so we dont add NaNs
        return write_dataframe_to_csv_and_yaml(metrics_df, outfile,
                                               csvinput.dtypes,
                                               skip_header=skip_header)

    metrics_df = metrics_df.merge(reformed_annotation, on=on, how='outer')

    csv_dtypes = csvinput.dtypes

    for col, dtype in csv_dtypes.items():
        if col in annotation_dtypes:
            assert dtype == annotation_dtypes[col]

    csv_dtypes.update(annotation_dtypes)

    output = CsverveOutputDataFrame(metrics_df, outfile, csv_dtypes, skip_header=skip_header)
    output.write_df()


def simple_annotate_csv(
        in_f: str,
        out_f: str,
        col_name: str,
        col_val: str,
        col_dtype: str,
        skip_header: bool = False,
        **kwargs
) -> None:
    """
    Simplified version of the annotate_csv method.
    Add column with the same value for all rows.

    @param in_f:
    @param out_f:
    @param col_name:
    @param col_val:
    @param col_dtype:
    @param skip_header:
    @return:
    """
    if kwargs.get('write_header') is not None:
        warn('write_header has been deprecated and will be ignored, please use skip_header instead', DeprecationWarning)

    csvinput = CsverveInput(in_f)
    metrics_df = csvinput.read_csv()
    metrics_df[col_name] = col_val

    csv_dtypes = csvinput.dtypes
    csv_dtypes[col_name] = col_dtype

    output = CsverveOutputDataFrame(metrics_df, out_f, csv_dtypes, skip_header=skip_header)
    output.write_df()


def add_col_from_dict(
        infile,
        col_data,
        outfile,
        dtypes,
        skip_header=False,
        **kwargs
):
    """
    TODO: fill this in
    Add column to gzipped CSV.

    @param infile:
    @param col_data:
    @param outfile:
    @param dtypes:
    @param skip_header:
    @return:
    """

    if kwargs.get('write_header') is not None:
        warn('write_header has been deprecated and will be ignored, please use skip_header instead', DeprecationWarning)

    csvinput = CsverveInput(infile)
    csv_dtypes = csvinput.dtypes
    csvinput = csvinput.read_csv()

    for col_name, col_value in col_data.items():
        csvinput[col_name] = col_value

    dtypes = utils.merge_dtypes([csv_dtypes, dtypes])
    output = CsverveOutputDataFrame(
        csvinput, outfile, dtypes, skip_header=skip_header
    )
    output.write_df()


def write_dataframe_to_csv_and_yaml(
        df: pd.DataFrame,
        outfile: str,
        dtypes: Dict[str, str],
        skip_header: bool = False,
        **kwargs
) -> None:
    """
    Output pandas dataframe to a CSV and meta YAML files.

    @param df: pandas DataFrame.
    @param outfile: Path of CSV & YAML file to be written to.
    @param dtypes: dictionary of pandas dtypes by column, keys = column name, value = dtype.
    @param skip_header: boolean, True = skip writing header, False = write header
    @return:
    """

    if kwargs.get('write_header') is not None:
        warn('write_header has been deprecated and will be ignored, please use skip_header instead', DeprecationWarning)

    csvoutput: CsverveOutputDataFrame = CsverveOutputDataFrame(
        df, outfile, dtypes, skip_header=skip_header
    )
    csvoutput.write_df()


def read_csv(infile: str, chunksize: int = None, usecols=None, dtype=None) -> pd.DataFrame:
    """
    Read in CSV file and return as a pandas DataFrame.

    Assumes a YAML meta file in the same path with the same name, with a .yaml extension.
    YAML file structure is atop this file.

    @param infile: Path to CSV file.
    @param chunksize: Number of rows to read at a time (optional, applies to large datasets).
    @param usecols: Restrict to specific columns (optional).
    @param dtype: Override the dtypes on specific columns (optional).
    @return: pandas DataFrame.
    """
    return CsverveInput(infile).read_csv(chunksize=chunksize, usecols=usecols, dtype=dtype)


def remove_duplicates(
        filepath: str, outputfile: str, skip_header: bool = False,

) -> None:
    """
    remove duplicate rows

    Assumes a YAML meta file in the same path with the same name, with a .yaml extension.
    YAML file structure is atop this file.

    @param filepath: Path to CSV file.
    @param outputfile: Path to CSV file.
    """

    csvinput = CsverveInput(filepath)

    df = csvinput.read_csv()

    df = df.drop_duplicates(keep='first')

    csvoutput: CsverveOutputDataFrame = CsverveOutputDataFrame(
        df, outputfile, csvinput.dtypes, skip_header=skip_header
    )
    csvoutput.write_df()
