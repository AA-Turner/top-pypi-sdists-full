# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
import threading
from bstack_utils.helper import bstack1ll111lll_opy_
from bstack_utils.constants import bstack1111111l1ll_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1l1lll1l1_opy_:
    bstack1ll11llll1ll_opy_ = None
    @classmethod
    def bstack11llll1111_opy_(cls):
        if cls.on() and os.getenv(bstack1l1111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⣼")):
            logger.info(
                bstack1l1111l_opy_ (u"ࠧࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧ⣽").format(os.getenv(bstack1l1111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ⣾"))))
    @classmethod
    def bstack1l111lllll_opy_(cls, config=None):
        try:
            bstack1ll1111ll111_opy_ = os.getenv(bstack1l1111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⣿"))
            if not bstack1ll1111ll111_opy_:
                return
            bstack1ll1111l1lll_opy_ = os.getenv(bstack1l1111l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⤀"))
            bstack1l1lllll1l_opy_ = bstack1ll1111l1lll_opy_ is not None and bstack1ll1111l1lll_opy_ != bstack1l1111l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⤁") and len(bstack1ll1111l1lll_opy_) > 0
            bstack1ll1111lll1l_opy_ = config.get(bstack1l1111l_opy_ (u"ࠬࡧࡰࡱࠩ⤂")) is not None if config else False
            if bstack1l1lllll1l_opy_ and not bstack1ll1111lll1l_opy_:
                logger.info(
                    bstack1l1111l_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨࡨ࠲ࡺࡥࡴࡶࡶ࠳ࡵࡸ࡯࡫ࡧࡦࡸࡸ࠵ࡰ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡤ࠲࠵ࡄࡺࡨࡃࡷ࡬ࡰࡩࡏࡤ࠾ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡱࡱࡵࡸ࠳ࡢ࡮ࠨ⤃").format(bstack1ll1111ll111_opy_))
        except Exception as e:
            logger.debug(bstack1l1111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡳ࡫ࡱࡸ࡮ࡴࡧࠡࡣ࠴࠵ࡾࠦࡢࡶ࡫࡯ࡨࠥࡲࡩ࡯࡭࠽ࠤࢀࢃࠢ⤄").format(e))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⤅"), None) is None or os.environ[bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⤆")] == bstack1l1111l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⤇"):
            return False
        return True
    @classmethod
    def bstack1ll111l111l1_opy_(cls, bs_config, framework=bstack1l1111l_opy_ (u"ࠦࠧ⤈")):
        bstack11111ll111l_opy_ = False
        for fw in bstack1111111l1ll_opy_:
            if fw in framework:
                bstack11111ll111l_opy_ = True
        return bstack1ll111lll_opy_(bs_config.get(bstack1l1111l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⤉"), bstack11111ll111l_opy_))
    @classmethod
    def bstack1ll1111lll11_opy_(cls, framework):
        return framework in bstack1111111l1ll_opy_
    @classmethod
    def bstack1ll111ll1ll1_opy_(cls, bs_config, framework):
        return cls.bstack1ll111l111l1_opy_(bs_config, framework) is True and cls.bstack1ll1111lll11_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⤊"), None)
    @staticmethod
    def bstack1llll11l11l_opy_():
        if getattr(threading.current_thread(), bstack1l1111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⤋"), None):
            return {
                bstack1l1111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭⤌"): bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺࠧ⤍"),
                bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⤎"): getattr(threading.current_thread(), bstack1l1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⤏"), None)
            }
        if getattr(threading.current_thread(), bstack1l1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⤐"), None):
            return {
                bstack1l1111l_opy_ (u"࠭ࡴࡺࡲࡨࠫ⤑"): bstack1l1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⤒"),
                bstack1l1111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⤓"): getattr(threading.current_thread(), bstack1l1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⤔"), None)
            }
        return None
    @staticmethod
    def bstack1ll1111ll1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1lll1l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1lll1l11ll1_opy_(test, hook_name=None):
        bstack1ll1111ll11l_opy_ = test.parent
        if hook_name in [bstack1l1111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ⤕"), bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ⤖"), bstack1l1111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⤗"), bstack1l1111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⤘")]:
            bstack1ll1111ll11l_opy_ = test
        scope = []
        while bstack1ll1111ll11l_opy_ is not None:
            scope.append(bstack1ll1111ll11l_opy_.name)
            bstack1ll1111ll11l_opy_ = bstack1ll1111ll11l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1111l1ll1_opy_(hook_type):
        if hook_type == bstack1l1111l_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧ⤙"):
            return bstack1l1111l_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧ⤚")
        elif hook_type == bstack1l1111l_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨ⤛"):
            return bstack1l1111l_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥ⤜")
    @staticmethod
    def bstack1ll1111ll1l1_opy_(bstack11ll1l11ll_opy_):
        try:
            if not bstack1l1lll1l1_opy_.on():
                return bstack11ll1l11ll_opy_
            if os.environ.get(bstack1l1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤ⤝"), None) == bstack1l1111l_opy_ (u"ࠧࡺࡲࡶࡧࠥ⤞"):
                tests = os.environ.get(bstack1l1111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥ⤟"), None)
                if tests is None or tests == bstack1l1111l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⤠"):
                    return bstack11ll1l11ll_opy_
                bstack11ll1l11ll_opy_ = tests.split(bstack1l1111l_opy_ (u"ࠨ࠮ࠪ⤡"))
                return bstack11ll1l11ll_opy_
        except Exception as exc:
            logger.debug(bstack1l1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥ⤢") + str(str(exc)) + bstack1l1111l_opy_ (u"ࠥࠦ⤣"))
        return bstack11ll1l11ll_opy_