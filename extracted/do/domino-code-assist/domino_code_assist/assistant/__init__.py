from IPython.display import clear_output, display


def init():
    from .assistant import Assistant

    element = Assistant()
    display(element, clear=True)
