# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import builtins
import logging
class bstack111lll1l1l_opy_:
    def __init__(self, handler):
        self._11ll111l11l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll1111ll1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstackl_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ᝸"), bstackl_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩ᝹"), bstackl_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬ᝺"), bstackl_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ᝻")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll111l1ll_opy_
        self._11ll111l1l1_opy_()
    def _11ll111l1ll_opy_(self, *args, **kwargs):
        self._11ll111l11l_opy_(*args, **kwargs)
        message = bstackl_opy_ (u"࠭ࠠࠨ᝼").join(map(str, args)) + bstackl_opy_ (u"ࠧ࡝ࡰࠪ᝽")
        self._log_message(bstackl_opy_ (u"ࠨࡋࡑࡊࡔ࠭᝾"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstackl_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ᝿"): level, bstackl_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫក"): msg})
    def _11ll111l1l1_opy_(self):
        for level, bstack11ll111l111_opy_ in self._11ll1111ll1_opy_.items():
            setattr(logging, level, self._11ll1111lll_opy_(level, bstack11ll111l111_opy_))
    def _11ll1111lll_opy_(self, level, bstack11ll111l111_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll111l111_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll111l11l_opy_
        for level, bstack11ll111l111_opy_ in self._11ll1111ll1_opy_.items():
            setattr(logging, level, bstack11ll111l111_opy_)