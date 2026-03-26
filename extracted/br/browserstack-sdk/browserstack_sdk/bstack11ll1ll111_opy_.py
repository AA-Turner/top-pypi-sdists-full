# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.test_data import bstack1lllll1l111_opy_, TestData
from bstack_utils.bstack1l11111l1_opy_ import bstack11llll1l_opy_
from bstack_utils.helper import bstack1l11lll1_opy_, current_time, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack1lllll11l1l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11ll1ll111_opy_:
    def __init__(self):
        self.bstack1lllll1ll11_opy_ = bstack1lllll11l1l_opy_(self.bstack1lllll11l11_opy_)
        self.tests = {}
    @staticmethod
    def bstack1lllll11l11_opy_(log):
        if not (log[bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬႝ")] and log[bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭႞")].strip()):
            return
        active = bstack11llll1l_opy_.bstack1llll1lll11_opy_()
        log = {
            bstack1ll1lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ႟"): log[bstack1ll1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ⴀ")],
            bstack1ll1lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫႡ"): current_time(),
            bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪႢ"): log[bstack1ll1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫႣ")],
        }
        if active:
            if active[bstack1ll1lll_opy_ (u"ࠫࡹࡿࡰࡦࠩႤ")] == bstack1ll1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪႥ"):
                log[bstack1ll1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ⴆ")] = active[bstack1ll1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧႧ")]
            elif active[bstack1ll1lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭Ⴈ")] == bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࠧႩ"):
                log[bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪႪ")] = active[bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫႫ")]
        TestHubHandler.bstack11111l1l1l_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1lllll1ll11_opy_.start()
        driver = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫႬ"), None)
        test_data = TestData(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=current_time(),
            file_path=attrs.feature.filename,
            result=bstack1ll1lll_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢႭ"),
            framework=bstack1ll1lll_opy_ (u"ࠧࡃࡧ࡫ࡥࡻ࡫ࠧႮ"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack1lllll1l11l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫႯ")] = test_data
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.send_run_event(bstack1ll1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪႰ"), test_data)
    def end_test(self, attrs):
        bstack1llll1lllll_opy_ = {
            bstack1ll1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣႱ"): attrs.feature.name,
            bstack1ll1lll_opy_ (u"ࠦࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤႲ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        test_data = self.tests[current_test_uuid][bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨႳ")]
        meta = {
            bstack1ll1lll_opy_ (u"ࠨࡦࡦࡣࡷࡹࡷ࡫ࠢႴ"): bstack1llll1lllll_opy_,
            bstack1ll1lll_opy_ (u"ࠢࡴࡶࡨࡴࡸࠨႵ"): test_data.meta.get(bstack1ll1lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧႶ"), []),
            bstack1ll1lll_opy_ (u"ࠤࡶࡧࡪࡴࡡࡳ࡫ࡲࠦႷ"): {
                bstack1ll1lll_opy_ (u"ࠥࡲࡦࡳࡥࠣႸ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        test_data.bstack1lllll1llll_opy_(meta)
        test_data.bstack1lllll1ll1l_opy_(bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩႹ"), []))
        bstack1lllll1l1ll_opy_, exception = self._1lllll1111l_opy_(attrs)
        status = bstack1ll1lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬႺ") if attrs.status.name.lower() == bstack1ll1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬႻ") else attrs.status.name.lower()
        bstack1lllll11111_opy_ = Result(result=status, exception=exception, bstack1llll1llll1_opy_=[bstack1lllll1l1ll_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪႼ")].stop(time=current_time(), duration=int(attrs.duration)*1000, result=bstack1lllll11111_opy_)
        TestHubHandler.send_run_event(bstack1ll1lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪႽ"), self.tests[threading.current_thread().current_test_uuid][bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬႾ")])
    def bstack111ll11l11_opy_(self, attrs):
        bstack1llll1lll1l_opy_ = {
            bstack1ll1lll_opy_ (u"ࠪ࡭ࡩ࠭Ⴟ"): uuid4().__str__(),
            bstack1ll1lll_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬჀ"): attrs.keyword,
            bstack1ll1lll_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬჁ"): [],
            bstack1ll1lll_opy_ (u"࠭ࡴࡦࡺࡷࠫჂ"): attrs.name,
            bstack1ll1lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫჃ"): current_time(),
            bstack1ll1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨჄ"): bstack1ll1lll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪჅ"),
            bstack1ll1lll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ჆"): bstack1ll1lll_opy_ (u"ࠫࠬჇ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ჈")].add_step(bstack1llll1lll1l_opy_)
        threading.current_thread().current_step_uuid = bstack1llll1lll1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩ჉")]
    def bstack1l1l1ll111_opy_(self, attrs):
        current_test_id = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ჊"), None)
        current_step_uuid = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬ჋"), None)
        bstack1lllll1l1ll_opy_, exception = self._1lllll1111l_opy_(attrs)
        status = bstack1ll1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ჌") if attrs.status.name.lower() == bstack1ll1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩჍ") else attrs.status.name.lower()
        bstack1lllll11111_opy_ = Result(result=status, exception=exception, bstack1llll1llll1_opy_=[bstack1lllll1l1ll_opy_])
        self.tests[current_test_id][bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ჎")].bstack1lllll11ll1_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1lllll11111_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack111l1l11_opy_(self, name, attrs):
        try:
            bstack1lllll1lll1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤ࡙ࡄࡌࡡࡇࡉࡋࡇࡕࡍࡖࡢࡌࡔࡕࡋࡔࠩ჏"), bstack1ll1lll_opy_ (u"࠭ࠧა")).split(bstack1ll1lll_opy_ (u"ࠧ࠭ࠩბ"))
            if name in bstack1lllll1lll1_opy_ and bstack1lllll1lll1_opy_ != [bstack1ll1lll_opy_ (u"ࠨࠩგ")]:
                return
            bstack1llllll1111_opy_ = uuid4().__str__()
            self.tests[bstack1llllll1111_opy_] = {}
            self.bstack1lllll1ll11_opy_.start()
            scopes = []
            driver = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨდ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1ll1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨე")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1llllll1111_opy_)
            if name in [bstack1ll1lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣვ"), bstack1ll1lll_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣზ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1ll1lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢთ"), bstack1ll1lll_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠢი")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1ll1lll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩკ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1lllll1l111_opy_(
                name=name,
                uuid=bstack1llllll1111_opy_,
                started_at=current_time(),
                file_path=file_path,
                framework=bstack1ll1lll_opy_ (u"ࠤࡅࡩ࡭ࡧࡶࡦࠤლ"),
                integrations=TestHubHandler.bstack1lllll1l11l_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1ll1lll_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦმ"),
                hook_type=name
            )
            self.tests[bstack1llllll1111_opy_][bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠢნ")] = hook_data
            current_test_id = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤო"), None)
            if current_test_id:
                hook_data.bstack1lllll111l1_opy_(current_test_id)
            if name == bstack1ll1lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥპ"):
                threading.current_thread().before_all_hook_uuid = bstack1llllll1111_opy_
            threading.current_thread().current_hook_uuid = bstack1llllll1111_opy_
            TestHubHandler.send_run_event(bstack1ll1lll_opy_ (u"ࠢࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠣჟ"), hook_data)
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤ࡭ࡵ࡯࡬ࠢࡨࡺࡪࡴࡴࡴ࠮ࠣ࡬ࡴࡵ࡫ࠡࡰࡤࡱࡪࡀࠠࠦࡵ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠪࡹࠢრ"), name, e)
    def bstack111lll111l_opy_(self, attrs):
        hook_name = getattr(attrs, bstack1ll1lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬს"), None) or (hasattr(self, bstack1ll1lll_opy_ (u"ࠪࡣࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨტ")) and self._1lllll111ll_opy_)
        bstack1lllll1lll1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡘࡊࡋࡠࡆࡈࡊࡆ࡛ࡌࡕࡡࡋࡓࡔࡑࡓࠨუ"), bstack1ll1lll_opy_ (u"ࠬ࠭ფ")).split(bstack1ll1lll_opy_ (u"࠭ࠬࠨქ"))
        if hook_name in bstack1lllll1lll1_opy_ and bstack1lllll1lll1_opy_ != [bstack1ll1lll_opy_ (u"ࠧࠨღ")]:
            return
        bstack1lllll1l1l1_opy_ = bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬყ"), None)
        hook_data = self.tests[bstack1lllll1l1l1_opy_][bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬშ")]
        status = bstack1ll1lll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥჩ")
        exception = None
        bstack1lllll1l1ll_opy_ = None
        if hook_data.name == bstack1ll1lll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠢც"):
            self.bstack1lllll1ll11_opy_.reset()
            bstack1lllll11lll_opy_ = self.tests[bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬძ"), None)][bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩწ")].result.result
            if bstack1lllll11lll_opy_ == bstack1ll1lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢჭ"):
                if attrs.hook_failures == 1:
                    status = bstack1ll1lll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣხ")
                elif attrs.hook_failures == 2:
                    status = bstack1ll1lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤჯ")
            elif attrs.aborted:
                status = bstack1ll1lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥჰ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1ll1lll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠨჱ") and attrs.hook_failures == 1:
                status = bstack1ll1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧჲ")
            elif hasattr(attrs, bstack1ll1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࡤࡳࡥࡴࡵࡤ࡫ࡪ࠭ჳ")) and attrs.error_message:
                status = bstack1ll1lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢჴ")
            bstack1lllll1l1ll_opy_, exception = self._1lllll1111l_opy_(attrs)
        bstack1lllll11111_opy_ = Result(result=status, exception=exception, bstack1llll1llll1_opy_=[bstack1lllll1l1ll_opy_])
        hook_data.stop(time=current_time(), duration=0, result=bstack1lllll11111_opy_)
        TestHubHandler.send_run_event(bstack1ll1lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪჵ"), self.tests[bstack1lllll1l1l1_opy_][bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬჶ")])
        threading.current_thread().current_hook_uuid = None
    def _1lllll1111l_opy_(self, attrs):
        try:
            import traceback
            bstack1111l11l1l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1lllll1l1ll_opy_ = bstack1111l11l1l_opy_[-1] if bstack1111l11l1l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1ll1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡨࡻࡳࡵࡱࡰࠤࡹࡸࡡࡤࡧࡥࡥࡨࡱࠢჷ"))
            bstack1lllll1l1ll_opy_ = None
            exception = None
        return bstack1lllll1l1ll_opy_, exception