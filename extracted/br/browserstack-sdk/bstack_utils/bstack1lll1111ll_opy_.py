# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1ll1ll1l11_opy_
from bstack_utils.helper import bstack1l111ll111_opy_
logger = logging.getLogger(__name__)
def bstack1l1111l111_opy_(bstack1ll1ll11l_opy_):
  return True if bstack1ll1ll11l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1lll1ll11_opy_(context, *args):
    tags = getattr(args[0], bstack1l11l11_opy_ (u"ࠧࡵࡣࡪࡷࠬᝯ"), [])
    bstack1l1ll1111_opy_ = bstack1ll1ll1l11_opy_.bstack11l1ll1lll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l1ll1111_opy_
    try:
      bstack11l11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1111l111_opy_(bstack1l11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᝰ")) else context.browser
      if bstack11l11lll_opy_ and bstack11l11lll_opy_.session_id and bstack1l1ll1111_opy_ and bstack1l111ll111_opy_(
              threading.current_thread(), bstack1l11l11_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᝱"), None):
          threading.current_thread().isA11yTest = bstack1ll1ll1l11_opy_.bstack1111l11l1_opy_(bstack11l11lll_opy_, bstack1l1ll1111_opy_)
    except Exception as e:
       logger.debug(bstack1l11l11_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪᝲ").format(str(e)))
def bstack1l111l111_opy_(bstack11l11lll_opy_):
    if bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᝳ"), None) and bstack1l111ll111_opy_(
      threading.current_thread(), bstack1l11l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ᝴"), None) and not bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩ᝵"), False):
      threading.current_thread().a11y_stop = True
      bstack1ll1ll1l11_opy_.bstack11l1l1lll_opy_(bstack11l11lll_opy_, name=bstack1l11l11_opy_ (u"ࠢࠣ᝶"), path=bstack1l11l11_opy_ (u"ࠣࠤ᝷"))