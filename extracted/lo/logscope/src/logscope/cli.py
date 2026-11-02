"""Command-line interface for Logscope."""

import argparse
from logscope.report import view_runs

def main():
    """Entry point for the logscope CLI."""
    parser = argparse.ArgumentParser(
        description='Logscope - Queryable logging with SQLite storage',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--db-path',
        default='logscope.db',
        help='Path to the SQLite database file (default: logscope.db)'
    )
    
    parser.add_argument(
        '--runs',
        type=int,
        default=1,
        help='Number of recent runs to view (default: 1)'
    )
    
    args = parser.parse_args()
    
    view_runs(args.db_path, args.runs)


if __name__ == '__main__':
    main() 