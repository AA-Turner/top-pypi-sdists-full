# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack11l11l11ll_opy_
from bstack_utils.helper import bstack1lll11l111_opy_
logger = logging.getLogger(__name__)
def bstack1l1lllll_opy_(bstack1ll1l1lll1_opy_):
  return True if bstack1ll1l1lll1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1llll1l11l_opy_(context, *args):
    tags = getattr(args[0], bstack11ll111_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᥨ"), [])
    bstack11l1llll1_opy_ = bstack11l11l11ll_opy_.bstack1l11ll1111_opy_(tags)
    threading.current_thread().isA11yTest = bstack11l1llll1_opy_
    try:
      bstack111111l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1lllll_opy_(bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᥩ")) else context.browser
      if bstack111111l1_opy_ and bstack111111l1_opy_.session_id and bstack11l1llll1_opy_ and bstack1lll11l111_opy_(
              threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᥪ"), None):
          threading.current_thread().isA11yTest = bstack11l11l11ll_opy_.bstack11lll111l1_opy_(bstack111111l1_opy_, bstack11l1llll1_opy_)
    except Exception as e:
       logger.debug(bstack11ll111_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡡ࠲࠳ࡼࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫᥫ").format(str(e)))
def bstack1l1llll1_opy_(bstack111111l1_opy_):
    if bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᥬ"), None) and bstack1lll11l111_opy_(
      threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᥭ"), None) and not bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࠪ᥮"), False):
      threading.current_thread().a11y_stop = True
      bstack11l11l11ll_opy_.bstack111l1l11l1_opy_(bstack111111l1_opy_, name=bstack11ll111_opy_ (u"ࠣࠤ᥯"), path=bstack11ll111_opy_ (u"ࠤࠥᥰ"))