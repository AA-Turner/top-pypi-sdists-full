from .connect import *
def get_db_table_count(table):
    query = f"SELECT COUNT(*) FROM {table}"
    count = query_data(query)
    return count[0].get('count')
def get_latest_from_table(table=None,limit = None,offset=None,asc=None):
    table = table or 'log_payloads'
    asc = 'ASC' if asc else 'DESC'
    limit = limit or 1
    offset = offset or 1
    rows = query_data(f'''
        SELECT *
        FROM {table}
        ORDER BY id {asc}
        LIMIT {limit}
        OFFSET {offset}
        ''')
    return rows
