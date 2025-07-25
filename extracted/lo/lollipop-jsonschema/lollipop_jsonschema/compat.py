import sys

PY2 = int(sys.version_info[0]) == 2

if PY2:
    def itervalues(d):
        return d.itervalues()

    def iteritems(d):
        return d.iteritems()
else:
    def itervalues(d):
        return d.values()

    def iteritems(d):
        return d.items()
