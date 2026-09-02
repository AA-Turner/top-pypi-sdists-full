# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2017 Luzzi Valerio 
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        mssqldb.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     01/09/2017
# -------------------------------------------------------------------------------
from .databases import *
from .datatypes import *
from .xml_utils import *
import pyodbc


class mssqlDB(AbstractDB):
    __env__ = {}

    def __init__(self, dsn):
        """
        Constructor
        """
        if isinstance(dsn, dict):
            self.__env__ = dsn
        elif isstring(dsn) and file(dsn):
            self.__env__ = readMSSQL(dsn)
        elif isstring(dsn):
            self.__env__ = readmssqlstring(dsn)
        else:
            raise Exception("Unable to initialize the mssql connection!")

        self.dsn = sformat("""DRIVER={SQL Server};SERVER={server};PORT=1433;DATABASE={database};uid={uid};pwd={pwd}""",
                           self.__env__)
        AbstractDB.__init__(self, self.dsn)

    def __connect__(self):
        """
        Connect to the mysql instance
        """
        try:
            self.conn = pyodbc.connect(self.dsn)

        except pyodbc.Error as err:
            print(err)
            self.close()

    def execute(self, sql, environ={}, return_cursor=False, keepdims=True, commit=True, verbose=False):
        """
        execute
        """
        return AbstractDB.execute(self, sql, environ, return_cursor, keepdims, commit, verbose)

    def executeScalar(self, sql, environ={}, commit=True, verbose=False):
        """
        executeScalar
        """
        return AbstractDB.executeScalar(self, sql, environ, commit, verbose)


def main():
    env = {
        "server": r".\SQLEXPRESS",
        "uid": r"sa",
        "pwd": r"12345",
        "database": "Catasto",
        "tablename": "civici"
    }

    db = mssqlDB(env)

    cursor = db.execute("""SELECT TOP(1) comune FROM  [{database}].[dbo].[{tablename}]""", env, keepdims=True,
                        verbose=True)
    print(cursor)



    # db.close()


if __name__ == "__main__":
    main()
