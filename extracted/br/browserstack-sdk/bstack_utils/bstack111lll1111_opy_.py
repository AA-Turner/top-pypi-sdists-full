# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import os
import threading
from bstack_utils.helper import bstack11lll11ll1_opy_
from bstack_utils.constants import bstack11l1ll11lll_opy_, EVENTS, STAGE
from bstack_utils.bstack1l1ll11lll_opy_ import get_logger
logger = get_logger(__name__)
class bstack1l1lllll1l_opy_:
    bstack1llllllll1ll_opy_ = None
    @classmethod
    def bstack1l11l1ll_opy_(cls):
        if cls.on() and os.getenv(bstack1l11l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ⇡")):
            logger.info(
                bstack1l11l11_opy_ (u"ࠨࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠫ⇢").format(os.getenv(bstack1l11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⇣"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⇤"), None) is None or os.environ[bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⇥")] == bstack1l11l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⇦"):
            return False
        return True
    @classmethod
    def bstack1llll1l11l11_opy_(cls, bs_config, framework=bstack1l11l11_opy_ (u"ࠨࠢ⇧")):
        bstack11ll11111l1_opy_ = False
        for fw in bstack11l1ll11lll_opy_:
            if fw in framework:
                bstack11ll11111l1_opy_ = True
        return bstack11lll11ll1_opy_(bs_config.get(bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⇨"), bstack11ll11111l1_opy_))
    @classmethod
    def bstack1llll11lll1l_opy_(cls, framework):
        return framework in bstack11l1ll11lll_opy_
    @classmethod
    def bstack1llll1lll1ll_opy_(cls, bs_config, framework):
        return cls.bstack1llll1l11l11_opy_(bs_config, framework) is True and cls.bstack1llll11lll1l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l11l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⇩"), None)
    @staticmethod
    def bstack111lll1l1l_opy_():
        if getattr(threading.current_thread(), bstack1l11l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⇪"), None):
            return {
                bstack1l11l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ⇫"): bstack1l11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ⇬"),
                bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⇭"): getattr(threading.current_thread(), bstack1l11l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⇮"), None)
            }
        if getattr(threading.current_thread(), bstack1l11l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⇯"), None):
            return {
                bstack1l11l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭⇰"): bstack1l11l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⇱"),
                bstack1l11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⇲"): getattr(threading.current_thread(), bstack1l11l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⇳"), None)
            }
        return None
    @staticmethod
    def bstack1llll11ll11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1lllll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l11l1l1_opy_(test, hook_name=None):
        bstack1llll11ll1ll_opy_ = test.parent
        if hook_name in [bstack1l11l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ⇴"), bstack1l11l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ⇵"), bstack1l11l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭⇶"), bstack1l11l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ⇷")]:
            bstack1llll11ll1ll_opy_ = test
        scope = []
        while bstack1llll11ll1ll_opy_ is not None:
            scope.append(bstack1llll11ll1ll_opy_.name)
            bstack1llll11ll1ll_opy_ = bstack1llll11ll1ll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll11ll1l1_opy_(hook_type):
        if hook_type == bstack1l11l11_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢ⇸"):
            return bstack1l11l11_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢ⇹")
        elif hook_type == bstack1l11l11_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣ⇺"):
            return bstack1l11l11_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧ⇻")
    @staticmethod
    def bstack1llll11lll11_opy_(bstack1ll11lll1l_opy_):
        try:
            if not bstack1l1lllll1l_opy_.on():
                return bstack1ll11lll1l_opy_
            if os.environ.get(bstack1l11l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦ⇼"), None) == bstack1l11l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ⇽"):
                tests = os.environ.get(bstack1l11l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧ⇾"), None)
                if tests is None or tests == bstack1l11l11_opy_ (u"ࠤࡱࡹࡱࡲࠢ⇿"):
                    return bstack1ll11lll1l_opy_
                bstack1ll11lll1l_opy_ = tests.split(bstack1l11l11_opy_ (u"ࠪ࠰ࠬ∀"))
                return bstack1ll11lll1l_opy_
        except Exception as exc:
            logger.debug(bstack1l11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧ∁") + str(str(exc)) + bstack1l11l11_opy_ (u"ࠧࠨ∂"))
        return bstack1ll11lll1l_opy_