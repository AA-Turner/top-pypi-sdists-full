# From Python 3.6 hmac.py
# needed to change mklambda rule
def __init__(self, msg = None, digestmod = None) -> None:
    self.digest_cons = lambda d='': digestmod.new(d)

# From Python 3.6 functools.py
# Bug was handling lambda for MAKE_FUNCTION_8 (closure)
# vs to MAKE_FUNCTION_9 (pos_args + closure)
def bug() -> None:
    def register(cls, func=None):
        return lambda f: register(cls, f)

# From Python 3.6 configparser.py
def items(self, d, section: int=5, raw: bool=False, vars=None) -> None:
    if vars:
        for key, value in vars.items():
            d[self.optionxform(key)] = value
    d = lambda option: self._interpolation.before_get(self,
        section, option, d[option], d)
    return
