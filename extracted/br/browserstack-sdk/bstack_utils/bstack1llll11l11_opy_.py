# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import threading
from bstack_utils.helper import bstack1lll11l1_opy_
from bstack_utils.constants import bstack111l11ll11l_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1ll1l1l1l1_opy_:
    bstack1lll11111lll_opy_ = None
    @classmethod
    def bstack1lllllll1l_opy_(cls):
        if cls.on() and os.getenv(bstack11lll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ⚲")):
            logger.info(
                bstack11lll1_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩ⚳").format(os.getenv(bstack11lll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ⚴"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⚵"), None) is None or os.environ[bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⚶")] == bstack11lll1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⚷"):
            return False
        return True
    @classmethod
    def bstack1ll1l1l1lll1_opy_(cls, bs_config, framework=bstack11lll1_opy_ (u"ࠢࠣ⚸")):
        bstack111l1ll11l1_opy_ = False
        for fw in bstack111l11ll11l_opy_:
            if fw in framework:
                bstack111l1ll11l1_opy_ = True
        return bstack1lll11l1_opy_(bs_config.get(bstack11lll1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⚹"), bstack111l1ll11l1_opy_))
    @classmethod
    def bstack1ll1l1l11l1l_opy_(cls, framework):
        return framework in bstack111l11ll11l_opy_
    @classmethod
    def bstack1ll1l1ll1lll_opy_(cls, bs_config, framework):
        return cls.bstack1ll1l1l1lll1_opy_(bs_config, framework) is True and cls.bstack1ll1l1l11l1l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⚺"), None)
    @staticmethod
    def bstack1lllll1ll11_opy_():
        if getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⚻"), None):
            return {
                bstack11lll1_opy_ (u"ࠫࡹࡿࡰࡦࠩ⚼"): bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࠪ⚽"),
                bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⚾"): getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⚿"), None)
            }
        if getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⛀"), None):
            return {
                bstack11lll1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⛁"): bstack11lll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⛂"),
                bstack11lll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⛃"): getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⛄"), None)
            }
        return None
    @staticmethod
    def bstack1ll1l1l11ll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll1l1l1l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1lllll11l11_opy_(test, hook_name=None):
        bstack1ll1l1l11l11_opy_ = test.parent
        if hook_name in [bstack11lll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⛅"), bstack11lll1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⛆"), bstack11lll1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⛇"), bstack11lll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ⛈")]:
            bstack1ll1l1l11l11_opy_ = test
        scope = []
        while bstack1ll1l1l11l11_opy_ is not None:
            scope.append(bstack1ll1l1l11l11_opy_.name)
            bstack1ll1l1l11l11_opy_ = bstack1ll1l1l11l11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1l1l111ll_opy_(hook_type):
        if hook_type == bstack11lll1_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣ⛉"):
            return bstack11lll1_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣ⛊")
        elif hook_type == bstack11lll1_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤ⛋"):
            return bstack11lll1_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨ⛌")
    @staticmethod
    def bstack1ll1l1l11lll_opy_(bstack111lll1ll_opy_):
        try:
            if not bstack1ll1l1l1l1_opy_.on():
                return bstack111lll1ll_opy_
            if os.environ.get(bstack11lll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧ⛍"), None) == bstack11lll1_opy_ (u"ࠣࡶࡵࡹࡪࠨ⛎"):
                tests = os.environ.get(bstack11lll1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨ⛏"), None)
                if tests is None or tests == bstack11lll1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⛐"):
                    return bstack111lll1ll_opy_
                bstack111lll1ll_opy_ = tests.split(bstack11lll1_opy_ (u"ࠫ࠱࠭⛑"))
                return bstack111lll1ll_opy_
        except Exception as exc:
            logger.debug(bstack11lll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨ⛒") + str(str(exc)) + bstack11lll1_opy_ (u"ࠨࠢ⛓"))
        return bstack111lll1ll_opy_