#!/usr/bin/env python

import logging

import datetime
import sqlalchemy
from sqlalchemy import MetaData, Table, Column, text, literal_column, select, literal
from sqlalchemy.sql import sqltypes
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.DEBUG)

URL="monetdb://localhost/test"
print(f'sqlalchemy {sqlalchemy.__version__}')

engine = sqlalchemy.create_engine(URL)

with engine.connect() as conn:
    try:
        conn.execute(('DROP TABLE IF EXISTS foo'))

        value = datetime.date(2015, 2, 14)
        value_type = sqltypes.Date
        #value = 42
        #value_type = sqltypes.Integer

        metadata = MetaData()

        table = Table('foo', metadata, Column('x', value_type))

        table.create(conn)
        ins = table.insert().values(x=value)
        print('ins', ins)

        # compiled1 = ins.compile(dialect=engine.dialect)
        # print('compiled1', compiled1)
        # conn.execute(compiled1)

        compiled2 = ins.compile(dialect=engine.dialect, compile_kwargs=dict(literal_binds=True))
        print('compiled2', compiled2)
        conn.execute(compiled2)
    
    finally:
        conn.execute(text('DROP TABLE IF EXISTS foo'))



