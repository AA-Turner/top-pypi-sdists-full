# encoding: utf-8

from future.builtins import str
from uiutil.tk_names import tkinter as tk, FALSE, TclError
from fdutil.string_tools import make_multi_line

u"""
Tooltip.

Places a tooltip near the pointer.

Attempts best fit based on available space above, below, left right
of the pointer, not the control.

Will reduce the font size repeatedly if it doesn't fit.

If it still doesn't fit after reducing to minimum font size,
defaults to the right.

Note that the height and width are estimated based on pixels on Windows 7 for
Courier and Times fonts only. These may differ on other platforms. This could
cause the tooltip to overlay the cursor if positioned above or to the left on
other platforms or with other fonts. That would cause the tooltip to close and
may appear to flicker. Right and below are favoured for this reason.

"""

import logging_helper

from timingsutil import Timeout
logging = logging_helper.setup_logging()

TOOLTIP = u'tooltip'

POINTER_SIZE = 20
NAME = 0
POINTS = 1
WEIGHT = 2
WIDTH = 0
HEIGHT = 1

MINIMUM_FONT_SIZE = 8

ESTIMATED_SIZE = {
    u'times': {
        u'6':  (1920 / 478, 1200 / 119),
        u'7':  (1920 / 383, 1200 / 99),
        u'8':  (1920 / 319, 1200 / 85),
        u'10': (1920 / 319, 1200 / 80),
        u'12': (1920 / 239, 1200 / 63)
    },
    u'courier': {
        u'6':  (1920 / 383, 1200 / 149),
        u'7':  (1920 / 383, 1200 / 99),
        u'8':  (1920 / 273, 1200 / 85),
        u'10': (1920 / 239, 1200 / 75),
        u'12': (1920 / 191, 1200 / 66)
    }
}


def estimate_line_height(font):

    try:
        return ESTIMATED_SIZE[font[NAME]][font[POINTS]][HEIGHT]

    except KeyError:
        pass

    try:
        return ESTIMATED_SIZE[u'times'][POINTS][HEIGHT]

    except KeyError:
        return ESTIMATED_SIZE[u'times'][u'10'][HEIGHT]


def estimate_line_width(font):
    try:
        return ESTIMATED_SIZE[font[NAME]][font[POINTS]][WIDTH]

    except KeyError:
        pass

    try:
        return ESTIMATED_SIZE[u'times'][POINTS][WIDTH]

    except KeyError:
        return ESTIMATED_SIZE[u'times'][u'10'][WIDTH]


def reduce_font_size(font):
    try:
        sizes = [int(size) for size in ESTIMATED_SIZE[font[NAME]]]

    except KeyError:
        sizes = [6, 7, 8, 10, 12]

    current_size = int(font[POINTS])

    if current_size == MINIMUM_FONT_SIZE:
        raise ValueError(u'minimum font size')

    while True:
        current_size -= 1

        if current_size in sizes or current_size == MINIMUM_FONT_SIZE:
            break

    font = (font[NAME], str(current_size), font[WEIGHT])

    return font


