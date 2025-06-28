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
import threading
import logging
import bstack_utils.accessibility as bstack1l11ll1lll_opy_
from bstack_utils.helper import bstack11l1ll11ll_opy_
logger = logging.getLogger(__name__)
def bstack1ll1lll1l_opy_(bstack1ll1l111_opy_):
  return True if bstack1ll1l111_opy_ in threading.current_thread().__dict__.keys() else False
def bstack111llll1_opy_(context, *args):
    tags = getattr(args[0], bstack1l1ll1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᜱ"), [])
    bstack1l1111l11l_opy_ = bstack1l11ll1lll_opy_.bstack11l11l11_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l1111l11l_opy_
    try:
      bstack1llll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1lll1l_opy_(bstack1l1ll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᜲ")) else context.browser
      if bstack1llll1l1_opy_ and bstack1llll1l1_opy_.session_id and bstack1l1111l11l_opy_ and bstack11l1ll11ll_opy_(
              threading.current_thread(), bstack1l1ll1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᜳ"), None):
          threading.current_thread().isA11yTest = bstack1l11ll1lll_opy_.bstack1llll1l11_opy_(bstack1llll1l1_opy_, bstack1l1111l11l_opy_)
    except Exception as e:
       logger.debug(bstack1l1ll1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡡ࠲࠳ࡼࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀ᜴ࠫ").format(str(e)))
def bstack1l1l11l1l1_opy_(bstack1llll1l1_opy_):
    if bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ᜵"), None) and bstack11l1ll11ll_opy_(
      threading.current_thread(), bstack1l1ll1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᜶"), None) and not bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࠪ᜷"), False):
      threading.current_thread().a11y_stop = True
      bstack1l11ll1lll_opy_.bstack11ll11l1_opy_(bstack1llll1l1_opy_, name=bstack1l1ll1_opy_ (u"ࠣࠤ᜸"), path=bstack1l1ll1_opy_ (u"ࠤࠥ᜹"))