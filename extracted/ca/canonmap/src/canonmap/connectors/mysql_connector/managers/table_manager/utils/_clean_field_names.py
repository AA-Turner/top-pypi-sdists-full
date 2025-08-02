import re
from typing import Dict, Set

def clean_field_names(columns: list) -> Dict[str, str]:
    """
    Clean column names to be valid MySQL identifiers.
    
    Args:
        columns: List of original column names
        
    Returns:
        Dictionary mapping original column names to cleaned column names
    """
    col_name_map = {}
    used_names: Set[str] = set()
    
    # MySQL reserved words
    mysql_reserved = {
        "add", "all", "alter", "analyze", "and", "as", "asc", "between", "by", "create", "delete", "desc", "distinct",
        "drop", "exists", "from", "group", "having", "in", "index", "insert", "into", "join", "key", "like", "limit",
        "not", "null", "on", "or", "order", "outer", "select", "set", "table", "update", "union", "where"
    }
    
    for col in columns:
        col_clean = col.strip()
        col_clean = re.sub(r'[^0-9A-Za-z_]', '_', col_clean)
        if col_clean == '' or col_clean.isdigit() or re.match(r'^\d', col_clean):
            col_clean = 'col_' + col_clean
        col_clean = col_clean.lower()
        if col_clean in mysql_reserved:
            col_clean += "_col"
        if len(col_clean) > 64:
            col_clean = col_clean[:64]
        # Ensure uniqueness by appending a number if needed
        base_name = col_clean
        count = 1
        while col_clean in used_names:
            col_clean = f"{base_name}_{count}"
            count += 1
            if len(col_clean) > 64:
                # truncate base part if necessary to keep length ≤ 64
                trim_len = len(col_clean) - 64
                base_name = base_name[:-trim_len]
                col_clean = f"{base_name}_{count}"
        used_names.add(col_clean)
        col_name_map[col] = col_clean
    
    return col_name_map
