import xlrd
import xlwt
import pandas as pd
import math
import os
import json
from typing import Tuple, Optional
from datetime import datetime
import sys
from pyexcelerate import Workbook
import psutil

def _split_xls_file(input_path: str, output_dir: str, title_rows: int, columns: Optional[int] = None) -> Tuple[str, str]:
    """
    Split an .xls file into two equal parts using xlrd/xlwt, preserving title rows.

    Args:
        input_path (str): Path to the input .xls file
        output_dir (str): Directory to save output files
        title_rows (int): Number of top rows to treat as title rows
        columns (Optional[int]): Number of columns to process (default: None, all columns)

    Returns:
        Tuple[str, str]: Paths to the two output files
    """
    workbook = xlrd.open_workbook(input_path)
    sheet = workbook.sheet_by_index(0)
    total_rows = sheet.nrows
    total_cols = sheet.ncols if columns is None else min(columns, sheet.ncols)

    if title_rows > total_rows:
        raise ValueError(f"Number of title rows ({title_rows}) cannot exceed total rows ({total_rows})")

    data_rows = total_rows - title_rows
    split_point = math.ceil(data_rows / 2) + title_rows

    workbook1 = xlwt.Workbook()
    workbook2 = xlwt.Workbook()
    sheet1 = workbook1.add_sheet(sheet.name)
    sheet2 = workbook2.add_sheet(sheet.name)

    for row in range(title_rows):
        for col in range(total_cols):
            sheet1.write(row, col, sheet.cell_value(row, col))
            sheet2.write(row, col, sheet.cell_value(row, col))

    for row in range(title_rows, min(split_point, total_rows)):
        for col in range(total_cols):
            sheet1.write(row, col, sheet.cell_value(row, col))

    for row in range(split_point, total_rows):
        for col in range(total_cols):
            sheet2.write(row - split_point + title_rows, col, sheet.cell_value(row, col))

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path1 = os.path.join(output_dir, f"{base_name}_part1.xls")
    output_path2 = os.path.join(output_dir, f"{base_name}_part2.xls")

    workbook1.save(output_path1)
    workbook2.save(output_path2)

    return output_path1, output_path2

def _split_xlsx_file(input_path: str, output_dir: str, title_rows: int, columns: Optional[int] = None) -> Tuple[str, str]:
    """
    Split an .xlsx file into two equal parts using pandas, preserving title rows.

    Args:
        input_path (str): Path to the input .xlsx file
        output_dir (str): Directory to save output files
        title_rows (int): Number of top rows to treat as title rows
        columns (Optional[int]): Number of columns to process (default: None, all columns)

    Returns:
        Tuple[str, str]: Paths to the two output files
    """
    usecols = list(range(columns)) if columns is not None else None
    df = pd.read_excel(input_path, nrows=1, engine='openpyxl', usecols=usecols)
    total_rows = pd.read_excel(input_path, engine='openpyxl', sheet_name=0, usecols=usecols).shape[0]

    if title_rows > total_rows:
        raise ValueError(f"Number of title rows ({title_rows}) cannot exceed total rows ({total_rows})")

    data_rows = total_rows - title_rows
    split_point = math.ceil(data_rows / 2) + title_rows

    df1 = pd.read_excel(input_path, nrows=split_point, engine='openpyxl', usecols=usecols)
    df2 = pd.read_excel(input_path, skiprows=split_point, nrows=total_rows - split_point, engine='openpyxl', usecols=usecols)

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path1 = os.path.join(output_dir, f"{base_name}_part1.xlsx")
    output_path2 = os.path.join(output_dir, f"{base_name}_part2.xlsx")

    wb1 = Workbook()
    wb1.new_sheet("Sheet1", data=[df1.columns.tolist()] + df1.values.tolist())
    wb1.save(output_path1)

    wb2 = Workbook()
    wb2.new_sheet("Sheet1", data=[df2.columns.tolist()] + df2.values.tolist())
    wb2.save(output_path2)

    return output_path1, output_path2

def _process_xls_chunk(workbook: xlrd.book.Book, output_dir: str, start_row: int, rows_per_iteration: int, file_index: int, sheet_name: str, columns: Optional[int] = None) -> Tuple[str, int]:
    """
    Process a chunk of rows from an .xls file, saving to a new file.

    Args:
        workbook (xlrd.book.Book): Open xlrd workbook
        output_dir (str): Directory to save output files
        start_row (int): Starting row index (0-based)
        rows_per_iteration (int): Number of rows to process in this chunk
        file_index (int): Index for naming the output file
        sheet_name (str): Name of the sheet
        columns (Optional[int]): Number of columns to process (default: None, all columns)

    Returns:
        Tuple[str, int]: Output file path and last processed row index
    """
    sheet = workbook.sheet_by_index(0)
    total_rows = sheet.nrows
    total_cols = sheet.ncols if columns is None else min(columns, sheet.ncols)

    end_row = min(start_row + rows_per_iteration, total_rows)

    output_workbook = xlwt.Workbook()
    output_sheet = output_workbook.add_sheet(sheet_name)

    for row in range(start_row, end_row):
        for col in range(total_cols):
            output_sheet.write(row - start_row, col, sheet.cell_value(row, col))

    base_name = os.path.splitext(os.path.basename(workbook._filename))[0]
    output_path = os.path.join(output_dir, f"{base_name}_part{file_index:03d}.xls")
    output_workbook.save(output_path)

    return output_path, end_row - 1

def _process_xlsx_chunk(input_path: str, output_dir: str, start_row: int, rows_per_iteration: int, file_index: int, columns: Optional[int] = None) -> Tuple[str, int]:
    """
    Process a chunk of rows from an .xlsx file using pandas, saving to a new file.

    Args:
        input_path (str): Path to the input .xlsx file
        output_dir (str): Directory to save output files
        start_row (int): Starting row index (0-based)
        rows_per_iteration (int): Number of rows to process in this chunk
        file_index (int): Index for naming the output file
        columns (Optional[int]): Number of columns to process (default: None, all columns)

    Returns:
        Tuple[str, int]: Output file path and last processed row index
    """
    usecols = list(range(columns)) if columns is not None else None
    memory_before = psutil.Process().memory_info().rss / 1024**2
    print(f"Memory before reading chunk: {memory_before:.2f} MB")

    df_chunk = pd.read_excel(
        input_path,
        skiprows=start_row,
        nrows=rows_per_iteration,
        engine='openpyxl',
        usecols=usecols
    )

    memory_after = psutil.Process().memory_info().rss / 1024**2
    print(f"Memory after reading chunk: {memory_after:.2f} MB")

    total_rows = len(df_chunk)
    end_row = start_row + total_rows

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}_part{file_index:03d}.xlsx")

    wb = Workbook()
    wb.new_sheet("Sheet1", data=[df_chunk.columns.tolist()] + df_chunk.values.tolist())
    wb.save(output_path)

    del df_chunk  # Free memory
    return output_path, end_row - 1, {"memory_before_mb": memory_before, "memory_after_mb": memory_after}

def split_spreadsheet_file(input_path: str, output_dir: str = "output", title_rows: int = 1, columns: Optional[int] = None) -> None:
    """
    Split an Spreadsheet (.xls or .xlsx) file into two equal parts, preserving specified title rows.

    Args:
        input_path (str): Path to the input .xls or .xlsx file
        output_dir (str): Directory to save output files
        title_rows (int): Number of top rows to treat as title rows (default: 1)
        columns (Optional[int]): Number of columns to process (default: None, all columns)
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} does not exist")
    if not input_path.lower().endswith(('.xls', '.xlsx')):
        raise ValueError("Input file must be an .xls or .xlsx file")
    if title_rows < 0:
        raise ValueError("Number of title rows cannot be negative")
    if columns is not None and columns <= 0:
        raise ValueError("Number of columns must be positive")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if input_path.lower().endswith('.xls'):
        output_path1, output_path2 = _split_xls_file(input_path, output_dir, title_rows, columns)
    else:
        output_path1, output_path2 = _split_xlsx_file(input_path, output_dir, title_rows, columns)

    print(f"Files saved as: {output_path1} and {output_path2}")

def split_large_spreadsheet_file(
    input_path: str,
    output_dir: str = "output",
    rows_per_iteration: int = 500,
    max_iterations: int = 10,
    resume: bool = False,
    log_file: str = "split_log.json",
    columns: Optional[int] = None
) -> None:
    """
    Split a large Spreadsheet (.xls or .xlsx) file into smaller files with limited rows per iteration.

    Args:
        input_path (str): Path to the input .xls or .xlsx file
        output_dir (str): Directory to save output files
        rows_per_iteration (int): Number of rows to process per iteration (default: 500)
        max_iterations (int): Maximum number of iterations to process (default: 10)
        resume (bool): Whether to resume from the last processed row (default: False)
        log_file (str): Path to the log file (default: split_log.json)
        columns (Optional[int]): Number of columns to process (default: None, all columns)
    """
    # Validate inputs
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} does not exist")
    if not input_path.lower().endswith(('.xls', '.xlsx')):
        raise ValueError("Input file must be an .xls or .xlsx file")
    if rows_per_iteration <= 0:
        raise ValueError("Rows per iteration must be positive")
    if max_iterations <= 0:
        raise ValueError("Max iterations must be positive")
    if columns is not None and columns <= 0:
        raise ValueError("Number of columns must be positive")

    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize log
    log_data = {
        "input_path": input_path,
        "output_dir": output_dir,
        "rows_per_iteration": rows_per_iteration,
        "processed_ranges": [],
        "last_row_processed": 0,
        "timestamp": "",
        "columns": columns,
        "file_profile": {},
        "memory_usage": []
    }

    # Profile the file
    is_xls = input_path.lower().endswith('.xls')
    total_rows = 0
    total_cols = 0
    dtypes = {}

    if is_xls:
        workbook = xlrd.open_workbook(input_path, on_demand=True)
        sheet = workbook.sheet_by_index(0)
        total_rows = sheet.nrows
        total_cols = sheet.ncols
        sheet_name = sheet.name
    else:
        usecols = list(range(columns)) if columns is not None else None
        df_profile = pd.read_excel(input_path, engine='openpyxl', sheet_name=0, usecols=usecols, nrows=1)
        total_cols = df_profile.shape[1]
        dtypes = df_profile.dtypes.astype(str).to_dict()
        df_count = pd.read_excel(input_path, engine='openpyxl', sheet_name=0, usecols=usecols, nrows=1)
        total_rows = df_count.shape[0]
        del df_profile, df_count  # Free memory

    # Validate columns
    if columns is not None and columns > total_cols:
        raise ValueError(f"Specified columns ({columns}) exceeds actual columns ({total_cols}) in the file")

    log_data["file_profile"] = {
        "total_rows": total_rows,
        "total_columns": total_cols,
        "data_types": dtypes if not is_xls else "Not available for .xls"
    }

    if total_rows == 0:
        print("Warning: Input file has no rows. No processing will be performed.")
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        return

    # Check for existing log file to resume
    start_row = 0
    file_index = 1
    if resume and os.path.exists(log_file):
        with open(log_file, 'r') as f:
            log_data = json.load(f)
        if log_data["input_path"] != input_path:
            raise ValueError("Log file input path does not match provided input path")
        if log_data.get("columns") != columns:
            raise ValueError("Log file column count does not match provided column count")
        start_row = log_data["last_row_processed"]
        file_index = len(log_data["processed_ranges"]) + 1

    print(f"File profile: {total_rows} rows, {total_cols} columns")
    if not is_xls:
        print(f"Data types: {dtypes}")

    processed_files = []

    try:
        for i in range(max_iterations):
            print(f"Processing iteration {i + 1}/{max_iterations} (rows {start_row + 1} to {min(start_row + rows_per_iteration, total_rows)})...", end='\r')
            sys.stdout.flush()

            if is_xls:
                output_path, last_row = _process_xls_chunk(
                    workbook, output_dir, start_row, rows_per_iteration, file_index, sheet_name, columns
                )
                memory_info = {"memory_before_mb": 0, "memory_after_mb": 0}  # No memory tracking for .xls
            else:
                output_path, last_row, memory_info = _process_xlsx_chunk(
                    input_path, output_dir, start_row, rows_per_iteration, file_index, columns
                )

            # Update log
            log_data["processed_ranges"].append({
                "file": output_path,
                "start_row": start_row + 1,
                "end_row": last_row + 1,
                "iteration": i + 1
            })
            log_data["last_row_processed"] = last_row
            log_data["timestamp"] = datetime.now().isoformat()
            log_data["memory_usage"].append({
                "iteration": i + 1,
                "memory_before_mb": memory_info["memory_before_mb"],
                "memory_after_mb": memory_info["memory_after_mb"]
            })

            # Save log incrementally
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)

            processed_files.append(output_path)
            file_index += 1
            start_row = last_row + 1

            # Check if we've reached the end of the file
            if start_row >= total_rows:
                break

    finally:
        if is_xls and workbook:
            workbook.release_resources()

    print("\nDone.")
    if processed_files:
        print("Processed files:")
        for f in processed_files:
            print(f"- {f}")
        print(f"Log saved to: {log_file}")
    else:
        print("No files processed.")
