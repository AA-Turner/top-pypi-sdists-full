import sys

try:
    from contextlib import GeneratorContextManager
except ImportError:
    class GeneratorContextManager(object):
        """Compatibility shim to provide a python27-like interface to contextlib"""

        def __init__(self, gen):
            self.gen = gen

        def __enter__(self):
            try:
                return self.gen.__next__()
            except StopIteration:
                raise RuntimeError("generator didn't yield")

        def __exit__(self, type, value, traceback):
            if type is None:
                try:
                    self.gen.__next__()
                except StopIteration:
                    return
                else:
                    raise RuntimeError("generator didn't stop")
            else:
                if value is None:
                    # Need to force instantiation so we can reliably
                    # tell if we get the same exception back
                    value = type()
                try:
                    self.gen.throw(type, value, traceback)
                    raise RuntimeError("generator didn't stop after throw()")
                except StopIteration as exc:
                    # Suppress the exception *unless* it's the same exception that
                    # was passed to throw().  This prevents a StopIteration
                    # raised inside the "with" statement from being suppressed
                    return exc is not value
                except:
                    # only re-raise if it's *not* the exception that was
                    # passed to throw(), because __exit__() must not raise
                    # an exception unless __exit__() itself failed.  But throw()
                    # has to raise the exception to signal propagation, so this
                    # fixes the impedance mismatch between the throw() protocol
                    # and the __exit__() protocol.
                    #
                    if sys.exc_info()[1] is not value:
                        raise
