# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
class bstack11l1lll1ll_opy_:
    def __init__(self, handler):
        self._11111111lll_opy_ = None
        self.handler = handler
        self._11111111ll1_opy_ = self.bstack1111111l111_opy_()
        self.patch()
    def patch(self):
        self._11111111lll_opy_ = self._11111111ll1_opy_.execute
        self._11111111ll1_opy_.execute = self.bstack1111111l11l_opy_()
    def bstack1111111l11l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11l1111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࠦ὚"), driver_command, None, this, args)
            response = self._11111111lll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11l1111_opy_ (u"ࠧࡧࡦࡵࡧࡵࠦὛ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111111ll1_opy_.execute = self._11111111lll_opy_
    @staticmethod
    def bstack1111111l111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver