# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
class bstack11llll11l1_opy_:
    def __init__(self, handler):
        self._1llllll1l1ll_opy_ = None
        self.handler = handler
        self._1llllll1l111_opy_ = self.bstack1llllll1l1l1_opy_()
        self.patch()
    def patch(self):
        self._1llllll1l1ll_opy_ = self._1llllll1l111_opy_.execute
        self._1llllll1l111_opy_.execute = self.bstack1llllll1l11l_opy_()
    def bstack1llllll1l11l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥῥ"), driver_command, None, this, args)
            response = self._1llllll1l1ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l11l11_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥῦ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llllll1l111_opy_.execute = self._1llllll1l1ll_opy_
    @staticmethod
    def bstack1llllll1l1l1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver