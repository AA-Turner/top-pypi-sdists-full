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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.test_data import bstack1111ll11l1_opy_, TestData
from bstack_utils.bstack1111ll1l1l_opy_ import bstack11lll1ll1_opy_
from bstack_utils.helper import bstack1lll11l111_opy_, current_time, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack1111ll1l11_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1111111ll_opy_:
    def __init__(self):
        self.bstack1111l1l11l_opy_ = bstack1111ll1l11_opy_(self.bstack1111ll111l_opy_)
        self.tests = {}
    @staticmethod
    def bstack1111ll111l_opy_(log):
        if not (log[bstack11ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩླ")] and log[bstack11ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྴ")].strip()):
            return
        active = bstack11lll1ll1_opy_.bstack1111l1lll1_opy_()
        log = {
            bstack11ll111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩྵ"): log[bstack11ll111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪྶ")],
            bstack11ll111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨྷ"): current_time(),
            bstack11ll111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྸ"): log[bstack11ll111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྐྵ")],
        }
        if active:
            if active[bstack11ll111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ྺ")] == bstack11ll111_opy_ (u"ࠩ࡫ࡳࡴࡱࠧྻ"):
                log[bstack11ll111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪྼ")] = active[bstack11ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ྽")]
            elif active[bstack11ll111_opy_ (u"ࠬࡺࡹࡱࡧࠪ྾")] == bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࠫ྿"):
                log[bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ࿀")] = active[bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ࿁")]
        TestHubHandler.bstack1ll11l1ll_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1111l1l11l_opy_.start()
        driver = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ࿂"), None)
        test_data = TestData(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=current_time(),
            file_path=attrs.feature.filename,
            result=bstack11ll111_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦ࿃"),
            framework=bstack11ll111_opy_ (u"ࠫࡇ࡫ࡨࡢࡸࡨࠫ࿄"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack1111l11l1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿅")] = test_data
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.send_run_event(bstack11ll111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪ࿆ࠧ"), test_data)
    def end_test(self, attrs):
        bstack1111ll1111_opy_ = {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ࿇"): attrs.feature.name,
            bstack11ll111_opy_ (u"ࠣࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨ࿈"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        test_data = self.tests[current_test_uuid][bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿉")]
        meta = {
            bstack11ll111_opy_ (u"ࠥࡪࡪࡧࡴࡶࡴࡨࠦ࿊"): bstack1111ll1111_opy_,
            bstack11ll111_opy_ (u"ࠦࡸࡺࡥࡱࡵࠥ࿋"): test_data.meta.get(bstack11ll111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ࿌"), []),
            bstack11ll111_opy_ (u"ࠨࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ࿍"): {
                bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ࿎"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        test_data.bstack1111lll111_opy_(meta)
        test_data.bstack1111l1l1l1_opy_(bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭࿏"), []))
        bstack1111ll1ll1_opy_, exception = self._1111lll11l_opy_(attrs)
        status = bstack11ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ࿐") if attrs.status.name.lower() == bstack11ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ࿑") else attrs.status.name.lower()
        bstack1111l1ll1l_opy_ = Result(result=status, exception=exception, bstack1111ll1lll_opy_=[bstack1111ll1ll1_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࿒")].stop(time=current_time(), duration=int(attrs.duration)*1000, result=bstack1111l1ll1l_opy_)
        TestHubHandler.send_run_event(bstack11ll111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ࿓"), self.tests[threading.current_thread().current_test_uuid][bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿔")])
    def bstack11l11111l_opy_(self, attrs):
        bstack1111l1ll11_opy_ = {
            bstack11ll111_opy_ (u"ࠧࡪࡦࠪ࿕"): uuid4().__str__(),
            bstack11ll111_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩ࿖"): attrs.keyword,
            bstack11ll111_opy_ (u"ࠩࡶࡸࡪࡶ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠩ࿗"): [],
            bstack11ll111_opy_ (u"ࠪࡸࡪࡾࡴࠨ࿘"): attrs.name,
            bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ࿙"): current_time(),
            bstack11ll111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ࿚"): bstack11ll111_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ࿛"),
            bstack11ll111_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ࿜"): bstack11ll111_opy_ (u"ࠨࠩ࿝")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿞")].add_step(bstack1111l1ll11_opy_)
        threading.current_thread().current_step_uuid = bstack1111l1ll11_opy_[bstack11ll111_opy_ (u"ࠪ࡭ࡩ࠭࿟")]
    def bstack11l11l1l_opy_(self, attrs):
        current_test_id = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ࿠"), None)
        current_step_uuid = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩ࿡"), None)
        bstack1111ll1ll1_opy_, exception = self._1111lll11l_opy_(attrs)
        status = bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭࿢") if attrs.status.name.lower() == bstack11ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭࿣") else attrs.status.name.lower()
        bstack1111l1ll1l_opy_ = Result(result=status, exception=exception, bstack1111ll1lll_opy_=[bstack1111ll1ll1_opy_])
        self.tests[current_test_id][bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿤")].bstack1111l11lll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1111l1ll1l_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11l1lll11l_opy_(self, name, attrs):
        try:
            bstack1111l1l1ll_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡉࡑࡒࡏࡘ࠭࿥"), bstack11ll111_opy_ (u"ࠪࠫ࿦")).split(bstack11ll111_opy_ (u"ࠫ࠱࠭࿧"))
            if name in bstack1111l1l1ll_opy_ and bstack1111l1l1ll_opy_ != [bstack11ll111_opy_ (u"ࠬ࠭࿨")]:
                return
            bstack1111l11ll1_opy_ = uuid4().__str__()
            self.tests[bstack1111l11ll1_opy_] = {}
            self.bstack1111l1l11l_opy_.start()
            scopes = []
            driver = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ࿩"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack11ll111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ࿪")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1111l11ll1_opy_)
            if name in [bstack11ll111_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ࿫"), bstack11ll111_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠧ࿬")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack11ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ࿭"), bstack11ll111_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠦ࿮")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack11ll111_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭࿯")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1111ll11l1_opy_(
                name=name,
                uuid=bstack1111l11ll1_opy_,
                started_at=current_time(),
                file_path=file_path,
                framework=bstack11ll111_opy_ (u"ࠨࡂࡦࡪࡤࡺࡪࠨ࿰"),
                integrations=TestHubHandler.bstack1111l11l1l_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack11ll111_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣ࿱"),
                hook_type=name
            )
            self.tests[bstack1111l11ll1_opy_][bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡢࡶࡤࠦ࿲")] = hook_data
            current_test_id = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠤࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨ࿳"), None)
            if current_test_id:
                hook_data.bstack1111ll11ll_opy_(current_test_id)
            if name == bstack11ll111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ࿴"):
                threading.current_thread().before_all_hook_uuid = bstack1111l11ll1_opy_
            threading.current_thread().current_hook_uuid = bstack1111l11ll1_opy_
            TestHubHandler.send_run_event(bstack11ll111_opy_ (u"ࠦࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠧ࿵"), hook_data)
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࠡࡪࡲࡳࡰࠦࡥࡷࡧࡱࡸࡸ࠲ࠠࡩࡱࡲ࡯ࠥࡴࡡ࡮ࡧ࠽ࠤࠪࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠧࡶࠦ࿶"), name, e)
    def bstack111ll1l1l_opy_(self, attrs):
        hook_name = getattr(attrs, bstack11ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ࿷"), None) or (hasattr(self, bstack11ll111_opy_ (u"ࠧࡠࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ࿸")) and self._1111lll1l1_opy_)
        bstack1111l1l1ll_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡈࡐࡑࡎࡗࠬ࿹"), bstack11ll111_opy_ (u"ࠩࠪ࿺")).split(bstack11ll111_opy_ (u"ࠪ࠰ࠬ࿻"))
        if hook_name in bstack1111l1l1ll_opy_ and bstack1111l1l1ll_opy_ != [bstack11ll111_opy_ (u"ࠫࠬ࿼")]:
            return
        bstack1111l1l111_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ࿽"), None)
        hook_data = self.tests[bstack1111l1l111_opy_][bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿾")]
        status = bstack11ll111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ࿿")
        exception = None
        bstack1111ll1ll1_opy_ = None
        if hook_data.name == bstack11ll111_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦက"):
            self.bstack1111l1l11l_opy_.reset()
            bstack1111l1llll_opy_ = self.tests[bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩခ"), None)][bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ဂ")].result.result
            if bstack1111l1llll_opy_ == bstack11ll111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦဃ"):
                if attrs.hook_failures == 1:
                    status = bstack11ll111_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧင")
                elif attrs.hook_failures == 2:
                    status = bstack11ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨစ")
            elif attrs.aborted:
                status = bstack11ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢဆ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11ll111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬဇ") and attrs.hook_failures == 1:
                status = bstack11ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤဈ")
            elif hasattr(attrs, bstack11ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪဉ")) and attrs.error_message:
                status = bstack11ll111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦည")
            bstack1111ll1ll1_opy_, exception = self._1111lll11l_opy_(attrs)
        bstack1111l1ll1l_opy_ = Result(result=status, exception=exception, bstack1111ll1lll_opy_=[bstack1111ll1ll1_opy_])
        hook_data.stop(time=current_time(), duration=0, result=bstack1111l1ll1l_opy_)
        TestHubHandler.send_run_event(bstack11ll111_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧဋ"), self.tests[bstack1111l1l111_opy_][bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩဌ")])
        threading.current_thread().current_hook_uuid = None
    def _1111lll11l_opy_(self, attrs):
        try:
            import traceback
            bstack1l11ll1l1_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1111ll1ll1_opy_ = bstack1l11ll1l1_opy_[-1] if bstack1l11ll1l1_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11ll111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࠦဍ"))
            bstack1111ll1ll1_opy_ = None
            exception = None
        return bstack1111ll1ll1_opy_, exception