# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
class bstack1llll1l1l_opy_:
    def __init__(self, handler):
        self._1111l111l11_opy_ = None
        self.handler = handler
        self._1111l111ll1_opy_ = self.bstack1111l1111ll_opy_()
        self.patch()
    def patch(self):
        self._1111l111l11_opy_ = self._1111l111ll1_opy_.execute
        self._1111l111ll1_opy_.execute = self.bstack1111l111l1l_opy_()
    def bstack1111l111l1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢỊ"), driver_command, None, this, args)
            response = self._1111l111l11_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111lll_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢị"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1111l111ll1_opy_.execute = self._1111l111l11_opy_
    @staticmethod
    def bstack1111l1111ll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver