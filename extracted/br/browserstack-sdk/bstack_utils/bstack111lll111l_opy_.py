# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
import threading
from bstack_utils.helper import bstack1l111ll1l_opy_
from bstack_utils.constants import bstack11ll1111111_opy_, EVENTS, STAGE
from bstack_utils.bstack1111l1ll1_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l1ll11_opy_:
    bstack11111l111l1_opy_ = None
    @classmethod
    def bstack1l1l11ll_opy_(cls):
        if cls.on() and os.getenv(bstack11ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄ⃯ࠣ")):
            logger.info(
                bstack11ll11_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧ⃰").format(os.getenv(bstack11ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⃱"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⃲"), None) is None or os.environ[bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⃳")] == bstack11ll11_opy_ (u"ࠣࡰࡸࡰࡱࠨ⃴"):
            return False
        return True
    @classmethod
    def bstack1lllll111ll1_opy_(cls, bs_config, framework=bstack11ll11_opy_ (u"ࠤࠥ⃵")):
        bstack11ll11l11ll_opy_ = False
        for fw in bstack11ll1111111_opy_:
            if fw in framework:
                bstack11ll11l11ll_opy_ = True
        return bstack1l111ll1l_opy_(bs_config.get(bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⃶"), bstack11ll11l11ll_opy_))
    @classmethod
    def bstack1lllll1111l1_opy_(cls, framework):
        return framework in bstack11ll1111111_opy_
    @classmethod
    def bstack1lllll1ll1ll_opy_(cls, bs_config, framework):
        return cls.bstack1lllll111ll1_opy_(bs_config, framework) is True and cls.bstack1lllll1111l1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⃷"), None)
    @staticmethod
    def bstack111llll1l1_opy_():
        if getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⃸"), None):
            return {
                bstack11ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫ⃹"): bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࠬ⃺"),
                bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⃻"): getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⃼"), None)
            }
        if getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⃽"), None):
            return {
                bstack11ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩ⃾"): bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ⃿"),
                bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭℀"): getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ℁"), None)
            }
        return None
    @staticmethod
    def bstack1lllll1111ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l1ll11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111ll111ll_opy_(test, hook_name=None):
        bstack1lllll111l11_opy_ = test.parent
        if hook_name in [bstack11ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ℂ"), bstack11ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ℃"), bstack11ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ℄"), bstack11ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭℅")]:
            bstack1lllll111l11_opy_ = test
        scope = []
        while bstack1lllll111l11_opy_ is not None:
            scope.append(bstack1lllll111l11_opy_.name)
            bstack1lllll111l11_opy_ = bstack1lllll111l11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lllll111l1l_opy_(hook_type):
        if hook_type == bstack11ll11_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥ℆"):
            return bstack11ll11_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥℇ")
        elif hook_type == bstack11ll11_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦ℈"):
            return bstack11ll11_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣ℉")
    @staticmethod
    def bstack1lllll11111l_opy_(bstack11ll1l11_opy_):
        try:
            if not bstack11l1ll11_opy_.on():
                return bstack11ll1l11_opy_
            if os.environ.get(bstack11ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢℊ"), None) == bstack11ll11_opy_ (u"ࠥࡸࡷࡻࡥࠣℋ"):
                tests = os.environ.get(bstack11ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣℌ"), None)
                if tests is None or tests == bstack11ll11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥℍ"):
                    return bstack11ll1l11_opy_
                bstack11ll1l11_opy_ = tests.split(bstack11ll11_opy_ (u"࠭ࠬࠨℎ"))
                return bstack11ll1l11_opy_
        except Exception as exc:
            logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣℏ") + str(str(exc)) + bstack11ll11_opy_ (u"ࠣࠤℐ"))
        return bstack11ll1l11_opy_