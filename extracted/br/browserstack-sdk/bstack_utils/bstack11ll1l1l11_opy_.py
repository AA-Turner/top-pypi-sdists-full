# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
class bstack1lll11111_opy_:
    def __init__(self, handler):
        self._1ll1llll11l1_opy_ = None
        self.handler = handler
        self._1ll1llll111l_opy_ = self.bstack1ll1llll1111_opy_()
        self.patch()
    def patch(self):
        self._1ll1llll11l1_opy_ = self._1ll1llll111l_opy_.execute
        self._1ll1llll111l_opy_.execute = self.bstack1ll1lll1llll_opy_()
    def bstack1ll1lll1llll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll1lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢ⒫"), driver_command, None, this, args)
            response = self._1ll1llll11l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll1lll_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢ⒬"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1llll111l_opy_.execute = self._1ll1llll11l1_opy_
    @staticmethod
    def bstack1ll1llll1111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver