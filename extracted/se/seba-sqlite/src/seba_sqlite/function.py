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


class Function:
    ID_NAME = "ID"
    NAME_NAME = "NAME"
    EXPERIMENT_NAME = "EXPERIMENTID"
    WEIGHT_NAME = "WEIGHT"
    NORMALIZATION_NAME = "NORMALIZATION"
    TYPE_NAME = "TYPE"
    RIGHTHANDSIDE_NAME = "RIGHTHANDSIDE"
    CONSTRAINTTYPE_NAME = "CONSTRAINTTYPE"
    TABLE_NAME = "FUNCTION"

    FUNCTION_CONSTRAINT_TYPE = "CONSTRAINT"
    FUNCTION_OBJECTIVE_TYPE = "OBJECTIVE"

    def __init__(
        self,
        conn,
        function_id=None,
        name=None,
        experiment_id=None,
        weight=1.0,
        normalization=1.0,
        function_type=None,
        rhs_value=0.0,
        constraint_type=None,
        commit=False,
    ):
        # Constructor.
        # :param conn: the sqlite database connection
        # :type conn:
        # :param function_id: id of the function to load, if this is a new function
        # set it to None
        # :type function_id: int
        # :param name: the name of the function
        # :type name: str
        # :param experiment_id: the id of the experiment this function is used in
        # :type experiment_id: int
        # :param weight: the weight of the function
        # :type weight: float
        # :param normalization: the normalization of the function
        # :type normalization: float
        # :param rhs_value: the rhs_value of the function
        # :type rhs_value: float
        # :param function_type: the type of the function
        # :type function_type: str
        # :param constraint_type: the constraint_type of the function
        # :type constraint_type: str
        self.function_id = function_id
        self.name = name
        self.experimentid = experiment_id
        self.weight = weight
        self.normalization = normalization
        self.function_type = function_type
        self.rhs_value = rhs_value
        self.constraint_type = constraint_type
        if commit:
            # save it to the database

            sql = (
                "INSERT INTO {table} ({name}, {experiment}, {weight}, "
                "{normalization}, {type}, "
                "{rhs_value}, {constrainttype})  VALUES (?,?,?,?,?,?,?)".format(
                    name=self.NAME_NAME,
                    experiment=self.EXPERIMENT_NAME,
                    weight=self.WEIGHT_NAME,
                    normalization=self.NORMALIZATION_NAME,
                    type=self.TYPE_NAME,
                    rhs_value=self.RIGHTHANDSIDE_NAME,
                    constrainttype=self.CONSTRAINTTYPE_NAME,
                    table=self.TABLE_NAME,
                )
            )

            cursor = conn.cursor()
            cursor.execute(
                sql,
                (
                    self.name,
                    self.experimentid,
                    self.weight,
                    self.normalization,
                    self.function_type,
                    self.rhs_value,
                    self.constraint_type,
                ),
            )
            self.function_id = cursor.lastrowid
            conn.commit()

    def __repr__(self):
        func = (
            "functionId: {id}, "
            "name: {name}, "
            "experimentId: {experiment}, "
            "weight: {weight}, "
            "normalization: {normalization}, "
            "functionType: {type}, "
            "righthandside: {rhs_value}, "
            "constraintType: {constrainttype}".format(
                id=self.function_id,
                name=self.name,
                experiment=self.experimentid,
                weight=self.weight,
                normalization=self.normalization,
                type=self.function_type,
                rhs_value=self.rhs_value,
                constrainttype=self.constraint_type,
            )
        )
        return func

    @classmethod
    def create_or_get_existing(
        cls,
        conn,
        function_id=None,
        name=None,
        experiment_id=None,
        function_type=None,
        weight=1.0,
        normalization=1.0,
        rhs_value=0.0,
        constraint_type=None,
    ):
        creation_data = not None in (function_type, name, experiment_id)
        if function_id or (
            name is not None and experiment_id is not None and not creation_data
        ):
            return cls.get(conn, function_id, name, experiment_id)
        if creation_data:
            return Function(
                conn,
                name=name,
                experiment_id=experiment_id,
                function_type=function_type,
                weight=weight,
                normalization=normalization,
                rhs_value=rhs_value,
                constraint_type=constraint_type,
                commit=True,
            )
        return None

    @classmethod
    def get(cls, conn, function_id=None, name=None, experiment_id=None):
        first_sql = "SELECT * FROM {table} WHERE ".format(table=cls.TABLE_NAME)
        cursor = conn.cursor()
        if function_id is not None:
            sql = first_sql + "{id}=?".format(id=cls.ID_NAME)
            sql_arguments = (function_id,)
        elif name is not None and experiment_id is not None:
            sql = first_sql + "{name}=? AND {experiment}=?".format(
                name=cls.NAME_NAME, experiment=cls.EXPERIMENT_NAME
            )
            sql_arguments = (name, experiment_id)
        else:
            raise ObjectNotFoundError("Function can not be found with the given data")
        cursor.execute(sql, sql_arguments)
        row = cursor.fetchone()
        if row is None:
            raise ObjectNotFoundError("Function can not be found")
        return Function(conn, *row)

    @classmethod
    def get_all_by_type(cls, conn, function_type):
        sql = "SELECT * FROM {table} WHERE {type}=?".format(
            type=cls.TYPE_NAME, table=cls.TABLE_NAME
        )
        if function_type not in [
            cls.FUNCTION_CONSTRAINT_TYPE,
            cls.FUNCTION_OBJECTIVE_TYPE,
        ]:
            raise ValueError("Invalid Function Type")
        cursor = conn.cursor()
        cursor.execute(sql, (function_type,))
        rows = cursor.fetchall()
        result = [Function(conn, *row) for row in rows]
        return result
