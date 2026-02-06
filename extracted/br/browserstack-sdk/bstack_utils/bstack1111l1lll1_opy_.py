# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import threading
from bstack_utils.helper import bstack1ll1ll111_opy_
from bstack_utils.constants import bstack11l111lll11_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1l1l11llll_opy_:
    bstack1lll1lll1lll_opy_ = None
    @classmethod
    def bstack1l1lll11ll_opy_(cls):
        if cls.on() and os.getenv(bstack11lllll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⎠")):
            logger.info(
                bstack11lllll_opy_ (u"ࠧࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧ⎡").format(os.getenv(bstack11lllll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ⎢"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⎣"), None) is None or os.environ[bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⎤")] == bstack11lllll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⎥"):
            return False
        return True
    @classmethod
    def bstack1lll111lll1l_opy_(cls, bs_config, framework=bstack11lllll_opy_ (u"ࠧࠨ⎦")):
        bstack11l11l11l1l_opy_ = False
        for fw in bstack11l111lll11_opy_:
            if fw in framework:
                bstack11l11l11l1l_opy_ = True
        return bstack1ll1ll111_opy_(bs_config.get(bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⎧"), bstack11l11l11l1l_opy_))
    @classmethod
    def bstack1lll111l11ll_opy_(cls, framework):
        return framework in bstack11l111lll11_opy_
    @classmethod
    def bstack1lll11lll11l_opy_(cls, bs_config, framework):
        return cls.bstack1lll111lll1l_opy_(bs_config, framework) is True and cls.bstack1lll111l11ll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⎨"), None)
    @staticmethod
    def bstack1111ll1ll1_opy_():
        if getattr(threading.current_thread(), bstack11lllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⎩"), None):
            return {
                bstack11lllll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⎪"): bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࠨ⎫"),
                bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⎬"): getattr(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⎭"), None)
            }
        if getattr(threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⎮"), None):
            return {
                bstack11lllll_opy_ (u"ࠧࡵࡻࡳࡩࠬ⎯"): bstack11lllll_opy_ (u"ࠨࡪࡲࡳࡰ࠭⎰"),
                bstack11lllll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⎱"): getattr(threading.current_thread(), bstack11lllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⎲"), None)
            }
        return None
    @staticmethod
    def bstack1lll111l11l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1l11llll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1111111lll_opy_(test, hook_name=None):
        bstack1lll111l1111_opy_ = test.parent
        if hook_name in [bstack11lllll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ⎳"), bstack11lllll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭⎴"), bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⎵"), bstack11lllll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⎶")]:
            bstack1lll111l1111_opy_ = test
        scope = []
        while bstack1lll111l1111_opy_ is not None:
            scope.append(bstack1lll111l1111_opy_.name)
            bstack1lll111l1111_opy_ = bstack1lll111l1111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll111l111l_opy_(hook_type):
        if hook_type == bstack11lllll_opy_ (u"ࠣࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍࠨ⎷"):
            return bstack11lllll_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡪࡲࡳࡰࠨ⎸")
        elif hook_type == bstack11lllll_opy_ (u"ࠥࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠢ⎹"):
            return bstack11lllll_opy_ (u"࡙ࠦ࡫ࡡࡳࡦࡲࡻࡳࠦࡨࡰࡱ࡮ࠦ⎺")
    @staticmethod
    def bstack1lll111l1l11_opy_(bstack111l11111_opy_):
        try:
            if not bstack1l1l11llll_opy_.on():
                return bstack111l11111_opy_
            if os.environ.get(bstack11lllll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠥ⎻"), None) == bstack11lllll_opy_ (u"ࠨࡴࡳࡷࡨࠦ⎼"):
                tests = os.environ.get(bstack11lllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠦ⎽"), None)
                if tests is None or tests == bstack11lllll_opy_ (u"ࠣࡰࡸࡰࡱࠨ⎾"):
                    return bstack111l11111_opy_
                bstack111l11111_opy_ = tests.split(bstack11lllll_opy_ (u"ࠩ࠯ࠫ⎿"))
                return bstack111l11111_opy_
        except Exception as exc:
            logger.debug(bstack11lllll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡩࡷࡻ࡮ࠡࡪࡤࡲࡩࡲࡥࡳ࠼ࠣࠦ⏀") + str(str(exc)) + bstack11lllll_opy_ (u"ࠦࠧ⏁"))
        return bstack111l11111_opy_