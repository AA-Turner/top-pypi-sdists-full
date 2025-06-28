"""
Generates JSON schema from introspection. Use `make generate`.
"""

import json

from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.introspection import query, variables
from sgqlc.introspection.__main__ import get_arg_parse
from vars import ensure_token_env_vars

if __name__ == "__main__":
    api_id, api_token = ensure_token_env_vars()
    args = get_arg_parse().parse_args()

    headers = {"x-mcd-id": api_id, "x-mcd-token": api_token}
    endpoint = RequestsEndpoint(url=args.url, base_headers=headers)
    data = endpoint(query, variables(include_description=True, include_deprecated=True))
    if "headers" in data:
        del data["headers"]

    if data.get("errors"):
        raise SystemExit(f"Failed to retrieve schema with - {data.get('errors')}")
    json.dump(data, args.outfile, sort_keys=True, indent=2, default=str)
