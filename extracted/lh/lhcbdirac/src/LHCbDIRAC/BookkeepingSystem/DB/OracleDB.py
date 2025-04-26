###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
########################################################################
"""DIRAC Basic Oracle Class It provides access to the basic Oracle methods in a
multithread-safe mode keeping used connections in a python Queue for further
reuse.

These are the coded methods:

__init__( user, passwd, tns, [maxConnsInQueue=10] )

Initializes the Queue and tries to connect to the DB server,
using the _connect method.
"maxConnsInQueue" defines the size of the Queue of open connections
that are kept for reuse. It also defined the maximum number of open
connections available from the object.
maxConnsInQueue = 0 means unlimited and it is not supported.


_except( methodName, exception, errorMessage )

Helper method for exceptions: the "methodName" and the "errorMessage"
are printed with ERROR level, then the "exception" is printed (with
full description if it is a Oracle Exception) and S_ERROR is returned
with the errorMessage and the exception.


_connect()

Attemps connection to DB and sets the _connected flag to True upon success.
Returns S_OK or S_ERROR.


query( cmd, [conn] )

Executes SQL command "cmd".
Gets a connection from the Queue (or open a new one if none is available),
the used connection is  back into the Queue.
If a connection to the the DB is passed as second argument this connection
is used and is not  in the Queue.
Returns S_OK with fetchall() out in Value or S_ERROR upon failure.


_getConnection()

Gets a connection from the Queue (or open a new one if none is available)
Returns S_OK with connection in Value or S_ERROR
the calling method is responsible for closing this connection once it is no
longer needed.
"""
# FIXME: use Connection Pooling
# https://python-oracledb.readthedocs.io/en/latest/user_guide/connection_handling.html#connection-pooling
# FIXME: tnsEntry is named dsn in python-oracledb

import time
import threading
import queue

import oracledb
from oracledb import STRING as oracledb_STRING  # pylint: disable=no-name-in-module
from oracledb import NUMBER as oracledb_NUMBER  # pylint: disable=no-name-in-module

from DIRAC import gLogger
from DIRAC import S_OK, S_ERROR


gInstancesCount = 0
gModeFixed = False

maxConnectRetry = 100
maxArraysize = 5000  # max allowed


class OracleDB:
    """Basic multithreaded DIRAC Oracle Client Class."""

    def __init__(self, userName, password="", tnsEntry="", confDir="", mode="", maxQueueSize=100, **kwargs):
        """set Oracle connection parameters and try to connect."""
        global gInstancesCount
        gInstancesCount += 1

        self.__initialized = False
        self._connected = False

        if "logger" not in dir(self):
            self.logger = gLogger.getSubLogger("Oracle")

        # let the derived class decide what to do with if is not 1
        self._threadsafe = oracledb.threadsafety
        self.logger.debug(f"thread_safe = {self._threadsafe}")

        self.__checkQueueSize(maxQueueSize)

        self.__connect_kwargs = kwargs | dict(
            user=userName,
            password=password,
            dsn=tnsEntry,
            config_dir=confDir,
        )
        self.__mode = mode
        # Create the connection Queue to reuse connections
        self.__connectionQueue = queue.Queue(maxQueueSize)
        # Create the connection Semaphore to limit total number of open connection
        self.__connectionSemaphore = threading.Semaphore(maxQueueSize)

        self.__initialized = True
        self._connect()

        if not self._connected:
            raise RuntimeError("Can not connect, exiting...")

        self.logger.info("===================== Oracle =====================")
        self.logger.info("User:           " + self.__connect_kwargs.get("user"))
        self.logger.info("TNS:            " + self.__connect_kwargs.get("dsn"))
        self.logger.info("==================================================")

    def __del__(self):
        global gInstancesCount

        while 1 and self.__initialized:
            self.__connectionSemaphore.release()
            try:
                connection = self.__connectionQueue.get_nowait()
                connection.close()
            except queue.Empty:
                # self.logger.debug("No more connection in Queue")
                break

    @staticmethod
    def __checkQueueSize(maxQueueSize):
        """the size of the internal queue is limited."""

        if maxQueueSize <= 0:
            raise Exception("OracleDB.__init__: maxQueueSize must positive")
        try:
            test = maxQueueSize - 1
        except TypeError:
            raise TypeError(f"OracleDB.__init__: wrong type for maxQueueSize {type(maxQueueSize)}")

    def _except(self, methodName, x, err):
        """print Oracle error or exeption return S_ERROR with Exception."""

        try:
            raise x
        except oracledb.Error as e:
            self.logger.error(f"{methodName}: {err}", str(e))
            return S_ERROR(f"{err}: ( {e} )")
        except Exception as x:
            self.logger.error(f"{methodName}: {err}", str(x))
            return S_ERROR(f"{err}: ({x})")

    def _connect(self):
        """open connection to Oracle DB and put Connection into Queue set connected
        flag to True and return S_OK return S_ERROR upon failure."""
        self.logger.debug("_connect:", self._connected)
        if self._connected:
            return S_OK()

        self.logger.debug("_connect: Attempting to access DB", f"by user {self.__connect_kwargs.get('user')}.")
        try:
            self.__newConnection()
            self.logger.debug("_connect: Connected.")
            self._connected = True
            return S_OK()
        except Exception as x:
            return self._except("_connect", x, "Could not connect to DB.")

    def query(self, cmd, conn=False, params=[], kwparams={}, pre_inserts=[]):
        """execute Oracle query command return S_OK structure with fetchall result
        as tuple it returns an empty tuple if no matching rows are found return
        S_ERROR upon error.

        Use of params and kwparams to pass bind variabes is strongly encouraged
        to prevent SQL injection and improve performance. See the python-oracledb
        documentation for more information.

        :param str cmd: the SQL string to be executed
        :param conn: the connection to use, optional
        :param list params: positional bind variables to pass to oracledb.Cursor.execute
        :param dict kwparams: named bind variables to pass to oracledb.Cursor.execute
        :param list pre_inserts: list of tuples with the query and data to be inserted before the main query
        """
        self.logger.debug("query:", f"{cmd!r} {params!r} {kwparams!r}")

        retDict = self.__getConnection(conn=conn)
        if not retDict["OK"]:
            return retDict
        connection = retDict["Value"]

        try:
            cursor = connection.cursor()
            cursor.arraysize = maxArraysize

            for pre_insert_query, pre_insert_data in pre_inserts:
                self.logger.debug(
                    "query: Pre-inserting data into temp table", f"{pre_insert_query!r} {pre_insert_data!r}"
                )
                cursor.executemany(pre_insert_query, pre_insert_data)

            if cursor.execute(cmd, *params, **kwparams):
                res = cursor.fetchall()
            else:
                res = ()

            # Log the result limiting it to just 10 records
            if len(res) < 10:
                self.logger.debug("query: Records returned", res)
            else:
                self.logger.debug(
                    "query: First 10 records returned out of",
                    f"{len(res)}: {res[:10]} ...",
                )

            retDict = S_OK(res)
        except Exception as x:
            self.logger.debug("query:", cmd)
            retDict = self._except("query", x, "Execution failed.")
            self.logger.debug("Start Rollback transaction")
            connection.rollback()
            self.logger.debug("End Rollback transaction")

        try:
            connection.commit()
            cursor.close()
        except Exception:
            pass
        if not conn:
            self.__putConnection(connection)

        return retDict

    def executeStoredProcedure(self, packageName, parameters, output=True, array=None, conn=False):
        """executes a stored procedure."""
        self.logger.debug("_query:", packageName + "(" + str(parameters) + ")")

        retDict = self.__getConnection(conn=conn)
        if not retDict["OK"]:
            return retDict
        connection = retDict["Value"]

        try:
            cursor = connection.cursor()
            result = None
            results = None
            if array:
                fArray = array[0]
                if isinstance(fArray, str):
                    result = cursor.arrayvar(oracledb_STRING, array)
                    parameters += [result]
                elif isinstance(fArray, int):
                    result = cursor.arrayvar(oracledb_NUMBER, array)
                    parameters += [result]
                elif isinstance(fArray, list):
                    for i in array:
                        if isinstance(i, (bool, str, int)):
                            parameters += [i]
                        elif i:
                            if isinstance(i[0], str):
                                result = cursor.arrayvar(oracledb_STRING, i)
                                parameters += [result]
                            elif isinstance(i[0], int):
                                result = cursor.arrayvar(oracledb_NUMBER, i)
                                parameters += [result]
                            else:
                                return S_ERROR("The array type is not supported!!!")
                        else:
                            result = cursor.arrayvar(oracledb_STRING, [], 0)
                            parameters += [result]
                else:
                    return S_ERROR("The array type is not supported!!!")
            if output:
                result = connection.cursor()
                result.arraysize = maxArraysize  # 500x faster!!
                parameters += [result]
                cursor.callproc(packageName, parameters)
                results = result.fetchall()
            else:
                cursor.callproc(packageName, parameters)
            retDict = S_OK(results)
        except Exception as x:
            self.logger.debug("query:", packageName + "(" + str(parameters) + ")")
            retDict = self._except("query", x, "Execution failed.")
            connection.rollback()

        try:
            cursor.close()
        except Exception as ex:
            self._except("__getConnection:", ex, "Failed to close a connection")
        if not conn:
            self.__putConnection(connection)

        return retDict

    def executeStoredFunctions(self, packageName, returnType, parameters=None, conn=False):
        """executes a stored function."""
        if parameters is None:
            parameters = []
        retDict = self.__getConnection(conn=conn)
        if not retDict["OK"]:
            return retDict
        connection = retDict["Value"]
        try:
            cursor = connection.cursor()
            cursor.arraysize = maxArraysize
            result = cursor.callfunc(packageName, returnType, parameters)
            retDict = S_OK(result)
        except Exception as x:
            self.logger.debug(f"_query: {packageName} ({parameters})")
            retDict = self._except("_query", x, "Execution failed.")
            connection.rollback()

        try:
            cursor.close()
        except Exception as ex:
            self._except("__getConnection:", ex, "Failed to close a connection")
        if not conn:
            self.__putConnection(connection)
        return retDict

    def __newConnection(self):
        """Create a New connection and put it in the Queue."""
        global gModeFixed
        self.logger.debug("__newConnection:")
        if not gModeFixed:
            gModeFixed = True
            if self.__mode == "":
                try:
                    connection = oracledb.connect(**self.__connect_kwargs)
                except Exception as ex:
                    self.logger.debug(f"Thin mode has failed: {ex}, we will try thick")
                else:
                    self.logger.debug("Using implicit thin mode")
                    self.__putConnection(connection)
                    return
                self.__mode = "Thick"
            if self.__mode == "Thick":
                oracledb.init_oracle_client(config_dir=self.__connect_kwargs.get("config_dir"))
            self.logger.debug(f'Using {"thin" if oracledb.is_thin_mode() else "thick"} mode')
        connection = oracledb.connect(**self.__connect_kwargs)
        self.__putConnection(connection)

    def __putConnection(self, connection):
        """Put a connection in the Queue, if the queue is full, the connection is
        closed."""
        self.logger.debug("__putConnection:")

        # Release the semaphore first, in case something fails
        self.__connectionSemaphore.release()
        try:
            self.__connectionQueue.put_nowait(connection)
        except queue.Full:
            self.logger.debug("__putConnection: Full Queue")
            try:
                connection.close()
            except Exception as x:
                self._except("__putConnection", x, "Failed to put Connection in Queue")
        except Exception as x:
            self._except("__putConnection", x, "Failed to put Connection in Queue")

    def _getConnection(self):
        """Return a new connection to the DB It uses the private method
        __getConnection."""
        self.logger.debug("_getConnection:")

        retDict = self.__getConnection(trial=0)
        self.__connectionSemaphore.release()
        return retDict

    def __getConnection(self, conn=False, trial=0):
        """Return a new connection to the DB, if conn is provided then just return it.

        then try the Queue, if it is empty add a newConnection to the Queue
        and retry it will retry maxConnectRetry to open a new connection and
        will return an error if it fails.
        """
        self.logger.debug("__getConnection:")

        if conn:
            return S_OK(conn)

        try:
            self.__connectionSemaphore.acquire()
            connection = self.__connectionQueue.get_nowait()
            self.logger.debug("__getConnection: Got a connection from Queue")
            if connection:
                try:
                    # This will try to reconnect if the connection has timeout
                    connection.commit()
                except BaseException:
                    # if the ping fails try with a new connection from the Queue
                    self.__connectionSemaphore.release()
                    return self.__getConnection()
                return S_OK(connection)
        except queue.Empty:
            self.__connectionSemaphore.release()
            self.logger.debug("__getConnection: Empty Queue")
            try:
                if trial == min(100, maxConnectRetry):
                    return S_ERROR(f"Could not get a connection after {maxConnectRetry} retries.")
                try:
                    self.__newConnection()
                    return self.__getConnection()
                except Exception as x:
                    self.logger.debug("__getConnection: Fails to get connection from Queue", x)
                    time.sleep(trial * 5.0)
                    newtrial = trial + 1
                    return self.__getConnection(trial=newtrial)
            except Exception as x:
                return self._except("__getConnection:", x, "Failed to get connection from Queue")
        except Exception as x:
            return self._except("__getConnection:", x, "Failed to get connection from Queue")
