# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1lll11l1_opy_
from bstack_utils.helper import bstack11111ll1l_opy_
logger = logging.getLogger(__name__)
def bstack11ll1l1111_opy_(bstack11l111ll1l_opy_):
  return True if bstack11l111ll1l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l1lll1l1_opy_(context, *args):
    tags = getattr(args[0], bstack11ll1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᜱ"), [])
    bstack1lllllll1l_opy_ = bstack1lll11l1_opy_.bstack1lll11l1l1_opy_(tags)
    threading.current_thread().isA11yTest = bstack1lllllll1l_opy_
    try:
      bstack11ll111lll_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll1l1111_opy_(bstack11ll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᜲ")) else context.browser
      if bstack11ll111lll_opy_ and bstack11ll111lll_opy_.session_id and bstack1lllllll1l_opy_ and bstack11111ll1l_opy_(
              threading.current_thread(), bstack11ll1l1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᜳ"), None):
          threading.current_thread().isA11yTest = bstack1lll11l1_opy_.bstack111ll1l1l_opy_(bstack11ll111lll_opy_, bstack1lllllll1l_opy_)
    except Exception as e:
       logger.debug(bstack11ll1l1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡡ࠲࠳ࡼࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀ᜴ࠫ").format(str(e)))
def bstack1l11l1l1ll_opy_(bstack11ll111lll_opy_):
    if bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ᜵"), None) and bstack11111ll1l_opy_(
      threading.current_thread(), bstack11ll1l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᜶"), None) and not bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࠪ᜷"), False):
      threading.current_thread().a11y_stop = True
      bstack1lll11l1_opy_.bstack11l1l1l1l1_opy_(bstack11ll111lll_opy_, name=bstack11ll1l1_opy_ (u"ࠣࠤ᜸"), path=bstack11ll1l1_opy_ (u"ࠤࠥ᜹"))