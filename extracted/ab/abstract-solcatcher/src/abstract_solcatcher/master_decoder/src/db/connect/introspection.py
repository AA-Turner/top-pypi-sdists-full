from .core import query_data

def get_all_table_names(schema="public"):
    return [
        r["table_name"]
        for r in query_data(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s
              AND table_type = 'BASE TABLE'
            """,
            [schema],
        )
    ]
