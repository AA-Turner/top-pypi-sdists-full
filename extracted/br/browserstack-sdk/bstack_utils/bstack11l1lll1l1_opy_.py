# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
class bstack1ll111111_opy_:
    def __init__(self, handler):
        self._1lll1ll11l1l_opy_ = None
        self.handler = handler
        self._1lll1ll11l11_opy_ = self.bstack1lll1ll111ll_opy_()
        self.patch()
    def patch(self):
        self._1lll1ll11l1l_opy_ = self._1lll1ll11l11_opy_.execute
        self._1lll1ll11l11_opy_.execute = self.bstack1lll1ll11ll1_opy_()
    def bstack1lll1ll11ll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11lllll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣ↜"), driver_command, None, this, args)
            response = self._1lll1ll11l1l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11lllll_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣ↝"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll1ll11l11_opy_.execute = self._1lll1ll11l1l_opy_
    @staticmethod
    def bstack1lll1ll111ll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver