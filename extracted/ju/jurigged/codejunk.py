# import gc
import importlib.util
import logging
import sys

# import time
# import types
# from collections import defaultdict
# from inspect import getattr_static
from _frozen_importlib_external import SourceFileLoader

# from .utils import EventSource


# ##########
# # CodeDB #
# ##########

# MAX_TIME = 0.1


log = logging.getLogger(__name__)


class ImportSniffer:
    """A spec finder that simply sniffs for attempted imports.

    Basically we install this at the front of sys.meta_path so that
    importlib.util.find_spec calls it, then we call find_spec
    ourselves to locate the file that's going to be read so that we
    know we have to cache its contents and watch for changes.
    """

    def __init__(self, report):
        self.working = False
        self.report = report

    def install(self):
        sys.meta_path.insert(0, self)

    def uninstall(self):
        sys.meta_path.remove(self)

    def find_module(self, spec, path):
        if not self.working:
            self.working = True
            # We call find_spec ourselves to find out where the file is.
            # This will not cause an infinite loop because self.working
            # is True and we will not enter the conditional. I'm not
            # sure if it's dangerous to call find_spec within find_spec,
            # but it seems to work, so whatever.
            mspec = importlib.util.find_spec(spec, path)
            if (
                mspec is not None
                and isinstance(mspec.loader, SourceFileLoader)
                and mspec.name is not None
                and mspec.origin is not None
            ):
                try:
                    self.report(mspec.name, mspec.origin)
                except Exception as exc:
                    log.error(
                        f"jurigged: Error processing spec {mspec.name}",
                        exc_info=exc,
                    )
            self.working = False
        return None


# def make_audithook(self):
#     def watch_exec(event, obj):  # pragma: no cover
#         # Note: Python does not trace audit hooks, so normal use will not show
#         # coverage of this function even if it is executed
#         if event == "exec":
#             (code,) = obj
#             self.assimilate(code)
#         elif event == "import":
#             (module_name, filename, *_) = obj
#             self.register_filename(filename, module_name)

#     # The closure is faster than a method on _CodeDB
#     return watch_exec


# class _CodeDB:
#     def __init__(self):
#         self.codes = {}
#         self.functions = defaultdict(set)
#         self.last_cost = 0
#         self.always_use_cache = False
#         self.filename_to_module = {}
#         self.module_activity = EventSource()

#     def setup(self):
#         self.collect_all()
#         sys.addaudithook(make_audithook(self))

#     def collect_all(self):
#         # Collect code objects
#         results = []
#         for obj in gc.get_objects():
#             if isinstance(obj, types.FunctionType):
#                 results.append((obj, obj.__code__))
#             elif getattr_static(obj, "__conform__", None) is not None:
#                 for x in gc.get_referents(obj):
#                     if isinstance(x, types.CodeType):
#                         results.append((obj, x))
#         for obj, co in results:
#             if isinstance((qual := getattr(obj, "__qualname__", None)), str):
#                 self.assimilate(co, (co.co_filename, *qual.split(".")[:-1]))
#             self.functions[co].add(obj)

#         # Collect module names / filenames
#         for module_name, module in sys.modules.items():
#             fname = getattr(module, "__file__", None)
#             if fname:
#                 self.register_filename(fname, module_name)

#     def assimilate(self, code, path=()):
#         if code.co_name == "<module>":  # pragma: no cover
#             # Typically triggered by the audit hook
#             name = code.co_filename
#         elif code.co_name.startswith("<"):
#             return
#         else:
#             name = code.co_name
#         if name:
#             path = (*path, name)
#             self.codes[(*path, code.co_firstlineno)] = code
#         for ct in code.co_consts:
#             if isinstance(ct, types.CodeType):
#                 self.assimilate(ct, path)

#     def register_filename(self, filename, module_name):
#         self.filename_to_module[filename] = module_name
#         self.activity

#     def _get_functions(self, code):
#         t = time.time()
#         results = [
#             fn
#             for fn in gc.get_referrers(code)
#             if isinstance(fn, types.FunctionType) or hasattr(fn, "__conform__")
#         ]
#         self.functions[code] = set(results)
#         self.last_cost = time.time() - t
#         return results

#     def get_functions(self, code, use_cache=False):
#         use_cache = (
#             use_cache or self.always_use_cache or self.last_cost > MAX_TIME
#         )
#         if use_cache and (results := self.functions[code]):
#             return list(results)
#         else:
#             return self._get_functions(code)

