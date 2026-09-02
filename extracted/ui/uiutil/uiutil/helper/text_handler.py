# encoding: utf-8

import logging
from queue import Queue, Empty
from tkinter.constants import END

from logging_helper import setup_log_format


class TextHandler(logging.Handler):

    """This class sets up a custom log Handler that allows you to log to a Tkinter Text or ScrolledText widget"""

    def __init__(self,
                 text,
                 *args,
                 **kwargs):

        logging.Handler.__init__(self, *args, **kwargs)

        self.text = text
        self.setFormatter(setup_log_format())
        self.setup_line_colours()
        self.log_queue = Queue()

    def handle(self, record):

        rv = self.filter(record)

        if rv:
            self.log_queue.put(record)

        return rv

    def emit(self, record):

        # Might be a better way to do these .replace methods!
        # Needed to do this to avoid an issue with self.text.insert when there was a single "
        msg = (self.format(record)
               .replace(u'\"', u'"')
               .replace(u'"', u'\"')
               .replace(u"\'", u"'")
               .replace(u'"', u"\'"))

        try:
            colour_key = msg.split(u' - ')[1][:7].strip()

        except IndexError:
            colour_key = tuple()

        self.text.append(msg + u'\n', colour_key)

    def clear(self, start=1.0, end=END):
        self.text.clear(start=start,
                        end=end)

    def setup_line_colours(self):

        tag_colours = {u'DEBUG': u'blue',
                       u'INFO': u'black',
                       u'WARNING': u'orange',
                       u'ERROR': u'red',
                       u'CRITICAL': u'red'}

        for colour in tag_colours:
            self.text.tag_configure(colour, foreground=tag_colours[colour])

    def poll(self):

        try:
            record = self.log_queue.get_nowait()

            self.emit(record=record)

            self.log_queue.task_done()

        except Empty:
            pass
