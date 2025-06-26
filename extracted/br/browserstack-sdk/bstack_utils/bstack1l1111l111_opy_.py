# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
class bstack1l1l1l1l1l_opy_:
    def __init__(self, handler):
        self._1111111l1ll_opy_ = None
        self.handler = handler
        self._1111111ll11_opy_ = self.bstack1111111ll1l_opy_()
        self.patch()
    def patch(self):
        self._1111111l1ll_opy_ = self._1111111ll11_opy_.execute
        self._1111111ll11_opy_.execute = self.bstack1111111l1l1_opy_()
    def bstack1111111l1l1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11ll1l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣἘ"), driver_command, None, this, args)
            response = self._1111111l1ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11ll1l1_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣἙ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1111111ll11_opy_.execute = self._1111111l1ll_opy_
    @staticmethod
    def bstack1111111ll1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver