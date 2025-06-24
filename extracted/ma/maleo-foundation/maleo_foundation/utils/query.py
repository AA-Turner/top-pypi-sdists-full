from sqlalchemy import Column, Table
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Query, Session, aliased
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.expression import or_, asc, cast, desc
from sqlalchemy.types import DATE, String, TEXT, TIMESTAMP
from typing import Type
from maleo_foundation.types import BaseTypes
from maleo_foundation.extended_types import ExtendedTypes

class BaseQueryUtils:
    @staticmethod
    def filter_column(
        query: Query,
        table: Type[DeclarativeMeta],
        column: str,
        value: BaseTypes.OptionalAny = None,
        include_null: bool = False
    ) -> Query:
        column_attr = getattr(table, column, None)
        if column_attr is None or not isinstance(column_attr, InstrumentedAttribute):
            return query

        value_filters = []
        if value is not None:
            value_filters.extend([column_attr == val for val in value])

        if value_filters:
            if include_null:
                value_filters.append(column_attr.is_(None))
            query = query.filter(or_(*value_filters))

        return query

    @staticmethod
    def filter_ids(
        query: Query,
        table: Type[DeclarativeMeta],
        column: str,
        ids: BaseTypes.OptionalListOfIntegers = None,
        include_null: bool = False
    ) -> Query:
        column_attr = getattr(table, column, None)
        if column_attr is None or not isinstance(column_attr, InstrumentedAttribute):
            return query

        id_filters = []
        if ids is not None:
            id_filters.extend([column_attr == id for id in ids])

        if id_filters:
            if include_null:
                id_filters.append(column_attr.is_(None))
            query = query.filter(or_(*id_filters))

        return query

    @staticmethod
    def filter_timestamps(
        query: Query,
        table: Type[DeclarativeMeta],
        date_filters: ExtendedTypes.ListOfDateFilters
    ) -> Query:
        if date_filters and len(date_filters) > 0:
            for date_filter in date_filters:
                try:
                    table:Table = table.__table__
                    column:Column = table.columns[date_filter.name]
                    column_attr:InstrumentedAttribute = getattr(table, date_filter.name)
                    if isinstance(column.type, (TIMESTAMP, DATE)):
                        if date_filter.from_date and date_filter.to_date:
                            query = query.filter(
                                column_attr.between(
                                    date_filter.from_date,
                                    date_filter.to_date
                                )
                            )
                        elif date_filter.from_date:
                            query = query.filter(column_attr >= date_filter.from_date)
                        elif date_filter.to_date:
                            query = query.filter(column_attr <= date_filter.to_date)
                except KeyError:
                    continue
        return query

    @staticmethod
    def filter_statuses(
        query: Query,
        table: Type[DeclarativeMeta],
        statuses: BaseTypes.OptionalListOfStatuses
    ) -> Query:
        if statuses is not None:
            status_filters = [table.status == status for status in statuses]
            query = query.filter(or_(*status_filters))
        return query

    @staticmethod
    def filter_is_root(
        query: Query,
        table: Type[DeclarativeMeta],
        parent_column: str = "parent_id",
        is_root: BaseTypes.OptionalBoolean=None
    ) -> Query:
        parent_attr = getattr(table, parent_column, None)
        if parent_attr is None or not isinstance(parent_attr, InstrumentedAttribute):
            return query
        if is_root is not None:
            query = query.filter(parent_attr.is_(None) if is_root else parent_attr.is_not(None))
        return query

    @staticmethod
    def filter_is_parent(
        session: Session,
        query: Query,
        table: Type[DeclarativeMeta],
        id_column: str = "id",
        parent_column: str = "parent_id",
        is_parent: BaseTypes.OptionalBoolean = None
    ) -> Query:
        id_attr = getattr(table, id_column, None)
        if id_attr is None or not isinstance(id_attr, InstrumentedAttribute):
            return query
        parent_attr = getattr(table, parent_column, None)
        if parent_attr is None or not isinstance(parent_attr, InstrumentedAttribute):
            return query
        if is_parent is not None:
            child_table = aliased(table)
            child_parent_attr = getattr(child_table, parent_column)
            subq = session.query(child_table).filter(child_parent_attr == id_attr).exists()
            query = query.filter(subq if is_parent else ~subq)
        return query

    @staticmethod
    def filter_is_child(
        query: Query,
        table: Type[DeclarativeMeta],
        parent_column: str = "parent_id",
        is_child: BaseTypes.OptionalBoolean = None
    ) -> Query:
        parent_attr = getattr(table, parent_column, None)
        if parent_attr is None or not isinstance(parent_attr, InstrumentedAttribute):
            return query
        if is_child is not None:
            query = query.filter(parent_attr.is_not(None) if is_child else parent_attr.is_(None))
        return query

    @staticmethod
    def filter_is_leaf(
        session: Session,
        query: Query,
        table: Type[DeclarativeMeta],
        id_column: str = "id",
        parent_column: str = "parent_id",
        is_leaf: BaseTypes.OptionalBoolean = None
    ) -> Query:
        id_attr = getattr(table, id_column, None)
        if id_attr is None or not isinstance(id_attr, InstrumentedAttribute):
            return query
        parent_attr = getattr(table, parent_column, None)
        if parent_attr is None or not isinstance(parent_attr, InstrumentedAttribute):
            return query
        if is_leaf is not None:
            child_table = aliased(table)
            child_parent_attr = getattr(child_table, parent_column)
            subq = session.query(child_table).filter(child_parent_attr == id_attr).exists()
            query = query.filter(~subq if is_leaf else subq)
        return query

    @staticmethod
    def filter_search(
        query: Query,
        table: Type[DeclarativeMeta],
        search: BaseTypes.OptionalString
    ) -> Query:
        if search:
            search_term = f"%{search}%" #* Use wildcard for partial matching
            search_filters = []
            sqla_table:Table = table.__table__
            for name, attr in vars(table).items():
                try:
                    column: Column = sqla_table.columns[name]
                    if not isinstance(attr, InstrumentedAttribute):
                        continue
                    if isinstance(column.type, (String, TEXT)):
                        search_filters.append(cast(attr, TEXT).ilike(search_term))
                except KeyError:
                    continue
            if search_filters:
                query = query.filter(or_(*search_filters))
        return query


    @staticmethod
    def sort(
        query: Query,
        table: Type[DeclarativeMeta],
        sort_columns: ExtendedTypes.ListOfSortColumns
    ) -> Query:
        for sort_column in sort_columns:
            try:
                sort_col = getattr(table, sort_column.name)
                sort_col = asc(sort_col) if sort_column.order.value.lower() == "asc" else desc(sort_col)
                query = query.order_by(sort_col)
            except AttributeError:
                continue
        return query

    @staticmethod
    def paginate(
        query: Query,
        page: int,
        limit: int
    ) -> Query:
        offset: int = int((page - 1) * limit) #* Calculate offset based on page
        query = query.limit(limit=limit).offset(offset=offset)
        return query