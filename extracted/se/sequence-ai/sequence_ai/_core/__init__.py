"""
Shared internals every surface (act / chat / decide) builds on: the HTTP transport,
the catalogue lookup + `Model` row, the response envelope, and image encoding. Nothing here is
specific to one endpoint; per-endpoint code lives in the sibling packages.
"""
