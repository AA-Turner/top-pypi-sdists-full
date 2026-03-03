# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
class bstack1l111l1l1l_opy_:
    def __init__(self, handler):
        self._1lll1l111111_opy_ = None
        self.handler = handler
        self._1lll1l1111ll_opy_ = self.bstack1lll1l11111l_opy_()
        self.patch()
    def patch(self):
        self._1lll1l111111_opy_ = self._1lll1l1111ll_opy_.execute
        self._1lll1l1111ll_opy_.execute = self.bstack1lll1l1111l1_opy_()
    def bstack1lll1l1111l1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥ≰"), driver_command, None, this, args)
            response = self._1lll1l111111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11ll111_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥ≱"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll1l1111ll_opy_.execute = self._1lll1l111111_opy_
    @staticmethod
    def bstack1lll1l11111l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver