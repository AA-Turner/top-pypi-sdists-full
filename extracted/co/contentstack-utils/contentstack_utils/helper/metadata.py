"""
    Metadata is the model class for embedded objects

    Returns:
        str: text, item_type, item_uid, type_uid, style_type, outer_html and attributes
"""

from contentstack_utils.embedded.styletype import StyleType


class Metadata:
    """
    model helper class to set and get value
    """

    def __init__(self, text: str, item_type: str, item_uid: str,
                 content_type_uid: str, style_type: StyleType,
                 outer_html: str, attributes: str):
        """
        Used to set the value to the variables

        Args:
            text (str): text for embedded objects
            item_type (str): item_type for embedded objects
            item_uid (str): item_uid for embedded objects
            content_type_uid (str): content_type_uid for embedded objects
            style_type (StyleType): style_type for embedded objects
            outer_html (str): outer_html for embedded objects
            attributes (str): attributes for embedded objects
        """
        self.text = text
        self.item_type = item_type
        self.item_uid = item_uid
        self.content_type_uid = content_type_uid
        self.style_type = style_type
        self.outer_html = outer_html
        self.attributes = attributes

    @property
    def get_text(self):
        return self.text

    @property
    def get_item_type(self):
        return self.item_type

    @property
    def get_item_uid(self):
        return self.item_uid

    @property
    def get_content_type_uid(self):
        return self.content_type_uid

    @property
    def get_style_type(self) -> StyleType:
        return self.style_type

    @property
    def get_outer_html(self):
        return self.outer_html

    @property
    def get_attributes(self):
        return self.attributes
