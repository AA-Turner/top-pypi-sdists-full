# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import builtins
import logging
class bstack111ll1lll1_opy_:
    def __init__(self, handler):
        self._11ll11ll111_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll11l1l11_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11ll11_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ᜙"), bstack11ll11_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬ᜚"), bstack11ll11_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨ᜛"), bstack11ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᜜")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll11l1lll_opy_
        self._11ll11l1l1l_opy_()
    def _11ll11l1lll_opy_(self, *args, **kwargs):
        self._11ll11ll111_opy_(*args, **kwargs)
        message = bstack11ll11_opy_ (u"ࠩࠣࠫ᜝").join(map(str, args)) + bstack11ll11_opy_ (u"ࠪࡠࡳ࠭᜞")
        self._log_message(bstack11ll11_opy_ (u"ࠫࡎࡔࡆࡐࠩᜟ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11ll11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᜠ"): level, bstack11ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᜡ"): msg})
    def _11ll11l1l1l_opy_(self):
        for level, bstack11ll11ll11l_opy_ in self._11ll11l1l11_opy_.items():
            setattr(logging, level, self._11ll11l1ll1_opy_(level, bstack11ll11ll11l_opy_))
    def _11ll11l1ll1_opy_(self, level, bstack11ll11ll11l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll11ll11l_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll11ll111_opy_
        for level, bstack11ll11ll11l_opy_ in self._11ll11l1l11_opy_.items():
            setattr(logging, level, bstack11ll11ll11l_opy_)