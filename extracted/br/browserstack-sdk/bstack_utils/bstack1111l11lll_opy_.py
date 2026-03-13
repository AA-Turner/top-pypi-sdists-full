# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
class bstack1l111l1lll_opy_:
    def __init__(self, handler):
        self._1lll1111ll11_opy_ = None
        self.handler = handler
        self._1lll1111ll1l_opy_ = self.bstack1lll1111l1ll_opy_()
        self.patch()
    def patch(self):
        self._1lll1111ll11_opy_ = self._1lll1111ll1l_opy_.execute
        self._1lll1111ll1l_opy_.execute = self.bstack1lll1111lll1_opy_()
    def bstack1lll1111lll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥ⑚"), driver_command, None, this, args)
            response = self._1lll1111ll11_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1111l_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥ⑛"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll1111ll1l_opy_.execute = self._1lll1111ll11_opy_
    @staticmethod
    def bstack1lll1111l1ll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver