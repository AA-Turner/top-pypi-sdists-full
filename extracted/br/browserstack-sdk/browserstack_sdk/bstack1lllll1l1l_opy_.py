# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.test_data import bstack1111ll1l11_opy_, TestData
from bstack_utils.bstack1111ll1111_opy_ import bstack111lllll1_opy_
from bstack_utils.helper import bstack1lll111ll_opy_, current_time, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack1111l1l11l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1lllll1l1l_opy_:
    def __init__(self):
        self.bstack1111ll11l1_opy_ = bstack1111l1l11l_opy_(self.bstack1111ll1l1l_opy_)
        self.tests = {}
    @staticmethod
    def bstack1111ll1l1l_opy_(log):
        if not (log[bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྻ")] and log[bstack1lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྼ")].strip()):
            return
        active = bstack111lllll1_opy_.bstack1111l111ll_opy_()
        log = {
            bstack1lll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ྽"): log[bstack1lll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ྾")],
            bstack1lll1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ྿"): current_time(),
            bstack1lll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿀"): log[bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿁")],
        }
        if active:
            if active[bstack1lll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ࿂")] == bstack1lll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ࿃"):
                log[bstack1lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ࿄")] = active[bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ࿅")]
            elif active[bstack1lll1l_opy_ (u"࠭ࡴࡺࡲࡨ࿆ࠫ")] == bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࠬ࿇"):
                log[bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ࿈")] = active[bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ࿉")]
        TestHubHandler.bstack11ll1l1l11_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1111ll11l1_opy_.start()
        driver = bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ࿊"), None)
        test_data = TestData(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=current_time(),
            file_path=attrs.feature.filename,
            result=bstack1lll1l_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ࿋"),
            framework=bstack1lll1l_opy_ (u"ࠬࡈࡥࡩࡣࡹࡩࠬ࿌"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack1111l11ll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿍")] = test_data
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.send_run_event(bstack1lll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ࿎"), test_data)
    def end_test(self, attrs):
        bstack1111l11l11_opy_ = {
            bstack1lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨ࿏"): attrs.feature.name,
            bstack1lll1l_opy_ (u"ࠤࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢ࿐"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        test_data = self.tests[current_test_uuid][bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿑")]
        meta = {
            bstack1lll1l_opy_ (u"ࠦ࡫࡫ࡡࡵࡷࡵࡩࠧ࿒"): bstack1111l11l11_opy_,
            bstack1lll1l_opy_ (u"ࠧࡹࡴࡦࡲࡶࠦ࿓"): test_data.meta.get(bstack1lll1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ࿔"), []),
            bstack1lll1l_opy_ (u"ࠢࡴࡥࡨࡲࡦࡸࡩࡰࠤ࿕"): {
                bstack1lll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨ࿖"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        test_data.bstack1111ll111l_opy_(meta)
        test_data.bstack1111l111l1_opy_(bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ࿗"), []))
        bstack1111l1llll_opy_, exception = self._1111l1lll1_opy_(attrs)
        status = bstack1lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ࿘") if attrs.status.name.lower() == bstack1lll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ࿙") else attrs.status.name.lower()
        bstack1111l1ll11_opy_ = Result(result=status, exception=exception, bstack1111l1ll1l_opy_=[bstack1111l1llll_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿚")].stop(time=current_time(), duration=int(attrs.duration)*1000, result=bstack1111l1ll11_opy_)
        TestHubHandler.send_run_event(bstack1lll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ࿛"), self.tests[threading.current_thread().current_test_uuid][bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ࿜")])
    def bstack111ll1llll_opy_(self, attrs):
        bstack1111l1l1l1_opy_ = {
            bstack1lll1l_opy_ (u"ࠨ࡫ࡧࠫ࿝"): uuid4().__str__(),
            bstack1lll1l_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪ࿞"): attrs.keyword,
            bstack1lll1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪ࿟"): [],
            bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ࿠"): attrs.name,
            bstack1lll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ࿡"): current_time(),
            bstack1lll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭࿢"): bstack1lll1l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ࿣"),
            bstack1lll1l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭࿤"): bstack1lll1l_opy_ (u"ࠩࠪ࿥")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿦")].add_step(bstack1111l1l1l1_opy_)
        threading.current_thread().current_step_uuid = bstack1111l1l1l1_opy_[bstack1lll1l_opy_ (u"ࠫ࡮ࡪࠧ࿧")]
    def bstack11llllllll_opy_(self, attrs):
        current_test_id = bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ࿨"), None)
        current_step_uuid = bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪ࿩"), None)
        bstack1111l1llll_opy_, exception = self._1111l1lll1_opy_(attrs)
        status = bstack1lll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ࿪") if attrs.status.name.lower() == bstack1lll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ࿫") else attrs.status.name.lower()
        bstack1111l1ll11_opy_ = Result(result=status, exception=exception, bstack1111l1ll1l_opy_=[bstack1111l1llll_opy_])
        self.tests[current_test_id][bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿬")].bstack1111ll1ll1_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1111l1ll11_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11111l11_opy_(self, name, attrs):
        try:
            bstack1111l1111l_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡗࡉࡑ࡟ࡅࡇࡉࡅ࡚ࡒࡔࡠࡊࡒࡓࡐ࡙ࠧ࿭"), bstack1lll1l_opy_ (u"ࠫࠬ࿮")).split(bstack1lll1l_opy_ (u"ࠬ࠲ࠧ࿯"))
            if name in bstack1111l1111l_opy_ and bstack1111l1111l_opy_ != [bstack1lll1l_opy_ (u"࠭ࠧ࿰")]:
                return
            bstack1111l11lll_opy_ = uuid4().__str__()
            self.tests[bstack1111l11lll_opy_] = {}
            self.bstack1111ll11l1_opy_.start()
            scopes = []
            driver = bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭࿱"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1lll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭࿲")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1111l11lll_opy_)
            if name in [bstack1lll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ࿳"), bstack1lll1l_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨ࿴")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1lll1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ࿵"), bstack1lll1l_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠧ࿶")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1lll1l_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧ࿷")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1111ll1l11_opy_(
                name=name,
                uuid=bstack1111l11lll_opy_,
                started_at=current_time(),
                file_path=file_path,
                framework=bstack1lll1l_opy_ (u"ࠢࡃࡧ࡫ࡥࡻ࡫ࠢ࿸"),
                integrations=TestHubHandler.bstack1111l11ll1_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1lll1l_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤ࿹"),
                hook_type=name
            )
            self.tests[bstack1111l11lll_opy_][bstack1lll1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠧ࿺")] = hook_data
            current_test_id = bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠥࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠢ࿻"), None)
            if current_test_id:
                hook_data.bstack1111ll11ll_opy_(current_test_id)
            if name == bstack1lll1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ࿼"):
                threading.current_thread().before_all_hook_uuid = bstack1111l11lll_opy_
            threading.current_thread().current_hook_uuid = bstack1111l11lll_opy_
            TestHubHandler.send_run_event(bstack1lll1l_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩࠨ࿽"), hook_data)
        except Exception as e:
            logger.debug(bstack1lll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡪࡰࠣࡷࡹࡧࡲࡵࠢ࡫ࡳࡴࡱࠠࡦࡸࡨࡲࡹࡹࠬࠡࡪࡲࡳࡰࠦ࡮ࡢ࡯ࡨ࠾ࠥࠫࡳ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠨࡷࠧ࿾"), name, e)
    def bstack1l11l1111_opy_(self, attrs):
        hook_name = getattr(attrs, bstack1lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪ࿿"), None) or (hasattr(self, bstack1lll1l_opy_ (u"ࠨࡡࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭က")) and self._1111l1l1ll_opy_)
        bstack1111l1111l_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡉࡑࡒࡏࡘ࠭ခ"), bstack1lll1l_opy_ (u"ࠪࠫဂ")).split(bstack1lll1l_opy_ (u"ࠫ࠱࠭ဃ"))
        if hook_name in bstack1111l1111l_opy_ and bstack1111l1111l_opy_ != [bstack1lll1l_opy_ (u"ࠬ࠭င")]:
            return
        bstack1111l1l111_opy_ = bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪစ"), None)
        hook_data = self.tests[bstack1111l1l111_opy_][bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪဆ")]
        status = bstack1lll1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣဇ")
        exception = None
        bstack1111l1llll_opy_ = None
        if hook_data.name == bstack1lll1l_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠧဈ"):
            self.bstack1111ll11l1_opy_.reset()
            bstack1111l11l1l_opy_ = self.tests[bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪဉ"), None)][bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧည")].result.result
            if bstack1111l11l1l_opy_ == bstack1lll1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧဋ"):
                if attrs.hook_failures == 1:
                    status = bstack1lll1l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨဌ")
                elif attrs.hook_failures == 2:
                    status = bstack1lll1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢဍ")
            elif attrs.aborted:
                status = bstack1lll1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣဎ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1lll1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱ࠭ဏ") and attrs.hook_failures == 1:
                status = bstack1lll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥတ")
            elif hasattr(attrs, bstack1lll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫထ")) and attrs.error_message:
                status = bstack1lll1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧဒ")
            bstack1111l1llll_opy_, exception = self._1111l1lll1_opy_(attrs)
        bstack1111l1ll11_opy_ = Result(result=status, exception=exception, bstack1111l1ll1l_opy_=[bstack1111l1llll_opy_])
        hook_data.stop(time=current_time(), duration=0, result=bstack1111l1ll11_opy_)
        TestHubHandler.send_run_event(bstack1lll1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨဓ"), self.tests[bstack1111l1l111_opy_][bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪန")])
        threading.current_thread().current_hook_uuid = None
    def _1111l1lll1_opy_(self, attrs):
        try:
            import traceback
            bstack1111l11ll_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1111l1llll_opy_ = bstack1111l11ll_opy_[-1] if bstack1111l11ll_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1lll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࠧပ"))
            bstack1111l1llll_opy_ = None
            exception = None
        return bstack1111l1llll_opy_, exception