# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import builtins
import logging
class bstack1llllllll1l_opy_:
    def __init__(self, handler):
        self._111l1lll11l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111l1ll1ll1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11lll1_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᮚ"), bstack11lll1_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᮛ"), bstack11lll1_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ᮜ"), bstack11lll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᮝ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111l1ll1lll_opy_
        self._111l1lll1l1_opy_()
    def _111l1ll1lll_opy_(self, *args, **kwargs):
        self._111l1lll11l_opy_(*args, **kwargs)
        message = bstack11lll1_opy_ (u"ࠧࠡࠩᮞ").join(map(str, args)) + bstack11lll1_opy_ (u"ࠨ࡞ࡱࠫᮟ")
        self._111l1ll1l1l_opy_(bstack11lll1_opy_ (u"ࠩࡌࡒࡋࡕࠧᮠ"), message)
    def _111l1ll1l1l_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11lll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᮡ"): level, bstack11lll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᮢ"): msg})
    def _111l1lll1l1_opy_(self):
        for level, bstack111l1lll111_opy_ in self._111l1ll1ll1_opy_.items():
            setattr(logging, level, self._111l1lll1ll_opy_(level, bstack111l1lll111_opy_))
    def _111l1lll1ll_opy_(self, level, bstack111l1lll111_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111l1lll111_opy_(msg, *args, **kwargs)
            self._111l1ll1l1l_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111l1lll11l_opy_
        for level, bstack111l1lll111_opy_ in self._111l1ll1ll1_opy_.items():
            setattr(logging, level, bstack111l1lll111_opy_)