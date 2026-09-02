#!/usr/bin/env python3
"""Pushover Client installable by `pip install macwinnie_py_pushover_client`"""

import datetime
import json
import os
import pathlib
from pathlib import Path

import requests


class device:
    """Pushover Device"""

    def __init__(self, name):
        self.name = name


class user:
    """Pushover User class"""

    def __init__(self, token, device=None):
        self.devices = []
        self.token = token
        if device != None:
            self.devices.append(device)

    def addDevice(self, name):
        """Method that adds a device to an user"""
        self.devices.appen(name)


class app:
    """Pushover App class"""

    def __init__(self, token):
        """Each App that wants to send a Pushover Notification has to be registered and get an official token."""
        self.token = token


class receipt:
    """Pushover receipt handling class"""

    def __init__(self, receipt, app):

        self.receipt = None
        self.app = None
        self.apiUrl = None
        self.info = None

        self.apiUrl = pushover.baseUrl.format(
            location="receipts/{receipt}.json?token={app}".format(
                receipt=receipt, app=app
            )
        )

    def setInfo(self, data):
        """Decrypt and store JSON data from receipt"""
        self.info = json.loads(data)


class pushover:
    """
    Class that handles Pushover actions.

    By default at instantiation, `user_tkn` is `None` which will either fetch `PUSHOVER_USERS` environmental variable or ask for users input.
    To skip adding users at creation, set to `False` instead!
    """

    userAgent = "curl/7.54"

    apiVersion = 1
    baseUrl = "https://api.pushover.net/{version}/".format(version=str(apiVersion))
    baseUrl += "{location}"

    def __init__(self, app_tkn=None, user_tkn=None):
        """ENV variables `PUSHOVER_APP` (API token) and `PUSHOVER_USERS` (JSON List of User token like `["asdfghj123456", "yxcvbnm098765"]`) can be used."""

        self.db = None
        self.colNames = None
        self.dbTable = "po_messages"

        self.app = None
        self.users = []
        self.receipts = []

        self.session = requests.session()
        self.session.headers = {"User-Agent": self.userAgent}
        if app_tkn != None:
            self.app = app(app_tkn)
        else:
            app_tkn = os.getenv("PUSHOVER_APP")
            if app_tkn == None:
                app_tkn = input("{d}: ".format(d="Input your API token: "))
            self.app = app(app_tkn)
        if user_tkn != None and user_tkn != False:
            self.users.append(user_tkn)
        elif user_tkn != False:
            user_tkn = os.getenv("PUSHOVER_USERS")
            if user_tkn == None:
                user_tkn = input("{d}: ".format(d="Input your User token: "))
                self.users.append(user(user_tkn))
            else:
                user_tkn = json.loads(user_tkn)
                for u in user_tkn:
                    self.users.append(user(u))

    def setDB(self, db=None):
        """
        Define a Database object to interact with, store sent messages and cofirmation dates fetched from Pushover.
        Example of how such a Database object has to look like can be seen in [macwinnie_sqlite3](https://macwinnie.github.io/py-sqlite3) which can seemlessly be used.
        ENV variable `PUSHOVER_SQLITE_FILENAME` (default `database.sqlite`, relative to working dir!) can be used to rename the default DB SQLite file.
        Database object needs to implement ability of usage of yoyo-migrations through method `migrate`.
        """
        dbMigrationPath = "{}/{}".format(
            os.path.dirname(os.path.abspath(__file__)), "db_migrations"
        )
        if db == None:
            from macwinnie_sqlite3 import SQLite

            envPath = Path(os.getenv("PUSHOVER_SQLITE_FILENAME", "database.sqlite"))
            sqlitePath = str(envPath if envPath.is_absolute() else Path.cwd() / envPath)

            self.db = SQLite.database(
                sqlitePath,
                dbMigrationPath,
            )
        else:
            db.migrate(dbMigrationPath)
            self.db = db
        self.db.startAction()
        sql = "SELECT name FROM pragma_table_info( '{dbTable}' ) ORDER BY cid;".format(
            dbTable=self.dbTable
        )
        self.db.execute(sql)
        self.colNames = [n[0] for n in self.db.fetchall()]
        self.db.close()

    def addUser(self, user_tkn, device=None):
        """Add an user who should be informed"""
        self.users.append(user(user_tkn, device))

    def messageAll(
        self,
        message,
        title=None,
        priority=0,
        expire=None,
        retry=None,
        device=None,
        sound=None,
        url=None,
        url_title=None,
        attachment=None,
        timestamp=None,
    ):
        """Method to send a message to all defined users"""
        for user in self.users:
            self.message(
                message=message,
                user=user,
                title=title,
                priority=priority,
                expire=expire,
                retry=retry,
                device=device,
                sound=sound,
                url=url,
                url_title=url_title,
                attachment=attachment,
                timestamp=timestamp,
            )

    def sendMessage(
        self,
        message,
        title=None,
        expire=None,
        retry=None,
        device=None,
        sound=None,
        url=None,
        url_title=None,
        attachment=None,
        timestamp=None,
    ):
        """Use `messageAll` and send a regular message to all users"""
        self.messageAll(
            message=message,
            title=title,
            expire=expire,
            retry=retry,
            device=device,
            sound=sound,
            url=url,
            url_title=url_title,
            attachment=attachment,
            timestamp=timestamp,
        )

    def sendPrioMessage(
        self,
        message,
        title=None,
        expire=None,
        retry=None,
        device=None,
        sound=None,
        url=None,
        url_title=None,
        attachment=None,
        timestamp=None,
    ):
        """Use `messageAll` and send a prio message to all users (prio 1)"""
        self.messageAll(
            message=message,
            title=title,
            priority=1,
            expire=expire,
            retry=retry,
            device=device,
            sound=sound,
            url=url,
            url_title=url_title,
            attachment=attachment,
            timestamp=timestamp,
        )

    def sendConfirmPrioMessage(
        self,
        message,
        title=None,
        expire=None,
        retry=None,
        device=None,
        sound=None,
        url=None,
        url_title=None,
        attachment=None,
        timestamp=None,
    ):
        """Use `messageAll` and send a prio message to all users, that has to be confirmed (high prio, prio 2)"""
        self.messageAll(
            message=message,
            title=title,
            priority=2,
            expire=expire,
            retry=retry,
            device=device,
            sound=sound,
            url=url,
            url_title=url_title,
            attachment=attachment,
            timestamp=timestamp,
        )

    def message(
        self,
        message,
        user,
        title=None,
        priority=0,
        expire=None,
        retry=None,
        device=None,
        sound=None,
        url=None,
        url_title=None,
        attachment=None,
        timestamp=None,
    ):
        """Method to publish a message per device"""
        apiUrl = self.baseUrl.format(location="messages.json")

        data = {"token": self.app.token, "user": user.token, "message": message}

        if title != None:
            data["title"] = title
        if priority != 0:
            data["priority"] = priority
            if expire == None:
                expire = 10800  # maximum value: 10800
            if retry == None:
                retry = 60  # minimum value: 30
        if expire != None:
            data["expire"] = expire
        if retry != None:
            data["retry"] = retry
        if device != None:
            data["device"] = device
        if sound != None:
            data["sound"] = sound
        if url != None:
            data["url"] = url
        if url_title != None:
            data["url_title"] = url_title
        if attachment != None:
            data["attachment"] = attachment
        if timestamp != None:
            data["timestamp"] = timestamp

        if self.db != None:
            db_data = {}
            for key in data:
                if key in self.colNames:
                    db_data[key] = data[key]
            sql = "INSERT INTO {dbTable} ({colNames}) VALUES ({valPh});".format(
                dbTable=self.dbTable,
                colNames=", ".join(db_data.keys()),
                valPh=", ".join(["?"] * len(db_data)),
            )
            self.db.fullExecute(sql, list(db_data.values()))
            db_id = self.db.lastrowid()

        rsp = self.session.post(
            apiUrl, data=json.dumps(data), headers={"content-type": "application/json"}
        )

        if self.db != None:
            sql = "UPDATE {dbTable} SET api_rc = ? WHERE id = ?;".format(
                dbTable=self.dbTable
            )
            self.db.fullExecute(sql, [rsp.status_code, db_id])

        if rsp.status_code == 200:
            data = json.loads(rsp.text)
            if self.db != None:
                if "receipt" in data:
                    self.receipts.append(receipt(data["receipt"], self.app.token))
                    sql = "UPDATE {dbTable} SET receipt = ? WHERE id = ?;".format(
                        dbTable=self.dbTable
                    )
                    self.db.fullExecute(sql, [data["receipt"], db_id])

    def checkUnconfirmedPrio(self):
        """When a DB is defined for Pushover client, this method should run on a reccuring period to fetch and update confirmation dates for PRIO 2 messages"""
        sql = "SELECT * FROM {dbTable} WHERE priority = 2 AND receipt IS NOT NULL AND confirmation IS NULL;".format(
            dbTable=self.dbTable
        )
        self.db.startAction()
        self.db.execute(sql)
        allUnconfirmed = self.db.fetchallNamed()
        self.db.close()
        for uc in allUnconfirmed:
            apiUrl = self.baseUrl.format(
                location="receipts/{receipt}.json?token={token}".format(
                    receipt=uc["receipt"], token=self.app.token
                )
            )
            rsp = self.session.get(apiUrl)
            if rsp.status_code == 200:
                data = json.loads(rsp.text)
                if data["acknowledged"] == True:
                    confirmationDate = datetime.datetime.fromtimestamp(
                        data["acknowledged_at"]
                    )
                    sql = "UPDATE {dbTable} SET receipt_info = ?, confirmation = ? WHERE id = ?".format(
                        dbTable=self.dbTable
                    )
                    self.db.fullExecute(
                        sql,
                        [
                            json.dumps(data, indent=4),
                            confirmationDate.strftime("%Y-%m-%d %H:%M:%S"),
                            uc["id"],
                        ],
                    )
                else:
                    sql = "UPDATE {dbTable} SET receipt_info = ? WHERE id = ?".format(
                        dbTable=self.dbTable
                    )
                    self.db.fullExecute(sql, [json.dumps(data, indent=4), uc["id"]])
