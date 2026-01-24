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
# Name:        databases.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     26/07/2017
# -------------------------------------------------------------------------------

import time
import csv
import sqlite3 as sqlite
from .excel import *
from .strings import *
from .filesystem import *


class AbstractDB:
    def __init__(self, dsn):
        """
        Constructor
        """
        # Copy contructor
        if isinstance(dsn, (AbstractDB,)):
            db = dsn
            self.dsn = db.dsn
        else:
            mkdirs(justpath(dsn))
            self.dsn = dsn
        self.conn = None
        self.__connect__()


    def __del__(self):
        self.close()


    def __get_cursor__(self):
        return self.conn.cursor()


    def __connect__(self):
        raise Exception("Not implemented here!")

    def GetTables(self):
        raise Exception("Not implemented here!")

    def GetFieldNames(self, tablename, ctype=""):
        raise Exception("Not implemented here!")

    def GetPrimaryKeys(self, tablename):
        raise Exception("Not implemented here!")

    def GetTablenameFromQuery(sql, env=None):
        env = env if env else {}
        expr = '(?<=select)\s*\(?\s*(?P<database>(\'(.*?)\'))\s*;'
        m = re.search(expr, sformat(sql, env), re.MULTILINE | re.IGNORECASE)
        if m:
            return (m.group("database").strip("'"), "")

        expr = '(?<=from|join|info|into|ists|date)\s*\(?\s*{tablelist}\s*(\?|,|;)?'
        tablename = '(?P<tablename>(\[(.*?)\])|(\w+))'
        tablelist = '(?P<database>(\[(.*?)\])|(\w+))(\.(?P<tablename>(\[(.*?)\])|(\w+)))?'
        expr = sformat(expr, {"tablename": tablename, "tablelist": tablelist})
        m = re.search(expr, sformat(sql, env), re.MULTILINE | re.IGNORECASE)
        if m:
            database = m.group("database")
            tablename = m.group("tablename")
            if not tablename:
                return (main, database.strip("[]"))
        else:
            return (None, None)
        return (database.strip("[]"), tablename.strip("[]"))

    GetTablenameFromQuery = staticmethod(GetTablenameFromQuery)

    def tableExists(self, tablename):
        raise Exception("Not implemented here!")

    def escape(self, text):
        if isinstance(text, (str)):
            return text.decode("utf-8", "ignore")
        elif isinstance(text, (list, tuple)):
            return [self.escape(item) for item in text]
        else:
            return text

    def __prepare_query__(self, sql, env={}, verbose=False):
        """
        prepare the query
        remove comments and blank lines
        """
        comment1 = "--"
        comment2 = "#"
        sql = sql.replace("\r\n", "\n")
        sql = sql.replace("\r", "\n")
        lines = split(sql, "\n", "'\"")

        # follow statement remove comments after SQL line code.
        lines = [split(line, comment2, "'\"")[0] for line in lines]
        lines = [line.strip(" \t") for line in lines]

        # follow statement remove all lines of comments
        lines = [line for line in lines if len(line) > 0 and not line.startswith(comment1)]
        lines = [line for line in lines if len(line) > 0 and not line.startswith(comment2)]

        sql = " ".join(lines)

        env = self.__check_args__(env)

        return sql, env

    def __check_args__(self, env):
        """
        __check_args__
        """
        for key in env:
            if key in ("sql", "__sql__"):
                continue
            value = env[key]
            #I dont remeber why stripping [] but if value ="[name],[value],[etc]" strip causes troubles
            if isstring(value) and value.startswith("[") and value.endswith("]") and not "," in value:
                env[key] = value.strip("[]")
            elif isstring(value) and "'" in value and not "POINT" in value:
                env[key] = value.replace("'", "''")
                # print "pathcing %s=%s..." % (key, env[key])
        return env

    def getCursorFor(self, query):
        """
        Returns a cursor from a query or tablename or cursor
        """
        if isstring(query) and query.strip().upper().startswith("SELECT "):
            # It'a query
            return self.execute(query, outputmode="cursor")
        elif isstring(query):
            # maybe it's a tablename
            return self.execute("""SELECT * FROM [%s];""" % (query), outputmode="cursor")
        else:
            # Probably it's a cursor
            return query

    def fast_execute(self, sql, commit=True, verbose=False):
        """
        Make a single query statement try protected
        Returns a cursor
        """
        cursor = self.__get_cursor__()
        if cursor:
            try:
                t1 = time.time()
                cursor = self.__get_cursor__()
                cursor.execute(sql)
                if commit:
                    self.commit()
                t2 = time.time()

                if verbose:
                    line = sql
                    print("->%s:Done in (%.2f)s" % (line[:], (t2 - t1)))
            except Exception as ex:
                if verbose:
                    line = sql
                    print("->%s...:No![%s]!" % (line[:], ex))
        return cursor


    def safe_execute(self, sql, commit=True, verbose=False):
        """
        Make a single query statement try protected
        Returns a cursor
        """
        retry = True
        cursor = self.__get_cursor__()
        if cursor:
            while retry:
                try:
                    t1 = time.time()
                    ## Try each command
                    cursor.execute(sql)
                    if commit and not startswith(sql.strip(' \r\n'), "select", False):
                        self.commit()
                    t2 = time.time()

                    if verbose:
                        line = sql
                        print("->%s:Done in (%.2f)s" % (line[:], (t2 - t1)))

                    retry = False

                except sqlite.OperationalError as ex:
                    if str(ex) == "database is locked":
                        print("locked sleep")
                        time.sleep(3)
                        print("Trying again")
                        retry = True
                    else:
                        retry = False
                        if verbose:
                            # line = sql.decode('ascii','ignore').replace("\n"," ")
                            line = sql
                            print("->%s...:No![%s]!" % (line[:], ex))
                except Exception as ex:
                    retry = False
                    if verbose:
                        # line = sql.decode('ascii','ignore').replace("\n"," ")
                        line = sql
                        print("Exception:%s...:No![%s]!" % (line[:], ex))
        else:
            if verbose:
                line = sql
                print("Cannot execute the command <%s> because the cursor is None." % line)

        return cursor

    def execute(self, sql, environ={}, outputmode="array", keepdims=True, commit=True, verbose=False):
        """
        Make a query statement list
        Returns a cursor
        """
        cursor = None
        sql, environ = self.__prepare_query__(sql, environ, verbose)

        sql = sformat(sql, environ)
        commands = split(sql, ";", "'\"")
        commands = [command.strip() + ";" for command in commands if len(command) > 0]

        for command in commands:
            cursor = self.safe_execute(command, commit=commit, verbose=verbose)

        if outputmode == "cursor":
            return cursor

        rows = []

        if outputmode == "array":
            for row in cursor:
                rows.append(row)

        elif outputmode == "scalar":
            row = cursor.fetchone()
            if row and len(row):
                return row[0]
            else:
                return None

        elif outputmode == "table":
            metadata = cursor.description
            if metadata:
                rows.append(tuple([item[0] for item in metadata]))
            for row in cursor:
                rows.append(row)

        elif outputmode == "object":
            if cursor.description:
                columns = [item[0] for item in cursor.description]
                for row in cursor:
                    line = {}
                    for j in range(len(row)):
                        line[columns[j]] = row[j]
                    rows.append(line)

        elif outputmode == "columns":
            n = len(cursor.description)
            rows = [[] for j in range(n)]
            for row in cursor:
                for j in range(n):
                    rows[j].append(row[j])

        elif outputmode == "response":
            metadata = []
            res = {}
            if cursor.description:
                metadata = cursor.description
                columns = [item[0] for item in cursor.description]
                for row in cursor:
                    line = {}
                    for j in range(len(row)):
                        line[columns[j]] = row[j]
                    rows.append(line)

                res = {"status": "success", "success": True, "data": rows, "metadata": metadata, "exception": None}
            # else:
            #    res = {"status": "fail", "success": False, "exception": "SqliteDB execute exception" % ex, "sql": sql}
            return res

        if not keepdims:
            # scale down dimensions
            if len(rows) == 0:
                return tuple([None] * len(cursor.description))

            elif len(rows) == 1:
                firstrow = rows[0]
                if len(firstrow) == 1:
                    return firstrow[0]
                return firstrow

        return rows


    def executeScalar(self, sql, environ={}, commit=True, verbose=False):
        """
        Make a query statetment
        Returns a value
        """
        rows = self.execute(sql, environ, keepdims=True, commit=commit, verbose=verbose)
        if len(rows) > 0:
            firstRow = rows[0]
            return firstRow[0] if firstRow else None
        return None


    def executeMany(self, sql, environ={}, values=[], commit=True, verbose=False):
        """
        Make a query statetment
        Returns a cursor
        """
        cursor = self.__get_cursor__()
        line = sformat(sql, environ)
        try:
            t1 = time.time()
            # cursor.executemany(line, self.escape(values))
            cursor.executemany(line, values)
            if commit:
                self.commit()
            t2 = time.time()
            if verbose:
                print("->%s:Done in (%.2f)s" % (line[:], (t2 - t1)))
        except sqlite.Error as ex:
            print("SqlException in <%s> id (%s)" % (line, ex))


    def executemany(self, sql, environ={}, values=[], commit=True, verbose=False):
        """
        executemany -  alias od executeMany
        """
        self.executeMany(sql, environ, values, commit, verbose)

    def select(self, tablename, fieldnames="*", orderby="", limit=-1, outputmode="array", keepdims=True, verbose=False):
        """
        select
        """
        fieldnames = ",".join(wrap(listify(fieldnames, ","), "[", "]")) if fieldnames != "*" else fieldnames
        orderby = ",".join(wrap(listify(orderby, ","), "[", "]"))
        env = {
            "tablename": tablename,
            "fieldnames": fieldnames,
            "where_clause": "",
            "group_by_clause": "",
            "having_clause": "",
            "order_by_clause": "ORDER BY %s" % orderby if orderby else "",
            "limit_clause": "LIMIT %d" % limit if limit > 0 else ""
        }
        sql = """
        SELECT {fieldnames} 
        FROM [{tablename}]
        {where_clause}
        {group_by_clause}
        {having_clause}
        {order_by_clause}
        {limit_clause};
        """
        if outputmode == "table":
            rows = self.execute(sql, env, outputmode="object", keepdims=keepdims, verbose=verbose)
            return {"name": tablename, "data": rows}
        else:
            return self.execute(sql, env, outputmode=outputmode, keepdims=keepdims, verbose=verbose)

    def commit(self):
        """
        Commit
        """
        if self.conn:
            self.conn.commit()

    def close(self, verbose=False):
        """
        Close the db connection
        """
        if self.conn:
            if verbose:
                print("closing db...")
            self.conn.close()

    def drop(self, tablename, verbose=False):
        """
        drop - a list of tables
        """
        sql = ""
        for tablename in trim(listify(tablename, ",")):
            tablename = tablename.strip("[]")
            sql += """DROP TABLE IF EXISTS [{tablename}];"""
        self.execute(sql, {"tablename": tablename}, verbose=verbose)

    def createTable(self, tablename, fieldlist,
                    typelist=None,
                    primarykeys=None,
                    Temp=False,
                    overwrite=False,
                    verbose=False):
        """
        Create a Table from field list
        """
        fieldlist = trim(listify(fieldlist))
        typelist = trim(listify(typelist, ","))
        primarykeys = trim(listify(primarykeys))

        # print(fieldlist,typelist,primarykeys)
        typelist = [""] * len(fieldlist) if not typelist else typelist
        fieldnames = ["[%s] %s" % (fieldname, fieldtype) for (fieldname, fieldtype) in zip(fieldlist, typelist)]
        if primarykeys:
            fieldnames += ["""PRIMARY KEY(%s)""" % (",".join(wrap(primarykeys, "[", "]")))]
        fieldnames = ",".join(fieldnames)

        temp = "TEMP" if Temp else ""
        tablename = tablename.strip("[]")
        env = {"tablename": tablename, "TEMP": temp, "fieldnames": fieldnames}
        sql = """"""
        if overwrite:
            sql += """DROP TABLE IF EXISTS [{tablename}];"""

        sql += """CREATE {TEMP} TABLE IF NOT EXISTS [{tablename}]({fieldnames});"""
        self.execute(sql, env, verbose=verbose)

        return tablename

    def rotateOn(self, srctable, dsttable, fieldlist="", Temp=False, verbose=True):
        """
        Rotate the table from Horizontal to Vertical
        """
        fieldlist = trim(listify(fieldlist))

        primarykeys = fieldlist + ["tablename", "fieldname"]
        self.createTable(dsttable, fieldlist + ["tablename", "fieldname", "value"], primarykeys=primarykeys, Temp=Temp,
                         overwrite=True, verbose=verbose)

        for fieldname in self.GetFieldNames(srctable):
            if fieldname not in fieldlist:
                env = {
                    "srctable": srctable,
                    "dsttable": dsttable,
                    "fieldlist": ",".join(fieldlist),
                    "fieldname": fieldname
                }

                self.execute(
                    """INSERT OR REPLACE INTO [{dsttable}]
                           SELECT {fieldlist},
                            '{srctable}'  AS tablename,
                            '{fieldname}' AS fieldname,
                            [{fieldname}] AS value
                            FROM [{srctable}]
                    """, env, commit=False, verbose=verbose)
            self.commit()

        return dsttable


    def importCsv(self, filename, sep=";", tablename=None, primarykeys="", guess_primary_key=True, Temp=False,
                  append=False,
                  nodata=["", "Na", "NaN", "-", "--", "N/A"], verbose=False):
        raise Exception("Not implemented here!")

    def importXls(self, filename, sheetname=None, tablename=None, primarykeys="", guess_primary_key=True, Temp=False,
                  append=False,
                  nodata=["", "Na", "NaN", "-", "--", "N/A"], verbose=False):
        raise Exception("Not implemented here!")

    def importFrom(self, filename, sheetnames="", sep=";", into_table=None, primarykeys="", guess_primary_key=True,
                   Temp=False, append=True,
                   nodata=["", "Na", "NaN", "--"], verbose=False):
        """
        Export the database or part of it into various formats
        """
        ext = justext(filename).lower()

        if ext in ("csv", "txt"):
            self.importCsv(filename, sep, into_table, primarykeys, False, Temp, append, nodata, verbose)

        elif ext in ("xls", "xlsx"):
            self.importXls(filename, sheetnames, into_table, primarykeys, False, Temp, append, nodata, verbose)

    def ExportTo(self, filename, tables="", sep=";", decimal=".", verbose=False):
        """
        Export the database or part of it into various formats
        """
        ext = justext(filename).lower()

        if ext in ("csv", "txt"):
            self.toCsv(filename, tables, sep, decimal, verbose)

        elif ext in ("xls", "xlsx"):
            self.toExcel(filename, tables, verbose)

    def toCsv(self, filename, tables="", sep=";", decimal=".", verbose=True):
        """
        Generate a csv file from cursor
        """
        ext = justext(filename).lower()
        filecsv = filename
        dbtables = [tablename.lower() for tablename in self.GetTables()]
        tablenames = listify(tables, ';') if tables else dbtables

        for tablename in tablenames:

            if isquery(tablename):
                cursor = self.getCursorFor(tablename)
                _, tablename = self.GetTablenameFromQuery(tablename)
            else:
                if tablename.lower() in dbtables:
                    cursor = self.select(tablename, outputmode="cursor")
                else:
                    continue

            metadata = cursor.description
            columnnames = [item[0] for item in metadata]

            if len(tablenames) > 1:
                filecsv = forceext(filename, "[%s].%s" % (tablename, ext))

            # Finally write on csv!!
            with open(filecsv, 'wb') as stream:
                if verbose:
                    print("writing <%s>..." % filecsv)
                writer = csv.writer(stream, dialect='excel', delimiter=sep, quotechar='"', quoting=csv.QUOTE_MINIMAL)
                line = columnnames
                writer.writerow(line)
                for row in cursor:
                    row = [("%s" % (item if item != None else "")) for item in row]
                    if decimal == ",":
                        row = [item.replace(".", ",") for item in row]
                    writer.writerow(row)

    def toExcel(self, filename, tables="", verbose=False):
        """
        Generate a excel file from sql query
        """
        ext = justext(filename).lower()

        dbtables = self.GetTables()
        tablenames = listify(tables, ';') if tables else dbtables
        if len(tablenames) == 0:
            return False
        # Create or open the workbook
        wb = Workbook(type=ext)

        for tablename in tablenames:
            if verbose:
                print("adding <%s>..." % tablename)

            if isquery(tablename):
                cursor = self.getCursorFor(tablename)
                _, tablename = self.GetTablenameFromQuery(tablename)
            else:
                if tablename.lower() in lower(dbtables):
                    cursor = self.select(tablename, outputmode=cursor)
                else:
                    continue

            # Get an existing sheet or create a new one
            sheet = wb.add_sheet(tablename)
            metadata = cursor.description

            all_columns = [item[0] for item in metadata]
            columnnames = [item for item in all_columns if not item.startswith("style-")]
            columnidxs = [all_columns.index(item) for item in columnnames]

            styles = {}
            for columnname in columnnames:
                if "style-" + columnname in all_columns:
                    styles[columnname] = all_columns.index("style-" + columnname)  # index of column-style related

            # Write the header
            i = 0
            for j in range(len(columnnames)):
                sheet.cell(i, j, columnnames[j])
            i = 1
            # For each row,column  write ...
            for row in cursor:
                j = 0
                for jj in range(len(row)):
                    # eclude style-column
                    if jj in columnidxs:
                        # - get style info
                        columnname = all_columns[jj]
                        if columname in styles:
                            sj = styles[columnname]
                            style = row[sj]
                        else:
                            style = None
                        # ---

                        value = row[jj]
                        if value != None:
                            sheet.cell(i, j, value, style)

                        j += 1
                i += 1

        wb.save(filename)
        return True

if __name__ == "__main__":
    pass
