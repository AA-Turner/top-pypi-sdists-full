# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
class bstack11l1l11111_opy_:
    def __init__(self, handler):
        self._111111l1l11_opy_ = None
        self.handler = handler
        self._111111l11ll_opy_ = self.bstack111111l111l_opy_()
        self.patch()
    def patch(self):
        self._111111l1l11_opy_ = self._111111l11ll_opy_.execute
        self._111111l11ll_opy_.execute = self.bstack111111l11l1_opy_()
    def bstack111111l11l1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1l1l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࠦỸ"), driver_command, None, this, args)
            response = self._111111l1l11_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1l1l1_opy_ (u"ࠧࡧࡦࡵࡧࡵࠦỹ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111111l11ll_opy_.execute = self._111111l1l11_opy_
    @staticmethod
    def bstack111111l111l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver