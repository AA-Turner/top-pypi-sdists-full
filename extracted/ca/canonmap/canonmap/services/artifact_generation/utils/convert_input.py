from typing import Union, Dict, Any, Optional, List
import pandas as pd
from pathlib import Path
import glob

from canonmap.utils.logger import setup_logger
from canonmap.services.artifact_generation.utils.load_csv import convert_csv_to_df

logger = setup_logger(__name__)

def process_directory(
    dir_path: str,
    recursive: bool = False,
    file_pattern: Union[str, List[str]] = "*.csv",
    num_rows: Optional[int] = None
) -> Dict[str, pd.DataFrame]:
    """
    Process all files in a directory matching the given pattern(s).
    
    Args:
        dir_path: Directory path to process
        recursive: Whether to search subdirectories
        file_pattern: Glob pattern(s) for file matching. Can be a string or list of strings.
        num_rows: Maximum number of rows to process per file
        
    Returns:
        Dict mapping table names to DataFrames
        
    Table Naming Strategy:
        - When recursive=False: Uses filename without extension as table name
        - When recursive=True: Uses relative path with separators replaced by underscores
        - If conflicts occur: Appends incremental counter (e.g., table_1, table_2)
        
    Examples:
        Directory structure:
        data/
        ├── main.csv
        ├── subdir1/
        │   ├── file1.csv
        │   └── file2.csv
        └── subdir2/
            └── deep/
                └── file1.csv
                
        With recursive=True:
        - data/main.csv -> "main"
        - data/subdir1/file1.csv -> "subdir1_file1"
        - data/subdir1/file2.csv -> "subdir1_file2"
        - data/subdir2/deep/file1.csv -> "subdir2_deep_file1"
    """
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        raise ValueError(f"Path {dir_path} is not a directory")

    # Convert single pattern to list for uniform processing
    if isinstance(file_pattern, str):
        file_patterns = [file_pattern]
    else:
        file_patterns = file_pattern

    all_files = set()  # Use set to avoid duplicates
    
    for pattern in file_patterns:
        pattern_with_recursive = "**/" + pattern if recursive else pattern
        search_path = dir_path / pattern_with_recursive
        
        files = glob.glob(str(search_path), recursive=recursive)
        all_files.update(files)
    
    if not all_files:
        pattern_str = ", ".join(file_patterns)
        raise ValueError(f"No files matching patterns '{pattern_str}' found in {dir_path}")

    dfs = {}
    filename_counts = {}  # Track how many times each filename appears
    
    for file_path in sorted(all_files):  # Sort for consistent ordering
        file_path = Path(file_path)
        base_table_name = file_path.stem
        
        # Handle naming conflicts when recursive=True
        if recursive:
            # Create a unique table name based on the relative path
            try:
                relative_path = file_path.relative_to(dir_path)
                # Replace path separators with underscores and remove extension
                table_name = str(relative_path).replace('/', '_').replace('\\', '_').replace('.', '_')
                # Remove the final extension if it exists
                if '.' in table_name:
                    table_name = '.'.join(table_name.split('.')[:-1])
            except ValueError:
                # Fallback if relative_to fails
                table_name = base_table_name
        else:
            table_name = base_table_name
        
        # If we still have conflicts (same table_name), append a counter
        if table_name in filename_counts:
            filename_counts[table_name] += 1
            table_name = f"{table_name}_{filename_counts[table_name]}"
        else:
            filename_counts[table_name] = 0

        try:
            if file_path.suffix.lower() == '.json':
                df = pd.read_json(file_path)
            else:
                df = convert_csv_to_df(str(file_path))

            if num_rows and num_rows < len(df):
                df = df.head(num_rows)

            dfs[table_name] = df
            logger.info(f"Successfully processed {file_path} -> table: {table_name}")

        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            continue

    if not dfs:
        raise ValueError("No files were successfully processed")

    return dfs

def convert_data_to_df(
    input_path: Union[str, pd.DataFrame, Dict[str, Any]],
    num_rows: Optional[int] = None,
    recursive: bool = False,
    file_pattern: Union[str, List[str]] = "*.csv",
) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Convert various input formats to pandas DataFrames.
    
    Args:
        input_path: Input data (file path, DataFrame, or dict)
        num_rows: Maximum number of rows to process
        recursive: Whether to search subdirectories
        file_pattern: Glob pattern(s) for file matching. Can be a string or list of strings.
        
    Returns:
        DataFrame or dict of DataFrames
    """
    if isinstance(input_path, pd.DataFrame):
        return input_path.head(num_rows) if num_rows and num_rows < len(input_path) else input_path

    elif isinstance(input_path, dict):
        # Check if this is a dict of DataFrames
        if all(isinstance(v, pd.DataFrame) for v in input_path.values()):
            # Return the dict of DataFrames directly
            if num_rows:
                return {k: v.head(num_rows) if num_rows < len(v) else v for k, v in input_path.items()}
            return input_path
        else:
            # Try to create a DataFrame from the dict
            df = pd.DataFrame(input_path)
            return df.head(num_rows) if num_rows and num_rows < len(df) else df

    elif isinstance(input_path, str):
        path = Path(input_path)
        if path.is_dir():
            return process_directory(
                str(path),
                recursive=recursive,
                file_pattern=file_pattern,
                num_rows=num_rows
            )
        else:
            if path.suffix.lower() == '.json':
                df = pd.read_json(input_path)
            else:
                df = convert_csv_to_df(input_path)

            return df.head(num_rows) if num_rows and num_rows < len(df) else df

    raise ValueError(f"Unsupported input type: {type(input_path)}")