from .models.basic import BasicExample

instance = BasicExample.objects.create(
    txt_enum=BasicExample.TextEnum.VALUE1,
    int_enum=3  # by-value assignment also works
)

assert instance.txt_enum is BasicExample.TextEnum('V1')
if instance.txt_enum is not None:
    assert instance.txt_enum.value == 'V1'
    assert instance.txt_enum.label == 'Value 1'

assert instance.int_enum is BasicExample.IntEnum.THREE
assert instance.int_enum.value == 3
assert instance.int_enum.label == 'Three'
