# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import builtins
import logging
class bstack1llll1llll1_opy_:
    def __init__(self, handler):
        self._111l1l11lll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111l1l1ll1l_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1ll11_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᯋ"), bstack1ll11_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᯌ"), bstack1ll11_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ᯍ"), bstack1ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᯎ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111l1l1l111_opy_
        self._111l1l1l11l_opy_()
    def _111l1l1l111_opy_(self, *args, **kwargs):
        self._111l1l11lll_opy_(*args, **kwargs)
        message = bstack1ll11_opy_ (u"ࠧࠡࠩᯏ").join(map(str, args)) + bstack1ll11_opy_ (u"ࠨ࡞ࡱࠫᯐ")
        self._111l1l1l1l1_opy_(bstack1ll11_opy_ (u"ࠩࡌࡒࡋࡕࠧᯑ"), message)
    def _111l1l1l1l1_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1ll11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᯒ"): level, bstack1ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᯓ"): msg})
    def _111l1l1l11l_opy_(self):
        for level, bstack111l1l1ll11_opy_ in self._111l1l1ll1l_opy_.items():
            setattr(logging, level, self._111l1l1l1ll_opy_(level, bstack111l1l1ll11_opy_))
    def _111l1l1l1ll_opy_(self, level, bstack111l1l1ll11_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111l1l1ll11_opy_(msg, *args, **kwargs)
            self._111l1l1l1l1_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111l1l11lll_opy_
        for level, bstack111l1l1ll11_opy_ in self._111l1l1ll1l_opy_.items():
            setattr(logging, level, bstack111l1l1ll11_opy_)