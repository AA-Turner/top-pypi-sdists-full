# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack11l1111111_opy_
from bstack_utils.helper import bstack1lll111ll_opy_
logger = logging.getLogger(__name__)
def bstack111l1l1l11_opy_(bstack11l11ll111_opy_):
  return True if bstack11l11ll111_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l11lll1ll_opy_(context, *args):
    tags = getattr(args[0], bstack1lll1l_opy_ (u"ࠬࡺࡡࡨࡵࠪ᪒"), [])
    bstack1l1ll11l1_opy_ = bstack11l1111111_opy_.bstack1lll11ll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l1ll11l1_opy_
    try:
      bstack11ll1ll111_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1l1l11_opy_(bstack1lll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ᪓")) else context.browser
      if bstack11ll1ll111_opy_ and bstack11ll1ll111_opy_.session_id and bstack1l1ll11l1_opy_ and bstack1lll111ll_opy_(
              threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭᪔"), None):
          threading.current_thread().isA11yTest = bstack11l1111111_opy_.bstack11ll1lll11_opy_(bstack11ll1ll111_opy_, bstack1l1ll11l1_opy_)
    except Exception as e:
       logger.debug(bstack1lll1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨ᪕").format(str(e)))
def bstack11111llll_opy_(bstack11ll1ll111_opy_):
    if bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭᪖"), None) and bstack1lll111ll_opy_(
      threading.current_thread(), bstack1lll1l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᪗"), None) and not bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧ᪘"), False):
      threading.current_thread().a11y_stop = True
      bstack11l1111111_opy_.bstack11111ll11_opy_(bstack11ll1ll111_opy_, name=bstack1lll1l_opy_ (u"ࠧࠨ᪙"), path=bstack1lll1l_opy_ (u"ࠨࠢ᪚"))