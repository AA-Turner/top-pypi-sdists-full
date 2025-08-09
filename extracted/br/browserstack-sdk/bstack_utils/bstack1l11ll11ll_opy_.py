# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
class bstack1ll1l1l1l_opy_:
    def __init__(self, handler):
        self._1llllll1lll1_opy_ = None
        self.handler = handler
        self._1llllll1ll1l_opy_ = self.bstack1llllll1ll11_opy_()
        self.patch()
    def patch(self):
        self._1llllll1lll1_opy_ = self._1llllll1ll1l_opy_.execute
        self._1llllll1ll1l_opy_.execute = self.bstack1llllll1llll_opy_()
    def bstack1llllll1llll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࠦῦ"), driver_command, None, this, args)
            response = self._1llllll1lll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11l1_opy_ (u"ࠧࡧࡦࡵࡧࡵࠦῧ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llllll1ll1l_opy_.execute = self._1llllll1lll1_opy_
    @staticmethod
    def bstack1llllll1ll11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver