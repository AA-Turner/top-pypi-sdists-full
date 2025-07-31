# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111ll1llll_opy_ import bstack111lll11l1_opy_, bstack111ll1l1l1_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l1lllll1l_opy_
from bstack_utils.helper import bstack1l111ll111_opy_, bstack1ll11ll11l_opy_, Result
from bstack_utils.bstack111ll1l1ll_opy_ import bstack11ll111ll1_opy_
from bstack_utils.capture import bstack111ll11111_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1ll111lll_opy_:
    def __init__(self):
        self.bstack111lll111l_opy_ = bstack111ll11111_opy_(self.bstack111ll11ll1_opy_)
        self.tests = {}
    @staticmethod
    def bstack111ll11ll1_opy_(log):
        if not (log[bstack1l11l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༯")] and log[bstack1l11l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༰")].strip()):
            return
        active = bstack1l1lllll1l_opy_.bstack111lll1l1l_opy_()
        log = {
            bstack1l11l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ༱"): log[bstack1l11l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ༲")],
            bstack1l11l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ༳"): bstack1ll11ll11l_opy_(),
            bstack1l11l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༴"): log[bstack1l11l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦ༵ࠩ")],
        }
        if active:
            if active[bstack1l11l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ༶")] == bstack1l11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ༷"):
                log[bstack1l11l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ༸")] = active[bstack1l11l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨ༹ࠬ")]
            elif active[bstack1l11l11_opy_ (u"࠭ࡴࡺࡲࡨࠫ༺")] == bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࠬ༻"):
                log[bstack1l11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ༼")] = active[bstack1l11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ༽")]
        bstack11ll111ll1_opy_.bstack1l11lll1l1_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111lll111l_opy_.start()
        driver = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ༾"), None)
        bstack111ll1llll_opy_ = bstack111ll1l1l1_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1ll11ll11l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1l11l11_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ༿"),
            framework=bstack1l11l11_opy_ (u"ࠬࡈࡥࡩࡣࡹࡩࠬཀ"),
            scope=[attrs.feature.name],
            bstack111ll111ll_opy_=bstack11ll111ll1_opy_.bstack111ll11l1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1l11l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩཁ")] = bstack111ll1llll_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack11ll111ll1_opy_.bstack111ll1l111_opy_(bstack1l11l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨག"), bstack111ll1llll_opy_)
    def end_test(self, attrs):
        bstack111ll1l11l_opy_ = {
            bstack1l11l11_opy_ (u"ࠣࡰࡤࡱࡪࠨགྷ"): attrs.feature.name,
            bstack1l11l11_opy_ (u"ࠤࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢང"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111ll1llll_opy_ = self.tests[current_test_uuid][bstack1l11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ཅ")]
        meta = {
            bstack1l11l11_opy_ (u"ࠦ࡫࡫ࡡࡵࡷࡵࡩࠧཆ"): bstack111ll1l11l_opy_,
            bstack1l11l11_opy_ (u"ࠧࡹࡴࡦࡲࡶࠦཇ"): bstack111ll1llll_opy_.meta.get(bstack1l11l11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ཈"), []),
            bstack1l11l11_opy_ (u"ࠢࡴࡥࡨࡲࡦࡸࡩࡰࠤཉ"): {
                bstack1l11l11_opy_ (u"ࠣࡰࡤࡱࡪࠨཊ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111ll1llll_opy_.bstack111lll1l11_opy_(meta)
        bstack111ll1llll_opy_.bstack111lll1ll1_opy_(bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧཋ"), []))
        bstack111lll11ll_opy_, exception = self._111ll11lll_opy_(attrs)
        bstack111ll111l1_opy_ = Result(result=attrs.status.name, exception=exception, bstack111ll11l11_opy_=[bstack111lll11ll_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1l11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ཌ")].stop(time=bstack1ll11ll11l_opy_(), duration=int(attrs.duration)*1000, result=bstack111ll111l1_opy_)
        bstack11ll111ll1_opy_.bstack111ll1l111_opy_(bstack1l11l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ཌྷ"), self.tests[threading.current_thread().current_test_uuid][bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨཎ")])
    def bstack111l11l1l_opy_(self, attrs):
        bstack111ll1ll11_opy_ = {
            bstack1l11l11_opy_ (u"࠭ࡩࡥࠩཏ"): uuid4().__str__(),
            bstack1l11l11_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨཐ"): attrs.keyword,
            bstack1l11l11_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨད"): [],
            bstack1l11l11_opy_ (u"ࠩࡷࡩࡽࡺࠧདྷ"): attrs.name,
            bstack1l11l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧན"): bstack1ll11ll11l_opy_(),
            bstack1l11l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫཔ"): bstack1l11l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ཕ"),
            bstack1l11l11_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫབ"): bstack1l11l11_opy_ (u"ࠧࠨབྷ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1l11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫམ")].add_step(bstack111ll1ll11_opy_)
        threading.current_thread().current_step_uuid = bstack111ll1ll11_opy_[bstack1l11l11_opy_ (u"ࠩ࡬ࡨࠬཙ")]
    def bstack1l11l1ll1l_opy_(self, attrs):
        current_test_id = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧཚ"), None)
        current_step_uuid = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨཛ"), None)
        bstack111lll11ll_opy_, exception = self._111ll11lll_opy_(attrs)
        bstack111ll111l1_opy_ = Result(result=attrs.status.name, exception=exception, bstack111ll11l11_opy_=[bstack111lll11ll_opy_])
        self.tests[current_test_id][bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨཛྷ")].bstack111ll1ll1l_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111ll111l1_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack111111ll_opy_(self, name, attrs):
        try:
            bstack111ll1111l_opy_ = uuid4().__str__()
            self.tests[bstack111ll1111l_opy_] = {}
            self.bstack111lll111l_opy_.start()
            scopes = []
            driver = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬཝ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1l11l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬཞ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack111ll1111l_opy_)
            if name in [bstack1l11l11_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧཟ"), bstack1l11l11_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠧའ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1l11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦཡ"), bstack1l11l11_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠦར")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1l11l11_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ལ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111lll11l1_opy_(
                name=name,
                uuid=bstack111ll1111l_opy_,
                started_at=bstack1ll11ll11l_opy_(),
                file_path=file_path,
                framework=bstack1l11l11_opy_ (u"ࠨࡂࡦࡪࡤࡺࡪࠨཤ"),
                bstack111ll111ll_opy_=bstack11ll111ll1_opy_.bstack111ll11l1l_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1l11l11_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣཥ"),
                hook_type=name
            )
            self.tests[bstack111ll1111l_opy_][bstack1l11l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡢࡶࡤࠦས")] = hook_data
            current_test_id = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠤࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨཧ"), None)
            if current_test_id:
                hook_data.bstack111ll1lll1_opy_(current_test_id)
            if name == bstack1l11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢཨ"):
                threading.current_thread().before_all_hook_uuid = bstack111ll1111l_opy_
            threading.current_thread().current_hook_uuid = bstack111ll1111l_opy_
            bstack11ll111ll1_opy_.bstack111ll1l111_opy_(bstack1l11l11_opy_ (u"ࠦࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠧཀྵ"), hook_data)
        except Exception as e:
            logger.debug(bstack1l11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࠡࡪࡲࡳࡰࠦࡥࡷࡧࡱࡸࡸ࠲ࠠࡩࡱࡲ࡯ࠥࡴࡡ࡮ࡧ࠽ࠤࠪࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠧࡶࠦཪ"), name, e)
    def bstack11111l1ll_opy_(self, attrs):
        bstack111lll1lll_opy_ = bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪཫ"), None)
        hook_data = self.tests[bstack111lll1lll_opy_][bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཬ")]
        status = bstack1l11l11_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ཭")
        exception = None
        bstack111lll11ll_opy_ = None
        if hook_data.name == bstack1l11l11_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠧ཮"):
            self.bstack111lll111l_opy_.reset()
            bstack111llll111_opy_ = self.tests[bstack1l111ll111_opy_(threading.current_thread(), bstack1l11l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ཯"), None)][bstack1l11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ཰")].result.result
            if bstack111llll111_opy_ == bstack1l11l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨཱࠧ"):
                if attrs.hook_failures == 1:
                    status = bstack1l11l11_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨི")
                elif attrs.hook_failures == 2:
                    status = bstack1l11l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪཱིࠢ")
            elif attrs.aborted:
                status = bstack1l11l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤུࠣ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1l11l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱཱུ࠭") and attrs.hook_failures == 1:
                status = bstack1l11l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥྲྀ")
            elif hasattr(attrs, bstack1l11l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡢࡱࡪࡹࡳࡢࡩࡨࠫཷ")) and attrs.error_message:
                status = bstack1l11l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧླྀ")
            bstack111lll11ll_opy_, exception = self._111ll11lll_opy_(attrs)
        bstack111ll111l1_opy_ = Result(result=status, exception=exception, bstack111ll11l11_opy_=[bstack111lll11ll_opy_])
        hook_data.stop(time=bstack1ll11ll11l_opy_(), duration=0, result=bstack111ll111l1_opy_)
        bstack11ll111ll1_opy_.bstack111ll1l111_opy_(bstack1l11l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨཹ"), self.tests[bstack111lll1lll_opy_][bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣེࠪ")])
        threading.current_thread().current_hook_uuid = None
    def _111ll11lll_opy_(self, attrs):
        try:
            import traceback
            bstack1l11l111l1_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111lll11ll_opy_ = bstack1l11l111l1_opy_[-1] if bstack1l11l111l1_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1l11l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡶࡦࡩࡥࡣࡣࡦ࡯ཻࠧ"))
            bstack111lll11ll_opy_ = None
            exception = None
        return bstack111lll11ll_opy_, exception