
def identity(f):
    return f


@identity
def fefe(x):
    ...
    ...
    ...
    ...
    raise Exception("fefe")


def fifi(x):
    raise Exception("fifi")


def fofo(x):
    return fifi(x + 4)


def fafa(x):
    raise Exception("fafa")


def fufu(x):
    return fofo(x + 5)
