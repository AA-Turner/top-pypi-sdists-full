# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import builtins
import logging
class bstack111llll1ll_opy_:
    def __init__(self, handler):
        self._11lll11l1l1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11lll11l1ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1llllll_opy_ (u"ࠧࡪࡰࡩࡳࠬᙥ"), bstack1llllll_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᙦ"), bstack1llllll_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᙧ"), bstack1llllll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᙨ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11lll111ll1_opy_
        self._11lll11l111_opy_()
    def _11lll111ll1_opy_(self, *args, **kwargs):
        self._11lll11l1l1_opy_(*args, **kwargs)
        message = bstack1llllll_opy_ (u"ࠫࠥ࠭ᙩ").join(map(str, args)) + bstack1llllll_opy_ (u"ࠬࡢ࡮ࠨᙪ")
        self._log_message(bstack1llllll_opy_ (u"࠭ࡉࡏࡈࡒࠫᙫ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1llllll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᙬ"): level, bstack1llllll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᙭"): msg})
    def _11lll11l111_opy_(self):
        for level, bstack11lll11l11l_opy_ in self._11lll11l1ll_opy_.items():
            setattr(logging, level, self._11lll111lll_opy_(level, bstack11lll11l11l_opy_))
    def _11lll111lll_opy_(self, level, bstack11lll11l11l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11lll11l11l_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11lll11l1l1_opy_
        for level, bstack11lll11l11l_opy_ in self._11lll11l1ll_opy_.items():
            setattr(logging, level, bstack11lll11l11l_opy_)