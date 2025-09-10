# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111lll1111_opy_ import bstack111l1lll1l_opy_, bstack111l1ll1ll_opy_
from bstack_utils.bstack111ll11111_opy_ import bstack11lllllll1_opy_
from bstack_utils.helper import bstack1111l1l11_opy_, bstack11l1l1l1l1_opy_, Result
from bstack_utils.bstack111ll11l1l_opy_ import bstack1l11ll1l_opy_
from bstack_utils.capture import bstack111ll111l1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11l111l11l_opy_:
    def __init__(self):
        self.bstack111ll1l111_opy_ = bstack111ll111l1_opy_(self.bstack111l1llll1_opy_)
        self.tests = {}
    @staticmethod
    def bstack111l1llll1_opy_(log):
        if not (log[bstack1ll11ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ༹࠭")] and log[bstack1ll11ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ༺")].strip()):
            return
        active = bstack11lllllll1_opy_.bstack111ll1l11l_opy_()
        log = {
            bstack1ll11ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭༻"): log[bstack1ll11ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ༼")],
            bstack1ll11ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ༽"): bstack11l1l1l1l1_opy_(),
            bstack1ll11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༾"): log[bstack1ll11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༿")],
        }
        if active:
            if active[bstack1ll11ll_opy_ (u"ࠬࡺࡹࡱࡧࠪཀ")] == bstack1ll11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫཁ"):
                log[bstack1ll11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧག")] = active[bstack1ll11ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨགྷ")]
            elif active[bstack1ll11ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧང")] == bstack1ll11ll_opy_ (u"ࠪࡸࡪࡹࡴࠨཅ"):
                log[bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫཆ")] = active[bstack1ll11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬཇ")]
        bstack1l11ll1l_opy_.bstack11lllll11l_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111ll1l111_opy_.start()
        driver = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ཈"), None)
        bstack111lll1111_opy_ = bstack111l1ll1ll_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack11l1l1l1l1_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1ll11ll_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣཉ"),
            framework=bstack1ll11ll_opy_ (u"ࠨࡄࡨ࡬ࡦࡼࡥࠨཊ"),
            scope=[attrs.feature.name],
            bstack111l1lllll_opy_=bstack1l11ll1l_opy_.bstack111ll1ll1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬཋ")] = bstack111lll1111_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack1l11ll1l_opy_.bstack111ll1ll11_opy_(bstack1ll11ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫཌ"), bstack111lll1111_opy_)
    def end_test(self, attrs):
        bstack111ll111ll_opy_ = {
            bstack1ll11ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤཌྷ"): attrs.feature.name,
            bstack1ll11ll_opy_ (u"ࠧࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥཎ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111lll1111_opy_ = self.tests[current_test_uuid][bstack1ll11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩཏ")]
        meta = {
            bstack1ll11ll_opy_ (u"ࠢࡧࡧࡤࡸࡺࡸࡥࠣཐ"): bstack111ll111ll_opy_,
            bstack1ll11ll_opy_ (u"ࠣࡵࡷࡩࡵࡹࠢད"): bstack111lll1111_opy_.meta.get(bstack1ll11ll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨདྷ"), []),
            bstack1ll11ll_opy_ (u"ࠥࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧན"): {
                bstack1ll11ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤཔ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111lll1111_opy_.bstack111lll11l1_opy_(meta)
        bstack111lll1111_opy_.bstack111lll111l_opy_(bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪཕ"), []))
        bstack111ll1111l_opy_, exception = self._111ll11ll1_opy_(attrs)
        bstack111ll11l11_opy_ = Result(result=attrs.status.name, exception=exception, bstack111ll1l1l1_opy_=[bstack111ll1111l_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1ll11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩབ")].stop(time=bstack11l1l1l1l1_opy_(), duration=int(attrs.duration)*1000, result=bstack111ll11l11_opy_)
        bstack1l11ll1l_opy_.bstack111ll1ll11_opy_(bstack1ll11ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩབྷ"), self.tests[threading.current_thread().current_test_uuid][bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫམ")])
    def bstack11llll1ll_opy_(self, attrs):
        bstack111ll1l1ll_opy_ = {
            bstack1ll11ll_opy_ (u"ࠩ࡬ࡨࠬཙ"): uuid4().__str__(),
            bstack1ll11ll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫཚ"): attrs.keyword,
            bstack1ll11ll_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫཛ"): [],
            bstack1ll11ll_opy_ (u"ࠬࡺࡥࡹࡶࠪཛྷ"): attrs.name,
            bstack1ll11ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪཝ"): bstack11l1l1l1l1_opy_(),
            bstack1ll11ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧཞ"): bstack1ll11ll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩཟ"),
            bstack1ll11ll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧའ"): bstack1ll11ll_opy_ (u"ࠪࠫཡ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧར")].add_step(bstack111ll1l1ll_opy_)
        threading.current_thread().current_step_uuid = bstack111ll1l1ll_opy_[bstack1ll11ll_opy_ (u"ࠬ࡯ࡤࠨལ")]
    def bstack1ll111ll1_opy_(self, attrs):
        current_test_id = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪཤ"), None)
        current_step_uuid = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫཥ"), None)
        bstack111ll1111l_opy_, exception = self._111ll11ll1_opy_(attrs)
        bstack111ll11l11_opy_ = Result(result=attrs.status.name, exception=exception, bstack111ll1l1l1_opy_=[bstack111ll1111l_opy_])
        self.tests[current_test_id][bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫས")].bstack111ll1lll1_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111ll11l11_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1lllll1ll1_opy_(self, name, attrs):
        try:
            bstack111ll11lll_opy_ = uuid4().__str__()
            self.tests[bstack111ll11lll_opy_] = {}
            self.bstack111ll1l111_opy_.start()
            scopes = []
            driver = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨཧ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1ll11ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨཨ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack111ll11lll_opy_)
            if name in [bstack1ll11ll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣཀྵ"), bstack1ll11ll_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣཪ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1ll11ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢཫ"), bstack1ll11ll_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠢཬ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1ll11ll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ཭")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111l1lll1l_opy_(
                name=name,
                uuid=bstack111ll11lll_opy_,
                started_at=bstack11l1l1l1l1_opy_(),
                file_path=file_path,
                framework=bstack1ll11ll_opy_ (u"ࠤࡅࡩ࡭ࡧࡶࡦࠤ཮"),
                bstack111l1lllll_opy_=bstack1l11ll1l_opy_.bstack111ll1ll1l_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1ll11ll_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦ཯"),
                hook_type=name
            )
            self.tests[bstack111ll11lll_opy_][bstack1ll11ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠢ཰")] = hook_data
            current_test_id = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠧࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤཱ"), None)
            if current_test_id:
                hook_data.bstack111l1lll11_opy_(current_test_id)
            if name == bstack1ll11ll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ིࠥ"):
                threading.current_thread().before_all_hook_uuid = bstack111ll11lll_opy_
            threading.current_thread().current_hook_uuid = bstack111ll11lll_opy_
            bstack1l11ll1l_opy_.bstack111ll1ll11_opy_(bstack1ll11ll_opy_ (u"ࠢࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤཱིࠣ"), hook_data)
        except Exception as e:
            logger.debug(bstack1ll11ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤ࡭ࡵ࡯࡬ࠢࡨࡺࡪࡴࡴࡴ࠮ࠣ࡬ࡴࡵ࡫ࠡࡰࡤࡱࡪࡀࠠࠦࡵ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠪࡹུࠢ"), name, e)
    def bstack1ll11lll1l_opy_(self, attrs):
        bstack111ll1llll_opy_ = bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩཱུ࠭"), None)
        hook_data = self.tests[bstack111ll1llll_opy_][bstack1ll11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྲྀ")]
        status = bstack1ll11ll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦཷ")
        exception = None
        bstack111ll1111l_opy_ = None
        if hook_data.name == bstack1ll11ll_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣླྀ"):
            self.bstack111ll1l111_opy_.reset()
            bstack111lll11ll_opy_ = self.tests[bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ཹ"), None)][bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣེࠪ")].result.result
            if bstack111lll11ll_opy_ == bstack1ll11ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤཻࠣ"):
                if attrs.hook_failures == 1:
                    status = bstack1ll11ll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤོ")
                elif attrs.hook_failures == 2:
                    status = bstack1ll11ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦཽࠥ")
            elif attrs.aborted:
                status = bstack1ll11ll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦཾ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1ll11ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩཿ") and attrs.hook_failures == 1:
                status = bstack1ll11ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨྀ")
            elif hasattr(attrs, bstack1ll11ll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ཱྀࠧ")) and attrs.error_message:
                status = bstack1ll11ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣྂ")
            bstack111ll1111l_opy_, exception = self._111ll11ll1_opy_(attrs)
        bstack111ll11l11_opy_ = Result(result=status, exception=exception, bstack111ll1l1l1_opy_=[bstack111ll1111l_opy_])
        hook_data.stop(time=bstack11l1l1l1l1_opy_(), duration=0, result=bstack111ll11l11_opy_)
        bstack1l11ll1l_opy_.bstack111ll1ll11_opy_(bstack1ll11ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫྃ"), self.tests[bstack111ll1llll_opy_][bstack1ll11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ྄࠭")])
        threading.current_thread().current_hook_uuid = None
    def _111ll11ll1_opy_(self, attrs):
        try:
            import traceback
            bstack11lll11l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111ll1111l_opy_ = bstack11lll11l_opy_[-1] if bstack11lll11l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1ll11ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡴࡶࡲࡱࠥࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࠣ྅"))
            bstack111ll1111l_opy_ = None
            exception = None
        return bstack111ll1111l_opy_, exception