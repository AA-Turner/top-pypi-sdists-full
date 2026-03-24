# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import threading
from bstack_utils.helper import bstack11llll111l_opy_
from bstack_utils.constants import bstack111l11lllll_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11lll1l11_opy_:
    bstack1ll1llllllll_opy_ = None
    @classmethod
    def bstack1111ll11l_opy_(cls):
        if cls.on() and os.getenv(bstack1ll1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ⚸")):
            logger.info(
                bstack1ll1lll_opy_ (u"ࠨࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨ⚹").format(os.getenv(bstack1ll1lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⚺"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⚻"), None) is None or os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⚼")] == bstack1ll1lll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⚽"):
            return False
        return True
    @classmethod
    def bstack1ll1l1l1l111_opy_(cls, bs_config, framework=bstack1ll1lll_opy_ (u"ࠨࠢ⚾")):
        bstack111l1l1ll1l_opy_ = False
        for fw in bstack111l11lllll_opy_:
            if fw in framework:
                bstack111l1l1ll1l_opy_ = True
        return bstack11llll111l_opy_(bs_config.get(bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⚿"), bstack111l1l1ll1l_opy_))
    @classmethod
    def bstack1ll1l1l111l1_opy_(cls, framework):
        return framework in bstack111l11lllll_opy_
    @classmethod
    def bstack1ll1l1lll111_opy_(cls, bs_config, framework):
        return cls.bstack1ll1l1l1l111_opy_(bs_config, framework) is True and cls.bstack1ll1l1l111l1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⛀"), None)
    @staticmethod
    def bstack1llllll1l1l_opy_():
        if getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⛁"), None):
            return {
                bstack1ll1lll_opy_ (u"ࠪࡸࡾࡶࡥࠨ⛂"): bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ⛃"),
                bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⛄"): getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⛅"), None)
            }
        if getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⛆"), None):
            return {
                bstack1ll1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭⛇"): bstack1ll1lll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⛈"),
                bstack1ll1lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⛉"): getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⛊"), None)
            }
        return None
    @staticmethod
    def bstack1ll1l1l111ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11lll1l11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1llll1l1111_opy_(test, hook_name=None):
        bstack1ll1l1l11l11_opy_ = test.parent
        if hook_name in [bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ⛋"), bstack1ll1lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ⛌"), bstack1ll1lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭⛍"), bstack1ll1lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ⛎")]:
            bstack1ll1l1l11l11_opy_ = test
        scope = []
        while bstack1ll1l1l11l11_opy_ is not None:
            scope.append(bstack1ll1l1l11l11_opy_.name)
            bstack1ll1l1l11l11_opy_ = bstack1ll1l1l11l11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1l1l1111l_opy_(hook_type):
        if hook_type == bstack1ll1lll_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢ⛏"):
            return bstack1ll1lll_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢ⛐")
        elif hook_type == bstack1ll1lll_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣ⛑"):
            return bstack1ll1lll_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧ⛒")
    @staticmethod
    def bstack1ll1l1l11111_opy_(bstack111ll1llll_opy_):
        try:
            if not bstack11lll1l11_opy_.on():
                return bstack111ll1llll_opy_
            if os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦ⛓"), None) == bstack1ll1lll_opy_ (u"ࠢࡵࡴࡸࡩࠧ⛔"):
                tests = os.environ.get(bstack1ll1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧ⛕"), None)
                if tests is None or tests == bstack1ll1lll_opy_ (u"ࠤࡱࡹࡱࡲࠢ⛖"):
                    return bstack111ll1llll_opy_
                bstack111ll1llll_opy_ = tests.split(bstack1ll1lll_opy_ (u"ࠪ࠰ࠬ⛗"))
                return bstack111ll1llll_opy_
        except Exception as exc:
            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧ⛘") + str(str(exc)) + bstack1ll1lll_opy_ (u"ࠧࠨ⛙"))
        return bstack111ll1llll_opy_