#     def update_cache_entry(self, obj, old_code, new_code):
#         self.functions[old_code].discard(obj)
#         self.functions[new_code].add(obj)


# db = _CodeDB()
# db.setup()


# ###########
# # Conform #
# ###########


# class ConformException(Exception):
#     pass


# def conform(obj1, obj2, use_cache=False):
#     if hasattr(obj1, "__conform__"):
#         obj1.__conform__(obj2)

#     elif isinstance(obj1, types.CodeType):
#         for fn in db.get_functions(obj1, use_cache=use_cache):
#             conform(fn, obj2)

#     elif isinstance(obj2, types.FunctionType):
#         conform(obj1, obj2.__code__)
#         obj1.__defaults__ = obj2.__defaults__
#         obj1.__kwdefaults__ = obj2.__kwdefaults__

#     elif isinstance(obj2, types.CodeType):
#         fv1 = obj1.__code__.co_freevars
#         fv2 = obj2.co_freevars
#         if fv1 != fv2:
#             msg = (
#                 f"Cannot replace closure `{obj1.__name__}` because the free "
#                 f"variables changed. Before: {fv1}; after: {fv2}."
#             )
#             if ("__class__" in (fv1 or ())) ^ ("__class__" in (fv2 or ())):
#                 msg += " Note: The use of `super` entails the `__class__` free variable."
#             raise ConformException(msg)
#         db.update_cache_entry(obj1, obj1.__code__, obj2)
#         obj1.__code__ = obj2

#     elif obj2 is None:
#         pass

#     else:  # pragma: no cover
#         raise ConformException(f"Cannot conform {obj1} with {obj2}")


# # @ovld.dispatch
# # def conform(self, obj1, obj2, **kwargs):
# #     if hasattr(obj1, "__conform__"):
# #         obj1.__conform__(obj2)
# #     else:
# #         self.resolve(obj1, obj2)(obj1, obj2, **kwargs)


# # @ovld
# # def conform(self, obj1: types.FunctionType, obj2: types.FunctionType, **kwargs):
# #     self(obj1, obj2.__code__, **kwargs)
# #     obj1.__defaults__ = obj2.__defaults__
# #     obj1.__kwdefaults__ = obj2.__kwdefaults__


# # @ovld
# # def conform(self, obj1: types.FunctionType, obj2: types.CodeType, **kwargs):
# #     fv1 = obj1.__code__.co_freevars
# #     fv2 = obj2.co_freevars
# #     if fv1 != fv2:
# #         msg = (
# #             f"Cannot replace closure `{obj1.__name__}` because the free "
# #             f"variables changed. Before: {fv1}; after: {fv2}."
# #         )
# #         if ("__class__" in (fv1 or ())) ^ ("__class__" in (fv2 or ())):
# #             msg += " Note: The use of `super` entails the `__class__` free variable."
# #         raise ConformException(msg)
# #     db.update_cache_entry(obj1, obj1.__code__, obj2)
# #     obj1.__code__ = obj2


# # @ovld
# # def conform(
# #     self,
# #     obj1: types.CodeType,
# #     obj2: (types.CodeType, types.FunctionType, type(None)),
# #     **kwargs,
# # ):
# #     for fn in db.get_functions(obj1, **kwargs):
# #         self(fn, obj2, **kwargs)


# # @ovld
# # def conform(self, obj1, obj2, **kwargs):
# #     pass


# def loop(self):
#     with self.lv:
#         result, err = self.run()
#         try:
#             while True:
#                 time.sleep(0.1)
#                 result, err = self.run()
#         except KeyboardInterrupt:
#             if err is not None:
#                 raise err
#             else:
#                 return result

# def loop(self):
#     result = None
#     err = None

#     def go(_=None):
#         nonlocal result, err
#         result, err = self.run()

#     def stop(_=None):
#         scheduler.dispose()

#     with self.lv:
#         with cbreak(), watching_changes() as chgs:
#             scheduler = rx.scheduler.EventLoopScheduler()
#             keypresses = ObservableProxy(
#                 rx.from_iterable(
#                     read_chars(),
#                     scheduler=scheduler
#                 )
#             ).share()

#             with given() as gv:
#                 keypresses.where(char="\n") >> stop
#                 keypresses.where(char="r") >> go
#                 chgs >> go

#                 go()
#                 scheduler.run()

#     if err is not None:
#         raise err
#     else:
#         return result
