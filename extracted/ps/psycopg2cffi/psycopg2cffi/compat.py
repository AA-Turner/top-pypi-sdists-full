import sys
import psycopg2cffi


def register():
    sys.modules['psycopg2'] = psycopg2cffi

