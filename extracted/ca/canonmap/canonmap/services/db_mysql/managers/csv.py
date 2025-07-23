import logging
import csv
from pathlib import Path
from typing import Union, List, Dict, Any, Tuple
import pandas as pd

from canonmap.services.db_mysql.adapters.connection import ConnectionManager
from canonmap.services.db_mysql.helpers.create_ddl import create_mysql_ddl

logger = logging.getLogger(__name__)

class CSVManager:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    def create_table_ddl_from_csv(
        self,
        csv_path_or_buffer,
        table_name: str,
        save_dir: Union[None, str, Path] = None
    ) -> str:
        return create_mysql_ddl(csv_path_or_buffer, table_name, save_dir)

    def _smart_fix_csv(
        self,
        csv_path: Union[str, Path],
        fixed_csv_path: Union[str, Path] = "fixed.csv",
        bad_rows_path: Union[str, Path] = "bad_rows.csv",
        log_bad_rows: bool = True
    ) -> Tuple[str, List[Tuple[int, str]]]:
        """
        Reads a CSV, identifies and separates malformed rows, and writes a clean version.
        A row is considered malformed if it has a different number of columns than the header.
        It attempts to fix rows with more columns by merging adjacent fields.
        
        Returns:
            Tuple[str, List[Tuple[int, str]]]: (fixed_csv_path, bad_rows_data)
        """
        csv_path = Path(csv_path)
        fixed_csv_path = Path(fixed_csv_path)
        bad_rows_path = Path(bad_rows_path)
        
        bad_rows_data = []

        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as infile:
                # Read header to determine expected number of columns
                try:
                    header = next(csv.reader(infile))
                    expected_cols = len(header)
                except StopIteration:
                    logger.warning(f"CSV file '{csv_path}' is empty.")
                    # Create empty fixed file and return
                    fixed_csv_path.touch()
                    return str(fixed_csv_path), []

                # Rewind and process whole file
                infile.seek(0)
                reader = csv.reader(infile)
                next(reader) # Skip header

                with open(fixed_csv_path, 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(header)

                    for lineno, row in enumerate(reader, start=2):
                        if len(row) == expected_cols:
                            writer.writerow(row)
                        elif len(row) > expected_cols:
                            # Heuristic: try to merge fields to fix it.
                            # This merges the second field with subsequent fields to meet the expected column count.
                            num_extra_cols = len(row) - expected_cols
                            merged_row = row[:1] + [','.join(row[1:1 + num_extra_cols + 1])] + row[1 + num_extra_cols + 1:]
                            if len(merged_row) == expected_cols:
                                writer.writerow(merged_row)
                                logger.debug(f"Fixed line {lineno} by merging columns.")
                            else:
                                # This case should ideally not be reached with this logic
                                bad_rows_data.append((lineno, ','.join(row)))
                        else: # len(row) < expected_cols
                            # This is a malformed row, log it. 
                            # Don't pad, as it can hide data integrity issues.
                            bad_rows_data.append((lineno, ','.join(row)))
            
            if bad_rows_data and log_bad_rows:
                logger.warning(f"Found {len(bad_rows_data)} malformed row(s). Writing them to '{bad_rows_path}'.")
                with open(bad_rows_path, 'w', newline='', encoding='utf-8') as bad_file:
                    writer = csv.writer(bad_file)
                    writer.writerow(['line_number', 'original_content'])
                    for lineno, content in bad_rows_data:
                        writer.writerow([lineno, content])

            logger.info(f"✅ Finished cleaning. Clean CSV written to: {fixed_csv_path}")
            return str(fixed_csv_path), bad_rows_data

        except Exception as e:
            logger.error(f"Error processing CSV file '{csv_path}': {e}")
            raise

    def process_csv_to_json(
        self,
        csv_path: Union[str, Path],
        table_name: str
    ) -> Tuple[List[Dict[str, Any]], str]:
        """
        Process a CSV file: clean it, convert to JSON format, and generate DDL statement.
        
        Args:
            csv_path (Union[str, Path]): Path to the CSV file
            table_name (str): Name of the table for DDL generation
            
        Returns:
            Tuple[List[Dict[str, Any]], str]: (json_data, ddl_statement)
        """
        try:
            # Use a more descriptive name for the bad rows file.
            bad_rows_csv_path = Path(csv_path).stem + "_bad_rows.csv"
            fixed_csv_path, bad_rows = self._smart_fix_csv(
                csv_path, 
                bad_rows_path=bad_rows_csv_path,
                log_bad_rows=True
            )
            
            if not Path(fixed_csv_path).exists() or Path(fixed_csv_path).stat().st_size == 0:
                logger.warning(f"CSV file '{csv_path}' is empty or could not be processed. Nothing to load.")
                return [], ""

            # Generate DDL statement
            ddl_statement = self.create_table_ddl_from_csv(fixed_csv_path, table_name)
            
            # Convert CSV to JSON format
            import pandas.errors
            logger.info(f"Converting CSV '{fixed_csv_path}' to JSON format...")
            try:
                # Read the CSV, keeping blank values as empty strings and handling NaNs
                df = pd.read_csv(fixed_csv_path, keep_default_na=False, na_values=[''])

                # Replace any numpy NaN values with None for SQL compatibility (NULL)
                df = df.astype(object).where(pd.notnull(df), None)
                
                # Convert DataFrame to list of dictionaries
                json_data = df.to_dict('records')
                
                logger.info(f"✅ Converted {len(json_data)} rows to JSON format")
                return json_data, ddl_statement

            except pandas.errors.ParserError as e:
                logger.error(f"ParserError while reading cleaned CSV '{fixed_csv_path}': {e}")
                raise
            except Exception as e:
                logger.error(f"An unexpected error occurred while reading the CSV: {e}")
                raise
            
        except Exception as e:
            logger.error(f"Error while processing CSV '{csv_path}': {e}")
            raise