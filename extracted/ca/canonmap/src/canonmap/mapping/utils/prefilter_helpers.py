"""
Helper functions for creating prefilter SQL queries from lists and other data structures.
"""

from typing import List, Optional, Union


def create_prefilter_with_list(
    table_name: str, 
    field_name: str, 
    values_list: List[str], 
    operator: str = "IN"
) -> str:
    """
    Create a prefilter SQL query that filters by a list of values.
    
    Args:
        table_name: The table to query
        field_name: The field to filter on
        values_list: List of values to filter for
        operator: SQL operator ('IN', 'NOT IN', 'LIKE')
    
    Returns:
        SQL string for prefiltering
        
    Examples:
        >>> create_prefilter_with_list("users", "name", ["John", "Jane"], "IN")
        "SELECT * FROM users WHERE name IN ('John', 'Jane')"
        
        >>> create_prefilter_with_list("users", "name", ["john", "jane"], "LIKE")
        "SELECT * FROM users WHERE name LIKE '%john%' OR name LIKE '%jane%'"
        
        >>> create_prefilter_with_list("users", "department", ["temp", "test"], "NOT IN")
        "SELECT * FROM users WHERE department NOT IN ('temp', 'test')"
    """
    if not values_list:
        return f"SELECT * FROM {table_name}"
    
    if operator.upper() in ["IN", "NOT IN"]:
        # For IN/NOT IN operators, create comma-separated quoted list
        values_str = "', '".join(str(v) for v in values_list)
        return f"SELECT * FROM {table_name} WHERE {field_name} {operator} ('{values_str}')"
    
    elif operator.upper() == "LIKE":
        # For LIKE operator, create OR conditions
        like_conditions = " OR ".join([f"{field_name} LIKE '%{v}%'" for v in values_list])
        return f"SELECT * FROM {table_name} WHERE {like_conditions}"
    
    else:
        raise ValueError(f"Unsupported operator: {operator}. Supported operators: 'IN', 'NOT IN', 'LIKE'")


def create_prefilter_with_multiple_lists(
    table_name: str,
    filters: List[tuple[str, str, List[str], str]],
    additional_conditions: Optional[str] = None
) -> str:
    """
    Create a prefilter SQL query with multiple list-based filters.
    
    Args:
        table_name: The table to query
        filters: List of tuples (field_name, operator, values_list, logical_operator)
                logical_operator can be 'AND' or 'OR'
        additional_conditions: Additional SQL conditions to append
        
    Returns:
        SQL string for prefiltering
        
    Examples:
        >>> filters = [
        ...     ("status", "IN", ["active", "pending"], "AND"),
        ...     ("department", "IN", ["engineering", "sales"], "AND"),
        ...     ("country", "IN", ["US", "CA"], "OR")
        ... ]
        >>> create_prefilter_with_multiple_lists("users", filters, "created_date >= '2023-01-01'")
    """
    if not filters:
        base_sql = f"SELECT * FROM {table_name}"
        if additional_conditions:
            return f"{base_sql} WHERE {additional_conditions}"
        return base_sql
    
    conditions = []
    
    for field_name, operator, values_list, logical_op in filters:
        if not values_list:
            continue
            
        if operator.upper() in ["IN", "NOT IN"]:
            values_str = "', '".join(str(v) for v in values_list)
            condition = f"{field_name} {operator} ('{values_str}')"
        elif operator.upper() == "LIKE":
            like_conditions = " OR ".join([f"{field_name} LIKE '%{v}%'" for v in values_list])
            condition = f"({like_conditions})"
        else:
            raise ValueError(f"Unsupported operator: {operator}")
        
        conditions.append(condition)
    
    if not conditions:
        base_sql = f"SELECT * FROM {table_name}"
        if additional_conditions:
            return f"{base_sql} WHERE {additional_conditions}"
        return base_sql
    
    # Join conditions with the specified logical operators
    where_clause = conditions[0]
    for i, (_, _, _, logical_op) in enumerate(filters[1:], 1):
        if i < len(conditions):
            where_clause += f" {logical_op} {conditions[i]}"
    
    sql = f"SELECT * FROM {table_name} WHERE {where_clause}"
    
    if additional_conditions:
        sql += f" AND {additional_conditions}"
    
    return sql


def create_prefilter_with_date_range(
    table_name: str,
    date_field: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    additional_filters: Optional[List[tuple[str, str, List[str], str]]] = None
) -> str:
    """
    Create a prefilter SQL query with date range filtering.
    
    Args:
        table_name: The table to query
        date_field: The date field to filter on
        start_date: Start date (inclusive) in 'YYYY-MM-DD' format
        end_date: End date (inclusive) in 'YYYY-MM-DD' format
        additional_filters: Additional list-based filters
        
    Returns:
        SQL string for prefiltering
        
    Examples:
        >>> create_prefilter_with_date_range("users", "created_date", "2023-01-01", "2023-12-31")
        "SELECT * FROM users WHERE created_date >= '2023-01-01' AND created_date <= '2023-12-31'"
    """
    date_conditions = []
    
    if start_date:
        date_conditions.append(f"{date_field} >= '{start_date}'")
    
    if end_date:
        date_conditions.append(f"{date_field} <= '{end_date}'")
    
    if additional_filters:
        additional_sql = create_prefilter_with_multiple_lists(table_name, additional_filters)
        # Extract the WHERE clause from the additional SQL
        if "WHERE" in additional_sql:
            where_part = additional_sql.split("WHERE", 1)[1]
            date_conditions.append(where_part)
    
    if not date_conditions:
        return f"SELECT * FROM {table_name}"
    
    where_clause = " AND ".join(date_conditions)
    return f"SELECT * FROM {table_name} WHERE {where_clause}"


def create_prefilter_with_joins(
    base_table: str,
    joins: List[tuple[str, str, str, str]],  # (table, condition, join_type)
    filters: Optional[List[tuple[str, str, List[str], str]]] = None,
    additional_conditions: Optional[str] = None
) -> str:
    """
    Create a prefilter SQL query with table joins.
    
    Args:
        base_table: The main table to query
        joins: List of join tuples (table, condition, join_type)
        filters: List-based filters to apply
        additional_conditions: Additional SQL conditions
        
    Returns:
        SQL string for prefiltering
        
    Examples:
        >>> joins = [
        ...     ("user_permissions", "users.id = user_permissions.user_id", "INNER"),
        ...     ("departments", "users.dept_id = departments.id", "LEFT")
        ... ]
        >>> filters = [("user_permissions.permission_level", "IN", ["2", "3"], "AND")]
        >>> create_prefilter_with_joins("users", joins, filters)
    """
    sql = f"SELECT {base_table}.* FROM {base_table}"
    
    # Add joins
    for table, condition, join_type in joins:
        sql += f" {join_type} JOIN {table} ON {condition}"
    
    # Add filters
    if filters:
        filter_sql = create_prefilter_with_multiple_lists("", filters)
        if "WHERE" in filter_sql:
            where_clause = filter_sql.split("WHERE", 1)[1]
            sql += f" WHERE {where_clause}"
    
    # Add additional conditions
    if additional_conditions:
        if "WHERE" in sql:
            sql += f" AND {additional_conditions}"
        else:
            sql += f" WHERE {additional_conditions}"
    
    return sql
