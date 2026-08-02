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


class ControlDefinition:
    ID_NAME = "ID"
    NAME_NAME = "NAME"
    EXPERIMENT_NAME = "EXPERIMENTID"
    INITIAL_VALUE_NAME = "INITIALVALUE"
    MIN_VALUE_NAME = "MINVALUE"
    MAX_VALUE_NAME = "MAXVALUE"
    TABLE_NAME = "CONTROLDEFINITION"

    def __init__(
        self,
        conn,
        control_id=None,
        experiment_id=None,
        name=None,
        initial_value=None,
        min_value=None,
        max_value=None,
        commit=False,
    ):
        # Constructor.
        # :param conn: the sqlite database connection
        # :type conn:
        # :param control_id: int specifying the id of the control in the database,
        # If new control object: None
        # :type control_id: int
        # :param name: specifying the name of the control as set in the
        # configuration of the experiment
        # :type name: str or None
        # :param experiment_id: the experiment this control belongs to
        # :type experiment_id: int or None
        # :param initial_value: specifying the initial value of the control
        # :type initial_value: float or None
        # :param min_value: float specifying the minimum  value of the control
        # :type min_value: float or None
        # :param max_value: float specifying the maximum value of the control
        # :type max_value: float or None
        self.control_id = control_id
        self.experiment_id = experiment_id
        self.name = name
        self.initial_value = initial_value
        self.min_value = min_value
        self.max_value = max_value
        # save it to the database
        if commit:
            sql = (
                "INSERT INTO {table} ({experiment}, {name}, {init_val}, "
                "{min_val}, {max_val}) "
                "VALUES (?,?,?,?,?)".format(
                    name=self.NAME_NAME,
                    experiment=self.EXPERIMENT_NAME,
                    init_val=self.INITIAL_VALUE_NAME,
                    min_val=self.MIN_VALUE_NAME,
                    max_val=self.MAX_VALUE_NAME,
                    table=self.TABLE_NAME,
                )
            )
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (
                    self.experiment_id,
                    self.name,
                    self.initial_value,
                    self.min_value,
                    self.max_value,
                ),
            )
            self.control_id = cursor.lastrowid
            conn.commit()

    def __repr__(self):
        control = (
            "controlDefinitionId: {id}, "
            "experimentId: {experiment}, "
            "name: {name}, "
            "initialValue: {init}, "
            "minValue: {min}, "
            "maxValue: {max}".format(
                id=self.control_id,
                experiment=self.experiment_id,
                name=self.name,
                init=self.initial_value,
                min=self.min_value,
                max=self.max_value,
            )
        )

        return control

    @classmethod
    def create_or_get_existing(
        cls,
        conn,
        name=None,
        experiment_id=None,
        initial_value=None,
        min_value=None,
        max_value=None,
        control_id=None,
    ):
        create = not None in (experiment_id, name, initial_value, min_value, max_value)
        if create:
            return ControlDefinition(
                conn,
                name=name,
                experiment_id=experiment_id,
                initial_value=initial_value,
                min_value=min_value,
                max_value=max_value,
                commit=True,
            )
        try:
            return cls.get(
                conn, control_id=control_id, experiment_id=experiment_id, name=name
            )
        except ObjectNotFoundError as onf:
            raise onf

    @classmethod
    def get(cls, conn, control_id=None, experiment_id=None, name=None):
        first_part = "SELECT * FROM {table} WHERE ".format(table=cls.TABLE_NAME)
        if control_id is not None:
            sql = first_part + "{id}=?".format(id=cls.ID_NAME)
            sql_params = (control_id,)
        elif experiment_id is not None and name is not None:
            sql = first_part + "{name}=? AND {experiment}=?".format(
                name=cls.NAME_NAME, experiment=cls.EXPERIMENT_NAME
            )
            sql_params = (name, experiment_id)
        else:
            raise ValueError("Not enough information to load a control definition")
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        row = cursor.fetchone()
        if row is None:
            raise ObjectNotFoundError
        return ControlDefinition(conn, *row)

    @classmethod
    def get_all(cls, conn):
        sql = "SELECT * FROM {table} ".format(table=cls.TABLE_NAME)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [ControlDefinition(conn, *row) for row in rows]
        return result
