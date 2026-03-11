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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.test_data import bstack11111l11ll_opy_, TestData
from bstack_utils.bstack11l1llll_opy_ import bstack11l1ll1111_opy_
from bstack_utils.helper import bstack11llll11l_opy_, current_time, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack111111ll1l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1ll11l11_opy_:
    def __init__(self):
        self.bstack11111ll1l1_opy_ = bstack111111ll1l_opy_(self.bstack111111ll11_opy_)
        self.tests = {}
    @staticmethod
    def bstack111111ll11_opy_(log):
        if not (log[bstack1ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဤ")] and log[bstack1ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫဥ")].strip()):
            return
        active = bstack11l1ll1111_opy_.bstack11111l1111_opy_()
        log = {
            bstack1ll111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪဦ"): log[bstack1ll111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫဧ")],
            bstack1ll111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩဨ"): current_time(),
            bstack1ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨဩ"): log[bstack1ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩဪ")],
        }
        if active:
            if active[bstack1ll111_opy_ (u"ࠩࡷࡽࡵ࡫ࠧါ")] == bstack1ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨာ"):
                log[bstack1ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫိ")] = active[bstack1ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬီ")]
            elif active[bstack1ll111_opy_ (u"࠭ࡴࡺࡲࡨࠫု")] == bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸࠬူ"):
                log[bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨေ")] = active[bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩဲ")]
        TestHubHandler.bstack11lll1l1_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack11111ll1l1_opy_.start()
        driver = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩဳ"), None)
        test_data = TestData(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=current_time(),
            file_path=attrs.feature.filename,
            result=bstack1ll111_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧဴ"),
            framework=bstack1ll111_opy_ (u"ࠬࡈࡥࡩࡣࡹࡩࠬဵ"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack11111l111l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩံ")] = test_data
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.send_run_event(bstack1ll111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ့"), test_data)
    def end_test(self, attrs):
        bstack11111lll1l_opy_ = {
            bstack1ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨး"): attrs.feature.name,
            bstack1ll111_opy_ (u"ࠤࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴ္ࠢ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        test_data = self.tests[current_test_uuid][bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ်࠭")]
        meta = {
            bstack1ll111_opy_ (u"ࠦ࡫࡫ࡡࡵࡷࡵࡩࠧျ"): bstack11111lll1l_opy_,
            bstack1ll111_opy_ (u"ࠧࡹࡴࡦࡲࡶࠦြ"): test_data.meta.get(bstack1ll111_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬွ"), []),
            bstack1ll111_opy_ (u"ࠢࡴࡥࡨࡲࡦࡸࡩࡰࠤှ"): {
                bstack1ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨဿ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        test_data.bstack111111lll1_opy_(meta)
        test_data.bstack11111lll11_opy_(bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ၀"), []))
        bstack11111ll111_opy_, exception = self._11111l1l11_opy_(attrs)
        status = bstack1ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ၁") if attrs.status.name.lower() == bstack1ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ၂") else attrs.status.name.lower()
        bstack111111llll_opy_ = Result(result=status, exception=exception, bstack11111ll1ll_opy_=[bstack11111ll111_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ၃")].stop(time=current_time(), duration=int(attrs.duration)*1000, result=bstack111111llll_opy_)
        TestHubHandler.send_run_event(bstack1ll111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ၄"), self.tests[threading.current_thread().current_test_uuid][bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ၅")])
    def bstack111lll1ll1_opy_(self, attrs):
        bstack11111l1lll_opy_ = {
            bstack1ll111_opy_ (u"ࠨ࡫ࡧࠫ၆"): uuid4().__str__(),
            bstack1ll111_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪ၇"): attrs.keyword,
            bstack1ll111_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪ၈"): [],
            bstack1ll111_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ၉"): attrs.name,
            bstack1ll111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ၊"): current_time(),
            bstack1ll111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭။"): bstack1ll111_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ၌"),
            bstack1ll111_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭၍"): bstack1ll111_opy_ (u"ࠩࠪ၎")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭၏")].add_step(bstack11111l1lll_opy_)
        threading.current_thread().current_step_uuid = bstack11111l1lll_opy_[bstack1ll111_opy_ (u"ࠫ࡮ࡪࠧၐ")]
    def bstack1l1l11lll1_opy_(self, attrs):
        current_test_id = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩၑ"), None)
        current_step_uuid = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪၒ"), None)
        bstack11111ll111_opy_, exception = self._11111l1l11_opy_(attrs)
        status = bstack1ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧၓ") if attrs.status.name.lower() == bstack1ll111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧၔ") else attrs.status.name.lower()
        bstack111111llll_opy_ = Result(result=status, exception=exception, bstack11111ll1ll_opy_=[bstack11111ll111_opy_])
        self.tests[current_test_id][bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬၕ")].bstack11111lllll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111111llll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1llllll111_opy_(self, name, attrs):
        try:
            bstack111111l1ll_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡗࡉࡑ࡟ࡅࡇࡉࡅ࡚ࡒࡔࡠࡊࡒࡓࡐ࡙ࠧၖ"), bstack1ll111_opy_ (u"ࠫࠬၗ")).split(bstack1ll111_opy_ (u"ࠬ࠲ࠧၘ"))
            if name in bstack111111l1ll_opy_ and bstack111111l1ll_opy_ != [bstack1ll111_opy_ (u"࠭ࠧၙ")]:
                return
            bstack11111ll11l_opy_ = uuid4().__str__()
            self.tests[bstack11111ll11l_opy_] = {}
            self.bstack11111ll1l1_opy_.start()
            scopes = []
            driver = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ၚ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ၛ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11111ll11l_opy_)
            if name in [bstack1ll111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨၜ"), bstack1ll111_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨၝ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧၞ"), bstack1ll111_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠧၟ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1ll111_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧၠ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack11111l11ll_opy_(
                name=name,
                uuid=bstack11111ll11l_opy_,
                started_at=current_time(),
                file_path=file_path,
                framework=bstack1ll111_opy_ (u"ࠢࡃࡧ࡫ࡥࡻ࡫ࠢၡ"),
                integrations=TestHubHandler.bstack11111l111l_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1ll111_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤၢ"),
                hook_type=name
            )
            self.tests[bstack11111ll11l_opy_][bstack1ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠧၣ")] = hook_data
            current_test_id = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠥࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠢၤ"), None)
            if current_test_id:
                hook_data.bstack11111llll1_opy_(current_test_id)
            if name == bstack1ll111_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣၥ"):
                threading.current_thread().before_all_hook_uuid = bstack11111ll11l_opy_
            threading.current_thread().current_hook_uuid = bstack11111ll11l_opy_
            TestHubHandler.send_run_event(bstack1ll111_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩࠨၦ"), hook_data)
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡪࡰࠣࡷࡹࡧࡲࡵࠢ࡫ࡳࡴࡱࠠࡦࡸࡨࡲࡹࡹࠬࠡࡪࡲࡳࡰࠦ࡮ࡢ࡯ࡨ࠾ࠥࠫࡳ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠨࡷࠧၧ"), name, e)
    def bstack111l1llll_opy_(self, attrs):
        hook_name = getattr(attrs, bstack1ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪၨ"), None) or (hasattr(self, bstack1ll111_opy_ (u"ࠨࡡࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ၩ")) and self._11111l1ll1_opy_)
        bstack111111l1ll_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡉࡑࡒࡏࡘ࠭ၪ"), bstack1ll111_opy_ (u"ࠪࠫၫ")).split(bstack1ll111_opy_ (u"ࠫ࠱࠭ၬ"))
        if hook_name in bstack111111l1ll_opy_ and bstack111111l1ll_opy_ != [bstack1ll111_opy_ (u"ࠬ࠭ၭ")]:
            return
        bstack11111l11l1_opy_ = bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪၮ"), None)
        hook_data = self.tests[bstack11111l11l1_opy_][bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪၯ")]
        status = bstack1ll111_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣၰ")
        exception = None
        bstack11111ll111_opy_ = None
        if hook_data.name == bstack1ll111_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠧၱ"):
            self.bstack11111ll1l1_opy_.reset()
            bstack11111l1l1l_opy_ = self.tests[bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪၲ"), None)][bstack1ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧၳ")].result.result
            if bstack11111l1l1l_opy_ == bstack1ll111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧၴ"):
                if attrs.hook_failures == 1:
                    status = bstack1ll111_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨၵ")
                elif attrs.hook_failures == 2:
                    status = bstack1ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢၶ")
            elif attrs.aborted:
                status = bstack1ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣၷ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1ll111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭ၸ") and attrs.hook_failures == 1:
                status = bstack1ll111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥၹ")
            elif hasattr(attrs, bstack1ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫၺ")) and attrs.error_message:
                status = bstack1ll111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧၻ")
            bstack11111ll111_opy_, exception = self._11111l1l11_opy_(attrs)
        bstack111111llll_opy_ = Result(result=status, exception=exception, bstack11111ll1ll_opy_=[bstack11111ll111_opy_])
        hook_data.stop(time=current_time(), duration=0, result=bstack111111llll_opy_)
        TestHubHandler.send_run_event(bstack1ll111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨၼ"), self.tests[bstack11111l11l1_opy_][bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪၽ")])
        threading.current_thread().current_hook_uuid = None
    def _11111l1l11_opy_(self, attrs):
        try:
            import traceback
            bstack1ll111lll1_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11111ll111_opy_ = bstack1ll111lll1_opy_[-1] if bstack1ll111lll1_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࠧၾ"))
            bstack11111ll111_opy_ = None
            exception = None
        return bstack11111ll111_opy_, exception