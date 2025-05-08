# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
class bstack11l1lll1ll_opy_:
    def __init__(self, handler):
        self._111l111lll1_opy_ = None
        self.handler = handler
        self._111l111ll1l_opy_ = self.bstack111l111ll11_opy_()
        self.patch()
    def patch(self):
        self._111l111lll1_opy_ = self._111l111ll1l_opy_.execute
        self._111l111ll1l_opy_.execute = self.bstack111l111llll_opy_()
    def bstack111l111llll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥᶒ"), driver_command, None, this, args)
            response = self._111l111lll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1lll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥᶓ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111l111ll1l_opy_.execute = self._111l111lll1_opy_
    @staticmethod
    def bstack111l111ll11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver