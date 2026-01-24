# type: ignore
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


from csverve.api import rewrite_csv_file
from csverve.api import merge_csv
from csverve.api import concatenate_csv
from csverve.api import annotate_csv
from csverve.api import simple_annotate_csv
from csverve.api import add_col_from_dict
from csverve.api import write_dataframe_to_csv_and_yaml
from csverve.api import read_csv
from csverve.api import get_columns
from csverve.api import get_dtypes
from csverve.api import remove_duplicates