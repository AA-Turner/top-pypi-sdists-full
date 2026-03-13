# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.test_data import bstack111111llll_opy_, TestData
from bstack_utils.bstack1lll1lll_opy_ import bstack11l11ll1l1_opy_
from bstack_utils.helper import bstack1l11l11l11_opy_, current_time, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack11111l1l11_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1ll1l1ll1l_opy_:
    def __init__(self):
        self.bstack11111ll1l1_opy_ = bstack11111l1l11_opy_(self.bstack111111l1l1_opy_)
        self.tests = {}
    @staticmethod
    def bstack111111l1l1_opy_(log):
        if not (log[bstack1111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨၚ")] and log[bstack1111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩၛ")].strip()):
            return
        active = bstack11l11ll1l1_opy_.bstack1111111lll_opy_()
        log = {
            bstack1111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨၜ"): log[bstack1111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩၝ")],
            bstack1111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧၞ"): current_time(),
            bstack1111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ၟ"): log[bstack1111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧၠ")],
        }
        if active:
            if active[bstack1111l_opy_ (u"ࠧࡵࡻࡳࡩࠬၡ")] == bstack1111l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ၢ"):
                log[bstack1111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩၣ")] = active[bstack1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪၤ")]
            elif active[bstack1111l_opy_ (u"ࠫࡹࡿࡰࡦࠩၥ")] == bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࠪၦ"):
                log[bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ၧ")] = active[bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧၨ")]
        TestHubHandler.bstack1l1l1111l_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack11111ll1l1_opy_.start()
        driver = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧၩ"), None)
        test_data = TestData(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=current_time(),
            file_path=attrs.feature.filename,
            result=bstack1111l_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥၪ"),
            framework=bstack1111l_opy_ (u"ࠪࡆࡪ࡮ࡡࡷࡧࠪၫ"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack11111ll1ll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧၬ")] = test_data
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.send_run_event(bstack1111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ၭ"), test_data)
    def end_test(self, attrs):
        bstack11111l11l1_opy_ = {
            bstack1111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦၮ"): attrs.feature.name,
            bstack1111l_opy_ (u"ࠢࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧၯ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        test_data = self.tests[current_test_uuid][bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫၰ")]
        meta = {
            bstack1111l_opy_ (u"ࠤࡩࡩࡦࡺࡵࡳࡧࠥၱ"): bstack11111l11l1_opy_,
            bstack1111l_opy_ (u"ࠥࡷࡹ࡫ࡰࡴࠤၲ"): test_data.meta.get(bstack1111l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪၳ"), []),
            bstack1111l_opy_ (u"ࠧࡹࡣࡦࡰࡤࡶ࡮ࡵࠢၴ"): {
                bstack1111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦၵ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        test_data.bstack11111l1l1l_opy_(meta)
        test_data.bstack111111ll11_opy_(bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬၶ"), []))
        bstack111111l11l_opy_, exception = self._11111ll111_opy_(attrs)
        status = bstack1111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨၷ") if attrs.status.name.lower() == bstack1111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨၸ") else attrs.status.name.lower()
        bstack11111l1lll_opy_ = Result(result=status, exception=exception, bstack11111l1111_opy_=[bstack111111l11l_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ၹ")].stop(time=current_time(), duration=int(attrs.duration)*1000, result=bstack11111l1lll_opy_)
        TestHubHandler.send_run_event(bstack1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ၺ"), self.tests[threading.current_thread().current_test_uuid][bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨၻ")])
    def bstack1ll1l111l_opy_(self, attrs):
        bstack111111l1ll_opy_ = {
            bstack1111l_opy_ (u"࠭ࡩࡥࠩၼ"): uuid4().__str__(),
            bstack1111l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨၽ"): attrs.keyword,
            bstack1111l_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨၾ"): [],
            bstack1111l_opy_ (u"ࠩࡷࡩࡽࡺࠧၿ"): attrs.name,
            bstack1111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧႀ"): current_time(),
            bstack1111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫႁ"): bstack1111l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ႂ"),
            bstack1111l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫႃ"): bstack1111l_opy_ (u"ࠧࠨႄ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫႅ")].add_step(bstack111111l1ll_opy_)
        threading.current_thread().current_step_uuid = bstack111111l1ll_opy_[bstack1111l_opy_ (u"ࠩ࡬ࡨࠬႆ")]
    def bstack1lll1l1l_opy_(self, attrs):
        current_test_id = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧႇ"), None)
        current_step_uuid = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨႈ"), None)
        bstack111111l11l_opy_, exception = self._11111ll111_opy_(attrs)
        status = bstack1111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬႉ") if attrs.status.name.lower() == bstack1111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬႊ") else attrs.status.name.lower()
        bstack11111l1lll_opy_ = Result(result=status, exception=exception, bstack11111l1111_opy_=[bstack111111l11l_opy_])
        self.tests[current_test_id][bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪႋ")].bstack11111ll11l_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11111l1lll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11l111l1l_opy_(self, name, attrs):
        try:
            bstack11111l1ll1_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡈࡐࡑࡎࡗࠬႌ"), bstack1111l_opy_ (u"ႍࠩࠪ")).split(bstack1111l_opy_ (u"ࠪ࠰ࠬႎ"))
            if name in bstack11111l1ll1_opy_ and bstack11111l1ll1_opy_ != [bstack1111l_opy_ (u"ࠫࠬႏ")]:
                return
            bstack11111l111l_opy_ = uuid4().__str__()
            self.tests[bstack11111l111l_opy_] = {}
            self.bstack11111ll1l1_opy_.start()
            scopes = []
            driver = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ႐"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ႑")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11111l111l_opy_)
            if name in [bstack1111l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ႒"), bstack1111l_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦ႓")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1111l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥ႔"), bstack1111l_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠥ႕")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1111l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬ႖")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111111llll_opy_(
                name=name,
                uuid=bstack11111l111l_opy_,
                started_at=current_time(),
                file_path=file_path,
                framework=bstack1111l_opy_ (u"ࠧࡈࡥࡩࡣࡹࡩࠧ႗"),
                integrations=TestHubHandler.bstack11111ll1ll_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1111l_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢ႘"),
                hook_type=name
            )
            self.tests[bstack11111l111l_opy_][bstack1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡡࡵࡣࠥ႙")] = hook_data
            current_test_id = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠣࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧႚ"), None)
            if current_test_id:
                hook_data.bstack111111lll1_opy_(current_test_id)
            if name == bstack1111l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨႛ"):
                threading.current_thread().before_all_hook_uuid = bstack11111l111l_opy_
            threading.current_thread().current_hook_uuid = bstack11111l111l_opy_
            TestHubHandler.send_run_event(bstack1111l_opy_ (u"ࠥࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠦႜ"), hook_data)
        except Exception as e:
            logger.debug(bstack1111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠࡩࡱࡲ࡯ࠥ࡫ࡶࡦࡰࡷࡷ࠱ࠦࡨࡰࡱ࡮ࠤࡳࡧ࡭ࡦ࠼ࠣࠩࡸ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠦࡵࠥႝ"), name, e)
    def bstack1ll11lllll_opy_(self, attrs):
        hook_name = getattr(attrs, bstack1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ႞"), None) or (hasattr(self, bstack1111l_opy_ (u"࠭࡟ࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ႟")) and self._11111l11ll_opy_)
        bstack11111l1ll1_opy_ = os.environ.get(bstack1111l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡉࡋࡆࡂࡗࡏࡘࡤࡎࡏࡐࡍࡖࠫႠ"), bstack1111l_opy_ (u"ࠨࠩႡ")).split(bstack1111l_opy_ (u"ࠩ࠯ࠫႢ"))
        if hook_name in bstack11111l1ll1_opy_ and bstack11111l1ll1_opy_ != [bstack1111l_opy_ (u"ࠪࠫႣ")]:
            return
        bstack111111l111_opy_ = bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨႤ"), None)
        hook_data = self.tests[bstack111111l111_opy_][bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨႥ")]
        status = bstack1111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨႦ")
        exception = None
        bstack111111l11l_opy_ = None
        if hook_data.name == bstack1111l_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠥႧ"):
            self.bstack11111ll1l1_opy_.reset()
            bstack111111ll1l_opy_ = self.tests[bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨႨ"), None)][bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬႩ")].result.result
            if bstack111111ll1l_opy_ == bstack1111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥႪ"):
                if attrs.hook_failures == 1:
                    status = bstack1111l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦႫ")
                elif attrs.hook_failures == 2:
                    status = bstack1111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧႬ")
            elif attrs.aborted:
                status = bstack1111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨႭ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1111l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫႮ") and attrs.hook_failures == 1:
                status = bstack1111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣႯ")
            elif hasattr(attrs, bstack1111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡠ࡯ࡨࡷࡸࡧࡧࡦࠩႰ")) and attrs.error_message:
                status = bstack1111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥႱ")
            bstack111111l11l_opy_, exception = self._11111ll111_opy_(attrs)
        bstack11111l1lll_opy_ = Result(result=status, exception=exception, bstack11111l1111_opy_=[bstack111111l11l_opy_])
        hook_data.stop(time=current_time(), duration=0, result=bstack11111l1lll_opy_)
        TestHubHandler.send_run_event(bstack1111l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ⴒ"), self.tests[bstack111111l111_opy_][bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨႳ")])
        threading.current_thread().current_hook_uuid = None
    def _11111ll111_opy_(self, attrs):
        try:
            import traceback
            bstack1llllll111_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111111l11l_opy_ = bstack1llllll111_opy_[-1] if bstack1llllll111_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡶࡸࡴࡳࠠࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࠥႴ"))
            bstack111111l11l_opy_ = None
            exception = None
        return bstack111111l11l_opy_, exception