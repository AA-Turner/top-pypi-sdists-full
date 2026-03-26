# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import threading
from bstack_utils.helper import bstack1l11l11111_opy_
from bstack_utils.constants import bstack111l1l11111_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11llll1l_opy_:
    bstack1ll1llllll11_opy_ = None
    @classmethod
    def bstack1l1lllll1l_opy_(cls):
        if cls.on() and os.getenv(bstack1ll1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⛙")):
            logger.info(
                bstack1ll1lll_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭⛚").format(os.getenv(bstack1ll1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ⛛"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⛜"), None) is None or os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⛝")] == bstack1ll1lll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⛞"):
            return False
        return True
    @classmethod
    def bstack1ll1l1l1l11l_opy_(cls, bs_config, framework=bstack1ll1lll_opy_ (u"ࠦࠧ⛟")):
        bstack111l1l11l1l_opy_ = False
        for fw in bstack111l1l11111_opy_:
            if fw in framework:
                bstack111l1l11l1l_opy_ = True
        return bstack1l11l11111_opy_(bs_config.get(bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⛠"), bstack111l1l11l1l_opy_))
    @classmethod
    def bstack1ll1l11l1lll_opy_(cls, framework):
        return framework in bstack111l1l11111_opy_
    @classmethod
    def bstack1ll1l1lll1ll_opy_(cls, bs_config, framework):
        return cls.bstack1ll1l1l1l11l_opy_(bs_config, framework) is True and cls.bstack1ll1l11l1lll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⛡"), None)
    @staticmethod
    def bstack1llll1lll11_opy_():
        if getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⛢"), None):
            return {
                bstack1ll1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭⛣"): bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࠧ⛤"),
                bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⛥"): getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⛦"), None)
            }
        if getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⛧"), None):
            return {
                bstack1ll1lll_opy_ (u"࠭ࡴࡺࡲࡨࠫ⛨"): bstack1ll1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⛩"),
                bstack1ll1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⛪"): getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⛫"), None)
            }
        return None
    @staticmethod
    def bstack1ll1l11ll1l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11llll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1lll1ll11l1_opy_(test, hook_name=None):
        bstack1ll1l11ll11l_opy_ = test.parent
        if hook_name in [bstack1ll1lll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ⛬"), bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ⛭"), bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⛮"), bstack1ll1lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⛯")]:
            bstack1ll1l11ll11l_opy_ = test
        scope = []
        while bstack1ll1l11ll11l_opy_ is not None:
            scope.append(bstack1ll1l11ll11l_opy_.name)
            bstack1ll1l11ll11l_opy_ = bstack1ll1l11ll11l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1l11ll111_opy_(hook_type):
        if hook_type == bstack1ll1lll_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧ⛰"):
            return bstack1ll1lll_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧ⛱")
        elif hook_type == bstack1ll1lll_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨ⛲"):
            return bstack1ll1lll_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥ⛳")
    @staticmethod
    def bstack1ll1l11ll1ll_opy_(bstack11llll1l11_opy_):
        try:
            if not bstack11llll1l_opy_.on():
                return bstack11llll1l11_opy_
            if os.environ.get(bstack1ll1lll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤ⛴"), None) == bstack1ll1lll_opy_ (u"ࠧࡺࡲࡶࡧࠥ⛵"):
                tests = os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥ⛶"), None)
                if tests is None or tests == bstack1ll1lll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⛷"):
                    return bstack11llll1l11_opy_
                bstack11llll1l11_opy_ = tests.split(bstack1ll1lll_opy_ (u"ࠨ࠮ࠪ⛸"))
                return bstack11llll1l11_opy_
        except Exception as exc:
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥ⛹") + str(str(exc)) + bstack1ll1lll_opy_ (u"ࠥࠦ⛺"))
        return bstack11llll1l11_opy_