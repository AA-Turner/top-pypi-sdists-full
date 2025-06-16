import pyloco


class Echo(pyloco.Task):
    """displays input text

    'echo' task reads user's input from command-line and displays
    it on screen. This is an example of a simple task creation.
    """

    _name_ = "echotask"

    def __init__(self, parent):

        self.add_data_argument("text", type=str, help="input text to print")
        self.register_forward("text", help="printed text")

    def perform(self, targs):

        print(targs.text)

        self.add_forward(text=targs.text)
