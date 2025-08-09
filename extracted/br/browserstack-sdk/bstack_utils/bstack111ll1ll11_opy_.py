# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import threading
from bstack_utils.helper import bstack1ll1l11111_opy_
from bstack_utils.constants import bstack11l1ll1llll_opy_, EVENTS, STAGE
from bstack_utils.bstack1l1111111_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l1l1111_opy_:
    bstack1lllllllll11_opy_ = None
    @classmethod
    def bstack1ll1111l11_opy_(cls):
        if cls.on() and os.getenv(bstack11l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ⇢")):
            logger.info(
                bstack11l1_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬ⇣").format(os.getenv(bstack11l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ⇤"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⇥"), None) is None or os.environ[bstack11l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⇦")] == bstack11l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⇧"):
            return False
        return True
    @classmethod
    def bstack1llll1l11l11_opy_(cls, bs_config, framework=bstack11l1_opy_ (u"ࠢࠣ⇨")):
        bstack11ll1111lll_opy_ = False
        for fw in bstack11l1ll1llll_opy_:
            if fw in framework:
                bstack11ll1111lll_opy_ = True
        return bstack1ll1l11111_opy_(bs_config.get(bstack11l1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⇩"), bstack11ll1111lll_opy_))
    @classmethod
    def bstack1llll1l11111_opy_(cls, framework):
        return framework in bstack11l1ll1llll_opy_
    @classmethod
    def bstack1llll1lll1l1_opy_(cls, bs_config, framework):
        return cls.bstack1llll1l11l11_opy_(bs_config, framework) is True and cls.bstack1llll1l11111_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⇪"), None)
    @staticmethod
    def bstack111ll1l1ll_opy_():
        if getattr(threading.current_thread(), bstack11l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⇫"), None):
            return {
                bstack11l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ⇬"): bstack11l1_opy_ (u"ࠬࡺࡥࡴࡶࠪ⇭"),
                bstack11l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⇮"): getattr(threading.current_thread(), bstack11l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⇯"), None)
            }
        if getattr(threading.current_thread(), bstack11l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⇰"), None):
            return {
                bstack11l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⇱"): bstack11l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⇲"),
                bstack11l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⇳"): getattr(threading.current_thread(), bstack11l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⇴"), None)
            }
        return None
    @staticmethod
    def bstack1llll1l1111l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l1l1111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l111l1l_opy_(test, hook_name=None):
        bstack1llll11lll1l_opy_ = test.parent
        if hook_name in [bstack11l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⇵"), bstack11l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⇶"), bstack11l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⇷"), bstack11l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ⇸")]:
            bstack1llll11lll1l_opy_ = test
        scope = []
        while bstack1llll11lll1l_opy_ is not None:
            scope.append(bstack1llll11lll1l_opy_.name)
            bstack1llll11lll1l_opy_ = bstack1llll11lll1l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll11lllll_opy_(hook_type):
        if hook_type == bstack11l1_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣ⇹"):
            return bstack11l1_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣ⇺")
        elif hook_type == bstack11l1_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤ⇻"):
            return bstack11l1_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨ⇼")
    @staticmethod
    def bstack1llll11llll1_opy_(bstack1l11lll11_opy_):
        try:
            if not bstack11l1l1111_opy_.on():
                return bstack1l11lll11_opy_
            if os.environ.get(bstack11l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧ⇽"), None) == bstack11l1_opy_ (u"ࠣࡶࡵࡹࡪࠨ⇾"):
                tests = os.environ.get(bstack11l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨ⇿"), None)
                if tests is None or tests == bstack11l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ∀"):
                    return bstack1l11lll11_opy_
                bstack1l11lll11_opy_ = tests.split(bstack11l1_opy_ (u"ࠫ࠱࠭∁"))
                return bstack1l11lll11_opy_
        except Exception as exc:
            logger.debug(bstack11l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨ∂") + str(str(exc)) + bstack11l1_opy_ (u"ࠨࠢ∃"))
        return bstack1l11lll11_opy_