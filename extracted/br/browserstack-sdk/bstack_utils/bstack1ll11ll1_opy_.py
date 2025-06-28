# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
class bstack11l1l1111_opy_:
    def __init__(self, handler):
        self._1111111ll1l_opy_ = None
        self.handler = handler
        self._1111111l1ll_opy_ = self.bstack1111111ll11_opy_()
        self.patch()
    def patch(self):
        self._1111111ll1l_opy_ = self._1111111l1ll_opy_.execute
        self._1111111l1ll_opy_.execute = self.bstack1111111lll1_opy_()
    def bstack1111111lll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1ll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣἘ"), driver_command, None, this, args)
            response = self._1111111ll1l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1ll1_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣἙ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1111111l1ll_opy_.execute = self._1111111ll1l_opy_
    @staticmethod
    def bstack1111111ll11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver