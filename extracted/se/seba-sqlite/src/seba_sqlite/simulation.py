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


class Simulation:
    ID_NAME = "ID"
    BATCH_NAME = "BATCHID"
    REALIZATION_NAME = "REALIZATIONID"
    SET_NAME = "SETID"
    START_TIMESTAMP_NAME = "STARTTIMESTAMP"
    END_TIMESTAMP_NAME = "ENDTIMESTAMP"
    NAME_NAME = "NAME"
    IS_SUCCESS_NAME = "SUCCESS"
    IS_GRADIENT_NAME = "ISGRADIENT"
    TABLE_NAME = "SIMULATION"

    def __init__(
        self,
        conn,
        sim_id=None,
        batch_id=None,
        realization_id=None,
        set_id=None,
        start_time_stamp=None,
        end_time_stamp=None,
        name=None,
        success=None,
        is_gradient=False,
        commit=False,
    ):
        # Constructor.
        # :param conn: the sqlite database connection
        # :type conn:
        # :param batch_id: the batch this simulation belongs to
        # :type batch_id: int or None
        # :param realization_id: the realization that is used in this simulation
        # :type realization_id: int or None
        # :param set_id: the set id of the set used in this simulation
        # :type set_id: int or None
        # :param start_time_stamp: the start datetime of this simulation
        # :type start_time_stamp: float
        # :param name: A name for this simulation
        # :type name: str
        # :param is_gradient: is this a gradient simulation
        # :type is_gradient: int [0|1]
        self.simulation_id = sim_id
        self.batch_id = batch_id
        self.realization_id = realization_id
        self.set_id = set_id
        self.start_time_stamp = start_time_stamp
        self.end_time_stamp = end_time_stamp
        self.success = success
        self.name = name
        self.is_gradient = int(is_gradient)
        # save it to the database if required
        if commit:
            sql = (
                "INSERT INTO {table} ({batch}, {realization}, "
                "{set}, {start}, "
                "{name}, {gradient}) VALUES (?,?,?,?,?,?)".format(
                    batch=self.BATCH_NAME,
                    realization=self.REALIZATION_NAME,
                    set=self.SET_NAME,
                    start=self.START_TIMESTAMP_NAME,
                    name=self.NAME_NAME,
                    gradient=self.IS_GRADIENT_NAME,
                    table=self.TABLE_NAME,
                )
            )
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (
                    self.batch_id,
                    self.realization_id,
                    self.set_id,
                    self.start_time_stamp,
                    self.name,
                    self.is_gradient,
                ),
            )
            self.simulation_id = cursor.lastrowid
            conn.commit()

    def __repr__(self):
        simulation = (
            "simulationId: {id}, "
            "name: {name}, "
            "batchId: {batch}, "
            "realizationId: {realization}, "
            "setId: {set}, "
            "startTimeDtamp: {start}, "
            "endTimeDtamp: {end}, "
            "success: {success}, "
            "isGradient: {is_grad}".format(
                id=self.simulation_id,
                name=self.name,
                batch=self.batch_id,
                realization=self.realization_id,
                set=self.set_id,
                start=self.start_time_stamp,
                end=self.end_time_stamp,
                success=self.success,
                is_grad=self.is_gradient,
            )
        )
        return simulation

    @classmethod
    def create_or_get_existing(
        cls,
        conn,
        simulation_id=None,
        batch_id=None,
        realization_id=None,
        set_id=None,
        start_time_stamp=None,
        name=None,
        is_gradient=False,
    ):
        try:
            return cls.get(conn, simulation_id)
        except ObjectNotFoundError:
            return Simulation(
                conn=conn,
                batch_id=batch_id,
                realization_id=realization_id,
                set_id=set_id,
                start_time_stamp=start_time_stamp,
                name=name,
                is_gradient=is_gradient,
                commit=True,
            )

    @classmethod
    def get(cls, conn, simulation_id=None, name=None):
        sql = "SELECT * FROM {table}".format(table=cls.TABLE_NAME)
        cursor = conn.cursor()
        if simulation_id is not None:
            sql += " WHERE {id} = ?".format(id=cls.ID_NAME)
            params = (simulation_id,)
        elif name is not None:
            sql += " WHERE {name} = ?".format(name=cls.NAME_NAME)
            params = (name,)
        try:
            cursor.execute(sql, params)
            row = cursor.fetchone()

            if row is None:
                raise ObjectNotFoundError("Simulation does not exist")
            return Simulation(conn, *row)
        except NameError as exc:
            raise ObjectNotFoundError("Simulation does not exist") from exc

    @classmethod
    def get_all(cls, conn):
        sql = "SELECT * FROM {table}".format(table=cls.TABLE_NAME)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [Simulation(conn, *row) for row in rows]
        return result

    @classmethod
    def filter_by_gradient(cls, conn, gradient):
        sql = "SELECT * FROM {table}  WHERE {name} = ?".format(
            table=cls.TABLE_NAME, name=cls.IS_GRADIENT_NAME
        )
        params = (int(gradient),)
        cursor = conn.cursor()
        cursor.execute(sql, params)

        rows = cursor.fetchall()
        result = [Simulation(conn, *row) for row in rows]
        return result

    def set_ended(self, conn, success, end_time_stamp):
        # update the experiment in the database
        # Set the end timestamp of this simulation.
        # :param conn: the sqlite database connection
        # :type conn:
        # :param success: was the simulation a success
        # :type success: int[0|1]
        # :param end_time_stamp: the end timestamp of the simulation
        # :type end_time_stamp: float
        self.end_time_stamp = end_time_stamp
        self.success = success
        sql = "UPDATE {table} SET {end}=?, {success}=?  WHERE {id}=?".format(
            end=self.END_TIMESTAMP_NAME,
            success=self.IS_SUCCESS_NAME,
            id=self.ID_NAME,
            table=self.TABLE_NAME,
        )
        cursor = conn.cursor()
        cursor.execute(sql, (self.end_time_stamp, int(success), self.simulation_id))
        conn.commit()
