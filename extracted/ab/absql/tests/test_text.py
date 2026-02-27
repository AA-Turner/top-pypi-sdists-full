from absql.text import clean_spacing, create_replacements, flatten_inputs


def test_clean_spaces():
    text = "{{   hello  }}   world"
    got = clean_spacing(text)
    want = "{{ hello }}   world"
    assert got == want


def test_clean_spaces_2():
    want = "{{ hello }}   world"

    text = "{{hello }}   world"
    got = clean_spacing(text)
    assert got == want

    text = "{{ hello}}   world"
    got = clean_spacing(text)
    assert got == want


def test_clean_tabs():
    text = "{{  hello   }}   world"
    got = clean_spacing(text)
    want = "{{ hello }}   world"
    assert got == want


def test_replacements():
    got = create_replacements(foo="bar")
    want = {"{{foo}}": "bar", "{{ foo }}": "bar"}
    assert got == want


def test_flatten_inputs_flat():
    got = flatten_inputs(a="1", b="2")
    assert got == {"a": "1", "b": "2"}


def test_flatten_inputs_nested():
    got = flatten_inputs(config={"table": "my_table", "schema": "public"})
    assert got == {"config.table": "my_table", "config.schema": "public"}


def test_flatten_inputs_deeply_nested():
    got = flatten_inputs(a={"b": {"c": "deep"}})
    assert got == {"a.b.c": "deep"}


def test_flatten_inputs_empty():
    got = flatten_inputs()
    assert got == {}


def test_flatten_inputs_mixed():
    got = flatten_inputs(top="value", nested={"key": "val"})
    assert got == {"top": "value", "nested.key": "val"}
