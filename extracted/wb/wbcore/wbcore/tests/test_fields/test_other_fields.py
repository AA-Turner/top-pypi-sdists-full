from wbcore.serializers import RangeSelectField, StarRatingField


class TestStarRatingField:
    def setup_method(self):
        self.field = StarRatingField()

    def test_not_none(self):
        assert self.field is not None

    def test_field_type(self):
        assert self.field.field_type == "starrating"

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == (
            "field_name",
            {
                "key": "field_name",
                "label": None,
                "type": self.field.field_type,
                "required": True,
                "read_only": False,
                "precision": 0,
                "max_digits": 34,
                "decorators": [],
                "depends_on": [],
                "display_mode": "decimal",
                "signed": True,
                "disable_formatting": True,
            },
        )


class TestRangeSelectField:
    def setup_method(self):
        self.field = RangeSelectField()

    def test_not_none(self):
        assert self.field is not None

    def test_field_type(self):
        assert self.field.field_type == "rangeselect"

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == (
            "field_name",
            {
                "key": "field_name",
                "label": None,
                "type": self.field.field_type,
                "required": True,
                "read_only": False,
                "color": self.field.color,
                "decorators": [],
                "depends_on": [],
                "start": self.field.start,
                "end": self.field.end,
                "step_size": self.field.step_size,
            },
        )
