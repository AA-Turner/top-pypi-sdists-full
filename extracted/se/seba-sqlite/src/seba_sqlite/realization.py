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


class Realization:
    ID_NAME = "ID"
    NAME_NAME = "NAME"
    EXPERIMENT_NAME = "EXPERIMENTID"
    TABLE_NAME = "REALIZATION"
    WEIGHT_NAME = "WEIGHT"

    def __init__(
        self,
        conn,
        realization_id=None,
        name=None,
        experiment_id=None,
        weight=None,
        commit=False,
    ):
        # Constructor.
        # :param conn: the sqlite database connection
        # :type conn:
        # :param realization_id: id of the realization to load, if this is a new
        # realization set it to None
        # :type realization_id: int or None
        # :param name: the name of the realization
        # :type name: str or None
        # :param experiment_id: the experiment id of the experiment in which this
        # realization is used in
        # :type experiment_id: int or None
        self.realization_id = realization_id
        self.name = name
        self.experiment_id = experiment_id
        self.weight = weight

        if commit:
            sql = (
                "INSERT INTO {table} ({experiment}, {name}, {weight}) VALUES (?,"
                "?,?)".format(
                    experiment=self.EXPERIMENT_NAME,
                    name=self.NAME_NAME,
                    weight=self.WEIGHT_NAME,
                    table=self.TABLE_NAME,
                )
            )
            cursor = conn.cursor()
            cursor.execute(sql, (self.experiment_id, self.name, self.weight))
            self.realization_id = cursor.lastrowid
            conn.commit()

    def __repr__(self):
        realization = (
            "realizationId: {id}, "
            "name: {name}, "
            "experimentId: {exp}, "
            "weight: {weight}".format(
                id=self.realization_id,
                name=self.name,
                exp=self.experiment_id,
                weight=self.weight,
            )
        )
        return realization

    @classmethod
    def create_or_get_existing(
        cls, conn, realization_id=None, name=None, experiment_id=None, weight=None
    ):
        try:
            return cls.get(conn, realization_id, name, experiment_id)
        except ObjectNotFoundError:
            return Realization(
                conn,
                realization_id=realization_id,
                name=name,
                experiment_id=experiment_id,
                weight=weight,
                commit=True,
            )
        except ValueError as value_error:
            raise value_error

    @classmethod
    def get(cls, conn, realization_id=None, name=None, experiment_id=None):
        first_part = "SELECT * FROM {table} WHERE ".format(table=cls.TABLE_NAME)

        if realization_id:
            sql = first_part + "{id}=?".format(id=cls.ID_NAME)
            sql_param = (realization_id,)
        elif name and experiment_id:
            sql = first_part + "{name}=? AND {experiment}=?".format(
                name=cls.NAME_NAME, experiment=cls.EXPERIMENT_NAME
            )
            sql_param = (name, experiment_id)
        else:
            raise ValueError(
                "A realization should be instantiated either with an id or a name"
            )
        cursor = conn.cursor()
        cursor.execute(sql, sql_param)
        row = cursor.fetchone()
        if row is None:
            raise ObjectNotFoundError("Realization with given parameters not found")
        return Realization(conn, *row)

    @classmethod
    def get_all(cls, conn):
        sql = "SELECT * FROM {table}".format(table=cls.TABLE_NAME)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [Realization(conn, *row) for row in rows]
        return result
