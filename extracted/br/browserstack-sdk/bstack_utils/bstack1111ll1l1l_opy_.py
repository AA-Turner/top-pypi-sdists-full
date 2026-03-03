# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
import threading
from bstack_utils.helper import bstack11l1lll1_opy_
from bstack_utils.constants import bstack111lll11l11_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11lll1ll1_opy_:
    bstack1lll1l1l11ll_opy_ = None
    @classmethod
    def bstack11ll1lll_opy_(cls):
        if cls.on() and os.getenv(bstack11ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ⑴")):
            logger.info(
                bstack11ll111_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩ⑵").format(os.getenv(bstack11ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ⑶"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⑷"), None) is None or os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⑸")] == bstack11ll111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⑹"):
            return False
        return True
    @classmethod
    def bstack1ll1lllll1l1_opy_(cls, bs_config, framework=bstack11ll111_opy_ (u"ࠢࠣ⑺")):
        bstack111lllllll1_opy_ = False
        for fw in bstack111lll11l11_opy_:
            if fw in framework:
                bstack111lllllll1_opy_ = True
        return bstack11l1lll1_opy_(bs_config.get(bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⑻"), bstack111lllllll1_opy_))
    @classmethod
    def bstack1ll1lll1llll_opy_(cls, framework):
        return framework in bstack111lll11l11_opy_
    @classmethod
    def bstack1lll111l1lll_opy_(cls, bs_config, framework):
        return cls.bstack1ll1lllll1l1_opy_(bs_config, framework) is True and cls.bstack1ll1lll1llll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⑼"), None)
    @staticmethod
    def bstack1111l1lll1_opy_():
        if getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⑽"), None):
            return {
                bstack11ll111_opy_ (u"ࠫࡹࡿࡰࡦࠩ⑾"): bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࠪ⑿"),
                bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⒀"): getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⒁"), None)
            }
        if getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⒂"), None):
            return {
                bstack11ll111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⒃"): bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⒄"),
                bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⒅"): getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⒆"), None)
            }
        return None
    @staticmethod
    def bstack1ll1llll111l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11lll1ll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111111ll1l_opy_(test, hook_name=None):
        bstack1ll1lll1ll1l_opy_ = test.parent
        if hook_name in [bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ⒇"), bstack11ll111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨ⒈"), bstack11ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⒉"), bstack11ll111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ⒊")]:
            bstack1ll1lll1ll1l_opy_ = test
        scope = []
        while bstack1ll1lll1ll1l_opy_ is not None:
            scope.append(bstack1ll1lll1ll1l_opy_.name)
            bstack1ll1lll1ll1l_opy_ = bstack1ll1lll1ll1l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll1llll1111_opy_(hook_type):
        if hook_type == bstack11ll111_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣ⒋"):
            return bstack11ll111_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣ⒌")
        elif hook_type == bstack11ll111_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤ⒍"):
            return bstack11ll111_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨ⒎")
    @staticmethod
    def bstack1ll1lll1lll1_opy_(bstack1l111l1lll_opy_):
        try:
            if not bstack11lll1ll1_opy_.on():
                return bstack1l111l1lll_opy_
            if os.environ.get(bstack11ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧ⒏"), None) == bstack11ll111_opy_ (u"ࠣࡶࡵࡹࡪࠨ⒐"):
                tests = os.environ.get(bstack11ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨ⒑"), None)
                if tests is None or tests == bstack11ll111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⒒"):
                    return bstack1l111l1lll_opy_
                bstack1l111l1lll_opy_ = tests.split(bstack11ll111_opy_ (u"ࠫ࠱࠭⒓"))
                return bstack1l111l1lll_opy_
        except Exception as exc:
            logger.debug(bstack11ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨ⒔") + str(str(exc)) + bstack11ll111_opy_ (u"ࠨࠢ⒕"))
        return bstack1l111l1lll_opy_