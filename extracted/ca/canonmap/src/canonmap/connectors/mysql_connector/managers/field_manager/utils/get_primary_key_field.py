def get_primary_key_field(self, conn, table_name: str) -> str:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT column_name
            FROM information_schema.key_column_usage
            WHERE table_schema = %s AND table_name = %s AND constraint_name = 'PRIMARY'
            LIMIT 1
        """, (self.connection_manager.config.database, table_name))
        row = cur.fetchone()
        if row:
            return row[0]
        raise RuntimeError(f"No primary key found for table {table_name}")