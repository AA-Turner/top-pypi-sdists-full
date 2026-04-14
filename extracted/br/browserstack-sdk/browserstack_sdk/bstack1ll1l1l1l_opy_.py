# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack1llll1l11ll_opy_ import bstack1llll11l1ll_opy_, bstack1llll1111l1_opy_
from bstack_utils.bstack1lll111111_opy_ import bstack1l1ll1l1ll_opy_
from bstack_utils.helper import bstack1l111l11l_opy_, bstack111111l1l_opy_, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack1llll11l11l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1ll1l1l1l_opy_:
    def __init__(self):
        self.bstack1llll111l1l_opy_ = bstack1llll11l11l_opy_(self.bstack1llll11ll11_opy_)
        self.tests = {}
    @staticmethod
    def bstack1llll11ll11_opy_(log):
        if not (log[bstack1l111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨი")] and log[bstack1l111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩკ")].strip()):
            return
        active = bstack1l1ll1l1ll_opy_.bstack1llll111lll_opy_()
        log = {
            bstack1l111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨლ"): log[bstack1l111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩმ")],
            bstack1l111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧნ"): bstack111111l1l_opy_(),
            bstack1l111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ო"): log[bstack1l111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧპ")],
        }
        if active:
            if active[bstack1l111l_opy_ (u"ࠧࡵࡻࡳࡩࠬჟ")] == bstack1l111l_opy_ (u"ࠨࡪࡲࡳࡰ࠭რ"):
                log[bstack1l111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩს")] = active[bstack1l111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪტ")]
            elif active[bstack1l111l_opy_ (u"ࠫࡹࡿࡰࡦࠩუ")] == bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࠪფ"):
                log[bstack1l111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ქ")] = active[bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧღ")]
        TestHubHandler.bstack1ll111l11_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1llll111l1l_opy_.start()
        driver = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧყ"), None)
        bstack1llll1l11ll_opy_ = bstack1llll1111l1_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack111111l1l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1l111l_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥშ"),
            framework=bstack1l111l_opy_ (u"ࠪࡆࡪ࡮ࡡࡷࡧࠪჩ"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack1llll11l1l1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1l111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧც")] = bstack1llll1l11ll_opy_
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.bstack1llll1l1111_opy_(bstack1l111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ძ"), bstack1llll1l11ll_opy_)
    def end_test(self, attrs):
        bstack1llll11llll_opy_ = {
            bstack1l111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦწ"): attrs.feature.name,
            bstack1l111l_opy_ (u"ࠢࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧჭ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack1llll1l11ll_opy_ = self.tests[current_test_uuid][bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫხ")]
        meta = {
            bstack1l111l_opy_ (u"ࠤࡩࡩࡦࡺࡵࡳࡧࠥჯ"): bstack1llll11llll_opy_,
            bstack1l111l_opy_ (u"ࠥࡷࡹ࡫ࡰࡴࠤჰ"): bstack1llll1l11ll_opy_.meta.get(bstack1l111l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪჱ"), []),
            bstack1l111l_opy_ (u"ࠧࡹࡣࡦࡰࡤࡶ࡮ࡵࠢჲ"): {
                bstack1l111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦჳ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack1llll1l11ll_opy_.bstack1llll111ll1_opy_(meta)
        bstack1llll1l11ll_opy_.bstack1llll1l1lll_opy_(bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬჴ"), []))
        bstack1llll11ll1l_opy_, exception = self._1llll1l1ll1_opy_(attrs)
        status = bstack1l111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨჵ") if attrs.status.name.lower() == bstack1l111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨჶ") else attrs.status.name.lower()
        bstack1llll11l111_opy_ = Result(result=status, exception=exception, bstack1llll1l111l_opy_=[bstack1llll11ll1l_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1l111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ჷ")].stop(time=bstack111111l1l_opy_(), duration=int(attrs.duration)*1000, result=bstack1llll11l111_opy_)
        TestHubHandler.bstack1llll1l1111_opy_(bstack1l111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ჸ"), self.tests[threading.current_thread().current_test_uuid][bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨჹ")])
    def bstack111lll111_opy_(self, attrs):
        bstack1llll1111ll_opy_ = {
            bstack1l111l_opy_ (u"࠭ࡩࡥࠩჺ"): uuid4().__str__(),
            bstack1l111l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨ჻"): attrs.keyword,
            bstack1l111l_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨჼ"): [],
            bstack1l111l_opy_ (u"ࠩࡷࡩࡽࡺࠧჽ"): attrs.name,
            bstack1l111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧჾ"): bstack111111l1l_opy_(),
            bstack1l111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫჿ"): bstack1l111l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᄀ"),
            bstack1l111l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᄁ"): bstack1l111l_opy_ (u"ࠧࠨᄂ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1l111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᄃ")].add_step(bstack1llll1111ll_opy_)
        threading.current_thread().current_step_uuid = bstack1llll1111ll_opy_[bstack1l111l_opy_ (u"ࠩ࡬ࡨࠬᄄ")]
    def bstack1ll1lll111_opy_(self, attrs):
        current_test_id = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᄅ"), None)
        current_step_uuid = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨᄆ"), None)
        bstack1llll11ll1l_opy_, exception = self._1llll1l1ll1_opy_(attrs)
        status = bstack1l111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᄇ") if attrs.status.name.lower() == bstack1l111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᄈ") else attrs.status.name.lower()
        bstack1llll11l111_opy_ = Result(result=status, exception=exception, bstack1llll1l111l_opy_=[bstack1llll11ll1l_opy_])
        self.tests[current_test_id][bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᄉ")].bstack1llll1l1l11_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1llll11l111_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11l11ll1_opy_(self, name, attrs):
        try:
            bstack1llll11lll1_opy_ = os.environ.get(bstack1l111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡈࡐࡑࡎࡗࠬᄊ"), bstack1l111l_opy_ (u"ࠩࠪᄋ")).split(bstack1l111l_opy_ (u"ࠪ࠰ࠬᄌ"))
            if name in bstack1llll11lll1_opy_ and bstack1llll11lll1_opy_ != [bstack1l111l_opy_ (u"ࠫࠬᄍ")]:
                return
            bstack1llll1l11l1_opy_ = uuid4().__str__()
            self.tests[bstack1llll1l11l1_opy_] = {}
            self.bstack1llll111l1l_opy_.start()
            scopes = []
            driver = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫᄎ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1l111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫᄏ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1llll1l11l1_opy_)
            if name in [bstack1l111l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦᄐ"), bstack1l111l_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦᄑ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1l111l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥᄒ"), bstack1l111l_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠥᄓ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1l111l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᄔ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1llll11l1ll_opy_(
                name=name,
                uuid=bstack1llll1l11l1_opy_,
                started_at=bstack111111l1l_opy_(),
                file_path=file_path,
                framework=bstack1l111l_opy_ (u"ࠧࡈࡥࡩࡣࡹࡩࠧᄕ"),
                integrations=TestHubHandler.bstack1llll11l1l1_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1l111l_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢᄖ"),
                hook_type=name
            )
            self.tests[bstack1llll1l11l1_opy_][bstack1l111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡡࡵࡣࠥᄗ")] = hook_data
            current_test_id = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠣࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧᄘ"), None)
            if current_test_id:
                hook_data.bstack1llll111l11_opy_(current_test_id)
            if name == bstack1l111l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨᄙ"):
                threading.current_thread().before_all_hook_uuid = bstack1llll1l11l1_opy_
            threading.current_thread().current_hook_uuid = bstack1llll1l11l1_opy_
            TestHubHandler.bstack1llll1l1111_opy_(bstack1l111l_opy_ (u"ࠥࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠦᄚ"), hook_data)
        except Exception as e:
            logger.debug(bstack1l111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠࡩࡱࡲ࡯ࠥ࡫ࡶࡦࡰࡷࡷ࠱ࠦࡨࡰࡱ࡮ࠤࡳࡧ࡭ࡦ࠼ࠣࠩࡸ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠦࡵࠥᄛ"), name, e)
    def bstack1llllll1lll_opy_(self, attrs):
        hook_name = getattr(attrs, bstack1l111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᄜ"), None) or (hasattr(self, bstack1l111l_opy_ (u"࠭࡟ࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᄝ")) and self._1llll111111_opy_)
        bstack1llll11lll1_opy_ = os.environ.get(bstack1l111l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡉࡋࡆࡂࡗࡏࡘࡤࡎࡏࡐࡍࡖࠫᄞ"), bstack1l111l_opy_ (u"ࠨࠩᄟ")).split(bstack1l111l_opy_ (u"ࠩ࠯ࠫᄠ"))
        if hook_name in bstack1llll11lll1_opy_ and bstack1llll11lll1_opy_ != [bstack1l111l_opy_ (u"ࠪࠫᄡ")]:
            return
        bstack1llll11111l_opy_ = bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᄢ"), None)
        hook_data = self.tests[bstack1llll11111l_opy_][bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᄣ")]
        status = bstack1l111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᄤ")
        exception = None
        bstack1llll11ll1l_opy_ = None
        if hook_data.name == bstack1l111l_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠥᄥ"):
            self.bstack1llll111l1l_opy_.reset()
            bstack1llll1l1l1l_opy_ = self.tests[bstack1l111l11l_opy_(threading.current_thread(), bstack1l111l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᄦ"), None)][bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᄧ")].result.result
            if bstack1llll1l1l1l_opy_ == bstack1l111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᄨ"):
                if attrs.hook_failures == 1:
                    status = bstack1l111l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᄩ")
                elif attrs.hook_failures == 2:
                    status = bstack1l111l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᄪ")
            elif attrs.aborted:
                status = bstack1l111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᄫ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1l111l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫᄬ") and attrs.hook_failures == 1:
                status = bstack1l111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᄭ")
            elif hasattr(attrs, bstack1l111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡠ࡯ࡨࡷࡸࡧࡧࡦࠩᄮ")) and attrs.error_message:
                status = bstack1l111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᄯ")
            bstack1llll11ll1l_opy_, exception = self._1llll1l1ll1_opy_(attrs)
        bstack1llll11l111_opy_ = Result(result=status, exception=exception, bstack1llll1l111l_opy_=[bstack1llll11ll1l_opy_])
        hook_data.stop(time=bstack111111l1l_opy_(), duration=0, result=bstack1llll11l111_opy_)
        TestHubHandler.bstack1llll1l1111_opy_(bstack1l111l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᄰ"), self.tests[bstack1llll11111l_opy_][bstack1l111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᄱ")])
        threading.current_thread().current_hook_uuid = None
    def _1llll1l1ll1_opy_(self, attrs):
        try:
            import traceback
            bstack111lllll1_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1llll11ll1l_opy_ = bstack111lllll1_opy_[-1] if bstack111lllll1_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1l111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡶࡸࡴࡳࠠࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࠥᄲ"))
            bstack1llll11ll1l_opy_ = None
            exception = None
        return bstack1llll11ll1l_opy_, exception