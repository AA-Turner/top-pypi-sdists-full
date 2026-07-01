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
import threading
import os
import logging
import json
from uuid import uuid4
from bstack_utils.test_data import bstack11ll1l1l_opy_, bstack1l1l1111_opy_
from bstack_utils.bstack11l111ll_opy_ import bstack1ll111ll_opy_
from bstack_utils.helper import bstack11llll11_opy_, bstack1l1111ll_opy_, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack111ll1l1_opy_
from bstack_utils.constants import *
from bstack_utils.config import Config
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.test_framework import TestFrameworkContext, TestFrameworkState, TestHookState
logger = logging.getLogger(__name__)
try:
    import behave as _11lllll1_opy_
    _111l1lll_opy_ = getattr(_11lllll1_opy_, bstack1l1llll_opy_ (u"࠭࡟ࡠࡸࡨࡶࡸ࡯࡯࡯ࡡࡢࠫ࣍"), bstack1l1llll_opy_ (u"ࠧ࠲࠰࠵࠲࠻࠭࣎"))
except ImportError:
    _111l1lll_opy_ = bstack1l1llll_opy_ (u"ࠨ࠳࠱࠶࠳࠼࣏ࠧ")
class bstack_behave_listener:
    def __init__(self):
        self.bstack11l1l111_opy_ = bstack111ll1l1_opy_(self.log_handler)
        self.tests = {}
        self._thread_local = threading.local()
    def _111l1ll1_opy_(self):
        bstack1l1llll_opy_ (u"ࠤ࡙ࠥࠦ࡮ࡲࡦࡣࡧ࠱ࡸࡧࡦࡦࠢࡪࡩࡹࡺࡥࡳࠢࡩࡳࡷࠦ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤࡪ࡯࡯ࡧࠣࡪࡱࡧࡧ࠯ࠤ࣐ࠥࠦ")
        return getattr(self._thread_local, bstack1l1llll_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡦࡲࡲࡪ࣑࠭"), False)
    def _11ll1lll_opy_(self, value):
        bstack1l1llll_opy_ (u"ࠦࠧࠨࡔࡩࡴࡨࡥࡩ࠳ࡳࡢࡨࡨࠤࡸ࡫ࡴࡵࡧࡵࠤ࡫ࡵࡲࠡࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࡟ࡥࡱࡱࡩࠥ࡬࡬ࡢࡩ࠱ࠦࠧࠨ࣒")
        setattr(self._thread_local, bstack1l1llll_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶࡢࡨࡴࡴࡥࠨ࣓"), value)
    def _11l1ll1l_opy_(self):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡖ࡫ࡶࡪࡧࡤ࠮ࡵࡤࡪࡪࠦࡧࡦࡶࡷࡩࡷࠦࡦࡰࡴࠣࡧࡦࡩࡨࡦࡦࠣࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠮ࠣࠤࠥࣔ")
        return getattr(self._thread_local, bstack1l1llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫࣕ"), None)
    def _1l11l11l_opy_(self, value):
        bstack1l1llll_opy_ (u"ࠣࠤࠥࡘ࡭ࡸࡥࡢࡦ࠰ࡷࡦ࡬ࡥࠡࡵࡨࡸࡹ࡫ࡲࠡࡨࡲࡶࠥࡩࡡࡤࡪࡨࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠰ࠥࠦࠧࣖ")
        setattr(self._thread_local, bstack1l1llll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ࣗ"), value)
    def _11l111l1_opy_(self):
        bstack1l1llll_opy_ (u"࡚ࠥࠦࠧࡨࡳࡧࡤࡨ࠲ࡹࡡࡧࡧࠣ࡫ࡪࡺࡴࡦࡴࠣࡪࡴࡸࠠࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫࡟ࡴࡧࡷࠤ࡫ࡲࡡࡨ࠰ࠥࠦࠧࣘ")
        return getattr(self._thread_local, bstack1l1llll_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࡢࡷࡪࡺࠧࣙ"), False)
    def _1l1lll1l_opy_(self, value):
        bstack1l1llll_opy_ (u"ࠧࠨࠢࡕࡪࡵࡩࡦࡪ࠭ࡴࡣࡩࡩࠥࡹࡥࡵࡶࡨࡶࠥ࡬࡯ࡳࠢࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࡡࡶࡩࡹࠦࡦ࡭ࡣࡪ࠲ࠧࠨࠢࣚ")
        setattr(self._thread_local, bstack1l1llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࡤࡹࡥࡵࠩࣛ"), value)
    def _111ll11l_opy_(self):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡗ࡬ࡷ࡫ࡡࡥ࠯ࡶࡥ࡫࡫ࠠࡨࡧࡷࡸࡪࡸࠠࡧࡱࡵࠤࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸࡥ࡭ࡢࡴ࡮ࡩࡩࠦࡦ࡭ࡣࡪ࠲ࠧࠨࠢࣜ")
        return getattr(self._thread_local, bstack1l1llll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࡡࡰࡥࡷࡱࡥࡥࠩࣝ"), None)
    def _111lll11_opy_(self, value):
        bstack1l1llll_opy_ (u"ࠤࠥࠦࡥࡦࡥ࡯ࡦࡢࡷࡹ࡫ࡰࡡࡢ࠰ࡰࡴࡩࡡ࡭ࠢ࡯ࡥࡹࡩࡨ࠻ࠢࡰࡳࡸࡺࠠࡳࡧࡦࡩࡳࡺࠠࡴࡶࡤࡸࡺࡹࠠࡦ࡯࡬ࡸࡹ࡫ࡤࠡࠪࠪࡴࡦࡹࡳࡦࡦࠪࠤ࠴ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠨࡨࡤ࡭ࡱ࡫ࡤࠨࠢ࠲ࠤࡓࡵ࡮ࡦࠫ࠱ࠤࡗ࡫ࡡࡥࠢࡲࡲࡱࡿࠠࡣࡻࠣࡸ࡭࡫ࠠࡱࡣࡶࡷࡪࡪ࠭࡭ࡣࡶࡸ࠲ࡹࡴࡦࡲࠣࡦࡷࡧ࡮ࡤࡪࠣࡸࡴࠦࡡࡷࡱ࡬ࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡯ࡷࡧࡵࡻࡷ࡯ࡴࡪࡰࡪࠤࡦࡴࠠࡦࡣࡵࡰ࡮࡫ࡲࠡࠩࡩࡥ࡮ࡲࡥࡥࠩ࠱ࠤࡥࡦࡥ࡯ࡦࡢࡸࡪࡹࡴࡡࡢࠣ࡭ࡸࠦࡡࡶࡶ࡫ࡳࡷ࡯ࡴࡢࡶ࡬ࡺࡪࠦࡡ࡯ࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡮࡭࡮ࡰࡴࡨࡷࠥࡺࡨࡪࡵࠣࡰࡦࡺࡣࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢࣞ")
        setattr(self._thread_local, bstack1l1llll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࡣࡲࡧࡲ࡬ࡧࡧࠫࣟ"), value)
    def _11l11ll1_opy_(self):
        bstack1l1llll_opy_ (u"ࠦࠧࠨࡔࡩࡴࡨࡥࡩ࠳ࡳࡢࡨࡨࠤ࡬࡫ࡴࡵࡧࡵࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡩࡵࡳࡴࡨࡲࡹࠦࡳࡤࡧࡱࡥࡷ࡯࡯ࠨࡵࠣࡰࡦࡹࡴࠡࡵࡷࡩࡵࠦ࡬ࡪࡰࡨ࠲ࠧࠨࠢ࣠")
        return getattr(self._thread_local, bstack1l1llll_opy_ (u"ࠬࡲࡡࡴࡶࡢࡷࡹ࡫ࡰࡠ࡮࡬ࡲࡪ࠭࣡"), None)
    def _1ll11l11_opy_(self, value):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡕࡨࡸࠥ࡯࡮ࠡࡢࡣࡷࡹࡧࡲࡵࡡࡷࡩࡸࡺࡠࡡࠢࡩࡶࡴࡳࠠࡡࡢࡶࡧࡪࡴࡡࡳ࡫ࡲ࠲ࡸࡺࡥࡱࡵ࡞࠱࠶ࡣ࠮࡭࡫ࡱࡩࡥࡦ࠮ࠡࡔࡨࡥࡩࠦࡢࡺࠌࠣࠤࠥࠦࠠࠡࠢࠣࡤࡥ࡫࡮ࡥࡡࡶࡸࡪࡶࡠࡡࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࡴࡴࡣࡦࠢࡲࡲࠥࡺࡨࡦࠢ࡯ࡥࡸࡺࠠࡴࡶࡨࡴࠥ࡯࡮ࡴࡶࡨࡥࡩࠦ࡯ࡧࠌࠣࠤࠥࠦࠠࠡࠢࠣࡴࡪࡸࠠࡴࡶࡨࡴ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ࣢")
        setattr(self._thread_local, bstack1l1llll_opy_ (u"ࠧ࡭ࡣࡶࡸࡤࡹࡴࡦࡲࡢࡰ࡮ࡴࡥࠨࣣ"), value)
    def _1l1l1lll_opy_(self) -> TestFrameworkContext:
        bstack1l1llll_opy_ (u"ࠣࠤࠥࡆࡺ࡯࡬ࡥࠢࡤࠤ࡙࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡇࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡄࡨ࡬ࡦࡼࡥࠡࡄ࡬ࡲࡦࡸࡹࠡࡈ࡯ࡳࡼࠦࡣࡢ࡮࡯ࡷ࠳ࠨࠢࠣࣤ")
        platform_index = -1
        try:
            platform_index = int(threading.current_thread().name)
        except (ValueError, AttributeError):
            try:
                if cli.automation_framework:
                    platform_index = cli.automation_framework.platform_index
            except Exception:
                pass
            if platform_index < 0:
                platform_index = int(os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩࣥ"), bstack1l1llll_opy_ (u"ࠪ࠴ࣦࠬ")))
        return TestFrameworkContext(
            test_framework_name=bstack1l1llll_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫࣧ"),
            test_framework_version=_111l1lll_opy_,
            platform_index=platform_index,
        )
    def _1ll1111l_opy_(self) -> bool:
        return bool(
            cli.is_running()
            and getattr(cli, bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ࣨ"), None) is not None
            and cli.test_framework.is_behave_framework()
        )
    @staticmethod
    def log_handler(log):
        if not (log[bstack1l1llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࣩࠧ")] and log[bstack1l1llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࣪")].strip()):
            return
        active = bstack1ll111ll_opy_.bstack11llll1l_opy_()
        log = {
            bstack1l1llll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ࣫"): log[bstack1l1llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ࣬")],
            bstack1l1llll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࣭࠭"): bstack1l1111ll_opy_(),
            bstack1l1llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩ࣮ࠬ"): log[bstack1l1llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࣯࠭")],
        }
        if active:
            if active[bstack1l1llll_opy_ (u"࠭ࡴࡺࡲࡨࣰࠫ")] == bstack1l1llll_opy_ (u"ࠧࡩࡱࡲ࡯ࣱࠬ"):
                log[bstack1l1llll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨࣲ")] = active[bstack1l1llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩࣳ")]
            elif active[bstack1l1llll_opy_ (u"ࠪࡸࡾࡶࡥࠨࣴ")] == bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩࣵ"):
                log[bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࣶࠬ")] = active[bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ࣷ")]
        TestHubHandler.bstack1ll11111_opy_([log])
    def _111l1l1l_opy_(self):
        try:
            page = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡐࡢࡩࡨࠫࣸ"), None)
            if page and hasattr(page, bstack1l1llll_opy_ (u"ࠨࡧࡹࡥࡱࡻࡡࡵࡧࣹࠪ")):
                return True
            return False
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠤࡢ࡬ࡦࡹ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡱࡣࡪࡩࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡥࡾࠤࣺ").format(e=e))
            return False
    def _1l11llll_opy_(self, action, arguments):
        try:
            page = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡓࡥ࡬࡫ࠧࣻ"), None)
            if not page:
                logger.debug(bstack1l1llll_opy_ (u"ࠦࡤ࡫ࡸࡦࡥࡸࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡰࡲࠤࡦࡩࡴࡪࡸࡨࠤࡵࡧࡧࡦ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࢁࡡࡤࡶ࡬ࡳࡳࢃࠢࣼ").format(action=action))
                return None
            bstack1l11l111_opy_ = {
                bstack1l1llll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬࣽ"): action,
                bstack1l1llll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩࣾ"): arguments
            }
            executor_cmd = bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠪࣿ") + json.dumps(bstack1l11l111_opy_)
            result = page.evaluate(bstack1l1llll_opy_ (u"ࠣࡣࡵ࡫ࠥࡃ࠾ࠡࡽࢀࠦऀ"), executor_cmd)
            logger.debug(bstack1l1llll_opy_ (u"ࠤࡢࡩࡽ࡫ࡣࡶࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡢࡥࡷ࡭ࡴࡴࡽࠡࡧࡻࡩࡨࡻࡴࡦࡦ࠯ࠤࡷ࡫ࡳࡶ࡮ࡷࡁࢀࡸࡥࡴࡷ࡯ࡸࢂࠨँ").format(
                action=action, result=result))
            return result
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡣࡪࡾࡥࡤࡷࡷࡩࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࢀࡧࡣࡵ࡫ࡲࡲࢂࡀࠠࡼࡧࢀࠦं").format(
                action=action, e=e))
            return None
    def _call_driver_init(self):
        bstack1l1llll_opy_ (u"ࠦࠧࠨࡍࡢ࡭ࡨࠤࡹ࡮ࡥࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠥ࡭ࡒࡑࡅࠣࡧࡦࡲ࡬ࠡࡶࡲࠤࡷ࡫ࡧࡪࡵࡷࡩࡷࠦࡴࡩ࡫ࡶࠤࡧ࡫ࡨࡢࡸࡨ࠱ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡵࡪࡨࠤࡧ࡯࡮ࡢࡴࡼ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡘࡑ࠰ࡗ࡙ࡋࡐࠡࡆࡈࡗࡎࡍࡎࠡࠪࡸࡲ࡮࡬ࡩࡦࡦࠣࡅ࠶࠷ࡹࠡ࠭ࠣࡓ࠶࠷ࡹࠡࡨ࡬ࡼ࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡷࡩࡵࠦ࠱࠻ࠢࡄࡐ࡜ࡇ࡙ࡔࠢࡦࡶࡪࡧࡴࡦࠢࡷ࡬ࡪࠦࡳࡺࡰࡷ࡬ࡪࡺࡩࡤࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡃࡴࡲࡻࡸ࡫ࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩ࡫ࡶࠤ࡮ࡹࠠࡵࡪࡨࠤࠧࡨࡵࡤ࡭ࡨࡸࠧࠦࡴࡩࡣࡷࠤࡔ࠷࠱ࡺࠢࡸࡷࡪࡹࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠴ࠠࡘ࡫ࡷ࡬ࡴࡻࡴࠡ࡫ࡷ࠰ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡨࡧࡷࡣࡨࡨࡴࡠࡧࡹࡩࡳࡺࠠࡩࡣࡶࠤࡳࡵࡴࡩ࡫ࡱ࡫ࠥࡺ࡯ࠡࡴࡨࡥࡩࠦ⦒ࠡࡑ࠴࠵ࡾࠦࡦࡢ࡮࡯ࡷࠥࡨࡡࡤ࡭ࠣࡸࡴࠦࡷࡳࡱࡱ࡫ࠥࡪࡡࡵࡣ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡴࡦࡲࠣ࠶࠿ࠦࡃࡩࡧࡦ࡯ࠥ࡯ࡦࠡࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡲࡡࡶࡰࡦ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡤࡪࡦࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࠩࡃ࠴࠵ࡾࠦࡦ࡭ࡱࡺ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡋࡩࠤࡾ࡫ࡳ࠭ࠢࡶ࡯࡮ࡶࠠࡵࡪࡨࠤ࡬ࡘࡐࡄࠢࡦࡥࡱࡲࠠࠩࡲࡵࡩࡻ࡫࡮ࡵࡵࠣࡨࡺࡶ࡬ࡪࡥࡤࡸࡪࠦ࡯ࡳࡲ࡫ࡥࡳ࡫ࡤࠡࡵࡨࡷࡸ࡯࡯࡯ࠫ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡧࠣࡦࡺࡩ࡫ࡦࡶࠣࡪࡷࡵ࡭ࠡࡕࡷࡩࡵࠦ࠱ࠡࡵࡷ࡭ࡱࡲࠠࡦࡺ࡬ࡷࡹࡹࠠࡧࡱࡵࠤࡔ࠷࠱ࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢः")
        try:
            from browserstack_sdk.sdk_cli.automation_framework import bstack1l111l1l_opy_, AutomationFrameworkBrowser, AutomationFrameworkState
            from browserstack_sdk.sdk_cli.bstack1l1ll1l1_opy_ import bstack111ll111_opy_
            from browserstack_sdk import sdk_pb2 as structs
            from browserstack_sdk.sdk_cli.tracked_instance import TrackedInstance
            if not cli.cli_service or not cli.cli_bin_session_id:
                logger.debug(bstack1l1llll_opy_ (u"ࠧࡥࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࡧࡱ࡯ࠠ࡯ࡱࡷࠤࡷ࡫ࡡࡥࡻ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠨऄ"))
                return None
            bstack11l11l11_opy_ = threading.get_ident()
            bstack1l1llll1_opy_ = str(os.getpid()) + str(bstack11l11l11_opy_)
            bstack11ll1ll1_opy_ = hash(bstack1l1llll1_opy_)
            if bstack11ll1ll1_opy_ not in bstack1l111l1l_opy_.instances:
                bstack1l1lll11_opy_ = getattr(getattr(cli, bstack1l1llll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭अ"), None), bstack1l1llll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫआ"), bstack1l1llll_opy_ (u"ࠨ࠳࠱࠴ࠬइ"))
                ctx = TrackedInstance.create_context(bstack1l1llll1_opy_)
                bstack111l1l11_opy_ = AutomationFrameworkBrowser(ctx, bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ई"), bstack1l1lll11_opy_, AutomationFrameworkState.CREATE)
                bstack1l111l1l_opy_.instances[ctx.id] = bstack111l1l11_opy_
                logger.debug(bstack1l1llll_opy_ (u"ࠥࡣࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࡅࡵࡩࡦࡺࡥࡥࠢࡶࡽࡳࡺࡨࡦࡶ࡬ࡧࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡳࡧࡩࡁࢀࢃࠠࡧࡱࡵࠤࡹ࡮ࡲࡦࡣࡧࡁࢀࢃࠢउ").format(
                    bstack111l1l11_opy_.ref(), bstack11l11l11_opy_))
            bstack11l1lll1_opy_ = bstack1l111l1l_opy_.instances.get(bstack11ll1ll1_opy_, None)
            bstack11lll11l_opy_ = bstack11l1lll1_opy_.ref() if bstack11l1lll1_opy_ else str(bstack11ll1ll1_opy_)
            if getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶࡢࡨࡴࡴࡥࠨऊ"), False):
                logger.debug(bstack1l1llll_opy_ (u"ࠧࡥࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥ࡭ࡒࡑࡅ࠯ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡧࡳࡳ࡫ࠠࡣࡻࠣࡳࡳࡥࡢࡳࡱࡺࡷࡪࡸ࡟࡭ࡣࡸࡲࡨ࡮ࠠࠩࡤࡸࡧࡰ࡫ࡴࠡࡧࡻ࡭ࡸࡺࡳࠪࠤऋ"))
                return None
            test_instance = None
            bstack1l1l1l1l_opy_ = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡢࡦࡪࡤࡺࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࡠࡶࡤࡶ࡬࡫ࡴࠨऌ"), None)
            if bstack1l1l1l1l_opy_:
                test_instance = cli.test_framework.get_tracked_instance(bstack1l1l1l1l_opy_, strict=False)
            hub_url = os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡆࡊࡄ࡚ࡊࡥࡐࡘࡡࡆࡈࡕࡥࡕࡓࡎࠪऍ"), bstack1l1llll_opy_ (u"ࠨࠩऎ"))
            platform_index = self._1l1l1lll_opy_().platform_index
            if platform_index < 0:
                platform_index = 0
            req = structs.DriverInitRequest()
            req.bin_session_id = cli.cli_bin_session_id
            req.platform_index = platform_index
            req.ref = bstack11lll11l_opy_
            req.user_input_params = json.dumps({bstack1l1llll_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨए"): True}).encode(bstack1l1llll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤऐ"))
            if hub_url:
                req.hub_url = hub_url
            req.client_worker_id = bstack1l1llll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥऑ").format(threading.get_ident(), os.getpid())
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡥࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡴࡨࡪࡂࢁࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࢁࠧऒ").format(
                bstack11lll11l_opy_, req.platform_index))
            response = cli.cli_service.DriverInit(req)
            if response and response.success:
                logger.debug(bstack1l1llll_opy_ (u"ࠨ࡟ࡤࡣ࡯ࡰࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡵࡸࡧࡨ࡫ࡥࡥࡧࡧࠦओ"))
                if response.capabilities:
                    try:
                        bstack11l1ll11_opy_ = json.loads(response.capabilities.decode(bstack1l1llll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨऔ")))
                        if bstack11l1ll11_opy_:
                            if test_instance:
                                bstack111ll111_opy_.set_state(test_instance, bstack111ll111_opy_.bstack1l111lll_opy_, bstack11l1ll11_opy_)
                            if bstack11l1lll1_opy_:
                                bstack111ll111_opy_.set_state(bstack11l1lll1_opy_, bstack111ll111_opy_.bstack1l111lll_opy_, bstack11l1ll11_opy_)
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        logger.debug(bstack1l1llll_opy_ (u"ࠣࡡࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠺ࠡࡽࡨࢁࠧक").format(e=e))
                return response
            else:
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡢࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤࡷ࡫ࡴࡶࡴࡱࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࡇࡣ࡯ࡷࡪࠨख"))
                return None
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡣࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࡩࢂࠨग").format(e=e))
            return None
    def _populate_browser_instance_data(self):
        bstack1l1llll_opy_ (u"ࠦࠧࠨࡐࡰࡲࡸࡰࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠥࡧ࡮ࡥࠢ࡫ࡹࡧࡥࡵࡳ࡮ࠣࡳࡳࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠡࡨࡲࡶࠥࡨࡥࡩࡣࡹࡩ࠲ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡒ࡛ࡌࡕࡋ࠰ࡔࡑࡇࡔࡇࡑࡕࡑࠥࡌࡉ࡙࠼ࠣࡓࡳࡲࡹࠡࡷࡳࡨࡦࡺࡥࠡࡶ࡫ࡩࠥࡉࡕࡓࡔࡈࡒ࡙ࠦࡴࡩࡴࡨࡥࡩ࠭ࡳࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠤࡎࡴࠠࡑࡒࡓࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡫ࡡࡤࡪࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡺࡨࡳࡧࡤࡨࠥ࠮ࡃࡩࡴࡲࡱࡪ࠲ࠠࡆࡦࡪࡩ࠱ࠦࡥࡵࡥ࠱࠭ࠥ࡮ࡡࡴࠢ࡬ࡸࡸࠦ࡯ࡸࡰࠣࡷࡾࡴࡴࡩࡧࡷ࡭ࡨࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡮ࡩࡾ࡫ࡤࠡࡤࡼࠤ࡭ࡧࡳࡩࠪࡳ࡭ࡩࡥࡴࡪࡦࠬ࠲ࠥࡕ࡬ࡥࠢࡦࡳࡩ࡫ࠠࡪࡶࡨࡶࡦࡺࡥࡥࠢࡄࡐࡑࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠢࡤࡲࡩࠦࡷࡳࡱࡷࡩࠥࡺࡨࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡺࡸࡲࡦࡰࡷࠤࡹ࡮ࡲࡦࡣࡧࠫࡸࠦࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡸࡴࠦࡥࡷࡧࡵࡽࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠ⠕ࠢࡦࡥࡺࡹࡩ࡯ࡩࠣࡧࡷࡵࡳࡴ࠯ࡦࡳࡳࡺࡡ࡮࡫ࡱࡥࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠬࡪ࠴ࡧ࠯ࠢࡈࡨ࡬࡫ࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡ࡫ࡷࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡲࡲࡹࡵࠠࡄࡪࡵࡳࡲ࡫ࠧࡴࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ⦗ࠦࡏ࠲࠳ࡼࠤࡸ࡮࡯ࡸࡵࠣࡦࡴࡺࡨࠋࠢࠣࠤࠥࠦࠠࠡࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡦࡹࠠࡆࡦࡪࡩ࠮࠴ࠠࡇ࡫ࡻ࠾ࠥࡳࡩࡳࡴࡲࡶࠥࡥࡣࡢࡲࡷࡹࡷ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡣࡪࡧࡲ࡭ࡻࠫ࠭ࠥࡧ࡮ࡥࠢࡦࡶࡪࡧࡴࡦ࠱ࡸࡴࡩࡧࡴࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࡳࡳࡲࡹࠡࡶ࡫࡭ࡸࠦࡴࡩࡴࡨࡥࡩ࠭ࡳࠡࡵࡼࡲࡹ࡮ࡥࡵ࡫ࡦࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦघ")
        try:
            from browserstack_sdk.sdk_cli.automation_framework import bstack1l111l1l_opy_, AutomationFrameworkBrowser, AutomationFrameworkState
            from browserstack_sdk.sdk_cli.bstack1l1ll1l1_opy_ import bstack111ll111_opy_
            from browserstack_sdk.sdk_cli.tracked_instance import TrackedInstance
            if not self._111l1l1l_opy_():
                logger.debug(bstack1l1llll_opy_ (u"ࠧࡥࡰࡰࡲࡸࡰࡦࡺࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡣࡩࡧࡴࡢ࠼ࠣࡲࡴࠦࡡࡤࡶ࡬ࡺࡪࠦࡰࡢࡩࡨ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠢङ"))
                return
            if not self._111l1ll1_opy_():
                response = self._call_driver_init()
                self._11ll1lll_opy_(True)
                if response and response.success:
                    logger.debug(bstack1l1llll_opy_ (u"ࠨ࡟ࡱࡱࡳࡹࡱࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡪࡡࡵࡣ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠥच"))
            result = self._1l11llll_opy_(bstack1l1llll_opy_ (u"ࠧࡨࡧࡷࡗࡪࡹࡳࡪࡱࡱࡈࡪࡺࡡࡪ࡮ࡶࠫछ"), {})
            logger.debug(bstack1l1llll_opy_ (u"ࠣࡡࡳࡳࡵࡻ࡬ࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡥࡣࡷࡥ࠿ࠦࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠣࡶࡪࡹࡵ࡭ࡶࡀࡿࡷࢃࠢज").format(r=result))
            if not result:
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡢࡴࡴࡶࡵ࡭ࡣࡷࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡦࡤࡸࡦࡀࠠ࡯ࡱࠣࡶࡪࡹࡵ࡭ࡶࠣࡪࡷࡵ࡭ࠡࡩࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡉ࡫ࡴࡢ࡫࡯ࡷࠧझ"))
                return
            bstack111ll1ll_opy_ = json.loads(result) if isinstance(result, str) else result
            session_id = bstack111ll1ll_opy_.get(bstack1l1llll_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ञ"), bstack1l1llll_opy_ (u"ࠫࠬट"))
            hub_url = os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡋࡈࡂࡘࡈࡣࡕ࡝࡟ࡄࡆࡓࡣ࡚ࡘࡌࠨठ"), bstack1l1llll_opy_ (u"࠭ࠧड"))
            logger.debug(bstack1l1llll_opy_ (u"ࠢࡠࡲࡲࡴࡺࡲࡡࡵࡧࡢࡦࡷࡵࡷࡴࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡥࡤࡢࡶࡤ࠾ࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࡾࡷ࡮ࡪࡽ࠭ࠢ࡫ࡹࡧࡥࡵࡳ࡮ࡀࡿࡺࡸ࡬ࡾࠤढ").format(
                sid=session_id, url=hub_url[:80] if hub_url else bstack1l1llll_opy_ (u"ࠨࠩण")))
            self._1l11l11l_opy_(session_id)
            bstack11l11l11_opy_ = threading.get_ident()
            bstack1l1llll1_opy_ = str(os.getpid()) + str(bstack11l11l11_opy_)
            bstack11ll1ll1_opy_ = hash(bstack1l1llll1_opy_)
            if bstack11ll1ll1_opy_ not in bstack1l111l1l_opy_.instances:
                bstack1l1lll11_opy_ = getattr(getattr(cli, bstack1l1llll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩत"), None), bstack1l1llll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧथ"), bstack1l1llll_opy_ (u"ࠫ࠶࠴࠰ࠨद"))
                ctx = TrackedInstance.create_context(bstack1l1llll1_opy_)
                bstack111l1l11_opy_ = AutomationFrameworkBrowser(ctx, bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩध"), bstack1l1lll11_opy_, AutomationFrameworkState.CREATE)
                bstack1l111l1l_opy_.instances[ctx.id] = bstack111l1l11_opy_
                logger.debug(bstack1l1llll_opy_ (u"ࠨ࡟ࡱࡱࡳࡹࡱࡧࡴࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡪࡡࡵࡣ࠽ࠤࡈࡸࡥࡢࡶࡨࡨࠥࡹࡹ࡯ࡶ࡫ࡩࡹ࡯ࡣࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡪࡴࡸࠠࡵࡪࡵࡩࡦࡪ࠽ࡼࡿࠥन").format(bstack11l11l11_opy_))
            if bstack11ll1ll1_opy_ in bstack1l111l1l_opy_.instances:
                instance = bstack1l111l1l_opy_.instances[bstack11ll1ll1_opy_]
                bstack111ll111_opy_.set_state(instance, bstack111ll111_opy_.bstack111lllll_opy_, session_id)
                if hub_url:
                    bstack111ll111_opy_.set_state(instance, bstack111ll111_opy_.bstack11lll111_opy_, hub_url)
                if not bstack111ll111_opy_.get_state(instance, bstack111ll111_opy_.bstack1l111lll_opy_, None):
                    for other in bstack1l111l1l_opy_.instances.values():
                        caps = bstack111ll111_opy_.get_state(other, bstack111ll111_opy_.bstack1l111lll_opy_, None)
                        if caps and other is not instance:
                            bstack1l1ll111_opy_ = getattr(other.context, bstack1l1llll_opy_ (u"ࠧࡵࡪࡵࡩࡦࡪ࡟ࡪࡦࠪऩ"), None)
                            if str(bstack1l1ll111_opy_) == str(bstack11l11l11_opy_):
                                bstack111ll111_opy_.set_state(instance, bstack111ll111_opy_.bstack1l111lll_opy_, caps)
                                break
                logger.debug(bstack1l1llll_opy_ (u"ࠣࡡࡳࡳࡵࡻ࡬ࡢࡶࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫࡟ࡥࡣࡷࡥ࠿ࠦࡕࡱࡦࡤࡸࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡩࡳࡷࠦࡴࡩࡴࡨࡥࡩࡃࡻࡾ࠮ࠣࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࡼࡿࠥप").format(
                    bstack11l11l11_opy_, session_id))
            else:
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡢࡴࡴࡶࡵ࡭ࡣࡷࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡦࡤࡸࡦࡀࠠࡏࡱࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡶࡪࡧࡤ࠾ࡽࢀࠦफ").format(bstack11l11l11_opy_))
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡣࡵࡵࡰࡶ࡮ࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡧࡥࡹࡧࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࡨࢁࠧब").format(e=e))
    def _1l11l1l1_opy_(self, status):
        bstack1l1llll_opy_ (u"ࠦࠧࠨࡍࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࡵ࡮ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱ࠮ࠡࡔࡨࡷࡵ࡫ࡣࡵࡵࠣࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠠࡤࡱࡱࡪ࡮࡭࠮ࠣࠤࠥभ")
        try:
            if Config.bstack1lll1l11_opy_().bstack11l11l1l_opy_():
                return
            bstack1l111ll1_opy_ = bstack1l1llll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧम") if status.status.name.lower() == bstack1l1llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭य") else bstack1l1llll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢर")
            self._1l11llll_opy_(bstack1l1llll_opy_ (u"ࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦऱ"), {
                bstack1l1llll_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤल"): bstack1l111ll1_opy_,
                bstack1l1llll_opy_ (u"ࠥࡶࡪࡧࡳࡰࡰࠥळ"): bstack1l1llll_opy_ (u"ࠦࠧऴ")
            })
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡥ࡭ࡢࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡹࡴࡢࡶࡸࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡦࡿࠥव").format(e=e))
    def _1l11l1ll_opy_(self):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡅࡤࡴࡹࡻࡲࡦࠢࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠦࡅࡂࡔࡏ࡝ࠥ࠮ࡢࡦࡨࡲࡶࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡤ࡮ࡲࡷࡪࡹࠩࠡࡨࡲࡶࠥࡲࡡࡵࡧࡵࠤࡺࡹࡥࠡ࡫ࡱࠤࡪࡴࡤࡠࡶࡨࡷࡹ࠮ࠩ࠯ࠤࠥࠦश")
        if self._11l1ll1l_opy_():
            return
        try:
            from browserstack_sdk.sdk_cli.automation_framework import bstack1l111l1l_opy_, AutomationFrameworkBrowser, AutomationFrameworkState
            from browserstack_sdk.sdk_cli.bstack1l1ll1l1_opy_ import bstack111ll111_opy_
            from browserstack_sdk.sdk_cli.tracked_instance import TrackedInstance
            if not self._111l1l1l_opy_():
                return
            bstack11l11l11_opy_ = threading.get_ident()
            bstack1l1llll1_opy_ = str(os.getpid()) + str(bstack11l11l11_opy_)
            bstack11ll1ll1_opy_ = hash(bstack1l1llll1_opy_)
            if bstack11ll1ll1_opy_ not in bstack1l111l1l_opy_.instances:
                bstack1l1lll11_opy_ = getattr(getattr(cli, bstack1l1llll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧष"), None), bstack1l1llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬस"), bstack1l1llll_opy_ (u"ࠩ࠴࠲࠵࠭ह"))
                ctx = TrackedInstance.create_context(bstack1l1llll1_opy_)
                bstack111l1l11_opy_ = AutomationFrameworkBrowser(ctx, bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧऺ"), bstack1l1lll11_opy_, AutomationFrameworkState.CREATE)
                bstack1l111l1l_opy_.instances[ctx.id] = bstack111l1l11_opy_
                logger.debug(bstack1l1llll_opy_ (u"ࠦࡤࡩࡡࡱࡶࡸࡶࡪࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࡢࡩࡦࡸ࡬ࡺ࠼ࠣࡇࡷ࡫ࡡࡵࡧࡧࠤࡸࡿ࡮ࡵࡪࡨࡸ࡮ࡩࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡩࡳࡷࠦࡴࡩࡴࡨࡥࡩࡃࡻࡾࠤऻ").format(bstack11l11l11_opy_))
            if not self._111l1ll1_opy_():
                response = self._call_driver_init()
                self._11ll1lll_opy_(True)
                if response and response.success:
                    logger.debug(bstack1l1llll_opy_ (u"ࠧࡥࡣࡢࡲࡷࡹࡷ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡣࡪࡧࡲ࡭ࡻ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧ़ࠦ"))
            result = self._1l11llll_opy_(bstack1l1llll_opy_ (u"࠭ࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠪऽ"), {})
            if result:
                try:
                    bstack111ll1ll_opy_ = json.loads(result) if isinstance(result, str) else result
                    self._1l11l11l_opy_(bstack111ll1ll_opy_.get(bstack1l1llll_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪा"), bstack1l1llll_opy_ (u"ࠨࠩि")))
                    logger.debug(bstack1l1llll_opy_ (u"ࠤࡢࡧࡦࡶࡴࡶࡴࡨࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࡠࡧࡤࡶࡱࡿ࠺ࠡࡅࡤࡴࡹࡻࡲࡦࡦࠣࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪ࠽ࡼࡵ࡬ࡨࢂࠨी").format(
                        sid=self._11l1ll1l_opy_()))
                    hub_url = os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡉࡍࡇࡖࡆࡡࡓ࡛ࡤࡉࡄࡑࡡࡘࡖࡑ࠭ु"), bstack1l1llll_opy_ (u"ࠫࠬू"))
                    updated = 0
                    if bstack11ll1ll1_opy_ in bstack1l111l1l_opy_.instances:
                        instance = bstack1l111l1l_opy_.instances[bstack11ll1ll1_opy_]
                        bstack111ll111_opy_.set_state(instance, bstack111ll111_opy_.bstack111lllll_opy_, self._11l1ll1l_opy_())
                        if hub_url:
                            bstack111ll111_opy_.set_state(instance, bstack111ll111_opy_.bstack11lll111_opy_, hub_url)
                        updated += 1
                    logger.debug(bstack1l1llll_opy_ (u"ࠧࡥࡣࡢࡲࡷࡹࡷ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࡣࡪࡧࡲ࡭ࡻ࠽ࠤ࡚ࡶࡤࡢࡶࡨࡨࠥࢁࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠫࡷ࠮ࠦࡷࡪࡶ࡫ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡨࡲࡶࠥࡺࡨࡳࡧࡤࡨࡂࢁࡽࠣृ").format(
                        updated, bstack11l11l11_opy_))
                except Exception as e:
                    logger.debug(bstack1l1llll_opy_ (u"ࠨ࡟ࡤࡣࡳࡸࡺࡸࡥࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡤ࡫ࡡࡳ࡮ࡼ࠾ࠥࡶࡡࡳࡵࡨࠤࡪࡸࡲࡰࡴ࠽ࠤࢀ࡫ࡽࠣॄ").format(e=e))
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠢࡠࡥࡤࡴࡹࡻࡲࡦࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡥࡥࡢࡴ࡯ࡽࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡦࡿࠥॅ").format(e=e))
    def start_test(self, attrs):
        test_uuid = getattr(attrs, bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫॆ"), None) or str(uuid4())
        if self._1ll1111l_opy_():
            try:
                ctx = self._1l1l1lll_opy_()
                sc = attrs.scenario
                scenario_target = bstack1l1llll_opy_ (u"ࠤࡾࢁ࠿ࡀࡻࡾ࠼࠽ࡿࢂࠨे").format(
                    sc.feature.filename if (hasattr(sc, bstack1l1llll_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫै")) and sc.feature) else bstack1l1llll_opy_ (u"ࠫࠬॉ"),
                    sc.name,
                    str(sc.line),
                )
                if ctx.platform_index >= 0:
                    scenario_target = bstack1l1llll_opy_ (u"ࠧࢁࡽ࠻࠼࡞ࡴࡱࡧࡴࡧࡱࡵࡱࡤࢁࡽ࡞ࠤॊ").format(scenario_target, ctx.platform_index)
                threading.current_thread().bstack_behave_scenario_target = scenario_target
                try:
                    steps = getattr(sc, bstack1l1llll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬो"), None) or []
                    self._1ll11l11_opy_(steps[-1].line if steps else None)
                except Exception:
                    self._1ll11l11_opy_(None)
                cli.test_framework.track_event(ctx, TestFrameworkState.INIT_TEST, TestHookState.PRE, attrs)
                cli.test_framework.track_event(ctx, TestFrameworkState.TEST, TestHookState.PRE, attrs)
            except Exception as e:
                logger.debug(bstack1l1llll_opy_ (u"ࠢࡃ࡫ࡱࡥࡷࡿࡆ࡭ࡱࡺࠤࡸࡺࡡࡳࡶࡢࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸ࠺ࠡࠧࡶࠦौ"), e)
            return
        self.tests[test_uuid] = {}
        self.bstack11l1l111_opy_.start()
        driver = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸ्ࠧ"), None)
        bstack11ll1111_opy_ = self._11ll1l11_opy_(attrs.scenario)
        test_data = bstack1l1l1111_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1l1111ll_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1l1llll_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥॎ"),
            framework=bstack1l1llll_opy_ (u"ࠪࡆࡪ࡮ࡡࡷࡧࠪॏ"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack1l11111l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags,
            code=bstack11ll1111_opy_
        )
        self.tests[test_uuid][bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧॐ")] = test_data
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.bstack11lll1ll_opy_(bstack1l1llll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭॑"), test_data)
    def end_test(self, attrs, runner=None):
        if self._1ll1111l_opy_():
            try:
                ctx = self._1l1l1lll_opy_()
                if self._111l1l1l_opy_():
                    try:
                        if not self._11l111l1_opy_():
                            self._populate_browser_instance_data()
                        self._1l11l1l1_opy_(attrs)
                    except Exception as e:
                        logger.debug(bstack1l1llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡪࡴࡤࡠࡶࡨࡷࡹࡀࠠࠦࡵ॒ࠥ"), e)
                self._11ll1lll_opy_(False)
                self._1l11l11l_opy_(None)
                self._1l1lll1l_opy_(False)
                self._111lll11_opy_(None)
                self._1ll11l11_opy_(None)
                cli.test_framework.track_event(ctx, TestFrameworkState.TEST, TestHookState.POST, attrs)
                _1l111l11_opy_ = threading.current_thread()
                for attr in (bstack1l1llll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭॓"), bstack1l1llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧ॔"), bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨॕ"),
                             bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡓࡥ࡬࡫ࠧॖ"), bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡆࡴࡵࡳࡷࡓࡥࡴࡵࡤ࡫ࡪࡹࠧॗ"),
                             bstack1l1llll_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡦࡼࡥࡠࡴࡨࡷࡺࡲࡴࡠࡦࡲࡲࡪ࠭क़"), bstack1l1llll_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨख़"), bstack1l1llll_opy_ (u"ࠧࡢ࠳࠴ࡽࡤࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩग़"),
                             bstack1l1llll_opy_ (u"ࠨࡣ࠴࠵ࡾࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ज़"), bstack1l1llll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡦࡲࡲࡪ࠭ड़")):
                    try:
                        delattr(_1l111l11_opy_, attr)
                    except AttributeError:
                        pass
                cli.test_framework.track_event(ctx, TestFrameworkState.LOG_REPORT, TestHookState.POST, attrs)
            except Exception as e:
                logger.debug(bstack1l1llll_opy_ (u"ࠥࡆ࡮ࡴࡡࡳࡻࡉࡰࡴࡽࠠࡦࡰࡧࡣࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲ࠻ࠢࠨࡷࠧढ़"), e)
            return
        bstack11l1111l_opy_ = {
            bstack1l1llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤफ़"): attrs.feature.name,
            bstack1l1llll_opy_ (u"ࠧࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥय़"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        test_data = self.tests[current_test_uuid][bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩॠ")]
        meta = {
            bstack1l1llll_opy_ (u"ࠢࡧࡧࡤࡸࡺࡸࡥࠣॡ"): bstack11l1111l_opy_,
            bstack1l1llll_opy_ (u"ࠣࡵࡷࡩࡵࡹࠢॢ"): test_data.meta.get(bstack1l1llll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨॣ"), []),
            bstack1l1llll_opy_ (u"ࠥࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ।"): {
                bstack1l1llll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ॥"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        test_data.bstack1l1ll1ll_opy_(meta)
        test_data.bstack11l1l1ll_opy_(bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ०"), []))
        status = bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭१") if attrs.status.name.lower() == bstack1l1llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭२") else attrs.status.name.lower()
        exception, bstack1l1l1ll1_opy_ = self._1l1l111l_opy_(attrs, runner, status)
        bstack111lll1l_opy_ = Result(result=status, exception=exception, bstack1l1l1ll1_opy_=bstack1l1l1ll1_opy_)
        self.tests[threading.current_thread().current_test_uuid][bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ३")].stop(time=bstack1l1111ll_opy_(), duration=int(attrs.duration)*1000, result=bstack111lll1l_opy_)
        TestHubHandler.bstack11lll1ll_opy_(bstack1l1llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ४"), self.tests[threading.current_thread().current_test_uuid][bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭५")])
    def start_step(self, attrs):
        if self._1ll1111l_opy_():
            try:
                ctx = self._1l1l1lll_opy_()
                scenario_target = getattr(
                    threading.current_thread(), bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡧ࡫ࡨࡢࡸࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡥࡴࡢࡴࡪࡩࡹ࠭६"), None
                )
                if scenario_target:
                    cli.test_framework.track_event(
                        ctx, TestFrameworkState.STEP, TestHookState.PRE, attrs,
                        scenario_target=scenario_target,
                    )
            except Exception as e:
                logger.debug(bstack1l1llll_opy_ (u"ࠧࡈࡩ࡯ࡣࡵࡽࡋࡲ࡯ࡸࠢࡶࡸࡦࡸࡴࡠࡵࡷࡩࡵࠦࡥࡳࡴࡲࡶ࠿ࠦࠥࡴࠤ७"), e)
            return
        bstack11ll111l_opy_ = {
            bstack1l1llll_opy_ (u"࠭ࡩࡥࠩ८"): uuid4().__str__(),
            bstack1l1llll_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ९"): attrs.keyword,
            bstack1l1llll_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨ॰"): [],
            bstack1l1llll_opy_ (u"ࠩࡷࡩࡽࡺࠧॱ"): attrs.name,
            bstack1l1llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧॲ"): bstack1l1111ll_opy_(),
            bstack1l1llll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫॳ"): bstack1l1llll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ॴ"),
            bstack1l1llll_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫॵ"): bstack1l1llll_opy_ (u"ࠧࠨॶ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫॷ")].add_step(bstack11ll111l_opy_)
        threading.current_thread().current_step_uuid = bstack11ll111l_opy_[bstack1l1llll_opy_ (u"ࠩ࡬ࡨࠬॸ")]
    def end_step(self, attrs):
        if self._1ll1111l_opy_():
            try:
                ctx = self._1l1l1lll_opy_()
                scenario_target = getattr(
                    threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡦࡪ࡮ࡡࡷࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡤࡺࡡࡳࡩࡨࡸࠬॹ"), None
                )
                if self._111l1l1l_opy_():
                    if not self._111l1ll1_opy_():
                        self._call_driver_init()
                        self._11ll1lll_opy_(True)
                        try:
                            self._populate_browser_instance_data()
                        except Exception as e:
                            logger.debug(bstack1l1llll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡱࡳࡹࡱࡧࡴࡦࠢࡶࡩࡸࡹࡩࡰࡰࠣࡨࡦࡺࡡࠡࡣࡩࡸࡪࡸࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷ࠾ࠥࠫࡳࠣॺ"), e)
                    _config = Config.bstack1lll1l11_opy_()
                    if not _config.bstack11lll1l1_opy_() and not self._11l111l1_opy_() and scenario_target:
                        try:
                            parts = scenario_target.split(bstack1l1llll_opy_ (u"ࠬࡀ࠺ࠨॻ"))
                            scenario_name = parts[1] if len(parts) >= 2 else None
                            if scenario_name:
                                self._1l11llll_opy_(bstack1l1llll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧॼ"), {bstack1l1llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬॽ"): scenario_name})
                                self._1l1lll1l_opy_(True)
                                logger.debug(bstack1l1llll_opy_ (u"ࠣࡧࡱࡨࡤࡹࡴࡦࡲ࠽ࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡵࡱࠣࠫࢀࡴࡽࠨࠤॾ").format(n=scenario_name))
                        except Exception as e:
                            logger.debug(bstack1l1llll_opy_ (u"ࠤࡨࡲࡩࡥࡳࡵࡧࡳ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࠫࡳࠣॿ"), e)
                    step_status = attrs.status.name.lower()
                    bstack11l1llll_opy_ = (
                        self._11l11ll1_opy_() is not None
                        and getattr(attrs, bstack1l1llll_opy_ (u"ࠪࡰ࡮ࡴࡥࠨঀ"), None) == self._11l11ll1_opy_()
                    )
                    bstack11l1l1l1_opy_ = bstack1l1llll_opy_ (u"ࠫࠬঁ")
                    bstack1l1l11l1_opy_ = bstack1l1llll_opy_ (u"ࠬ࠭ং")
                    if step_status in (bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ঃ"), bstack1l1llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭঄")):
                        try:
                            import traceback as _11ll11ll_opy_
                            exc = getattr(attrs, bstack1l1llll_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࠫঅ"), None)
                            exc_tb = getattr(attrs, bstack1l1llll_opy_ (u"ࠩࡨࡼࡨࡥࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࠩআ"), None)
                            if exc and exc_tb:
                                tb_lines = _11ll11ll_opy_.format_tb(exc_tb)
                                bstack1l1l11l1_opy_ = bstack1l1llll_opy_ (u"ࠪࠤࠬই").join(tb_lines)
                                bstack11l1l1l1_opy_ = exc.__class__.__name__ + (tb_lines[-1] if tb_lines else bstack1l1llll_opy_ (u"ࠫࠬঈ")) + str(exc)
                            else:
                                bstack11l1l1l1_opy_ = str(exc or bstack1l1llll_opy_ (u"ࠬ࠭উ"))
                        except Exception:
                            bstack11l1l1l1_opy_ = str(getattr(attrs, bstack1l1llll_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠩঊ"), bstack1l1llll_opy_ (u"ࠧࠨঋ")) or bstack1l1llll_opy_ (u"ࠨࠩঌ"))
                    if not _config.bstack11l11l1l_opy_():
                        try:
                            if step_status in (bstack1l1llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ঍"), bstack1l1llll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ঎")):
                                self._1l11llll_opy_(bstack1l1llll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧএ"), {bstack1l1llll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬঐ"): bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭঑"), bstack1l1llll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ঒"): bstack1l1llll_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧও") + bstack11l1l1l1_opy_ if bstack11l1l1l1_opy_ else bstack1l1llll_opy_ (u"ࠩࠪঔ")})
                                self._111lll11_opy_(bstack1l1llll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪক"))
                            elif step_status == bstack1l1llll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫখ") and bstack11l1llll_opy_ and self._111ll11l_opy_() != bstack1l1llll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬগ"):
                                self._1l11llll_opy_(bstack1l1llll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩঘ"), {bstack1l1llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧঙ"): bstack1l1llll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨচ"), bstack1l1llll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩছ"): bstack1l1llll_opy_ (u"ࠪࠫজ")})
                                self._111lll11_opy_(bstack1l1llll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫঝ"))
                        except Exception as e:
                            logger.debug(bstack1l1llll_opy_ (u"ࠧ࡫࡮ࡥࡡࡶࡸࡪࡶ࠺ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦঞ") + str(e))
                    try:
                        step_keyword = str(getattr(attrs, bstack1l1llll_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧট"), bstack1l1llll_opy_ (u"ࠧࠨঠ")) or bstack1l1llll_opy_ (u"ࠨࠩড")).strip()
                        step_name = str(getattr(attrs, bstack1l1llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧঢ"), bstack1l1llll_opy_ (u"ࠪࠫণ")) or bstack1l1llll_opy_ (u"ࠫࠬত"))
                        prefix = (step_keyword + bstack1l1llll_opy_ (u"ࠬࠦࠧথ") + step_name).strip() if step_keyword else step_name
                        if step_status in (bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭দ"), bstack1l1llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ধ")):
                            bstack1l11ll11_opy_ = prefix + bstack1l1llll_opy_ (u"ࠨࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࠬন") + (bstack1l1llll_opy_ (u"ࠩ࡟ࡲࠬ঩") + bstack1l1l11l1_opy_ if bstack1l1l11l1_opy_ else bstack1l1llll_opy_ (u"ࠪࠫপ"))
                            bstack11l1l11l_opy_ = bstack1l1llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪফ")
                        elif step_status == bstack1l1llll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬব"):
                            bstack1l11ll11_opy_ = prefix + bstack1l1llll_opy_ (u"࠭ࠠ࠮ࠢࡓࡥࡸࡹࡥࡥࠣࠪভ")
                            bstack11l1l11l_opy_ = bstack1l1llll_opy_ (u"ࠧࡪࡰࡩࡳࠬম")
                        else:
                            bstack1l11ll11_opy_ = prefix + bstack1l1llll_opy_ (u"ࠨࠢ࠰ࠤࠬয") + step_status.title() + bstack1l1llll_opy_ (u"ࠩࠤࠫর")
                            bstack11l1l11l_opy_ = bstack1l1llll_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨ঱")
                        self._1l11llll_opy_(bstack1l1llll_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ল"), {
                            bstack1l1llll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ঳"): bstack11l1l11l_opy_,
                            bstack1l1llll_opy_ (u"࠭ࡤࡢࡶࡤࠫ঴"): bstack1l11ll11_opy_,
                        })
                    except Exception as e:
                        logger.debug(bstack1l1llll_opy_ (u"ࠢࡦࡰࡧࡣࡸࡺࡥࡱ࠼ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡡ࡯ࡰࡲࡸࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࠦ঵") + str(e))
                else:
                    self._1l11l1ll_opy_()
                if scenario_target:
                    cli.test_framework.track_event(
                        ctx, TestFrameworkState.STEP, TestHookState.POST, attrs,
                        scenario_target=scenario_target,
                    )
            except Exception as e:
                logger.debug(bstack1l1llll_opy_ (u"ࠣࡄ࡬ࡲࡦࡸࡹࡇ࡮ࡲࡻࠥ࡫࡮ࡥࡡࡶࡸࡪࡶࠠࡦࡴࡵࡳࡷࡀࠠࠦࡵࠥশ"), e)
            return
        current_test_id = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ষ"), None)
        current_step_uuid = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡺࡥࡱࡡࡸࡹ࡮ࡪࠧস"), None)
        bstack11llllll_opy_, exception = self._1l1ll11l_opy_(attrs)
        status = bstack1l1llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫহ") if attrs.status.name.lower() == bstack1l1llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ঺") else attrs.status.name.lower()
        bstack111lll1l_opy_ = Result(result=status, exception=exception, bstack1l1l1ll1_opy_=[bstack11llllll_opy_])
        self.tests[current_test_id][bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ঻")].bstack1l111111_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111lll1l_opy_)
        threading.current_thread().current_step_uuid = None
    def start_hook(self, name, attrs):
        if self._1ll1111l_opy_():
            try:
                ctx = self._1l1l1lll_opy_()
                bstack1l1111l1_opy_ = {
                    bstack1l1llll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯়ࠫ"):      TestFrameworkState.BEFORE_ALL,
                    bstack1l1llll_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫঽ"):       TestFrameworkState.AFTER_ALL,
                    bstack1l1llll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫা"): TestFrameworkState.BEFORE_EACH,
                    bstack1l1llll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫি"):  TestFrameworkState.AFTER_EACH,
                    bstack1l1llll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬী"):  TestFrameworkState.BEFORE_ALL,
                    bstack1l1llll_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬু"):   TestFrameworkState.AFTER_ALL,
                }
                state = bstack1l1111l1_opy_.get(name)
                if state:
                    scenario_target = getattr(
                        threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡢࡦࡪࡤࡺࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࡠࡶࡤࡶ࡬࡫ࡴࠨূ"), None
                    )
                    cli.test_framework.track_event(
                        ctx, state, TestHookState.PRE, attrs,
                        **({bstack1l1llll_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࡡࡷࡥࡷ࡭ࡥࡵࠩৃ"): scenario_target} if scenario_target else {}),
                    )
            except Exception as e:
                logger.debug(bstack1l1llll_opy_ (u"ࠣࡄ࡬ࡲࡦࡸࡹࡇ࡮ࡲࡻࠥࡹࡴࡢࡴࡷࡣ࡭ࡵ࡯࡬ࠢࡨࡶࡷࡵࡲ࠻ࠢࠨࡷࠧৄ"), e)
            return
        try:
            bstack11l11lll_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡉࡑࡒࡏࡘ࠭৅"), bstack1l1llll_opy_ (u"ࠪࠫ৆")).split(bstack1l1llll_opy_ (u"ࠫ࠱࠭ে"))
            if name in bstack11l11lll_opy_ and bstack11l11lll_opy_ != [bstack1l1llll_opy_ (u"ࠬ࠭ৈ")]:
                return
            bstack11l11111_opy_ = uuid4().__str__()
            self.tests[bstack11l11111_opy_] = {}
            self.bstack11l1l111_opy_.start()
            scopes = []
            driver = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ৉"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1l1llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ৊")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11l11111_opy_)
            if name in [bstack1l1llll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧো"), bstack1l1llll_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠧৌ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1l1llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨ্ࠦ"), bstack1l1llll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠦৎ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1l1llll_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭৏")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11ll1l1l_opy_(
                name=name,
                uuid=bstack11l11111_opy_,
                started_at=bstack1l1111ll_opy_(),
                file_path=file_path,
                framework=bstack1l1llll_opy_ (u"ࠨࡂࡦࡪࡤࡺࡪࠨ৐"),
                integrations=TestHubHandler.bstack1l11111l_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1l1llll_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣ৑"),
                hook_type=name
            )
            self.tests[bstack11l11111_opy_][bstack1l1llll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡢࡶࡤࠦ৒")] = hook_data
            current_test_id = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠤࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨ৓"), None)
            if current_test_id:
                hook_data.bstack111llll1_opy_(current_test_id)
            if name == bstack1l1llll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ৔"):
                threading.current_thread().before_all_hook_uuid = bstack11l11111_opy_
            threading.current_thread().current_hook_uuid = bstack11l11111_opy_
            TestHubHandler.bstack11lll1ll_opy_(bstack1l1llll_opy_ (u"ࠦࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠧ৕"), hook_data)
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࠡࡪࡲࡳࡰࠦࡥࡷࡧࡱࡸࡸ࠲ࠠࡩࡱࡲ࡯ࠥࡴࡡ࡮ࡧ࠽ࠤࠪࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠧࡶࠦ৖"), name, e)
    def end_hook(self, hook_name, attrs):
        if self._1ll1111l_opy_():
            try:
                ctx = self._1l1l1lll_opy_()
                bstack1l1111l1_opy_ = {
                    bstack1l1llll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪৗ"):      TestFrameworkState.BEFORE_ALL,
                    bstack1l1llll_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ৘"):       TestFrameworkState.AFTER_ALL,
                    bstack1l1llll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ৙"): TestFrameworkState.BEFORE_EACH,
                    bstack1l1llll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ৚"):  TestFrameworkState.AFTER_EACH,
                    bstack1l1llll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫ৛"):  TestFrameworkState.BEFORE_ALL,
                    bstack1l1llll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫড়"):   TestFrameworkState.AFTER_ALL,
                }
                state = bstack1l1111l1_opy_.get(hook_name) if hook_name else None
                if state:
                    scenario_target = getattr(
                        threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡨࡥࡩࡣࡹࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ࡟ࡵࡣࡵ࡫ࡪࡺࠧঢ়"), None
                    )
                    cli.test_framework.track_event(
                        ctx, state, TestHookState.POST, attrs,
                        **({bstack1l1llll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࡠࡶࡤࡶ࡬࡫ࡴࠨ৞"): scenario_target} if scenario_target else {}),
                    )
            except Exception as e:
                logger.debug(bstack1l1llll_opy_ (u"ࠢࡃ࡫ࡱࡥࡷࡿࡆ࡭ࡱࡺࠤࡪࡴࡤࡠࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࠥࡴࠤয়"), e)
            return
        hook_name = getattr(attrs, bstack1l1llll_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫৠ"), None) or (hasattr(self, bstack1l1llll_opy_ (u"ࠩࡢࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧৡ")) and self._1l1l1l11_opy_)
        bstack11l11lll_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡗࡉࡑ࡟ࡅࡇࡉࡅ࡚ࡒࡔࡠࡊࡒࡓࡐ࡙ࠧৢ"), bstack1l1llll_opy_ (u"ࠫࠬৣ")).split(bstack1l1llll_opy_ (u"ࠬ࠲ࠧ৤"))
        if hook_name in bstack11l11lll_opy_ and bstack11l11lll_opy_ != [bstack1l1llll_opy_ (u"࠭ࠧ৥")]:
            return
        bstack1ll111l1_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ০"), None)
        hook_data = self.tests[bstack1ll111l1_opy_][bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ১")]
        status = bstack1l1llll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ২")
        exception = None
        bstack11llllll_opy_ = None
        if hook_data.name == bstack1l1llll_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨ৩"):
            self.bstack11l1l111_opy_.reset()
            bstack1l1l11ll_opy_ = self.tests[bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ৪"), None)][bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ৫")].result.result
            if bstack1l1l11ll_opy_ == bstack1l1llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ৬"):
                if attrs.hook_failures == 1:
                    status = bstack1l1llll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ৭")
                elif attrs.hook_failures == 2:
                    status = bstack1l1llll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ৮")
            elif attrs.aborted:
                status = bstack1l1llll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ৯")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1l1llll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧৰ") and attrs.hook_failures == 1:
                status = bstack1l1llll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦৱ")
            elif hasattr(attrs, bstack1l1llll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬ৲")) and attrs.error_message:
                status = bstack1l1llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ৳")
            bstack11llllll_opy_, exception = self._1l1ll11l_opy_(attrs)
        bstack111lll1l_opy_ = Result(result=status, exception=exception, bstack1l1l1ll1_opy_=[bstack11llllll_opy_])
        hook_data.stop(time=bstack1l1111ll_opy_(), duration=0, result=bstack111lll1l_opy_)
        TestHubHandler.bstack11lll1ll_opy_(bstack1l1llll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ৴"), self.tests[bstack1ll111l1_opy_][bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ৵")])
        threading.current_thread().current_hook_uuid = None
    def _1l1ll11l_opy_(self, attrs):
        try:
            import traceback
            bstack1l11ll1l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11llllll_opy_ = bstack1l11ll1l_opy_[-1] if bstack1l11ll1l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1l1llll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡷࡧࡣࡦࡤࡤࡧࡰࠨ৶"))
            bstack11llllll_opy_ = None
            exception = None
        return bstack11llllll_opy_, exception
    def _1l1l111l_opy_(self, attrs, runner, status):
        bstack1l1llll_opy_ (u"ࠥࠦࠧࡋࡸࡵࡴࡤࡧࡹࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠮ࠤࡹࡸࡡࡤࡧࡥࡥࡨࡱࠠࡧࡱࡵࠤࡦࠦࡂࡦࡪࡤࡺࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡹࠦࡥ࡯ࡦࡢࡸࡪࡹࡴࠡࠪࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠬ࠰ࠥࡧࡴࡵࡴࡶࠤ࡮ࡹࠠࡵࡪࡨࠤࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡩ࡫ࡦ࡬ࠥ࡮ࡡࡴࠢࡱࡳࠏࠦࠠࠡࠢࠣࠤࠥࠦࡠࡦࡺࡦࡩࡵࡺࡩࡰࡰࡣ࠳ࡥ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡥࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦࡵࠣ⠘ࠥࡵ࡮࡭ࡻࠣࡗࡹ࡫ࡰࠡࡦࡲࡩࡸ࠴ࠠࡕࡪࡨࠤࡷࡻ࡮࡯ࡧࡵࠎࠥࠦࠠࠡࠢࠣࠤࠥࡩࡡࡳࡴ࡬ࡩࡸࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡦࡦࠣࡷࡹ࡫ࡰࠨࡵࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡶࡪࡣࠣࡱ࡮ࡸࡲࡰࡴ࡬ࡲ࡬ࠦࡤࡰࡰࡨࠤ࡮ࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡯ࡲࡨࡤࡨࡥࡩࡣࡹࡩࡤࡹࡴࡦࡲࡢࡶࡺࡴࠠࠩࡵࡨࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫࠰ࡡࡢ࡭ࡳ࡯ࡴࡠࡡ࠱ࡴࡾ࠯࠮࡙ࠡ࡫ࡩࡳࠦࡲࡶࡰࡱࡩࡷࠦࡩࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡱࡴࡨࡪࡪࡸࠠࡪࡶ࠱ࠤࡋࡧ࡬࡭ࡵࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡓࡵ࡮ࡦࠢ࠲ࠤࡠࡔ࡯࡯ࡧࡠࠤࡴࡴࠠࡢࡰࡼࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡹ࡯ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷ࡬ࡪࠦࡓࡅࡍࠣࡲࡪࡼࡥࡳࠢࡥࡶࡪࡧ࡫ࡴࠢࡷ࡬ࡪࠦࡵࡴࡧࡵࠫࡸࠦࡴࡦࡵࡷࠤࡷࡻ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤ࠭࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮࠭ࠢࡦࡹࡸࡺ࡯࡮ࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡲࡩࡴࡶࡢࡳ࡫ࡥࡳࡵࡴ࡬ࡲ࡬ࡹࠩ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ৷")
        if status != bstack1l1llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ৸"):
            return None, None
        try:
            import traceback
            bstack1l11lll1_opy_ = getattr(runner, bstack1l1llll_opy_ (u"ࠬ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨ৹"), None) if runner is not None else None
            bstack1l1lllll_opy_ = getattr(runner, bstack1l1llll_opy_ (u"࠭ࡥࡹࡥࡢࡸࡷࡧࡣࡦࡤࡤࡧࡰ࠭৺"), None) if runner is not None else None
            if bstack1l11lll1_opy_ is not None or bstack1l1lllll_opy_ is not None:
                bstack11ll11l1_opy_ = traceback.format_tb(bstack1l1lllll_opy_) if bstack1l1lllll_opy_ is not None else []
                return bstack1l11lll1_opy_, (bstack11ll11l1_opy_ if bstack11ll11l1_opy_ else [None])
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠢࡠࡧࡻࡸࡷࡧࡣࡵࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࡣࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡴࡸࡲࡳ࡫ࡲ࠮ࡤࡤࡷࡪࡪࠠࡦࡺࡷࡶࡦࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣ৻").format(str(e)))
        return None, [None]
    def _11ll1l11_opy_(self, scenario):
        bstack1l1llll_opy_ (u"ࠣࠤࠥࡖࡪࡴࡤࡦࡴࠣࡸ࡭࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰࠢࡶࡸࡪࡶࠠࡵࡧࡻࡸࠥࡧࡳࠡࡣࠣࡷ࡮ࡴࡧ࡭ࡧࠣࡷࡹࡸࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡧࡶࡸࡤࡸࡵ࡯࠰ࡥࡳࡩࡿ࠮ࡤࡱࡧࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡋࡱ࡬ࡲࡸࠦࡢࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦࡢࡷࡹ࡫ࡰࡴࠢࠫ࡭࡫ࠦࡡ࡯ࡻࠬࠤࡦࡴࡤࠡࡵࡦࡩࡳࡧࡲࡪࡱࠣࡷࡹ࡫ࡰࡴࠢࡤࡷࠥࠨ࡫ࡦࡻࡺࡳࡷࡪࠠ࡯ࡣࡰࡩࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠ࡭࡫ࡱࡩࡸ࠴ࠠࡖࡵࡨࡷࠥ࠴ࡦࡰࡴࡰࡥࡹ࠮ࠩࠡ࡫ࡱࡷࡹ࡫ࡡࡥࠢࡲࡪࠥ࡬࠭ࡴࡶࡵ࡭ࡳ࡭ࡳࠡࡶࡲࠤࡷ࡫࡭ࡢ࡫ࡱࠤࡸࡧࡦࡦࠢࡸࡲࡩ࡫ࡲࠡࡶ࡫ࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡳࡧ࡬ࡵࡴࡥࡤࡸࡴࡸࠠࠩࡵࡨࡩࠥࡧ࡮ࡵ࡫࠰ࡴࡦࡺࡴࡦࡴࡱࠤࠨ࠷࠴ࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢৼ")
        try:
            steps = []
            background_steps = getattr(scenario, bstack1l1llll_opy_ (u"ࠩࡥࡥࡨࡱࡧࡳࡱࡸࡲࡩࡥࡳࡵࡧࡳࡷࠬ৽"), None) or []
            for s in background_steps:
                keyword = getattr(s, bstack1l1llll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ৾"), bstack1l1llll_opy_ (u"ࠫࠬ৿")) or bstack1l1llll_opy_ (u"ࠬ࠭਀")
                name = getattr(s, bstack1l1llll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫਁ"), bstack1l1llll_opy_ (u"ࠧࠨਂ")) or bstack1l1llll_opy_ (u"ࠨࠩਃ")
                steps.append(bstack1l1llll_opy_ (u"ࠤࡾࢁࠥࢁࡽࠣ਄").format(keyword, name).strip())
            scenario_steps = getattr(scenario, bstack1l1llll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩਅ"), None) or []
            for s in scenario_steps:
                keyword = getattr(s, bstack1l1llll_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬਆ"), bstack1l1llll_opy_ (u"ࠬ࠭ਇ")) or bstack1l1llll_opy_ (u"࠭ࠧਈ")
                name = getattr(s, bstack1l1llll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬਉ"), bstack1l1llll_opy_ (u"ࠨࠩਊ")) or bstack1l1llll_opy_ (u"ࠩࠪ਋")
                steps.append(bstack1l1llll_opy_ (u"ࠥࡿࢂࠦࡻࡾࠤ਌").format(keyword, name).strip())
            return bstack1l1llll_opy_ (u"ࠦࡡࡴࠢ਍").join(steps) if steps else None
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡥࡲࡦࡰࡧࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࡠࡥࡲࡨࡪࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠥ਎").format(str(e)))
            return None