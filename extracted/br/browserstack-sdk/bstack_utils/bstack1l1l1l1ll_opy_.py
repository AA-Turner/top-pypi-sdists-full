# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
class bstack1l1ll11111_opy_:
    def __init__(self, handler):
        self._1111111l11l_opy_ = None
        self.handler = handler
        self._11111111lll_opy_ = self.bstack11111111ll1_opy_()
        self.patch()
    def patch(self):
        self._1111111l11l_opy_ = self._11111111lll_opy_.execute
        self._11111111lll_opy_.execute = self.bstack1111111l111_opy_()
    def bstack1111111l111_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࠤ὘"), driver_command, None, this, args)
            response = self._1111111l11l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࠤὙ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111111lll_opy_.execute = self._1111111l11l_opy_
    @staticmethod
    def bstack11111111ll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver