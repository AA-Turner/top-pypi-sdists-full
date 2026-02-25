# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.test_data import bstack1111l11lll_opy_, TestData
from bstack_utils.bstack1111lll11l_opy_ import bstack1l111111_opy_
from bstack_utils.helper import bstack11llll11l1_opy_, current_time, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack1111l1lll1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l111l1ll_opy_:
    def __init__(self):
        self.bstack1111ll1lll_opy_ = bstack1111l1lll1_opy_(self.bstack1111l1l11l_opy_)
        self.tests = {}
    @staticmethod
    def bstack1111l1l11l_opy_(log):
        if not (log[bstack11l1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ྷ")] and log[bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྸ")].strip()):
            return
        active = bstack1l111111_opy_.bstack1111l1l1l1_opy_()
        log = {
            bstack11l1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ྐྵ"): log[bstack11l1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧྺ")],
            bstack11l1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬྻ"): current_time(),
            bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྼ"): log[bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ྽")],
        }
        if active:
            if active[bstack11l1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪ྾")] == bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ྿"):
                log[bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ࿀")] = active[bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ࿁")]
            elif active[bstack11l1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ࿂")] == bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࠨ࿃"):
                log[bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ࿄")] = active[bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ࿅")]
        TestHubHandler.bstack1l111ll1_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1111ll1lll_opy_.start()
        driver = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶ࿆ࠬ"), None)
        test_data = TestData(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=current_time(),
            file_path=attrs.feature.filename,
            result=bstack11l1l11_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣ࿇"),
            framework=bstack11l1l11_opy_ (u"ࠨࡄࡨ࡬ࡦࡼࡥࠨ࿈"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack1111ll1ll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿉")] = test_data
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.send_run_event(bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ࿊"), test_data)
    def end_test(self, attrs):
        bstack1111ll1111_opy_ = {
            bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ࿋"): attrs.feature.name,
            bstack11l1l11_opy_ (u"ࠧࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥ࿌"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        test_data = self.tests[current_test_uuid][bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿍")]
        meta = {
            bstack11l1l11_opy_ (u"ࠢࡧࡧࡤࡸࡺࡸࡥࠣ࿎"): bstack1111ll1111_opy_,
            bstack11l1l11_opy_ (u"ࠣࡵࡷࡩࡵࡹࠢ࿏"): test_data.meta.get(bstack11l1l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ࿐"), []),
            bstack11l1l11_opy_ (u"ࠥࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ࿑"): {
                bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ࿒"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        test_data.bstack1111lll111_opy_(meta)
        test_data.bstack1111ll1l11_opy_(bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ࿓"), []))
        bstack1111ll111l_opy_, exception = self._1111ll11ll_opy_(attrs)
        status = bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭࿔") if attrs.status.name.lower() == bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭࿕") else attrs.status.name.lower()
        bstack1111lll1ll_opy_ = Result(result=status, exception=exception, bstack1111l11ll1_opy_=[bstack1111ll111l_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿖")].stop(time=current_time(), duration=int(attrs.duration)*1000, result=bstack1111lll1ll_opy_)
        TestHubHandler.send_run_event(bstack11l1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ࿗"), self.tests[threading.current_thread().current_test_uuid][bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿘")])
    def bstack1lll11111l_opy_(self, attrs):
        bstack1111l1l1ll_opy_ = {
            bstack11l1l11_opy_ (u"ࠫ࡮ࡪࠧ࿙"): uuid4().__str__(),
            bstack11l1l11_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭࿚"): attrs.keyword,
            bstack11l1l11_opy_ (u"࠭ࡳࡵࡧࡳࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭࿛"): [],
            bstack11l1l11_opy_ (u"ࠧࡵࡧࡻࡸࠬ࿜"): attrs.name,
            bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ࿝"): current_time(),
            bstack11l1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ࿞"): bstack11l1l11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ࿟"),
            bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ࿠"): bstack11l1l11_opy_ (u"ࠬ࠭࿡")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿢")].add_step(bstack1111l1l1ll_opy_)
        threading.current_thread().current_step_uuid = bstack1111l1l1ll_opy_[bstack11l1l11_opy_ (u"ࠧࡪࡦࠪ࿣")]
    def bstack11l1ll1l1l_opy_(self, attrs):
        current_test_id = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ࿤"), None)
        current_step_uuid = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭࿥"), None)
        bstack1111ll111l_opy_, exception = self._1111ll11ll_opy_(attrs)
        status = bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ࿦") if attrs.status.name.lower() == bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ࿧") else attrs.status.name.lower()
        bstack1111lll1ll_opy_ = Result(result=status, exception=exception, bstack1111l11ll1_opy_=[bstack1111ll111l_opy_])
        self.tests[current_test_id][bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿨")].bstack1111l1llll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1111lll1ll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l1ll11l_opy_(self, name, attrs):
        try:
            bstack1111lll1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡓࡅࡍࡢࡈࡊࡌࡁࡖࡎࡗࡣࡍࡕࡏࡌࡕࠪ࿩"), bstack11l1l11_opy_ (u"ࠧࠨ࿪")).split(bstack11l1l11_opy_ (u"ࠨ࠮ࠪ࿫"))
            if name in bstack1111lll1l1_opy_ and bstack1111lll1l1_opy_ != [bstack11l1l11_opy_ (u"ࠩࠪ࿬")]:
                return
            bstack1111l1l111_opy_ = uuid4().__str__()
            self.tests[bstack1111l1l111_opy_] = {}
            self.bstack1111ll1lll_opy_.start()
            scopes = []
            driver = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ࿭"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ࿮")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1111l1l111_opy_)
            if name in [bstack11l1l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ࿯"), bstack11l1l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ࿰")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack11l1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ࿱"), bstack11l1l11_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠣ࿲")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack11l1l11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ࿳")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1111l11lll_opy_(
                name=name,
                uuid=bstack1111l1l111_opy_,
                started_at=current_time(),
                file_path=file_path,
                framework=bstack11l1l11_opy_ (u"ࠥࡆࡪ࡮ࡡࡷࡧࠥ࿴"),
                integrations=TestHubHandler.bstack1111ll1ll1_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack11l1l11_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ࿵"),
                hook_type=name
            )
            self.tests[bstack1111l1l111_opy_][bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡦࡺࡡࠣ࿶")] = hook_data
            current_test_id = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥ࿷"), None)
            if current_test_id:
                hook_data.bstack1111ll11l1_opy_(current_test_id)
            if name == bstack11l1l11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ࿸"):
                threading.current_thread().before_all_hook_uuid = bstack1111l1l111_opy_
            threading.current_thread().current_hook_uuid = bstack1111l1l111_opy_
            TestHubHandler.send_run_event(bstack11l1l11_opy_ (u"ࠣࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤ࿹"), hook_data)
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥ࡮࡯ࡰ࡭ࠣࡩࡻ࡫࡮ࡵࡵ࠯ࠤ࡭ࡵ࡯࡬ࠢࡱࡥࡲ࡫࠺ࠡࠧࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠫࡳࠣ࿺"), name, e)
    def bstack1l1l1ll1_opy_(self, attrs):
        hook_name = getattr(attrs, bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭࿻"), None) or (hasattr(self, bstack11l1l11_opy_ (u"ࠫࡤࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ࿼")) and self._1111ll1l1l_opy_)
        bstack1111lll1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤ࡙ࡄࡌࡡࡇࡉࡋࡇࡕࡍࡖࡢࡌࡔࡕࡋࡔࠩ࿽"), bstack11l1l11_opy_ (u"࠭ࠧ࿾")).split(bstack11l1l11_opy_ (u"ࠧ࠭ࠩ࿿"))
        if hook_name in bstack1111lll1l1_opy_ and bstack1111lll1l1_opy_ != [bstack11l1l11_opy_ (u"ࠨࠩက")]:
            return
        bstack1111l1ll11_opy_ = bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ခ"), None)
        hook_data = self.tests[bstack1111l1ll11_opy_][bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ဂ")]
        status = bstack11l1l11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦဃ")
        exception = None
        bstack1111ll111l_opy_ = None
        if hook_data.name == bstack11l1l11_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣင"):
            self.bstack1111ll1lll_opy_.reset()
            bstack1111l1ll1l_opy_ = self.tests[bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭စ"), None)][bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪဆ")].result.result
            if bstack1111l1ll1l_opy_ == bstack11l1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣဇ"):
                if attrs.hook_failures == 1:
                    status = bstack11l1l11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤဈ")
                elif attrs.hook_failures == 2:
                    status = bstack11l1l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥဉ")
            elif attrs.aborted:
                status = bstack11l1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦည")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11l1l11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩဋ") and attrs.hook_failures == 1:
                status = bstack11l1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨဌ")
            elif hasattr(attrs, bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧဍ")) and attrs.error_message:
                status = bstack11l1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣဎ")
            bstack1111ll111l_opy_, exception = self._1111ll11ll_opy_(attrs)
        bstack1111lll1ll_opy_ = Result(result=status, exception=exception, bstack1111l11ll1_opy_=[bstack1111ll111l_opy_])
        hook_data.stop(time=current_time(), duration=0, result=bstack1111lll1ll_opy_)
        TestHubHandler.send_run_event(bstack11l1l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫဏ"), self.tests[bstack1111l1ll11_opy_][bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭တ")])
        threading.current_thread().current_hook_uuid = None
    def _1111ll11ll_opy_(self, attrs):
        try:
            import traceback
            bstack1lll1ll11l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1111ll111l_opy_ = bstack1lll1ll11l_opy_[-1] if bstack1lll1ll11l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11l1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡴࡶࡲࡱࠥࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࠣထ"))
            bstack1111ll111l_opy_ = None
            exception = None
        return bstack1111ll111l_opy_, exception