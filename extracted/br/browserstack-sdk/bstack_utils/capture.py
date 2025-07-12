# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import builtins
import logging
class bstack111ll11l1l_opy_:
    def __init__(self, handler):
        self._11l111l11l1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11l111l11ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11l1111_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᠰ"), bstack11l1111_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᠱ"), bstack11l1111_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧᠲ"), bstack11l1111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᠳ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11l1111lll1_opy_
        self._11l1111llll_opy_()
    def _11l1111lll1_opy_(self, *args, **kwargs):
        self._11l111l11l1_opy_(*args, **kwargs)
        message = bstack11l1111_opy_ (u"ࠨࠢࠪᠴ").join(map(str, args)) + bstack11l1111_opy_ (u"ࠩ࡟ࡲࠬᠵ")
        self._log_message(bstack11l1111_opy_ (u"ࠪࡍࡓࡌࡏࠨᠶ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11l1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᠷ"): level, bstack11l1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᠸ"): msg})
    def _11l1111llll_opy_(self):
        for level, bstack11l111l1111_opy_ in self._11l111l11ll_opy_.items():
            setattr(logging, level, self._11l111l111l_opy_(level, bstack11l111l1111_opy_))
    def _11l111l111l_opy_(self, level, bstack11l111l1111_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11l111l1111_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11l111l11l1_opy_
        for level, bstack11l111l1111_opy_ in self._11l111l11ll_opy_.items():
            setattr(logging, level, bstack11l111l1111_opy_)