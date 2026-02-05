# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
class bstack1ll111l111_opy_:
    def __init__(self, handler):
        self._1lll1ll1ll11_opy_ = None
        self.handler = handler
        self._1lll1ll1l1l1_opy_ = self.bstack1lll1ll1l1ll_opy_()
        self.patch()
    def patch(self):
        self._1lll1ll1ll11_opy_ = self._1lll1ll1l1l1_opy_.execute
        self._1lll1ll1l1l1_opy_.execute = self.bstack1lll1ll1l11l_opy_()
    def bstack1lll1ll1l11l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11l1ll1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࠦⅼ"), driver_command, None, this, args)
            response = self._1lll1ll1ll11_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11l1ll1_opy_ (u"ࠧࡧࡦࡵࡧࡵࠦⅽ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll1ll1l1l1_opy_.execute = self._1lll1ll1ll11_opy_
    @staticmethod
    def bstack1lll1ll1l1ll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver