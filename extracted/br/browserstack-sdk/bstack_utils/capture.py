# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import builtins
import logging
class bstack1llll11l1l1_opy_:
    def __init__(self, handler):
        self._1111l111ll1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._1111l1111ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᶚ"), bstack1ll1l11_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᶛ"), bstack1ll1l11_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧᶜ"), bstack1ll1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᶝ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._1111l1111l1_opy_
        self._1111l111l11_opy_()
    def _1111l1111l1_opy_(self, *args, **kwargs):
        self._1111l111ll1_opy_(*args, **kwargs)
        message = bstack1ll1l11_opy_ (u"ࠨࠢࠪᶞ").join(map(str, args)) + bstack1ll1l11_opy_ (u"ࠩ࡟ࡲࠬᶟ")
        self._1111l111111_opy_(bstack1ll1l11_opy_ (u"ࠪࡍࡓࡌࡏࠨᶠ"), message)
    def _1111l111111_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1ll1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᶡ"): level, bstack1ll1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᶢ"): msg})
    def _1111l111l11_opy_(self):
        for level, bstack1111l111l1l_opy_ in self._1111l1111ll_opy_.items():
            setattr(logging, level, self._1111l11111l_opy_(level, bstack1111l111l1l_opy_))
    def _1111l11111l_opy_(self, level, bstack1111l111l1l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack1111l111l1l_opy_(msg, *args, **kwargs)
            self._1111l111111_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._1111l111ll1_opy_
        for level, bstack1111l111l1l_opy_ in self._1111l1111ll_opy_.items():
            setattr(logging, level, bstack1111l111l1l_opy_)