# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1l11l1l111_opy_
from bstack_utils.helper import bstack111111lll_opy_
logger = logging.getLogger(__name__)
def bstack11l1l11l_opy_(bstack1l111111ll_opy_):
  return True if bstack1l111111ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11ll1ll1l_opy_(context, *args):
    tags = getattr(args[0], bstack1l1111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᢑ"), [])
    bstack11l111l1l1_opy_ = bstack1l11l1l111_opy_.bstack1lllll11ll_opy_(tags)
    threading.current_thread().isA11yTest = bstack11l111l1l1_opy_
    try:
      bstack1l1llll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l1l11l_opy_(bstack1l1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᢒ")) else context.browser
      if bstack1l1llll111_opy_ and bstack1l1llll111_opy_.session_id and bstack11l111l1l1_opy_ and bstack111111lll_opy_(
              threading.current_thread(), bstack1l1111_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᢓ"), None):
          threading.current_thread().isA11yTest = bstack1l11l1l111_opy_.bstack111l11l1ll_opy_(bstack1l1llll111_opy_, bstack11l111l1l1_opy_)
    except Exception as e:
       logger.debug(bstack1l1111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭ᢔ").format(str(e)))
def bstack1l1l1l1lll_opy_(bstack1l1llll111_opy_):
    if bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᢕ"), None) and bstack111111lll_opy_(
      threading.current_thread(), bstack1l1111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᢖ"), None) and not bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬᢗ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l11l1l111_opy_.bstack111ll1ll1_opy_(bstack1l1llll111_opy_, name=bstack1l1111_opy_ (u"ࠥࠦᢘ"), path=bstack1l1111_opy_ (u"ࠦࠧᢙ"))