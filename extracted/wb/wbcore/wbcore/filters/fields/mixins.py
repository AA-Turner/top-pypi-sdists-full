class RangeMixin:
    def _validate_initial(self, request, initial):
        if isinstance(initial, (list, tuple, set)):
            initial = ",".join(map(lambda o: "" if o is None else str(o), initial))
        return initial
