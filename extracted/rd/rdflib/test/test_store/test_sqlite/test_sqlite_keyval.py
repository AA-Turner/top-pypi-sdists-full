# import sqlite3
# from collections import UserDict

# import pytest


# class SQLiteDict(UserDict):
#     def __init__(self, connection: sqlite3.Connection):
#         self.connection = connection


#     def __getitem__(self, key: str):

#         cursor = self.connection.cursor()
#         cursor.execute("SELECT value FROM keyval WHERE key = ?", (key,))
#         result = cursor.fetchone()
#         if result is None:
#             raise KeyError(key)
#         return result[0]


# @pytest.fixture
# def connection(request: pytest.FixtureRequest):
#     connection = sqlite3.connect(":memory:")
#     request.addfinalizer(lambda: connection.close())
#     return connection


# def test(connection: sqlite3.Connection):
#     sqldict = SQLiteDict(connection)
