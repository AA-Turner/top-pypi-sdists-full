# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11l111111l_opy_ import bstack111ll1l1ll_opy_, bstack111llllll1_opy_
from bstack_utils.bstack111lll1l1l_opy_ import bstack11l1ll111_opy_
from bstack_utils.helper import bstack1ll11l1l1l_opy_, bstack1llllllll1_opy_, Result
from bstack_utils.bstack111lllll1l_opy_ import bstack11111ll1l_opy_
from bstack_utils.capture import bstack111ll1lll1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l1111l1l_opy_:
    def __init__(self):
        self.bstack111lll11ll_opy_ = bstack111ll1lll1_opy_(self.bstack11l1111111_opy_)
        self.tests = {}
    @staticmethod
    def bstack11l1111111_opy_(log):
        if not (log[bstack111lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭໳")] and log[bstack111lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ໴")].strip()):
            return
        active = bstack11l1ll111_opy_.bstack111ll1ll1l_opy_()
        log = {
            bstack111lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭໵"): log[bstack111lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ໶")],
            bstack111lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ໷"): bstack1llllllll1_opy_(),
            bstack111lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ໸"): log[bstack111lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ໹")],
        }
        if active:
            if active[bstack111lll_opy_ (u"ࠬࡺࡹࡱࡧࠪ໺")] == bstack111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ໻"):
                log[bstack111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ໼")] = active[bstack111lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ໽")]
            elif active[bstack111lll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ໾")] == bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࠨ໿"):
                log[bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫༀ")] = active[bstack111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ༁")]
        bstack11111ll1l_opy_.bstack11l1111ll_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack111lll11ll_opy_.start()
        driver = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ༂"), None)
        bstack11l111111l_opy_ = bstack111llllll1_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1llllllll1_opy_(),
            file_path=attrs.feature.filename,
            result=bstack111lll_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣ༃"),
            framework=bstack111lll_opy_ (u"ࠨࡄࡨ࡬ࡦࡼࡥࠨ༄"),
            scope=[attrs.feature.name],
            bstack111lll1l11_opy_=bstack11111ll1l_opy_.bstack111lll1lll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༅")] = bstack11l111111l_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack11111ll1l_opy_.bstack111lllllll_opy_(bstack111lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ༆"), bstack11l111111l_opy_)
    def end_test(self, attrs):
        bstack11l11111l1_opy_ = {
            bstack111lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ༇"): attrs.feature.name,
            bstack111lll_opy_ (u"ࠧࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥ༈"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11l111111l_opy_ = self.tests[current_test_uuid][bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ༉")]
        meta = {
            bstack111lll_opy_ (u"ࠢࡧࡧࡤࡸࡺࡸࡥࠣ༊"): bstack11l11111l1_opy_,
            bstack111lll_opy_ (u"ࠣࡵࡷࡩࡵࡹࠢ་"): bstack11l111111l_opy_.meta.get(bstack111lll_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ༌"), []),
            bstack111lll_opy_ (u"ࠥࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ།"): {
                bstack111lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ༎"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11l111111l_opy_.bstack111ll1ll11_opy_(meta)
        bstack11l111111l_opy_.bstack111lll1ll1_opy_(bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ༏"), []))
        bstack111lll1111_opy_, exception = self._111lll11l1_opy_(attrs)
        bstack111llll1ll_opy_ = Result(result=attrs.status.name, exception=exception, bstack111lll111l_opy_=[bstack111lll1111_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ༐")].stop(time=bstack1llllllll1_opy_(), duration=int(attrs.duration)*1000, result=bstack111llll1ll_opy_)
        bstack11111ll1l_opy_.bstack111lllllll_opy_(bstack111lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ༑"), self.tests[threading.current_thread().current_test_uuid][bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ༒")])
    def bstack11l11l1l1l_opy_(self, attrs):
        bstack111llll111_opy_ = {
            bstack111lll_opy_ (u"ࠩ࡬ࡨࠬ༓"): uuid4().__str__(),
            bstack111lll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ༔"): attrs.keyword,
            bstack111lll_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫ༕"): [],
            bstack111lll_opy_ (u"ࠬࡺࡥࡹࡶࠪ༖"): attrs.name,
            bstack111lll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ༗"): bstack1llllllll1_opy_(),
            bstack111lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺ༘ࠧ"): bstack111lll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨ༙ࠩ"),
            bstack111lll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ༚"): bstack111lll_opy_ (u"ࠪࠫ༛")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ༜")].add_step(bstack111llll111_opy_)
        threading.current_thread().current_step_uuid = bstack111llll111_opy_[bstack111lll_opy_ (u"ࠬ࡯ࡤࠨ༝")]
    def bstack1ll1ll1lll_opy_(self, attrs):
        current_test_id = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ༞"), None)
        current_step_uuid = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫ༟"), None)
        bstack111lll1111_opy_, exception = self._111lll11l1_opy_(attrs)
        bstack111llll1ll_opy_ = Result(result=attrs.status.name, exception=exception, bstack111lll111l_opy_=[bstack111lll1111_opy_])
        self.tests[current_test_id][bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ༠")].bstack111ll1l1l1_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111llll1ll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l1l111l11_opy_(self, name, attrs):
        try:
            bstack111ll1llll_opy_ = uuid4().__str__()
            self.tests[bstack111ll1llll_opy_] = {}
            self.bstack111lll11ll_opy_.start()
            scopes = []
            driver = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ༡"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack111lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ༢")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack111ll1llll_opy_)
            if name in [bstack111lll_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ༣"), bstack111lll_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣ༤")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack111lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ༥"), bstack111lll_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ༦")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack111lll_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ༧")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111ll1l1ll_opy_(
                name=name,
                uuid=bstack111ll1llll_opy_,
                started_at=bstack1llllllll1_opy_(),
                file_path=file_path,
                framework=bstack111lll_opy_ (u"ࠤࡅࡩ࡭ࡧࡶࡦࠤ༨"),
                bstack111lll1l11_opy_=bstack11111ll1l_opy_.bstack111lll1lll_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack111lll_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦ༩"),
                hook_type=name
            )
            self.tests[bstack111ll1llll_opy_][bstack111lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠢ༪")] = hook_data
            current_test_id = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠧࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤ༫"), None)
            if current_test_id:
                hook_data.bstack111llll1l1_opy_(current_test_id)
            if name == bstack111lll_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ༬"):
                threading.current_thread().before_all_hook_uuid = bstack111ll1llll_opy_
            threading.current_thread().current_hook_uuid = bstack111ll1llll_opy_
            bstack11111ll1l_opy_.bstack111lllllll_opy_(bstack111lll_opy_ (u"ࠢࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠣ༭"), hook_data)
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤ࡭ࡵ࡯࡬ࠢࡨࡺࡪࡴࡴࡴ࠮ࠣ࡬ࡴࡵ࡫ࠡࡰࡤࡱࡪࡀࠠࠦࡵ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠪࡹࠢ༮"), name, e)
    def bstack1lll11l1l_opy_(self, attrs):
        bstack111llll11l_opy_ = bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭༯"), None)
        hook_data = self.tests[bstack111llll11l_opy_][bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༰")]
        status = bstack111lll_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ༱")
        exception = None
        bstack111lll1111_opy_ = None
        if hook_data.name == bstack111lll_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣ༲"):
            self.bstack111lll11ll_opy_.reset()
            bstack111lllll11_opy_ = self.tests[bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭༳"), None)][bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ༴")].result.result
            if bstack111lllll11_opy_ == bstack111lll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤ༵ࠣ"):
                if attrs.hook_failures == 1:
                    status = bstack111lll_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ༶")
                elif attrs.hook_failures == 2:
                    status = bstack111lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦ༷ࠥ")
            elif attrs.aborted:
                status = bstack111lll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ༸")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack111lll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭༹ࠩ") and attrs.hook_failures == 1:
                status = bstack111lll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ༺")
            elif hasattr(attrs, bstack111lll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧ༻")) and attrs.error_message:
                status = bstack111lll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ༼")
            bstack111lll1111_opy_, exception = self._111lll11l1_opy_(attrs)
        bstack111llll1ll_opy_ = Result(result=status, exception=exception, bstack111lll111l_opy_=[bstack111lll1111_opy_])
        hook_data.stop(time=bstack1llllllll1_opy_(), duration=0, result=bstack111llll1ll_opy_)
        bstack11111ll1l_opy_.bstack111lllllll_opy_(bstack111lll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ༽"), self.tests[bstack111llll11l_opy_][bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༾")])
        threading.current_thread().current_hook_uuid = None
    def _111lll11l1_opy_(self, attrs):
        try:
            import traceback
            bstack11ll1l11_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111lll1111_opy_ = bstack11ll1l11_opy_[-1] if bstack11ll1l11_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack111lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡴࡶࡲࡱࠥࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࠣ༿"))
            bstack111lll1111_opy_ = None
            exception = None
        return bstack111lll1111_opy_, exception