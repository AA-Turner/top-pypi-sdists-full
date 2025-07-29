# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack11ll1ll11_opy_
from bstack_utils.helper import bstack11ll1111ll_opy_
logger = logging.getLogger(__name__)
def bstack1lll1l11l1_opy_(bstack11l111ll1l_opy_):
  return True if bstack11l111ll1l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11l1l11111_opy_(context, *args):
    tags = getattr(args[0], bstackl_opy_ (u"ࠧࡵࡣࡪࡷࠬᝯ"), [])
    bstack111l1l1l1_opy_ = bstack11ll1ll11_opy_.bstack1l111lll_opy_(tags)
    threading.current_thread().isA11yTest = bstack111l1l1l1_opy_
    try:
      bstack1l11l111l_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1l11l1_opy_(bstackl_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᝰ")) else context.browser
      if bstack1l11l111l_opy_ and bstack1l11l111l_opy_.session_id and bstack111l1l1l1_opy_ and bstack11ll1111ll_opy_(
              threading.current_thread(), bstackl_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᝱"), None):
          threading.current_thread().isA11yTest = bstack11ll1ll11_opy_.bstack1ll1l11111_opy_(bstack1l11l111l_opy_, bstack111l1l1l1_opy_)
    except Exception as e:
       logger.debug(bstackl_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪᝲ").format(str(e)))
def bstack1l11l11111_opy_(bstack1l11l111l_opy_):
    if bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᝳ"), None) and bstack11ll1111ll_opy_(
      threading.current_thread(), bstackl_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ᝴"), None) and not bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩ᝵"), False):
      threading.current_thread().a11y_stop = True
      bstack11ll1ll11_opy_.bstack11ll11111l_opy_(bstack1l11l111l_opy_, name=bstackl_opy_ (u"ࠢࠣ᝶"), path=bstackl_opy_ (u"ࠣࠤ᝷"))