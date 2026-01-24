# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
class bstack1lll1l1l11_opy_:
    def __init__(self, handler):
        self._1lll1lll111l_opy_ = None
        self.handler = handler
        self._1lll1lll1111_opy_ = self.bstack1lll1lll11l1_opy_()
        self.patch()
    def patch(self):
        self._1lll1lll111l_opy_ = self._1lll1lll1111_opy_.execute
        self._1lll1lll1111_opy_.execute = self.bstack1lll1lll11ll_opy_()
    def bstack1lll1lll11ll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢⅸ"), driver_command, None, this, args)
            response = self._1lll1lll111l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1111_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢⅹ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll1lll1111_opy_.execute = self._1lll1lll111l_opy_
    @staticmethod
    def bstack1lll1lll11l1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver