# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import builtins
import logging
class bstack111lll1111_opy_:
    def __init__(self, handler):
        self._11ll111lll1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll111llll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1ll1_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ᜺"), bstack1l1ll1_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪ᜻"), bstack1l1ll1_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭᜼"), bstack1l1ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ᜽")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll11l11l1_opy_
        self._11ll11l111l_opy_()
    def _11ll11l11l1_opy_(self, *args, **kwargs):
        self._11ll111lll1_opy_(*args, **kwargs)
        message = bstack1l1ll1_opy_ (u"ࠧࠡࠩ᜾").join(map(str, args)) + bstack1l1ll1_opy_ (u"ࠨ࡞ࡱࠫ᜿")
        self._log_message(bstack1l1ll1_opy_ (u"ࠩࡌࡒࡋࡕࠧᝀ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᝁ"): level, bstack1l1ll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᝂ"): msg})
    def _11ll11l111l_opy_(self):
        for level, bstack11ll11l11ll_opy_ in self._11ll111llll_opy_.items():
            setattr(logging, level, self._11ll11l1111_opy_(level, bstack11ll11l11ll_opy_))
    def _11ll11l1111_opy_(self, level, bstack11ll11l11ll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll11l11ll_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll111lll1_opy_
        for level, bstack11ll11l11ll_opy_ in self._11ll111llll_opy_.items():
            setattr(logging, level, bstack11ll11l11ll_opy_)