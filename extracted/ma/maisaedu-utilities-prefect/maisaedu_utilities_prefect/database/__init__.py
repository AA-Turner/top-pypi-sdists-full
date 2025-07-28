import re

def detect_sql_injection(input):
    if not input or not isinstance(input, str):
        return input

    sql_patterns = [
        r"(--|\#|\/\*)",  # Comments SQL
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC|UNION|GRANT|REVOKE|TRUNCATE)\b)",  # Danger Commands SQL
        r"(\b(OR|AND)\b\s*\d?\s*=\s*\d?)",  # Conditions booleans like OR 1=1
        r"(\bUNION\b.*\bSELECT\b)",  # Attacks like UNION SELECT
        r"('.+--)",  # "" before comments""
        r"([\"']\s*OR\s*[\"']?\d+=[\"']?\d+)",  # Injection OR '1'='1'
        r"(\bEXEC\s*\()",  # Remote execution
    ]

    normalized_string = input.lower().strip()

    for pattern in sql_patterns:
        if re.search(pattern, normalized_string, re.IGNORECASE):
            raise ValueError("SQL Injection detected")
        
    return input