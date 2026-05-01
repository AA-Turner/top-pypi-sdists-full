# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import threading
from bstack_utils.helper import bstack1lllll11ll1_opy_
from bstack_utils.constants import bstack11111111l11_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack111ll111_opy_:
    bstack1ll11lll1l11_opy_ = None
    @classmethod
    def bstack1111lll11l_opy_(cls):
        if cls.on() and os.getenv(bstack111ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ⥆")):
            logger.info(
                bstack111ll_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠫ⥇").format(os.getenv(bstack111ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⥈"))))
    @classmethod
    def bstack111lll1ll1_opy_(cls, config=None):
        try:
            bstack1ll1111ll1l1_opy_ = os.getenv(bstack111ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⥉"))
            if not bstack1ll1111ll1l1_opy_:
                return
            bstack1ll1111l1l1l_opy_ = os.getenv(bstack111ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ⥊"))
            bstack111lll11_opy_ = bstack1ll1111l1l1l_opy_ is not None and bstack1ll1111l1l1l_opy_ != bstack111ll_opy_ (u"ࠨࡰࡸࡰࡱ࠭⥋") and len(bstack1ll1111l1l1l_opy_) > 0
            bstack1ll1111l1ll1_opy_ = config.get(bstack111ll_opy_ (u"ࠩࡤࡴࡵ࠭⥌")) is not None if config else False
            if bstack111lll11_opy_ and not bstack1ll1111l1ll1_opy_:
                logger.info(
                    bstack111ll_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥࡥ࠯ࡷࡩࡸࡺࡳ࠰ࡲࡵࡳ࡯࡫ࡣࡵࡵ࠲ࡴ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࡨ࠯࠲ࡁࡷ࡬ࡇࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡵࡵࡲࡵ࠰࡟ࡲࠬ⥍").format(bstack1ll1111ll1l1_opy_))
        except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡴࡷ࡯࡮ࡵ࡫ࡱ࡫ࠥࡧ࠱࠲ࡻࠣࡦࡺ࡯࡬ࡥࠢ࡯࡭ࡳࡱ࠺ࠡࡽࢀࠦ⥎").format(e))
    @classmethod
    def on(cls):
        if os.environ.get(bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⥏"), None) is None or os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⥐")] == bstack111ll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⥑"):
            return False
        return True
    @classmethod
    def bstack1ll111l11l1l_opy_(cls, bs_config, framework=bstack111ll_opy_ (u"ࠣࠤ⥒")):
        bstack11111l1llll_opy_ = False
        for fw in bstack11111111l11_opy_:
            if fw in framework:
                bstack11111l1llll_opy_ = True
        return bstack1lllll11ll1_opy_(bs_config.get(bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⥓"), bstack11111l1llll_opy_))
    @classmethod
    def bstack1ll1111l11ll_opy_(cls, framework):
        return framework in bstack11111111l11_opy_
    @classmethod
    def bstack1ll111l1llll_opy_(cls, bs_config, framework):
        return cls.bstack1ll111l11l1l_opy_(bs_config, framework) is True and cls.bstack1ll1111l11ll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⥔"), None)
    @staticmethod
    def bstack1llll111l1l_opy_():
        if getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⥕"), None):
            return {
                bstack111ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ⥖"): bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࠫ⥗"),
                bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⥘"): getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⥙"), None)
            }
        if getattr(threading.current_thread(), bstack111ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⥚"), None):
            return {
                bstack111ll_opy_ (u"ࠪࡸࡾࡶࡥࠨ⥛"): bstack111ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⥜"),
                bstack111ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⥝"): getattr(threading.current_thread(), bstack111ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⥞"), None)
            }
        return None
    @staticmethod
    def bstack1ll1111ll11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111ll111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1lll1l1l1l1_opy_(test, hook_name=None):
        bstack1ll1111ll111_opy_ = test.parent
        if hook_name in [bstack111ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ⥟"), bstack111ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⥠"), bstack111ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨ⥡"), bstack111ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⥢")]:
            bstack1ll1111ll111_opy_ = test
        scope = []
        while bstack1ll1111ll111_opy_ is not None:
            scope.append(bstack1ll1111ll111_opy_.name)
            bstack1ll1111ll111_opy_ = bstack1ll1111ll111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1111l1lll_opy_(hook_type):
        if hook_type == bstack111ll_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤ⥣"):
            return bstack111ll_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤ⥤")
        elif hook_type == bstack111ll_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥ⥥"):
            return bstack111ll_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢ⥦")
    @staticmethod
    def bstack1ll1111l1l11_opy_(bstack1lll1l111_opy_):
        try:
            if not bstack111ll111_opy_.on():
                return bstack1lll1l111_opy_
            if os.environ.get(bstack111ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨ⥧"), None) == bstack111ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ⥨"):
                tests = os.environ.get(bstack111ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢ⥩"), None)
                if tests is None or tests == bstack111ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⥪"):
                    return bstack1lll1l111_opy_
                bstack1lll1l111_opy_ = tests.split(bstack111ll_opy_ (u"ࠬ࠲ࠧ⥫"))
                return bstack1lll1l111_opy_
        except Exception as exc:
            logger.debug(bstack111ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢ⥬") + str(str(exc)) + bstack111ll_opy_ (u"ࠢࠣ⥭"))
        return bstack1lll1l111_opy_