import re
from core.indexer import CodeIndex
from core.extract_method_body_static import _extract_method_body_static

def trace_endpoint(index: CodeIndex, path: str) -> str:
    """
    Given an endpoint path (e.g. /api/v1/bank/transactions), trace the full call chain:
    Controller method → Interface -> Service calls → Repository calls
    """
    matches = [
        ep for ep in index.endpoints
        if path.lower() in ep.path.lower() or ep.path.lower() in path.lower()
    ]

    if not matches:
        return f"No endpoint found matching '{path}'.\nAvailable paths:\n" + \
               "\n".join(f"  [{ep.http_method}] {ep.path}" for ep in index.endpoints)

    output = []
    for ep in matches:
        output.append(f"[{ep.http_method}] {ep.path}")
        output.append(f"  Controller : {ep.controller_class}.{ep.method_name}()")
        output.append(f"  File       : {ep.file_path}:{ep.line_number}")

        source = index.file_contents.get(ep.file_path, "")
        method_body = _extract_method_body_static(source, ep.method_name)

        if method_body:
            service_calls = re.findall(r'(\w+(?:Service|Manager))\.\s*(\w+)\s*\(', method_body)
            if service_calls:
                output.append("  Service calls:")
                for svc, method in service_calls:
                    output.append(f"    → {svc}.{method}()")

                    svc_class_name = svc[0].upper() + svc[1:]
                    svc_info = index.classes.get(svc_class_name)
                    if svc_info:
                        svc_source = index.file_contents.get(svc_info.file_path, "")
                        svc_body = _extract_method_body_static(svc_source, method)
                        if svc_body:
                            repo_calls = re.findall(r'(\w+(?:Repository|Repo))\.\s*(\w+)\s*\(', svc_body)
                            for repo, repo_method in repo_calls:
                                output.append(f"       → {repo}.{repo_method}() [repository]")

            return_match = re.search(r'return\s+(.*?);', method_body)
            if return_match:
                output.append(f"  Returns    : {return_match.group(1).strip()}")

        output.append("")

    return "\n".join(output)