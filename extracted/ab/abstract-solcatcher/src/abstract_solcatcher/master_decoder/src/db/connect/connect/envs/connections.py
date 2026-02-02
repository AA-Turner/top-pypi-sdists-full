from .imports import *
def getConnection(dbname=None,
            user=None,
            password=None,
            host=None,
            port=None):
    return psycopg2.connect(
            dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
