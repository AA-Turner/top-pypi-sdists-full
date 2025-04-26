import typing as t
from functools import reduce

from sqlalchemy import false, true  # type: ignore
from sqlalchemy.orm.query import Query  # type: ignore

from taktile_auth.entities.role import Role
from taktile_auth.enums import Action


def _map_and_filter(
    input_: t.Dict[str, t.Any], map_: t.Dict[str, str]
) -> t.Dict[str, t.Any]:
    """
    Mapping the keys of dictionary input_, ignoring keys that are not mentioned

    {"a": "b", "c": "d"} x {"a": "e"} -> {"e": "b"}
    """
    return {v: input_[k] for k, v in map_.items()}


def _to_sql_stmt(model: t.Any, key: str, value: str) -> t.Any:
    if "*" not in value:
        return getattr(model, key) == value
    elif value == "*":
        return true()


def to_sqlalchemy_filter(
    *,
    roles: t.List[Role],
    resource_name: str,
    action: Action,
    mappings: t.Dict[str, str],
) -> t.Callable[[t.Any, t.Any], t.Any]:
    """to_sqlalchemy_filter.

    Parameters
    ----------
    roles : t.List[Role]
        roles that the user has
    resource_name : str
        resource_name of the resource we try to filter for
    mappings : t.Dict[str, str]
        mapping of the names in the roles.yaml file to table column name. If a
        name is not mentioned as a key, it is not part of the query.

    Returns
    -------
    t.Callable[[t.Any, t.Any], t.Any]

    """

    all_permissions = [
        perm for role in roles for perm in role.get_all_permissions()
    ]

    filtered_permissions = [
        perm
        for perm in all_permissions
        if perm.resource_name == resource_name and action in perm.actions
    ]

    filtering_parameters = [
        _map_and_filter(perm.resource.dict(), mappings)
        for perm in filtered_permissions
    ]

    def func(model: t.Any, query: Query) -> Query:
        queries = [
            [_to_sql_stmt(model, k, v) for k, v in iden.items()]
            for iden in filtering_parameters
        ]

        inner_stmts = [
            reduce(lambda x, y: x & y, query, true()) for query in queries
        ]

        stmt = reduce(lambda x, y: x | y, inner_stmts, false())

        return query.filter(stmt)

    return func
