# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
import threading
from bstack_utils.helper import bstack11lll11l1l_opy_
from bstack_utils.constants import bstack1111111l1l1_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1ll111ll_opy_:
    bstack1ll111l1ll1l_opy_ = None
    @classmethod
    def bstack1lll1lll11_opy_(cls):
        if cls.on() and os.getenv(bstack1l1llll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤⳎ")):
            logger.info(
                bstack1l1llll_opy_ (u"ࠬ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬⳏ").format(os.getenv(bstack1l1llll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦⳐ"))))
    @classmethod
    def bstack1l1l1l1l1l_opy_(cls, config=None):
        try:
            bstack1llll1111l1l_opy_ = os.getenv(bstack1l1llll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧⳑ"))
            if not bstack1llll1111l1l_opy_:
                return
            bstack1l1ll1ll11l1_opy_ = os.getenv(bstack1l1llll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭Ⳓ"))
            bstack1ll111l111_opy_ = bstack1l1ll1ll11l1_opy_ is not None and bstack1l1ll1ll11l1_opy_ != bstack1l1llll_opy_ (u"ࠩࡱࡹࡱࡲࠧⳓ") and len(bstack1l1ll1ll11l1_opy_) > 0
            bstack1l1ll1ll11ll_opy_ = config.get(bstack1l1llll_opy_ (u"ࠪࡥࡵࡶࠧⳔ")) is not None if config else False
            if bstack1ll111l111_opy_ and not bstack1l1ll1ll11ll_opy_:
                logger.info(
                    bstack1l1llll_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡷࡷࡳࡲࡧࡴࡦࡦ࠰ࡸࡪࡹࡴࡴ࠱ࡳࡶࡴࡰࡥࡤࡶࡶ࠳ࡵ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡢ࠰࠳ࡂࡸ࡭ࡈࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡶ࡯ࡳࡶ࠱ࡠࡳ࠭ⳕ").format(bstack1llll1111l1l_opy_))
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡸࡩ࡯ࡶ࡬ࡲ࡬ࠦࡡ࠲࠳ࡼࠤࡧࡻࡩ࡭ࡦࠣࡰ࡮ࡴ࡫࠻ࠢࡾࢁࠧⳖ").format(e))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪⳗ"), None) is None or os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫⳘ")] == bstack1l1llll_opy_ (u"ࠣࡰࡸࡰࡱࠨⳙ"):
            return False
        return True
    @classmethod
    def bstack1l1ll1llllll_opy_(cls, bs_config, framework=bstack1l1llll_opy_ (u"ࠤࠥⳚ")):
        bstack111111l11l1_opy_ = False
        for fw in bstack1111111l1l1_opy_:
            if fw in framework:
                bstack111111l11l1_opy_ = True
        return bstack11lll11l1l_opy_(bs_config.get(bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧⳛ"), bstack111111l11l1_opy_))
    @classmethod
    def bstack1l1ll1ll1l1l_opy_(cls, framework):
        return framework in bstack1111111l1l1_opy_
    @classmethod
    def bstack1l1lll1ll11l_opy_(cls, bs_config, framework):
        return cls.bstack1l1ll1llllll_opy_(bs_config, framework) is True and cls.bstack1l1ll1ll1l1l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨⳜ"), None)
    @staticmethod
    def bstack11llll1l_opy_():
        if getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩⳝ"), None):
            return {
                bstack1l1llll_opy_ (u"࠭ࡴࡺࡲࡨࠫⳞ"): bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࠬⳟ"),
                bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨⳠ"): getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ⳡ"), None)
            }
        if getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧⳢ"), None):
            return {
                bstack1l1llll_opy_ (u"ࠫࡹࡿࡰࡦࠩⳣ"): bstack1l1llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪⳤ"),
                bstack1l1llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⳥"): getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⳦"), None)
            }
        return None
    @staticmethod
    def bstack1l1ll1ll1ll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll111ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1llll1ll1_opy_(test, hook_name=None):
        bstack1l1ll1ll1l11_opy_ = test.parent
        if hook_name in [bstack1l1llll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⳧"), bstack1l1llll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ⳨"), bstack1l1llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ⳩"), bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭⳪")]:
            bstack1l1ll1ll1l11_opy_ = test
        scope = []
        while bstack1l1ll1ll1l11_opy_ is not None:
            scope.append(bstack1l1ll1ll1l11_opy_.name)
            bstack1l1ll1ll1l11_opy_ = bstack1l1ll1ll1l11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1l1ll1ll111l_opy_(hook_type):
        if hook_type == bstack1l1llll_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥⳫ"):
            return bstack1l1llll_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥⳬ")
        elif hook_type == bstack1l1llll_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦⳭ"):
            return bstack1l1llll_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣⳮ")
    @staticmethod
    def bstack1l1ll1ll1lll_opy_(bstack1lll1lll_opy_):
        try:
            if not bstack1ll111ll_opy_.on():
                return bstack1lll1lll_opy_
            if os.environ.get(bstack1l1llll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢ⳯"), None) == bstack1l1llll_opy_ (u"ࠥࡸࡷࡻࡥࠣ⳰"):
                tests = os.environ.get(bstack1l1llll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣ⳱"), None)
                if tests is None or tests == bstack1l1llll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥⳲ"):
                    return bstack1lll1lll_opy_
                bstack1lll1lll_opy_ = tests.split(bstack1l1llll_opy_ (u"࠭ࠬࠨⳳ"))
                return bstack1lll1lll_opy_
        except Exception as exc:
            logger.debug(bstack1l1llll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣ⳴") + str(str(exc)) + bstack1l1llll_opy_ (u"ࠣࠤ⳵"))
        return bstack1lll1lll_opy_