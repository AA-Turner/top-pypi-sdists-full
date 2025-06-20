# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111lll1ll1_opy_ import bstack111lll11ll_opy_, bstack111ll11ll1_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack11l1ll11_opy_
from bstack_utils.helper import bstack111ll1lll_opy_, bstack1l11l11ll_opy_, Result
from bstack_utils.bstack111lllll1l_opy_ import bstack1l1l1l1ll_opy_
from bstack_utils.capture import bstack111ll1lll1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11l111ll11_opy_:
    def __init__(self):
        self.bstack111ll1llll_opy_ = bstack111ll1lll1_opy_(self.bstack111ll1l1l1_opy_)
        self.tests = {}
    @staticmethod
    def bstack111ll1l1l1_opy_(log):
        if not (log[bstack11ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ໴")] and log[bstack11ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ໵")].strip()):
            return
        active = bstack11l1ll11_opy_.bstack111llll1l1_opy_()
        log = {
            bstack11ll11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ໶"): log[bstack11ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ໷")],
            bstack11ll11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭໸"): bstack1l11l11ll_opy_(),
            bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ໹"): log[bstack11ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭໺")],
        }
        if active:
            if active[bstack11ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫ໻")] == bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ໼"):
                log[bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ໽")] = active[bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ໾")]
            elif active[bstack11ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨ໿")] == bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩༀ"):
                log[bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ༁")] = active[bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭༂")]
        bstack1l1l1l1ll_opy_.bstack11ll1lllll_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111ll1llll_opy_.start()
        driver = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭༃"), None)
        bstack111lll1ll1_opy_ = bstack111ll11ll1_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1l11l11ll_opy_(),
            file_path=attrs.feature.filename,
            result=bstack11ll11_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤ༄"),
            framework=bstack11ll11_opy_ (u"ࠩࡅࡩ࡭ࡧࡶࡦࠩ༅"),
            scope=[attrs.feature.name],
            bstack111lll11l1_opy_=bstack1l1l1l1ll_opy_.bstack111ll1l111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༆")] = bstack111lll1ll1_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack1l1l1l1ll_opy_.bstack111ll1l11l_opy_(bstack11ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ༇"), bstack111lll1ll1_opy_)
    def end_test(self, attrs):
        bstack111ll11l1l_opy_ = {
            bstack11ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ༈"): attrs.feature.name,
            bstack11ll11_opy_ (u"ࠨࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦ༉"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111lll1ll1_opy_ = self.tests[current_test_uuid][bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ༊")]
        meta = {
            bstack11ll11_opy_ (u"ࠣࡨࡨࡥࡹࡻࡲࡦࠤ་"): bstack111ll11l1l_opy_,
            bstack11ll11_opy_ (u"ࠤࡶࡸࡪࡶࡳࠣ༌"): bstack111lll1ll1_opy_.meta.get(bstack11ll11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ།"), []),
            bstack11ll11_opy_ (u"ࠦࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ༎"): {
                bstack11ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ༏"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111lll1ll1_opy_.bstack111lll1l1l_opy_(meta)
        bstack111lll1ll1_opy_.bstack111llll1ll_opy_(bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ༐"), []))
        bstack111lll1111_opy_, exception = self._111llll11l_opy_(attrs)
        bstack111lll1l11_opy_ = Result(result=attrs.status.name, exception=exception, bstack111ll1ll1l_opy_=[bstack111lll1111_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ༑")].stop(time=bstack1l11l11ll_opy_(), duration=int(attrs.duration)*1000, result=bstack111lll1l11_opy_)
        bstack1l1l1l1ll_opy_.bstack111ll1l11l_opy_(bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ༒"), self.tests[threading.current_thread().current_test_uuid][bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༓")])
    def bstack11l1llll11_opy_(self, attrs):
        bstack111ll1l1ll_opy_ = {
            bstack11ll11_opy_ (u"ࠪ࡭ࡩ࠭༔"): uuid4().__str__(),
            bstack11ll11_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬ༕"): attrs.keyword,
            bstack11ll11_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬ༖"): [],
            bstack11ll11_opy_ (u"࠭ࡴࡦࡺࡷࠫ༗"): attrs.name,
            bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷ༘ࠫ"): bstack1l11l11ll_opy_(),
            bstack11ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ༙"): bstack11ll11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ༚"),
            bstack11ll11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ༛"): bstack11ll11_opy_ (u"ࠫࠬ༜")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ༝")].add_step(bstack111ll1l1ll_opy_)
        threading.current_thread().current_step_uuid = bstack111ll1l1ll_opy_[bstack11ll11_opy_ (u"࠭ࡩࡥࠩ༞")]
    def bstack1lll11lll_opy_(self, attrs):
        current_test_id = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ༟"), None)
        current_step_uuid = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬ༠"), None)
        bstack111lll1111_opy_, exception = self._111llll11l_opy_(attrs)
        bstack111lll1l11_opy_ = Result(result=attrs.status.name, exception=exception, bstack111ll1ll1l_opy_=[bstack111lll1111_opy_])
        self.tests[current_test_id][bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༡")].bstack111ll1ll11_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111lll1l11_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1ll11111_opy_(self, name, attrs):
        try:
            bstack111llll111_opy_ = uuid4().__str__()
            self.tests[bstack111llll111_opy_] = {}
            self.bstack111ll1llll_opy_.start()
            scopes = []
            driver = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ༢"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ༣")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack111llll111_opy_)
            if name in [bstack11ll11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ༤"), bstack11ll11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ༥")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack11ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣ༦"), bstack11ll11_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠣ༧")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack11ll11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪ༨")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111lll11ll_opy_(
                name=name,
                uuid=bstack111llll111_opy_,
                started_at=bstack1l11l11ll_opy_(),
                file_path=file_path,
                framework=bstack11ll11_opy_ (u"ࠥࡆࡪ࡮ࡡࡷࡧࠥ༩"),
                bstack111lll11l1_opy_=bstack1l1l1l1ll_opy_.bstack111ll1l111_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack11ll11_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ༪"),
                hook_type=name
            )
            self.tests[bstack111llll111_opy_][bstack11ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡦࡺࡡࠣ༫")] = hook_data
            current_test_id = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠨࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥ༬"), None)
            if current_test_id:
                hook_data.bstack111lll1lll_opy_(current_test_id)
            if name == bstack11ll11_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ༭"):
                threading.current_thread().before_all_hook_uuid = bstack111llll111_opy_
            threading.current_thread().current_hook_uuid = bstack111llll111_opy_
            bstack1l1l1l1ll_opy_.bstack111ll1l11l_opy_(bstack11ll11_opy_ (u"ࠣࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠤ༮"), hook_data)
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣ࡭ࡳࠦࡳࡵࡣࡵࡸࠥ࡮࡯ࡰ࡭ࠣࡩࡻ࡫࡮ࡵࡵ࠯ࠤ࡭ࡵ࡯࡬ࠢࡱࡥࡲ࡫࠺ࠡࠧࡶ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠫࡳࠣ༯"), name, e)
    def bstack1l1lll1l_opy_(self, attrs):
        bstack111ll11lll_opy_ = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ༰"), None)
        hook_data = self.tests[bstack111ll11lll_opy_][bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ༱")]
        status = bstack11ll11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ༲")
        exception = None
        bstack111lll1111_opy_ = None
        if hook_data.name == bstack11ll11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠤ༳"):
            self.bstack111ll1llll_opy_.reset()
            bstack111lllll11_opy_ = self.tests[bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ༴"), None)][bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤ༵ࠫ")].result.result
            if bstack111lllll11_opy_ == bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ༶"):
                if attrs.hook_failures == 1:
                    status = bstack11ll11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦ༷ࠥ")
                elif attrs.hook_failures == 2:
                    status = bstack11ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ༸")
            elif attrs.aborted:
                status = bstack11ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨ༹ࠧ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11ll11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ༺") and attrs.hook_failures == 1:
                status = bstack11ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ༻")
            elif hasattr(attrs, bstack11ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨ༼")) and attrs.error_message:
                status = bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ༽")
            bstack111lll1111_opy_, exception = self._111llll11l_opy_(attrs)
        bstack111lll1l11_opy_ = Result(result=status, exception=exception, bstack111ll1ll1l_opy_=[bstack111lll1111_opy_])
        hook_data.stop(time=bstack1l11l11ll_opy_(), duration=0, result=bstack111lll1l11_opy_)
        bstack1l1l1l1ll_opy_.bstack111ll1l11l_opy_(bstack11ll11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ༾"), self.tests[bstack111ll11lll_opy_][bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ༿")])
        threading.current_thread().current_hook_uuid = None
    def _111llll11l_opy_(self, attrs):
        try:
            import traceback
            bstack1ll1ll11l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111lll1111_opy_ = bstack1ll1ll11l_opy_[-1] if bstack1ll1ll11l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡣࡶࡵࡷࡳࡲࠦࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࠤཀ"))
            bstack111lll1111_opy_ = None
            exception = None
        return bstack111lll1111_opy_, exception