# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
class bstack1l1lllllll_opy_:
    def __init__(self, handler):
        self._11111111ll1_opy_ = None
        self.handler = handler
        self._11111111l1l_opy_ = self.bstack11111111l11_opy_()
        self.patch()
    def patch(self):
        self._11111111ll1_opy_ = self._11111111l1l_opy_.execute
        self._11111111l1l_opy_.execute = self.bstack111111111ll_opy_()
    def bstack111111111ll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstackl_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࠤὟ"), driver_command, None, this, args)
            response = self._11111111ll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstackl_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࠤὠ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111111l1l_opy_.execute = self._11111111ll1_opy_
    @staticmethod
    def bstack11111111l11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver