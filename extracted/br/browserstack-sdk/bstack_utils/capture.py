# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import builtins
import logging
class bstack1lllllllll1_opy_:
    def __init__(self, handler):
        self._111l1ll11l1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111l1ll11ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᮢ"), bstack1l1_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᮣ"), bstack1l1_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧᮤ"), bstack1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᮥ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111l1ll1l11_opy_
        self._111l1ll1ll1_opy_()
    def _111l1ll1l11_opy_(self, *args, **kwargs):
        self._111l1ll11l1_opy_(*args, **kwargs)
        message = bstack1l1_opy_ (u"ࠨࠢࠪᮦ").join(map(str, args)) + bstack1l1_opy_ (u"ࠩ࡟ࡲࠬᮧ")
        self._111l1ll111l_opy_(bstack1l1_opy_ (u"ࠪࡍࡓࡌࡏࠨᮨ"), message)
    def _111l1ll111l_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᮩ"): level, bstack1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ᮪࠭"): msg})
    def _111l1ll1ll1_opy_(self):
        for level, bstack111l1ll1l1l_opy_ in self._111l1ll11ll_opy_.items():
            setattr(logging, level, self._111l1ll1lll_opy_(level, bstack111l1ll1l1l_opy_))
    def _111l1ll1lll_opy_(self, level, bstack111l1ll1l1l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111l1ll1l1l_opy_(msg, *args, **kwargs)
            self._111l1ll111l_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111l1ll11l1_opy_
        for level, bstack111l1ll1l1l_opy_ in self._111l1ll11ll_opy_.items():
            setattr(logging, level, bstack111l1ll1l1l_opy_)