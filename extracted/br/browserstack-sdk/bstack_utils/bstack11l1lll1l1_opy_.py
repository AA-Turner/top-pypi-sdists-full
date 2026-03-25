# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
class bstack1lll1llll1_opy_:
    def __init__(self, handler):
        self._1ll1lll1llll_opy_ = None
        self.handler = handler
        self._1ll1llll111l_opy_ = self.bstack1ll1lll1lll1_opy_()
        self.patch()
    def patch(self):
        self._1ll1lll1llll_opy_ = self._1ll1llll111l_opy_.execute
        self._1ll1llll111l_opy_.execute = self.bstack1ll1llll1111_opy_()
    def bstack1ll1llll1111_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧ⒰"), driver_command, None, this, args)
            response = self._1ll1lll1llll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧ⒱"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1llll111l_opy_.execute = self._1ll1lll1llll_opy_
    @staticmethod
    def bstack1ll1lll1lll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver