# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
class bstack111lll111_opy_:
    def __init__(self, handler):
        self._1ll1llll11l1_opy_ = None
        self.handler = handler
        self._1ll1llll1l11_opy_ = self.bstack1ll1llll1l1l_opy_()
        self.patch()
    def patch(self):
        self._1ll1llll11l1_opy_ = self._1ll1llll1l11_opy_.execute
        self._1ll1llll1l11_opy_.execute = self.bstack1ll1llll11ll_opy_()
    def bstack1ll1llll11ll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11lll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣ⒥"), driver_command, None, this, args)
            response = self._1ll1llll11l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11lll1_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣ⒦"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1llll1l11_opy_.execute = self._1ll1llll11l1_opy_
    @staticmethod
    def bstack1ll1llll1l1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver