###############################################################################
# (c) Copyright 2023 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from sqlalchemy import JSON
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression


class json_group_array(expression.FunctionElement):
    """Aggregate function that returns a JSON array comprised of all values in the aggregation.

    Provides compatibility between different database engines for performing JSON aggregation.
    See ``sqlite``'s ``json_group_array`` for details.
    """

    type = JSON()
    inherit_cache = True


@compiles(json_group_array, "mysql")
def mysql_json_group_array(element, compiler, **kw):
    if len(element.clauses) != 1:
        raise ValueError("json_group_array requires 1 argument")
    return f"json_arrayagg({compiler.process(element.clauses, **kw)})"


@compiles(json_group_array, "sqlite")
def sqlite_json_group_array(element, compiler, **kw):
    if len(element.clauses) != 1:
        raise ValueError("json_group_array requires 1 arguments")
    return f"json_group_array({compiler.process(element.clauses, **kw)})"


class json_group_object(expression.FunctionElement):
    """Aggregate function that returns a JSON object comprised of all name/value pairs in the aggregation.

    Provides compatibility between different database engines for performing JSON aggregation.
    See ``sqlite``'s ``json_group_object`` for details.
    """

    type = JSON()
    inherit_cache = True


@compiles(json_group_object, "mysql")
def mysql_json_group_object(element, compiler, **kw):
    if len(element.clauses) != 2:
        raise ValueError("json_group_object requires 2 arguments")
    return f"json_objectagg({compiler.process(element.clauses, **kw)})"


@compiles(json_group_object, "sqlite")
def sqlite_json_group_object(element, compiler, **kw):
    if len(element.clauses) != 2:
        raise ValueError("json_group_object requires 2 arguments")
    return f"json_group_object({compiler.process(element.clauses, **kw)})"


class json_length(expression.FunctionElement):
    """Function that returns a JSON array length.

    Provides compatibility between different database engines.
    """

    type = JSON()
    inherit_cache = True


@compiles(json_length, "mysql")
def mysql_json_length(element, compiler, **kw):
    if len(element.clauses) != 1:
        raise ValueError("json_length requires 1 argument")
    return f"json_length({compiler.process(element.clauses, **kw)})"


@compiles(json_length, "sqlite")
def sqlite_json_length(element, compiler, **kw):
    if len(element.clauses) != 1:
        raise ValueError("json_length requires 1 arguments")
    return f"json_array_length({compiler.process(element.clauses, **kw)})"
