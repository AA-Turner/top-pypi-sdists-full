# encoding: utf-8

import logging_helper

logging = logging_helper.setup_logging()


class FramesMixIn(object):

    def __init__(self,
                 *args,
                 **kwargs):
        self._frames = []
        super(FramesMixIn, self).__init__()

    def register_frame(self,
                       frame_object):
        if frame_object not in self._frames:
            self._frames.append(frame_object)

    @staticmethod
    def add_frame(frame,
                  **kwargs):

        try:
            frame_object = frame(**kwargs)

        except Exception as e:
            logging.error(u'There was a problem initialising {frame}'.format(frame=frame))
            logging.exception(e)
            frame_object = None

        return frame_object

    def remove_frame(self,
                     frame,
                     **kwargs):
        try:
            self._frames.pop(self._frames.index(frame))
        except (IndexError, ValueError):
            logging.warning(u'Removing unregistered frame: {frame}'.format(frame=frame))
        frame.destroy()

    def update_geometry(self):
        """ Pass update geometry request to window this frame is a part of. """
        self.parent.update_geometry()

    def exit_frames(self):
        while self._frames:
            frame = self._frames.pop()
            try:
                frame.exit()

            except Exception as err:
                logging.error(u'Something went wrong while exiting frame: {f}'.format(f=frame))
                logging.error(err)
