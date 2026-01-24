from reportlab.platypus import Paragraph as BaseParagraph


class FormattedParagraph(BaseParagraph):
    def __init__(self, text, *args, **kwargs):
        text = text.replace("<br>", "<br/>")  # convert the HTML line break into a compatible XML line break tag
        super().__init__(text, *args, **kwargs)
