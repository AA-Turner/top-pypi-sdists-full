# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack1lll1lllll1_opy_ import bstack1llll111111_opy_, bstack1llll11l1ll_opy_
from bstack_utils.bstack111l1ll11_opy_ import bstack111ll111_opy_
from bstack_utils.helper import bstack1ll11l1ll1_opy_, bstack1111l1l1l_opy_, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack1llll11111l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11l111ll1l_opy_:
    def __init__(self):
        self.bstack1lll1llll1l_opy_ = bstack1llll11111l_opy_(self.bstack1llll11l111_opy_)
        self.tests = {}
    @staticmethod
    def bstack1llll11l111_opy_(log):
        if not (log[bstack111ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨღ")] and log[bstack111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩყ")].strip()):
            return
        active = bstack111ll111_opy_.bstack1llll111l1l_opy_()
        log = {
            bstack111ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨშ"): log[bstack111ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩჩ")],
            bstack111ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧც"): bstack1111l1l1l_opy_(),
            bstack111ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ძ"): log[bstack111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧწ")],
        }
        if active:
            if active[bstack111ll_opy_ (u"ࠧࡵࡻࡳࡩࠬჭ")] == bstack111ll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ხ"):
                log[bstack111ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩჯ")] = active[bstack111ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪჰ")]
            elif active[bstack111ll_opy_ (u"ࠫࡹࡿࡰࡦࠩჱ")] == bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࠪჲ"):
                log[bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ჳ")] = active[bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧჴ")]
        TestHubHandler.bstack1lllll1l1_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1lll1llll1l_opy_.start()
        driver = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧჵ"), None)
        bstack1lll1lllll1_opy_ = bstack1llll11l1ll_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1111l1l1l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack111ll_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥჶ"),
            framework=bstack111ll_opy_ (u"ࠪࡆࡪ࡮ࡡࡷࡧࠪჷ"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack1llll11lll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧჸ")] = bstack1lll1lllll1_opy_
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.bstack1llll11ll11_opy_(bstack111ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ჹ"), bstack1lll1lllll1_opy_)
    def end_test(self, attrs):
        bstack1lll1llllll_opy_ = {
            bstack111ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦჺ"): attrs.feature.name,
            bstack111ll_opy_ (u"ࠢࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧ჻"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack1lll1lllll1_opy_ = self.tests[current_test_uuid][bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫჼ")]
        meta = {
            bstack111ll_opy_ (u"ࠤࡩࡩࡦࡺࡵࡳࡧࠥჽ"): bstack1lll1llllll_opy_,
            bstack111ll_opy_ (u"ࠥࡷࡹ࡫ࡰࡴࠤჾ"): bstack1lll1lllll1_opy_.meta.get(bstack111ll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪჿ"), []),
            bstack111ll_opy_ (u"ࠧࡹࡣࡦࡰࡤࡶ࡮ࡵࠢᄀ"): {
                bstack111ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᄁ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack1lll1lllll1_opy_.bstack1llll1111l1_opy_(meta)
        bstack1lll1lllll1_opy_.bstack1llll1l11l1_opy_(bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬᄂ"), []))
        bstack1llll11l11l_opy_, exception = self._1llll111l11_opy_(attrs)
        status = bstack111ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᄃ") if attrs.status.name.lower() == bstack111ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᄄ") else attrs.status.name.lower()
        bstack1llll1l11ll_opy_ = Result(result=status, exception=exception, bstack1llll1l111l_opy_=[bstack1llll11l11l_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᄅ")].stop(time=bstack1111l1l1l_opy_(), duration=int(attrs.duration)*1000, result=bstack1llll1l11ll_opy_)
        TestHubHandler.bstack1llll11ll11_opy_(bstack111ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᄆ"), self.tests[threading.current_thread().current_test_uuid][bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᄇ")])
    def bstack1l1111ll_opy_(self, attrs):
        bstack1lll1llll11_opy_ = {
            bstack111ll_opy_ (u"࠭ࡩࡥࠩᄈ"): uuid4().__str__(),
            bstack111ll_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨᄉ"): attrs.keyword,
            bstack111ll_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨᄊ"): [],
            bstack111ll_opy_ (u"ࠩࡷࡩࡽࡺࠧᄋ"): attrs.name,
            bstack111ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᄌ"): bstack1111l1l1l_opy_(),
            bstack111ll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᄍ"): bstack111ll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᄎ"),
            bstack111ll_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᄏ"): bstack111ll_opy_ (u"ࠧࠨᄐ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᄑ")].add_step(bstack1lll1llll11_opy_)
        threading.current_thread().current_step_uuid = bstack1lll1llll11_opy_[bstack111ll_opy_ (u"ࠩ࡬ࡨࠬᄒ")]
    def bstack1llll11ll_opy_(self, attrs):
        current_test_id = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᄓ"), None)
        current_step_uuid = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨᄔ"), None)
        bstack1llll11l11l_opy_, exception = self._1llll111l11_opy_(attrs)
        status = bstack111ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᄕ") if attrs.status.name.lower() == bstack111ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᄖ") else attrs.status.name.lower()
        bstack1llll1l11ll_opy_ = Result(result=status, exception=exception, bstack1llll1l111l_opy_=[bstack1llll11l11l_opy_])
        self.tests[current_test_id][bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᄗ")].bstack1llll111lll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1llll1l11ll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11l11l1l11_opy_(self, name, attrs):
        try:
            bstack1llll11llll_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡈࡐࡑࡎࡗࠬᄘ"), bstack111ll_opy_ (u"ࠩࠪᄙ")).split(bstack111ll_opy_ (u"ࠪ࠰ࠬᄚ"))
            if name in bstack1llll11llll_opy_ and bstack1llll11llll_opy_ != [bstack111ll_opy_ (u"ࠫࠬᄛ")]:
                return
            bstack1llll111ll1_opy_ = uuid4().__str__()
            self.tests[bstack1llll111ll1_opy_] = {}
            self.bstack1lll1llll1l_opy_.start()
            scopes = []
            driver = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫᄜ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack111ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫᄝ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1llll111ll1_opy_)
            if name in [bstack111ll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦᄞ"), bstack111ll_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦᄟ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack111ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥᄠ"), bstack111ll_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠥᄡ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack111ll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᄢ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1llll111111_opy_(
                name=name,
                uuid=bstack1llll111ll1_opy_,
                started_at=bstack1111l1l1l_opy_(),
                file_path=file_path,
                framework=bstack111ll_opy_ (u"ࠧࡈࡥࡩࡣࡹࡩࠧᄣ"),
                integrations=TestHubHandler.bstack1llll11lll1_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack111ll_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢᄤ"),
                hook_type=name
            )
            self.tests[bstack1llll111ll1_opy_][bstack111ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡡࡵࡣࠥᄥ")] = hook_data
            current_test_id = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠣࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧᄦ"), None)
            if current_test_id:
                hook_data.bstack1llll1111ll_opy_(current_test_id)
            if name == bstack111ll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨᄧ"):
                threading.current_thread().before_all_hook_uuid = bstack1llll111ll1_opy_
            threading.current_thread().current_hook_uuid = bstack1llll111ll1_opy_
            TestHubHandler.bstack1llll11ll11_opy_(bstack111ll_opy_ (u"ࠥࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠦᄨ"), hook_data)
        except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠࡩࡱࡲ࡯ࠥ࡫ࡶࡦࡰࡷࡷ࠱ࠦࡨࡰࡱ࡮ࠤࡳࡧ࡭ࡦ࠼ࠣࠩࡸ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠦࡵࠥᄩ"), name, e)
    def bstack11ll1ll11l_opy_(self, attrs):
        hook_name = getattr(attrs, bstack111ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᄪ"), None) or (hasattr(self, bstack111ll_opy_ (u"࠭࡟ࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᄫ")) and self._1llll11ll1l_opy_)
        bstack1llll11llll_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡉࡋࡆࡂࡗࡏࡘࡤࡎࡏࡐࡍࡖࠫᄬ"), bstack111ll_opy_ (u"ࠨࠩᄭ")).split(bstack111ll_opy_ (u"ࠩ࠯ࠫᄮ"))
        if hook_name in bstack1llll11llll_opy_ and bstack1llll11llll_opy_ != [bstack111ll_opy_ (u"ࠪࠫᄯ")]:
            return
        bstack1llll11l1l1_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᄰ"), None)
        hook_data = self.tests[bstack1llll11l1l1_opy_][bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᄱ")]
        status = bstack111ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᄲ")
        exception = None
        bstack1llll11l11l_opy_ = None
        if hook_data.name == bstack111ll_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠥᄳ"):
            self.bstack1lll1llll1l_opy_.reset()
            bstack1llll1l1111_opy_ = self.tests[bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᄴ"), None)][bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᄵ")].result.result
            if bstack1llll1l1111_opy_ == bstack111ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᄶ"):
                if attrs.hook_failures == 1:
                    status = bstack111ll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᄷ")
                elif attrs.hook_failures == 2:
                    status = bstack111ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᄸ")
            elif attrs.aborted:
                status = bstack111ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᄹ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack111ll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫᄺ") and attrs.hook_failures == 1:
                status = bstack111ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᄻ")
            elif hasattr(attrs, bstack111ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡠ࡯ࡨࡷࡸࡧࡧࡦࠩᄼ")) and attrs.error_message:
                status = bstack111ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᄽ")
            bstack1llll11l11l_opy_, exception = self._1llll111l11_opy_(attrs)
        bstack1llll1l11ll_opy_ = Result(result=status, exception=exception, bstack1llll1l111l_opy_=[bstack1llll11l11l_opy_])
        hook_data.stop(time=bstack1111l1l1l_opy_(), duration=0, result=bstack1llll1l11ll_opy_)
        TestHubHandler.bstack1llll11ll11_opy_(bstack111ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᄾ"), self.tests[bstack1llll11l1l1_opy_][bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᄿ")])
        threading.current_thread().current_hook_uuid = None
    def _1llll111l11_opy_(self, attrs):
        try:
            import traceback
            bstack11l1lll11_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1llll11l11l_opy_ = bstack11l1lll11_opy_[-1] if bstack11l1lll11_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack111ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡶࡸࡴࡳࠠࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࠥᅀ"))
            bstack1llll11l11l_opy_ = None
            exception = None
        return bstack1llll11l11l_opy_, exception