# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
class bstack1lll1l1ll_opy_:
    def __init__(self, handler):
        self._1lll1lll1111_opy_ = None
        self.handler = handler
        self._1lll1ll1llll_opy_ = self.bstack1lll1lll11l1_opy_()
        self.patch()
    def patch(self):
        self._1lll1lll1111_opy_ = self._1lll1ll1llll_opy_.execute
        self._1lll1ll1llll_opy_.execute = self.bstack1lll1lll111l_opy_()
    def bstack1lll1lll111l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢỊ"), driver_command, None, this, args)
            response = self._1lll1lll1111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll111_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢị"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll1ll1llll_opy_.execute = self._1lll1lll1111_opy_
    @staticmethod
    def bstack1lll1lll11l1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver