from uiutil import BaseFrame, standalone, Combobox


class MyFrame(BaseFrame):

    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.combo = Combobox(value=2,
                              values=(1, 2, 3, 4, 5, "Text"))


standalone(frame=MyFrame,
           title="Welcome to UI Util app")
