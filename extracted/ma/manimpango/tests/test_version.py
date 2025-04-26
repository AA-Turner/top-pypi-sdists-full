# -*- coding: utf-8 -*-
def test_pango_version():
    import manimpango

    v = manimpango.pango_version()
    assert isinstance(v, str)


def test_cairo_version():
    import manimpango

    v = manimpango.cairo_version()
    assert isinstance(v, str)
