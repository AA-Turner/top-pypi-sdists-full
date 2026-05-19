import unicodedata

import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.types as patypes


def format_csv(table: pa.Table, info: str = "") -> str:
    """Format an Arrow table as a pipe-delimited CSV string, cleaning text columns.

    - cleans string/large_string columns by normalizing unicode, stripping non-ascii
      characters, and replacing newlines with spaces.
    - preserves original column types and table schema/metadata.
    """
    cleaned_columns: list[pa.Array] = []
    field_names = table.schema.names

    def _clean_value(x: object) -> object:
        if x is None:
            return None
        s = unicodedata.normalize("NFKD", str(x))
        s = s.encode("ascii", "ignore").decode("ascii")
        s = s.replace("\n", " ").replace("\r", " ")
        return s

    for name in field_names:
        field = table.schema.field(name)
        col = table[name]
        if patypes.is_string(field.type) or patypes.is_large_string(field.type):
            cleaned_list = [_clean_value(v) for v in col.to_pylist()]
            cleaned_arr = pa.array(cleaned_list, type=field.type)
            cleaned_columns.append(cleaned_arr)
        else:
            cleaned_columns.append(col)

    cleaned_table = pa.table(cleaned_columns, schema=table.schema)

    if info:
        info += "csv delimited with | containing header starts in next line:\n"

    sink = pa.BufferOutputStream()
    write_options = pacsv.WriteOptions(delimiter="|", include_header=True)
    pacsv.write_csv(cleaned_table, sink, write_options=write_options)
    csv_text = sink.getvalue().to_pybytes().decode("utf-8")
    return str(info + csv_text)
