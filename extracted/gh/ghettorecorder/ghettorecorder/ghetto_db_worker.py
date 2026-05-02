"""Made with multiprocessing in mind.

"""
import os
import time
import sqlite3
import datetime
dir_name = os.path.join(os.path.dirname(os.path.abspath(__file__)))


class DBWorker:
    def __init__(self):
        self.kwargs = None  # caller kwargs of whatever interesting things, pull from somewhere; use as container
        self.feature_dct = {'runs_meta': None,
                            'runs_record': None,
                            'record_stop': None,
                            'runs_listen': None}

        self.radios_parent_dir = ''
        self.db_name = 'ghetto_recorder_control.db'


dbWorker = DBWorker()


def db_worker_init(**kwargs):
    """One can write modules of any kind and make it mp.

    Switch attributes and trigger methods from frontend.

    * one read and one write table
    * read table for frontend server to support delivery
    * write for client
    * internal db thread reads order table
    * database functions module
    """
    if kwargs:
        dbWorker.kwargs = kwargs  # kwargs from caller dumped for the whole module
        dbWorker.__dict__.update(kwargs)
        dbWorker.radios_parent_dir = kwargs['radios_parent_dir']

        db_path = os.path.join(dbWorker.radios_parent_dir, dbWorker.db_name)
        if not os.path.isfile(db_path):
            empty_db_from_schema()


def instance_start_stop(radio_name=None):
    """*stop* in DB will be executed on the radio instance.
    """
    stop = False
    SQL = "SELECT stop FROM GRAction WHERE radio_name = ? "
    data = (radio_name,)
    cursor = table_select(SQL, data)

    for row in cursor:
        if row['stop']:
            stop = True
    cursor.close()
    return stop


def feature_start_stop_get(radio_name=None):
    """runs_listen, runs_record, runs_meta
    | 0 off
    | 1 on
    | None Null (default)
    list wit tuples [(chill,0), (foo,1), (bar,1)]
    """
    SQL = "SELECT runs_meta, runs_record, record_stop, runs_listen FROM GRAction WHERE radio_name = ?"
    data = (radio_name,)
    cursor = table_select(SQL, data)

    for row in cursor:
        dbWorker.feature_dct = {'runs_meta': row['runs_meta'],
                                'runs_record': row['runs_record'],
                                'record_stop': row['record_stop'],
                                'runs_listen': row['runs_listen']}
    cursor.close()
    return dbWorker.feature_dct


def feature_start_stop_reset(radio_name=None):
    """Set feature cell Null.
    """
    col_lst = [feat + ' = ?' for feat in dbWorker.feature_dct]
    SQL = "UPDATE GRAction SET " + ','.join(col_lst) + " WHERE radio_name = ?"
    val_lst = [None for _ in range(len(col_lst))]
    val_lst.append(radio_name)
    data = tuple(column for column in val_lst)
    table_insert(SQL, data)


def db_radio_del(table_id):
    """
    """
    table_insert("DELETE FROM GhettoRecorder WHERE id = ?;", (int(table_id),))
    table_insert("DELETE FROM GRAction WHERE id = ?;", (int(table_id),))


def db_radio_name_url_show_all():
    """"""
    print('\n\t---')
    SQL = "SELECT radio_name, radio_url FROM GhettoRecorder "
    data = ()
    cursor = table_select(SQL, data)
    for row in cursor:
        print(f"* {row['radio_name']:<20} {row['radio_url']}")
    print('\t---\n')
    cursor.close()


def db_insert_retry(sql, data):
    """Retry until locked DB is open."""
    while 1:
        done = table_insert(sql, data)
        if done:
            break
        time.sleep(0.5)


def db_upd_radio_props(self, attr_dct):
    """Update current settings in db"""
    upd_attr_tbl, val_tbl = [], []

    for attrib, val in attr_dct.items():  # update new columns
        upd_attr = str(attrib) + ' = ?'
        upd_attr_tbl.append(str(upd_attr))

        upd_val = getattr(self, str(attrib))
        if attrib == 'time_stamp':
            upd_val = datetime.datetime.now()
        val_tbl.append(str(upd_val))

    set_str = ','.join(upd_attr_tbl)
    SQL = "UPDATE GhettoRecorder SET " + set_str + " WHERE radio_name = ?"
    val_tbl.append(self.radio_name)

    table_insert(SQL, tuple(val for val in val_tbl))


def db_create_rows(self):
    """Create rows in tables.

    :params: self: caller instance it(self) context
    """
    SQL = "INSERT INTO GhettoRecorder (radio_name) VALUES (?);"
    table_insert(SQL, (self.radio_name,))
    SQL = "INSERT INTO GRAction (runs_meta, runs_record, record_stop, recorder_file_write, " \
          "runs_listen, stop,  radio_name) VALUES (?,?,?,?, ?,?,?);"
    data = (None, None, None, None, None, None, self.radio_name)
    table_insert(SQL, data)


def db_alter_table_cols(col_count_tbl, attr_dct):
    """Alter GhettoRecorder (read) table by columns of __init__ attributes.

    :params: col_count_tbl: table with names of current columns
    :params: attr_dct: dict of dump of (dead, no way to get own instance?) instance of GR with current values (getattr)
    """
    alter_tbl_col = True if len(col_count_tbl) < len(attr_dct) else False
    if alter_tbl_col:
        for attrib in attr_dct.keys():
            SQL = "ALTER TABLE GhettoRecorder ADD " + attrib + " VARCHAR;"
            table_insert(SQL, ())


def db_count_table_cols():
    """Column NAME dump (current) of GhettoRecorder table to see how many columns we have here.
    """
    SQL, column_name = "SELECT * FROM GhettoRecorder", 0
    cursor = table_select(SQL, ())
    col_count_tbl = [tup[column_name] for tup in cursor.description]
    cursor.close()
    return col_count_tbl


def db_remote_control_loop(self, attr_dct):
    """Content of while loop.

    * update read table
    * check we must shut down
    * check which feature attribute to switch

    We can also run methods here.

    :params: self: caller instance it(self) context
    :params: attr_dct: dump of a (fake) instance.__dict__ with actual val of caller instance;
    :method: radio_db_remote_control: caller instance.radio_db_remote_control()
    """
    exit_ = instance_start_stop(self.radio_name)  # read stop order
    if bool(exit_):
        print(f'\tDB set: . {self.radio_name} . shut down radio')
        self.cancel()

    upd = False
    feat_dct = feature_start_stop_get(self.radio_name)  # read feature change
    for feat, setting in feat_dct.items():
        if setting is not None:
            upd = True
            print(f'\tDB set: . {self.radio_name} . {feat} {bool(setting)}')
            val_bool = getattr(self, feat)  # only features with True or False here
            if bool(setting) != val_bool:
                setattr(self, feat, bool(setting))
    if upd:
        feature_start_stop_reset(self.radio_name)

    db_upd_radio_props(self, attr_dct)


def query_col_tbl_ghetto_recorder(column, radio_name):
    """Select a column from GhettoRecorder table.

    :params: column: table column
    :params: radio_name: radio_name
    :returns: string of cell, column row, else empty string
    """
    SQL = "SELECT " + column + " FROM GhettoRecorder WHERE radio_name = ? "
    data = (radio_name,)
    cursor = table_select(SQL, data)
    col_row_val = None
    bla = cursor.fetchall()
    print(bla)
    if cursor:
        col_row_val = [row[column] for row in bla if row[column] is not None]
        cursor.close()
    return ''.join(str(col_row_val)) if cursor else None


def query_all_tbl_ghetto_recorder():
    """Select all.
    Caller close cursor.
    """
    SQL = "SELECT * FROM GhettoRecorder"
    cursor = table_select(SQL, ())
    tbl = cursor
    return tbl


def get_db_path(db=dbWorker.db_name):
    return os.path.join(dbWorker.radios_parent_dir, db)


def get_db_connection():

    db = get_db_path()
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row  # can use column names, but often get str([1,2,3])
    return conn


def table_select(sql_statement, data):
    """rv.close() on caller
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        rv = cur.execute(sql_statement, data)
        conn.commit()
    except sqlite3.OperationalError:
        print(f'table_select() {sql_statement} {data}')
        rv = None
    # conn.close()  # remainder
    return rv


def table_insert(sql_statement, data):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql_statement, data)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        print(sql_statement)
        print(data)
        return False
    finally:
        conn.close()


def empty_db_from_schema():
    """
    | Schema with
    | minimum GhettoRecorder table for reading properties,
    | complete GRAction table for setting integer values to switch a feature on/off .
    """
    if not dbWorker.radios_parent_dir:
        raise ValueError('no path for empty_db_from_schema')
    db_path = str(os.path.join(dbWorker.radios_parent_dir, dbWorker.db_name))
    conn = sqlite3.connect(db_path)

    with open((os.path.join(dir_name, 'schema.sql')), encoding='utf-8') as text_reader:
        conn.executescript(text_reader.read())
    conn.close()
    print(f'Database path: {db_path}')
