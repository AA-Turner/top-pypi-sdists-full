# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import builtins
import logging
class bstack111ll1l1l1_opy_:
    def __init__(self, handler):
        self._11ll111ll1l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll111lll1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11l1_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ᝹"), bstack11l1_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪ᝺"), bstack11l1_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭᝻"), bstack11l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ᝼")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll111llll_opy_
        self._11ll111l1ll_opy_()
    def _11ll111llll_opy_(self, *args, **kwargs):
        self._11ll111ll1l_opy_(*args, **kwargs)
        message = bstack11l1_opy_ (u"ࠧࠡࠩ᝽").join(map(str, args)) + bstack11l1_opy_ (u"ࠨ࡞ࡱࠫ᝾")
        self._log_message(bstack11l1_opy_ (u"ࠩࡌࡒࡋࡕࠧ᝿"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩក"): level, bstack11l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬខ"): msg})
    def _11ll111l1ll_opy_(self):
        for level, bstack11ll111ll11_opy_ in self._11ll111lll1_opy_.items():
            setattr(logging, level, self._11ll111l1l1_opy_(level, bstack11ll111ll11_opy_))
    def _11ll111l1l1_opy_(self, level, bstack11ll111ll11_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll111ll11_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll111ll1l_opy_
        for level, bstack11ll111ll11_opy_ in self._11ll111lll1_opy_.items():
            setattr(logging, level, bstack11ll111ll11_opy_)