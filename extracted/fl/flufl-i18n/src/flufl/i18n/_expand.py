"""String interpolation."""

import logging

from string import Template

from public import public


log = logging.getLogger('flufl.i18n')


@public
def expand(
    template: str,
    substitutions: dict[str, str],
    template_class: type = Template,
) -> str:
    """Expand string template with substitutions.

    :param template: A PEP 292 $-string template.
    :param substitutions: The substitutions dictionary.
    :param template_class: The template class to use.
    :return: The substituted string.
    """
    try:
        # Do it this way to make the type checker and linter happy.
        # TRY300 Consider moving this statement to an `else` block
        expanded: str = template_class(template).safe_substitute(substitutions)
    except (TypeError, ValueError):
        # The template is really screwed up.
        log.exception('broken template: %s', template)
        raise
    else:
        return expanded
