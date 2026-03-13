# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import threading
import logging
import bstack_utils.accessibility as a11y
from bstack_utils.helper import bstack1l11l11l11_opy_
logger = logging.getLogger(__name__)
def bstack1ll111ll_opy_(bstack11ll111ll1_opy_):
  return True if bstack11ll111ll1_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll1ll11l_opy_(context, *args):
    tags = getattr(args[0], bstack1111l_opy_ (u"ࠬࡺࡡࡨࡵࠪᭈ"), [])
    bstack1lllll1l1_opy_ = a11y.is_enabled_testcase(tags)
    threading.current_thread().isA11yTest = bstack1lllll1l1_opy_
    try:
      bstack1lll1lllll_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll111ll_opy_(bstack1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬᭉ")) else context.browser
      if bstack1lll1lllll_opy_ and bstack1lll1lllll_opy_.session_id and bstack1lllll1l1_opy_ and bstack1l11l11l11_opy_(
              threading.current_thread(), bstack1111l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᭊ"), None):
          caps = bstack1lll1lllll_opy_.capabilities
          if not a11y.is_platform_supported(caps, None):
              logger.debug(bstack1111l_opy_ (u"ࠨࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥࡹࡵࡱࡲࡲࡶࡹࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࠬࡪ࠴ࡧ࠯࠮ࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠬࠫᭋ"))
              threading.current_thread().isA11yTest = False
              return
          threading.current_thread().isA11yTest = a11y.start_test_capture(bstack1lll1lllll_opy_, bstack1lllll1l1_opy_)
    except Exception as e:
       logger.debug(bstack1111l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡦ࠷࠱ࡺࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩᭌ").format(str(e)))
def bstack1111l1lll1_opy_(bstack1lll1lllll_opy_):
    if bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ᭍"), None) and bstack1l11l11l11_opy_(
      threading.current_thread(), bstack1111l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᭎"), None) and not bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࠨ᭏"), False):
      threading.current_thread().a11y_stop = True
      a11y.bstack1l1l1ll11_opy_(bstack1lll1lllll_opy_, name=bstack1111l_opy_ (u"ࠨࠢ᭐"), path=bstack1111l_opy_ (u"ࠢࠣ᭑"))