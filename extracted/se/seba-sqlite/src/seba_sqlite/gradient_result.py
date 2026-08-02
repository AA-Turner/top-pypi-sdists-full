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


class GradientResult:
    ID_NAME = "ID"
    BATCH_NAME = "BATCHID"
    FUNCTION_NAME = "FUNCTIONID"
    VALUE_NAME = "VALUE"
    IS_SUCCESS_NAME = "SUCCESS"
    CONTROL_NAME = "CONTROLID"
    TABLE_NAME = "GRADIENTRESULT"

    def __init__(
        self,
        conn,
        gradient_result_id=None,
        batch_id=None,
        function_id=None,
        control_definition_id=None,
        value=None,
        success=None,
        commit=False,
    ):
        # Constructor.
        # :param conn: the sqlite database connection
        # :type conn:
        # :param batch_id: the batch this result refers to
        # :type batch_id: int
        # :param function_id: the function for this result
        # :type function_id: int
        # :param control_definition_id: the control definition for this result
        # :type control_definition_id: int
        # :param value: the value of the gradient
        # :type value: float
        # :param success: was the simulation a success
        # :type success: int [0|1]
        self.gradient_result_id = gradient_result_id
        self.batch_id = batch_id
        self.value = value
        self.function_id = function_id
        self.success = success
        self.control_definition_id = control_definition_id

        if commit:
            # save it to the database
            cursor = conn.cursor()
            sql = (
                "INSERT INTO {table} ({batch}, "
                "{function}, {control}, "
                "{value}, {success}) \
                  VALUES (?,?,?,?,?)".format(
                    batch=self.BATCH_NAME,
                    function=self.FUNCTION_NAME,
                    control=self.CONTROL_NAME,
                    value=self.VALUE_NAME,
                    success=self.IS_SUCCESS_NAME,
                    table=self.TABLE_NAME,
                )
            )
            cursor.execute(
                sql,
                (
                    self.batch_id,
                    self.function_id,
                    self.control_definition_id,
                    self.value,
                    int(self.success),
                ),
            )
            self.gradient_result_id = cursor.lastrowid
            conn.commit()

    def __repr__(self):
        gradient = (
            "gradientResultId: {id}, "
            "batchId: {batch}, "
            "functionId: {function}, "
            "controlDefinitionId: {control}, "
            "value: {value}, "
            "success: {success}".format(
                id=self.gradient_result_id,
                batch=self.batch_id,
                function=self.function_id,
                control=self.control_definition_id,
                value=self.value,
                success=self.success,
            )
        )
        return gradient

    @classmethod
    def get_update_or_create(
        cls, conn, batch_id, function_id, control_definition_id, gradient_value, success
    ):
        try:
            return cls.get(conn, batch_id, function_id, control_definition_id).update(
                conn, gradient_value, success
            )
        except ObjectNotFoundError:
            return GradientResult(
                conn,
                batch_id=batch_id,
                function_id=function_id,
                control_definition_id=control_definition_id,
                value=gradient_value,
                success=success,
                commit=True,
            )

    @classmethod
    def get(cls, conn, batch, function, control):
        sql = (
            "SELECT {id} ,{batch}, {function}, {control}, {value}, "
            "{success} FROM {table} "
            "WHERE {batch}=? AND {function}=? AND {control}=?".format(
                id=cls.ID_NAME,
                batch=cls.BATCH_NAME,
                function=cls.FUNCTION_NAME,
                value=cls.VALUE_NAME,
                success=cls.IS_SUCCESS_NAME,
                control=cls.CONTROL_NAME,
                table=cls.TABLE_NAME,
            )
        )
        cursor = conn.cursor()
        cursor.execute(sql, (batch, function, control))
        row = cursor.fetchone()
        if row is None:
            raise ObjectNotFoundError
        return GradientResult(conn, *row)

    @classmethod
    def get_all(cls, conn):
        sql = (
            "SELECT {id} ,{batch}, {function}, {control}, {value}, "
            "{success} FROM {table}".format(
                id=cls.ID_NAME,
                batch=cls.BATCH_NAME,
                function=cls.FUNCTION_NAME,
                value=cls.VALUE_NAME,
                success=cls.IS_SUCCESS_NAME,
                control=cls.CONTROL_NAME,
                table=cls.TABLE_NAME,
            )
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [GradientResult(conn, *row) for row in rows]
        return result

    @classmethod
    def get_for_batch_id(cls, conn, batch_id):
        sql = (
            "SELECT {id} ,{batch}, {function}, {control}, {value}, {success}"
            " FROM {table} WHERE {batch}=?".format(
                id=cls.ID_NAME,
                batch=cls.BATCH_NAME,
                function=cls.FUNCTION_NAME,
                success=cls.IS_SUCCESS_NAME,
                control=cls.CONTROL_NAME,
                value=cls.VALUE_NAME,
                table=cls.TABLE_NAME,
            )
        )
        cursor = conn.cursor()
        cursor.execute(sql, (batch_id,))
        rows = cursor.fetchall()
        result = [GradientResult(conn, *row) for row in rows]
        return result

    def update(self, conn, value=None, success=None):
        sql = "UPDATE {table} SET {value}=?, {success}=? WHERE \
               {batch}=? AND {function}=? AND {control}=?".format(
            value=self.VALUE_NAME,
            success=self.IS_SUCCESS_NAME,
            batch=self.BATCH_NAME,
            function=self.FUNCTION_NAME,
            control=self.CONTROL_NAME,
            table=self.TABLE_NAME,
        )
        cupdate = conn.cursor()
        cupdate.execute(
            sql,
            (
                value,
                int(success),
                self.batch_id,
                self.function_id,
                self.control_definition_id,
            ),
        )
        conn.commit()
        self.gradient_result_id = value
        self.success = success
