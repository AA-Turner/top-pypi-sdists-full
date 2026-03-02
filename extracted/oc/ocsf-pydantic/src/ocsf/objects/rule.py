from ._entity import Entity


class Rule(Entity):
    """
    The Rule object describes characteristics of a rule associated with a policy or
    an event.
    """

    # Optional:
    category: str | None = None # The rule category.
    desc: str | None = None # The description of the rule that generated the event.
    name: str | None = None # The name of the rule that generated the event.
    type: str | None = None # The rule type.
    uid: str | None = None # The unique identifier of the rule that generated the event.
    version: str | None = None # The rule version. For example: `1.1`.
