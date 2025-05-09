# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
class bstack11l11l1ll1_opy_:
    def __init__(self, handler):
        self._111l111ll1l_opy_ = None
        self.handler = handler
        self._111l111l1l1_opy_ = self.bstack111l111l1ll_opy_()
        self.patch()
    def patch(self):
        self._111l111ll1l_opy_ = self._111l111l1l1_opy_.execute
        self._111l111l1l1_opy_.execute = self.bstack111l111ll11_opy_()
    def bstack111l111ll11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᶖ"), driver_command, None, this, args)
            response = self._111l111ll1l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11lll_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᶗ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l111l1l1_opy_.execute = self._111l111ll1l_opy_
    @staticmethod
    def bstack111l111l1ll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver