import os
import re

def _extract_method_body_static(source: str, method_name: str) -> str:
    pattern = rf'(?:public|private|protected)[^{{]*{re.escape(method_name)}\s*\([^)]*\)\s*(?:throws[^{{]*)?\{{'
    match = re.search(pattern, source)
    if not match:
        return ""
    start = match.end()
    depth = 1
    i = start
    while i < len(source) and depth > 0:
        if source[i] == '{':
            depth += 1
        elif source[i] == '}':
            depth -= 1
        i += 1
    return source[start:i - 1]