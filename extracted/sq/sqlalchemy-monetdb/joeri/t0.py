#!/usr/bin/env python

import logging

import datetime
import sqlalchemy
from sqlalchemy import text, literal_column, select, literal
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.DEBUG)

URL="monetdb://localhost/test"
print(f'sqlalchemy {sqlalchemy.__version__}')

engine = sqlalchemy.create_engine(URL)

dt = datetime.date(2026, 2, 6)
with engine.connect() as conn:
    conn.execute(text('DROP TABLE IF EXISTS foo'))
    conn.execute(text('CREATE TABLE foo(i DATE)'))
    conn.execute(text('INSERT INTO foo VALUES (:n)'), dict(n='2024-02-06'))

    with Session(engine) as session:
        stmt = select(literal('1974-03-07', sqlalchemy.types.DATE))
        res = conn.execute(stmt)
        print(res)


