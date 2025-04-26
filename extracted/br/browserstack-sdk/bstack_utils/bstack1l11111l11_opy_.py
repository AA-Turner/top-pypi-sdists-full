# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
class bstack11llll11_opy_:
    def __init__(self, handler):
        self._111l111llll_opy_ = None
        self.handler = handler
        self._111l111lll1_opy_ = self.bstack111l111ll11_opy_()
        self.patch()
    def patch(self):
        self._111l111llll_opy_ = self._111l111lll1_opy_.execute
        self._111l111lll1_opy_.execute = self.bstack111l111ll1l_opy_()
    def bstack111l111ll1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l11lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥᶋ"), driver_command, None, this, args)
            response = self._111l111llll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l11lll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥᶌ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l111lll1_opy_.execute = self._111l111llll_opy_
    @staticmethod
    def bstack111l111ll11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver