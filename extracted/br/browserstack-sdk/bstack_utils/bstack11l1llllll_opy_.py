# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
class bstack1llll111l1_opy_:
    def __init__(self, handler):
        self._1ll11llll111_opy_ = None
        self.handler = handler
        self._1ll11lll1lll_opy_ = self.bstack1ll11lll1ll1_opy_()
        self.patch()
    def patch(self):
        self._1ll11llll111_opy_ = self._1ll11lll1lll_opy_.execute
        self._1ll11lll1lll_opy_.execute = self.bstack1ll11lll1l1l_opy_()
    def bstack1ll11lll1l1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥ⛐"), driver_command, None, this, args)
            response = self._1ll11llll111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l111l_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥ⛑"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll11lll1lll_opy_.execute = self._1ll11llll111_opy_
    @staticmethod
    def bstack1ll11lll1ll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver