#  Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  Licensed under the Amazon Software License (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at
#
#  http://aws.amazon.com/asl/
#
#  or in the "license" file accompanying this file. This file is distributed
#  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
#  express or implied. See the License for the specific language governing
#  permissions and limitations under the License.

from datetime import datetime
import json
import sqlite3
from threading import Lock


class KeyValueStore(object):
    """
    A sqlite based key value store.
    """

    # A lock to improve perf by avoiding concurrent write operation
    lock = Lock()

    def __init__(self, db, table):
        self.table = table
        self.conn = sqlite3.connect(db, check_same_thread=False)
        cur = self.conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS {table} ('
                    'k TEXT PRIMARY KEY NOT NULL, '
                    'v TEXT NOT NULL, '
                    'ctime DATETIME, '
                    'mtime DATETIME)'.format(table=table))
        self.conn.commit()

    def save(self, key, value):
        with self.lock:
            cur = self.conn.cursor()
            if self._get(key):
                cur.execute('UPDATE {table} SET v = ?, mtime = ? WHERE k = ?'.
                            format(table=self.table),
                            (json.dumps(value),
                             datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
                             key))
            else:
                cur.execute('INSERT INTO {table} VALUES (?, ?, ?, ?)'.
                            format(table=self.table),
                            (key,
                             json.dumps(value),
                             datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
                             datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')))
            self.conn.commit()

    def get(self, key):
        with self.lock:
            return self._get(key)

    def _get(self, key):
        cur = self.conn.cursor()
        cur.execute('SELECT v FROM {table} WHERE k = ?'.
                    format(table=self.table), (key,))
        row = cur.fetchone()
        if row is not None:
            return json.loads(row[0])
        return None

    def delete(self, key):
        with self.lock:
            cur = self.conn.cursor()
            cur.execute('DELETE FROM {table} WHERE k = ?'.
                        format(table=self.table), (key,))
            self.conn.commit()

    def close(self):
        self.conn.close()
