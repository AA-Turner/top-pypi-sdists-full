from rapidpe_rift_pipe import modules

def test_placeholder():
    assert True


def test_convert_list_string_to_dict():
    test_cases = [
        ("[x=y,a=b]", {"x": "y", "a": "b"}),
        ("[x=1,a=b]", {"x": "1", "a": "b"}),
#        ("[]", {}),
    ]

    for list_string, dct in test_cases:
        assert modules.convert_list_string_to_dict(list_string) == dct
