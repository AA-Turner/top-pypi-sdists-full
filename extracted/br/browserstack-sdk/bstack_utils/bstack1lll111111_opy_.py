# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
class bstack1l1ll111l1_opy_:
    def __init__(self, handler):
        self._1ll1l11111l1_opy_ = None
        self.handler = handler
        self._1ll1l111111l_opy_ = self.bstack1ll1l1111111_opy_()
        self.patch()
    def patch(self):
        self._1ll1l11111l1_opy_ = self._1ll1l111111l_opy_.execute
        self._1ll1l111111l_opy_.execute = self.bstack1ll11lllllll_opy_()
    def bstack1ll11lllllll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll1l11_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨ⚰"), driver_command, None, this, args)
            response = self._1ll1l11111l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll1l11_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨ⚱"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1l111111l_opy_.execute = self._1ll1l11111l1_opy_
    @staticmethod
    def bstack1ll1l1111111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver