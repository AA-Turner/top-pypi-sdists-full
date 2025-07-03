# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack11l111l11_opy_
from bstack_utils.helper import bstack1ll11lll1l_opy_
logger = logging.getLogger(__name__)
def bstack111lll1l1_opy_(bstack1llll111ll_opy_):
  return True if bstack1llll111ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11l1111111_opy_(context, *args):
    tags = getattr(args[0], bstack1l1_opy_ (u"ࠧࡵࡣࡪࡷࠬᝨ"), [])
    bstack1111l1ll1_opy_ = bstack11l111l11_opy_.bstack11l1111ll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1111l1ll1_opy_
    try:
      bstack11lll11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack111lll1l1_opy_(bstack1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᝩ")) else context.browser
      if bstack11lll11lll_opy_ and bstack11lll11lll_opy_.session_id and bstack1111l1ll1_opy_ and bstack1ll11lll1l_opy_(
              threading.current_thread(), bstack1l1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᝪ"), None):
          threading.current_thread().isA11yTest = bstack11l111l11_opy_.bstack11l11l1l_opy_(bstack11lll11lll_opy_, bstack1111l1ll1_opy_)
    except Exception as e:
       logger.debug(bstack1l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪᝫ").format(str(e)))
def bstack11ll1ll1_opy_(bstack11lll11lll_opy_):
    if bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᝬ"), None) and bstack1ll11lll1l_opy_(
      threading.current_thread(), bstack1l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ᝭"), None) and not bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩᝮ"), False):
      threading.current_thread().a11y_stop = True
      bstack11l111l11_opy_.bstack11lll1111_opy_(bstack11lll11lll_opy_, name=bstack1l1_opy_ (u"ࠢࠣᝯ"), path=bstack1l1_opy_ (u"ࠣࠤᝰ"))