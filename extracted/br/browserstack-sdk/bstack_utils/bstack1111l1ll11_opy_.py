# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
class bstack1ll1ll1ll_opy_:
    def __init__(self, handler):
        self._1ll1lll11lll_opy_ = None
        self.handler = handler
        self._1ll1lll1l111_opy_ = self.bstack1ll1lll11ll1_opy_()
        self.patch()
    def patch(self):
        self._1ll1lll11lll_opy_ = self._1ll1lll1l111_opy_.execute
        self._1ll1lll1l111_opy_.execute = self.bstack1ll1lll1l11l_opy_()
    def bstack1ll1lll1l11l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll1lll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧⓌ"), driver_command, None, this, args)
            response = self._1ll1lll11lll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll1lll_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧⓍ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1lll1l111_opy_.execute = self._1ll1lll11lll_opy_
    @staticmethod
    def bstack1ll1lll11ll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver