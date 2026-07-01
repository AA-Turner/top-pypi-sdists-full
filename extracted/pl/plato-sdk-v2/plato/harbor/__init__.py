"""Plato integration for the Harbor agent-evaluation framework.

This subpackage provides a Harbor ``BaseEnvironment`` implementation backed by a
Plato computer-use VM. It is intentionally *not* imported by the top-level
``plato`` package: ``import plato`` must never require Harbor (which targets
Python 3.12+, while the SDK supports 3.11+).

Harbor is an optional, externally-installed dependency. Install it yourself
(``pip install harbor`` / ``uv pip install harbor``, Python 3.12+), then point
Harbor at the provider via::

    harbor run ... \\
        --environment-import-path plato.harbor.environment:PlatoEnvironment

Only ``plato.harbor.environment`` imports Harbor; ``plato.harbor._shell`` is a
pure-Python helper module with no Harbor dependency.
"""
