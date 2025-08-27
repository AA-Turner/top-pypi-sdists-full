# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1llllll1l1_opy_
from bstack_utils.helper import bstack1l11l1l1ll_opy_
logger = logging.getLogger(__name__)
def bstack1ll1l11ll_opy_(bstack1l1lllllll_opy_):
  return True if bstack1l1lllllll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11ll1111ll_opy_(context, *args):
    tags = getattr(args[0], bstack1111lll_opy_ (u"ࠧࡵࡣࡪࡷࠬ᝶"), [])
    bstack11l1ll11_opy_ = bstack1llllll1l1_opy_.bstack11llll111l_opy_(tags)
    threading.current_thread().isA11yTest = bstack11l1ll11_opy_
    try:
      bstack1llll1lll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll1l11ll_opy_(bstack1111lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ᝷")) else context.browser
      if bstack1llll1lll1_opy_ and bstack1llll1lll1_opy_.session_id and bstack11l1ll11_opy_ and bstack1l11l1l1ll_opy_(
              threading.current_thread(), bstack1111lll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᝸"), None):
          threading.current_thread().isA11yTest = bstack1llllll1l1_opy_.bstack11111llll_opy_(bstack1llll1lll1_opy_, bstack11l1ll11_opy_)
    except Exception as e:
       logger.debug(bstack1111lll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪ᝹").format(str(e)))
def bstack1l1l1llll1_opy_(bstack1llll1lll1_opy_):
    if bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ᝺"), None) and bstack1l11l1l1ll_opy_(
      threading.current_thread(), bstack1111lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ᝻"), None) and not bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩ᝼"), False):
      threading.current_thread().a11y_stop = True
      bstack1llllll1l1_opy_.bstack1ll1ll1l1l_opy_(bstack1llll1lll1_opy_, name=bstack1111lll_opy_ (u"ࠢࠣ᝽"), path=bstack1111lll_opy_ (u"ࠣࠤ᝾"))