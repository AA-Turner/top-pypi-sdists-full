from contentstack_utils.embedded.styletype import StyleType


def convert_style(style) -> StyleType:
    if style == 'block':
        return StyleType.BLOCK
    if style == 'inline':
        return StyleType.INLINE
    if style == 'link':
        return StyleType.LINK
    if style == 'display':
        return StyleType.DISPLAY
    if style == 'download':
        return StyleType.DOWNLOAD
