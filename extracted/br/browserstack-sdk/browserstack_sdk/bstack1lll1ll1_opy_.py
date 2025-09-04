# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111ll1l1ll_opy_ import bstack111lll1l11_opy_, bstack111l1lllll_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack1ll11lll1_opy_
from bstack_utils.helper import bstack1l11l1lll_opy_, bstack1ll111ll1l_opy_, Result
from bstack_utils.bstack111lll111l_opy_ import bstack11l1lllll1_opy_
from bstack_utils.capture import bstack111ll1ll1l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1lll1ll1_opy_:
    def __init__(self):
        self.bstack111lll11l1_opy_ = bstack111ll1ll1l_opy_(self.bstack111ll1llll_opy_)
        self.tests = {}
    @staticmethod
    def bstack111ll1llll_opy_(log):
        if not (log[bstack1111l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ༺")] and log[bstack1111l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༻")].strip()):
            return
        active = bstack1ll11lll1_opy_.bstack111ll1l1l1_opy_()
        log = {
            bstack1111l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ༼"): log[bstack1111l1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ༽")],
            bstack1111l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭༾"): bstack1ll111ll1l_opy_(),
            bstack1111l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༿"): log[bstack1111l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཀ")],
        }
        if active:
            if active[bstack1111l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫཁ")] == bstack1111l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬག"):
                log[bstack1111l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨགྷ")] = active[bstack1111l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩང")]
            elif active[bstack1111l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨཅ")] == bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩཆ"):
                log[bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬཇ")] = active[bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭཈")]
        bstack11l1lllll1_opy_.bstack11l11l1l1l_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111lll11l1_opy_.start()
        driver = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ཉ"), None)
        bstack111ll1l1ll_opy_ = bstack111l1lllll_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1ll111ll1l_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1111l1l_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤཊ"),
            framework=bstack1111l1l_opy_ (u"ࠩࡅࡩ࡭ࡧࡶࡦࠩཋ"),
            scope=[attrs.feature.name],
            bstack111lll11ll_opy_=bstack11l1lllll1_opy_.bstack111ll11ll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ཌ")] = bstack111ll1l1ll_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack11l1lllll1_opy_.bstack111ll11111_opy_(bstack1111l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬཌྷ"), bstack111ll1l1ll_opy_)
    def end_test(self, attrs):
        bstack111ll111l1_opy_ = {
            bstack1111l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥཎ"): attrs.feature.name,
            bstack1111l1l_opy_ (u"ࠨࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦཏ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111ll1l1ll_opy_ = self.tests[current_test_uuid][bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཐ")]
        meta = {
            bstack1111l1l_opy_ (u"ࠣࡨࡨࡥࡹࡻࡲࡦࠤད"): bstack111ll111l1_opy_,
            bstack1111l1l_opy_ (u"ࠤࡶࡸࡪࡶࡳࠣདྷ"): bstack111ll1l1ll_opy_.meta.get(bstack1111l1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩན"), []),
            bstack1111l1l_opy_ (u"ࠦࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨཔ"): {
                bstack1111l1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥཕ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111ll1l1ll_opy_.bstack111l1lll1l_opy_(meta)
        bstack111ll1l1ll_opy_.bstack111l1lll11_opy_(bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫབ"), []))
        bstack111ll11lll_opy_, exception = self._111ll111ll_opy_(attrs)
        bstack111ll1lll1_opy_ = Result(result=attrs.status.name, exception=exception, bstack111ll1111l_opy_=[bstack111ll11lll_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪབྷ")].stop(time=bstack1ll111ll1l_opy_(), duration=int(attrs.duration)*1000, result=bstack111ll1lll1_opy_)
        bstack11l1lllll1_opy_.bstack111ll11111_opy_(bstack1111l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪམ"), self.tests[threading.current_thread().current_test_uuid][bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬཙ")])
    def bstack11ll11l1_opy_(self, attrs):
        bstack111ll11l11_opy_ = {
            bstack1111l1l_opy_ (u"ࠪ࡭ࡩ࠭ཚ"): uuid4().__str__(),
            bstack1111l1l_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬཛ"): attrs.keyword,
            bstack1111l1l_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬཛྷ"): [],
            bstack1111l1l_opy_ (u"࠭ࡴࡦࡺࡷࠫཝ"): attrs.name,
            bstack1111l1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫཞ"): bstack1ll111ll1l_opy_(),
            bstack1111l1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨཟ"): bstack1111l1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪའ"),
            bstack1111l1l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨཡ"): bstack1111l1l_opy_ (u"ࠫࠬར")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨལ")].add_step(bstack111ll11l11_opy_)
        threading.current_thread().current_step_uuid = bstack111ll11l11_opy_[bstack1111l1l_opy_ (u"࠭ࡩࡥࠩཤ")]
    def bstack11l11lll11_opy_(self, attrs):
        current_test_id = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫཥ"), None)
        current_step_uuid = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬས"), None)
        bstack111ll11lll_opy_, exception = self._111ll111ll_opy_(attrs)
        bstack111ll1lll1_opy_ = Result(result=attrs.status.name, exception=exception, bstack111ll1111l_opy_=[bstack111ll11lll_opy_])
        self.tests[current_test_id][bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬཧ")].bstack111ll1l11l_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111ll1lll1_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l1ll111_opy_(self, name, attrs):
        try:
            bstack111ll11l1l_opy_ = uuid4().__str__()
            self.tests[bstack111ll11l1l_opy_] = {}
            self.bstack111lll11l1_opy_.start()
            scopes = []
            driver = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩཨ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1111l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩཀྵ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack111ll11l1l_opy_)
            if name in [bstack1111l1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤཪ"), bstack1111l1l_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤཫ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1111l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣཬ"), bstack1111l1l_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠣ཭")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1111l1l_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ཮")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111lll1l11_opy_(
                name=name,
                uuid=bstack111ll11l1l_opy_,
                started_at=bstack1ll111ll1l_opy_(),
                file_path=file_path,
                framework=bstack1111l1l_opy_ (u"ࠥࡆࡪ࡮ࡡࡷࡧࠥ཯"),
                bstack111lll11ll_opy_=bstack11l1lllll1_opy_.bstack111ll11ll1_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1111l1l_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ཰"),
                hook_type=name
            )
            self.tests[bstack111ll11l1l_opy_][bstack1111l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡦࡺࡡཱࠣ")] = hook_data
            current_test_id = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠨࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦིࠥ"), None)
            if current_test_id:
                hook_data.bstack111ll1l111_opy_(current_test_id)
            if name == bstack1111l1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ཱིࠦ"):
                threading.current_thread().before_all_hook_uuid = bstack111ll11l1l_opy_
            threading.current_thread().current_hook_uuid = bstack111ll11l1l_opy_
            bstack11l1lllll1_opy_.bstack111ll11111_opy_(bstack1111l1l_opy_ (u"ࠣࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤུ"), hook_data)
        except Exception as e:
            logger.debug(bstack1111l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥ࡮࡯ࡰ࡭ࠣࡩࡻ࡫࡮ࡵࡵ࠯ࠤ࡭ࡵ࡯࡬ࠢࡱࡥࡲ࡫࠺ࠡࠧࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠫࡳཱུࠣ"), name, e)
    def bstack11l1llll1l_opy_(self, attrs):
        bstack111lll1111_opy_ = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧྲྀ"), None)
        hook_data = self.tests[bstack111lll1111_opy_][bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧཷ")]
        status = bstack1111l1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧླྀ")
        exception = None
        bstack111ll11lll_opy_ = None
        if hook_data.name == bstack1111l1l_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤཹ"):
            self.bstack111lll11l1_opy_.reset()
            bstack111l1llll1_opy_ = self.tests[bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪེࠧ"), None)][bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤཻࠫ")].result.result
            if bstack111l1llll1_opy_ == bstack1111l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤོ"):
                if attrs.hook_failures == 1:
                    status = bstack1111l1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦཽࠥ")
                elif attrs.hook_failures == 2:
                    status = bstack1111l1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦཾ")
            elif attrs.aborted:
                status = bstack1111l1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧཿ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1111l1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ྀࠪ") and attrs.hook_failures == 1:
                status = bstack1111l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪཱྀࠢ")
            elif hasattr(attrs, bstack1111l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨྂ")) and attrs.error_message:
                status = bstack1111l1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤྃ")
            bstack111ll11lll_opy_, exception = self._111ll111ll_opy_(attrs)
        bstack111ll1lll1_opy_ = Result(result=status, exception=exception, bstack111ll1111l_opy_=[bstack111ll11lll_opy_])
        hook_data.stop(time=bstack1ll111ll1l_opy_(), duration=0, result=bstack111ll1lll1_opy_)
        bstack11l1lllll1_opy_.bstack111ll11111_opy_(bstack1111l1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨ྄ࠬ"), self.tests[bstack111lll1111_opy_][bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ྅")])
        threading.current_thread().current_hook_uuid = None
    def _111ll111ll_opy_(self, attrs):
        try:
            import traceback
            bstack1llllll11_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111ll11lll_opy_ = bstack1llllll11_opy_[-1] if bstack1llllll11_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1111l1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡵࡷࡳࡲࠦࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࠤ྆"))
            bstack111ll11lll_opy_ = None
            exception = None
        return bstack111ll11lll_opy_, exception