
from ..imports import sql,logging,RealDictCursor,contextmanager
from .connect import get_connection, release_connection

log = logging.getLogger(__name__)

@contextmanager
def db_conn():
    conn = get_connection()
    try:
        yield conn
    finally:
        release_connection(conn)


def query_data(query, values=None, zipit=None,zip_rows=None):
    """
    Safe query execution.
    - Supports sql.SQL / sql.Composed
    - Always releases connection
    """
    if zipit == None:
        zipit = zip_rows
    if zipit == None:
        zipit = True
    with db_conn() as conn:
        cursor_factory = RealDictCursor if zipit else None
        with conn.cursor(cursor_factory=cursor_factory) as cur:
            try:
                if isinstance(query, (sql.SQL, sql.Composed)):
                    cur.execute(query, values)
                else:
                    cur.execute(query, values)

                if cur.description:
                    rows = cur.fetchall()
                    if rows:
                        log.debug("First row: %s", rows[0])
                    return rows

                conn.commit()
                return []

            except Exception:
                conn.rollback()
                log.exception("DB QUERY FAILED")
                raise
