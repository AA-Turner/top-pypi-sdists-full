'Print given config (with optional path in config) as shell snippet.'
from .functions import OpaqueKey
from .model import Boolean, Entry, Locator, Number, Text
from .scope import Scope, StaticScope
import os, shlex, sys

def _configpath(configname):
    if os.sep in configname:
        return configname
    for parent in os.environ['PATH'].split(os.pathsep):
        path = os.path.join(parent, configname)
        if os.path.exists(path):
            return path
    raise Exception(f"Not found: {configname}")

def _bashforeval(scope):
    return ''.join(f"{name}={obj.tobash()}\n" for name, obj in scope.resolveditems())

def _scopetobash(self, toplevel = False):
    if toplevel:
        return _bashforeval(self)
    d = dict(self.resolveditems())
    if all(map(OpaqueKey.isopaque, d)):
        return f"({' '.join(x.tobash() for x in d.values())})"
    return shlex.quote(_bashforeval(self))

Scope.tobash = _scopetobash
Boolean.tobash = lambda self, toplevel: 'true' if self.booleanvalue else 'false'
Number.tobash = lambda self: str(self.numbervalue)
Text.tobash = lambda self: shlex.quote(self.textvalue)

def main():
    scope = StaticScope.createchild()
    Locator(_configpath(sys.argv[1])).source(scope, Entry([]))
    sys.stdout.write(scope.resolved(*sys.argv[2:]).tobash(True))

if '__main__' == __name__:
    main()
