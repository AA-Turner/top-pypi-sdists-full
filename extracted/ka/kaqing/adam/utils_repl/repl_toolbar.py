from prompt_toolkit.application import get_app
from prompt_toolkit.formatted_text import FormattedText

status_message = "Initializing..."

class ReplToolbar:
    _message : str = None

    def set(msg: str):
        ReplToolbar._message = msg

        get_app().invalidate()

    def get():
        return ReplToolbar._message

def get_bottom_toolbar_text():
    # This function can return any dynamic status information
    return FormattedText([
        ('class:status', ' Status:'),
        ('class:status.field', ' Active '),
        ('class:status', ' | Time:'),
        ('class:status.field', ' 10:30 AM ')
    ])