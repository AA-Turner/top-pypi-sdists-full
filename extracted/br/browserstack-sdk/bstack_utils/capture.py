# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import builtins
import logging
class bstack1lllll11l1l_opy_:
    def __init__(self, handler):
        self._111l1l1l1ll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111l1l1ll1l_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1ll1lll_opy_ (u"ࠧࡪࡰࡩࡳࠬᮺ"), bstack1ll1lll_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᮻ"), bstack1ll1lll_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᮼ"), bstack1ll1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᮽ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111l1l1l11l_opy_
        self._111l1l1llll_opy_()
    def _111l1l1l11l_opy_(self, *args, **kwargs):
        self._111l1l1l1ll_opy_(*args, **kwargs)
        message = bstack1ll1lll_opy_ (u"ࠫࠥ࠭ᮾ").join(map(str, args)) + bstack1ll1lll_opy_ (u"ࠬࡢ࡮ࠨᮿ")
        self._111l1l1lll1_opy_(bstack1ll1lll_opy_ (u"࠭ࡉࡏࡈࡒࠫᯀ"), message)
    def _111l1l1lll1_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1ll1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᯁ"): level, bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᯂ"): msg})
    def _111l1l1llll_opy_(self):
        for level, bstack111l1l1l1l1_opy_ in self._111l1l1ll1l_opy_.items():
            setattr(logging, level, self._111l1l1ll11_opy_(level, bstack111l1l1l1l1_opy_))
    def _111l1l1ll11_opy_(self, level, bstack111l1l1l1l1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111l1l1l1l1_opy_(msg, *args, **kwargs)
            self._111l1l1lll1_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111l1l1l1ll_opy_
        for level, bstack111l1l1l1l1_opy_ in self._111l1l1ll1l_opy_.items():
            setattr(logging, level, bstack111l1l1l1l1_opy_)