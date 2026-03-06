# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import threading
from bstack_utils.helper import bstack11ll1l1l1l_opy_
from bstack_utils.constants import bstack111ll11l1l1_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11l111ll11_opy_:
    bstack1lll11l1llll_opy_ = None
    @classmethod
    def bstack11l1111ll1_opy_(cls):
        if cls.on() and os.getenv(bstack1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ▟")):
            logger.info(
                bstack1111_opy_ (u"ࠧࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧ■").format(os.getenv(bstack1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ□"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭▢"), None) is None or os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ▣")] == bstack1111_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ▤"):
            return False
        return True
    @classmethod
    def bstack1ll1ll1llll1_opy_(cls, bs_config, framework=bstack1111_opy_ (u"ࠧࠨ▥")):
        bstack111ll1lll11_opy_ = False
        for fw in bstack111ll11l1l1_opy_:
            if fw in framework:
                bstack111ll1lll11_opy_ = True
        return bstack11ll1l1l1l_opy_(bs_config.get(bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ▦"), bstack111ll1lll11_opy_))
    @classmethod
    def bstack1ll1ll1l111l_opy_(cls, framework):
        return framework in bstack111ll11l1l1_opy_
    @classmethod
    def bstack1ll1llll111l_opy_(cls, bs_config, framework):
        return cls.bstack1ll1ll1llll1_opy_(bs_config, framework) is True and cls.bstack1ll1ll1l111l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ▧"), None)
    @staticmethod
    def bstack1111ll1l11_opy_():
        if getattr(threading.current_thread(), bstack1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ▨"), None):
            return {
                bstack1111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ▩"): bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࠨ▪"),
                bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ▫"): getattr(threading.current_thread(), bstack1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ▬"), None)
            }
        if getattr(threading.current_thread(), bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ▭"), None):
            return {
                bstack1111_opy_ (u"ࠧࡵࡻࡳࡩࠬ▮"): bstack1111_opy_ (u"ࠨࡪࡲࡳࡰ࠭▯"),
                bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ▰"): getattr(threading.current_thread(), bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ▱"), None)
            }
        return None
    @staticmethod
    def bstack1ll1ll1l1111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l111ll11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11111l1l11_opy_(test, hook_name=None):
        bstack1ll1ll1l11ll_opy_ = test.parent
        if hook_name in [bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ▲"), bstack1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭△"), bstack1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ▴"), bstack1111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ▵")]:
            bstack1ll1ll1l11ll_opy_ = test
        scope = []
        while bstack1ll1ll1l11ll_opy_ is not None:
            scope.append(bstack1ll1ll1l11ll_opy_.name)
            bstack1ll1ll1l11ll_opy_ = bstack1ll1ll1l11ll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1ll11llll_opy_(hook_type):
        if hook_type == bstack1111_opy_ (u"ࠣࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍࠨ▶"):
            return bstack1111_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡪࡲࡳࡰࠨ▷")
        elif hook_type == bstack1111_opy_ (u"ࠥࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠢ▸"):
            return bstack1111_opy_ (u"࡙ࠦ࡫ࡡࡳࡦࡲࡻࡳࠦࡨࡰࡱ࡮ࠦ▹")
    @staticmethod
    def bstack1ll1ll1l11l1_opy_(bstack11llllll11_opy_):
        try:
            if not bstack11l111ll11_opy_.on():
                return bstack11llllll11_opy_
            if os.environ.get(bstack1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠥ►"), None) == bstack1111_opy_ (u"ࠨࡴࡳࡷࡨࠦ▻"):
                tests = os.environ.get(bstack1111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠦ▼"), None)
                if tests is None or tests == bstack1111_opy_ (u"ࠣࡰࡸࡰࡱࠨ▽"):
                    return bstack11llllll11_opy_
                bstack11llllll11_opy_ = tests.split(bstack1111_opy_ (u"ࠩ࠯ࠫ▾"))
                return bstack11llllll11_opy_
        except Exception as exc:
            logger.debug(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡩࡷࡻ࡮ࠡࡪࡤࡲࡩࡲࡥࡳ࠼ࠣࠦ▿") + str(str(exc)) + bstack1111_opy_ (u"ࠦࠧ◀"))
        return bstack11llllll11_opy_