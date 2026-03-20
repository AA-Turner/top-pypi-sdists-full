# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.test_data import bstack1llllll111l_opy_, TestData
from bstack_utils.bstack1llll11l11_opy_ import bstack1ll1l1l1l1_opy_
from bstack_utils.helper import bstack111ll1ll_opy_, current_time, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack1llllllll1l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1lll1lll11_opy_:
    def __init__(self):
        self.bstack1llllll1l11_opy_ = bstack1llllllll1l_opy_(self.bstack1lllllll1ll_opy_)
        self.tests = {}
    @staticmethod
    def bstack1lllllll1ll_opy_(log):
        if not (log[bstack11lll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩႅ")] and log[bstack11lll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪႆ")].strip()):
            return
        active = bstack1ll1l1l1l1_opy_.bstack1lllll1ll11_opy_()
        log = {
            bstack11lll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩႇ"): log[bstack11lll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪႈ")],
            bstack11lll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨႉ"): current_time(),
            bstack11lll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧႊ"): log[bstack11lll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨႋ")],
        }
        if active:
            if active[bstack11lll1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ႌ")] == bstack11lll1_opy_ (u"ࠩ࡫ࡳࡴࡱႍࠧ"):
                log[bstack11lll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪႎ")] = active[bstack11lll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫႏ")]
            elif active[bstack11lll1_opy_ (u"ࠬࡺࡹࡱࡧࠪ႐")] == bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࠫ႑"):
                log[bstack11lll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ႒")] = active[bstack11lll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ႓")]
        TestHubHandler.bstack1l1111l1ll_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1llllll1l11_opy_.start()
        driver = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ႔"), None)
        test_data = TestData(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=current_time(),
            file_path=attrs.feature.filename,
            result=bstack11lll1_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦ႕"),
            framework=bstack11lll1_opy_ (u"ࠫࡇ࡫ࡨࡢࡸࡨࠫ႖"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack1llllll1ll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ႗")] = test_data
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.send_run_event(bstack11lll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ႘"), test_data)
    def end_test(self, attrs):
        bstack1llllllllll_opy_ = {
            bstack11lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ႙"): attrs.feature.name,
            bstack11lll1_opy_ (u"ࠣࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨႚ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        test_data = self.tests[current_test_uuid][bstack11lll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬႛ")]
        meta = {
            bstack11lll1_opy_ (u"ࠥࡪࡪࡧࡴࡶࡴࡨࠦႜ"): bstack1llllllllll_opy_,
            bstack11lll1_opy_ (u"ࠦࡸࡺࡥࡱࡵࠥႝ"): test_data.meta.get(bstack11lll1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ႞"), []),
            bstack11lll1_opy_ (u"ࠨࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ႟"): {
                bstack11lll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧႠ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        test_data.bstack1lllllll11l_opy_(meta)
        test_data.bstack1llllll1l1l_opy_(bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭Ⴁ"), []))
        bstack1lllllll111_opy_, exception = self._1lllllll1l1_opy_(attrs)
        status = bstack11lll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩႢ") if attrs.status.name.lower() == bstack11lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩႣ") else attrs.status.name.lower()
        bstack1lllll1ll1l_opy_ = Result(result=status, exception=exception, bstack1llllll11ll_opy_=[bstack1lllllll111_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧႤ")].stop(time=current_time(), duration=int(attrs.duration)*1000, result=bstack1lllll1ll1l_opy_)
        TestHubHandler.send_run_event(bstack11lll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧႥ"), self.tests[threading.current_thread().current_test_uuid][bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩႦ")])
    def bstack1ll11ll111_opy_(self, attrs):
        bstack1lllll1llll_opy_ = {
            bstack11lll1_opy_ (u"ࠧࡪࡦࠪႧ"): uuid4().__str__(),
            bstack11lll1_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩႨ"): attrs.keyword,
            bstack11lll1_opy_ (u"ࠩࡶࡸࡪࡶ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠩႩ"): [],
            bstack11lll1_opy_ (u"ࠪࡸࡪࡾࡴࠨႪ"): attrs.name,
            bstack11lll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨႫ"): current_time(),
            bstack11lll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬႬ"): bstack11lll1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧႭ"),
            bstack11lll1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬႮ"): bstack11lll1_opy_ (u"ࠨࠩႯ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11lll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬႰ")].add_step(bstack1lllll1llll_opy_)
        threading.current_thread().current_step_uuid = bstack1lllll1llll_opy_[bstack11lll1_opy_ (u"ࠪ࡭ࡩ࠭Ⴑ")]
    def bstack1l11111111_opy_(self, attrs):
        current_test_id = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨႲ"), None)
        current_step_uuid = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩႳ"), None)
        bstack1lllllll111_opy_, exception = self._1lllllll1l1_opy_(attrs)
        status = bstack11lll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ⴔ") if attrs.status.name.lower() == bstack11lll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭Ⴕ") else attrs.status.name.lower()
        bstack1lllll1ll1l_opy_ = Result(result=status, exception=exception, bstack1llllll11ll_opy_=[bstack1lllllll111_opy_])
        self.tests[current_test_id][bstack11lll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫႶ")].bstack1llllll11l1_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1lllll1ll1l_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11l1111ll_opy_(self, name, attrs):
        try:
            bstack1llllll1lll_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡉࡑࡒࡏࡘ࠭Ⴗ"), bstack11lll1_opy_ (u"ࠪࠫႸ")).split(bstack11lll1_opy_ (u"ࠫ࠱࠭Ⴙ"))
            if name in bstack1llllll1lll_opy_ and bstack1llllll1lll_opy_ != [bstack11lll1_opy_ (u"ࠬ࠭Ⴚ")]:
                return
            bstack1lllll1l1ll_opy_ = uuid4().__str__()
            self.tests[bstack1lllll1l1ll_opy_] = {}
            self.bstack1llllll1l11_opy_.start()
            scopes = []
            driver = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬႻ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack11lll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬႼ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1lllll1l1ll_opy_)
            if name in [bstack11lll1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧႽ"), bstack11lll1_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠧႾ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack11lll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦႿ"), bstack11lll1_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠦჀ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack11lll1_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭Ⴡ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1llllll111l_opy_(
                name=name,
                uuid=bstack1lllll1l1ll_opy_,
                started_at=current_time(),
                file_path=file_path,
                framework=bstack11lll1_opy_ (u"ࠨࡂࡦࡪࡤࡺࡪࠨჂ"),
                integrations=TestHubHandler.bstack1llllll1ll1_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack11lll1_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣჃ"),
                hook_type=name
            )
            self.tests[bstack1lllll1l1ll_opy_][bstack11lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡢࡶࡤࠦჄ")] = hook_data
            current_test_id = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠤࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨჅ"), None)
            if current_test_id:
                hook_data.bstack1llllll1111_opy_(current_test_id)
            if name == bstack11lll1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ჆"):
                threading.current_thread().before_all_hook_uuid = bstack1lllll1l1ll_opy_
            threading.current_thread().current_hook_uuid = bstack1lllll1l1ll_opy_
            TestHubHandler.send_run_event(bstack11lll1_opy_ (u"ࠦࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠧჇ"), hook_data)
        except Exception as e:
            logger.debug(bstack11lll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࠡࡪࡲࡳࡰࠦࡥࡷࡧࡱࡸࡸ࠲ࠠࡩࡱࡲ࡯ࠥࡴࡡ࡮ࡧ࠽ࠤࠪࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠧࡶࠦ჈"), name, e)
    def bstack1111ll1111_opy_(self, attrs):
        hook_name = getattr(attrs, bstack11lll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ჉"), None) or (hasattr(self, bstack11lll1_opy_ (u"ࠧࡠࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ჊")) and self._1llllllll11_opy_)
        bstack1llllll1lll_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡈࡐࡑࡎࡗࠬ჋"), bstack11lll1_opy_ (u"ࠩࠪ჌")).split(bstack11lll1_opy_ (u"ࠪ࠰ࠬჍ"))
        if hook_name in bstack1llllll1lll_opy_ and bstack1llllll1lll_opy_ != [bstack11lll1_opy_ (u"ࠫࠬ჎")]:
            return
        bstack1lllllllll1_opy_ = bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ჏"), None)
        hook_data = self.tests[bstack1lllllllll1_opy_][bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩა")]
        status = bstack11lll1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢბ")
        exception = None
        bstack1lllllll111_opy_ = None
        if hook_data.name == bstack11lll1_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦგ"):
            self.bstack1llllll1l11_opy_.reset()
            bstack1lllll1lll1_opy_ = self.tests[bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩდ"), None)][bstack11lll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ე")].result.result
            if bstack1lllll1lll1_opy_ == bstack11lll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦვ"):
                if attrs.hook_failures == 1:
                    status = bstack11lll1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧზ")
                elif attrs.hook_failures == 2:
                    status = bstack11lll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨთ")
            elif attrs.aborted:
                status = bstack11lll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢი")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11lll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬკ") and attrs.hook_failures == 1:
                status = bstack11lll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤლ")
            elif hasattr(attrs, bstack11lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪმ")) and attrs.error_message:
                status = bstack11lll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦნ")
            bstack1lllllll111_opy_, exception = self._1lllllll1l1_opy_(attrs)
        bstack1lllll1ll1l_opy_ = Result(result=status, exception=exception, bstack1llllll11ll_opy_=[bstack1lllllll111_opy_])
        hook_data.stop(time=current_time(), duration=0, result=bstack1lllll1ll1l_opy_)
        TestHubHandler.send_run_event(bstack11lll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧო"), self.tests[bstack1lllllllll1_opy_][bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩპ")])
        threading.current_thread().current_hook_uuid = None
    def _1lllllll1l1_opy_(self, attrs):
        try:
            import traceback
            bstack1lll1l1l1l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1lllllll111_opy_ = bstack1lll1l1l1l_opy_[-1] if bstack1lll1l1l1l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11lll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࠦჟ"))
            bstack1lllllll111_opy_ = None
            exception = None
        return bstack1lllllll111_opy_, exception