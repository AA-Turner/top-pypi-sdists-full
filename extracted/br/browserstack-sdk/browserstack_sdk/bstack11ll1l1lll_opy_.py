# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111ll1ll1l_opy_ import bstack111ll1ll11_opy_, bstack111ll111ll_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack11llll1l11_opy_
from bstack_utils.helper import bstack1ll11lllll_opy_, bstack1ll1ll1l1_opy_, Result
from bstack_utils.bstack111ll1l111_opy_ import bstack1l1ll1l11_opy_
from bstack_utils.capture import bstack111lll111l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11ll1l1lll_opy_:
    def __init__(self):
        self.bstack111ll1l11l_opy_ = bstack111lll111l_opy_(self.bstack111ll1lll1_opy_)
        self.tests = {}
    @staticmethod
    def bstack111ll1lll1_opy_(log):
        if not (log[bstack111l111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ༮")] and log[bstack111l111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༯")].strip()):
            return
        active = bstack11llll1l11_opy_.bstack111ll1llll_opy_()
        log = {
            bstack111l111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ༰"): log[bstack111l111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ༱")],
            bstack111l111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ༲"): bstack1ll1ll1l1_opy_(),
            bstack111l111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ༳"): log[bstack111l111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༴")],
        }
        if active:
            if active[bstack111l111_opy_ (u"ࠨࡶࡼࡴࡪ༵࠭")] == bstack111l111_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ༶"):
                log[bstack111l111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦ༷ࠪ")] = active[bstack111l111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ༸")]
            elif active[bstack111l111_opy_ (u"ࠬࡺࡹࡱࡧ༹ࠪ")] == bstack111l111_opy_ (u"࠭ࡴࡦࡵࡷࠫ༺"):
                log[bstack111l111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ༻")] = active[bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ༼")]
        bstack1l1ll1l11_opy_.bstack1l1111ll1l_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111ll1l11l_opy_.start()
        driver = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ༽"), None)
        bstack111ll1ll1l_opy_ = bstack111ll111ll_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1ll1ll1l1_opy_(),
            file_path=attrs.feature.filename,
            result=bstack111l111_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦ༾"),
            framework=bstack111l111_opy_ (u"ࠫࡇ࡫ࡨࡢࡸࡨࠫ༿"),
            scope=[attrs.feature.name],
            bstack111llll111_opy_=bstack1l1ll1l11_opy_.bstack111lll1l11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack111l111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨཀ")] = bstack111ll1ll1l_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack1l1ll1l11_opy_.bstack111ll1l1ll_opy_(bstack111l111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧཁ"), bstack111ll1ll1l_opy_)
    def end_test(self, attrs):
        bstack111ll11l1l_opy_ = {
            bstack111l111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧག"): attrs.feature.name,
            bstack111l111_opy_ (u"ࠣࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨགྷ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111ll1ll1l_opy_ = self.tests[current_test_uuid][bstack111l111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬང")]
        meta = {
            bstack111l111_opy_ (u"ࠥࡪࡪࡧࡴࡶࡴࡨࠦཅ"): bstack111ll11l1l_opy_,
            bstack111l111_opy_ (u"ࠦࡸࡺࡥࡱࡵࠥཆ"): bstack111ll1ll1l_opy_.meta.get(bstack111l111_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫཇ"), []),
            bstack111l111_opy_ (u"ࠨࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ཈"): {
                bstack111l111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧཉ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111ll1ll1l_opy_.bstack111ll111l1_opy_(meta)
        bstack111ll1ll1l_opy_.bstack111lll1111_opy_(bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ཊ"), []))
        bstack111lll1lll_opy_, exception = self._111lll11ll_opy_(attrs)
        bstack111ll11ll1_opy_ = Result(result=attrs.status.name, exception=exception, bstack111lll1ll1_opy_=[bstack111lll1lll_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack111l111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬཋ")].stop(time=bstack1ll1ll1l1_opy_(), duration=int(attrs.duration)*1000, result=bstack111ll11ll1_opy_)
        bstack1l1ll1l11_opy_.bstack111ll1l1ll_opy_(bstack111l111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬཌ"), self.tests[threading.current_thread().current_test_uuid][bstack111l111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧཌྷ")])
    def bstack1l1l1l11l1_opy_(self, attrs):
        bstack111lll1l1l_opy_ = {
            bstack111l111_opy_ (u"ࠬ࡯ࡤࠨཎ"): uuid4().__str__(),
            bstack111l111_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧཏ"): attrs.keyword,
            bstack111l111_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧཐ"): [],
            bstack111l111_opy_ (u"ࠨࡶࡨࡼࡹ࠭ད"): attrs.name,
            bstack111l111_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭དྷ"): bstack1ll1ll1l1_opy_(),
            bstack111l111_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪན"): bstack111l111_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬཔ"),
            bstack111l111_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪཕ"): bstack111l111_opy_ (u"࠭ࠧབ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack111l111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪབྷ")].add_step(bstack111lll1l1l_opy_)
        threading.current_thread().current_step_uuid = bstack111lll1l1l_opy_[bstack111l111_opy_ (u"ࠨ࡫ࡧࠫམ")]
    def bstack1l1l1111_opy_(self, attrs):
        current_test_id = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ཙ"), None)
        current_step_uuid = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡺࡥࡱࡡࡸࡹ࡮ࡪࠧཚ"), None)
        bstack111lll1lll_opy_, exception = self._111lll11ll_opy_(attrs)
        bstack111ll11ll1_opy_ = Result(result=attrs.status.name, exception=exception, bstack111lll1ll1_opy_=[bstack111lll1lll_opy_])
        self.tests[current_test_id][bstack111l111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧཛ")].bstack111ll11lll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111ll11ll1_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1lll1l1l_opy_(self, name, attrs):
        try:
            bstack111lll11l1_opy_ = uuid4().__str__()
            self.tests[bstack111lll11l1_opy_] = {}
            self.bstack111ll1l11l_opy_.start()
            scopes = []
            driver = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫཛྷ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack111l111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫཝ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack111lll11l1_opy_)
            if name in [bstack111l111_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦཞ"), bstack111l111_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦཟ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack111l111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥའ"), bstack111l111_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠥཡ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack111l111_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬར")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111ll1ll11_opy_(
                name=name,
                uuid=bstack111lll11l1_opy_,
                started_at=bstack1ll1ll1l1_opy_(),
                file_path=file_path,
                framework=bstack111l111_opy_ (u"ࠧࡈࡥࡩࡣࡹࡩࠧལ"),
                bstack111llll111_opy_=bstack1l1ll1l11_opy_.bstack111lll1l11_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack111l111_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢཤ"),
                hook_type=name
            )
            self.tests[bstack111lll11l1_opy_][bstack111l111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡡࡵࡣࠥཥ")] = hook_data
            current_test_id = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠣࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧས"), None)
            if current_test_id:
                hook_data.bstack111ll1l1l1_opy_(current_test_id)
            if name == bstack111l111_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨཧ"):
                threading.current_thread().before_all_hook_uuid = bstack111lll11l1_opy_
            threading.current_thread().current_hook_uuid = bstack111lll11l1_opy_
            bstack1l1ll1l11_opy_.bstack111ll1l1ll_opy_(bstack111l111_opy_ (u"ࠥࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠦཨ"), hook_data)
        except Exception as e:
            logger.debug(bstack111l111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠࡩࡱࡲ࡯ࠥ࡫ࡶࡦࡰࡷࡷ࠱ࠦࡨࡰࡱ࡮ࠤࡳࡧ࡭ࡦ࠼ࠣࠩࡸ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠦࡵࠥཀྵ"), name, e)
    def bstack1ll111lll1_opy_(self, attrs):
        bstack111ll11l11_opy_ = bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩཪ"), None)
        hook_data = self.tests[bstack111ll11l11_opy_][bstack111l111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩཫ")]
        status = bstack111l111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢཬ")
        exception = None
        bstack111lll1lll_opy_ = None
        if hook_data.name == bstack111l111_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦ཭"):
            self.bstack111ll1l11l_opy_.reset()
            bstack111llll11l_opy_ = self.tests[bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ཮"), None)][bstack111l111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭཯")].result.result
            if bstack111llll11l_opy_ == bstack111l111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ཰"):
                if attrs.hook_failures == 1:
                    status = bstack111l111_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨཱࠧ")
                elif attrs.hook_failures == 2:
                    status = bstack111l111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨི")
            elif attrs.aborted:
                status = bstack111l111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪཱིࠢ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack111l111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰུࠬ") and attrs.hook_failures == 1:
                status = bstack111l111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤཱུ")
            elif hasattr(attrs, bstack111l111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪྲྀ")) and attrs.error_message:
                status = bstack111l111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦཷ")
            bstack111lll1lll_opy_, exception = self._111lll11ll_opy_(attrs)
        bstack111ll11ll1_opy_ = Result(result=status, exception=exception, bstack111lll1ll1_opy_=[bstack111lll1lll_opy_])
        hook_data.stop(time=bstack1ll1ll1l1_opy_(), duration=0, result=bstack111ll11ll1_opy_)
        bstack1l1ll1l11_opy_.bstack111ll1l1ll_opy_(bstack111l111_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧླྀ"), self.tests[bstack111ll11l11_opy_][bstack111l111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩཹ")])
        threading.current_thread().current_hook_uuid = None
    def _111lll11ll_opy_(self, attrs):
        try:
            import traceback
            bstack1l11l1lll_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111lll1lll_opy_ = bstack1l11l1lll_opy_[-1] if bstack1l11l1lll_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack111l111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ེࠦ"))
            bstack111lll1lll_opy_ = None
            exception = None
        return bstack111lll1lll_opy_, exception