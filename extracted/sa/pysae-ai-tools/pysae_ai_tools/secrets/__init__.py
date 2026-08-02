"""Raw AWS Secrets Manager read/write commands (no environment notion).

Exposed as ``pysae-ai-tools secrets``. Unlike ``env resolve`` / ``env activate``
(which are environment-aware and map usual names per env), these commands operate
directly on a secret id — defaulting to the caller's private secret
``iam/<username>/private``.
"""
