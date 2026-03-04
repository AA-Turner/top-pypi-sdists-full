# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
class bstack11l111l1ll_opy_:
    def __init__(self, handler):
        self._1lll11l111ll_opy_ = None
        self.handler = handler
        self._1lll11l111l1_opy_ = self.bstack1lll11l11l11_opy_()
        self.patch()
    def patch(self):
        self._1lll11l111ll_opy_ = self._1lll11l111l1_opy_.execute
        self._1lll11l111l1_opy_.execute = self.bstack1lll11l11l1l_opy_()
    def bstack1lll11l11l1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1lll1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢ⎚"), driver_command, None, this, args)
            response = self._1lll11l111ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1lll1l_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢ⎛"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lll11l111l1_opy_.execute = self._1lll11l111ll_opy_
    @staticmethod
    def bstack1lll11l11l11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver