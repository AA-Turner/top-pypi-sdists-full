import logging
import logging.handlers

import traceback

from requests_futures.sessions import FuturesSession

session = FuturesSession()


def response_callback(resp, *args, **kwargs):
    """ Don't do anything with the response """
    pass


session.hooks['response'] = response_callback


class HTTPSHandler(logging.Handler):
    def __init__(self, url, fqdn=False, localname=None, facility=None):
        logging.Handler.__init__(self)
        self.url = url
        self.fqdn = fqdn
        self.localname = localname
        self.facility = facility

    def get_full_message(self, record):
        if record.exc_info:
            return '\n'.join(traceback.format_exception(*record.exc_info))
        else:
            return record.getMessage()

    def emit(self, record):
        try:
            payload = self.format(record)
            session.post(self.url, data=payload.encode("utf-8"))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
