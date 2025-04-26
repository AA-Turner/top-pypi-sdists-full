CSV = 'csv'
NDJSON = 'ndjson'
PARQUET = 'parquet'

ALL = (CSV, NDJSON, PARQUET)

def mime_type_for(fmt):
    if fmt == 'csv':
        return 'text/csv; charset=utf-8'
    if fmt == 'ndjson':
        return 'application/x-ndjson; charset=utf-8'
    if fmt == 'parquet':
        return 'application/vnd.apache.parquet'
    # This error condition should not be triggered. Arriving here means client
    # code is hard-coding strings instead of using the constants above.
    raise Exception(f'Unknown format: {fmt}')
