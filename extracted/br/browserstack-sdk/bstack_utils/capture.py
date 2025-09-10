# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import builtins
import logging
class bstack111ll111l1_opy_:
    def __init__(self, handler):
        self._11l1llll1ll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11l1llll111_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1ll11ll_opy_ (u"ࠫ࡮ࡴࡦࡰࠩឈ"), bstack1ll11ll_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫញ"), bstack1ll11ll_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧដ"), bstack1ll11ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ឋ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11l1llll1l1_opy_
        self._11l1lll1lll_opy_()
    def _11l1llll1l1_opy_(self, *args, **kwargs):
        self._11l1llll1ll_opy_(*args, **kwargs)
        message = bstack1ll11ll_opy_ (u"ࠨࠢࠪឌ").join(map(str, args)) + bstack1ll11ll_opy_ (u"ࠩ࡟ࡲࠬឍ")
        self._log_message(bstack1ll11ll_opy_ (u"ࠪࡍࡓࡌࡏࠨណ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1ll11ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪត"): level, bstack1ll11ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ថ"): msg})
    def _11l1lll1lll_opy_(self):
        for level, bstack11l1lllll11_opy_ in self._11l1llll111_opy_.items():
            setattr(logging, level, self._11l1llll11l_opy_(level, bstack11l1lllll11_opy_))
    def _11l1llll11l_opy_(self, level, bstack11l1lllll11_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11l1lllll11_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11l1llll1ll_opy_
        for level, bstack11l1lllll11_opy_ in self._11l1llll111_opy_.items():
            setattr(logging, level, bstack11l1lllll11_opy_)