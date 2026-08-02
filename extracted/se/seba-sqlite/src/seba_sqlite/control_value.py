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


class ControlValue:
    CONTROL_DEFINITION_NAME = "controlDefinitionId"
    SET_ID_NAME = "SETID"
    VALUE_NAME = "VALUE"
    TABLE_NAME = "CONTROLVALUE"

    def __init__(self, conn, set_id, control_definition_id, value, commit=False):
        # The class "constructor" - It's actually an initializer
        # :param conn: the sqlite database connection
        # :type conn:
        # :param set_id: set the controlvalue refers to
        # :type set_id: int
        # :param control_definition_id: controlDefinition the controlvalue refers to
        # :type control_definition_id: int
        # :param value: the value
        # :type value: float
        self.set_id = set_id
        self.control_definition_id = control_definition_id
        self.value = value
        if commit:
            # save it to the database
            sql = (
                "INSERT INTO {table} ({set}, {control}, {value}) "
                "VALUES (?,?,?)".format(
                    set=self.SET_ID_NAME,
                    control=self.CONTROL_DEFINITION_NAME,
                    value=self.VALUE_NAME,
                    table=self.TABLE_NAME,
                )
            )
            cursor = conn.cursor()
            cursor.execute(sql, (self.set_id, self.control_definition_id, self.value))
            conn.commit()

    def __repr__(self):
        control = (
            "controlDefinitionId: {control}, "
            "setId: {set}, "
            "value: {value}".format(
                control=self.control_definition_id, set=self.set_id, value=self.value
            )
        )
        return control

    @classmethod
    def create_or_get_existing(cls, conn, set_id, control_definition_id, value=None):
        try:
            return cls.get(conn, set_id, control_definition_id)
        except ObjectNotFoundError:
            return ControlValue(
                conn,
                set_id=set_id,
                control_definition_id=control_definition_id,
                value=value,
                commit=True,
            )

    @classmethod
    def get(cls, conn, set_id, control_definition_id):
        sql = "SELECT * FROM {table} WHERE {control_def}=? AND {set}=?".format(
            control_def=cls.CONTROL_DEFINITION_NAME,
            set=cls.SET_ID_NAME,
            table=cls.TABLE_NAME,
        )
        cursor = conn.cursor()
        cursor.execute(sql, (control_definition_id, set_id))
        row = cursor.fetchone()
        if row is not None:
            ControlValue(conn, *row)
        else:
            raise ObjectNotFoundError(
                "Control Value not existing for control "
                "definition {} and set {}".format(control_definition_id, set_id)
            )

    @classmethod
    def get_all(cls, conn):
        sql = "SELECT * FROM {table} ".format(table=cls.TABLE_NAME)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [ControlValue(conn, *row) for row in rows]
        return result

    @classmethod
    def get_for_set(cls, conn, set_id):
        sql = "SELECT * FROM {table} WHERE {set}=?".format(
            set=cls.SET_ID_NAME, table=cls.TABLE_NAME
        )
        cursor = conn.cursor()
        cursor.execute(sql, (set_id,))
        rows = cursor.fetchall()
        result = [ControlValue(conn, *row) for row in rows]
        return result
