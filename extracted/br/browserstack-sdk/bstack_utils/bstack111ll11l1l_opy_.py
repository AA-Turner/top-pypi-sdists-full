# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
class bstack1111l1111_opy_:
    def __init__(self, handler):
        self._1ll11lllllll_opy_ = None
        self.handler = handler
        self._1ll11lllll1l_opy_ = self.bstack1ll11llllll1_opy_()
        self.patch()
    def patch(self):
        self._1ll11lllllll_opy_ = self._1ll11lllll1l_opy_.execute
        self._1ll11lllll1l_opy_.execute = self.bstack1ll11lllll11_opy_()
    def bstack1ll11lllll11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥ⚴"), driver_command, None, this, args)
            response = self._1ll11lllllll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11ll11_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥ⚵"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll11lllll1l_opy_.execute = self._1ll11lllllll_opy_
    @staticmethod
    def bstack1ll11llllll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver