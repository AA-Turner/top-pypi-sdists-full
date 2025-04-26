# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11l1111l11_opy_ import bstack111lll1lll_opy_, bstack111lll1ll1_opy_
from bstack_utils.bstack111lllll11_opy_ import bstack111l1llll_opy_
from bstack_utils.helper import bstack11l11l1ll1_opy_, bstack11lll111l1_opy_, Result
from bstack_utils.bstack111llll11l_opy_ import bstack111ll1ll1_opy_
from bstack_utils.capture import bstack11l111ll1l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack111l1lll1_opy_:
    def __init__(self):
        self.bstack11l11111ll_opy_ = bstack11l111ll1l_opy_(self.bstack111llll111_opy_)
        self.tests = {}
    @staticmethod
    def bstack111llll111_opy_(log):
        if not (log[bstack1l11lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ໏")] and log[bstack1l11lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭໐")].strip()):
            return
        active = bstack111l1llll_opy_.bstack111llllll1_opy_()
        log = {
            bstack1l11lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ໑"): log[bstack1l11lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭໒")],
            bstack1l11lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ໓"): bstack11lll111l1_opy_(),
            bstack1l11lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ໔"): log[bstack1l11lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ໕")],
        }
        if active:
            if active[bstack1l11lll_opy_ (u"ࠫࡹࡿࡰࡦࠩ໖")] == bstack1l11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ໗"):
                log[bstack1l11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭໘")] = active[bstack1l11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ໙")]
            elif active[bstack1l11lll_opy_ (u"ࠨࡶࡼࡴࡪ࠭໚")] == bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺࠧ໛"):
                log[bstack1l11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪໜ")] = active[bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫໝ")]
        bstack111ll1ll1_opy_.bstack1l1l111ll_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack11l11111ll_opy_.start()
        driver = bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫໞ"), None)
        bstack11l1111l11_opy_ = bstack111lll1ll1_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack11lll111l1_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1l11lll_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢໟ"),
            framework=bstack1l11lll_opy_ (u"ࠧࡃࡧ࡫ࡥࡻ࡫ࠧ໠"),
            scope=[attrs.feature.name],
            bstack11l111ll11_opy_=bstack111ll1ll1_opy_.bstack11l1111lll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1l11lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ໡")] = bstack11l1111l11_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack111ll1ll1_opy_.bstack11l111l11l_opy_(bstack1l11lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ໢"), bstack11l1111l11_opy_)
    def end_test(self, attrs):
        bstack11l1111111_opy_ = {
            bstack1l11lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ໣"): attrs.feature.name,
            bstack1l11lll_opy_ (u"ࠦࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤ໤"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11l1111l11_opy_ = self.tests[current_test_uuid][bstack1l11lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ໥")]
        meta = {
            bstack1l11lll_opy_ (u"ࠨࡦࡦࡣࡷࡹࡷ࡫ࠢ໦"): bstack11l1111111_opy_,
            bstack1l11lll_opy_ (u"ࠢࡴࡶࡨࡴࡸࠨ໧"): bstack11l1111l11_opy_.meta.get(bstack1l11lll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ໨"), []),
            bstack1l11lll_opy_ (u"ࠤࡶࡧࡪࡴࡡࡳ࡫ࡲࠦ໩"): {
                bstack1l11lll_opy_ (u"ࠥࡲࡦࡳࡥࠣ໪"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11l1111l11_opy_.bstack11l111111l_opy_(meta)
        bstack11l1111l11_opy_.bstack111lllll1l_opy_(bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ໫"), []))
        bstack11l111lll1_opy_, exception = self._11l111llll_opy_(attrs)
        bstack111lllllll_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l1111ll1_opy_=[bstack11l111lll1_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1l11lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ໬")].stop(time=bstack11lll111l1_opy_(), duration=int(attrs.duration)*1000, result=bstack111lllllll_opy_)
        bstack111ll1ll1_opy_.bstack11l111l11l_opy_(bstack1l11lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ໭"), self.tests[threading.current_thread().current_test_uuid][bstack1l11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໮")])
    def bstack1l11l1111_opy_(self, attrs):
        bstack11l111l1l1_opy_ = {
            bstack1l11lll_opy_ (u"ࠨ࡫ࡧࠫ໯"): uuid4().__str__(),
            bstack1l11lll_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪ໰"): attrs.keyword,
            bstack1l11lll_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪ໱"): [],
            bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ໲"): attrs.name,
            bstack1l11lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ໳"): bstack11lll111l1_opy_(),
            bstack1l11lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭໴"): bstack1l11lll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ໵"),
            bstack1l11lll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭໶"): bstack1l11lll_opy_ (u"ࠩࠪ໷")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1l11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭໸")].add_step(bstack11l111l1l1_opy_)
        threading.current_thread().current_step_uuid = bstack11l111l1l1_opy_[bstack1l11lll_opy_ (u"ࠫ࡮ࡪࠧ໹")]
    def bstack1l1l1ll1_opy_(self, attrs):
        current_test_id = bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ໺"), None)
        current_step_uuid = bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪ໻"), None)
        bstack11l111lll1_opy_, exception = self._11l111llll_opy_(attrs)
        bstack111lllllll_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l1111ll1_opy_=[bstack11l111lll1_opy_])
        self.tests[current_test_id][bstack1l11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໼")].bstack11l111l1ll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack111lllllll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l11lllll_opy_(self, name, attrs):
        try:
            bstack11l1111l1l_opy_ = uuid4().__str__()
            self.tests[bstack11l1111l1l_opy_] = {}
            self.bstack11l11111ll_opy_.start()
            scopes = []
            driver = bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ໽"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1l11lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ໾")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11l1111l1l_opy_)
            if name in [bstack1l11lll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ໿"), bstack1l11lll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠢༀ")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1l11lll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ༁"), bstack1l11lll_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ༂")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1l11lll_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ༃")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111lll1lll_opy_(
                name=name,
                uuid=bstack11l1111l1l_opy_,
                started_at=bstack11lll111l1_opy_(),
                file_path=file_path,
                framework=bstack1l11lll_opy_ (u"ࠣࡄࡨ࡬ࡦࡼࡥࠣ༄"),
                bstack11l111ll11_opy_=bstack111ll1ll1_opy_.bstack11l1111lll_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1l11lll_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥ༅"),
                hook_type=name
            )
            self.tests[bstack11l1111l1l_opy_][bstack1l11lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡤࡸࡦࠨ༆")] = hook_data
            current_test_id = bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠦࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠣ༇"), None)
            if current_test_id:
                hook_data.bstack111llll1ll_opy_(current_test_id)
            if name == bstack1l11lll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ༈"):
                threading.current_thread().before_all_hook_uuid = bstack11l1111l1l_opy_
            threading.current_thread().current_hook_uuid = bstack11l1111l1l_opy_
            bstack111ll1ll1_opy_.bstack11l111l11l_opy_(bstack1l11lll_opy_ (u"ࠨࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠢ༉"), hook_data)
        except Exception as e:
            logger.debug(bstack1l11lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡ࡫ࡱࠤࡸࡺࡡࡳࡶࠣ࡬ࡴࡵ࡫ࠡࡧࡹࡩࡳࡺࡳ࠭ࠢ࡫ࡳࡴࡱࠠ࡯ࡣࡰࡩ࠿ࠦࠥࡴ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠩࡸࠨ༊"), name, e)
    def bstack1llll1lll_opy_(self, attrs):
        bstack11l11111l1_opy_ = bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ་"), None)
        hook_data = self.tests[bstack11l11111l1_opy_][bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༌")]
        status = bstack1l11lll_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ།")
        exception = None
        bstack11l111lll1_opy_ = None
        if hook_data.name == bstack1l11lll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠢ༎"):
            self.bstack11l11111ll_opy_.reset()
            bstack11l111l111_opy_ = self.tests[bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ༏"), None)][bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ༐")].result.result
            if bstack11l111l111_opy_ == bstack1l11lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ༑"):
                if attrs.hook_failures == 1:
                    status = bstack1l11lll_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ༒")
                elif attrs.hook_failures == 2:
                    status = bstack1l11lll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ༓")
            elif attrs.bstack111llll1l1_opy_:
                status = bstack1l11lll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ༔")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1l11lll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠨ༕") and attrs.hook_failures == 1:
                status = bstack1l11lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ༖")
            elif hasattr(attrs, bstack1l11lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࡤࡳࡥࡴࡵࡤ࡫ࡪ࠭༗")) and attrs.error_message:
                status = bstack1l11lll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ༘ࠢ")
            bstack11l111lll1_opy_, exception = self._11l111llll_opy_(attrs)
        bstack111lllllll_opy_ = Result(result=status, exception=exception, bstack11l1111ll1_opy_=[bstack11l111lll1_opy_])
        hook_data.stop(time=bstack11lll111l1_opy_(), duration=0, result=bstack111lllllll_opy_)
        bstack111ll1ll1_opy_.bstack11l111l11l_opy_(bstack1l11lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦ༙ࠪ"), self.tests[bstack11l11111l1_opy_][bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༚")])
        threading.current_thread().current_hook_uuid = None
    def _11l111llll_opy_(self, attrs):
        try:
            import traceback
            bstack11lllllll1_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11l111lll1_opy_ = bstack11lllllll1_opy_[-1] if bstack11lllllll1_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1l11lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡨࡻࡳࡵࡱࡰࠤࡹࡸࡡࡤࡧࡥࡥࡨࡱࠢ༛"))
            bstack11l111lll1_opy_ = None
            exception = None
        return bstack11l111lll1_opy_, exception