"""The jinja rules plugin bundle."""

from collate_sqlfluff.core.plugin import hookimpl
from collate_sqlfluff.core.rules import BaseRule


@hookimpl
def get_rules() -> list[type[BaseRule]]:
    """Get plugin rules.

    NOTE: Rules are imported only on fetch to manage import times
    when rules aren't used.
    """
    from collate_sqlfluff.rules.jinja.JJ01 import Rule_JJ01

    return [Rule_JJ01]
