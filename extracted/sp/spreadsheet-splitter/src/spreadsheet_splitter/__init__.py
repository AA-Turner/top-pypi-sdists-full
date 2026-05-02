import argparse
from .splitter import split_spreadsheet_file, split_large_spreadsheet_file

def main() -> None:
    parser = argparse.ArgumentParser(description="Split a Spreadsheet (.xls or .xlsx) file into smaller parts.")
    parser.add_argument("input_file", help="Path to the input .xls or .xlsx file")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="output",
        help="Directory to save output files (default: output)"
    )
    parser.add_argument(
        "-t",
        "--title-rows",
        type=int,
        default=1,
        help="Number of top rows to treat as title rows (default: 1, ignored in --large mode)"
    )
    parser.add_argument(
        "--large",
        action="store_true",
        help="Process large files iteratively with limited rows per iteration"
    )
    parser.add_argument(
        "--rows-per-iteration",
        type=int,
        default=500,
        help="Number of data rows to process per iteration (default: 500)"
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=10,
        help="Maximum number of iterations to process (default: 10)"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume processing from the last row in the log file"
    )
    parser.add_argument(
        "--log-file",
        default="split_log.json",
        help="Path to the log file for tracking processed rows (default: split_log.json)"
    )
    parser.add_argument(
        "--columns",
        type=int,
        help="Number of columns to process (default: all columns)"
    )
    args = parser.parse_args()

    try:
        if args.large:
            split_large_spreadsheet_file(
                args.input_file,
                args.output_dir,
                args.rows_per_iteration,
                args.max_iterations,
                args.resume,
                args.log_file,
                args.columns
            )
        else:
            split_spreadsheet_file(args.input_file, args.output_dir, args.title_rows, args.columns)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
