# `mistralai.workflows` is a PEP 420 namespace shared across several distributions
# (the core `mistralai-workflows` SDK, its plugins, and this worker client). Type
# checkers (pyright in particular) only merge submodules from a namespace into a
# *regular* package when every contributing root is itself a regular package, so
# this lightweight `__init__.py` exists to make `worker_client` resolvable from the
# core package's perspective. It deliberately does NOT import from the core SDK:
# this client is distributed standalone and must not depend on `mistralai-workflows`.
__path__ = __import__("pkgutil").extend_path(__path__, __name__)
