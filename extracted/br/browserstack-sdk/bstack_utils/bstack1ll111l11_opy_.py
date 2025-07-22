# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1l1ll11l1l_opy_
from bstack_utils.helper import bstack1ll11lllll_opy_
logger = logging.getLogger(__name__)
def bstack1111ll1l_opy_(bstack1l1l111l1l_opy_):
  return True if bstack1l1l111l1l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l1111l1_opy_(context, *args):
    tags = getattr(args[0], bstack111l111_opy_ (u"ࠫࡹࡧࡧࡴࠩᝳ"), [])
    bstack1ll1ll11l_opy_ = bstack1l1ll11l1l_opy_.bstack11ll111lll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1ll1ll11l_opy_
    try:
      bstack11lll11l1l_opy_ = threading.current_thread().bstackSessionDriver if bstack1111ll1l_opy_(bstack111l111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ᝴")) else context.browser
      if bstack11lll11l1l_opy_ and bstack11lll11l1l_opy_.session_id and bstack1ll1ll11l_opy_ and bstack1ll11lllll_opy_(
              threading.current_thread(), bstack111l111_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᝵"), None):
          threading.current_thread().isA11yTest = bstack1l1ll11l1l_opy_.bstack111l11l1_opy_(bstack11lll11l1l_opy_, bstack1ll1ll11l_opy_)
    except Exception as e:
       logger.debug(bstack111l111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡤ࠵࠶ࡿࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃࠧ᝶").format(str(e)))
def bstack111ll1ll1_opy_(bstack11lll11l1l_opy_):
    if bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ᝷"), None) and bstack1ll11lllll_opy_(
      threading.current_thread(), bstack111l111_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᝸"), None) and not bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠪࡥ࠶࠷ࡹࡠࡵࡷࡳࡵ࠭᝹"), False):
      threading.current_thread().a11y_stop = True
      bstack1l1ll11l1l_opy_.bstack1llllll11_opy_(bstack11lll11l1l_opy_, name=bstack111l111_opy_ (u"ࠦࠧ᝺"), path=bstack111l111_opy_ (u"ࠧࠨ᝻"))