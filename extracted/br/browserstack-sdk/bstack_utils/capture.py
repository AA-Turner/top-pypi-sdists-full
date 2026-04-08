# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import builtins
import logging
class bstack1llll111l1l_opy_:
    def __init__(self, handler):
        self._1111l111l11_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._1111l1111l1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack111l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᶚ"), bstack111l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᶛ"), bstack111l_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧᶜ"), bstack111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᶝ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._1111l111l1l_opy_
        self._1111l111111_opy_()
    def _1111l111l1l_opy_(self, *args, **kwargs):
        self._1111l111l11_opy_(*args, **kwargs)
        message = bstack111l_opy_ (u"ࠨࠢࠪᶞ").join(map(str, args)) + bstack111l_opy_ (u"ࠩ࡟ࡲࠬᶟ")
        self._1111l11111l_opy_(bstack111l_opy_ (u"ࠪࡍࡓࡌࡏࠨᶠ"), message)
    def _1111l11111l_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᶡ"): level, bstack111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᶢ"): msg})
    def _1111l111111_opy_(self):
        for level, bstack1111l1111ll_opy_ in self._1111l1111l1_opy_.items():
            setattr(logging, level, self._1111l111ll1_opy_(level, bstack1111l1111ll_opy_))
    def _1111l111ll1_opy_(self, level, bstack1111l1111ll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack1111l1111ll_opy_(msg, *args, **kwargs)
            self._1111l11111l_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._1111l111l11_opy_
        for level, bstack1111l1111ll_opy_ in self._1111l1111l1_opy_.items():
            setattr(logging, level, bstack1111l1111ll_opy_)