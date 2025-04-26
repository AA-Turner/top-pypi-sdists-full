# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import builtins
import logging
class bstack11l111ll1l_opy_:
    def __init__(self, handler):
        self._11lll11l1ll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11lll11l1l1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l11lll_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᙣ"), bstack1l11lll_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᙤ"), bstack1l11lll_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨᙥ"), bstack1l11lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᙦ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11lll11l111_opy_
        self._11lll111ll1_opy_()
    def _11lll11l111_opy_(self, *args, **kwargs):
        self._11lll11l1ll_opy_(*args, **kwargs)
        message = bstack1l11lll_opy_ (u"ࠩࠣࠫᙧ").join(map(str, args)) + bstack1l11lll_opy_ (u"ࠪࡠࡳ࠭ᙨ")
        self._log_message(bstack1l11lll_opy_ (u"ࠫࡎࡔࡆࡐࠩᙩ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l11lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᙪ"): level, bstack1l11lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᙫ"): msg})
    def _11lll111ll1_opy_(self):
        for level, bstack11lll111lll_opy_ in self._11lll11l1l1_opy_.items():
            setattr(logging, level, self._11lll11l11l_opy_(level, bstack11lll111lll_opy_))
    def _11lll11l11l_opy_(self, level, bstack11lll111lll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11lll111lll_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11lll11l1ll_opy_
        for level, bstack11lll111lll_opy_ in self._11lll11l1l1_opy_.items():
            setattr(logging, level, bstack11lll111lll_opy_)