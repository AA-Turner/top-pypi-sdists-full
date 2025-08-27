# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
import threading
from bstack_utils.helper import bstack11lll1111_opy_
from bstack_utils.constants import bstack11l1lll111l_opy_, EVENTS, STAGE
from bstack_utils.bstack1l1l11111_opy_ import get_logger
logger = get_logger(__name__)
class bstack1ll11l1ll1_opy_:
    bstack1llllllll111_opy_ = None
    @classmethod
    def bstack111l1111l_opy_(cls):
        if cls.on() and os.getenv(bstack1111lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ⇡")):
            logger.info(
                bstack1111lll_opy_ (u"ࠨࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨ⇢").format(os.getenv(bstack1111lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⇣"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⇤"), None) is None or os.environ[bstack1111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⇥")] == bstack1111lll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⇦"):
            return False
        return True
    @classmethod
    def bstack1llll11l1l1l_opy_(cls, bs_config, framework=bstack1111lll_opy_ (u"ࠨࠢ⇧")):
        bstack11ll1111l1l_opy_ = False
        for fw in bstack11l1lll111l_opy_:
            if fw in framework:
                bstack11ll1111l1l_opy_ = True
        return bstack11lll1111_opy_(bs_config.get(bstack1111lll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⇨"), bstack11ll1111l1l_opy_))
    @classmethod
    def bstack1llll11l11l1_opy_(cls, framework):
        return framework in bstack11l1lll111l_opy_
    @classmethod
    def bstack1llll1l11l1l_opy_(cls, bs_config, framework):
        return cls.bstack1llll11l1l1l_opy_(bs_config, framework) is True and cls.bstack1llll11l11l1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⇩"), None)
    @staticmethod
    def bstack111ll11ll1_opy_():
        if getattr(threading.current_thread(), bstack1111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⇪"), None):
            return {
                bstack1111lll_opy_ (u"ࠪࡸࡾࡶࡥࠨ⇫"): bstack1111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ⇬"),
                bstack1111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⇭"): getattr(threading.current_thread(), bstack1111lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⇮"), None)
            }
        if getattr(threading.current_thread(), bstack1111lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⇯"), None):
            return {
                bstack1111lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭⇰"): bstack1111lll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⇱"),
                bstack1111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⇲"): getattr(threading.current_thread(), bstack1111lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⇳"), None)
            }
        return None
    @staticmethod
    def bstack1llll11l11ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll11l1ll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111l111l1l_opy_(test, hook_name=None):
        bstack1llll11l111l_opy_ = test.parent
        if hook_name in [bstack1111lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ⇴"), bstack1111lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ⇵"), bstack1111lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭⇶"), bstack1111lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ⇷")]:
            bstack1llll11l111l_opy_ = test
        scope = []
        while bstack1llll11l111l_opy_ is not None:
            scope.append(bstack1llll11l111l_opy_.name)
            bstack1llll11l111l_opy_ = bstack1llll11l111l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll11l1111_opy_(hook_type):
        if hook_type == bstack1111lll_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢ⇸"):
            return bstack1111lll_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢ⇹")
        elif hook_type == bstack1111lll_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣ⇺"):
            return bstack1111lll_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧ⇻")
    @staticmethod
    def bstack1llll11l1l11_opy_(bstack11l11ll1l_opy_):
        try:
            if not bstack1ll11l1ll1_opy_.on():
                return bstack11l11ll1l_opy_
            if os.environ.get(bstack1111lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦ⇼"), None) == bstack1111lll_opy_ (u"ࠢࡵࡴࡸࡩࠧ⇽"):
                tests = os.environ.get(bstack1111lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧ⇾"), None)
                if tests is None or tests == bstack1111lll_opy_ (u"ࠤࡱࡹࡱࡲࠢ⇿"):
                    return bstack11l11ll1l_opy_
                bstack11l11ll1l_opy_ = tests.split(bstack1111lll_opy_ (u"ࠪ࠰ࠬ∀"))
                return bstack11l11ll1l_opy_
        except Exception as exc:
            logger.debug(bstack1111lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧ∁") + str(str(exc)) + bstack1111lll_opy_ (u"ࠧࠨ∂"))
        return bstack11l11ll1l_opy_