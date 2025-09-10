# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
import threading
from bstack_utils.helper import bstack1l1l1llll1_opy_
from bstack_utils.constants import bstack11l1ll1llll_opy_, EVENTS, STAGE
from bstack_utils.bstack1lll1llll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lllllll1_opy_:
    bstack11ll1lll1ll_opy_ = None
    @classmethod
    def bstack1ll1ll11l1_opy_(cls):
        if cls.on() and os.getenv(bstack1ll11ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ⇥")):
            logger.info(
                bstack1ll11ll_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬ⇦").format(os.getenv(bstack1ll11ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⇧"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⇨"), None) is None or os.environ[bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⇩")] == bstack1ll11ll_opy_ (u"ࠤࡱࡹࡱࡲࠢ⇪"):
            return False
        return True
    @classmethod
    def bstack1llll11ll11l_opy_(cls, bs_config, framework=bstack1ll11ll_opy_ (u"ࠥࠦ⇫")):
        bstack11l1lll1ll1_opy_ = False
        for fw in bstack11l1ll1llll_opy_:
            if fw in framework:
                bstack11l1lll1ll1_opy_ = True
        return bstack1l1l1llll1_opy_(bs_config.get(bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⇬"), bstack11l1lll1ll1_opy_))
    @classmethod
    def bstack1llll111ll11_opy_(cls, framework):
        return framework in bstack11l1ll1llll_opy_
    @classmethod
    def bstack1llll1ll1l11_opy_(cls, bs_config, framework):
        return cls.bstack1llll11ll11l_opy_(bs_config, framework) is True and cls.bstack1llll111ll11_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⇭"), None)
    @staticmethod
    def bstack111ll1l11l_opy_():
        if getattr(threading.current_thread(), bstack1ll11ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⇮"), None):
            return {
                bstack1ll11ll_opy_ (u"ࠧࡵࡻࡳࡩࠬ⇯"): bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹ࠭⇰"),
                bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⇱"): getattr(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⇲"), None)
            }
        if getattr(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⇳"), None):
            return {
                bstack1ll11ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ⇴"): bstack1ll11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⇵"),
                bstack1ll11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⇶"): getattr(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⇷"), None)
            }
        return None
    @staticmethod
    def bstack1llll111ll1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11lllllll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l11111l_opy_(test, hook_name=None):
        bstack1llll111lll1_opy_ = test.parent
        if hook_name in [bstack1ll11ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ⇸"), bstack1ll11ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ⇹"), bstack1ll11ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪ⇺"), bstack1ll11ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⇻")]:
            bstack1llll111lll1_opy_ = test
        scope = []
        while bstack1llll111lll1_opy_ is not None:
            scope.append(bstack1llll111lll1_opy_.name)
            bstack1llll111lll1_opy_ = bstack1llll111lll1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll111l1ll_opy_(hook_type):
        if hook_type == bstack1ll11ll_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦ⇼"):
            return bstack1ll11ll_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦ⇽")
        elif hook_type == bstack1ll11ll_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧ⇾"):
            return bstack1ll11ll_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤ⇿")
    @staticmethod
    def bstack1llll111l1l1_opy_(bstack11l1l1l11l_opy_):
        try:
            if not bstack11lllllll1_opy_.on():
                return bstack11l1l1l11l_opy_
            if os.environ.get(bstack1ll11ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣ∀"), None) == bstack1ll11ll_opy_ (u"ࠦࡹࡸࡵࡦࠤ∁"):
                tests = os.environ.get(bstack1ll11ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤ∂"), None)
                if tests is None or tests == bstack1ll11ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ∃"):
                    return bstack11l1l1l11l_opy_
                bstack11l1l1l11l_opy_ = tests.split(bstack1ll11ll_opy_ (u"ࠧ࠭ࠩ∄"))
                return bstack11l1l1l11l_opy_
        except Exception as exc:
            logger.debug(bstack1ll11ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤ∅") + str(str(exc)) + bstack1ll11ll_opy_ (u"ࠤࠥ∆"))
        return bstack11l1l1l11l_opy_