from wbcore.serializers.fields.text import CharField


# TODO: Color for each state
class FSMStatusField(CharField):
    field_type = "status"

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        read_only = kwargs.pop("read_only", True)
        super().__init__(*args, read_only=read_only, **kwargs)

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        representation["choices"] = list()

        for choice in self.choices:
            representation["choices"].append({"value": choice[0], "label": choice[1]})

        return key, representation
