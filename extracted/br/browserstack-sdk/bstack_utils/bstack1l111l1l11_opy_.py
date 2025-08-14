# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1lll11l1ll_opy_
from bstack_utils.helper import bstack1l111l1l_opy_
logger = logging.getLogger(__name__)
def bstack11l1ll11l1_opy_(bstack1lll111l1_opy_):
  return True if bstack1lll111l1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l111lll1l_opy_(context, *args):
    tags = getattr(args[0], bstack1l1l1ll_opy_ (u"ࠧࡵࡣࡪࡷࠬ᝶"), [])
    bstack1l11ll111l_opy_ = bstack1lll11l1ll_opy_.bstack111l1lll1_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l11ll111l_opy_
    try:
      bstack11111ll11_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1ll11l1_opy_(bstack1l1l1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ᝷")) else context.browser
      if bstack11111ll11_opy_ and bstack11111ll11_opy_.session_id and bstack1l11ll111l_opy_ and bstack1l111l1l_opy_(
              threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᝸"), None):
          threading.current_thread().isA11yTest = bstack1lll11l1ll_opy_.bstack1l1l1l11_opy_(bstack11111ll11_opy_, bstack1l11ll111l_opy_)
    except Exception as e:
       logger.debug(bstack1l1l1ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪ᝹").format(str(e)))
def bstack1l11l1l111_opy_(bstack11111ll11_opy_):
    if bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ᝺"), None) and bstack1l111l1l_opy_(
      threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ᝻"), None) and not bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩ᝼"), False):
      threading.current_thread().a11y_stop = True
      bstack1lll11l1ll_opy_.bstack1ll1l11ll_opy_(bstack11111ll11_opy_, name=bstack1l1l1ll_opy_ (u"ࠢࠣ᝽"), path=bstack1l1l1ll_opy_ (u"ࠣࠤ᝾"))