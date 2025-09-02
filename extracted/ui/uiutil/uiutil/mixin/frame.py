# encoding: utf-8

import logging_helper
from uiutil.helper.introspection import calling_base_frame
from ..helper.arguments import grid_and_non_grid_kwargs
from .frames import FramesMixIn
from .all import AllMixIn

logging = logging_helper.setup_logging()


class FrameMixIn(AllMixIn,
                 FramesMixIn):

    FRAME = None  # Redefine in subclass

    def _common_init(self,
                     parent=None,
                     layout=None,
                     *args,
                     **kwargs):

        self.parent = parent if parent else calling_base_frame(exclude=self)

        grid_kwargs, kwargs = grid_and_non_grid_kwargs(frame=self.parent,
                                                       **kwargs)

        # Unfortunately everything Tkinter is written in Old-Style classes so it blows up if you use super!
        self.FRAME.__init__(self, master=self.parent, **kwargs)

        kwargs.update(grid_kwargs)

        AllMixIn.__init__(self, layout=layout, *args, **kwargs)
        FramesMixIn.__init__(self, *args, **kwargs)

        try:
            self.parent.position_for_next_widget(**grid_kwargs)
        except AttributeError:
            pass  # Parent is not a Frame

        try:
            self.parent.register_frame(self)
        except AttributeError:
            logging.debug(u'{parent} does not have FramesMixIn'.format(parent=self.parent.__class__))

    def exists(self):
        return self.winfo_exists() != 0

    def exit(self):
        self.cancel_poll()
        self.unregister_observables()
        self.unregister_observers()
        self.stop_queue_processor()
        self.close_pool()

        self.exit_frames()

        self.close()

    def close(self):
        """ Override this to perform steps when the frame is closed. """
        pass
