# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
class bstack1ll11l1ll1_opy_:
    def __init__(self, handler):
        self._1ll11ll1l1ll_opy_ = None
        self.handler = handler
        self._1ll11ll1ll11_opy_ = self.bstack1ll11ll1ll1l_opy_()
        self.patch()
    def patch(self):
        self._1ll11ll1l1ll_opy_ = self._1ll11ll1ll11_opy_.execute
        self._1ll11ll1ll11_opy_.execute = self.bstack1ll11ll1l1l1_opy_()
    def bstack1ll11ll1l1l1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111ll11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣ⛪"), driver_command, None, this, args)
            response = self._1ll11ll1l1ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111ll11_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣ⛫"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll11ll1ll11_opy_.execute = self._1ll11ll1l1ll_opy_
    @staticmethod
    def bstack1ll11ll1ll1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver