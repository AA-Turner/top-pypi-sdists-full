# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111ll1lll1_opy_ import bstack111ll1ll11_opy_, bstack111ll1l1ll_opy_
from bstack_utils.bstack111lll11l1_opy_ import bstack1ll11l1ll1_opy_
from bstack_utils.helper import bstack1l11l1l1ll_opy_, bstack11l11ll1l1_opy_, Result
from bstack_utils.bstack111lll1lll_opy_ import bstack1lll11111l_opy_
from bstack_utils.capture import bstack111ll1l1l1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l11lll11l_opy_:
    def __init__(self):
        self.bstack111lll1ll1_opy_ = bstack111ll1l1l1_opy_(self.bstack111ll1llll_opy_)
        self.tests = {}
    @staticmethod
    def bstack111ll1llll_opy_(log):
        if not (log[bstack1111lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦ༵ࠩ")] and log[bstack1111lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༶")].strip()):
            return
        active = bstack1ll11l1ll1_opy_.bstack111ll11ll1_opy_()
        log = {
            bstack1111lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭༷ࠩ"): log[bstack1111lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ༸")],
            bstack1111lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ༹"): bstack11l11ll1l1_opy_(),
            bstack1111lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ༺"): log[bstack1111lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༻")],
        }
        if active:
            if active[bstack1111lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭༼")] == bstack1111lll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ༽"):
                log[bstack1111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ༾")] = active[bstack1111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ༿")]
            elif active[bstack1111lll_opy_ (u"ࠬࡺࡹࡱࡧࠪཀ")] == bstack1111lll_opy_ (u"࠭ࡴࡦࡵࡷࠫཁ"):
                log[bstack1111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧག")] = active[bstack1111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨགྷ")]
        bstack1lll11111l_opy_.bstack1lll1ll1ll_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111lll1ll1_opy_.start()
        driver = bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨང"), None)
        bstack111ll1lll1_opy_ = bstack111ll1l1ll_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack11l11ll1l1_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1111lll_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦཅ"),
            framework=bstack1111lll_opy_ (u"ࠫࡇ࡫ࡨࡢࡸࡨࠫཆ"),
            scope=[attrs.feature.name],
            bstack111ll11lll_opy_=bstack1lll11111l_opy_.bstack111ll111l1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨཇ")] = bstack111ll1lll1_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack1lll11111l_opy_.bstack111llll111_opy_(bstack1111lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ཈"), bstack111ll1lll1_opy_)
    def end_test(self, attrs):
        bstack111llll11l_opy_ = {
            bstack1111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧཉ"): attrs.feature.name,
            bstack1111lll_opy_ (u"ࠣࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨཊ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111ll1lll1_opy_ = self.tests[current_test_uuid][bstack1111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬཋ")]
        meta = {
            bstack1111lll_opy_ (u"ࠥࡪࡪࡧࡴࡶࡴࡨࠦཌ"): bstack111llll11l_opy_,
            bstack1111lll_opy_ (u"ࠦࡸࡺࡥࡱࡵࠥཌྷ"): bstack111ll1lll1_opy_.meta.get(bstack1111lll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫཎ"), []),
            bstack1111lll_opy_ (u"ࠨࡳࡤࡧࡱࡥࡷ࡯࡯ࠣཏ"): {
                bstack1111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧཐ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111ll1lll1_opy_.bstack111ll1111l_opy_(meta)
        bstack111ll1lll1_opy_.bstack111lll11ll_opy_(bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ད"), []))
        bstack111ll1l11l_opy_, exception = self._111lll111l_opy_(attrs)
        bstack111ll1l111_opy_ = Result(result=attrs.status.name, exception=exception, bstack111ll111ll_opy_=[bstack111ll1l11l_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬདྷ")].stop(time=bstack11l11ll1l1_opy_(), duration=int(attrs.duration)*1000, result=bstack111ll1l111_opy_)
        bstack1lll11111l_opy_.bstack111llll111_opy_(bstack1111lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬན"), self.tests[threading.current_thread().current_test_uuid][bstack1111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧཔ")])
    def bstack11lll1l11l_opy_(self, attrs):
        bstack111ll1ll1l_opy_ = {
            bstack1111lll_opy_ (u"ࠬ࡯ࡤࠨཕ"): uuid4().__str__(),
            bstack1111lll_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧབ"): attrs.keyword,
            bstack1111lll_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧབྷ"): [],
            bstack1111lll_opy_ (u"ࠨࡶࡨࡼࡹ࠭མ"): attrs.name,
            bstack1111lll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ཙ"): bstack11l11ll1l1_opy_(),
            bstack1111lll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪཚ"): bstack1111lll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬཛ"),
            bstack1111lll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪཛྷ"): bstack1111lll_opy_ (u"࠭ࠧཝ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཞ")].add_step(bstack111ll1ll1l_opy_)
        threading.current_thread().current_step_uuid = bstack111ll1ll1l_opy_[bstack1111lll_opy_ (u"ࠨ࡫ࡧࠫཟ")]
    def bstack1ll11111_opy_(self, attrs):
        current_test_id = bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭འ"), None)
        current_step_uuid = bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡺࡥࡱࡡࡸࡹ࡮ࡪࠧཡ"), None)
        bstack111ll1l11l_opy_, exception = self._111lll111l_opy_(attrs)
        bstack111ll1l111_opy_ = Result(result=attrs.status.name, exception=exception, bstack111ll111ll_opy_=[bstack111ll1l11l_opy_])
        self.tests[current_test_id][bstack1111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧར")].bstack111ll11l1l_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111ll1l111_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1ll11lll_opy_(self, name, attrs):
        try:
            bstack111ll11l11_opy_ = uuid4().__str__()
            self.tests[bstack111ll11l11_opy_] = {}
            self.bstack111lll1ll1_opy_.start()
            scopes = []
            driver = bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫལ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1111lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫཤ")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack111ll11l11_opy_)
            if name in [bstack1111lll_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦཥ"), bstack1111lll_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦས")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1111lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥཧ"), bstack1111lll_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠥཨ")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1111lll_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬཀྵ")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111ll1ll11_opy_(
                name=name,
                uuid=bstack111ll11l11_opy_,
                started_at=bstack11l11ll1l1_opy_(),
                file_path=file_path,
                framework=bstack1111lll_opy_ (u"ࠧࡈࡥࡩࡣࡹࡩࠧཪ"),
                bstack111ll11lll_opy_=bstack1lll11111l_opy_.bstack111ll111l1_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1111lll_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢཫ"),
                hook_type=name
            )
            self.tests[bstack111ll11l11_opy_][bstack1111lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡡࡵࡣࠥཬ")] = hook_data
            current_test_id = bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠣࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧ཭"), None)
            if current_test_id:
                hook_data.bstack111lll1l1l_opy_(current_test_id)
            if name == bstack1111lll_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ཮"):
                threading.current_thread().before_all_hook_uuid = bstack111ll11l11_opy_
            threading.current_thread().current_hook_uuid = bstack111ll11l11_opy_
            bstack1lll11111l_opy_.bstack111llll111_opy_(bstack1111lll_opy_ (u"ࠥࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠦ཯"), hook_data)
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠࡩࡱࡲ࡯ࠥ࡫ࡶࡦࡰࡷࡷ࠱ࠦࡨࡰࡱ࡮ࠤࡳࡧ࡭ࡦ࠼ࠣࠩࡸ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠦࡵࠥ཰"), name, e)
    def bstack1l11ll111l_opy_(self, attrs):
        bstack111lll1111_opy_ = bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥཱࠩ"), None)
        hook_data = self.tests[bstack111lll1111_opy_][bstack1111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢིࠩ")]
        status = bstack1111lll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪཱིࠢ")
        exception = None
        bstack111ll1l11l_opy_ = None
        if hook_data.name == bstack1111lll_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ུࠦ"):
            self.bstack111lll1ll1_opy_.reset()
            bstack111lll1l11_opy_ = self.tests[bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥཱུࠩ"), None)][bstack1111lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྲྀ")].result.result
            if bstack111lll1l11_opy_ == bstack1111lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦཷ"):
                if attrs.hook_failures == 1:
                    status = bstack1111lll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧླྀ")
                elif attrs.hook_failures == 2:
                    status = bstack1111lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨཹ")
            elif attrs.aborted:
                status = bstack1111lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪེࠢ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1111lll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰཻࠬ") and attrs.hook_failures == 1:
                status = bstack1111lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤོ")
            elif hasattr(attrs, bstack1111lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧཽࠪ")) and attrs.error_message:
                status = bstack1111lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦཾ")
            bstack111ll1l11l_opy_, exception = self._111lll111l_opy_(attrs)
        bstack111ll1l111_opy_ = Result(result=status, exception=exception, bstack111ll111ll_opy_=[bstack111ll1l11l_opy_])
        hook_data.stop(time=bstack11l11ll1l1_opy_(), duration=0, result=bstack111ll1l111_opy_)
        bstack1lll11111l_opy_.bstack111llll111_opy_(bstack1111lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧཿ"), self.tests[bstack111lll1111_opy_][bstack1111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢྀࠩ")])
        threading.current_thread().current_hook_uuid = None
    def _111lll111l_opy_(self, attrs):
        try:
            import traceback
            bstack1l1l11ll1_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111ll1l11l_opy_ = bstack1l1l11ll1_opy_[-1] if bstack1l1l11ll1_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1111lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ཱྀࠦ"))
            bstack111ll1l11l_opy_ = None
            exception = None
        return bstack111ll1l11l_opy_, exception