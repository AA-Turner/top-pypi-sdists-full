class FrameHelper():

    def __init__(self, context=None,logging_error=None,logging_info=None):
        super(FrameHelper, self).__init__()
        self.context = context
        self.logging_error = context.logging_link_error if context else logging_error
        self.logging_info = context.logging_link_info if context else logging_info

    def logging_link_error(self, content):
        if self.logging_error:
            self.logging_error(content)

    def logging_link_info(self, content):
        if self.logging_info:
            self.logging_info(content)