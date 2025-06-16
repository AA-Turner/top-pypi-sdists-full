import pyloco

class Echo(pyloco.Task):
    """displays input text

    'echo' task reads user's input from command-line and displays
    it on screen. This is an example of a simple task creation.
    """

    _version_ = "0.0.4"
    _name_ = "echo"

    def __init__(self, parent):

        self.add_data_argument("text", type=str, help="input text to print")

    def perform(self, targs):

        print(targs.text)
