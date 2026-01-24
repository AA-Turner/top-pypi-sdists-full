""""
There are two types StyleType ENTRY and ASSETS
For `Entry`: StyleType.BLOCK, StyleType.INLINE, StyleType.LINKED,
For `Assets`: StyleType.DISPLAY, StyleType.DOWNLOADABLE
 """
import enum


class StyleType(enum.Enum):

    """
    This StyleType contains four options like below.
    BLOCK ,INLINE ,LINK,DISPLAY,DOWNLOAD
    """

    BLOCK = 'block'
    INLINE = 'inline'
    LINK = 'link'
    DISPLAY = 'display'
    DOWNLOAD = 'download'
