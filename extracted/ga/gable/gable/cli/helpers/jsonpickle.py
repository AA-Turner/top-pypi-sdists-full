import datetime

import jsonpickle


def register_jsonpickle_handlers():
    jsonpickle.handlers.registry.register(datetime.datetime, DatetimeHandler)


class DatetimeHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj, data):
        return obj.isoformat()
