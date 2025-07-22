# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
class bstack1ll11l1l1l_opy_:
    def __init__(self, handler):
        self._11111111l11_opy_ = None
        self.handler = handler
        self._11111111ll1_opy_ = self.bstack11111111l1l_opy_()
        self.patch()
    def patch(self):
        self._11111111l11_opy_ = self._11111111ll1_opy_.execute
        self._11111111ll1_opy_.execute = self.bstack11111111lll_opy_()
    def bstack11111111lll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111l111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣ὞"), driver_command, None, this, args)
            response = self._11111111l11_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111l111_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣὟ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111111ll1_opy_.execute = self._11111111l11_opy_
    @staticmethod
    def bstack11111111l1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver