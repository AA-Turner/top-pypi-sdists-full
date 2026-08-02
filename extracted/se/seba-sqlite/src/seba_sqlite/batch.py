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


class Batch:
    ID_NAME = "ID"
    EXPERIMENT_NAME = "EXPERIMENTID"
    START_TIMESTAMP_NAME = "STARTTIMESTAMP"
    END_TIMESTAMP_NAME = "ENDTIMESTAMP"
    IS_SUCCESS_NAME = "SUCCESS"
    TABLE_NAME = "BATCH"

    def __init__(
        self,
        conn,
        batch_id=None,
        experiment_id=None,
        start_time_stamp=None,
        end_time_stamp=None,
        success=False,
        commit=False,
    ):  # Retrieve/Add a batch information from the database. Initialize a batch
        # instance from this data

        # :param conn: the sqlite database connection
        # :type conn:
        # :param batch_id: id of the batch to load, if this is a new batch set it to None
        # :type batch_id: int or None
        # :param experiment_id: the experiment this batch belongs to
        # :type experiment_id: int or None
        # :param start_time_stamp: the start timestamp
        # :type start_time_stamp: float or None
        # Check what is the next batch number in this experiment
        self.batch_id = batch_id
        self.experiment_id = experiment_id
        self.start_time_stamp = start_time_stamp
        self.end_time_stamp = end_time_stamp
        self.success = success

        if commit:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COALESCE(MAX({batch_id}), -1)+1  FROM {table} "
                "WHERE {experiment}=?".format(
                    table=self.TABLE_NAME,
                    batch_id=self.ID_NAME,
                    experiment=self.EXPERIMENT_NAME,
                ),
                (experiment_id,),
            )
            row = cursor.fetchone()

            self.batch_id = row[0]

            # Add a new record to the database for this batch
            sql = (
                "INSERT INTO {table} ({experiment}, {start}, {batch_id}, {succ}) "
                "VALUES (?,?,?,?)".format(
                    experiment=self.EXPERIMENT_NAME,
                    start=self.START_TIMESTAMP_NAME,
                    batch_id=self.ID_NAME,
                    succ=self.IS_SUCCESS_NAME,
                    table=self.TABLE_NAME,
                )
            )
            cursor.execute(
                sql,
                (
                    self.experiment_id,
                    self.start_time_stamp,
                    self.batch_id,
                    self.success,
                ),
            )
            conn.commit()

    def __repr__(self):
        batch = (
            "batchId: {id}, "
            "experimentId : {exp}, "
            "startTimeStamp: {start}, "
            "endTimeStamp: {end}, "
            "success: {succ}".format(
                id=self.batch_id,
                exp=self.experiment_id,
                start=self.start_time_stamp,
                end=self.end_time_stamp,
                succ=self.success,
            )
        )
        return batch

    @classmethod
    def create_or_get_existing(
        cls, conn, batch_id=None, experiment_id=None, start_time_stamp=None
    ):
        if batch_id and experiment_id:
            return cls.get(conn, experiment_id, batch_id)
        if experiment_id and start_time_stamp:
            return Batch(
                conn,
                experiment_id=experiment_id,
                start_time_stamp=start_time_stamp,
                commit=True,
            )
        raise ValueError("Not enough information to load or create a Batch")

    @classmethod
    def get(cls, conn, experiment, batch_id):
        sql = "SELECT * FROM {table} " "WHERE {experiment}=? AND {id}=?".format(
            experiment=cls.EXPERIMENT_NAME, table=cls.TABLE_NAME, id=cls.ID_NAME
        )
        cursor = conn.cursor()
        cursor.execute(sql, (experiment, batch_id))
        row = cursor.fetchone()
        if row is None:
            raise ObjectNotFoundError("A batch with given parameters does not exist")
        return Batch(conn, *row)

    @classmethod
    def get_all(cls, conn):
        sql = "SELECT * FROM {table}".format(table=cls.TABLE_NAME)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = [Batch(conn, *row) for row in cursor.fetchall()]
        return result

    @classmethod
    def get_for_experiment(cls, conn, experiment_id):
        sql = "SELECT * FROM {table} " "WHERE {experiment}=?".format(
            experiment=cls.EXPERIMENT_NAME, table=cls.TABLE_NAME
        )
        cursor = conn.cursor()
        cursor.execute(sql, (experiment_id,))
        result = [Batch(conn, *row) for row in cursor.fetchall()]
        return result

    def set_ended(self, conn, end_time_stamp, success):
        # Set the end time stamp for this batch and save it in the database.
        # :param conn: the sqlite database connection
        # :type conn:
        # :type end_time_stamp: float
        # :param success: was the batch successful
        # :type success: int [0|1]
        self.end_time_stamp = end_time_stamp
        self.success = success
        sql = (
            "UPDATE {table} SET {end}=?, {success}=? WHERE {id}=? AND "
            "{experiment}=?".format(
                end=self.END_TIMESTAMP_NAME,
                success=self.IS_SUCCESS_NAME,
                id=self.ID_NAME,
                experiment=self.EXPERIMENT_NAME,
                table=self.TABLE_NAME,
            )
        )
        cursor = conn.cursor()
        cursor.execute(
            sql, (end_time_stamp, int(success), self.batch_id, self.experiment_id)
        )
        conn.commit()

    def save(self, conn):
        # saves the current status of the instance to the database
        sql = (
            "UPDATE {table} SET {experiment}=?, "
            "{start}=?, {end}=?, {success}=? "
            "WHERE {id}=?".format(
                id=self.ID_NAME,
                experiment=self.EXPERIMENT_NAME,
                start=self.START_TIMESTAMP_NAME,
                end=self.END_TIMESTAMP_NAME,
                success=self.IS_SUCCESS_NAME,
                table=self.TABLE_NAME,
            )
        )
        cursor = conn.cursor()
        cursor.execute(
            sql,
            (
                self.experiment_id,
                self.batch_id,
                self.start_time_stamp,
                self.end_time_stamp,
                self.success,
                self.batch_id,
            ),
        )
