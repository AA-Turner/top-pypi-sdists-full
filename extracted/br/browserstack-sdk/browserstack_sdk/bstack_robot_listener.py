# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1111lll11l_opy_ import RobotHandler
from bstack_utils.capture import bstack111ll11l1l_opy_
from bstack_utils.bstack111ll1ll1l_opy_ import bstack111l11lll1_opy_, bstack111ll1l1l1_opy_, bstack111ll1ll11_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l1ll111ll_opy_
from bstack_utils.bstack111lll11l1_opy_ import bstack111lll111_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11ll1lll_opy_, bstack1lllllllll_opy_, Result, \
    bstack111l11l1l1_opy_, bstack111l111lll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack11l1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨཻࠬ"): [],
        bstack11l1111_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨོ"): [],
        bstack11l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹཽࠧ"): []
    }
    bstack111l1lll1l_opy_ = []
    bstack111l11111l_opy_ = []
    @staticmethod
    def bstack111ll11lll_opy_(log):
        if not ((isinstance(log[bstack11l1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཾ")], list) or (isinstance(log[bstack11l1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཿ")], dict)) and len(log[bstack11l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ྀࠧ")])>0) or (isinstance(log[bstack11l1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཱྀ")], str) and log[bstack11l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྂ")].strip())):
            return
        active = bstack1l1ll111ll_opy_.bstack111ll1l111_opy_()
        log = {
            bstack11l1111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨྃ"): log[bstack11l1111_opy_ (u"ࠪࡰࡪࡼࡥ࡭྄ࠩ")],
            bstack11l1111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ྅"): bstack111l111lll_opy_().isoformat() + bstack11l1111_opy_ (u"ࠬࡠࠧ྆"),
            bstack11l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ྇"): log[bstack11l1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྈ")],
        }
        if active:
            if active[bstack11l1111_opy_ (u"ࠨࡶࡼࡴࡪ࠭ྉ")] == bstack11l1111_opy_ (u"ࠩ࡫ࡳࡴࡱࠧྊ"):
                log[bstack11l1111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪྋ")] = active[bstack11l1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫྌ")]
            elif active[bstack11l1111_opy_ (u"ࠬࡺࡹࡱࡧࠪྍ")] == bstack11l1111_opy_ (u"࠭ࡴࡦࡵࡷࠫྎ"):
                log[bstack11l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧྏ")] = active[bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨྐ")]
        bstack111lll111_opy_.bstack11lll11l_opy_([log])
    def __init__(self):
        self.messages = bstack111l1l1111_opy_()
        self._111l1l111l_opy_ = None
        self._1111ll1l11_opy_ = None
        self._111l1ll11l_opy_ = OrderedDict()
        self.bstack111llll11l_opy_ = bstack111ll11l1l_opy_(self.bstack111ll11lll_opy_)
    @bstack111l11l1l1_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1l1lll_opy_()
        if not self._111l1ll11l_opy_.get(attrs.get(bstack11l1111_opy_ (u"ࠩ࡬ࡨࠬྑ")), None):
            self._111l1ll11l_opy_[attrs.get(bstack11l1111_opy_ (u"ࠪ࡭ࡩ࠭ྒ"))] = {}
        bstack111l111ll1_opy_ = bstack111ll1ll11_opy_(
                bstack111l1l11ll_opy_=attrs.get(bstack11l1111_opy_ (u"ࠫ࡮ࡪࠧྒྷ")),
                name=name,
                started_at=bstack1lllllllll_opy_(),
                file_path=os.path.relpath(attrs[bstack11l1111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬྔ")], start=os.getcwd()) if attrs.get(bstack11l1111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ྕ")) != bstack11l1111_opy_ (u"ࠧࠨྖ") else bstack11l1111_opy_ (u"ࠨࠩྗ"),
                framework=bstack11l1111_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ྘")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11l1111_opy_ (u"ࠪ࡭ࡩ࠭ྙ"), None)
        self._111l1ll11l_opy_[attrs.get(bstack11l1111_opy_ (u"ࠫ࡮ࡪࠧྚ"))][bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨྛ")] = bstack111l111ll1_opy_
    @bstack111l11l1l1_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111l11llll_opy_()
        self._111l1l11l1_opy_(messages)
        with self._lock:
            for bstack111l1l1l11_opy_ in self.bstack111l1lll1l_opy_:
                bstack111l1l1l11_opy_[bstack11l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨྜ")][bstack11l1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ྜྷ")].extend(self.store[bstack11l1111_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧྞ")])
                bstack111lll111_opy_.bstack1l1l11lll1_opy_(bstack111l1l1l11_opy_)
            self.bstack111l1lll1l_opy_ = []
            self.store[bstack11l1111_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨྟ")] = []
    @bstack111l11l1l1_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111llll11l_opy_.start()
        if not self._111l1ll11l_opy_.get(attrs.get(bstack11l1111_opy_ (u"ࠪ࡭ࡩ࠭ྠ")), None):
            self._111l1ll11l_opy_[attrs.get(bstack11l1111_opy_ (u"ࠫ࡮ࡪࠧྡ"))] = {}
        driver = bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫྡྷ"), None)
        bstack111ll1ll1l_opy_ = bstack111ll1ll11_opy_(
            bstack111l1l11ll_opy_=attrs.get(bstack11l1111_opy_ (u"࠭ࡩࡥࠩྣ")),
            name=name,
            started_at=bstack1lllllllll_opy_(),
            file_path=os.path.relpath(attrs[bstack11l1111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧྤ")], start=os.getcwd()),
            scope=RobotHandler.bstack1111lllll1_opy_(attrs.get(bstack11l1111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨྥ"), None)),
            framework=bstack11l1111_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨྦ"),
            tags=attrs[bstack11l1111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨྦྷ")],
            hooks=self.store[bstack11l1111_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪྨ")],
            bstack111lll11ll_opy_=bstack111lll111_opy_.bstack111lll1l11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11l1111_opy_ (u"ࠧࢁࡽࠡ࡞ࡱࠤࢀࢃࠢྩ").format(bstack11l1111_opy_ (u"ࠨࠠࠣྪ").join(attrs[bstack11l1111_opy_ (u"ࠧࡵࡣࡪࡷࠬྫ")]), name) if attrs[bstack11l1111_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ྫྷ")] else name
        )
        self._111l1ll11l_opy_[attrs.get(bstack11l1111_opy_ (u"ࠩ࡬ࡨࠬྭ"))][bstack11l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྮ")] = bstack111ll1ll1l_opy_
        threading.current_thread().current_test_uuid = bstack111ll1ll1l_opy_.bstack1111llll11_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11l1111_opy_ (u"ࠫ࡮ࡪࠧྯ"), None)
        self.bstack111ll111ll_opy_(bstack11l1111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ྰ"), bstack111ll1ll1l_opy_)
    @bstack111l11l1l1_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111llll11l_opy_.reset()
        bstack1111lll1l1_opy_ = bstack111l1ll1ll_opy_.get(attrs.get(bstack11l1111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ྱ")), bstack11l1111_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨྲ"))
        self._111l1ll11l_opy_[attrs.get(bstack11l1111_opy_ (u"ࠨ࡫ࡧࠫླ"))][bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྴ")].stop(time=bstack1lllllllll_opy_(), duration=int(attrs.get(bstack11l1111_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨྵ"), bstack11l1111_opy_ (u"ࠫ࠵࠭ྶ"))), result=Result(result=bstack1111lll1l1_opy_, exception=attrs.get(bstack11l1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ྷ")), bstack111lll1l1l_opy_=[attrs.get(bstack11l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྸ"))]))
        self.bstack111ll111ll_opy_(bstack11l1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩྐྵ"), self._111l1ll11l_opy_[attrs.get(bstack11l1111_opy_ (u"ࠨ࡫ࡧࠫྺ"))][bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྻ")], True)
        with self._lock:
            self.store[bstack11l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧྼ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111l11l1l1_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1l1lll_opy_()
        current_test_id = bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭྽"), None)
        bstack1111ll11l1_opy_ = current_test_id if bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ྾"), None) else bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ྿"), None)
        if attrs.get(bstack11l1111_opy_ (u"ࠧࡵࡻࡳࡩࠬ࿀"), bstack11l1111_opy_ (u"ࠨࠩ࿁")).lower() in [bstack11l1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ࿂"), bstack11l1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ࿃")]:
            hook_type = bstack111l11l1ll_opy_(attrs.get(bstack11l1111_opy_ (u"ࠫࡹࡿࡰࡦࠩ࿄")), bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ࿅"), None))
            hook_name = bstack11l1111_opy_ (u"࠭ࡻࡾ࿆ࠩ").format(attrs.get(bstack11l1111_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ࿇"), bstack11l1111_opy_ (u"ࠨࠩ࿈")))
            if hook_type in [bstack11l1111_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭࿉"), bstack11l1111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭࿊")]:
                hook_name = bstack11l1111_opy_ (u"ࠫࡠࢁࡽ࡞ࠢࡾࢁࠬ࿋").format(bstack1111lll111_opy_.get(hook_type), attrs.get(bstack11l1111_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ࿌"), bstack11l1111_opy_ (u"࠭ࠧ࿍")))
            bstack111l1111ll_opy_ = bstack111ll1l1l1_opy_(
                bstack111l1l11ll_opy_=bstack1111ll11l1_opy_ + bstack11l1111_opy_ (u"ࠧ࠮ࠩ࿎") + attrs.get(bstack11l1111_opy_ (u"ࠨࡶࡼࡴࡪ࠭࿏"), bstack11l1111_opy_ (u"ࠩࠪ࿐")).lower(),
                name=hook_name,
                started_at=bstack1lllllllll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11l1111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ࿑")), start=os.getcwd()),
                framework=bstack11l1111_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪ࿒"),
                tags=attrs[bstack11l1111_opy_ (u"ࠬࡺࡡࡨࡵࠪ࿓")],
                scope=RobotHandler.bstack1111lllll1_opy_(attrs.get(bstack11l1111_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭࿔"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l1111ll_opy_.bstack1111llll11_opy_()
            threading.current_thread().current_hook_id = bstack1111ll11l1_opy_ + bstack11l1111_opy_ (u"ࠧ࠮ࠩ࿕") + attrs.get(bstack11l1111_opy_ (u"ࠨࡶࡼࡴࡪ࠭࿖"), bstack11l1111_opy_ (u"ࠩࠪ࿗")).lower()
            with self._lock:
                self.store[bstack11l1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ࿘")] = [bstack111l1111ll_opy_.bstack1111llll11_opy_()]
                if bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ࿙"), None):
                    self.store[bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ࿚")].append(bstack111l1111ll_opy_.bstack1111llll11_opy_())
                else:
                    self.store[bstack11l1111_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ࿛")].append(bstack111l1111ll_opy_.bstack1111llll11_opy_())
            if bstack1111ll11l1_opy_:
                self._111l1ll11l_opy_[bstack1111ll11l1_opy_ + bstack11l1111_opy_ (u"ࠧ࠮ࠩ࿜") + attrs.get(bstack11l1111_opy_ (u"ࠨࡶࡼࡴࡪ࠭࿝"), bstack11l1111_opy_ (u"ࠩࠪ࿞")).lower()] = { bstack11l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿟"): bstack111l1111ll_opy_ }
            bstack111lll111_opy_.bstack111ll111ll_opy_(bstack11l1111_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ࿠"), bstack111l1111ll_opy_)
        else:
            bstack111llll111_opy_ = {
                bstack11l1111_opy_ (u"ࠬ࡯ࡤࠨ࿡"): uuid4().__str__(),
                bstack11l1111_opy_ (u"࠭ࡴࡦࡺࡷࠫ࿢"): bstack11l1111_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭࿣").format(attrs.get(bstack11l1111_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ࿤")), attrs.get(bstack11l1111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ࿥"), bstack11l1111_opy_ (u"ࠪࠫ࿦"))) if attrs.get(bstack11l1111_opy_ (u"ࠫࡦࡸࡧࡴࠩ࿧"), []) else attrs.get(bstack11l1111_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ࿨")),
                bstack11l1111_opy_ (u"࠭ࡳࡵࡧࡳࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭࿩"): attrs.get(bstack11l1111_opy_ (u"ࠧࡢࡴࡪࡷࠬ࿪"), []),
                bstack11l1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ࿫"): bstack1lllllllll_opy_(),
                bstack11l1111_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ࿬"): bstack11l1111_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ࿭"),
                bstack11l1111_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ࿮"): attrs.get(bstack11l1111_opy_ (u"ࠬࡪ࡯ࡤࠩ࿯"), bstack11l1111_opy_ (u"࠭ࠧ࿰"))
            }
            if attrs.get(bstack11l1111_opy_ (u"ࠧ࡭࡫ࡥࡲࡦࡳࡥࠨ࿱"), bstack11l1111_opy_ (u"ࠨࠩ࿲")) != bstack11l1111_opy_ (u"ࠩࠪ࿳"):
                bstack111llll111_opy_[bstack11l1111_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ࿴")] = attrs.get(bstack11l1111_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬ࿵"))
            if not self.bstack111l11111l_opy_:
                self._111l1ll11l_opy_[self._1111llll1l_opy_()][bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿶")].add_step(bstack111llll111_opy_)
                threading.current_thread().current_step_uuid = bstack111llll111_opy_[bstack11l1111_opy_ (u"࠭ࡩࡥࠩ࿷")]
            self.bstack111l11111l_opy_.append(bstack111llll111_opy_)
    @bstack111l11l1l1_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111l11llll_opy_()
        self._111l1l11l1_opy_(messages)
        current_test_id = bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩ࿸"), None)
        bstack1111ll11l1_opy_ = current_test_id if current_test_id else bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫ࿹"), None)
        bstack111l1111l1_opy_ = bstack111l1ll1ll_opy_.get(attrs.get(bstack11l1111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ࿺")), bstack11l1111_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ࿻"))
        bstack111l1l1ll1_opy_ = attrs.get(bstack11l1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿼"))
        if bstack111l1111l1_opy_ != bstack11l1111_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭࿽") and not attrs.get(bstack11l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿾")) and self._111l1l111l_opy_:
            bstack111l1l1ll1_opy_ = self._111l1l111l_opy_
        bstack111lll1lll_opy_ = Result(result=bstack111l1111l1_opy_, exception=bstack111l1l1ll1_opy_, bstack111lll1l1l_opy_=[bstack111l1l1ll1_opy_])
        if attrs.get(bstack11l1111_opy_ (u"ࠧࡵࡻࡳࡩࠬ࿿"), bstack11l1111_opy_ (u"ࠨࠩက")).lower() in [bstack11l1111_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨခ"), bstack11l1111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬဂ")]:
            bstack1111ll11l1_opy_ = current_test_id if current_test_id else bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧဃ"), None)
            if bstack1111ll11l1_opy_:
                bstack111ll1l11l_opy_ = bstack1111ll11l1_opy_ + bstack11l1111_opy_ (u"ࠧ࠳ࠢင") + attrs.get(bstack11l1111_opy_ (u"࠭ࡴࡺࡲࡨࠫစ"), bstack11l1111_opy_ (u"ࠧࠨဆ")).lower()
                self._111l1ll11l_opy_[bstack111ll1l11l_opy_][bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫဇ")].stop(time=bstack1lllllllll_opy_(), duration=int(attrs.get(bstack11l1111_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧဈ"), bstack11l1111_opy_ (u"ࠪ࠴ࠬဉ"))), result=bstack111lll1lll_opy_)
                bstack111lll111_opy_.bstack111ll111ll_opy_(bstack11l1111_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ည"), self._111l1ll11l_opy_[bstack111ll1l11l_opy_][bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨဋ")])
        else:
            bstack1111ll11l1_opy_ = current_test_id if current_test_id else bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤ࡯ࡤࠨဌ"), None)
            if bstack1111ll11l1_opy_ and len(self.bstack111l11111l_opy_) == 1:
                current_step_uuid = bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫဍ"), None)
                self._111l1ll11l_opy_[bstack1111ll11l1_opy_][bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫဎ")].bstack111ll1lll1_opy_(current_step_uuid, duration=int(attrs.get(bstack11l1111_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧဏ"), bstack11l1111_opy_ (u"ࠪ࠴ࠬတ"))), result=bstack111lll1lll_opy_)
            else:
                self.bstack1111ll1ll1_opy_(attrs)
            self.bstack111l11111l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11l1111_opy_ (u"ࠫ࡭ࡺ࡭࡭ࠩထ"), bstack11l1111_opy_ (u"ࠬࡴ࡯ࠨဒ")) == bstack11l1111_opy_ (u"࠭ࡹࡦࡵࠪဓ"):
                return
            self.messages.push(message)
            logs = []
            if bstack1l1ll111ll_opy_.bstack111ll1l111_opy_():
                logs.append({
                    bstack11l1111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪန"): bstack1lllllllll_opy_(),
                    bstack11l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩပ"): message.get(bstack11l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဖ")),
                    bstack11l1111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩဗ"): message.get(bstack11l1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪဘ")),
                    **bstack1l1ll111ll_opy_.bstack111ll1l111_opy_()
                })
                if len(logs) > 0:
                    bstack111lll111_opy_.bstack11lll11l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack111lll111_opy_.bstack111l1l1l1l_opy_()
    def bstack1111ll1ll1_opy_(self, bstack111l1llll1_opy_):
        if not bstack1l1ll111ll_opy_.bstack111ll1l111_opy_():
            return
        kwname = bstack11l1111_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫမ").format(bstack111l1llll1_opy_.get(bstack11l1111_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ယ")), bstack111l1llll1_opy_.get(bstack11l1111_opy_ (u"ࠧࡢࡴࡪࡷࠬရ"), bstack11l1111_opy_ (u"ࠨࠩလ"))) if bstack111l1llll1_opy_.get(bstack11l1111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧဝ"), []) else bstack111l1llll1_opy_.get(bstack11l1111_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪသ"))
        error_message = bstack11l1111_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠣࢀࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢ࡟ࠦࢀ࠸ࡽ࡝ࠤࠥဟ").format(kwname, bstack111l1llll1_opy_.get(bstack11l1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬဠ")), str(bstack111l1llll1_opy_.get(bstack11l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧအ"))))
        bstack111l1ll111_opy_ = bstack11l1111_opy_ (u"ࠢ࡬ࡹࡱࡥࡲ࡫࠺ࠡ࡞ࠥࡿ࠵ࢃ࡜ࠣࠢࡿࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࡢࠢࡼ࠳ࢀࡠࠧࠨဢ").format(kwname, bstack111l1llll1_opy_.get(bstack11l1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨဣ")))
        bstack111l1lllll_opy_ = error_message if bstack111l1llll1_opy_.get(bstack11l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဤ")) else bstack111l1ll111_opy_
        bstack111l1ll1l1_opy_ = {
            bstack11l1111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ဥ"): self.bstack111l11111l_opy_[-1].get(bstack11l1111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨဦ"), bstack1lllllllll_opy_()),
            bstack11l1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ဧ"): bstack111l1lllll_opy_,
            bstack11l1111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬဨ"): bstack11l1111_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭ဩ") if bstack111l1llll1_opy_.get(bstack11l1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨဪ")) == bstack11l1111_opy_ (u"ࠩࡉࡅࡎࡒࠧါ") else bstack11l1111_opy_ (u"ࠪࡍࡓࡌࡏࠨာ"),
            **bstack1l1ll111ll_opy_.bstack111ll1l111_opy_()
        }
        bstack111lll111_opy_.bstack11lll11l_opy_([bstack111l1ll1l1_opy_])
    def _1111llll1l_opy_(self):
        for bstack111l1l11ll_opy_ in reversed(self._111l1ll11l_opy_):
            bstack1111ll111l_opy_ = bstack111l1l11ll_opy_
            data = self._111l1ll11l_opy_[bstack111l1l11ll_opy_][bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧိ")]
            if isinstance(data, bstack111ll1l1l1_opy_):
                if not bstack11l1111_opy_ (u"ࠬࡋࡁࡄࡊࠪီ") in data.bstack1111lll1ll_opy_():
                    return bstack1111ll111l_opy_
            else:
                return bstack1111ll111l_opy_
    def _111l1l11l1_opy_(self, messages):
        try:
            bstack111l11ll1l_opy_ = BuiltIn().get_variable_value(bstack11l1111_opy_ (u"ࠨࠤࡼࡎࡒࡋࠥࡒࡅࡗࡇࡏࢁࠧု")) in (bstack1111ll1lll_opy_.DEBUG, bstack1111ll1lll_opy_.TRACE)
            for message, bstack111l111l11_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11l1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨူ"))
                level = message.get(bstack11l1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧေ"))
                if level == bstack1111ll1lll_opy_.FAIL:
                    self._111l1l111l_opy_ = name or self._111l1l111l_opy_
                    self._1111ll1l11_opy_ = bstack111l111l11_opy_.get(bstack11l1111_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥဲ")) if bstack111l11ll1l_opy_ and bstack111l111l11_opy_ else self._1111ll1l11_opy_
        except:
            pass
    @classmethod
    def bstack111ll111ll_opy_(self, event: str, bstack1111ll11ll_opy_: bstack111l11lll1_opy_, bstack111l11ll11_opy_=False):
        if event == bstack11l1111_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬဳ"):
            bstack1111ll11ll_opy_.set(hooks=self.store[bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨဴ")])
        if event == bstack11l1111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ဵ"):
            event = bstack11l1111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨံ")
        if bstack111l11ll11_opy_:
            bstack111l11l11l_opy_ = {
                bstack11l1111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ့ࠫ"): event,
                bstack1111ll11ll_opy_.bstack1111llllll_opy_(): bstack1111ll11ll_opy_.bstack111l111l1l_opy_(event)
            }
            with self._lock:
                self.bstack111l1lll1l_opy_.append(bstack111l11l11l_opy_)
        else:
            bstack111lll111_opy_.bstack111ll111ll_opy_(event, bstack1111ll11ll_opy_)
class bstack111l1l1111_opy_:
    def __init__(self):
        self._1111ll1l1l_opy_ = []
    def bstack111l1l1lll_opy_(self):
        self._1111ll1l1l_opy_.append([])
    def bstack111l11llll_opy_(self):
        return self._1111ll1l1l_opy_.pop() if self._1111ll1l1l_opy_ else list()
    def push(self, message):
        self._1111ll1l1l_opy_[-1].append(message) if self._1111ll1l1l_opy_ else self._1111ll1l1l_opy_.append([message])
class bstack1111ll1lll_opy_:
    FAIL = bstack11l1111_opy_ (u"ࠨࡈࡄࡍࡑ࠭း")
    ERROR = bstack11l1111_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ္")
    WARNING = bstack11l1111_opy_ (u"࡛ࠪࡆࡘࡎࠨ်")
    bstack111l111111_opy_ = bstack11l1111_opy_ (u"ࠫࡎࡔࡆࡐࠩျ")
    DEBUG = bstack11l1111_opy_ (u"ࠬࡊࡅࡃࡗࡊࠫြ")
    TRACE = bstack11l1111_opy_ (u"࠭ࡔࡓࡃࡆࡉࠬွ")
    bstack111l1lll11_opy_ = [FAIL, ERROR]
def bstack111l11l111_opy_(bstack111ll11111_opy_):
    if not bstack111ll11111_opy_:
        return None
    if bstack111ll11111_opy_.get(bstack11l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪှ"), None):
        return getattr(bstack111ll11111_opy_[bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫဿ")], bstack11l1111_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ၀"), None)
    return bstack111ll11111_opy_.get(bstack11l1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ၁"), None)
def bstack111l11l1ll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11l1111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ၂"), bstack11l1111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ၃")]:
        return
    if hook_type.lower() == bstack11l1111_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ၄"):
        if current_test_uuid is None:
            return bstack11l1111_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ၅")
        else:
            return bstack11l1111_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭၆")
    elif hook_type.lower() == bstack11l1111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ၇"):
        if current_test_uuid is None:
            return bstack11l1111_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭၈")
        else:
            return bstack11l1111_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ၉")