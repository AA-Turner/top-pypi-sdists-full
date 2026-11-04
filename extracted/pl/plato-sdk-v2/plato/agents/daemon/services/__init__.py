"""Daemon service modules.

Each exposes ``register(app, ctx)`` adding its routes and appending its
capability names to ``ctx.capabilities``. ``app.py`` composes them.
"""
