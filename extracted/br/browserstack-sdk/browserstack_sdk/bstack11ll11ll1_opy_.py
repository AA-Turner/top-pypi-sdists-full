# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack1111ll1lll_opy_ import bstack1111ll1l11_opy_, bstack1111llll1l_opy_
from bstack_utils.bstack1111l1ll11_opy_ import bstack1lll11ll11_opy_
from bstack_utils.helper import bstack111111lll_opy_, bstack1111l11l1_opy_, Result
from bstack_utils.bstack1111ll11l1_opy_ import bstack11l11111l_opy_
from bstack_utils.capture import bstack111l1111ll_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack11ll11ll1_opy_:
    def __init__(self):
        self.bstack1111l1lll1_opy_ = bstack111l1111ll_opy_(self.bstack111l11111l_opy_)
        self.tests = {}
    @staticmethod
    def bstack111l11111l_opy_(log):
        if not (log[bstack1l1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྋ")] and log[bstack1l1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྌ")].strip()):
            return
        active = bstack1lll11ll11_opy_.bstack1111lll1l1_opy_()
        log = {
            bstack1l1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫྍ"): log[bstack1l1111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬྎ")],
            bstack1l1111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪྏ"): bstack1111l11l1_opy_(),
            bstack1l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྐ"): log[bstack1l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྑ")],
        }
        if active:
            if active[bstack1l1111_opy_ (u"ࠪࡸࡾࡶࡥࠨྒ")] == bstack1l1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩྒྷ"):
                log[bstack1l1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬྔ")] = active[bstack1l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ྕ")]
            elif active[bstack1l1111_opy_ (u"ࠧࡵࡻࡳࡩࠬྖ")] == bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹ࠭ྗ"):
                log[bstack1l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ྘")] = active[bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪྙ")]
        bstack11l11111l_opy_.bstack1l1111ll_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack1111l1lll1_opy_.start()
        driver = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪྚ"), None)
        bstack1111ll1lll_opy_ = bstack1111llll1l_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack1111l11l1_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1l1111_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨྛ"),
            framework=bstack1l1111_opy_ (u"࠭ࡂࡦࡪࡤࡺࡪ࠭ྜ"),
            scope=[attrs.feature.name],
            bstack1111ll11ll_opy_=bstack11l11111l_opy_.bstack1111ll111l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪྜྷ")] = bstack1111ll1lll_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack11l11111l_opy_.bstack1111ll1111_opy_(bstack1l1111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩྞ"), bstack1111ll1lll_opy_)
    def end_test(self, attrs):
        bstack1111lll1ll_opy_ = {
            bstack1l1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢྟ"): attrs.feature.name,
            bstack1l1111_opy_ (u"ࠥࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣྠ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack1111ll1lll_opy_ = self.tests[current_test_uuid][bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧྡ")]
        meta = {
            bstack1l1111_opy_ (u"ࠧ࡬ࡥࡢࡶࡸࡶࡪࠨྡྷ"): bstack1111lll1ll_opy_,
            bstack1l1111_opy_ (u"ࠨࡳࡵࡧࡳࡷࠧྣ"): bstack1111ll1lll_opy_.meta.get(bstack1l1111_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ྤ"), []),
            bstack1l1111_opy_ (u"ࠣࡵࡦࡩࡳࡧࡲࡪࡱࠥྥ"): {
                bstack1l1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢྦ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack1111ll1lll_opy_.bstack1111l1ll1l_opy_(meta)
        bstack1111ll1lll_opy_.bstack1111ll1l1l_opy_(bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨྦྷ"), []))
        bstack111l1111l1_opy_, exception = self._1111llll11_opy_(attrs)
        status = bstack1l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫྨ") if attrs.status.name.lower() == bstack1l1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫྩ") else attrs.status.name.lower()
        bstack1111lllll1_opy_ = Result(result=status, exception=exception, bstack1111lll11l_opy_=[bstack111l1111l1_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩྪ")].stop(time=bstack1111l11l1_opy_(), duration=int(attrs.duration)*1000, result=bstack1111lllll1_opy_)
        bstack11l11111l_opy_.bstack1111ll1111_opy_(bstack1l1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩྫ"), self.tests[threading.current_thread().current_test_uuid][bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྫྷ")])
    def bstack1ll1ll11ll_opy_(self, attrs):
        bstack1111lll111_opy_ = {
            bstack1l1111_opy_ (u"ࠩ࡬ࡨࠬྭ"): uuid4().__str__(),
            bstack1l1111_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫྮ"): attrs.keyword,
            bstack1l1111_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫྯ"): [],
            bstack1l1111_opy_ (u"ࠬࡺࡥࡹࡶࠪྰ"): attrs.name,
            bstack1l1111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪྱ"): bstack1111l11l1_opy_(),
            bstack1l1111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧྲ"): bstack1l1111_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩླ"),
            bstack1l1111_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧྴ"): bstack1l1111_opy_ (u"ࠪࠫྵ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧྶ")].add_step(bstack1111lll111_opy_)
        threading.current_thread().current_step_uuid = bstack1111lll111_opy_[bstack1l1111_opy_ (u"ࠬ࡯ࡤࠨྷ")]
    def bstack1l11l1l11_opy_(self, attrs):
        current_test_id = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪྸ"), None)
        current_step_uuid = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫྐྵ"), None)
        bstack111l1111l1_opy_, exception = self._1111llll11_opy_(attrs)
        status = bstack1l1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨྺ") if attrs.status.name.lower() == bstack1l1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨྻ") else attrs.status.name.lower()
        bstack1111lllll1_opy_ = Result(result=status, exception=exception, bstack1111lll11l_opy_=[bstack111l1111l1_opy_])
        self.tests[current_test_id][bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྼ")].bstack1111llllll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1111lllll1_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11ll111111_opy_(self, name, attrs):
        try:
            bstack111l111l11_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡘࡊࡋࡠࡆࡈࡊࡆ࡛ࡌࡕࡡࡋࡓࡔࡑࡓࠨ྽"), bstack1l1111_opy_ (u"ࠬ࠭྾")).split(bstack1l1111_opy_ (u"࠭ࠬࠨ྿"))
            if name in bstack111l111l11_opy_ and bstack111l111l11_opy_ != [bstack1l1111_opy_ (u"ࠧࠨ࿀")]:
                return
            bstack1111l1l1l1_opy_ = uuid4().__str__()
            self.tests[bstack1111l1l1l1_opy_] = {}
            self.bstack1111l1lll1_opy_.start()
            scopes = []
            driver = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ࿁"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1l1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ࿂")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack1111l1l1l1_opy_)
            if name in [bstack1l1111_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢ࿃"), bstack1l1111_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠢ࿄")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1l1111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ࿅"), bstack1l1111_opy_ (u"ࠨࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ࿆")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1l1111_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨ࿇")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1111ll1l11_opy_(
                name=name,
                uuid=bstack1111l1l1l1_opy_,
                started_at=bstack1111l11l1_opy_(),
                file_path=file_path,
                framework=bstack1l1111_opy_ (u"ࠣࡄࡨ࡬ࡦࡼࡥࠣ࿈"),
                bstack1111ll11ll_opy_=bstack11l11111l_opy_.bstack1111ll111l_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1l1111_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥ࿉"),
                hook_type=name
            )
            self.tests[bstack1111l1l1l1_opy_][bstack1l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡤࡸࡦࠨ࿊")] = hook_data
            current_test_id = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠦࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠣ࿋"), None)
            if current_test_id:
                hook_data.bstack111l111111_opy_(current_test_id)
            if name == bstack1l1111_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ࿌"):
                threading.current_thread().before_all_hook_uuid = bstack1111l1l1l1_opy_
            threading.current_thread().current_hook_uuid = bstack1111l1l1l1_opy_
            bstack11l11111l_opy_.bstack1111ll1111_opy_(bstack1l1111_opy_ (u"ࠨࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠢ࿍"), hook_data)
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡ࡫ࡱࠤࡸࡺࡡࡳࡶࠣ࡬ࡴࡵ࡫ࠡࡧࡹࡩࡳࡺࡳ࠭ࠢ࡫ࡳࡴࡱࠠ࡯ࡣࡰࡩ࠿ࠦࠥࡴ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠩࡸࠨ࿎"), name, e)
    def bstack1l1l1lll_opy_(self, attrs):
        hook_name = getattr(attrs, bstack1l1111_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ࿏"), None) or (hasattr(self, bstack1l1111_opy_ (u"ࠩࡢࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ࿐")) and self._1111ll1ll1_opy_)
        bstack111l111l11_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡗࡉࡑ࡟ࡅࡇࡉࡅ࡚ࡒࡔࡠࡊࡒࡓࡐ࡙ࠧ࿑"), bstack1l1111_opy_ (u"ࠫࠬ࿒")).split(bstack1l1111_opy_ (u"ࠬ࠲ࠧ࿓"))
        if hook_name in bstack111l111l11_opy_ and bstack111l111l11_opy_ != [bstack1l1111_opy_ (u"࠭ࠧ࿔")]:
            return
        bstack1111l1l1ll_opy_ = bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ࿕"), None)
        hook_data = self.tests[bstack1111l1l1ll_opy_][bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿖")]
        status = bstack1l1111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ࿗")
        exception = None
        bstack111l1111l1_opy_ = None
        if hook_data.name == bstack1l1111_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨ࿘"):
            self.bstack1111l1lll1_opy_.reset()
            bstack1111l1llll_opy_ = self.tests[bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ࿙"), None)][bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿚")].result.result
            if bstack1111l1llll_opy_ == bstack1l1111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ࿛"):
                if attrs.hook_failures == 1:
                    status = bstack1l1111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ࿜")
                elif attrs.hook_failures == 2:
                    status = bstack1l1111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ࿝")
            elif attrs.aborted:
                status = bstack1l1111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ࿞")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1l1111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧ࿟") and attrs.hook_failures == 1:
                status = bstack1l1111_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࿠")
            elif hasattr(attrs, bstack1l1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬ࿡")) and attrs.error_message:
                status = bstack1l1111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ࿢")
            bstack111l1111l1_opy_, exception = self._1111llll11_opy_(attrs)
        bstack1111lllll1_opy_ = Result(result=status, exception=exception, bstack1111lll11l_opy_=[bstack111l1111l1_opy_])
        hook_data.stop(time=bstack1111l11l1_opy_(), duration=0, result=bstack1111lllll1_opy_)
        bstack11l11111l_opy_.bstack1111ll1111_opy_(bstack1l1111_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ࿣"), self.tests[bstack1111l1l1ll_opy_][bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿤")])
        threading.current_thread().current_hook_uuid = None
    def _1111llll11_opy_(self, attrs):
        try:
            import traceback
            bstack111llll11_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack111l1111l1_opy_ = bstack111llll11_opy_[-1] if bstack111llll11_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡷࡧࡣࡦࡤࡤࡧࡰࠨ࿥"))
            bstack111l1111l1_opy_ = None
            exception = None
        return bstack111l1111l1_opy_, exception