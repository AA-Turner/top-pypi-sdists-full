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
import threading
import logging
import bstack_utils.accessibility as bstack1ll1ll1111_opy_
from bstack_utils.helper import bstack1ll11l11ll_opy_
logger = logging.getLogger(__name__)
def bstack11ll1l1l1_opy_(bstack1ll1l1ll1l_opy_):
  return True if bstack1ll1l1ll1l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1llll1lll_opy_(context, *args):
    tags = getattr(args[0], bstack11l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᝰ"), [])
    bstack111ll11l_opy_ = bstack1ll1ll1111_opy_.bstack1ll11ll11_opy_(tags)
    threading.current_thread().isA11yTest = bstack111ll11l_opy_
    try:
      bstack111ll1ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll1l1l1_opy_(bstack11l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ᝱")) else context.browser
      if bstack111ll1ll1_opy_ and bstack111ll1ll1_opy_.session_id and bstack111ll11l_opy_ and bstack1ll11l11ll_opy_(
              threading.current_thread(), bstack11l1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᝲ"), None):
          threading.current_thread().isA11yTest = bstack1ll1ll1111_opy_.bstack1ll1lll1ll_opy_(bstack111ll1ll1_opy_, bstack111ll11l_opy_)
    except Exception as e:
       logger.debug(bstack11l1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡡ࠲࠳ࡼࠤ࡮ࡴࠠࡣࡧ࡫ࡥࡻ࡫࠺ࠡࡽࢀࠫᝳ").format(str(e)))
def bstack111l11lll_opy_(bstack111ll1ll1_opy_):
    if bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ᝴"), None) and bstack1ll11l11ll_opy_(
      threading.current_thread(), bstack11l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᝵"), None) and not bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࠪ᝶"), False):
      threading.current_thread().a11y_stop = True
      bstack1ll1ll1111_opy_.bstack1ll1l1lll1_opy_(bstack111ll1ll1_opy_, name=bstack11l1_opy_ (u"ࠣࠤ᝷"), path=bstack11l1_opy_ (u"ࠤࠥ᝸"))