# Bug in Python 3.6 and 3.7 was getting comma before **kw

def fn(arg: int, *, kwarg='test', **kw) -> None:
    assert arg == 1
    assert kwarg == 'testing'
    assert kw['foo'] == 'bar'


fn(1, kwarg='testing', foo='bar')
