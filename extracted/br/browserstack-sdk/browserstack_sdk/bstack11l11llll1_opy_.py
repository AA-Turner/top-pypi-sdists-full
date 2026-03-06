# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.test_data import bstack1111l1ll11_opy_, TestData
from bstack_utils.bstack1111l1l1l1_opy_ import bstack11l111ll11_opy_
from bstack_utils.helper import bstack1lll11lll1_opy_, current_time, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack1111l111ll_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11l11llll1_opy_:
    def __init__(self):
        self.bstack1111ll11ll_opy_ = bstack1111l111ll_opy_(self.bstack1111ll1111_opy_)
        self.tests = {}
    @staticmethod
    def bstack1111ll1111_opy_(log):
        if not (log[bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྼ")] and log[bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ྽")].strip()):
            return
        active = bstack11l111ll11_opy_.bstack1111ll1l11_opy_()
        log = {
            bstack1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ྾"): log[bstack1111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ྿")],
            bstack1111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ࿀"): current_time(),
            bstack1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿁"): log[bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿂")],
        }
        if active:
            if active[bstack1111_opy_ (u"ࠪࡸࡾࡶࡥࠨ࿃")] == bstack1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ࿄"):
                log[bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ࿅")] = active[bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࿆࠭")]
            elif active[bstack1111_opy_ (u"ࠧࡵࡻࡳࡩࠬ࿇")] == bstack1111_opy_ (u"ࠨࡶࡨࡷࡹ࠭࿈"):
                log[bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ࿉")] = active[bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ࿊")]
        TestHubHandler.bstack1l1111l11_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1111ll11ll_opy_.start()
        driver = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ࿋"), None)
        test_data = TestData(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=current_time(),
            file_path=attrs.feature.filename,
            result=bstack1111_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨ࿌"),
            framework=bstack1111_opy_ (u"࠭ࡂࡦࡪࡤࡺࡪ࠭࿍"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack11111lllll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ࿎")] = test_data
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.send_run_event(bstack1111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ࿏"), test_data)
    def end_test(self, attrs):
        bstack1111l11l1l_opy_ = {
            bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ࿐"): attrs.feature.name,
            bstack1111_opy_ (u"ࠥࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣ࿑"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        test_data = self.tests[current_test_uuid][bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࿒")]
        meta = {
            bstack1111_opy_ (u"ࠧ࡬ࡥࡢࡶࡸࡶࡪࠨ࿓"): bstack1111l11l1l_opy_,
            bstack1111_opy_ (u"ࠨࡳࡵࡧࡳࡷࠧ࿔"): test_data.meta.get(bstack1111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭࿕"), []),
            bstack1111_opy_ (u"ࠣࡵࡦࡩࡳࡧࡲࡪࡱࠥ࿖"): {
                bstack1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ࿗"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        test_data.bstack1111l1llll_opy_(meta)
        test_data.bstack1111l11ll1_opy_(bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ࿘"), []))
        bstack1111ll11l1_opy_, exception = self._1111l1111l_opy_(attrs)
        status = bstack1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ࿙") if attrs.status.name.lower() == bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ࿚") else attrs.status.name.lower()
        bstack1111l11l11_opy_ = Result(result=status, exception=exception, bstack1111l11lll_opy_=[bstack1111ll11l1_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿛")].stop(time=current_time(), duration=int(attrs.duration)*1000, result=bstack1111l11l11_opy_)
        TestHubHandler.send_run_event(bstack1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ࿜"), self.tests[threading.current_thread().current_test_uuid][bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿝")])
    def bstack11ll1l1l11_opy_(self, attrs):
        bstack1111l1lll1_opy_ = {
            bstack1111_opy_ (u"ࠩ࡬ࡨࠬ࿞"): uuid4().__str__(),
            bstack1111_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ࿟"): attrs.keyword,
            bstack1111_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫ࿠"): [],
            bstack1111_opy_ (u"ࠬࡺࡥࡹࡶࠪ࿡"): attrs.name,
            bstack1111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ࿢"): current_time(),
            bstack1111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ࿣"): bstack1111_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ࿤"),
            bstack1111_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ࿥"): bstack1111_opy_ (u"ࠪࠫ࿦")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࿧")].add_step(bstack1111l1lll1_opy_)
        threading.current_thread().current_step_uuid = bstack1111l1lll1_opy_[bstack1111_opy_ (u"ࠬ࡯ࡤࠨ࿨")]
    def bstack1l1l1lll_opy_(self, attrs):
        current_test_id = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ࿩"), None)
        current_step_uuid = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫ࿪"), None)
        bstack1111ll11l1_opy_, exception = self._1111l1111l_opy_(attrs)
        status = bstack1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ࿫") if attrs.status.name.lower() == bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ࿬") else attrs.status.name.lower()
        bstack1111l11l11_opy_ = Result(result=status, exception=exception, bstack1111l11lll_opy_=[bstack1111ll11l1_opy_])
        self.tests[current_test_id][bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿭")].bstack1111l1l11l_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1111l11l11_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11l1ll1l1_opy_(self, name, attrs):
        try:
            bstack1111l111l1_opy_ = os.environ.get(bstack1111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡘࡊࡋࡠࡆࡈࡊࡆ࡛ࡌࡕࡡࡋࡓࡔࡑࡓࠨ࿮"), bstack1111_opy_ (u"ࠬ࠭࿯")).split(bstack1111_opy_ (u"࠭ࠬࠨ࿰"))
            if name in bstack1111l111l1_opy_ and bstack1111l111l1_opy_ != [bstack1111_opy_ (u"ࠧࠨ࿱")]:
                return
            bstack1111l1l111_opy_ = uuid4().__str__()
            self.tests[bstack1111l1l111_opy_] = {}
            self.bstack1111ll11ll_opy_.start()
            scopes = []
            driver = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ࿲"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ࿳")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1111l1l111_opy_)
            if name in [bstack1111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ࿴"), bstack1111_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠢ࿵")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ࿶"), bstack1111_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ࿷")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1111_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ࿸")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1111l1ll11_opy_(
                name=name,
                uuid=bstack1111l1l111_opy_,
                started_at=current_time(),
                file_path=file_path,
                framework=bstack1111_opy_ (u"ࠣࡄࡨ࡬ࡦࡼࡥࠣ࿹"),
                integrations=TestHubHandler.bstack11111lllll_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1111_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥ࿺"),
                hook_type=name
            )
            self.tests[bstack1111l1l111_opy_][bstack1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡤࡸࡦࠨ࿻")] = hook_data
            current_test_id = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠦࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠣ࿼"), None)
            if current_test_id:
                hook_data.bstack1111ll111l_opy_(current_test_id)
            if name == bstack1111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ࿽"):
                threading.current_thread().before_all_hook_uuid = bstack1111l1l111_opy_
            threading.current_thread().current_hook_uuid = bstack1111l1l111_opy_
            TestHubHandler.send_run_event(bstack1111_opy_ (u"ࠨࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠢ࿾"), hook_data)
        except Exception as e:
            logger.debug(bstack1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡ࡫ࡱࠤࡸࡺࡡࡳࡶࠣ࡬ࡴࡵ࡫ࠡࡧࡹࡩࡳࡺࡳ࠭ࠢ࡫ࡳࡴࡱࠠ࡯ࡣࡰࡩ࠿ࠦࠥࡴ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠩࡸࠨ࿿"), name, e)
    def bstack1l1l11llll_opy_(self, attrs):
        hook_name = getattr(attrs, bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫက"), None) or (hasattr(self, bstack1111_opy_ (u"ࠩࡢࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧခ")) and self._1111l11111_opy_)
        bstack1111l111l1_opy_ = os.environ.get(bstack1111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡗࡉࡑ࡟ࡅࡇࡉࡅ࡚ࡒࡔࡠࡊࡒࡓࡐ࡙ࠧဂ"), bstack1111_opy_ (u"ࠫࠬဃ")).split(bstack1111_opy_ (u"ࠬ࠲ࠧင"))
        if hook_name in bstack1111l111l1_opy_ and bstack1111l111l1_opy_ != [bstack1111_opy_ (u"࠭ࠧစ")]:
            return
        bstack1111l1ll1l_opy_ = bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫဆ"), None)
        hook_data = self.tests[bstack1111l1ll1l_opy_][bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫဇ")]
        status = bstack1111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤဈ")
        exception = None
        bstack1111ll11l1_opy_ = None
        if hook_data.name == bstack1111_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨဉ"):
            self.bstack1111ll11ll_opy_.reset()
            bstack1111l1l1ll_opy_ = self.tests[bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫည"), None)][bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨဋ")].result.result
            if bstack1111l1l1ll_opy_ == bstack1111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨဌ"):
                if attrs.hook_failures == 1:
                    status = bstack1111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢဍ")
                elif attrs.hook_failures == 2:
                    status = bstack1111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣဎ")
            elif attrs.aborted:
                status = bstack1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤဏ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧတ") and attrs.hook_failures == 1:
                status = bstack1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦထ")
            elif hasattr(attrs, bstack1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬဒ")) and attrs.error_message:
                status = bstack1111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨဓ")
            bstack1111ll11l1_opy_, exception = self._1111l1111l_opy_(attrs)
        bstack1111l11l11_opy_ = Result(result=status, exception=exception, bstack1111l11lll_opy_=[bstack1111ll11l1_opy_])
        hook_data.stop(time=current_time(), duration=0, result=bstack1111l11l11_opy_)
        TestHubHandler.send_run_event(bstack1111_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩန"), self.tests[bstack1111l1ll1l_opy_][bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫပ")])
        threading.current_thread().current_hook_uuid = None
    def _1111l1111l_opy_(self, attrs):
        try:
            import traceback
            bstack1l111ll1ll_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1111ll11l1_opy_ = bstack1l111ll1ll_opy_[-1] if bstack1l111ll1ll_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡷࡧࡣࡦࡤࡤࡧࡰࠨဖ"))
            bstack1111ll11l1_opy_ = None
            exception = None
        return bstack1111ll11l1_opy_, exception