class ToolTip(object):

    """
    create a tooltip for a given widget
    'text' can be a string or a function
    that returns the tooltip text.
    The *args and *kwargs will be passed
    to the function.
    """

    def __init__(self,
                 widget,
                 text=u'widget info',
                 font=(u"courier", u"10", u"normal"),
                 max_width=None,
                 max_length=500,  # Arbitrary - larger than anything that fits on a normal display
                 observe=None,
                 text_colour=u'black',
                 background_colour=u'#ffffaf',
                 justify=u"center",
                 show_when_widget_is_disabled=False,
                 favour_start_of_text=True,
                 delay_before_display=0.5,
                 hang_time=None,
                 image_map=None,
                 *args,
                 **kwargs):
        """
        :param widget: Widget to associate the tooltip with
        :param text: text or function to fetch the text dynamically
        :param font:
        :param max_width: in character count, will cause lines to wrap
        :param max_length: limits line count (very long text will silently fail)
        :param observe: WARNING: Doesn't work yet!
                        An object to observe. Get notifications when
                        from the object of changes, which trigger an
                        update to the tooltip.
        :param text_colour: e.g. u'white', u'#202050'
        :param background_colour: e.g. u'white', u'#202050'
        :param justify:  left, right, or center
        :param show_when_widget_is_disabled:
        :param favour_start_of_text: When a tooltip doesn't fit
                                     vertically on screen, show
                                     the start of the text, and
                                     drop off the end.
                                     Set to False to reverse this.
        :param delay_before_display: Use this for complex tooltips
                                     that take a while to render.
                                     This stops the UI getting
                                     bogged down when passing over
                                     the associated widget.
        :param hang_time: Time in seconds to display the tooltip.
                          Default of None is an infinite hang time
        :param image_map: Allows discrete tooltips for different parts
                          of the widget. It should be an ImageMap instance.
        :param args: args passed to 'text' when it's a function
        :param kwargs: kwargs passed to 'text' when it's a function
        """

        self.widget = widget
        self.screen_width = self.widget.winfo_screenwidth()
        self.screen_height = self.widget.winfo_screenheight()
        self.args = args
        self.kwargs = kwargs
        self.update_label(text)
        self.widget.bind(u"<Enter>", self._enter)
        self.widget.bind(u"<Leave>", self.close)
        self.widget.bind(u"<ButtonPress>", self.close)
        self.__text = text
        self.max_width = max_width
        self.max_length = max_length
        self.font = font
        self.text_colour = text_colour
        self.background_colour = background_colour
        self.justify = justify
        self.show_when_widget_is_disabled = show_when_widget_is_disabled
        self.favour_start_of_text = favour_start_of_text
        self.delay_before_display = delay_before_display
        self.hang_time = hang_time
        self.image_map = image_map
        self.previous_tooltip_value = None
        if observe is not None:
            observe.register_observer(self)

    @property
    def _widget_is_disabled(self):
        try:
            if self.widget.cget(u'state').string == u'disabled':
                return True

        except AttributeError:
            if self.widget.cget(u'state') == u'disabled':
                return True

        return False

    @property
    def _no_longer_over_widget(self):
        x = self.widget.winfo_pointerx()
        y = self.widget.winfo_pointery()
        left = self.widget.winfo_rootx()
        right = left + self.widget.winfo_width()
        top = self.widget.winfo_rooty()
        bottom = top + self.widget.winfo_height()

        return not(left < x < right and top < y < bottom)

    @property
    def _relative_position(self):
        x = self.widget.winfo_pointerx() - self.widget.winfo_rootx()
        y = self.widget.winfo_pointery() - self.widget.winfo_rooty()
        return x, y

    def _key(self):
        return self.image_map.key(self._relative_position)

    def _enter(self,
               _=None):  # Need 'event' even though it's not used
        self.close()
        Timeout(self.delay_before_display).wait()
        self._create_tooltip()

    def _create_tooltip(self):

        if not self.show_when_widget_is_disabled:
            if self._widget_is_disabled:
                return

        if self._no_longer_over_widget:
            self.close()
            return

        if not self.image_map:
            try:
                self.widget.config(cursor=u"wait")
            except TclError:
                self.widget.config(cursor=u"watch")

        try:
            text = self.text
        except KeyError:
            text = u''

        if isinstance(text, dict):
            text_param = text.pop(u'text', u'-')
            self.update(**text)
            text = text_param

        if self.max_length:
            if self.favour_start_of_text:
                text = text.splitlines()[:self.max_length]
            else:
                text = text.splitlines()[-self.max_length:]
            text = '\n'.join(text)

        # text = unicode(text)  # TODO: Make this str when we can for PY3
        if self.max_width:
            text = make_multi_line(line=text,
                                   maximum_width=self.max_width)

        justify = self.justify
        background_colour = self.background_colour
        text_colour = self.text_colour
        font = self.font

        if text != self.previous_tooltip_value:
            self.close()

        if text and text != self.previous_tooltip_value:
            x, y, font = self.__best_position(text=text,
                                              font=font)
            # self.widget.cget('state')
            # creates a toplevel window
            self.tw = tk.Toplevel(self.widget)

            # Leaves only the label and removes the app window
            self.tw.wm_overrideredirect(True)

            # This is required with the above to make window borderless on macOS with tk 8.6+
            self.tw.resizable(width=FALSE, height=FALSE)

            self.tw.wm_geometry(u"+%d+%d" % (x, y))

            # Would like to import and use Label from .label,
            # but it causes a circular reference because Label
            # uses this Tooltip class!
            self.label = tk.Label(self.tw,
                                  justify=justify,
                                  background=background_colour,
                                  foreground=text_colour,
                                  font=font)
            self.label.config(text=text)
            self.label.grid()
            self.tw.lift()
            self.tw.attributes('-topmost', True)

        self.previous_tooltip_value = text
        self.widget.config(cursor=u"")
        if self.hang_time:
            self.tw.after(self.hang_time * 1000, self._expired)

    def __fits(self,
               height,
               width,
               left_space,
               right_space,
               top_space,
               bottom_space):

        if height <= bottom_space and width <= self.screen_width:
            return u'under'

        if width <= right_space and height <= self.screen_height:
            return u'right'

        if height <= top_space and width <= self.screen_width:
            return u'above'

        if width <= left_space and height <= self.screen_height:
            return u'left'

    def __best_position(self,
                        text,
                        font=None):

        pointer_x = self.widget.winfo_pointerx()
        pointer_y = self.widget.winfo_pointery()

        left_space = pointer_x - POINTER_SIZE
        right_space = self.screen_width - pointer_x - POINTER_SIZE
        top_space = pointer_y - POINTER_SIZE
        bottom_space = self.screen_height - pointer_y - POINTER_SIZE

        if isinstance(text, Exception):
            logging.exception(text)

        splitlines = str(text).splitlines()
        width = max([len(line) for line in splitlines])

        line_count = len(splitlines)

        font = (font
                if font
                else self.font)

        while True:
            pixel_height = estimate_line_height(font) * line_count
            pixel_width = estimate_line_width(font) * width
            fits = self.__fits(height=pixel_height,
                               width=pixel_width,
                               left_space=left_space,
                               right_space=right_space,
                               top_space=top_space,
                               bottom_space=bottom_space)

            if fits:
                break

            try:
                font = reduce_font_size(font)

            except ValueError:
                break

        x = pointer_x
        y = pointer_y

        if not fits:
            fits = u'right'

        if fits == u'right':
            x += POINTER_SIZE

        if fits == u'left':
            x -= POINTER_SIZE + pixel_width

        if fits == u'under':
            y += POINTER_SIZE

        if fits == u'above':
            y -= POINTER_SIZE + pixel_height

        if fits in (u'left', u'right'):
            y -= pixel_height // 2
            bottom_posn = y + pixel_height

            if bottom_posn > self.screen_height:
                # position at the bottom
                y = self.screen_height - pixel_height

            if y < 0:
                y = (0  # Cut off below the display
                     if self.favour_start_of_text
                     else self.screen_height - pixel_height)  # Cut off above the display

        if fits in (u'above', u'under'):
            x -= pixel_width // 2
            right_posn = x + pixel_width

            if right_posn > self.screen_width:
                # position at the bottom
                x = self.screen_width - pixel_width

            if x < 0:
                # position at the top (may cut off below the display)
                x = 0

        return x, y, font

    def update_label(self,
                     text=None):
        """
        Call this to update either the text string
        or text function used to up date the tooltip text
        """
        if text is not None:
            self.text = text

    @property
    def text(self):

        if callable(self.__text):
            # assume that it's a function
            try:
                return self.__text(*self.args,
                                   **self.kwargs)
            except Exception as e:
                logging.exception(e)
                return (u'EXCEPTION:\n{text}\nSee log file for more info.'
                        .format(text=str(e)))
        elif self.image_map:
            self.widget.after(100, self._create_tooltip)
            key = self._key()
            try:
                value = self.image_map.value(key)
            except KeyError:
                return u''
            return value[TOOLTIP] if value[TOOLTIP] else u''
        else:
            return self.__text

    @text.setter
    def text(self,
             value_or_function):
        u"""
        WARNING: If text was originally a function, setting it to
                 a string breaks the link with the function.
        """
        self.__text = value_or_function

    def update(self,
               text=None,
               font=None,
               text_colour=None,
               background_colour=None,
               justify=None):

        if text is not None:
            self.text = text

        if font is not None:
            self.font = font

        if text_colour is not None:
            self.text_colour = text_colour

        if background_colour is not None:
            self.background_colour = background_colour

        if justify is not None:
            self.justify = justify

    def notification(self,
                     notifier,
                     **params):

        """
        To use notify to update based on changes in another component, the
        tooltip should be set up with text as a function, not a value.
        Any arguments will be tossed.
        The notification is just a trigger.
        """
        # TODO: Pass parameters to update_label, or it won't do anything!
        self.update_label()

    def _expired(self,
                 _=None):  # Need 'event' even though it's not used
        self.close()

    def close(self,
              _=None):  # Need 'event' even though it's not used
        try:
            self.previous_tooltip_value = None
            self.widget.config(cursor=u"")

            if self.tw:
                self.tw.destroy()

        except AttributeError:
            pass


if __name__ == u"__main__":

    master = tk.Tk()

    def callback():
        print("click!")

    b = tk.Button(master, text=u"OK", command=callback)

    w = 50
    h = 150
    lines = [str(i) + u'.' * (w - len(str(i))) for i in range(h)]

    STB_COLOURS = {u'text_colour':       u'white',
                   u'background_colour': u'dark blue'}

    ToolTip(widget=b,
            text=u'\n'.join(lines),
            font=(u"courier", u'12', u"normal"),
            **STB_COLOURS)
    b.grid()

    tk.mainloop()
