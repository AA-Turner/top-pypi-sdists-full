from math import inf

import lmfit

from bec_lib.lmfit_serializer import deserialize_param_object, serialize_lmfit_params


def test_serialize_lmfit_params():
    params = lmfit.Parameters()
    params.add("a", value=1.0, vary=True)
    params.add("b", value=2.0, vary=False)
    result = serialize_lmfit_params(params)
    assert result == {
        "a": {
            "name": "a",
            "value": 1.0,
            "vary": True,
            "min": -inf,
            "max": inf,
            "expr": None,
            "brute_step": None,
        },
        "b": {
            "name": "b",
            "value": 2.0,
            "vary": False,
            "min": -inf,
            "max": inf,
            "expr": None,
            "brute_step": None,
        },
    }

    obj = deserialize_param_object(result)
    assert obj == params
