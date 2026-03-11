# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import threading
from bstack_utils.helper import bstack1l11lll111_opy_
from bstack_utils.constants import bstack1111l1l11l1_opy_, EVENTS, STAGE
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack11l1ll1111_opy_:
    bstack1llll111l11l_opy_ = None
    @classmethod
    def bstack11ll1l11l1_opy_(cls):
        if cls.on() and os.getenv(bstack1ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⃎")):
            logger.info(
                bstack1ll111_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭⃏").format(os.getenv(bstack1ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ⃐"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⃑"), None) is None or os.environ[bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ⃒࡛࡙࠭")] == bstack1ll111_opy_ (u"ࠥࡲࡺࡲ࡬⃓ࠣ"):
            return False
        return True
    @classmethod
    def bstack1lll11l1l1l1_opy_(cls, bs_config, framework=bstack1ll111_opy_ (u"ࠦࠧ⃔")):
        bstack1111l11lll1_opy_ = False
        for fw in bstack1111l1l11l1_opy_:
            if fw in framework:
                bstack1111l11lll1_opy_ = True
        return bstack1l11lll111_opy_(bs_config.get(bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⃕"), bstack1111l11lll1_opy_))
    @classmethod
    def bstack1lll111ll1l1_opy_(cls, framework):
        return framework in bstack1111l1l11l1_opy_
    @classmethod
    def bstack1lll11l1l1ll_opy_(cls, bs_config, framework):
        return cls.bstack1lll11l1l1l1_opy_(bs_config, framework) is True and cls.bstack1lll111ll1l1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⃖"), None)
    @staticmethod
    def bstack11111l1111_opy_():
        if getattr(threading.current_thread(), bstack1ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⃗"), None):
            return {
                bstack1ll111_opy_ (u"ࠨࡶࡼࡴࡪ⃘࠭"): bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ⃙ࠧ"),
                bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦ⃚ࠪ"): getattr(threading.current_thread(), bstack1ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ⃛"), None)
            }
        if getattr(threading.current_thread(), bstack1ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⃜"), None):
            return {
                bstack1ll111_opy_ (u"࠭ࡴࡺࡲࡨࠫ⃝"): bstack1ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⃞"),
                bstack1ll111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⃟"): getattr(threading.current_thread(), bstack1ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⃠"), None)
            }
        return None
    @staticmethod
    def bstack1lll111ll1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l1ll1111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111111l1l1_opy_(test, hook_name=None):
        bstack1lll111ll111_opy_ = test.parent
        if hook_name in [bstack1ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨ⃡"), bstack1ll111_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬ⃢"), bstack1ll111_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⃣"), bstack1ll111_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⃤")]:
            bstack1lll111ll111_opy_ = test
        scope = []
        while bstack1lll111ll111_opy_ is not None:
            scope.append(bstack1lll111ll111_opy_.name)
            bstack1lll111ll111_opy_ = bstack1lll111ll111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll111ll11l_opy_(hook_type):
        if hook_type == bstack1ll111_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌ⃥ࠧ"):
            return bstack1ll111_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯⃦ࠧ")
        elif hook_type == bstack1ll111_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨ⃧"):
            return bstack1ll111_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭⃨ࠥ")
    @staticmethod
    def bstack1lll111lll11_opy_(bstack11l111l111_opy_):
        try:
            if not bstack11l1ll1111_opy_.on():
                return bstack11l111l111_opy_
            if os.environ.get(bstack1ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤ⃩"), None) == bstack1ll111_opy_ (u"ࠧࡺࡲࡶࡧ⃪ࠥ"):
                tests = os.environ.get(bstack1ll111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕ⃫ࠥ"), None)
                if tests is None or tests == bstack1ll111_opy_ (u"ࠢ࡯ࡷ࡯ࡰ⃬ࠧ"):
                    return bstack11l111l111_opy_
                bstack11l111l111_opy_ = tests.split(bstack1ll111_opy_ (u"ࠨ࠮⃭ࠪ"))
                return bstack11l111l111_opy_
        except Exception as exc:
            logger.debug(bstack1ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻⃮ࠢࠥ") + str(str(exc)) + bstack1ll111_opy_ (u"⃯ࠥࠦ"))
        return bstack11l111l111_opy_