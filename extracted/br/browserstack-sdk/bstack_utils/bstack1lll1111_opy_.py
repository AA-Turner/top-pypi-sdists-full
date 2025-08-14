# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
class bstack1l11lllll_opy_:
    def __init__(self, handler):
        self._1llllll1ll11_opy_ = None
        self.handler = handler
        self._1llllll1l1l1_opy_ = self.bstack1llllll1ll1l_opy_()
        self.patch()
    def patch(self):
        self._1llllll1ll11_opy_ = self._1llllll1l1l1_opy_.execute
        self._1llllll1l1l1_opy_.execute = self.bstack1llllll1l1ll_opy_()
    def bstack1llllll1l1ll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1l1ll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥῳ"), driver_command, None, this, args)
            response = self._1llllll1ll11_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1l1ll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥῴ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llllll1l1l1_opy_.execute = self._1llllll1ll11_opy_
    @staticmethod
    def bstack1llllll1ll1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver