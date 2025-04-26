class LimitManager(object):
    def __init__(self, limiters=None):
        if limiters is None:
            limiters = []
        self.limiters = limiters

    def try_with_limits(self, start_time, aug_core, skip_limiters):
        can_execute = True
        afters_to_call = []

        try:
            for limiter in self.limiters:
                if limiter.before_run(start_time) or skip_limiters:
                    afters_to_call.append(lambda limiter=limiter: limiter.after_run(start_time))
                else:
                    can_execute = False

            if can_execute:
                aug_core()
        # Even if some limiter threw an exception, we want to call the `after`s of the previous limiters
        finally:
            for after in afters_to_call:
                after()
