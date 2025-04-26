
def identity(f):
    return f

@identity
def fafa(x):
    return x + 1

@identity
def fefe(x):
    return x + 2

def fifi(x):
    return x + 3

def fofo(x):
    return fifi(x + 4)

def fufu(x):
    return fofo(x + 5)
