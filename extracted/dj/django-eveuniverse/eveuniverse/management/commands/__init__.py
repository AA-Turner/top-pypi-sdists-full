EXPECTATION_TEXT = (
    "Note that this process can take some time to complete. "
    "It will create many tasks to load the data and "
    "you can watch the progress on the dashboard. "
    "It is likely finished as soon as the task queue is empty again."
)


def get_input(text):
    """wrapped input to enable unit testing / patching"""
    return input(text)
