# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
class bstack1ll111l1l_opy_:
    def __init__(self, handler):
        self._1llllll111l1_opy_ = None
        self.handler = handler
        self._1llllll111ll_opy_ = self.bstack1llllll1111l_opy_()
        self.patch()
    def patch(self):
        self._1llllll111l1_opy_ = self._1llllll111ll_opy_.execute
        self._1llllll111ll_opy_.execute = self.bstack1llllll11l11_opy_()
    def bstack1llllll11l11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1111lll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧῠ"), driver_command, None, this, args)
            response = self._1llllll111l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1111lll_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧῡ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llllll111ll_opy_.execute = self._1llllll111l1_opy_
    @staticmethod
    def bstack1llllll1111l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver