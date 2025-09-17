# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import builtins
import logging
class bstack111l1llll1_opy_:
    def __init__(self, handler):
        self._11ll1111l1l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll1111ll1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l11ll1_opy_ (u"ࠬ࡯࡮ࡧࡱࠪគ"), bstack1l11ll1_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬឃ"), bstack1l11ll1_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨង"), bstack1l11ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧច")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll1111l11_opy_
        self._11ll1111lll_opy_()
    def _11ll1111l11_opy_(self, *args, **kwargs):
        self._11ll1111l1l_opy_(*args, **kwargs)
        message = bstack1l11ll1_opy_ (u"ࠩࠣࠫឆ").join(map(str, args)) + bstack1l11ll1_opy_ (u"ࠪࡠࡳ࠭ជ")
        self._log_message(bstack1l11ll1_opy_ (u"ࠫࡎࡔࡆࡐࠩឈ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l11ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫញ"): level, bstack1l11ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧដ"): msg})
    def _11ll1111lll_opy_(self):
        for level, bstack11ll11111l1_opy_ in self._11ll1111ll1_opy_.items():
            setattr(logging, level, self._11ll11111ll_opy_(level, bstack11ll11111l1_opy_))
    def _11ll11111ll_opy_(self, level, bstack11ll11111l1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll11111l1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll1111l1l_opy_
        for level, bstack11ll11111l1_opy_ in self._11ll1111ll1_opy_.items():
            setattr(logging, level, bstack11ll11111l1_opy_)