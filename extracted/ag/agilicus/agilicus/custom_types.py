import click

from datetime import timezone


class Ternary:
    true_val = 1
    false_val = 0
    clear_val = 2

    def __init__(self, value):
        self.value = value

    def is_true(self):
        return self.value == self.true_val

    def is_false(self):
        return self.value == self.false_val

    def is_clear(self):
        return self.value == self.clear_val

    def to_bool_or_none(self):
        if self.is_true():
            return True
        if self.is_false():
            return False
        if self.is_clear():
            return None


class TernaryParamType(click.types.BoolParamType):
    name = "ternary"
    CLEAR = "clear"
    CHOICES = "BOOL|clear"

    def convert(self, value, param, ctx):
        if value == self.CLEAR:
            return Ternary(Ternary.clear_val)
        try:
            if super().convert(value, param, ctx):
                return Ternary(Ternary.true_val)
            return Ternary(Ternary.false_val)
        except click.BadParameter:
            pass

        self.fail(f"{value!r} is not a valid bool or 'clear'")

    def to_info_dict(self):
        info_dict = super().to_info_dict()
        info_dict["choices"] = self.CHOICES
        return info_dict

    def get_metavar(self, param) -> str:
        return self.CHOICES


class DateTime(click.DateTime):
    def __init__(self, formats=None):
        super().__init__(formats)
        self.formats = list(self.formats)
        self.formats.append("%Y-%m-%dT%H:%M:%S%z")

    def convert(self, value, param, ctx):
        converted = super().convert(value, param, ctx)
        if converted is not None:
            return converted.astimezone(timezone.utc)
        return None
