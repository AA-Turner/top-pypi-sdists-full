from kirin.prelude import basic_no_opt


@basic_no_opt
def setindex(a):
    a[1] = 2
    return a


@basic_no_opt
def index(a):
    return a[1]


# TODO: actually test the lowered code
def test_index():
    index.code.print()
    setindex.code.print()
