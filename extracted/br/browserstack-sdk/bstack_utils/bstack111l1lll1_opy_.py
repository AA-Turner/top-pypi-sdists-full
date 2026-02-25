# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
class bstack1l111111l_opy_:
    def __init__(self, handler):
        self._1lll1l1111ll_opy_ = None
        self.handler = handler
        self._1lll1l111l11_opy_ = self.bstack1lll1l11111l_opy_()
        self.patch()
    def patch(self):
        self._1lll1l1111ll_opy_ = self._1lll1l111l11_opy_.execute
        self._1lll1l111l11_opy_.execute = self.bstack1lll1l1111l1_opy_()
    def bstack1lll1l1111l1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11l1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨ≳"), driver_command, None, this, args)
            response = self._1lll1l1111ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11l1l11_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨ≴"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll1l111l11_opy_.execute = self._1lll1l1111ll_opy_
    @staticmethod
    def bstack1lll1l11111l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver