# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import builtins
import logging
class bstack111ll1lll1_opy_:
    def __init__(self, handler):
        self._11ll1l11l1l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll1l11lll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack111lll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᜋ"), bstack111lll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᜌ"), bstack111lll_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨᜍ"), bstack111lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᜎ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll1l11l11_opy_
        self._11ll1l11ll1_opy_()
    def _11ll1l11l11_opy_(self, *args, **kwargs):
        self._11ll1l11l1l_opy_(*args, **kwargs)
        message = bstack111lll_opy_ (u"ࠩࠣࠫᜏ").join(map(str, args)) + bstack111lll_opy_ (u"ࠪࡠࡳ࠭ᜐ")
        self._log_message(bstack111lll_opy_ (u"ࠫࡎࡔࡆࡐࠩᜑ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack111lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᜒ"): level, bstack111lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᜓ"): msg})
    def _11ll1l11ll1_opy_(self):
        for level, bstack11ll1l1l111_opy_ in self._11ll1l11lll_opy_.items():
            setattr(logging, level, self._11ll1l111ll_opy_(level, bstack11ll1l1l111_opy_))
    def _11ll1l111ll_opy_(self, level, bstack11ll1l1l111_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll1l1l111_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll1l11l1l_opy_
        for level, bstack11ll1l1l111_opy_ in self._11ll1l11lll_opy_.items():
            setattr(logging, level, bstack11ll1l1l111_opy_)