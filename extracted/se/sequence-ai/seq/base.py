"""
`seq.Policy` — the base class a user's policy subclasses.

WHY a base class at all (it is deliberately empty for S1): it is the DX anchor the templates and docs show
(`class Pi05(seq.Policy)`), it gives type checkers a nominal type for a policy, and it is where shared
runtime helpers (obs decode, chunk assembly) will live once the container harness (C-series) needs them.
For S1 (authoring + registry only) it carries no behaviour — a policy is identified by its `@seq.policy`
decoration, not by subclassing, so subclassing is a convention, not a requirement.


"""
from __future__ import annotations


class Policy:
    """Base class for a robot policy. Subclass it and decorate with `@seq.policy(...)`."""
