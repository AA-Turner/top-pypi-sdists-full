# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
class bstack111l111l1_opy_:
    def __init__(self, handler):
        self._1lll11ll111l_opy_ = None
        self.handler = handler
        self._1lll11ll1111_opy_ = self.bstack1lll11ll11l1_opy_()
        self.patch()
    def patch(self):
        self._1lll11ll111l_opy_ = self._1lll11ll1111_opy_.execute
        self._1lll11ll1111_opy_.execute = self.bstack1lll11ll11ll_opy_()
    def bstack1lll11ll11ll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࠤ≨"), driver_command, None, this, args)
            response = self._1lll11ll111l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11l11_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࠤ≩"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll11ll1111_opy_.execute = self._1lll11ll111l_opy_
    @staticmethod
    def bstack1lll11ll11l1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver