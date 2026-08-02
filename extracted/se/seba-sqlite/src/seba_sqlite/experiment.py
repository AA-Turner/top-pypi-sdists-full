# Copyright (C) The Netherlands Organisation for Applied Scientific Research,
# TNO, 2015-2022. All rights reserved.
#
# This file is part of Seba: a proprietary software library for ensemble based
# optimization developed by TNO. This file, the Seba software or data or
# information contained in the software may not be copied or distributed without
# prior written permission from TNO.
#
# Seba and the information and data contained in this software are confidential.
# Neither the whole or any part of the software and the data and information it
# contains may be disclosed to any third party without the prior written consent
# of The Netherlands Organisation for Applied Scientific Research (TNO).

from .exceptions import ObjectNotFoundError


class Experiment:
    ID_NAME = "ID"
    NAME_NAME = "NAME"
    STARTTIMESTAMP_NAME = "STARTTIMESTAMP"
    ENDTIMESTAMP_NAME = "ENDTIMESTAMP"
    TABLE_NAME = "EXPERIMENT"

    def __init__(
        self,
        conn,
        experiment_id=None,
        name=None,
        starttime=None,
        endtime=None,
        commit=False,
    ):
        # The class "constructor" - It's actually an initializer
        # if the request contains an experiment_id , get the experiment from the database.

        # :param conn: the sqlite database connection
        # :type conn:
        # :param experiment_id: id of the experiment to load, if this is a new
        # experiment set it to None
        # :type experiment_id: int or None
        # :param name: the name of the experiment
        # :type name: str or None
        # :param starttime: the start timestamp  of the experiment
        # :type starttime: float or None

        self.experiment_id = experiment_id
        self.name = name
        self.starttimestamp = starttime
        self.endtimestamp = endtime
        self.batches = {}  # batch_id as key
        self.functions = {}  # name as key
        self.controls = {}  # control name as key
        self.realizations = {}  # realization name as key

        cursor = conn.cursor()

        # First we will try to create
        # if we cant, we try to load a specific
        # if no load information is provided, we'll try to get the existing one
        # if doesn't exist we throw an exception

        if commit:
            cursor.execute(
                "INSERT INTO {table} ({name}, {start}) VALUES (?, "
                "?)".format(
                    name=self.NAME_NAME,
                    start=self.STARTTIMESTAMP_NAME,
                    table=self.TABLE_NAME,
                ),
                (name, starttime),
            )
            self.experiment_id = cursor.lastrowid
            conn.commit()

    def __repr__(self):
        experiment = (
            "experimentId: {id}, "
            "name: {name}, "
            "startTimeStamp: {start}, "
            "endTimeStamp: {end}".format(
                id=self.experiment_id,
                name=self.name,
                start=self.starttimestamp,
                end=self.endtimestamp,
            )
        )
        return experiment

    @classmethod
    def create_or_get_existing(
        cls, conn, experiment_id=None, name=None, starttime=None
    ):
        if name and starttime:
            return Experiment(conn, name=name, starttime=starttime, commit=True)
        try:
            return cls.get(conn, experiment_id)
        except ObjectNotFoundError as onf:
            raise onf

    @classmethod
    def get(cls, conn, experiment_id=None):
        cursor = conn.cursor()
        first_part = "SELECT * FROM {table} WHERE ".format(table=cls.TABLE_NAME)
        if experiment_id:
            cursor.execute(
                first_part + "{id}=?".format(id=cls.ID_NAME), (experiment_id,)
            )
        else:
            cursor.execute(
                first_part + "{id}=(SELECT MAX({id}) FROM "
                "{table})".format(id=cls.ID_NAME, table=cls.TABLE_NAME)
            )
        row = cursor.fetchone()
        if not row:
            raise ObjectNotFoundError("No existing experiments to load")
        return Experiment(conn, *row)

    def set_ended(self, conn, endtime):
        # Set the end timestampo of the experiment and save it to the database.
        # :param conn: the sqlite database connection
        # :type conn:
        # :param endtime: the start timestamp  of the experiment
        # :type endtime: float
        # update the experiment in the database
        if endtime:
            self.endtimestamp = endtime
            sql = "UPDATE {table} SET {end}=? WHERE {id}=?".format(
                table=self.TABLE_NAME, end=self.ENDTIMESTAMP_NAME, id=self.ID_NAME
            )
            cursor = conn.cursor()
            cursor.execute(sql, (self.endtimestamp, self.experiment_id))
            conn.commit()
        else:
            raise ValueError("Wrong end time for an experiment")
