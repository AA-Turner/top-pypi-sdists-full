# encoding: utf-8

from uiutil.tk_names import NSEW

from uiutil.window.root import RootWindow
from uiutil.frame.splash import SplashFrame


class SplashWindow(RootWindow):

    def __init__(self,
                 image_path,
                 wait_func,
                 info_title=None,
                 info_text=None,
                 message=u'Splash Screen',
                 menu=False,
                 *args,
                 **kwargs):

        self.window_title = message
        self.image_path = image_path
        self.wait_func = wait_func
        self.info_title = info_title
        self.info_text = info_text

        super(SplashWindow, self).__init__(width=640,
                                           height=452,
                                           fixed=True,
                                           padding=u'0 0 0 0',
                                           menu=menu,
                                           borderless=True,
                                           *args,
                                           **kwargs)

    def _draw_widgets(self):
        # Override width and height now that screen width and height are available!
        width = self.winfo_screenwidth() // 3
        height = self.winfo_screenheight() // 3

        self.width = width
        self.height = height

        # Manually update geometry
        self.geometry(u'{w}x{h}+{x}+{y}'.format(w=self.width,
                                                h=self.height,
                                                x=(self.winfo_screenwidth() // 2) - (self.width // 2),
                                                y=(self.winfo_screenheight() // 2) - (self.height // 2)))

        self.splash = self.add_frame(frame=SplashFrame,
                                     parent=self._main_frame,
                                     image_path=self.image_path,
                                     image_width=self.width,
                                     image_height=self.height,
                                     info_title=self.info_title,
                                     info_text=self.info_text,
                                     wait_func=self.wait_func,
                                     sticky=NSEW)
