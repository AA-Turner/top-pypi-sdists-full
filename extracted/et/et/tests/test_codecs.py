import et.codecs


tests = [
    {
        "data": 0,
        "e_data": {
            1: b'\x00\x010',
            2: b'\x00\x02x\x9c3\x00\x00\x001\x001'
        }
    },

    {
        "data": {},
        "e_data": {
            1: b'\x00\x01{}',
            2: b'\x00\x02x\x9c\xab\xae\x05\x00\x01u\x00\xf9'
        }
    },

]


def test_all():
    for test in tests:
        for fmt in sorted(test["e_data"].keys()):
            assert test["e_data"][fmt] == et.codecs.encode(test["data"], fmt)
            assert (test["data"], fmt) == et.codecs.decode(test["e_data"][fmt])
