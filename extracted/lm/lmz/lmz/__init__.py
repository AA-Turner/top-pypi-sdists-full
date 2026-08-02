from itertools import zip_longest
from functools import partial, reduce
import operator

def Map(*x,**y):
    f = partial(x[0],**y)
    if len(x) == 2:
        return rawMap(f,x[1])
    else:
        return rawMap(f,*x[1:])

def rawMap(*x,**y):
     return list(map(*x))

def Zip(*x,**y):
    return list(zip(*x,**y))

def Filter(*x,**y):
    return list(filter(*x,**y))

def grouper(iterable, n, fillvalue=None, list_no_fill=False):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    if list_no_fill:
        return [iterable[i:i + n] for i in range(0, len(iterable), n)]
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def Grouper(*x,**y):
    return list(grouper(*x,**y))


def iterselect(iterable, n):
    while n>0:
        next(iterable)
        n-=1
    return next(iterable)



def Flatten(li):
    return reduce(operator.iconcat, li, [])

def Range(*x):
    loi = lambda y: y if isinstance(y,int) else len(y)
    return list(range(*map(loi,x)))

def Transpose(x):
    return list(zip(*x))
