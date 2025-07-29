import re
import functools
import inspect
from typing import Any, Callable, Dict, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])

def detect_sql_injection(input):
    if input is None:
        return input

    # If it's a string, use it directly
    if isinstance(input, str):
        input_str = input
    # If it's an array (list, tuple, set), convert to string
    elif isinstance(input, (list, tuple, set)):
        input_str = str(input)
    # If it's a dictionary (object), convert to string
    elif isinstance(input, dict):
        input_str = str(input)
    # If it's any other type, return without checking
    else:
        return input

    sql_patterns = [
        r"(--|\#|\/\*)",  # SQL Comments
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC|UNION|GRANT|REVOKE|TRUNCATE)\b)",  # Dangerous SQL Commands
        r"(\b(OR|AND)\b\s*\d?\s*=\s*\d?)",  # Boolean conditions like OR 1=1
        r"(\bUNION\b.*\bSELECT\b)",  # UNION SELECT attacks
        r"('.+--)",  # Quote before comments
        r"([\"']\s*OR\s*[\"']?\d+=[\"']?\d+)",  # Injection pattern like OR '1'='1'
        r"(\bEXEC\s*\()",  # Remote code execution
    ]

    normalized_string = input_str.lower().strip()

    for pattern in sql_patterns:
        if re.search(pattern, normalized_string, re.IGNORECASE):
            raise ValueError("SQL Injection detected")
        
    return input


def flow_detect_sql_injection(func: F) -> F:
    """
    Decorator that checks all function parameters for SQL injection attacks.
    
    Args:
        func: The function to be decorated
        
    Returns:
        The decorated function with SQL injection validation
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check positional args
        for arg in args:
            detect_sql_injection(arg)
        
        # Check named kwargs
        for value in kwargs.values():
            detect_sql_injection(value)
            
        # Execute the original function
        return func(*args, **kwargs)
        
    return cast(F, wrapper)