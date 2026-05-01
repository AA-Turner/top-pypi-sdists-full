# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
class bstack1llll1l111_opy_:
    def __init__(self, handler):
        self._1ll11ll1l111_opy_ = None
        self.handler = handler
        self._1ll11ll11ll1_opy_ = self.bstack1ll11ll11l1l_opy_()
        self.patch()
    def patch(self):
        self._1ll11ll1l111_opy_ = self._1ll11ll11ll1_opy_.execute
        self._1ll11ll11ll1_opy_.execute = self.bstack1ll11ll11lll_opy_()
    def bstack1ll11ll11lll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢ✶"), driver_command, None, this, args)
            response = self._1ll11ll1l111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111ll_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢ✷"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll11ll11ll1_opy_.execute = self._1ll11ll1l111_opy_
    @staticmethod
    def bstack1ll11ll11l1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver