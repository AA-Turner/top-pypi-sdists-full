# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
class bstack11111lll_opy_:
    def __init__(self, handler):
        self._1ll11llll11l_opy_ = None
        self.handler = handler
        self._1ll11llll1l1_opy_ = self.bstack1ll11lll1lll_opy_()
        self.patch()
    def patch(self):
        self._1ll11llll11l_opy_ = self._1ll11llll1l1_opy_.execute
        self._1ll11llll1l1_opy_.execute = self.bstack1ll11llll111_opy_()
    def bstack1ll11llll111_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨ⚷"), driver_command, None, this, args)
            response = self._1ll11llll11l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨ⚸"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll11llll1l1_opy_.execute = self._1ll11llll11l_opy_
    @staticmethod
    def bstack1ll11lll1lll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver