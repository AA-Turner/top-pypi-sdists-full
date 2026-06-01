"""Hook implementation modules for the Strands integration.

Each submodule holds the body of one or more StrandsHandler hook methods as
module-level free functions, taking the StrandsHandler instance as the first
argument. This keeps handler.py at a manageable size while keeping all hook
state on a single ``StrandsHandler`` object (Strands' hook system requires
exactly one provider).
"""
