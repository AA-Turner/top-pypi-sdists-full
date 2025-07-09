# TODO: Most likely to be removed
from rest_framework import serializers

from .mixins import WBCoreSerializerFieldMixin
from .number import IntegerField


class StarRatingField(IntegerField):
    field_type = "starrating"
    disable_formatting = True


class EmojiRatingField(IntegerField):
    field_type = "emojirating"
    disable_formatting = True


class RangeSelectField(WBCoreSerializerFieldMixin, serializers.FloatField):
    field_type = "rangeselect"

    def __init__(self, *args, start: float = 0.0, end: float = 1.0, step_size: float = 0.25, **kwargs):
        self.color = kwargs.pop("color", "rgb(133, 144, 162)")
        self.start = start
        self.end = end
        self.step_size = step_size
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        representation["color"] = self.color
        representation["start"] = self.start
        representation["end"] = self.end
        representation["step_size"] = self.step_size
        return key, representation
