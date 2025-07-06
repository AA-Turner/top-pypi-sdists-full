import ast
import click


class PythonLiteralOption(click.Option):

    def type_cast_value(self, ctx, value):
        try:
            if value is None:
                return None
            if isinstance(value, list) and not value:
                return []
            if isinstance(value, dict) and not value:
                return {}
            return ast.literal_eval(value)
        except Exception:
            raise click.BadParameter(value)
