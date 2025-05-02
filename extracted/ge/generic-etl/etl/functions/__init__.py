from .ccsv import custom_intersection
from .general import execute_sql, merge_csv, move_frame, sub_run

FUNCTIONS = {
    "sql": execute_sql,
    "pandas_push": move_frame,
    "cat": sub_run,
    "python": sub_run,
    "merge_csv": merge_csv,
    "intersection": custom_intersection,
}
