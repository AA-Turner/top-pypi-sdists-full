# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
class bstack1l1111l11_opy_:
    def __init__(self, handler):
        self._1ll1lll11ll1_opy_ = None
        self.handler = handler
        self._1ll1lll11l11_opy_ = self.bstack1ll1lll11lll_opy_()
        self.patch()
    def patch(self):
        self._1ll1lll11ll1_opy_ = self._1ll1lll11l11_opy_.execute
        self._1ll1lll11l11_opy_.execute = self.bstack1ll1lll11l1l_opy_()
    def bstack1ll1lll11l1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣⓝ"), driver_command, None, this, args)
            response = self._1ll1lll11ll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll11_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣⓞ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1lll11l11_opy_.execute = self._1ll1lll11ll1_opy_
    @staticmethod
    def bstack1ll1lll11lll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver