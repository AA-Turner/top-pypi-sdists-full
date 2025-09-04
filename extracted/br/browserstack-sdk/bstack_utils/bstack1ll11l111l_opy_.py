# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
class bstack11llllll1_opy_:
    def __init__(self, handler):
        self._1lllll1lll1l_opy_ = None
        self.handler = handler
        self._1lllll1lllll_opy_ = self.bstack1lllll1lll11_opy_()
        self.patch()
    def patch(self):
        self._1lllll1lll1l_opy_ = self._1lllll1lllll_opy_.execute
        self._1lllll1lllll_opy_.execute = self.bstack1lllll1llll1_opy_()
    def bstack1lllll1llll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1111l1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥῥ"), driver_command, None, this, args)
            response = self._1lllll1lll1l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1111l1l_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥῦ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lllll1lllll_opy_.execute = self._1lllll1lll1l_opy_
    @staticmethod
    def bstack1lllll1lll11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver