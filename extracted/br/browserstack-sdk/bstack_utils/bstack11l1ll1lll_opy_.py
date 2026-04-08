# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
class bstack111ll11l1_opy_:
    def __init__(self, handler):
        self._1ll11lllll1l_opy_ = None
        self.handler = handler
        self._1ll11llllll1_opy_ = self.bstack1ll1l1111111_opy_()
        self.patch()
    def patch(self):
        self._1ll11lllll1l_opy_ = self._1ll11llllll1_opy_.execute
        self._1ll11llllll1_opy_.execute = self.bstack1ll11lllllll_opy_()
    def bstack1ll11lllllll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࠤ⚳"), driver_command, None, this, args)
            response = self._1ll11lllll1l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111l_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࠤ⚴"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll11llllll1_opy_.execute = self._1ll11lllll1l_opy_
    @staticmethod
    def bstack1ll1l1111111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver