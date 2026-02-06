# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack1111llllll_opy_ import bstack1111ll1lll_opy_, bstack1111ll11ll_opy_
from bstack_utils.bstack1111l1lll1_opy_ import bstack1l1l11llll_opy_
from bstack_utils.helper import bstack1l1ll1ll1_opy_, bstack1lll11lll1_opy_, Result
from bstack_utils.bstack1111lll1l1_opy_ import bstack11lll1111l_opy_
from bstack_utils.capture import bstack1111ll1l1l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1ll1111l1_opy_:
    def __init__(self):
        self.bstack1111llll1l_opy_ = bstack1111ll1l1l_opy_(self.bstack1111ll1l11_opy_)
        self.tests = {}
    @staticmethod
    def bstack1111ll1l11_opy_(log):
        if not (log[bstack11lllll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྐ")] and log[bstack11lllll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྑ")].strip()):
            return
        active = bstack1l1l11llll_opy_.bstack1111ll1ll1_opy_()
        log = {
            bstack11lllll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩྒ"): log[bstack11lllll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪྒྷ")],
            bstack11lllll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨྔ"): bstack1lll11lll1_opy_(),
            bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྕ"): log[bstack11lllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྖ")],
        }
        if active:
            if active[bstack11lllll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ྗ")] == bstack11lllll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ྘"):
                log[bstack11lllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪྙ")] = active[bstack11lllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫྚ")]
            elif active[bstack11lllll_opy_ (u"ࠬࡺࡹࡱࡧࠪྛ")] == bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࠫྜ"):
                log[bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧྜྷ")] = active[bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨྞ")]
        bstack11lll1111l_opy_.bstack1ll111l1ll_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1111llll1l_opy_.start()
        driver = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨྟ"), None)
        bstack1111llllll_opy_ = bstack1111ll11ll_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1lll11lll1_opy_(),
            file_path=attrs.feature.filename,
            result=bstack11lllll_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦྠ"),
            framework=bstack11lllll_opy_ (u"ࠫࡇ࡫ࡨࡢࡸࡨࠫྡ"),
            scope=[attrs.feature.name],
            bstack1111lllll1_opy_=bstack11lll1111l_opy_.bstack1111lll1ll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨྡྷ")] = bstack1111llllll_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack11lll1111l_opy_.bstack111l111111_opy_(bstack11lllll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧྣ"), bstack1111llllll_opy_)
    def end_test(self, attrs):
        bstack1111lll111_opy_ = {
            bstack11lllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧྤ"): attrs.feature.name,
            bstack11lllll_opy_ (u"ࠣࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨྥ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack1111llllll_opy_ = self.tests[current_test_uuid][bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྦ")]
        meta = {
            bstack11lllll_opy_ (u"ࠥࡪࡪࡧࡴࡶࡴࡨࠦྦྷ"): bstack1111lll111_opy_,
            bstack11lllll_opy_ (u"ࠦࡸࡺࡥࡱࡵࠥྨ"): bstack1111llllll_opy_.meta.get(bstack11lllll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫྩ"), []),
            bstack11lllll_opy_ (u"ࠨࡳࡤࡧࡱࡥࡷ࡯࡯ࠣྪ"): {
                bstack11lllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧྫ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack1111llllll_opy_.bstack1111ll111l_opy_(meta)
        bstack1111llllll_opy_.bstack111l1111l1_opy_(bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ྫྷ"), []))
        bstack1111l1l1l1_opy_, exception = self._111l1111ll_opy_(attrs)
        status = bstack11lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩྭ") if attrs.status.name.lower() == bstack11lllll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩྮ") else attrs.status.name.lower()
        bstack1111l1ll11_opy_ = Result(result=status, exception=exception, bstack1111ll11l1_opy_=[bstack1111l1l1l1_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧྯ")].stop(time=bstack1lll11lll1_opy_(), duration=int(attrs.duration)*1000, result=bstack1111l1ll11_opy_)
        bstack11lll1111l_opy_.bstack111l111111_opy_(bstack11lllll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧྰ"), self.tests[threading.current_thread().current_test_uuid][bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩྱ")])
    def bstack111ll1llll_opy_(self, attrs):
        bstack111l111l11_opy_ = {
            bstack11lllll_opy_ (u"ࠧࡪࡦࠪྲ"): uuid4().__str__(),
            bstack11lllll_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩླ"): attrs.keyword,
            bstack11lllll_opy_ (u"ࠩࡶࡸࡪࡶ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠩྴ"): [],
            bstack11lllll_opy_ (u"ࠪࡸࡪࡾࡴࠨྵ"): attrs.name,
            bstack11lllll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨྶ"): bstack1lll11lll1_opy_(),
            bstack11lllll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬྷ"): bstack11lllll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧྸ"),
            bstack11lllll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬྐྵ"): bstack11lllll_opy_ (u"ࠨࠩྺ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྻ")].add_step(bstack111l111l11_opy_)
        threading.current_thread().current_step_uuid = bstack111l111l11_opy_[bstack11lllll_opy_ (u"ࠪ࡭ࡩ࠭ྼ")]
    def bstack1111111l1_opy_(self, attrs):
        current_test_id = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ྽"), None)
        current_step_uuid = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩ྾"), None)
        bstack1111l1l1l1_opy_, exception = self._111l1111ll_opy_(attrs)
        status = bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭྿") if attrs.status.name.lower() == bstack11lllll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭࿀") else attrs.status.name.lower()
        bstack1111l1ll11_opy_ = Result(result=status, exception=exception, bstack1111ll11l1_opy_=[bstack1111l1l1l1_opy_])
        self.tests[current_test_id][bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿁")].bstack1111l1llll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1111l1ll11_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack1l11ll111_opy_(self, name, attrs):
        try:
            bstack1111l1ll1l_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡄࡆࡈࡄ࡙ࡑ࡚࡟ࡉࡑࡒࡏࡘ࠭࿂"), bstack11lllll_opy_ (u"ࠪࠫ࿃")).split(bstack11lllll_opy_ (u"ࠫ࠱࠭࿄"))
            if name in bstack1111l1ll1l_opy_ and bstack1111l1ll1l_opy_ != [bstack11lllll_opy_ (u"ࠬ࠭࿅")]:
                return
            bstack1111l1l1ll_opy_ = uuid4().__str__()
            self.tests[bstack1111l1l1ll_opy_] = {}
            self.bstack1111llll1l_opy_.start()
            scopes = []
            driver = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶ࿆ࠬ"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack11lllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ࿇")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1111l1l1ll_opy_)
            if name in [bstack11lllll_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ࿈"), bstack11lllll_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠧ࿉")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack11lllll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ࿊"), bstack11lllll_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠦ࿋")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack11lllll_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭࿌")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1111ll1lll_opy_(
                name=name,
                uuid=bstack1111l1l1ll_opy_,
                started_at=bstack1lll11lll1_opy_(),
                file_path=file_path,
                framework=bstack11lllll_opy_ (u"ࠨࡂࡦࡪࡤࡺࡪࠨ࿍"),
                bstack1111lllll1_opy_=bstack11lll1111l_opy_.bstack1111lll1ll_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack11lllll_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣ࿎"),
                hook_type=name
            )
            self.tests[bstack1111l1l1ll_opy_][bstack11lllll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡢࡶࡤࠦ࿏")] = hook_data
            current_test_id = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠤࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨ࿐"), None)
            if current_test_id:
                hook_data.bstack1111ll1111_opy_(current_test_id)
            if name == bstack11lllll_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ࿑"):
                threading.current_thread().before_all_hook_uuid = bstack1111l1l1ll_opy_
            threading.current_thread().current_hook_uuid = bstack1111l1l1ll_opy_
            bstack11lll1111l_opy_.bstack111l111111_opy_(bstack11lllll_opy_ (u"ࠦࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠧ࿒"), hook_data)
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࠡࡪࡲࡳࡰࠦࡥࡷࡧࡱࡸࡸ࠲ࠠࡩࡱࡲ࡯ࠥࡴࡡ࡮ࡧ࠽ࠤࠪࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠧࡶࠦ࿓"), name, e)
    def bstack111l11l11l_opy_(self, attrs):
        hook_name = getattr(attrs, bstack11lllll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ࿔"), None) or (hasattr(self, bstack11lllll_opy_ (u"ࠧࡠࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ࿕")) and self._1111llll11_opy_)
        bstack1111l1ll1l_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡊࡅࡇࡃࡘࡐ࡙ࡥࡈࡐࡑࡎࡗࠬ࿖"), bstack11lllll_opy_ (u"ࠩࠪ࿗")).split(bstack11lllll_opy_ (u"ࠪ࠰ࠬ࿘"))
        if hook_name in bstack1111l1ll1l_opy_ and bstack1111l1ll1l_opy_ != [bstack11lllll_opy_ (u"ࠫࠬ࿙")]:
            return
        bstack1111lll11l_opy_ = bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ࿚"), None)
        hook_data = self.tests[bstack1111lll11l_opy_][bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿛")]
        status = bstack11lllll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ࿜")
        exception = None
        bstack1111l1l1l1_opy_ = None
        if hook_data.name == bstack11lllll_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦ࿝"):
            self.bstack1111llll1l_opy_.reset()
            bstack111l11111l_opy_ = self.tests[bstack1l1ll1ll1_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ࿞"), None)][bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿟")].result.result
            if bstack111l11111l_opy_ == bstack11lllll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࿠"):
                if attrs.hook_failures == 1:
                    status = bstack11lllll_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ࿡")
                elif attrs.hook_failures == 2:
                    status = bstack11lllll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ࿢")
            elif attrs.aborted:
                status = bstack11lllll_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ࿣")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11lllll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ࿤") and attrs.hook_failures == 1:
                status = bstack11lllll_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ࿥")
            elif hasattr(attrs, bstack11lllll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪ࿦")) and attrs.error_message:
                status = bstack11lllll_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࿧")
            bstack1111l1l1l1_opy_, exception = self._111l1111ll_opy_(attrs)
        bstack1111l1ll11_opy_ = Result(result=status, exception=exception, bstack1111ll11l1_opy_=[bstack1111l1l1l1_opy_])
        hook_data.stop(time=bstack1lll11lll1_opy_(), duration=0, result=bstack1111l1ll11_opy_)
        bstack11lll1111l_opy_.bstack111l111111_opy_(bstack11lllll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ࿨"), self.tests[bstack1111lll11l_opy_][bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿩")])
        threading.current_thread().current_hook_uuid = None
    def _111l1111ll_opy_(self, attrs):
        try:
            import traceback
            bstack111l11ll1l_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack1111l1l1l1_opy_ = bstack111l11ll1l_opy_[-1] if bstack111l11ll1l_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11lllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࠦ࿪"))
            bstack1111l1l1l1_opy_ = None
            exception = None
        return bstack1111l1l1l1_opy_, exception