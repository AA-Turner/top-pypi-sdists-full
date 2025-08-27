# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import builtins
import logging
class bstack111ll1l1l1_opy_:
    def __init__(self, handler):
        self._11ll111l11l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll111l111_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1111lll_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ᝿"), bstack1111lll_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩក"), bstack1111lll_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬខ"), bstack1111lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫគ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll111ll11_opy_
        self._11ll111ll1l_opy_()
    def _11ll111ll11_opy_(self, *args, **kwargs):
        self._11ll111l11l_opy_(*args, **kwargs)
        message = bstack1111lll_opy_ (u"࠭ࠠࠨឃ").join(map(str, args)) + bstack1111lll_opy_ (u"ࠧ࡝ࡰࠪង")
        self._log_message(bstack1111lll_opy_ (u"ࠨࡋࡑࡊࡔ࠭ច"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1111lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨឆ"): level, bstack1111lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫជ"): msg})
    def _11ll111ll1l_opy_(self):
        for level, bstack11ll111l1ll_opy_ in self._11ll111l111_opy_.items():
            setattr(logging, level, self._11ll111l1l1_opy_(level, bstack11ll111l1ll_opy_))
    def _11ll111l1l1_opy_(self, level, bstack11ll111l1ll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll111l1ll_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll111l11l_opy_
        for level, bstack11ll111l1ll_opy_ in self._11ll111l111_opy_.items():
            setattr(logging, level, bstack11ll111l1ll_opy_)