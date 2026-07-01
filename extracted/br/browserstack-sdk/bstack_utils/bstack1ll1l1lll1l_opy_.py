# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
class bstack1llllllllll_opy_:
    def __init__(self, handler):
        self._1ll1111ll111_opy_ = None
        self.handler = handler
        self._1ll1111ll1l1_opy_ = self.bstack1ll1111l1lll_opy_()
        self.patch()
    def patch(self):
        self._1ll1111ll111_opy_ = self._1ll1111ll1l1_opy_.execute
        self._1ll1111ll1l1_opy_.execute = self.bstack1ll1111ll11l_opy_()
    def bstack1ll1111ll11l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥ⩳"), driver_command, None, this, args)
            response = self._1ll1111ll111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1llll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥ⩴"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1111ll1l1_opy_.execute = self._1ll1111ll111_opy_
    @staticmethod
    def bstack1ll1111l1lll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver