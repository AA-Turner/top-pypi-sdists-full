# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack11l11lll11_opy_
from bstack_utils.helper import bstack111ll1lll_opy_
logger = logging.getLogger(__name__)
def bstack1l11ll1lll_opy_(bstack111ll11ll_opy_):
  return True if bstack111ll11ll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l1l1l1lll_opy_(context, *args):
    tags = getattr(args[0], bstack11ll11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᜐ"), [])
    bstack1ll1l11l1l_opy_ = bstack11l11lll11_opy_.bstack1ll1lllll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1ll1l11l1l_opy_
    try:
      bstack1l1lll1lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l11ll1lll_opy_(bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᜑ")) else context.browser
      if bstack1l1lll1lll_opy_ and bstack1l1lll1lll_opy_.session_id and bstack1ll1l11l1l_opy_ and bstack111ll1lll_opy_(
              threading.current_thread(), bstack11ll11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᜒ"), None):
          threading.current_thread().isA11yTest = bstack11l11lll11_opy_.bstack1l1111l1l1_opy_(bstack1l1lll1lll_opy_, bstack1ll1l11l1l_opy_)
    except Exception as e:
       logger.debug(bstack11ll11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭ᜓ").format(str(e)))
def bstack1111l1111_opy_(bstack1l1lll1lll_opy_):
    if bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷ᜔ࠫ"), None) and bstack111ll1lll_opy_(
      threading.current_thread(), bstack11ll11_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳ᜕ࠧ"), None) and not bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬ᜖"), False):
      threading.current_thread().a11y_stop = True
      bstack11l11lll11_opy_.bstack1ll1l1l111_opy_(bstack1l1lll1lll_opy_, name=bstack11ll11_opy_ (u"ࠥࠦ᜗"), path=bstack11ll11_opy_ (u"ࠦࠧ᜘"))