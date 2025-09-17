# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import threading
from bstack_utils.helper import bstack11l1ll11l1_opy_
from bstack_utils.constants import bstack11l1lllll1l_opy_, EVENTS, STAGE
from bstack_utils.bstack1lll1l1l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack11llllllll_opy_:
    bstack1llllll1llll_opy_ = None
    @classmethod
    def bstack11l1111ll_opy_(cls):
        if cls.on() and os.getenv(bstack1l11ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ⇤")):
            logger.info(
                bstack1l11ll1_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠫ⇥").format(os.getenv(bstack1l11ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⇦"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⇧"), None) is None or os.environ[bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⇨")] == bstack1l11ll1_opy_ (u"ࠣࡰࡸࡰࡱࠨ⇩"):
            return False
        return True
    @classmethod
    def bstack1llll11l1l1l_opy_(cls, bs_config, framework=bstack1l11ll1_opy_ (u"ࠤࠥ⇪")):
        bstack11l1lllllll_opy_ = False
        for fw in bstack11l1lllll1l_opy_:
            if fw in framework:
                bstack11l1lllllll_opy_ = True
        return bstack11l1ll11l1_opy_(bs_config.get(bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⇫"), bstack11l1lllllll_opy_))
    @classmethod
    def bstack1llll111l1ll_opy_(cls, framework):
        return framework in bstack11l1lllll1l_opy_
    @classmethod
    def bstack1llll11lll1l_opy_(cls, bs_config, framework):
        return cls.bstack1llll11l1l1l_opy_(bs_config, framework) is True and cls.bstack1llll111l1ll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⇬"), None)
    @staticmethod
    def bstack111ll1l1ll_opy_():
        if getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⇭"), None):
            return {
                bstack1l11ll1_opy_ (u"࠭ࡴࡺࡲࡨࠫ⇮"): bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࠬ⇯"),
                bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⇰"): getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⇱"), None)
            }
        if getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⇲"), None):
            return {
                bstack1l11ll1_opy_ (u"ࠫࡹࡿࡰࡦࠩ⇳"): bstack1l11ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⇴"),
                bstack1l11ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⇵"): getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⇶"), None)
            }
        return None
    @staticmethod
    def bstack1llll111l1l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11llllllll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1111llllll_opy_(test, hook_name=None):
        bstack1llll111ll11_opy_ = test.parent
        if hook_name in [bstack1l11ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⇷"), bstack1l11ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ⇸"), bstack1l11ll1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ⇹"), bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭⇺")]:
            bstack1llll111ll11_opy_ = test
        scope = []
        while bstack1llll111ll11_opy_ is not None:
            scope.append(bstack1llll111ll11_opy_.name)
            bstack1llll111ll11_opy_ = bstack1llll111ll11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll111ll1l_opy_(hook_type):
        if hook_type == bstack1l11ll1_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥ⇻"):
            return bstack1l11ll1_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥ⇼")
        elif hook_type == bstack1l11ll1_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦ⇽"):
            return bstack1l11ll1_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣ⇾")
    @staticmethod
    def bstack1llll111lll1_opy_(bstack1l1ll1lll1_opy_):
        try:
            if not bstack11llllllll_opy_.on():
                return bstack1l1ll1lll1_opy_
            if os.environ.get(bstack1l11ll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢ⇿"), None) == bstack1l11ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣ∀"):
                tests = os.environ.get(bstack1l11ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣ∁"), None)
                if tests is None or tests == bstack1l11ll1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ∂"):
                    return bstack1l1ll1lll1_opy_
                bstack1l1ll1lll1_opy_ = tests.split(bstack1l11ll1_opy_ (u"࠭ࠬࠨ∃"))
                return bstack1l1ll1lll1_opy_
        except Exception as exc:
            logger.debug(bstack1l11ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣ∄") + str(str(exc)) + bstack1l11ll1_opy_ (u"ࠣࠤ∅"))
        return bstack1l1ll1lll1_opy_