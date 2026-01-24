import jinja2


class KeepPlaceholderUndefined(jinja2.Undefined):
    """
    Custom Jinja2 Undefined class that preserves undefined variables
    in the rendered output using placeholder syntax.

    Instead of replacing undefined variables with an empty string or raising
    an error, this class returns the variable name wrapped in delimiters,
    matching the environment's variable start and end strings.

    This is useful for:
      - Debugging template output with missing variables.
      - Partial rendering where some variables are intentionally left unresolved.
    """

    def __str__(self) -> str:
        # single-brace style, to match your custom delimiters
        return f'{{{self._undefined_name}}}'


#: Custom Jinja2 environment tailored for safe and partial rendering of docstring templates.
jinja_env: jinja2.Environment = jinja2.Environment(
    variable_start_string='{',
    variable_end_string='}',
    autoescape=True,  # ruff S701
    undefined=KeepPlaceholderUndefined,
)
