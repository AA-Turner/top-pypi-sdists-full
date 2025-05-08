# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1l1l1l11l_opy_
from bstack_utils.helper import bstack1l111l11_opy_
logger = logging.getLogger(__name__)
def bstack1lll1l111l_opy_(bstack1l1ll111ll_opy_):
  return True if bstack1l1ll111ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1lll1l1lll_opy_(context, *args):
    tags = getattr(args[0], bstack1l1lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᙡ"), [])
    bstack1111l1l1l_opy_ = bstack1l1l1l11l_opy_.bstack1ll1llll11_opy_(tags)
    threading.current_thread().isA11yTest = bstack1111l1l1l_opy_
    try:
      bstack1l1llll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1l111l_opy_(bstack1l1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᙢ")) else context.browser
      if bstack1l1llll1_opy_ and bstack1l1llll1_opy_.session_id and bstack1111l1l1l_opy_ and bstack1l111l11_opy_(
              threading.current_thread(), bstack1l1lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᙣ"), None):
          threading.current_thread().isA11yTest = bstack1l1l1l11l_opy_.bstack1l1l11111l_opy_(bstack1l1llll1_opy_, bstack1111l1l1l_opy_)
    except Exception as e:
       logger.debug(bstack1l1lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭ᙤ").format(str(e)))
def bstack11l1l11ll1_opy_(bstack1l1llll1_opy_):
    if bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᙥ"), None) and bstack1l111l11_opy_(
      threading.current_thread(), bstack1l1lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᙦ"), None) and not bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬᙧ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l1l1l11l_opy_.bstack1111l1111_opy_(bstack1l1llll1_opy_, name=bstack1l1lll_opy_ (u"ࠥࠦᙨ"), path=bstack1l1lll_opy_ (u"ࠦࠧᙩ"))