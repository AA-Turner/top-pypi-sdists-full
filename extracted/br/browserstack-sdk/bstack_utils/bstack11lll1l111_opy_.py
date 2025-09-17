# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
class bstack1ll1l11l11_opy_:
    def __init__(self, handler):
        self._1lllll1lll11_opy_ = None
        self.handler = handler
        self._1lllll1llll1_opy_ = self.bstack1lllll1ll1ll_opy_()
        self.patch()
    def patch(self):
        self._1lllll1lll11_opy_ = self._1lllll1llll1_opy_.execute
        self._1lllll1llll1_opy_.execute = self.bstack1lllll1lll1l_opy_()
    def bstack1lllll1lll1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l11ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣΰ"), driver_command, None, this, args)
            response = self._1lllll1lll11_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l11ll1_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣῤ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lllll1llll1_opy_.execute = self._1lllll1lll11_opy_
    @staticmethod
    def bstack1lllll1ll1ll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver