from uiutil import BaseFrame, standalone, Label, Button, Position, TextEntry


class MyFrame(BaseFrame):

    def __init__(self,
                 **kwargs):
        super(MyFrame, self).__init__(**kwargs)

        self.label = Label(value="Hello")

        self.text = TextEntry(column=Position.NEXT,
                              focus=True)

        Button(text="Click Me",
               column=Position.NEXT,
               command=self.clicked)

    def clicked(self):
        self.label.value = "Button was clicked!"


standalone(frame=MyFrame,
           title="Welcome to UI Util app",
           width=350)
