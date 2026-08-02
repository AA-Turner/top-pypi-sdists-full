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


class SimulationResult:
    ID_NAME = "ID"
    SIMULATION_NAME = "SIMULATIONID"
    FUNCTION_NAME = "FUNCTIONID"
    VALUE_NAME = "VALUE"
    TIMES_INDEX_NAME = "TIMESINDEX"
    TABLE_NAME = "SIMULATIONRESULT"

    def __init__(
        self,
        conn,
        res_id=None,
        simulation_id=None,
        function_id=None,
        value=None,
        times_index=None,
        commit=False,
    ):
        # Constructor.
        # :param conn: the sqlite database connection
        # :type conn:
        # :param simulation_id: the simulation this result refers to
        # :type simulation_id: int
        # :param function_id: the function id for this simulation result
        # :type function_id: int
        # :param value: the value of the result
        # :type value: float
        # :param times_index: order of simulation result in time
        # :type times_index: int
        self.simulation_result_id = res_id
        self.simulation_id = simulation_id
        self.function_id = function_id
        self.value = value
        self.times_index = times_index
        if commit:
            # save it to the database
            sql = (
                "INSERT INTO {table} ({simulation}, {function}, {value}, "
                "{times_index}) VALUES (?,?,?,?)".format(
                    simulation=self.SIMULATION_NAME,
                    function=self.FUNCTION_NAME,
                    value=self.VALUE_NAME,
                    times_index=self.TIMES_INDEX_NAME,
                    table=self.TABLE_NAME,
                )
            )
            cursor = conn.cursor()
            cursor.execute(sql, (simulation_id, function_id, value, int(times_index)))
            self.simulation_result_id = cursor.lastrowid
            conn.commit()

    def __repr__(self):
        sim_res = (
            "simulationId: {simulation}, "
            "functionId: {function}, "
            "value: {value}, "
            "timesIndex: {times_index}".format(
                simulation=self.simulation_id,
                function=self.function_id,
                value=self.value,
                times_index=self.times_index,
            )
        )
        return sim_res

    @classmethod
    def create_or_get_existing(
        cls, conn, simulation_id, function_id, value=None, times_index=None
    ):
        try:
            return cls.get(conn, simulation_id, function_id)
        except ObjectNotFoundError:
            return SimulationResult(
                conn,
                simulation_id=simulation_id,
                function_id=function_id,
                value=value,
                times_index=times_index,
                commit=True,
            )

    @classmethod
    def get(cls, conn, simulation_id, function_id):
        sql = "SELECT * FROM {table} " "WHERE {simulation}=? AND {function}=?".format(
            simulation=cls.SIMULATION_NAME,
            function=cls.FUNCTION_NAME,
            table=cls.TABLE_NAME,
        )
        cursor = conn.cursor()
        cursor.execute(sql, (simulation_id, function_id))
        row = cursor.fetchone()
        if row is None:
            raise ObjectNotFoundError(
                "No SimulationResult found with the given parameters"
            )
        return SimulationResult(conn, *row)

    @classmethod
    def get_all(cls, conn):
        sql = "SELECT * FROM {table} ".format(table=cls.TABLE_NAME)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [SimulationResult(conn, *row) for row in rows]
        return result

    @classmethod
    def get_for_simulation(cls, conn, simulation_id):
        sql = "SELECT * FROM {table} " "WHERE {simulation}=?".format(
            simulation=cls.SIMULATION_NAME, table=cls.TABLE_NAME
        )
        cursor = conn.cursor()
        cursor.execute(sql, (simulation_id,))
        rows = cursor.fetchall()
        result = [SimulationResult(conn, *row) for row in rows]
        return result

    @classmethod
    def get_for_function(cls, conn, function_id):
        sql = (
            "SELECT * FROM {table} "
            "WHERE {function}=? ORDER BY {simulation}".format(
                simulation=cls.SIMULATION_NAME,
                function=cls.FUNCTION_NAME,
                table=cls.TABLE_NAME,
            )
        )
        cursor = conn.cursor()
        cursor.execute(sql, (function_id,))
        rows = cursor.fetchall()
        result = [SimulationResult(conn, *row) for row in rows]
        return result

    def save(self, conn):
        # saves the current status of the instance to the database
        sql = (
            "UPDATE {table} SET {simulation}=?, {function}=?,"
            " {value}=?, {times_index}=? WHERE {id}=?".format(
                id=self.ID_NAME,
                simulation=self.SIMULATION_NAME,
                function=self.FUNCTION_NAME,
                value=self.VALUE_NAME,
                times_index=self.TIMES_INDEX_NAME,
                table=self.TABLE_NAME,
            )
        )
        cursor = conn.cursor()
        cursor.execute(
            sql,
            (
                self.simulation_id,
                self.function_id,
                self.value,
                self.times_index,
                self.simulation_result_id,
            ),
        )
        conn.commit()
