# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
class bstack11lll1l11_opy_:
    def __init__(self, handler):
        self._1ll11ll1l1l1_opy_ = None
        self.handler = handler
        self._1ll11ll1l1ll_opy_ = self.bstack1ll11ll1l111_opy_()
        self.patch()
    def patch(self):
        self._1ll11ll1l1l1_opy_ = self._1ll11ll1l1ll_opy_.execute
        self._1ll11ll1l1ll_opy_.execute = self.bstack1ll11ll1l11l_opy_()
    def bstack1ll11ll1l11l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥ⛬"), driver_command, None, this, args)
            response = self._1ll11ll1l1l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1111l_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥ⛭"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll11ll1l1ll_opy_.execute = self._1ll11ll1l1l1_opy_
    @staticmethod
    def bstack1ll11ll1l111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver