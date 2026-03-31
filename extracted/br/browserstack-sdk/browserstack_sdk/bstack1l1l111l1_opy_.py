# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.test_data import bstack1lllll111l1_opy_, TestData
from bstack_utils.bstack111l111l_opy_ import bstack11l11l1lll_opy_
from bstack_utils.helper import bstack1l1111l111_opy_, current_time, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack1llll1llll1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l1l111l1_opy_:
    def __init__(self):
        self.bstack1lllll1111l_opy_ = bstack1llll1llll1_opy_(self.bstack1lllll1ll11_opy_)
        self.tests = {}
    @staticmethod
    def bstack1lllll1ll11_opy_(log):
        if not (log[bstack1ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨႮ")] and log[bstack1ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩႯ")].strip()):
            return
        active = bstack11l11l1lll_opy_.bstack1lllll11ll1_opy_()
        log = {
            bstack1ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨႰ"): log[bstack1ll11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩႱ")],
            bstack1ll11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧႲ"): current_time(),
            bstack1ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ⴓ"): log[bstack1ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧႴ")],
        }
        if active:
            if active[bstack1ll11_opy_ (u"ࠧࡵࡻࡳࡩࠬႵ")] == bstack1ll11_opy_ (u"ࠨࡪࡲࡳࡰ࠭Ⴖ"):
                log[bstack1ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩႷ")] = active[bstack1ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪႸ")]
            elif active[bstack1ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩႹ")] == bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࠪႺ"):
                log[bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ⴛ")] = active[bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧႼ")]
        TestHubHandler.bstack11111lll1l_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1lllll1111l_opy_.start()
        driver = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧႽ"), None)
        test_data = TestData(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=current_time(),
            file_path=attrs.feature.filename,
            result=bstack1ll11_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥႾ"),
            framework=bstack1ll11_opy_ (u"ࠪࡆࡪ࡮ࡡࡷࡧࠪႿ"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack1lllll1l111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧჀ")] = test_data
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.send_run_event(bstack1ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭Ⴡ"), test_data)
    def end_test(self, attrs):
        bstack1lllll1lll1_opy_ = {
            bstack1ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦჂ"): attrs.feature.name,
            bstack1ll11_opy_ (u"ࠢࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧჃ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        test_data = self.tests[current_test_uuid][bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫჄ")]
        meta = {
            bstack1ll11_opy_ (u"ࠤࡩࡩࡦࡺࡵࡳࡧࠥჅ"): bstack1lllll1lll1_opy_,
            bstack1ll11_opy_ (u"ࠥࡷࡹ࡫ࡰࡴࠤ჆"): test_data.meta.get(bstack1ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪჇ"), []),
            bstack1ll11_opy_ (u"ࠧࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ჈"): {
                bstack1ll11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ჉"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        test_data.bstack1lllll111ll_opy_(meta)
        test_data.bstack1llll1lll1l_opy_(bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ჊"), []))
        bstack1lllll1ll1l_opy_, exception = self._1lllll11111_opy_(attrs)
        status = bstack1ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ჋") if attrs.status.name.lower() == bstack1ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ჌") else attrs.status.name.lower()
        bstack1llll1lllll_opy_ = Result(result=status, exception=exception, bstack1lllll11l1l_opy_=[bstack1lllll1ll1l_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭Ⴭ")].stop(time=current_time(), duration=int(attrs.duration)*1000, result=bstack1llll1lllll_opy_)
        TestHubHandler.send_run_event(bstack1ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭჎"), self.tests[threading.current_thread().current_test_uuid][bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ჏")])
    def bstack1ll11lll11_opy_(self, attrs):
        bstack1lllll1l11l_opy_ = {
            bstack1ll11_opy_ (u"࠭ࡩࡥࠩა"): uuid4().__str__(),
            bstack1ll11_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨბ"): attrs.keyword,
            bstack1ll11_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨგ"): [],
            bstack1ll11_opy_ (u"ࠩࡷࡩࡽࡺࠧდ"): attrs.name,
            bstack1ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧე"): current_time(),
            bstack1ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫვ"): bstack1ll11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ზ"),
            bstack1ll11_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫთ"): bstack1ll11_opy_ (u"ࠧࠨი")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫკ")].add_step(bstack1lllll1l11l_opy_)
        threading.current_thread().current_step_uuid = bstack1lllll1l11l_opy_[bstack1ll11_opy_ (u"ࠩ࡬ࡨࠬლ")]
    def bstack11111l11l_opy_(self, attrs):
        current_test_id = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧმ"), None)
        current_step_uuid = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨნ"), None)
        bstack1lllll1ll1l_opy_, exception = self._1lllll11111_opy_(attrs)
        status = bstack1ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬო") if attrs.status.name.lower() == bstack1ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬპ") else attrs.status.name.lower()
        bstack1llll1lllll_opy_ = Result(result=status, exception=exception, bstack1lllll11l1l_opy_=[bstack1lllll1ll1l_opy_])
        self.tests[current_test_id][bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪჟ")].bstack1lllll11lll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1llll1lllll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l1lll1lll_opy_(self, name, attrs):
        try:
            bstack1lllll11l11_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡈࡐࡑࡎࡗࠬრ"), bstack1ll11_opy_ (u"ࠩࠪს")).split(bstack1ll11_opy_ (u"ࠪ࠰ࠬტ"))
            if name in bstack1lllll11l11_opy_ and bstack1lllll11l11_opy_ != [bstack1ll11_opy_ (u"ࠫࠬუ")]:
                return
            bstack1llll1ll1l1_opy_ = uuid4().__str__()
            self.tests[bstack1llll1ll1l1_opy_] = {}
            self.bstack1lllll1111l_opy_.start()
            scopes = []
            driver = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫფ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫქ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1llll1ll1l1_opy_)
            if name in [bstack1ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦღ"), bstack1ll11_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦყ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1ll11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥშ"), bstack1ll11_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠥჩ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1ll11_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬც")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1lllll111l1_opy_(
                name=name,
                uuid=bstack1llll1ll1l1_opy_,
                started_at=current_time(),
                file_path=file_path,
                framework=bstack1ll11_opy_ (u"ࠧࡈࡥࡩࡣࡹࡩࠧძ"),
                integrations=TestHubHandler.bstack1lllll1l111_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1ll11_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢწ"),
                hook_type=name
            )
            self.tests[bstack1llll1ll1l1_opy_][bstack1ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡡࡵࡣࠥჭ")] = hook_data
            current_test_id = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠣࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧხ"), None)
            if current_test_id:
                hook_data.bstack1llll1ll1ll_opy_(current_test_id)
            if name == bstack1ll11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨჯ"):
                threading.current_thread().before_all_hook_uuid = bstack1llll1ll1l1_opy_
            threading.current_thread().current_hook_uuid = bstack1llll1ll1l1_opy_
            TestHubHandler.send_run_event(bstack1ll11_opy_ (u"ࠥࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠦჰ"), hook_data)
        except Exception as e:
            logger.debug(bstack1ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠࡩࡱࡲ࡯ࠥ࡫ࡶࡦࡰࡷࡷ࠱ࠦࡨࡰࡱ࡮ࠤࡳࡧ࡭ࡦ࠼ࠣࠩࡸ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠦࡵࠥჱ"), name, e)
    def bstack11l1l1l1l1_opy_(self, attrs):
        hook_name = getattr(attrs, bstack1ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨჲ"), None) or (hasattr(self, bstack1ll11_opy_ (u"࠭࡟ࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫჳ")) and self._1lllll1l1ll_opy_)
        bstack1lllll11l11_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡉࡋࡆࡂࡗࡏࡘࡤࡎࡏࡐࡍࡖࠫჴ"), bstack1ll11_opy_ (u"ࠨࠩჵ")).split(bstack1ll11_opy_ (u"ࠩ࠯ࠫჶ"))
        if hook_name in bstack1lllll11l11_opy_ and bstack1lllll11l11_opy_ != [bstack1ll11_opy_ (u"ࠪࠫჷ")]:
            return
        bstack1lllll1l1l1_opy_ = bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨჸ"), None)
        hook_data = self.tests[bstack1lllll1l1l1_opy_][bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨჹ")]
        status = bstack1ll11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨჺ")
        exception = None
        bstack1lllll1ll1l_opy_ = None
        if hook_data.name == bstack1ll11_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠥ჻"):
            self.bstack1lllll1111l_opy_.reset()
            bstack1llll1lll11_opy_ = self.tests[bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨჼ"), None)][bstack1ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬჽ")].result.result
            if bstack1llll1lll11_opy_ == bstack1ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥჾ"):
                if attrs.hook_failures == 1:
                    status = bstack1ll11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦჿ")
                elif attrs.hook_failures == 2:
                    status = bstack1ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᄀ")
            elif attrs.aborted:
                status = bstack1ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᄁ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1ll11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫᄂ") and attrs.hook_failures == 1:
                status = bstack1ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᄃ")
            elif hasattr(attrs, bstack1ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࡠ࡯ࡨࡷࡸࡧࡧࡦࠩᄄ")) and attrs.error_message:
                status = bstack1ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᄅ")
            bstack1lllll1ll1l_opy_, exception = self._1lllll11111_opy_(attrs)
        bstack1llll1lllll_opy_ = Result(result=status, exception=exception, bstack1lllll11l1l_opy_=[bstack1lllll1ll1l_opy_])
        hook_data.stop(time=current_time(), duration=0, result=bstack1llll1lllll_opy_)
        TestHubHandler.send_run_event(bstack1ll11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᄆ"), self.tests[bstack1lllll1l1l1_opy_][bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᄇ")])
        threading.current_thread().current_hook_uuid = None
    def _1lllll11111_opy_(self, attrs):
        try:
            import traceback
            bstack1lll11ll_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1lllll1ll1l_opy_ = bstack1lll11ll_opy_[-1] if bstack1lll11ll_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡶࡸࡴࡳࠠࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࠥᄈ"))
            bstack1lllll1ll1l_opy_ = None
            exception = None
        return bstack1lllll1ll1l_opy_, exception