import datetime


def log_execute_time(logger):
    def _log_execute_time(f):
        def __log_execute_time(*args, **kwargs):
            start = datetime.datetime.now()
            rest = f(*args, **kwargs)
            end = datetime.datetime.now()
            logger.info("function {} execute total cost {}.".format(f.__name__,
                                                                    round((end - start).total_seconds(), 5) * 1000))
            return rest

        return __log_execute_time

    return _log_execute_time
