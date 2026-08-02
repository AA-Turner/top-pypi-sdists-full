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


class CalculationResult:
    """
    storing values per a variable state X and the functions that evaluates or
    measures such state
    """

    ID_NAME = "ID"
    BATCH_NAME = "BATCHID"
    SET_NAME = "SETID"
    VALUE_NAME = "VALUE"
    MERIT_NAME = "MERITFNVALUE"
    IMPROVED_FLAG_NAME = "IMPROVEDFLAG"
    TABLE_NAME = "CALCULATIONRESULT"

    def __init__(
        self,
        conn,
        calc_res_id=None,
        batch_id=None,
        set_id=None,
        object_function_value=None,
        merit_function_value=None,
        improved_flag=False,
        commit=False,
    ):
        # Constructor.
        # :param conn: the sqlite database connection
        # :type conn:
        # :param calc_res_id: last id of the entry
        # :type calc_res_id:  int
        # :param batch_id: the batch this result belongs to
        # :type batch_id: int
        # :param set_id: set the results refers
        # :type set_id: int
        # :param object_function_value: averaged objectives over realizations
        # :type object_function_value: float
        # :param merit_function_value: merit function value of the current
        # simulation state
        # :type merit_function_value: float
        # :param improved_flag: True if the merit function has been only improving
        # recently
        # :type improved_flag: Boolean
        self.calculation_result_id = calc_res_id
        self.batch_id = batch_id
        self.set_id = set_id
        self.object_function_value = object_function_value
        self.merit_function_value = merit_function_value
        self.improved_flag = improved_flag

        if commit:
            # save it to the database
            sql = (
                "INSERT INTO {table} ({batch}, {set}, {objfnvalue}, "
                "{meritvalue}, {improvedflag}) VALUES (?,?,?,?,?)".format(
                    batch=self.BATCH_NAME,
                    set=self.SET_NAME,
                    objfnvalue=self.VALUE_NAME,
                    meritvalue=self.MERIT_NAME,
                    improvedflag=self.IMPROVED_FLAG_NAME,
                    table=self.TABLE_NAME,
                )
            )
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (
                    batch_id,
                    set_id,
                    object_function_value,
                    merit_function_value,
                    improved_flag,
                ),
            )
            self.calculation_result_id = cursor.lastrowid
            conn.commit()

    def __repr__(self):
        eval_res = (
            "batchId: {batch}, "
            "setId: {set}, "
            "avgFnValue: {objfnvalue}, "
            "meritFnValue: {meritvalue}, "
            "improvedFlag: {improvedflag}".format(
                batch=self.batch_id,
                set=self.set_id,
                objfnvalue=self.object_function_value,
                meritvalue=self.merit_function_value,
                improvedflag=self.improved_flag,
            )
        )
        return eval_res

    @classmethod
    def create_or_get_existing(
        cls,
        conn,
        batch_id,
        set_id,
        object_function_value=None,
        merit_function_value=None,
        improved_flag=False,
    ):
        try:
            return cls.get(conn, batch_id, set_id)
        except ObjectNotFoundError:
            return CalculationResult(
                conn,
                batch_id=batch_id,
                set_id=set_id,
                object_function_value=object_function_value,
                merit_function_value=merit_function_value,
                improved_flag=improved_flag,
                commit=True,
            )

    @classmethod
    def get(cls, conn, batch_id, set_id):
        sql = "SELECT * FROM {table} WHERE {batch}=? AND {set}=?".format(
            batch=cls.BATCH_NAME, set=cls.SET_NAME, table=cls.TABLE_NAME
        )
        cursor = conn.cursor()
        cursor.execute(sql, (batch_id, set_id))
        row = cursor.fetchone()
        if row is None:
            raise ObjectNotFoundError(
                "No evaluationResult found with the given parameters"
            )
        return CalculationResult(conn, *row)

    @classmethod
    def get_for_batch(cls, conn, batch_id):
        sql = "SELECT * FROM {table} WHERE {batch}=?".format(
            batch=cls.BATCH_NAME, table=cls.TABLE_NAME
        )
        cursor = conn.cursor()
        cursor.execute(sql, (batch_id,))
        rows = cursor.fetchall()
        return [CalculationResult(conn, *row) for row in rows]

    @classmethod
    def get_for_id(cls, conn, result_id):
        sql = "SELECT * FROM {table} WHERE {result_id}=?".format(
            result_id=cls.ID_NAME, table=cls.TABLE_NAME
        )
        cursor = conn.cursor()
        cursor.execute(sql, (result_id,))
        rows = cursor.fetchall()
        result = [CalculationResult(conn, *row) for row in rows]
        return result

    @classmethod
    def get_for_set(cls, conn, set_id):
        sql = "SELECT * FROM {table} WHERE {set}=?".format(
            set=cls.SET_NAME, table=cls.TABLE_NAME
        )
        cursor = conn.cursor()
        cursor.execute(sql, (set_id,))
        rows = cursor.fetchall()
        if not rows:
            raise ObjectNotFoundError(
                "No evaluationResult found with the given parameters"
            )
        return [CalculationResult(conn, *row) for row in rows]

    @classmethod
    def get_all(cls, conn):
        sql = "SELECT * FROM {table} ".format(table=cls.TABLE_NAME)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [CalculationResult(conn, *row) for row in rows]
        return result

    def save(self, conn):
        # saves the current status of the instance to the database
        sql = (
            "UPDATE {table} SET {batch}=?, {set}=?,"
            " {objfnvalue}=?, {meritvalue}=?, {improvedflag}=? WHERE {id}=?".format(
                id=self.ID_NAME,
                batch=self.BATCH_NAME,
                set=self.SET_NAME,
                objfnvalue=self.VALUE_NAME,
                meritvalue=self.MERIT_NAME,
                improvedflag=self.IMPROVED_FLAG_NAME,
                table=self.TABLE_NAME,
            )
        )
        cursor = conn.cursor()
        cursor.execute(
            sql,
            (
                self.batch_id,
                self.set_id,
                self.object_function_value,
                self.merit_function_value,
                self.improved_flag,
                self.calculation_result_id,
            ),
        )
        conn.commit()
