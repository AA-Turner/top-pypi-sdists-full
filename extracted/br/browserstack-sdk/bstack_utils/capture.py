# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import builtins
import logging
class bstack11l11111l1_opy_:
    def __init__(self, handler):
        self._11lll111lll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11lll11l1ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1lll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᙪ"), bstack1l1lll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᙫ"), bstack1l1lll_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨᙬ"), bstack1l1lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᙭")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11lll111ll1_opy_
        self._11lll11l111_opy_()
    def _11lll111ll1_opy_(self, *args, **kwargs):
        self._11lll111lll_opy_(*args, **kwargs)
        message = bstack1l1lll_opy_ (u"ࠩࠣࠫ᙮").join(map(str, args)) + bstack1l1lll_opy_ (u"ࠪࡠࡳ࠭ᙯ")
        self._log_message(bstack1l1lll_opy_ (u"ࠫࡎࡔࡆࡐࠩᙰ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᙱ"): level, bstack1l1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᙲ"): msg})
    def _11lll11l111_opy_(self):
        for level, bstack11lll11l11l_opy_ in self._11lll11l1ll_opy_.items():
            setattr(logging, level, self._11lll11l1l1_opy_(level, bstack11lll11l11l_opy_))
    def _11lll11l1l1_opy_(self, level, bstack11lll11l11l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11lll11l11l_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11lll111lll_opy_
        for level, bstack11lll11l11l_opy_ in self._11lll11l1ll_opy_.items():
            setattr(logging, level, bstack11lll11l11l_opy_)