# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
class bstack1l1l11l111_opy_:
    def __init__(self, handler):
        self._111111l11l1_opy_ = None
        self.handler = handler
        self._111111l11ll_opy_ = self.bstack111111l1l11_opy_()
        self.patch()
    def patch(self):
        self._111111l11l1_opy_ = self._111111l11ll_opy_.execute
        self._111111l11ll_opy_.execute = self.bstack111111l111l_opy_()
    def bstack111111l111l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11ll11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥỷ"), driver_command, None, this, args)
            response = self._111111l11l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11ll11_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥỸ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111111l11ll_opy_.execute = self._111111l11l1_opy_
    @staticmethod
    def bstack111111l1l11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver