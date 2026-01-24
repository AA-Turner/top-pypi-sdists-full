# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import contextlib
import functools
import logging
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from itertools import groupby
from operator import itemgetter

import tango
from tango.databaseds.db_errors import (
    DB_DeviceNotDefined,
    DB_IncorrectArguments,
    DB_IncorrectServerName,
    DB_SQLError,
)
from tango.test_context import parse_ior

th_exc = tango.Except.throw_exception
Executor = ThreadPoolExecutor(1)
cursor_lock = threading.RLock()


def log_me(f):
    @functools.wraps(f)
    def inner(self, *args, **kwargs):
        logging.info(f"Entering '{f.__name__}', args={args}, kwargs={kwargs}")
        try:
            t0 = time.time()
            result = f(self, *args, **kwargs)
            dt = time.time() - t0
            logging.info(
                f"Leaving '{f.__name__}' successfully, took {dt:.3f} s, returned({result})"
            )
            return result
        except tango.DevFailed:
            # This should be a "normal" error, intended for the client
            # No need to log as an error.
            logging.debug(f"Tango exception raised in {f.__name__}")
            raise
        except Exception:
            # This probably indicates a bug?
            logging.exception(f"Error in {f.__name__}")
            raise

    return inner


def get_create_db_statements():
    this_dir = os.path.dirname(__file__)
    statements = []
    with open(os.path.join(this_dir, "create_db_tables.sql")) as f:
        lines = f.readlines()
    # strip comments
    lines = (line for line in lines if not line.startswith("#"))
    lines = (line for line in lines if not line.lower().strip().startswith("key"))
    lines = (line for line in lines if not line.lower().strip().startswith("key"))
    lines = "".join(lines)
    lines = lines.replace("ENGINE=MyISAM", "")
    statements += lines.split(";")

    with open(os.path.join(this_dir, "create_db.sql")) as f:
        lines = f.readlines()
    # strip comments
    lines = (line for line in lines if not line.lower().startswith("#"))
    lines = (line for line in lines if not line.lower().startswith("create database"))
    lines = (line for line in lines if not line.lower().startswith("use"))
    lines = (line for line in lines if not line.lower().startswith("source"))
    lines = "".join(lines)
    statements += lines.split(";")

    return statements


def replace_wildcard(text):
    # escape '%' with '\'
    text = text.replace("%", "\\%")
    # escape '_' with '\'
    text = text.replace("_", "\\_")
    # escape '"' with '\'
    text = text.replace('"', '\\"')
    # escape ''' with '\'
    text = text.replace("'", "\\'")
    # replace '*' with '%'
    text = text.replace("*", "%")
    return text


def use_cursor(f):
    @functools.wraps(f)
    def wrap(self, *args, **kwargs):
        with cursor_lock:
            has_cursor = "cursor" in kwargs
            cursor = kwargs.pop("cursor", None)
            if not has_cursor:
                cursor = Executor.submit(self._get_cursor).result()
            self.cursor = cursor
            try:
                ret = Executor.submit(f, self, *args, **kwargs).result()
                if not has_cursor:
                    Executor.submit(self.cursor.connection.commit).result()
                return ret
            finally:
                if not has_cursor:
                    Executor.submit(self.cursor.close).result()
                    with contextlib.suppress(AttributeError):
                        del self.cursor

    return wrap


def regexp(expr, item):
    """Implement REGEXP function for MySQL compatibility"""
    # TODO may not be 100% compatible, as there are different regexp "flavors"
    if not isinstance(item, str):
        # Not sure when this can happen, but at least NULL (None) does
        return False
    return re.search(expr, item) is not None


class SqlDatabase:
    DB_API_NAME = "sqlite3"  # Default implementation

    def __init__(
        self,
        name,
        db_name=None,
        history_depth=10,
        fire_to_starter=False,  # TODO seems broken on pytango < 10
    ):
        self._db_api = None
        self._db_conn = None
        self.name = name
        self.dev_name = "sys/database/" + name
        if db_name is None:
            self.db_name = os.environ.get("PYTANGO_DATABASE_NAME", "tango_database.db")
        else:
            self.db_name = db_name
        self.history_depth = history_depth
        self.fire_to_starter = fire_to_starter
        self._logger = logging.getLogger(self.__class__.__name__)
        self._debug = self._logger.debug
        self._info = self._logger.info
        self._warn = self._logger.warn
        self._error = self._logger.error
        self._critical = self._logger.critical
        self._initialize()

    def close_db(self):
        if self._db_conn is not None:
            self._db_conn.commit()
            self._db_conn.close()
        self._db_api = None
        self._db_conn = None

    def get_db_api(self):
        if self._db_api is None:
            self._db_api = __import__(self.DB_API_NAME)
        return self._db_api

    @property
    def db_api(self):
        return self.get_db_api()

    @property
    def db_conn(self):
        if self._db_conn is None:
            self._db_conn = self.db_api.connect(self.db_name)
            if logging.root.level == logging.DEBUG:
                self._db_conn.set_trace_callback(lambda q: print(f"  Query: {q}"))
            self._db_conn.row_factory = self.db_api.Row
            # For MySQL compatibility, add REGEXP function
            self._db_conn.create_function("REGEXP", 2, regexp)
        return self._db_conn

    def _get_cursor(self):
        return self.db_conn.cursor()

    def _initialize(self):
        self._info(
            "Initializing database %r (%s)...",
            self.db_name,
            os.path.isfile(self.db_name),
        )
        if not os.path.isfile(self.db_name):
            self._create_db()
        else:
            # trigger connection
            self._trigger_connection()

    @use_cursor
    def _trigger_connection(self):
        return self.db_conn

    @use_cursor
    def _create_db(self):
        self._info("Creating database...")
        statements = get_create_db_statements()
        cursor = self.cursor
        for statement in statements:
            cursor.execute(statement)

    def _get_id(self, name, cursor):
        name += "_history_id"
        _id = cursor.execute(f"SELECT id FROM {name}").fetchone()[0] + 1
        cursor.execute(f"UPDATE {name} SET id={_id}")
        return _id

    def _purge_att_property(self, table, field, obj, attr, name, cursor):
        cursor.execute(
            f"SELECT DISTINCT id FROM {table} WHERE {field} = ? AND name = ? AND "
            + "attribute = ? ORDER BY date",
            (obj, name, attr),
        )
        rows = cursor.fetchall()
        to_del = len(rows) - self.history_depth
        if to_del > 0:
            for row in rows[:to_del]:
                cursor.execute(f"DELETE FROM {table} WHERE id=?", (row[0],))

    def _purge_property(self, table, field, obj, name, cursor):
        cursor.execute(
            f"SELECT DISTINCT id FROM {table} WHERE {field} = ? AND name = ? ORDER BY date",
            (obj, name),
        )
        cursor.execute(
            f"SELECT DISTINCT id FROM {table} WHERE {field} = ? AND name = ? ORDER BY date",
            (obj, name),
        )
        rows = cursor.fetchall()
        to_del = len(rows) - self.history_depth
        if to_del > 0:
            for row in rows[:to_del]:
                cursor.execute(f"DELETE FROM {table} WHERE id=?", (row[0],))

    def _get_device_host(self, name, cursor):
        name = replace_wildcard(name)
        cursor.execute(r"SELECT host FROM device WHERE name LIKE ? ESCAPE '\'", (name,))
        row = cursor.fetchone()
        if row is None:
            raise Exception("No host for device '" + name + "'")
        else:
            return row[0]

    def _send_starter_cmd(self, starter_dev_names):
        for name in starter_dev_names:
            pos = name.find(".")
            if pos != -1:
                name = name[0:pos]
            try:
                dev = tango.DeviceProxy(name)
                dev.UpdateServersInfo()
            except tango.DevFailed:
                pass

    # TANGO API

    def get_stored_procedure_release(self):
        return "release 1.8"

    @log_me
    @use_cursor
    def add_device(self, server_name, dev_info, klass_name, alias=None):
        self._info(
            "delete_attribute_alias(server_name=%s, dev_info=%s, klass_name=%s, alias=%s)",
            server_name,
            dev_info,
            klass_name,
            alias,
        )
        dev_name, (domain, family, member) = dev_info
        cursor = self.cursor
        # first delete the tuple (device,name) from the device table
        cursor.execute("DELETE FROM device WHERE name LIKE ?", (dev_name,))

        # then insert the new value for this tuple
        cursor.execute(
            "INSERT INTO device (name, alias, domain, family, member, exported, "
            "ior, host, server, pid, class, version, started, stopped) "
            'VALUES (?, ?, ?, ?, ?, 0, "nada", "nada", ?, 0, ?, "0", NULL, NULL)',
            (dev_name, alias, domain, family, member, server_name, klass_name),
        )

        # Check if a DServer device entry for the process already exists
        cursor.execute(
            'SELECT name FROM device WHERE server LIKE ? AND class LIKE "DServer"',
            (server_name,),
        )
        if cursor.fetchone() is None:
            dev_name = "dserver/" + server_name
            domain, family, member = dev_name.split("/", 2)
            cursor.execute(
                "INSERT INTO device (name, domain, family, member, exported, ior, "
                "host, server, pid, class, version, started, stopped) "
                'VALUES (?, ?, ?, ?, 0, "nada", "nada", ?, 0, "DServer", "0", NULL, NULL)',
                (dev_name, domain, family, member, server_name),
            )

    @log_me
    @use_cursor
    def delete_attribute_alias(self, alias):
        self._info("delete_attribute_alias(alias=%s)", alias)
        self.cursor.execute("DELETE FROM attribute_alias WHERE alias=?", (alias,))

    @log_me
    @use_cursor
    def delete_class_attribute(self, klass_name, attr_name):
        self.cursor.execute(
            "DELETE FROM property_attribute_class WHERE class LIKE ? AND "
            "attribute LIKE ?",
            (klass_name, attr_name),
        )

    @log_me
    @use_cursor
    def delete_class_attribute_property(self, klass_name, attr_name, prop_name):
        cursor = self.cursor

        # Is there something to delete ?
        cursor.execute(
            "SELECT count(*) FROM property_attribute_class WHERE class = ? "
            "AND attribute = ? AND name = ?",
            (klass_name, attr_name, prop_name),
        )
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if cursor.fetchone()[0] > 0:
            # then delete property from the property_attribute_class table
            cursor.execute(
                "DELETE FROM property_attribute_class WHERE class = ? AND "
                "attribute = ? and name = ?",
                (klass_name, attr_name, prop_name),
            )
            # mark this property as deleted
            hist_id = self._get_id("class_attribute", cursor=cursor)
            cursor.execute(
                "INSERT INTO property_attribute_class_hist (date, class, attribute, "
                "name, id, count, value) VALUES "
                '(?, ?, ?, ?, ?, "0", "DELETED")',
                (now, klass_name, attr_name, prop_name, hist_id),
            )
            self._purge_att_property(
                "property_attribute_class_hist",
                "class",
                klass_name,
                attr_name,
                prop_name,
                cursor=cursor,
            )

    @log_me
    @use_cursor
    def delete_class_property(self, klass_name, prop_name):
        cursor = self.cursor

        prop_name = replace_wildcard(prop_name)
        # Is there something to delete ?
        cursor.execute(
            r"SELECT DISTINCT name FROM property_class WHERE class=? AND name LIKE ? ESCAPE '\'",
            (klass_name, prop_name),
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for row in cursor.fetchall():
            # delete the tuple (device,name,count) from the property table
            name = row[0]
            cursor.execute(
                "DELETE FROM property_class WHERE class=? AND name=?",
                (klass_name, name),
            )
            # Mark this property as deleted
            hist_id = self._get_id("class", cursor=cursor)
            cursor.execute(
                "INSERT INTO property_class_hist (date, class, name, id, count, value)"
                + ' VALUES (?, ?, ?, ?, "0", "DELETED")',
                (now, klass_name, name, hist_id),
            )
            self._purge_property(
                "property_class_hist", "class", klass_name, name, cursor=cursor
            )

    @log_me
    @use_cursor
    def delete_device(self, dev_name):
        self._info("delete_device(dev_name=%s)", dev_name)
        cursor = self.cursor
        dev_name = replace_wildcard(dev_name)

        # delete the device from the device table
        cursor.execute(r"DELETE FROM device WHERE name LIKE ? ESCAPE '\'", (dev_name,))

        # delete device from the property_device table
        cursor.execute(
            r"DELETE FROM property_device WHERE device LIKE ? ESCAPE '\'", (dev_name,)
        )

        # delete device from the property_attribute_device table
        cursor.execute(
            r"DELETE FROM property_attribute_device WHERE device LIKE ? ESCAPE '\'",
            (dev_name,),
        )

    @log_me
    @use_cursor
    def delete_device_alias(self, dev_alias):
        self._info("delete_device_alias(dev_alias=%s)", dev_alias)
        self.cursor.execute("UPDATE device SET alias=NULL WHERE alias=?", (dev_alias,))

    @log_me
    @use_cursor
    def delete_device_attribute(self, dev_name, attr_name):
        dev_name = replace_wildcard(dev_name)
        self.cursor.execute(
            r"DELETE FROM property_attribute_device WHERE device LIKE ? ESCAPE '\'"
            + " AND attribute LIKE ?",
            (dev_name, attr_name),
        )

    @log_me
    @use_cursor
    def delete_device_attribute_property(self, dev_name, attr_name, prop_name):
        cursor = self.cursor
        # Is there something to delete ?
        cursor.execute(
            "SELECT count(*) FROM property_attribute_device WHERE device = ?"
            + " AND attribute = ? AND name = ?",
            (dev_name, attr_name, prop_name),
        )
        if cursor.fetchone()[0] > 0:
            # delete property from the property_attribute_device table
            cursor.execute(
                "DELETE FROM property_attribute_device WHERE device = ?"
                + " AND attribute = ? AND name = ?",
                (dev_name, attr_name, prop_name),
            )
            # Mark this property as deleted
            hist_id = self._get_id("device_attribute", cursor=cursor)
            # TODO I think this is incorrect; we need to insert all the rows
            # of the property here, to keep history intact
            cursor.execute(
                "INSERT INTO property_attribute_device_hist"
                + " (date, device, attribute, name, id, count, value)"
                + ' VALUES (datetime("now", "localtime"), ?, ?, ?, ?, "0", "DELETED")',
                (dev_name, attr_name, prop_name, hist_id),
            )
            self._purge_att_property(
                "property_attribute_device_hist",
                "device",
                dev_name,
                attr_name,
                prop_name,
                cursor=cursor,
            )

    @log_me
    @use_cursor
    def delete_device_property(self, dev_name, prop_name):
        cursor = self.cursor
        prop_name = replace_wildcard(prop_name)

        # Is there something to delete ?
        cursor.execute(
            "SELECT DISTINCT name, count FROM property_device WHERE device=?"
            + r" AND name LIKE ? ESCAPE '\'",
            (dev_name, prop_name),
        )
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for row in cursor.fetchall():
            # delete the tuple (device,name,count) from the property table
            cursor.execute(
                r"DELETE FROM property_device WHERE device=? AND name LIKE ? ESCAPE '\'",
                (dev_name, prop_name),
            )
            # Mark this property as deleted
            hist_id = self._get_id("device", cursor=cursor)
            cursor.execute(
                "INSERT INTO property_device_hist (device, name, id, count, value, date) VALUES (?, ?, ?, ?, ?, ?)",
                (dev_name, row[0], hist_id, str(row[1]), "DELETED", now),
            )
            self._purge_property(
                "property_device_hist", "device", dev_name, row[0], cursor=cursor
            )

    @log_me
    @use_cursor
    def delete_property(self, obj_name, prop_name):
        cursor = self.cursor
        prop_name = replace_wildcard(prop_name)

        # Is there something to delete ?
        cursor.execute(
            r"SELECT DISTINCT name FROM property WHERE object= ? AND name LIKE ? ESCAPE '\'",
            (obj_name, prop_name),
        )
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for row in cursor.fetchall():
            # delete the tuple (object,name,count) from the property table
            cursor.execute(
                r"DELETE FROM property WHERE object=? AND name LIKE ? ESCAPE '\'",
                (obj_name, prop_name),
            )
            # Mark this property as deleted
            hist_id = self._get_id("object", cursor=cursor)
            cursor.execute(
                "INSERT INTO property_hist (object, name, id, count, value, date) "
                'VALUES (?, ?, ?, "0", "DELETED", ?)',
                (obj_name, row[0], hist_id, now),
            )
            self._purge_property(
                "property_hist", "object", obj_name, row[0], cursor=cursor
            )

    @log_me
    @use_cursor
    def delete_server(self, server_instance):
        cursor = self.cursor
        server_instance = replace_wildcard(server_instance)

        previous_host = None
        # get host where running
        if self.fire_to_starter:
            adm_dev_name = "dserver/" + server_instance
            previous_host = self._get_device_host(adm_dev_name, cursor=cursor)

        # then delete the device from the device table
        cursor.execute(
            r"DELETE FROM device WHERE server LIKE ? ESCAPE '\'", (server_instance,)
        )

        # Update host's starter to update controlled servers list
        if self.fire_to_starter and previous_host:
            self._send_starter_cmd(previous_host)
            pass

    @log_me
    @use_cursor
    def delete_server_info(self, server_instance):
        self.cursor.execute("DELETE FROM server WHERE name=?", (server_instance,))

    @log_me
    @use_cursor
    def export_device(self, dev_name, IOR, host, pid, version):
        self._info(
            "export_device(dev_name=%s, host=%s, pid=%s, version=%s)",
            dev_name,
            host,
            pid,
            version,
        )
        self._info("export_device(IOR=%s)", IOR)
        cursor = self.cursor
        do_fire = False
        previous_host = None

        if self.fire_to_starter and dev_name[0:8] == "dserver/":
            # Get database server name
            tango_util = tango.Util.instance()
            db_serv = tango_util.get_ds_name()
            adm_dev_name = "dserver/" + db_serv.lower()
            if dev_name != adm_dev_name and dev_name[0:16] != "dserver/starter/":
                do_fire = True
                previous_host = self._get_device_host(dev_name, cursor=cursor)

        cursor.execute("SELECT server FROM device WHERE name = ?", (dev_name,))
        row = cursor.fetchone()
        if row is None:
            th_exc(
                DB_DeviceNotDefined,
                "device " + dev_name + " not defined in the database !",
                "DataBase::ExportDevice()",
            )
        server = row[0]

        # update the new value for this tuple
        cursor.execute(
            "UPDATE device SET exported=1, ior=?, host=?, pid=?, version=?, "
            'started=datetime("now", "localtime") WHERE name = ?',
            (IOR, host, pid, version, dev_name),
        )

        # update host name in server table
        cursor.execute("UPDATE server SET host=? WHERE name = ?", (host, server))

        if do_fire:
            hosts = []
            hosts.append(host)
            if (
                previous_host != ""
                and previous_host != "nada"
                and previous_host != host
            ):
                hosts.append(previous_host)
            self._send_starter_cmd(hosts)

    @log_me
    @use_cursor
    def export_event(self, event, IOR, host, pid, version):
        cursor = self.cursor
        cursor.execute(
            "INSERT INTO event (name,exported,ior,host,pid,version,started) "
            'VALUES (?, 1, ?, ?, ?, ?, datetime("now", "localtime"))',
            (event, IOR, host, pid, version),
        )

    @log_me
    @use_cursor
    def get_alias_device(self, dev_alias):
        cursor = self.cursor
        cursor.execute(
            r"SELECT name FROM device WHERE alias LIKE ? ESCAPE '\'", (dev_alias,)
        )
        row = cursor.fetchone()
        if row is None:
            th_exc(
                DB_DeviceNotDefined,
                "No device found for alias '" + dev_alias + "'",
                "DataBase::GetAliasDevice()",
            )
        return row[0]

    @log_me
    @use_cursor
    def get_attribute_alias(self, attr_alias):
        cursor = self.cursor
        cursor.execute(
            "SELECT name from attribute_alias WHERE alias LIKE ?", (attr_alias,)
        )
        row = cursor.fetchone()
        if row is None:
            th_exc(
                DB_SQLError,
                "No attribute found for alias '" + attr_alias + "'",
                "DataBase::GetAttributeAlias()",
            )
        return row[0]

    @log_me
    @use_cursor
    def get_attribute_alias_list(self, attr_alias):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT alias FROM attribute_alias WHERE alias LIKE ? ORDER BY attribute",
            (attr_alias,),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_class_attribute_list(self, class_name, wildcard):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT attribute FROM property_attribute_class WHERE class=? and attribute like ?",
            (class_name, wildcard),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_class_attribute_property(self, class_name, attributes):
        cursor = self.cursor
        stmt = "SELECT name,value FROM property_attribute_class WHERE class=? AND attribute LIKE ?"
        result = [class_name, str(len(attributes))]
        for attribute in attributes:
            cursor.execute(stmt, (class_name, attribute))
            rows = cursor.fetchall()
            result.append(attribute)
            result.append(str(len(rows)))
            for row in rows:
                result.append(row[0])
                result.append(row[1])
        return result

    @log_me
    @use_cursor
    def get_class_attribute_property2(self, class_name, attributes):
        cursor = self.cursor
        stmt = "SELECT name,value FROM property_attribute_class WHERE class=? AND attribute LIKE ? ORDER BY name,count"
        # result = [class_name, str(len(attributes))]

        result = [class_name, str(len(attributes))]
        for attribute in attributes:
            cursor.execute(stmt, (class_name, attribute))
            result.append(attribute)
            nb_props = 0
            props = []
            rows = cursor.fetchall()
            for prop, grp in groupby(rows, itemgetter(0)):
                values = [value for _, value in grp]
                nb_props += 1
                props.append(prop)
                props.append(str(len(values)))
                props.extend(values)
            result.append(str(nb_props))
            result.extend(props)

        return result

    @log_me
    @use_cursor
    def get_class_attribute_property_hist(self, class_name, attribute, prop_name):
        stmt = """
        SELECT attribute, name, date, count, value FROM property_attribute_class_hist
        WHERE class = ? AND attribute LIKE ? AND name LIKE ? ORDER BY class, attribute, name, id, date ASC
        """

        result = []
        self.cursor.execute(stmt, (class_name, attribute, prop_name))
        for row in self.cursor.fetchall():
            result.extend(
                [
                    row["attribute"],
                    row["name"],
                    row["date"],
                    str(row["count"]),
                    row["value"],
                ]
            )
        return result

    @log_me
    @use_cursor
    def get_class_for_device(self, dev_name):
        return self._get_class_for_device(dev_name, self.cursor)

    def _get_class_for_device(self, dev_name, cursor):
        cursor.execute("SELECT DISTINCT class FROM device WHERE name = ?", (dev_name,))
        row = cursor.fetchone()
        if row is None:
            th_exc(
                DB_IncorrectArguments,
                "Class not found for " + dev_name,
                "Database.GetClassForDevice",
            )
        return row["class"]

    @log_me
    @use_cursor
    def get_class_inheritance_for_device(self, dev_name):
        cursor = self.cursor
        class_name = self._get_class_for_device(dev_name, cursor=cursor)
        props = self._get_class_property(class_name, ["InheritedFrom"], cursor=cursor)
        return [class_name] + props[4:]

    @log_me
    @use_cursor
    def get_class_list(self, server):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT class FROM device WHERE class LIKE ? ORDER BY class",
            (server,),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_class_property(self, class_name, properties):
        return self._get_class_property(class_name, properties, self.cursor)

    def _get_class_property(self, class_name, properties, cursor):
        stmt = r"SELECT count, value, name FROM property_class WHERE class=? AND name LIKE ? ESCAPE '\' ORDER BY count"
        result = []
        result.append(class_name)
        result.append(str(len(properties)))
        for prop_name in properties:
            tmp_name = replace_wildcard(prop_name)
            cursor.execute(stmt, (class_name, tmp_name))
            rows = list(cursor.fetchall())
            result.append(prop_name)
            result.append(str(len(rows)))
            for row in rows:
                result.append(row[1])
        return result

    @log_me
    @use_cursor
    def get_class_property_hist(self, class_name, prop_name):
        cursor = self.cursor
        stmt = "SELECT DISTINCT id FROM property_class_hist WHERE class=? AND name LIKE ? ORDER by date ASC"

        result = []

        cursor.execute(stmt, (class_name, prop_name))

        for row in cursor.fetchall():
            idr = row[0]

            stmt = "SELECT strftime('%Y-%m-%d %H:%M:%S', date), name, value FROM property_class_hist WHERE id =? AND class =?"

            cursor.execute(stmt, (idr, class_name))

            rows = list(cursor.fetchall())
            date, name, _ = rows[0]
            result.append(name)
            result.append(date)
            result.append(str(len(rows)))
            for _, _, value in rows:
                result.append(value)

        return result

    @log_me
    @use_cursor
    def get_class_property_list(self, class_name):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT name FROM property_class WHERE class LIKE ? order by NAME",
            (class_name,),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_device_alias(self, dev_name):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT alias FROM device WHERE name LIKE ?", (dev_name,)
        )
        try:
            (alias,) = cursor.fetchone()
        except (IndexError, TypeError):
            th_exc(
                DB_DeviceNotDefined,
                "No device called '" + dev_name + "'",
                "DataBase::GetDeviceAlias()",
            )
        return alias

    @log_me
    @use_cursor
    def get_device_alias_list(self, alias):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT alias FROM device WHERE alias LIKE ? ORDER BY alias",
            (alias,),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_device_attribute_list(self, dev_name, attribute):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT  attribute FROM property_attribute_device WHERE device=?  AND attribute LIKE ? ORDER BY attribute",
            (
                dev_name,
                attribute,
            ),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_device_attribute_property(self, dev_name, attributes):
        cursor = self.cursor
        stmt = "SELECT name,value FROM property_attribute_device WHERE device=? AND attribute LIKE ?"
        result = [dev_name, str(len(attributes))]
        for attribute in attributes:
            cursor.execute(stmt, (dev_name, attribute))
            rows = cursor.fetchall()
            result.append(attribute)
            result.append(str(len(rows)))
            for row in rows:
                result.append(row[0])
                result.append(row[1])
        return result

    @log_me
    @use_cursor
    def get_device_attribute_property2(self, dev_name, attributes):
        cursor = self.cursor
        stmt = "SELECT name,value FROM property_attribute_device WHERE device=? AND attribute LIKE ? ORDER BY name,count"
        result = [dev_name, str(len(attributes))]

        for attribute in attributes:
            cursor.execute(stmt, (dev_name, attribute))
            result.append(attribute)
            nb_props = 0
            props = []
            rows = cursor.fetchall()
            for prop, grp in groupby(rows, itemgetter(0)):
                values = [value for _, value in grp]
                nb_props += 1
                props.append(prop)
                props.append(str(len(values)))
                props.extend(values)
            result.append(str(nb_props))
            result.extend(props)
        return result

    @log_me
    @use_cursor
    def get_device_attribute_property_hist(self, dev_name, attribute, prop_name):
        cursor = self.cursor
        stmt = "SELECT  DISTINCT id FROM property_attribute_device_hist WHERE device=? AND attribute LIKE ? AND name LIKE ? ORDER by date ASC"

        result = []

        cursor.execute(stmt, (dev_name, attribute, prop_name))

        for row in cursor.fetchall():
            idr = row[0]

            stmt = "SELECT attribute,name,strftime('%Y-%m-%d %H:%M:%S', date),value FROM property_attribute_device_hist WHERE id =? AND device =? ORDER BY count ASC"

            cursor.execute(stmt, (idr, dev_name))
            rows = cursor.fetchall()

            attribute, name, date = rows[0][:3]
            count = len(rows)
            result.extend([attribute, name, date, str(count)])
            for *_, value in rows:
                result.append(value)

        return result

    @log_me
    @use_cursor
    def get_device_class_list(self, server_name):
        cursor = self.cursor
        result = []
        cursor.execute(
            "SELECT name,class FROM device WHERE server =?  ORDER BY name",
            (server_name,),
        )
        for row in cursor.fetchall():
            result.append(row[0])
            result.append(row[1])

        return result

    @log_me
    @use_cursor
    def get_device_domain_list(self, wildcard):
        cursor = self.cursor
        cursor.execute(
            r"SELECT DISTINCT domain FROM device WHERE name LIKE ? ESCAPE '\' ORDER BY domain",
            (wildcard,),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_device_exported_list(self, wildcard):
        cursor = self.cursor
        cursor.execute(
            r"SELECT DISTINCT name FROM device WHERE (name LIKE ? ESCAPE '\' OR alias LIKE ?  ESCAPE '\') AND exported=1 ORDER BY name",
            (wildcard, wildcard),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_device_family_list(self, wildcard):
        cursor = self.cursor
        cursor.execute(
            r"SELECT DISTINCT family FROM device WHERE name LIKE ? ESCAPE '\' ORDER BY family",
            (wildcard,),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_device_info(self, dev_name):
        cursor = self.cursor
        cursor.execute(
            "SELECT exported,ior,version,pid,server,host,started,stopped,class FROM device WHERE name =?  or alias =?",
            (dev_name, dev_name),
        )
        result_long = []
        result_str = []
        for row in cursor.fetchall():
            if (row[4] is None) or (row[5] is None):
                th_exc(
                    DB_SQLError,
                    "Wrong info in database for device '" + dev_name + "'",
                    "DataBase::GetDeviceInfo()",
                )
            result_str.append(dev_name.lower())  # Lowercase for compatibility
            if row[1] is not None:
                result_str.append(str(row[1]))
            else:
                result_str.append("")
            result_str.append(str(row[2]))
            result_str.append(str(row[4]))
            result_str.append(str(row[5]))

            for i in range(0, 2):
                cursor.execute(
                    "SELECT strftime('%d-%m-%Y at %H:%M:%S', ?)", (row[6 + i],)
                )
                tmp_date = cursor.fetchone()[0]
                if tmp_date is None:
                    result_str.append("?")
                else:
                    result_str.append(str(tmp_date))
            result_str.append(str(row[8]))

            # TODO correct?
            # Exported
            try:
                result_long.append(None if row[0] == "nada" else int(row[0]))
            except ValueError:
                result_long.append(0)
            #
            try:
                result_long.append(int(row[3]))
            except ValueError:
                result_long.append(0)

        if not result_long:
            e0 = tango.DevError()
            e0.desc = f"device {dev_name} not defined in the database !"
            e0.origin = "DataBase::GetDeviceInfo()"
            e0.reason = "DB_DeviceNotDefined"
            e0.severity = tango.ErrSeverity.ERR
            raise tango.DevFailed(e0)

        result = (result_long, result_str)
        return result

    @log_me
    @use_cursor
    def get_device_list(self, server_name, class_name):
        cursor = self.cursor
        cursor.execute(
            r"SELECT DISTINCT name FROM device WHERE server LIKE ? ESCAPE '\' AND class LIKE ? ESCAPE '\' ORDER BY name",
            (server_name, class_name),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_device_wide_list(self, wildcard):
        cursor = self.cursor
        cursor.execute(
            r"SELECT DISTINCT name FROM device WHERE name LIKE ? ESCAPE '\' ORDER BY name",
            (wildcard,),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_device_member_list(self, wildcard):
        cursor = self.cursor
        cursor.execute(
            r"SELECT DISTINCT  member FROM device WHERE name LIKE ? ESCAPE '\' ORDER BY member",
            (wildcard,),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_device_property(self, dev_name, properties):
        cursor = self.cursor
        stmt = r"SELECT count,value,name FROM property_device WHERE device = ? AND name LIKE ? ESCAPE '\' ORDER BY count"
        result = []
        result.append(dev_name)
        result.append(str(len(properties)))
        for prop in properties:
            result.append(prop)
            tmp_name = replace_wildcard(prop)
            cursor.execute(stmt, (dev_name, tmp_name))
            rows = cursor.fetchall()
            result.append(str(len(rows)))
            for row in rows:
                result.append(row[1])
            if not rows:
                # TODO No idea what's the point of this but seems it's expected
                result.append(" ")
        return result

    @log_me
    @use_cursor
    def get_device_property_list(self, device_name, prop_filter):
        cursor = self.cursor
        cursor.execute(
            r"SELECT DISTINCT name FROM property_device WHERE device LIKE ? AND name LIKE ? ESCAPE '\' order by NAME",
            (device_name, prop_filter),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_device_property_hist(self, device_name, prop_name):
        cursor = self.cursor
        stmt1 = r"""
        SELECT DISTINCT id FROM property_device_hist
        WHERE device=? AND name LIKE ?  ESCAPE '\'
        ORDER by date ASC
        """
        result = []

        tmp_name = replace_wildcard(prop_name)

        stmt2 = r"""
        SELECT name, strftime('%Y-%m-%d %H:%M:%S', date), value
        FROM property_device_hist
        WHERE id = ? AND device = ? AND name LIKE ? ESCAPE '\'
        ORDER BY count ASC
        """

        cursor.execute(stmt1, (device_name, tmp_name))
        for (idr,) in cursor.fetchall():
            cursor.execute(stmt2, (idr, device_name, tmp_name))
            rows = list(cursor.fetchall())
            name, date, value = rows[0]
            result.extend([name, date, str(len(rows)), value])
            for row2 in rows[1:]:
                result.append(row2[2])
        return result

    @log_me
    @use_cursor
    def get_device_server_class_list(self, server_name):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT class FROM device WHERE server LIKE ? ORDER BY class",
            (server_name,),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_exported_device_list_for_class(self, class_name):
        cursor = self.cursor
        cursor.execute(
            "SELECT  DISTINCT name FROM device WHERE class LIKE ? AND exported=1 ORDER BY name",
            (class_name,),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_host_list(self, host_name):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT host FROM device WHERE host LIKE ?  ORDER BY host",
            (host_name,),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_host_server_list(self, host_name):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT server FROM device WHERE host LIKE ?  ORDER BY server",
            (host_name,),
        )
        return [row[0] for row in cursor.fetchall()]

    def get_host_servers_info(self, host_name):
        servers = self.get_host_server_list(host_name)
        result = []
        for server in servers:
            result.append(server)
            info = self.get_server_info(server)
            result.append(info[2])
            result.append(info[3])
        return result

    def get_instance_name_list(self, server_name):
        server_name = server_name + "/%"
        server_list = self.get_server_list(server_name)
        result = []
        for server in server_list:
            names = server.split("/")
            result.append(names[1])
        return result

    @log_me
    @use_cursor
    def get_object_list(self, name):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT object FROM property WHERE object LIKE ?  ORDER BY object",
            (name,),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_property(self, object_name, properties):
        cursor = self.cursor
        result = []
        result.append(object_name)
        result.append(str(len(properties)))
        stmt = r"SELECT count,value,name FROM property WHERE object LIKE ?  AND name LIKE ? ESCAPE '\' ORDER BY count"
        for prop_name in properties:
            result.append(prop_name)
            prop_name = replace_wildcard(prop_name)
            cursor.execute(stmt, (object_name, prop_name))
            rows = cursor.fetchall()
            n_rows = len(rows)
            result.append(str(n_rows))
            if n_rows:
                for row in rows:
                    result.append(row[1])
            else:
                result.append(" ")
        return result

    @log_me
    @use_cursor
    def get_property_hist(self, object_name, prop_name):
        cursor = self.cursor
        result = []

        stmt = r"""
        SELECT  DISTINCT id FROM property_hist
        WHERE object=? AND name LIKE ? ESCAPE '\'
        ORDER by date ASC
        """
        prop_name = replace_wildcard(prop_name)
        cursor.execute(stmt, (object_name, prop_name))
        rows = cursor.fetchall()

        stmt2 = r"""
        SELECT name, strftime('%Y-%m-%d %H:%M:%S', date), value, count
        FROM property_hist
        WHERE id =? AND object = ? AND name LIKE ? ESCAPE '\'
        ORDER BY count ASC
        """
        for row in rows:
            idr = row[0]
            cursor.execute(stmt2, (idr, object_name, prop_name))
            rows2 = cursor.fetchall()
            name, date, value, count = rows2[0]
            result.extend([name, date, str(len(rows2)), value])
            for _, _, value, _ in rows2[1:]:
                result.append(value)
        return result

    @log_me
    @use_cursor
    def get_property_list(self, object_name, wildcard):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT name FROM property WHERE object LIKE ? AND name LIKE ? ORDER BY name",
            (object_name, wildcard),
        )
        return [row[0] for row in cursor.fetchall()]

    @log_me
    @use_cursor
    def get_server_info(self, server_name):
        cursor = self.cursor
        cursor.execute(
            "SELECT host, mode, level FROM server WHERE name = ?", (server_name,)
        )
        result = []
        result.append(server_name)
        row = cursor.fetchone()
        if row is None:
            # TODO would it not make more sense to throw an error if no server was found,
            # instead of returning made up data?
            result.append(" ")
            result.append(" ")
            result.append(" ")
        else:
            result.append(row[0])
            result.append(str(row[1]))
            result.append(str(row[2]))

        return result

    @log_me
    @use_cursor
    def _get_server_list(self, wildcard):
        cursor = self.cursor
        cursor.execute(
            "SELECT DISTINCT server FROM device WHERE server LIKE ? ORDER BY server",
            (wildcard,),
        )
        return [row[0] for row in cursor.fetchall()]

    def get_server_list(self, wildcard):
        result = []
        server_list = self._get_server_list(wildcard)
        return server_list
        for server in server_list:
            found = 0
            server_name = server.split("/")[0]
            for res in result:
                if server_name.lower() == res.lower():
                    found = 1
            if not found:
                result.append(server_name)
        return result

    def get_server_name_list(self, wildcard):
        result = []
        server_list = self._get_server_list(wildcard)
        for server in server_list:
            found = 0
            server_name = server.split("/")[0]
            for res in result:
                if server_name.lower() == res.lower():
                    found = 1
            if not found:
                result.append(server_name)
        return result

    @log_me
    @use_cursor
    def import_device(self, dev_name):
        cursor = self.cursor
        result_long = []
        result_str = []
        # Search first by server name and if nothing found by alias
        # Using OR takes much more time
        cursor.execute(
            "SELECT exported,ior,version,pid,server,host,class FROM device WHERE name =? COLLATE NOCASE",
            (dev_name,),
        )
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute(
                "SELECT exported,ior,version,pid,server,host,class FROM device WHERE alias =? COLLATE NOCASE",
                (dev_name,),
            )
            rows = cursor.fetchall()
            if len(rows) == 0:
                th_exc(
                    DB_DeviceNotDefined,
                    "device " + dev_name + " not defined in the database !",
                    "DataBase::ImportDevice()",
                )
        for row in rows:
            result_str.append(dev_name)
            result_str.append(row[1])
            result_str.append(row[2] if row[2] != "nada" else "0")
            result_str.append(row[4])
            result_str.append(row[5])
            result_str.append(row[6])

            if row[0] != "nada":
                result_long.append(row[0])
            else:
                result_long.append(0)
            if row[3] != "nada":
                result_long.append(row[3])
            else:
                result_long.append(0)

        result = (result_long, result_str)
        return result

    @log_me
    @use_cursor
    def import_event(self, event_name):
        cursor = self.cursor
        result_long = []
        result_str = []
        cursor.execute(
            "SELECT exported,ior,version,pid,host FROM event WHERE name =?",
            (event_name,),
        )
        rows = cursor.fetchall()
        if len(rows) == 0:
            th_exc(
                DB_DeviceNotDefined,
                "event " + event_name + " not defined in the database !",
                "DataBase::ImportEvent()",
            )
        for row in rows:
            result_str.append(event_name)
            result_str.append(row[1])
            result_str.append(row[2])
            result_str.append(row[4])
            exported = -1
            if row[0] is not None and row[0] != "nada":
                exported = row[0]
            result_long.append(exported)
            pid = 0
            if row[3] is not None and row[2] != "nada":
                pid = row[3]
            result_long.append(pid)
        result = (result_long, result_str)
        return result

    @log_me
    @use_cursor
    def info(self):
        cursor = self.cursor
        result = []
        # db name
        info_str = "TANGO Database " + self.db_name
        result.append(info_str)
        # new line
        result.append(" ")
        # get start time of database
        cursor.execute("SELECT started FROM device WHERE name =?", (self.dev_name,))
        row = cursor.fetchone()
        info_str = "Running since ..." + str(row[0])
        result.append(info_str)
        # new line
        result.append(" ")
        # get number of devices defined
        cursor.execute("SELECT COUNT(*) FROM device")
        row = cursor.fetchone()
        info_str = "Devices defined = " + str(row[0])
        result.append(info_str)
        # get number of devices exported
        cursor.execute("SELECT COUNT(*) FROM device WHERE exported = 1")
        row = cursor.fetchone()
        info_str = "Devices exported = " + str(row[0])
        result.append(info_str)
        # get number of device servers defined
        cursor.execute('SELECT COUNT(*) FROM device WHERE class = "DServer" ')
        row = cursor.fetchone()
        info_str = "Device servers defined = " + str(row[0])
        result.append(info_str)
        # get number of device servers exported
        cursor.execute(
            'SELECT COUNT(*) FROM device WHERE class = "DServer"  AND exported = 1'
        )
        row = cursor.fetchone()
        info_str = "Device servers exported = " + str(row[0])
        result.append(info_str)
        # new line
        result.append(" ")
        # get number of device properties
        cursor.execute("SELECT COUNT(*) FROM property_device")
        row = cursor.fetchone()
        info_str = "Device properties defined = " + str(row[0])
        cursor.execute("SELECT COUNT(*) FROM property_device_hist")
        row = cursor.fetchone()
        info_str = info_str + " [History lgth = " + str(row[0]) + "]"
        result.append(info_str)
        # get number of class properties
        cursor.execute("SELECT COUNT(*) FROM property_class")
        row = cursor.fetchone()
        info_str = "Class properties defined = " + str(row[0])
        cursor.execute("SELECT COUNT(*) FROM property_class_hist")
        row = cursor.fetchone()
        info_str = info_str + " [History lgth = " + str(row[0]) + "]"
        result.append(info_str)
        # get number of device attribute properties
        cursor.execute("SELECT COUNT(*) FROM property_attribute_device")
        row = cursor.fetchone()
        info_str = "Device attribute properties defined = " + str(row[0])
        cursor.execute("SELECT COUNT(*) FROM property_attribute_device_hist")
        row = cursor.fetchone()
        info_str = info_str + " [History lgth = " + str(row[0]) + "]"
        result.append(info_str)
        # get number of class attribute properties
        cursor.execute("SELECT COUNT(*) FROM property_attribute_class")
        row = cursor.fetchone()
        info_str = "Class attribute properties defined = " + str(row[0])
        cursor.execute("SELECT COUNT(*) FROM property_attribute_class_hist")
        row = cursor.fetchone()
        info_str = info_str + " [History lgth = " + str(row[0]) + "]"
        result.append(info_str)
        # get number of object properties
        cursor.execute("SELECT COUNT(*) FROM property")
        row = cursor.fetchone()
        info_str = "Object properties defined = " + str(row[0])
        cursor.execute("SELECT COUNT(*) FROM property_hist")
        row = cursor.fetchone()
        info_str = info_str + " [History lgth = " + str(row[0]) + "]"
        result.append(info_str)

        return result

    @log_me
    @use_cursor
    def put_attribute_alias(self, attribute_name, attribute_alias):
        cursor = self.cursor
        attribute_name = attribute_name.lower()
        # first check if this alias exists
        cursor.execute(
            "SELECT alias from attribute_alias WHERE alias=? AND name <> ? ",
            (attribute_alias, attribute_name),
        )
        rows = cursor.fetchall()
        if len(rows) > 0:
            self._warn("DataBase::DbPutAttributeAlias(): this alias exists already ")
            th_exc(
                DB_SQLError,
                "alias " + attribute_alias + " already exists !",
                "DataBase::DbPutAttributeAlias()",
            )
        tmp_names = attribute_name.split("/")
        if len(tmp_names) != 4:
            self._warn(
                "DataBase::DbPutAttributeAlias(): attribute name has bad syntax, must have 3 / in it"
            )
            th_exc(
                DB_SQLError,
                "attribute name "
                + attribute_name
                + " has bad syntax, must have 3 / in it",
                "DataBase::DbPutAttributeAlias()",
            )
        # first delete the current entry (if any)
        cursor.execute("DELETE FROM attribute_alias WHERE name=?", (attribute_name,))
        # update the new value for this tuple
        tmp_device = tmp_names[0] + "/" + tmp_names[1] + "/" + tmp_names[2]
        tmp_attribute = tmp_names[3]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO attribute_alias (alias, name, device, attribute, updated, accessed) VALUES(?, ?, ?, ?, ?, ?)",
            (attribute_alias, attribute_name, tmp_device, tmp_attribute, now, now),
        )

    @log_me
    @use_cursor
    def put_class_attribute_property(self, class_name, nb_attributes, attr_prop_list):
        cursor = self.cursor
        k = 0
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for _i in range(0, nb_attributes):
            tmp_attribute = attr_prop_list[k]
            nb_properties = int(attr_prop_list[k + 1])
            for j in range(k + 2, k + nb_properties * 2 + 2, 2):
                tmp_name = attr_prop_list[j]
                tmp_value = attr_prop_list[j + 1]
                # first delete the tuple (device,name,count) from the property table
                cursor.execute(
                    "DELETE FROM property_attribute_class WHERE class LIKE ? AND attribute LIKE ? AND name LIKE ?",
                    (class_name, tmp_attribute, tmp_name),
                )
                # then insert the new value for this tuple
                cursor.execute(
                    "INSERT INTO property_attribute_class (class, attribute, name, count, value, updated, accessed) VALUES (?, ?, ?, '1', ?, ?, ?)",
                    (class_name, tmp_attribute, tmp_name, tmp_value, now, now),
                )
                # then insert the new value into the history table
                hist_id = self._get_id("class_attribute", cursor=cursor)
                cursor.execute(
                    "INSERT INTO property_attribute_class_hist (class, attribute, name, id, count, value, date) VALUES (?, ?, ?, ?, '1', ?, ?)",
                    (class_name, tmp_attribute, tmp_name, hist_id, tmp_value, now),
                )

                self._purge_att_property(
                    "property_attribute_class_hist",
                    "class",
                    class_name,
                    tmp_attribute,
                    tmp_name,
                    cursor=cursor,
                )
            k = k + nb_properties * 2 + 2

    @log_me
    @use_cursor
    def put_class_attribute_property2(self, class_name, nb_attributes, attr_prop_list):
        cursor = self.cursor
        k = 0
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for _i in range(0, nb_attributes):
            tmp_attribute = attr_prop_list[k]
            nb_properties = int(attr_prop_list[k + 1])
            for _jj in range(0, nb_properties, 1):
                j = k + 2
                tmp_name = attr_prop_list[j]
                # first delete the tuple (device,name,count) from the property table
                cursor.execute(
                    "DELETE FROM property_attribute_class WHERE class LIKE ? AND attribute LIKE ? AND name LIKE ?",
                    (class_name, tmp_attribute, tmp_name),
                )
                n_rows = int(attr_prop_list[j + 1])
                tmp_count = 0
                for _l in range(j + 1, j + n_rows + 1, 1):
                    tmp_value = attr_prop_list[_l + 1]
                    tmp_count = tmp_count + 1
                    # then insert the new value for this tuple
                    cursor.execute(
                        "INSERT INTO property_attribute_class (class, attribute, name, count, value, updated, accessed) VALUES (? ,?,?,?,?,?,?)",
                        (
                            class_name,
                            tmp_attribute,
                            tmp_name,
                            str(tmp_count),
                            tmp_value,
                            now,
                            now,
                        ),
                    )
                    # then insert the new value into the history table
                    hist_id = self._get_id("class_attribute", cursor=cursor)
                    cursor.execute(
                        "INSERT INTO property_attribute_class_hist (date, class, attribute, name, id, count, value) VALUES (?,?,?,?,?,?,?)",
                        (
                            now,
                            class_name,
                            tmp_attribute,
                            tmp_name,
                            hist_id,
                            str(tmp_count),
                            tmp_value,
                        ),
                    )

                    self._purge_att_property(
                        "property_attribute_class_hist",
                        "class",
                        class_name,
                        tmp_attribute,
                        tmp_name,
                        cursor=cursor,
                    )
                k = k + n_rows + 2
            k = k + 2

    @log_me
    @use_cursor
    def put_class_property(self, class_name, nb_properties, prop_list):
        cursor = self.cursor
        hist_id = self._get_id(
            "device", cursor=cursor
        )  # Single id for the whole operation
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        property_values = []
        lines = iter(prop_list)
        while len(property_values) < nb_properties:
            name = next(lines)
            number_of_lines = int(next(lines))
            value = [next(lines) for i in range(number_of_lines)]
            property_values.append((name, value))
            # Delete current property
            cursor.execute(
                "DELETE FROM property_class WHERE class LIKE ? AND name LIKE ?",
                (class_name, name),
            )
            # Insert into property table
            cursor.executemany(
                "INSERT INTO property_class (class, name, count, value, updated, accessed) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (class_name, name, str(i), line, now, now)
                    for i, line in enumerate(value, start=1)
                ],
            )
            # Insert into property history table
            cursor.executemany(
                "INSERT INTO property_class_hist (class, name, id, count, value, date) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (class_name, name, hist_id, str(i), line, now)
                    for i, line in enumerate(value, start=1)
                ],
            )
            # Make sure history is limited
            self._purge_property(
                "property_class_hist", "class", class_name, name, cursor=cursor
            )

    @log_me
    @use_cursor
    def put_device_alias(self, device_name, device_alias):
        cursor = self.cursor
        device_name = device_name.lower()
        # first check if this alias exists
        cursor.execute(
            "SELECT alias from device WHERE alias=? AND name <>?",
            (device_alias, device_name),
        )
        rows = cursor.fetchall()
        if len(rows) > 0:
            self._warn("DataBase::DbPutDeviceAlias(): this alias exists already ")
            th_exc(
                DB_SQLError,
                "alias " + device_alias + " already exists !",
                "DataBase::DbPutDeviceAlias()",
            )
        # update the new value for this tuple
        cursor.execute(
            "UPDATE device SET alias=? ,started=datetime('now', 'localtime') where name LIKE ?",
            (device_alias, device_name),
        )

    @log_me
    @use_cursor
    def put_device_attribute_property(self, device_name, nb_attributes, attr_prop_list):
        # TODO implement this using put_device_attribute_property2?
        cursor = self.cursor
        k = 0
        for _i in range(0, nb_attributes):
            tmp_attribute = attr_prop_list[k]
            nb_properties = int(attr_prop_list[k + 1])
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for j in range(k + 2, k + nb_properties * 2 + 2, 2):
                tmp_name = attr_prop_list[j]
                tmp_value = attr_prop_list[j + 1]
                # first delete the tuple (device,name,count) from the property table
                cursor.execute(
                    "DELETE FROM property_attribute_device WHERE device LIKE ? AND attribute LIKE ? AND name LIKE ?",
                    (device_name, tmp_attribute, tmp_name),
                )
                # then insert the new value for this tuple
                cursor.execute(
                    "INSERT INTO property_attribute_device (device, attribute, name, count, value, updated, accessed) VALUES (?, ?, ?, '1', ?, ?, ?)",
                    (device_name, tmp_attribute, tmp_name, tmp_value, now, now),
                )
                # then insert the new value into the history table
                hist_id = self._get_id("device_attribute", cursor=cursor)
                cursor.execute(
                    "INSERT INTO property_attribute_device_hist (date,device,attribute,name,id,count,value) VALUES (?,?,?,?,?,'1',?)",
                    (now, device_name, tmp_attribute, tmp_name, hist_id, tmp_value),
                )

                self._purge_att_property(
                    "property_attribute_device_hist",
                    "device",
                    device_name,
                    tmp_attribute,
                    tmp_name,
                    cursor=cursor,
                )
            k = k + nb_properties * 2 + 2

    @log_me
    @use_cursor
    def put_device_attribute_property2(
        self, device_name, nb_attributes, attr_prop_list
    ):
        cursor = self.cursor

        # Group the data
        attr_prop = {}
        items = iter(attr_prop_list)
        while len(attr_prop) < nb_attributes:
            attrname = next(items)
            attr = attr_prop[attrname] = {}
            n_props = int(next(items))
            for _i in range(n_props):
                propname = next(items)
                prop = attr[propname] = []
                n_lines = int(next(items))
                for _j in range(n_lines):
                    line = next(items)
                    prop.append(line)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hist_id = self._get_id("device_attribute", cursor=cursor)

        for attr_name, props in attr_prop.items():
            for prop_name, lines in props.items():
                cursor.execute(
                    "DELETE FROM property_attribute_device WHERE device LIKE ? AND attribute LIKE ? AND name LIKE ?",
                    (device_name, attr_name, prop_name),
                )
                for count, value in enumerate(lines, start=1):
                    cursor.execute(
                        "INSERT INTO property_attribute_device (device,attribute,name,count,value,updated,accessed) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (
                            device_name,
                            attr_name,
                            prop_name,
                            str(count),
                            value,
                            now,
                            now,
                        ),
                    )
                    cursor.execute(
                        "INSERT INTO property_attribute_device_hist (device,attribute,name,id,count,value,date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (
                            device_name,
                            attr_name,
                            prop_name,
                            hist_id,
                            str(count),
                            value,
                            now,
                        ),
                    )
                self._purge_att_property(
                    "property_attribute_device_hist",
                    "device",
                    device_name,
                    attr_name,
                    prop_name,
                    cursor=cursor,
                )

    @log_me
    @use_cursor
    def put_device_property(self, device_name, nb_properties, prop_list):
        cursor = self.cursor
        hist_id = self._get_id(
            "device", cursor=cursor
        )  # Single id for the whole operation
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # attr_prop_list consists of nb_properties number of:
        # - property name, e.g. "MyProperty"
        # - number of lines in the value, e.g. "3"
        # - that many arbitrary strings, here 3
        #
        # Example (nb_properties = 2)
        # - MyProperty
        # - 3
        # - line1
        # - line2
        # - line3
        # - MyOtherProperty
        # - 1
        # - something
        #
        # TODO verify this structure, and raise a helpful error
        property_values = []
        lines = iter(prop_list)
        while len(property_values) < nb_properties:
            name = next(lines)
            number_of_lines = int(next(lines))
            value = [next(lines) for i in range(number_of_lines)]
            property_values.append((name, value))
            # Delete current property
            cursor.execute(
                "DELETE FROM property_device WHERE device LIKE ? AND name LIKE ?",
                (device_name, name),
            )
            # Insert into property table
            cursor.executemany(
                "INSERT INTO property_device (device, name, count, value, updated, accessed) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (device_name, name, str(i), line, now, now)
                    for i, line in enumerate(value, start=1)
                ],
            )
            # Insert into property history table
            cursor.executemany(
                "INSERT INTO property_device_hist (device, name, id, count, value, date) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (device_name, name, hist_id, str(i), line, now)
                    for i, line in enumerate(value, start=1)
                ],
            )
            self._purge_property(
                "property_device_hist", "device", device_name, name, cursor=cursor
            )

    @log_me
    @use_cursor
    def put_property(self, object_name, nb_properties, prop_list):
        cursor = self.cursor
        hist_id = self._get_id("object", cursor=cursor)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        property_values = []
        lines = iter(prop_list)
        while len(property_values) < nb_properties:
            name = next(lines)
            number_of_lines = int(next(lines))
            value = [next(lines) for i in range(number_of_lines)]
            property_values.append((name, value))
            # first delete the property from the property table
            cursor.execute(
                "DELETE FROM property WHERE object = ? AND name = ?",
                (object_name, name),
            )
            # Insert into property table
            cursor.executemany(
                "INSERT INTO property (object, name, count, value, updated, accessed) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (object_name, name, str(i), line, now, now)
                    for i, line in enumerate(value, start=1)
                ],
            )
            # Insert into property history table
            cursor.executemany(
                "INSERT INTO property_hist (object, name, id, count, value, date) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (object_name, name, hist_id, str(i), line, now)
                    for i, line in enumerate(value, start=1)
                ],
            )
            self._purge_property(
                "property_hist", "object", object_name, name, cursor=cursor
            )

    @log_me
    @use_cursor
    def put_server_info(self, tmp_server, tmp_host, tmp_mode, tmp_level, tmp_extra):
        cursor = self.cursor
        # If it is an empty host name -> get previous host where running
        previous_host = ""
        if self.fire_to_starter and tmp_host == "":
            adm_dev_name = "dserver/" + tmp_server
            previous_host = self._get_device_host(adm_dev_name, cursor=cursor)
        # first delete the server from the server table
        cursor.execute("DELETE FROM server WHERE name=?", (tmp_server,))
        # insert the new info for this server
        cursor.execute(
            "INSERT INTO server (name, host, mode, level) VALUES (?, ?, ?, ?)",
            (tmp_server, tmp_host, tmp_mode, tmp_level),
        )
        #  Update host's starter to update controlled servers list
        if self.fire_to_starter:
            hosts = []
            if previous_host == "":
                hosts.append(tmp_host)
            else:
                hosts.append(previous_host)
            self._send_starter_cmd(hosts)

    @log_me
    @use_cursor
    def uexport_device(self, dev_name):
        cursor = self.cursor
        # self._info("un-export device(dev_name=%s)", dev_name)
        cursor.execute(
            "UPDATE device SET exported=0,stopped=datetime('now', 'localtime') WHERE name LIKE ?",
            (dev_name,),
        )

    @log_me
    @use_cursor
    def uexport_event(self, event_name):
        cursor = self.cursor
        self._info("un-export event (event_name=%s)", event_name)
        cursor.execute(
            "UPDATE event SET exported=0,stopped=datetime('now', 'localtime') WHERE name LIKE ?",
            (event_name,),
        )

    @log_me
    @use_cursor
    def uexport_server(self, server_name):
        cursor = self.cursor
        # self._info(f"un-export all devices from server {server_name}")
        cursor.execute(
            "UPDATE device SET exported=0,stopped=datetime('now', 'localtime') WHERE server LIKE ?",
            (server_name,),
        )

    @log_me
    @use_cursor
    def delete_all_device_attribute_property(self, dev_name, attr_list):
        cursor = self.cursor
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for attr_name in attr_list:
            self._info(
                "_delete_all_device_attribute_property(): delete device %s attribute %s property(ies) from database",
                dev_name,
                attr_name,
            )
            # Is there something to delete ?
            cursor.execute(
                "SELECT DISTINCT name FROM property_attribute_device WHERE device =? AND attribute = ?",
                (dev_name, attr_name),
            )
            rows = cursor.fetchall()
            if len(rows) != 0:
                cursor.execute(
                    "DELETE FROM property_attribute_device WHERE device = ? AND attribute = ?",
                    (dev_name, attr_name),
                )
            # Mark this property as deleted
            for row in rows:
                hist_id = self._get_id("device_attribute", cursor=cursor)
                cursor.execute(
                    "INSERT INTO property_attribute_device_hist (date,device,attribute,name,id,count,value) VALUES (?,?,?,?,?,'0','DELETED')",
                    (now, dev_name, attr_name, row[0], hist_id),
                )
                self._purge_att_property(
                    "property_attribute_device_hist",
                    "device",
                    dev_name,
                    attr_name,
                    row[0],
                    cursor=cursor,
                )

    @log_me
    @use_cursor
    def my_sql_select(self, cmd):
        cursor = self.cursor
        cursor.execute(cmd)
        result_long = []
        result_str = []
        rows = list(cursor.fetchall())
        for row in rows:
            if row is None:
                result_str.append("")
                result_long.append(0)
            else:
                for field in row:
                    if field is not None:
                        result_str.append(str(field))
                        result_long.append(1)
                    else:
                        result_str.append("")
                        result_long.append(0)
        nb_fields = len(rows[0]) if rows else 1

        result_long.append(len(rows))
        result_long.append(nb_fields)

        result = (result_long, result_str)
        return result

    @log_me
    @use_cursor
    def get_csdb_server_list(self):
        cursor = self.cursor

        cursor.execute(
            "SELECT DISTINCT ior FROM device WHERE exported=1 AND domain='sys' AND family='database'"
        )
        results = []
        for row in cursor.fetchall():
            info = parse_ior(row[0])
            results.append(f"{info.host.decode()}:{info.port}")
        return results

    @log_me
    @use_cursor
    def get_attribute_alias2(self, attr_name):
        cursor = self.cursor
        cursor.execute(
            "SELECT alias from attribute_alias WHERE name LIKE ? ", (attr_name,)
        )
        rows = list(cursor.fetchall())
        if rows:
            # TODO What if we get more than one match? Probably not possible?
            return rows[0][0]
        th_exc(
            DB_SQLError,
            f"No attribute found for attribute '{attr_name}'",
            "DataBase::db_get_attribute_alias2()",
        )

    @log_me
    @use_cursor
    def get_alias_attribute(self, alias):
        cursor = self.cursor
        cursor.execute("SELECT name from attribute_alias WHERE alias LIKE ? ", (alias,))
        rows = cursor.fetchall()
        if rows:
            # TODO What if we get more than one match? Probably not possible?
            return rows[0][0]
        th_exc(
            DB_SQLError,
            f"No device found for alias '{alias}' ",
            "DataBase::db_get_alias_attribute()",
        )

    @log_me
    @use_cursor
    def rename_server(self, old_name, new_name):
        cursor = self.cursor
        # Check that the new name is not already used
        new_adm_name = "dserver/" + new_name
        cursor.execute("SELECT name from device WHERE name = ? ", (new_adm_name,))
        rows = cursor.fetchall()
        if len(rows) != 0:
            th_exc(
                DB_SQLError,
                f"Device server process name {new_name} is already used !",
                "DataBase::DbRenameServer()",
            )

        # get host where running
        previous_host = ""
        if self.fire_to_starter:
            try:
                adm_dev = "dserver/" + old_name
                previous_host = self._get_device_host(adm_dev, cursor=cursor)
            except Exception:
                th_exc(
                    DB_IncorrectServerName,
                    "Server " + old_name + "not defined in database!",
                    "DataBase::DbRenameServer()",
                )
        # Change ds exec name. This means
        #  1 - Update the device's server column
        #  2 - Change the ds admin device name
        #  3 - Change admin device property (if any)
        #  4 - Change admin device attribute property (if any)

        old_adm_name = "dserver/" + old_name
        tmp_new = new_name.split("/")
        new_exec = tmp_new[0]
        new_inst = tmp_new[1]
        new_adm_name = "dserver/" + new_name

        cursor.execute(
            "UPDATE device SET name =?, family =?, mamber =? WHERE name =?",
            (new_adm_name, new_exec, new_inst, old_adm_name),
        )

        cursor.execute(
            "UPDATE property_device set device=? WHERE device=?",
            (new_adm_name, old_adm_name),
        )

        cursor.execute(
            "UPDATE property_attribute_device set device=? WHERE device=?",
            (new_adm_name, old_adm_name),
        )

        #  Update host's starter to update controlled servers list
        if self.fire_to_starter:
            hosts = []
            if previous_host != "":
                hosts.append(previous_host)
            self._send_starter_cmd(hosts)


class Sqlite3Database(SqlDatabase):
    DB_API_NAME = "sqlite3"


def main():
    db = Sqlite3Database("2")
    db.add_device("MyServer/my1", ("a/b/c", ("a", "b", "c")), "MyClass")
    db.close_db()


def get_db(personal_name="2"):
    #    return Executor.submit(Sqlite3Database).result()
    return Sqlite3Database(personal_name)


if __name__ == "__main__":
    main()
