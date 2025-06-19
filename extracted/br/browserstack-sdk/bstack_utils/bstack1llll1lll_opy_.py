# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1l11l11ll1_opy_
from bstack_utils.helper import bstack1ll11l1l1l_opy_
logger = logging.getLogger(__name__)
def bstack11ll1llll1_opy_(bstack11l111111_opy_):
  return True if bstack11l111111_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l1lll11_opy_(context, *args):
    tags = getattr(args[0], bstack111lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᜂ"), [])
    bstack111l11l1l_opy_ = bstack1l11l11ll1_opy_.bstack11lllllll1_opy_(tags)
    threading.current_thread().isA11yTest = bstack111l11l1l_opy_
    try:
      bstack111l1ll1l_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll1llll1_opy_(bstack111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᜃ")) else context.browser
      if bstack111l1ll1l_opy_ and bstack111l1ll1l_opy_.session_id and bstack111l11l1l_opy_ and bstack1ll11l1l1l_opy_(
              threading.current_thread(), bstack111lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᜄ"), None):
          threading.current_thread().isA11yTest = bstack1l11l11ll1_opy_.bstack1ll1l1l1l1_opy_(bstack111l1ll1l_opy_, bstack111l11l1l_opy_)
    except Exception as e:
       logger.debug(bstack111lll_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭ᜅ").format(str(e)))
def bstack111l1l111_opy_(bstack111l1ll1l_opy_):
    if bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᜆ"), None) and bstack1ll11l1l1l_opy_(
      threading.current_thread(), bstack111lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᜇ"), None) and not bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬᜈ"), False):
      threading.current_thread().a11y_stop = True
      bstack1l11l11ll1_opy_.bstack1ll1ll1l11_opy_(bstack111l1ll1l_opy_, name=bstack111lll_opy_ (u"ࠥࠦᜉ"), path=bstack111lll_opy_ (u"ࠦࠧᜊ"))