# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
class bstack1ll1l1l1ll_opy_:
    def __init__(self, handler):
        self._111l111lll1_opy_ = None
        self.handler = handler
        self._111l111llll_opy_ = self.bstack111l111ll11_opy_()
        self.patch()
    def patch(self):
        self._111l111lll1_opy_ = self._111l111llll_opy_.execute
        self._111l111llll_opy_.execute = self.bstack111l111ll1l_opy_()
    def bstack111l111ll1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1llllll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧᶍ"), driver_command, None, this, args)
            response = self._111l111lll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1llllll_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧᶎ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l111llll_opy_.execute = self._111l111lll1_opy_
    @staticmethod
    def bstack111l111ll11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver