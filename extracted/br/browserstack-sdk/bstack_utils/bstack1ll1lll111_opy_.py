# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
class bstack111l1lll_opy_:
    def __init__(self, handler):
        self._1lll11l111ll_opy_ = None
        self.handler = handler
        self._1lll11l111l1_opy_ = self.bstack1lll11l11111_opy_()
        self.patch()
    def patch(self):
        self._1lll11l111ll_opy_ = self._1lll11l111l1_opy_.execute
        self._1lll11l111l1_opy_.execute = self.bstack1lll11l1111l_opy_()
    def bstack1lll11l1111l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣ⎛"), driver_command, None, this, args)
            response = self._1lll11l111ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1111_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣ⎜"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll11l111l1_opy_.execute = self._1lll11l111ll_opy_
    @staticmethod
    def bstack1lll11l11111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver