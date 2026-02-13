# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11111lll1l_opy_ import bstack1111l1lll1_opy_, bstack1111ll1111_opy_
from bstack_utils.bstack1111l1ll11_opy_ import bstack11l1ll111l_opy_
from bstack_utils.helper import bstack11ll11l11_opy_, bstack11l1lll11_opy_, Result
from bstack_utils.bstack1111l11lll_opy_ import bstack1ll111l1_opy_
from bstack_utils.capture import bstack11111llll1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11llll11_opy_:
    def __init__(self):
        self.bstack1111l1l1l1_opy_ = bstack11111llll1_opy_(self.bstack1111ll111l_opy_)
        self.tests = {}
    @staticmethod
    def bstack1111ll111l_opy_(log):
        if not (log[bstack11l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྮ")] and log[bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྯ")].strip()):
            return
        active = bstack11l1ll111l_opy_.bstack11111ll1ll_opy_()
        log = {
            bstack11l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫྰ"): log[bstack11l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬྱ")],
            bstack11l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪྲ"): bstack11l1lll11_opy_(),
            bstack11l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩླ"): log[bstack11l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྴ")],
        }
        if active:
            if active[bstack11l11_opy_ (u"ࠪࡸࡾࡶࡥࠨྵ")] == bstack11l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩྶ"):
                log[bstack11l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬྷ")] = active[bstack11l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ྸ")]
            elif active[bstack11l11_opy_ (u"ࠧࡵࡻࡳࡩࠬྐྵ")] == bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭ྺ"):
                log[bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩྻ")] = active[bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪྼ")]
        bstack1ll111l1_opy_.bstack1l1l1l11l_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1111l1l1l1_opy_.start()
        driver = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ྽"), None)
        bstack11111lll1l_opy_ = bstack1111ll1111_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack11l1lll11_opy_(),
            file_path=attrs.feature.filename,
            result=bstack11l11_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨ྾"),
            framework=bstack11l11_opy_ (u"࠭ࡂࡦࡪࡤࡺࡪ࠭྿"),
            scope=[attrs.feature.name],
            bstack1111l111l1_opy_=bstack1ll111l1_opy_.bstack1111l11l1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ࿀")] = bstack11111lll1l_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack1ll111l1_opy_.bstack1111l11111_opy_(bstack11l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ࿁"), bstack11111lll1l_opy_)
    def end_test(self, attrs):
        bstack1111l1l111_opy_ = {
            bstack11l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ࿂"): attrs.feature.name,
            bstack11l11_opy_ (u"ࠥࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣ࿃"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11111lll1l_opy_ = self.tests[current_test_uuid][bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࿄")]
        meta = {
            bstack11l11_opy_ (u"ࠧ࡬ࡥࡢࡶࡸࡶࡪࠨ࿅"): bstack1111l1l111_opy_,
            bstack11l11_opy_ (u"ࠨࡳࡵࡧࡳࡷ࿆ࠧ"): bstack11111lll1l_opy_.meta.get(bstack11l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭࿇"), []),
            bstack11l11_opy_ (u"ࠣࡵࡦࡩࡳࡧࡲࡪࡱࠥ࿈"): {
                bstack11l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ࿉"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11111lll1l_opy_.bstack1111l11ll1_opy_(meta)
        bstack11111lll1l_opy_.bstack1111l1l11l_opy_(bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ࿊"), []))
        bstack1111l11l11_opy_, exception = self._1111l1ll1l_opy_(attrs)
        status = bstack11l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ࿋") if attrs.status.name.lower() == bstack11l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ࿌") else attrs.status.name.lower()
        bstack11111lll11_opy_ = Result(result=status, exception=exception, bstack1111ll11l1_opy_=[bstack1111l11l11_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿍")].stop(time=bstack11l1lll11_opy_(), duration=int(attrs.duration)*1000, result=bstack11111lll11_opy_)
        bstack1ll111l1_opy_.bstack1111l11111_opy_(bstack11l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ࿎"), self.tests[threading.current_thread().current_test_uuid][bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿏")])
    def bstack11lll11lll_opy_(self, attrs):
        bstack1111l1llll_opy_ = {
            bstack11l11_opy_ (u"ࠩ࡬ࡨࠬ࿐"): uuid4().__str__(),
            bstack11l11_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ࿑"): attrs.keyword,
            bstack11l11_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫ࿒"): [],
            bstack11l11_opy_ (u"ࠬࡺࡥࡹࡶࠪ࿓"): attrs.name,
            bstack11l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ࿔"): bstack11l1lll11_opy_(),
            bstack11l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ࿕"): bstack11l11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ࿖"),
            bstack11l11_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ࿗"): bstack11l11_opy_ (u"ࠪࠫ࿘")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࿙")].add_step(bstack1111l1llll_opy_)
        threading.current_thread().current_step_uuid = bstack1111l1llll_opy_[bstack11l11_opy_ (u"ࠬ࡯ࡤࠨ࿚")]
    def bstack1l1l11l1l1_opy_(self, attrs):
        current_test_id = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ࿛"), None)
        current_step_uuid = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫ࿜"), None)
        bstack1111l11l11_opy_, exception = self._1111l1ll1l_opy_(attrs)
        status = bstack11l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ࿝") if attrs.status.name.lower() == bstack11l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ࿞") else attrs.status.name.lower()
        bstack11111lll11_opy_ = Result(result=status, exception=exception, bstack1111ll11l1_opy_=[bstack1111l11l11_opy_])
        self.tests[current_test_id][bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿟")].bstack11111ll11l_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11111lll11_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack111l1l11l1_opy_(self, name, attrs):
        try:
            bstack1111l111ll_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡘࡊࡋࡠࡆࡈࡊࡆ࡛ࡌࡕࡡࡋࡓࡔࡑࡓࠨ࿠"), bstack11l11_opy_ (u"ࠬ࠭࿡")).split(bstack11l11_opy_ (u"࠭ࠬࠨ࿢"))
            if name in bstack1111l111ll_opy_ and bstack1111l111ll_opy_ != [bstack11l11_opy_ (u"ࠧࠨ࿣")]:
                return
            bstack1111l1111l_opy_ = uuid4().__str__()
            self.tests[bstack1111l1111l_opy_] = {}
            self.bstack1111l1l1l1_opy_.start()
            scopes = []
            driver = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ࿤"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack11l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ࿥")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1111l1111l_opy_)
            if name in [bstack11l11_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ࿦"), bstack11l11_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠢ࿧")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ࿨"), bstack11l11_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ࿩")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack11l11_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ࿪")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1111l1lll1_opy_(
                name=name,
                uuid=bstack1111l1111l_opy_,
                started_at=bstack11l1lll11_opy_(),
                file_path=file_path,
                framework=bstack11l11_opy_ (u"ࠣࡄࡨ࡬ࡦࡼࡥࠣ࿫"),
                bstack1111l111l1_opy_=bstack1ll111l1_opy_.bstack1111l11l1l_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack11l11_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥ࿬"),
                hook_type=name
            )
            self.tests[bstack1111l1111l_opy_][bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡤࡸࡦࠨ࿭")] = hook_data
            current_test_id = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠦࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠣ࿮"), None)
            if current_test_id:
                hook_data.bstack11111ll1l1_opy_(current_test_id)
            if name == bstack11l11_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ࿯"):
                threading.current_thread().before_all_hook_uuid = bstack1111l1111l_opy_
            threading.current_thread().current_hook_uuid = bstack1111l1111l_opy_
            bstack1ll111l1_opy_.bstack1111l11111_opy_(bstack11l11_opy_ (u"ࠨࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠢ࿰"), hook_data)
        except Exception as e:
            logger.debug(bstack11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡ࡫ࡱࠤࡸࡺࡡࡳࡶࠣ࡬ࡴࡵ࡫ࠡࡧࡹࡩࡳࡺࡳ࠭ࠢ࡫ࡳࡴࡱࠠ࡯ࡣࡰࡩ࠿ࠦࠥࡴ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠩࡸࠨ࿱"), name, e)
    def bstack11lll1l111_opy_(self, attrs):
        hook_name = getattr(attrs, bstack11l11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ࿲"), None) or (hasattr(self, bstack11l11_opy_ (u"ࠩࡢࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ࿳")) and self._1111l1l1ll_opy_)
        bstack1111l111ll_opy_ = os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡗࡉࡑ࡟ࡅࡇࡉࡅ࡚ࡒࡔࡠࡊࡒࡓࡐ࡙ࠧ࿴"), bstack11l11_opy_ (u"ࠫࠬ࿵")).split(bstack11l11_opy_ (u"ࠬ࠲ࠧ࿶"))
        if hook_name in bstack1111l111ll_opy_ and bstack1111l111ll_opy_ != [bstack11l11_opy_ (u"࠭ࠧ࿷")]:
            return
        bstack1111ll11ll_opy_ = bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ࿸"), None)
        hook_data = self.tests[bstack1111ll11ll_opy_][bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿹")]
        status = bstack11l11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ࿺")
        exception = None
        bstack1111l11l11_opy_ = None
        if hook_data.name == bstack11l11_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨ࿻"):
            self.bstack1111l1l1l1_opy_.reset()
            bstack11111lllll_opy_ = self.tests[bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ࿼"), None)][bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿽")].result.result
            if bstack11111lllll_opy_ == bstack11l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ࿾"):
                if attrs.hook_failures == 1:
                    status = bstack11l11_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ࿿")
                elif attrs.hook_failures == 2:
                    status = bstack11l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣက")
            elif attrs.aborted:
                status = bstack11l11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤခ")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧဂ") and attrs.hook_failures == 1:
                status = bstack11l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦဃ")
            elif hasattr(attrs, bstack11l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬင")) and attrs.error_message:
                status = bstack11l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨစ")
            bstack1111l11l11_opy_, exception = self._1111l1ll1l_opy_(attrs)
        bstack11111lll11_opy_ = Result(result=status, exception=exception, bstack1111ll11l1_opy_=[bstack1111l11l11_opy_])
        hook_data.stop(time=bstack11l1lll11_opy_(), duration=0, result=bstack11111lll11_opy_)
        bstack1ll111l1_opy_.bstack1111l11111_opy_(bstack11l11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩဆ"), self.tests[bstack1111ll11ll_opy_][bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫဇ")])
        threading.current_thread().current_hook_uuid = None
    def _1111l1ll1l_opy_(self, attrs):
        try:
            import traceback
            bstack1lllll11l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1111l11l11_opy_ = bstack1lllll11l_opy_[-1] if bstack1lllll11l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡷࡧࡣࡦࡤࡤࡧࡰࠨဈ"))
            bstack1111l11l11_opy_ = None
            exception = None
        return bstack1111l11l11_opy_, exception