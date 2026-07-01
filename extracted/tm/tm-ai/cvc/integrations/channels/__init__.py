"""Built-in CVC channel adapters.

All adapters live next to this file. They are NOT imported eagerly — the
bootstrap layer imports only the ones the user has configured. This
keeps install footprint tight and lets CVC ship channels whose SDKs
aren't installed without breaking import of the rest of CVC.
"""
