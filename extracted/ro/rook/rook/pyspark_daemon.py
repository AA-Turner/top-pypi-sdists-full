"""
Loads Rook into pyspark workers
Usage: spark-submit --conf spark.python.daemon.module=rook.pyspark_daemon
"""
import inspect
import os

import pyspark.daemon
import functools
import six
import sys

from rook.config import ImportServiceConfig

original_worker_main = pyspark.daemon.worker_main


def worker_main(*args, **kwargs):
    import rook
    try:
        rook.start(log_file="", log_to_stderr=True)
        from rook.logger import logger
        logger.debug("Started Rook in Spark worker")
        from rook.interface import _rook as singleton, _TRUE_VALUES
        from rook.services import ImportService
        import_service = singleton.get_trigger_services().get_service(ImportService.NAME)

        def try_load_rdd_udf_module(obj):
            try:
                # The pickled object that gets sent when you call a UDF on a RDD is a 4-elements tuple, with the first
                # one containing the function
                if type(obj) is tuple and len(obj) == 4 and callable(obj[0]):
                    # This looks complicated, but the UDF is stored as part of the closure, so we fetch it from the RDD
                    # object (there are several layers to traverse here...)
                    module_name = obj[0].__closure__[0].cell_contents.__closure__[0].cell_contents.__module__

                    # Sometimes the module's path isn't in sypath due to running pyspark in different working
                    # directory than the driver, so we add it just in case
                    path_to_module = os.path.dirname(inspect.getfile(obj[0].__closure__[0].cell_contents.__closure__[0].cell_contents))
                    sys.path.insert(0, path_to_module)
                    import_service.disable_evaluator()
                    import importlib
                    importlib.import_module(module_name)
                    return True
            except Exception as e:  # lgtm[py/catch-base-exception]
                logger.debug("pyspark udf (rdd): failed to read object {0} with error {1}".format(obj, str(e)))
            finally:
                import_service.enable_evaluator()

            return False

        def try_load_df_udf_module(obj):
            try:
                # The pickled object that gets sent when you call a UDF on a DF is a 2-elements tuple, with the first
                # one containing the function
                if type(obj) is tuple and len(obj) == 2 and callable(obj[0]):
                    # This looks complicated, but the UDF is stored as part of the closure, so we fetch it from the RDD
                    # object (there are several layers to traverse here...)
                    module_name = obj[0].__closure__[0].cell_contents.__module__

                    # Sometimes the module's path isn't in sypath due to running pyspark in different working
                    # directory than the driver, so we add it just in case
                    path_to_module = os.path.dirname(inspect.getfile(obj[0].__closure__[0].cell_contents))
                    sys.path.insert(0, path_to_module)
                    import_service.disable_evaluator()
                    import importlib
                    importlib.import_module(module_name)
                    return True
            except Exception as e:  # lgtm[py/catch-base-exception]
                logger.debug("pyspark udf (df): failed to read object {0} with error {1}".format(obj, str(e)))
            finally:
                import_service.enable_evaluator()

            return False

        def pickle_load_hook(orig_func, eager_load, *args, **kwargs):
            obj = orig_func(*args, **kwargs)
            loaded_udf = try_load_rdd_udf_module(obj)
            if not loaded_udf:
                loaded_udf = try_load_df_udf_module(obj)
            if eager_load or loaded_udf:
                try:
                    # this is here to deal with the delay of having the periodic thread call evaluate_module_list -
                    # it could miss a module being imported.
                    import_service.evaluate_module_list()
                except:  # lgtm[py/catch-base-exception]
                    logger.exception("Silenced exception during module list evaluation")
            return obj

        # we may end up missing pickle module imports if we rely on the sys.modules polling thread
        # only do this eagerly if we're not using the import hook
        should_eager_load = ImportServiceConfig.USE_IMPORT_HOOK is False
        import pyspark.serializers
        pyspark.serializers.pickle.loads = functools.partial(pickle_load_hook, pyspark.serializers.pickle.loads,
                                                             should_eager_load)
        pyspark.serializers.pickle.load = functools.partial(pickle_load_hook, pyspark.serializers.pickle.load,
                                                            should_eager_load)
    except:  # lgtm[py/catch-base-exception]
        six.print_("Starting Rook in worker_main failed", file=sys.stderr)

    result = original_worker_main(*args, **kwargs)
    try:
        rook.flush()
    except:  # lgtm[py/catch-base-exception]
        pass
    return result


pyspark.daemon.worker_main = worker_main

if __name__ == '__main__':
    pyspark.daemon.manager()
