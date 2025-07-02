def top():
    test()

def test():
    raise Exception("foo")


try:
    top()
except Exception as exc:
    raise exc#.with_traceback()# exc.__traceback__.tb_next)
    raise
