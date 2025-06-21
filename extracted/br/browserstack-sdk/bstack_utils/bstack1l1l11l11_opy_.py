# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import threading
import logging
import bstack_utils.accessibility as bstack1ll1l11ll_opy_
from bstack_utils.helper import bstack111l1ll1l_opy_
logger = logging.getLogger(__name__)
def bstack1l1l111l_opy_(bstack1111lll1_opy_):
  return True if bstack1111lll1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack11l11lll1_opy_(context, *args):
    tags = getattr(args[0], bstack1l1l1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩᜑ"), [])
    bstack1l111lll11_opy_ = bstack1ll1l11ll_opy_.bstack11lll1llll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l111lll11_opy_
    try:
      bstack1ll1l11ll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l111l_opy_(bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫᜒ")) else context.browser
      if bstack1ll1l11ll1_opy_ and bstack1ll1l11ll1_opy_.session_id and bstack1l111lll11_opy_ and bstack111l1ll1l_opy_(
              threading.current_thread(), bstack1l1l1l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᜓ"), None):
          threading.current_thread().isA11yTest = bstack1ll1l11ll_opy_.bstack1l1l1l111l_opy_(bstack1ll1l11ll1_opy_, bstack1l111lll11_opy_)
    except Exception as e:
       logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡤ࠵࠶ࡿࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃ᜔ࠧ").format(str(e)))
def bstack1l11ll1ll1_opy_(bstack1ll1l11ll1_opy_):
    if bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸ᜕ࠬ"), None) and bstack111l1ll1l_opy_(
      threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᜖"), None) and not bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪࡥ࠶࠷ࡹࡠࡵࡷࡳࡵ࠭᜗"), False):
      threading.current_thread().a11y_stop = True
      bstack1ll1l11ll_opy_.bstack1ll1lll111_opy_(bstack1ll1l11ll1_opy_, name=bstack1l1l1l1_opy_ (u"ࠦࠧ᜘"), path=bstack1l1l1l1_opy_ (u"ࠧࠨ᜙"))