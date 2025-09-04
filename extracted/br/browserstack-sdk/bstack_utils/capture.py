# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import builtins
import logging
class bstack111ll1ll1l_opy_:
    def __init__(self, handler):
        self._11ll1111l1l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll11111ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1111l1l_opy_ (u"ࠧࡪࡰࡩࡳࠬង"), bstack1111l1l_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧច"), bstack1111l1l_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪឆ"), bstack1111l1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩជ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll1111l11_opy_
        self._11ll1111lll_opy_()
    def _11ll1111l11_opy_(self, *args, **kwargs):
        self._11ll1111l1l_opy_(*args, **kwargs)
        message = bstack1111l1l_opy_ (u"ࠫࠥ࠭ឈ").join(map(str, args)) + bstack1111l1l_opy_ (u"ࠬࡢ࡮ࠨញ")
        self._log_message(bstack1111l1l_opy_ (u"࠭ࡉࡏࡈࡒࠫដ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1111l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ឋ"): level, bstack1111l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩឌ"): msg})
    def _11ll1111lll_opy_(self):
        for level, bstack11ll1111ll1_opy_ in self._11ll11111ll_opy_.items():
            setattr(logging, level, self._11ll111l111_opy_(level, bstack11ll1111ll1_opy_))
    def _11ll111l111_opy_(self, level, bstack11ll1111ll1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll1111ll1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll1111l1l_opy_
        for level, bstack11ll1111ll1_opy_ in self._11ll11111ll_opy_.items():
            setattr(logging, level, bstack11ll1111ll1_opy_)