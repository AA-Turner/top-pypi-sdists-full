"""Environment variable management.

Exposes the environment-aware CLI surfaces under ``pysae-ai-tools env``:

- ``env resolve`` — resolve env vars (per environment) from AWS Secrets Manager
  or shell auto-commands
- ``env activate`` — load an environment's vars into the current shell under
  their usual names
- ``env list`` — list every supported variable and how it resolves

Raw, environment-agnostic secret read/write lives in ``pysae-ai-tools secrets``.
The shared secret store (:mod:`pysae_ai_tools.env.secret_store`) backs both.
"""
