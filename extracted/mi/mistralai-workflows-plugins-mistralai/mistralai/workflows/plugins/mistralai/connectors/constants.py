# Top-level key in plugin_metadata and extensions
MISTRALAI_PLUGIN_KEY = "mistralai"
# Sub-key within the mistralai namespace for caller-supplied runtime bindings
CONNECTORS_KEY = "connectors"
# Resolved bindings live under a separate key so they aren't re-read as caller input
# when extensions propagate to continued/child workflows.
RESOLVED_CONNECTORS_KEY = "resolved_connectors"
