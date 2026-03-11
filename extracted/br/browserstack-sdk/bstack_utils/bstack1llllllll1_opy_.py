# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1ll11lll11_opy_
from bstack_utils.helper import bstack11llll11l_opy_
logger = logging.getLogger(__name__)
def bstack1ll1ll1ll_opy_(bstack1ll111l1ll_opy_):
  return True if bstack1ll111l1ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack111ll1l1ll_opy_(context, *args):
    tags = getattr(args[0], bstack1ll111_opy_ (u"ࠬࡺࡡࡨࡵࠪ≝"), [])
    bstack111lll1lll_opy_ = bstack1ll11lll11_opy_.bstack11l1llll11_opy_(tags)
    threading.current_thread().isA11yTest = bstack111lll1lll_opy_
    try:
      bstack11l11l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1ll1ll_opy_(bstack1ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ≞")) else context.browser
      if bstack11l11l11_opy_ and bstack11l11l11_opy_.session_id and bstack111lll1lll_opy_ and bstack11llll11l_opy_(
              threading.current_thread(), bstack1ll111_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭≟"), None):
          threading.current_thread().isA11yTest = bstack1ll11lll11_opy_.bstack11ll1l1l_opy_(bstack11l11l11_opy_, bstack111lll1lll_opy_)
    except Exception as e:
       logger.debug(bstack1ll111_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨ≠").format(str(e)))
def bstack1111lll1ll_opy_(bstack11l11l11_opy_):
    if bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭≡"), None) and bstack11llll11l_opy_(
      threading.current_thread(), bstack1ll111_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ≢"), None) and not bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧ≣"), False):
      threading.current_thread().a11y_stop = True
      bstack1ll11lll11_opy_.bstack11lll1lll1_opy_(bstack11l11l11_opy_, name=bstack1ll111_opy_ (u"ࠧࠨ≤"), path=bstack1ll111_opy_ (u"ࠨࠢ≥"))