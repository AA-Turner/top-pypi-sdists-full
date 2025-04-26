import fsspec
import pyarrow.parquet as pq
import sys
import braceexpand

# set the paths of the parquet files using brace expand

file_paths = [b for a in sys.argv[1:] for b in braceexpand.braceexpand(a) ]

print(file_paths)

# use fsspec to open the parquet files

def _open_arrow_table(path):
    fs, _, paths = fsspec.get_fs_token_paths(path)
    return pq.read_metadata(paths[0], filesystem=fs)


tables = (_open_arrow_table(f) for f in file_paths)

# read the parquet files and concatenate the resulting tables
#tables = (pq.read_table(file_stream) for file_stream in file_streams)

total_rows = 0
input_ids = 0
for t in tables:
  total_rows += t.num_rows
  for g in range(t.num_row_groups):
      input_ids += t.row_group(g).column(0).statistics.num_values

print("Total number of rows: ", total_rows)
print("input_ids",input_ids)
