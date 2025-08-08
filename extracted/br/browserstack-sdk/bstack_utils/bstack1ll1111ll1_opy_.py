# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1ll1ll1lll_opy_
from bstack_utils.helper import bstack11l1llllll_opy_
logger = logging.getLogger(__name__)
def bstack1l11l1l1l_opy_(bstack11lll11l11_opy_):
  return True if bstack11lll11l11_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll1llll11_opy_(context, *args):
    tags = getattr(args[0], bstack1ll1ll_opy_ (u"ࠧࡵࡣࡪࡷࠬᝯ"), [])
    bstack1l1111111_opy_ = bstack1ll1ll1lll_opy_.bstack1l1111llll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l1111111_opy_
    try:
      bstack11lllll1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11l1l1l_opy_(bstack1ll1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᝰ")) else context.browser
      if bstack11lllll1l1_opy_ and bstack11lllll1l1_opy_.session_id and bstack1l1111111_opy_ and bstack11l1llllll_opy_(
              threading.current_thread(), bstack1ll1ll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᝱"), None):
          threading.current_thread().isA11yTest = bstack1ll1ll1lll_opy_.bstack1l1ll1l1ll_opy_(bstack11lllll1l1_opy_, bstack1l1111111_opy_)
    except Exception as e:
       logger.debug(bstack1ll1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪᝲ").format(str(e)))
def bstack1lll1l11l1_opy_(bstack11lllll1l1_opy_):
    if bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᝳ"), None) and bstack11l1llllll_opy_(
      threading.current_thread(), bstack1ll1ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ᝴"), None) and not bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩ᝵"), False):
      threading.current_thread().a11y_stop = True
      bstack1ll1ll1lll_opy_.bstack1llllll11_opy_(bstack11lllll1l1_opy_, name=bstack1ll1ll_opy_ (u"ࠢࠣ᝶"), path=bstack1ll1ll_opy_ (u"ࠣࠤ᝷"))