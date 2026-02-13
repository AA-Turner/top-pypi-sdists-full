# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import threading
from bstack_utils.helper import bstack1ll1l11lll_opy_
from bstack_utils.constants import bstack111ll1lllll_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11l1ll111l_opy_:
    bstack1lll1l1111ll_opy_ = None
    @classmethod
    def bstack11l1lll111_opy_(cls):
        if cls.on() and os.getenv(bstack11l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ⑬")):
            logger.info(
                bstack11l11_opy_ (u"ࠨࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠤࡹࡵࠠࡷ࡫ࡨࡻࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡰࡰࡴࡷ࠰ࠥ࡯࡮ࡴ࡫ࡪ࡬ࡹࡹࠬࠡࡣࡱࡨࠥࡳࡡ࡯ࡻࠣࡱࡴࡸࡥࠡࡦࡨࡦࡺ࡭ࡧࡪࡰࡪࠤ࡮ࡴࡦࡰࡴࡰࡥࡹ࡯࡯࡯ࠢࡤࡰࡱࠦࡡࡵࠢࡲࡲࡪࠦࡰ࡭ࡣࡦࡩࠦࡢ࡮ࠨ⑭").format(os.getenv(bstack11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⑮"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⑯"), None) is None or os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⑰")] == bstack11l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⑱"):
            return False
        return True
    @classmethod
    def bstack1ll1lll1llll_opy_(cls, bs_config, framework=bstack11l11_opy_ (u"ࠨࠢ⑲")):
        bstack111llll1111_opy_ = False
        for fw in bstack111ll1lllll_opy_:
            if fw in framework:
                bstack111llll1111_opy_ = True
        return bstack1ll1l11lll_opy_(bs_config.get(bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⑳"), bstack111llll1111_opy_))
    @classmethod
    def bstack1ll1ll1lllll_opy_(cls, framework):
        return framework in bstack111ll1lllll_opy_
    @classmethod
    def bstack1ll1llllll11_opy_(cls, bs_config, framework):
        return cls.bstack1ll1lll1llll_opy_(bs_config, framework) is True and cls.bstack1ll1ll1lllll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⑴"), None)
    @staticmethod
    def bstack11111ll1ll_opy_():
        if getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⑵"), None):
            return {
                bstack11l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ⑶"): bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩ⑷"),
                bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⑸"): getattr(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⑹"), None)
            }
        if getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⑺"), None):
            return {
                bstack11l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭⑻"): bstack11l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⑼"),
                bstack11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⑽"): getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⑾"), None)
            }
        return None
    @staticmethod
    def bstack1ll1ll1llll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l1ll111l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11111l11ll_opy_(test, hook_name=None):
        bstack1ll1lll1111l_opy_ = test.parent
        if hook_name in [bstack11l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ⑿"), bstack11l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ⒀"), bstack11l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭⒁"), bstack11l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪ⒂")]:
            bstack1ll1lll1111l_opy_ = test
        scope = []
        while bstack1ll1lll1111l_opy_ is not None:
            scope.append(bstack1ll1lll1111l_opy_.name)
            bstack1ll1lll1111l_opy_ = bstack1ll1lll1111l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1lll11111_opy_(hook_type):
        if hook_type == bstack11l11_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢ⒃"):
            return bstack11l11_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢ⒄")
        elif hook_type == bstack11l11_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣ⒅"):
            return bstack11l11_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧ⒆")
    @staticmethod
    def bstack1ll1ll1lll1l_opy_(bstack1111l1ll1_opy_):
        try:
            if not bstack11l1ll111l_opy_.on():
                return bstack1111l1ll1_opy_
            if os.environ.get(bstack11l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦ⒇"), None) == bstack11l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ⒈"):
                tests = os.environ.get(bstack11l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧ⒉"), None)
                if tests is None or tests == bstack11l11_opy_ (u"ࠤࡱࡹࡱࡲࠢ⒊"):
                    return bstack1111l1ll1_opy_
                bstack1111l1ll1_opy_ = tests.split(bstack11l11_opy_ (u"ࠪ࠰ࠬ⒋"))
                return bstack1111l1ll1_opy_
        except Exception as exc:
            logger.debug(bstack11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧ⒌") + str(str(exc)) + bstack11l11_opy_ (u"ࠧࠨ⒍"))
        return bstack1111l1ll1_opy_