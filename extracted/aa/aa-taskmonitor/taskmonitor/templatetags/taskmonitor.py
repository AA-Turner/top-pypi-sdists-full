"""Template tags for Task Monitor."""

import random
import string

from django import template

register = template.Library()


@register.simple_tag
def random_id(size=8) -> str:
    """Generate random id."""
    return "id-" + "".join(random.choices(string.ascii_letters + string.digits, k=size))
