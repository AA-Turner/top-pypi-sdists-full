# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack1llll11llll_opy_ import bstack1llll1l111l_opy_, bstack1llll1l1l1l_opy_
from bstack_utils.bstack1l11l1l11l_opy_ import bstack1lllll1l11_opy_
from bstack_utils.helper import bstack11ll1l11l_opy_, bstack1l1l111l1l_opy_, Result
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.capture import bstack1llll111l1l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l1llllll_opy_:
    def __init__(self):
        self.bstack1llll1ll111_opy_ = bstack1llll111l1l_opy_(self.bstack1llll111lll_opy_)
        self.tests = {}
    @staticmethod
    def bstack1llll111lll_opy_(log):
        if not (log[bstack11ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ⴡ")] and log[bstack11ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧჂ")].strip()):
            return
        active = bstack1lllll1l11_opy_.bstack1llll1ll1l1_opy_()
        log = {
            bstack11ll11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ⴣ"): log[bstack11ll11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧჄ")],
            bstack11ll11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬჅ"): bstack1l1l111l1l_opy_(),
            bstack11ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ჆"): log[bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬჇ")],
        }
        if active:
            if active[bstack11ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪ჈")] == bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ჉"):
                log[bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ჊")] = active[bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ჋")]
            elif active[bstack11ll11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ჌")] == bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࠨჍ"):
                log[bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ჎")] = active[bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ჏")]
        TestHubHandler.bstack111ll1lll1_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1llll1ll111_opy_.start()
        driver = bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬა"), None)
        bstack1llll11llll_opy_ = bstack1llll1l1l1l_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1l1l111l1l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack11ll11_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣბ"),
            framework=bstack11ll11_opy_ (u"ࠨࡄࡨ࡬ࡦࡼࡥࠨგ"),
            scope=[attrs.feature.name],
            integrations=TestHubHandler.bstack1llll11ll11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬდ")] = bstack1llll11llll_opy_
        threading.current_thread().current_test_uuid = test_uuid
        TestHubHandler.bstack1llll1l1111_opy_(bstack11ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫე"), bstack1llll11llll_opy_)
    def end_test(self, attrs):
        bstack1llll111ll1_opy_ = {
            bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤვ"): attrs.feature.name,
            bstack11ll11_opy_ (u"ࠧࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥზ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack1llll11llll_opy_ = self.tests[current_test_uuid][bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩთ")]
        meta = {
            bstack11ll11_opy_ (u"ࠢࡧࡧࡤࡸࡺࡸࡥࠣი"): bstack1llll111ll1_opy_,
            bstack11ll11_opy_ (u"ࠣࡵࡷࡩࡵࡹࠢკ"): bstack1llll11llll_opy_.meta.get(bstack11ll11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨლ"), []),
            bstack11ll11_opy_ (u"ࠥࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧმ"): {
                bstack11ll11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤნ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack1llll11llll_opy_.bstack1llll1l1lll_opy_(meta)
        bstack1llll11llll_opy_.bstack1llll1l1l11_opy_(bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪო"), []))
        bstack1llll111l11_opy_, exception = self._1llll11l111_opy_(attrs)
        status = bstack11ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭პ") if attrs.status.name.lower() == bstack11ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ჟ") else attrs.status.name.lower()
        bstack1llll1l11ll_opy_ = Result(result=status, exception=exception, bstack1llll11ll1l_opy_=[bstack1llll111l11_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫრ")].stop(time=bstack1l1l111l1l_opy_(), duration=int(attrs.duration)*1000, result=bstack1llll1l11ll_opy_)
        TestHubHandler.bstack1llll1l1111_opy_(bstack11ll11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫს"), self.tests[threading.current_thread().current_test_uuid][bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ტ")])
    def bstack11lll1l1_opy_(self, attrs):
        bstack1llll11l1ll_opy_ = {
            bstack11ll11_opy_ (u"ࠫ࡮ࡪࠧუ"): uuid4().__str__(),
            bstack11ll11_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ფ"): attrs.keyword,
            bstack11ll11_opy_ (u"࠭ࡳࡵࡧࡳࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭ქ"): [],
            bstack11ll11_opy_ (u"ࠧࡵࡧࡻࡸࠬღ"): attrs.name,
            bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬყ"): bstack1l1l111l1l_opy_(),
            bstack11ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩშ"): bstack11ll11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫჩ"),
            bstack11ll11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩც"): bstack11ll11_opy_ (u"ࠬ࠭ძ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩწ")].add_step(bstack1llll11l1ll_opy_)
        threading.current_thread().current_step_uuid = bstack1llll11l1ll_opy_[bstack11ll11_opy_ (u"ࠧࡪࡦࠪჭ")]
    def bstack11111llll_opy_(self, attrs):
        current_test_id = bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬხ"), None)
        current_step_uuid = bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭ჯ"), None)
        bstack1llll111l11_opy_, exception = self._1llll11l111_opy_(attrs)
        status = bstack11ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪჰ") if attrs.status.name.lower() == bstack11ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪჱ") else attrs.status.name.lower()
        bstack1llll1l11ll_opy_ = Result(result=status, exception=exception, bstack1llll11ll1l_opy_=[bstack1llll111l11_opy_])
        self.tests[current_test_id][bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨჲ")].bstack1llll1ll11l_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1llll1l11ll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1ll1l1l1_opy_(self, name, attrs):
        try:
            bstack1llll11l1l1_opy_ = os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡓࡅࡍࡢࡈࡊࡌࡁࡖࡎࡗࡣࡍࡕࡏࡌࡕࠪჳ"), bstack11ll11_opy_ (u"ࠧࠨჴ")).split(bstack11ll11_opy_ (u"ࠨ࠮ࠪჵ"))
            if name in bstack1llll11l1l1_opy_ and bstack1llll11l1l1_opy_ != [bstack11ll11_opy_ (u"ࠩࠪჶ")]:
                return
            bstack1llll1111ll_opy_ = uuid4().__str__()
            self.tests[bstack1llll1111ll_opy_] = {}
            self.bstack1llll1ll111_opy_.start()
            scopes = []
            driver = bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩჷ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩჸ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1llll1111ll_opy_)
            if name in [bstack11ll11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤჹ"), bstack11ll11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤჺ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack11ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ჻"), bstack11ll11_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠣჼ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack11ll11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪჽ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1llll1l111l_opy_(
                name=name,
                uuid=bstack1llll1111ll_opy_,
                started_at=bstack1l1l111l1l_opy_(),
                file_path=file_path,
                framework=bstack11ll11_opy_ (u"ࠥࡆࡪ࡮ࡡࡷࡧࠥჾ"),
                integrations=TestHubHandler.bstack1llll11ll11_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack11ll11_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧჿ"),
                hook_type=name
            )
            self.tests[bstack1llll1111ll_opy_][bstack11ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡦࡺࡡࠣᄀ")] = hook_data
            current_test_id = bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠨࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥᄁ"), None)
            if current_test_id:
                hook_data.bstack1llll1l11l1_opy_(current_test_id)
            if name == bstack11ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦᄂ"):
                threading.current_thread().before_all_hook_uuid = bstack1llll1111ll_opy_
            threading.current_thread().current_hook_uuid = bstack1llll1111ll_opy_
            TestHubHandler.bstack1llll1l1111_opy_(bstack11ll11_opy_ (u"ࠣࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤᄃ"), hook_data)
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥ࡮࡯ࡰ࡭ࠣࡩࡻ࡫࡮ࡵࡵ࠯ࠤ࡭ࡵ࡯࡬ࠢࡱࡥࡲ࡫࠺ࠡࠧࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠫࡳࠣᄄ"), name, e)
    def bstack11ll1l1l1l_opy_(self, attrs):
        hook_name = getattr(attrs, bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᄅ"), None) or (hasattr(self, bstack11ll11_opy_ (u"ࠫࡤࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᄆ")) and self._1llll11l11l_opy_)
        bstack1llll11l1l1_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤ࡙ࡄࡌࡡࡇࡉࡋࡇࡕࡍࡖࡢࡌࡔࡕࡋࡔࠩᄇ"), bstack11ll11_opy_ (u"࠭ࠧᄈ")).split(bstack11ll11_opy_ (u"ࠧ࠭ࠩᄉ"))
        if hook_name in bstack1llll11l1l1_opy_ and bstack1llll11l1l1_opy_ != [bstack11ll11_opy_ (u"ࠨࠩᄊ")]:
            return
        bstack1llll1l1ll1_opy_ = bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᄋ"), None)
        hook_data = self.tests[bstack1llll1l1ll1_opy_][bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᄌ")]
        status = bstack11ll11_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦᄍ")
        exception = None
        bstack1llll111l11_opy_ = None
        if hook_data.name == bstack11ll11_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣᄎ"):
            self.bstack1llll1ll111_opy_.reset()
            bstack1llll11lll1_opy_ = self.tests[bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᄏ"), None)][bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᄐ")].result.result
            if bstack1llll11lll1_opy_ == bstack11ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᄑ"):
                if attrs.hook_failures == 1:
                    status = bstack11ll11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᄒ")
                elif attrs.hook_failures == 2:
                    status = bstack11ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᄓ")
            elif attrs.aborted:
                status = bstack11ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᄔ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11ll11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩᄕ") and attrs.hook_failures == 1:
                status = bstack11ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᄖ")
            elif hasattr(attrs, bstack11ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧᄗ")) and attrs.error_message:
                status = bstack11ll11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᄘ")
            bstack1llll111l11_opy_, exception = self._1llll11l111_opy_(attrs)
        bstack1llll1l11ll_opy_ = Result(result=status, exception=exception, bstack1llll11ll1l_opy_=[bstack1llll111l11_opy_])
        hook_data.stop(time=bstack1l1l111l1l_opy_(), duration=0, result=bstack1llll1l11ll_opy_)
        TestHubHandler.bstack1llll1l1111_opy_(bstack11ll11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᄙ"), self.tests[bstack1llll1l1ll1_opy_][bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᄚ")])
        threading.current_thread().current_hook_uuid = None
    def _1llll11l111_opy_(self, attrs):
        try:
            import traceback
            bstack1lllll11l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1llll111l11_opy_ = bstack1lllll11l_opy_[-1] if bstack1lllll11l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡴࡶࡲࡱࠥࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࠣᄛ"))
            bstack1llll111l11_opy_ = None
            exception = None
        return bstack1llll111l11_opy_, exception