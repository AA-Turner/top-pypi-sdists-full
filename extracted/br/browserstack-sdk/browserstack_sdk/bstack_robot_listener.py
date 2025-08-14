# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111l11l1l1_opy_ import RobotHandler
from bstack_utils.capture import bstack111ll1l1ll_opy_
from bstack_utils.bstack111lll1lll_opy_ import bstack111l1111ll_opy_, bstack111ll1l1l1_opy_, bstack111lll111l_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l1ll1l11l_opy_
from bstack_utils.bstack111ll1l111_opy_ import bstack1llllll11l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l111l1l_opy_, bstack11lllll1_opy_, Result, \
    error_handler, bstack111l11ll1l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1l1l1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬྂ"): [],
        bstack1l1l1ll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨྃ"): [],
        bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ྄ࠧ"): []
    }
    bstack111l111111_opy_ = []
    bstack111l1l1lll_opy_ = []
    @staticmethod
    def bstack111ll11l1l_opy_(log):
        if not ((isinstance(log[bstack1l1l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ྅")], list) or (isinstance(log[bstack1l1l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭྆")], dict)) and len(log[bstack1l1l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ྇")])>0) or (isinstance(log[bstack1l1l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྈ")], str) and log[bstack1l1l1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྉ")].strip())):
            return
        active = bstack1l1ll1l11l_opy_.bstack111ll1ll11_opy_()
        log = {
            bstack1l1l1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨྊ"): log[bstack1l1l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩྋ")],
            bstack1l1l1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧྌ"): bstack111l11ll1l_opy_().isoformat() + bstack1l1l1ll_opy_ (u"ࠬࡠࠧྍ"),
            bstack1l1l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྎ"): log[bstack1l1l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྏ")],
        }
        if active:
            if active[bstack1l1l1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ྐ")] == bstack1l1l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧྑ"):
                log[bstack1l1l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪྒ")] = active[bstack1l1l1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫྒྷ")]
            elif active[bstack1l1l1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪྔ")] == bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷࠫྕ"):
                log[bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧྖ")] = active[bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨྗ")]
        bstack1llllll11l_opy_.bstack1lll1ll11l_opy_([log])
    def __init__(self):
        self.messages = bstack1111ll1ll1_opy_()
        self._111l1l1ll1_opy_ = None
        self._1111lll11l_opy_ = None
        self._111l1l11l1_opy_ = OrderedDict()
        self.bstack111lll11ll_opy_ = bstack111ll1l1ll_opy_(self.bstack111ll11l1l_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1l1111_opy_()
        if not self._111l1l11l1_opy_.get(attrs.get(bstack1l1l1ll_opy_ (u"ࠩ࡬ࡨࠬ྘")), None):
            self._111l1l11l1_opy_[attrs.get(bstack1l1l1ll_opy_ (u"ࠪ࡭ࡩ࠭ྙ"))] = {}
        bstack111l11ll11_opy_ = bstack111lll111l_opy_(
                bstack1111ll1l1l_opy_=attrs.get(bstack1l1l1ll_opy_ (u"ࠫ࡮ࡪࠧྚ")),
                name=name,
                started_at=bstack11lllll1_opy_(),
                file_path=os.path.relpath(attrs[bstack1l1l1ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬྛ")], start=os.getcwd()) if attrs.get(bstack1l1l1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ྜ")) != bstack1l1l1ll_opy_ (u"ࠧࠨྜྷ") else bstack1l1l1ll_opy_ (u"ࠨࠩྞ"),
                framework=bstack1l1l1ll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨྟ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l1l1ll_opy_ (u"ࠪ࡭ࡩ࠭ྠ"), None)
        self._111l1l11l1_opy_[attrs.get(bstack1l1l1ll_opy_ (u"ࠫ࡮ࡪࠧྡ"))][bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨྡྷ")] = bstack111l11ll11_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1111llll11_opy_()
        self._111l1lll1l_opy_(messages)
        with self._lock:
            for bstack111l1ll11l_opy_ in self.bstack111l111111_opy_:
                bstack111l1ll11l_opy_[bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨྣ")][bstack1l1l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ྤ")].extend(self.store[bstack1l1l1ll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧྥ")])
                bstack1llllll11l_opy_.bstack11ll11l1ll_opy_(bstack111l1ll11l_opy_)
            self.bstack111l111111_opy_ = []
            self.store[bstack1l1l1ll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨྦ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111lll11ll_opy_.start()
        if not self._111l1l11l1_opy_.get(attrs.get(bstack1l1l1ll_opy_ (u"ࠪ࡭ࡩ࠭ྦྷ")), None):
            self._111l1l11l1_opy_[attrs.get(bstack1l1l1ll_opy_ (u"ࠫ࡮ࡪࠧྨ"))] = {}
        driver = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫྩ"), None)
        bstack111lll1lll_opy_ = bstack111lll111l_opy_(
            bstack1111ll1l1l_opy_=attrs.get(bstack1l1l1ll_opy_ (u"࠭ࡩࡥࠩྪ")),
            name=name,
            started_at=bstack11lllll1_opy_(),
            file_path=os.path.relpath(attrs[bstack1l1l1ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧྫ")], start=os.getcwd()),
            scope=RobotHandler.bstack111l11111l_opy_(attrs.get(bstack1l1l1ll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨྫྷ"), None)),
            framework=bstack1l1l1ll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨྭ"),
            tags=attrs[bstack1l1l1ll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨྮ")],
            hooks=self.store[bstack1l1l1ll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪྯ")],
            bstack111ll1ll1l_opy_=bstack1llllll11l_opy_.bstack111lll1l11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l1l1ll_opy_ (u"ࠧࢁࡽࠡ࡞ࡱࠤࢀࢃࠢྰ").format(bstack1l1l1ll_opy_ (u"ࠨࠠࠣྱ").join(attrs[bstack1l1l1ll_opy_ (u"ࠧࡵࡣࡪࡷࠬྲ")]), name) if attrs[bstack1l1l1ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ླ")] else name
        )
        self._111l1l11l1_opy_[attrs.get(bstack1l1l1ll_opy_ (u"ࠩ࡬ࡨࠬྴ"))][bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྵ")] = bstack111lll1lll_opy_
        threading.current_thread().current_test_uuid = bstack111lll1lll_opy_.bstack111l1lllll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l1l1ll_opy_ (u"ࠫ࡮ࡪࠧྶ"), None)
        self.bstack111ll1llll_opy_(bstack1l1l1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ྷ"), bstack111lll1lll_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111lll11ll_opy_.reset()
        bstack111l111lll_opy_ = bstack111l1l11ll_opy_.get(attrs.get(bstack1l1l1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ྸ")), bstack1l1l1ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨྐྵ"))
        self._111l1l11l1_opy_[attrs.get(bstack1l1l1ll_opy_ (u"ࠨ࡫ࡧࠫྺ"))][bstack1l1l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྻ")].stop(time=bstack11lllll1_opy_(), duration=int(attrs.get(bstack1l1l1ll_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨྼ"), bstack1l1l1ll_opy_ (u"ࠫ࠵࠭྽"))), result=Result(result=bstack111l111lll_opy_, exception=attrs.get(bstack1l1l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭྾")), bstack111lll1l1l_opy_=[attrs.get(bstack1l1l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ྿"))]))
        self.bstack111ll1llll_opy_(bstack1l1l1ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ࿀"), self._111l1l11l1_opy_[attrs.get(bstack1l1l1ll_opy_ (u"ࠨ࡫ࡧࠫ࿁"))][bstack1l1l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿂")], True)
        with self._lock:
            self.store[bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ࿃")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1l1111_opy_()
        current_test_id = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭࿄"), None)
        bstack111l111ll1_opy_ = current_test_id if bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ࿅"), None) else bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥ࿆ࠩ"), None)
        if attrs.get(bstack1l1l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬ࿇"), bstack1l1l1ll_opy_ (u"ࠨࠩ࿈")).lower() in [bstack1l1l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ࿉"), bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ࿊")]:
            hook_type = bstack111l1ll111_opy_(attrs.get(bstack1l1l1ll_opy_ (u"ࠫࡹࡿࡰࡦࠩ࿋")), bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ࿌"), None))
            hook_name = bstack1l1l1ll_opy_ (u"࠭ࡻࡾࠩ࿍").format(attrs.get(bstack1l1l1ll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ࿎"), bstack1l1l1ll_opy_ (u"ࠨࠩ࿏")))
            if hook_type in [bstack1l1l1ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭࿐"), bstack1l1l1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭࿑")]:
                hook_name = bstack1l1l1ll_opy_ (u"ࠫࡠࢁࡽ࡞ࠢࡾࢁࠬ࿒").format(bstack111l11lll1_opy_.get(hook_type), attrs.get(bstack1l1l1ll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ࿓"), bstack1l1l1ll_opy_ (u"࠭ࠧ࿔")))
            bstack1111ll1l11_opy_ = bstack111ll1l1l1_opy_(
                bstack1111ll1l1l_opy_=bstack111l111ll1_opy_ + bstack1l1l1ll_opy_ (u"ࠧ࠮ࠩ࿕") + attrs.get(bstack1l1l1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭࿖"), bstack1l1l1ll_opy_ (u"ࠩࠪ࿗")).lower(),
                name=hook_name,
                started_at=bstack11lllll1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l1l1ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ࿘")), start=os.getcwd()),
                framework=bstack1l1l1ll_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪ࿙"),
                tags=attrs[bstack1l1l1ll_opy_ (u"ࠬࡺࡡࡨࡵࠪ࿚")],
                scope=RobotHandler.bstack111l11111l_opy_(attrs.get(bstack1l1l1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭࿛"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1111ll1l11_opy_.bstack111l1lllll_opy_()
            threading.current_thread().current_hook_id = bstack111l111ll1_opy_ + bstack1l1l1ll_opy_ (u"ࠧ࠮ࠩ࿜") + attrs.get(bstack1l1l1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭࿝"), bstack1l1l1ll_opy_ (u"ࠩࠪ࿞")).lower()
            with self._lock:
                self.store[bstack1l1l1ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ࿟")] = [bstack1111ll1l11_opy_.bstack111l1lllll_opy_()]
                if bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ࿠"), None):
                    self.store[bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ࿡")].append(bstack1111ll1l11_opy_.bstack111l1lllll_opy_())
                else:
                    self.store[bstack1l1l1ll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ࿢")].append(bstack1111ll1l11_opy_.bstack111l1lllll_opy_())
            if bstack111l111ll1_opy_:
                self._111l1l11l1_opy_[bstack111l111ll1_opy_ + bstack1l1l1ll_opy_ (u"ࠧ࠮ࠩ࿣") + attrs.get(bstack1l1l1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭࿤"), bstack1l1l1ll_opy_ (u"ࠩࠪ࿥")).lower()] = { bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿦"): bstack1111ll1l11_opy_ }
            bstack1llllll11l_opy_.bstack111ll1llll_opy_(bstack1l1l1ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ࿧"), bstack1111ll1l11_opy_)
        else:
            bstack111ll1l11l_opy_ = {
                bstack1l1l1ll_opy_ (u"ࠬ࡯ࡤࠨ࿨"): uuid4().__str__(),
                bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡺࡷࠫ࿩"): bstack1l1l1ll_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭࿪").format(attrs.get(bstack1l1l1ll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ࿫")), attrs.get(bstack1l1l1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ࿬"), bstack1l1l1ll_opy_ (u"ࠪࠫ࿭"))) if attrs.get(bstack1l1l1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩ࿮"), []) else attrs.get(bstack1l1l1ll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ࿯")),
                bstack1l1l1ll_opy_ (u"࠭ࡳࡵࡧࡳࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭࿰"): attrs.get(bstack1l1l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬ࿱"), []),
                bstack1l1l1ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ࿲"): bstack11lllll1_opy_(),
                bstack1l1l1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ࿳"): bstack1l1l1ll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ࿴"),
                bstack1l1l1ll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ࿵"): attrs.get(bstack1l1l1ll_opy_ (u"ࠬࡪ࡯ࡤࠩ࿶"), bstack1l1l1ll_opy_ (u"࠭ࠧ࿷"))
            }
            if attrs.get(bstack1l1l1ll_opy_ (u"ࠧ࡭࡫ࡥࡲࡦࡳࡥࠨ࿸"), bstack1l1l1ll_opy_ (u"ࠨࠩ࿹")) != bstack1l1l1ll_opy_ (u"ࠩࠪ࿺"):
                bstack111ll1l11l_opy_[bstack1l1l1ll_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ࿻")] = attrs.get(bstack1l1l1ll_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬ࿼"))
            if not self.bstack111l1l1lll_opy_:
                self._111l1l11l1_opy_[self._111l1llll1_opy_()][bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿽")].add_step(bstack111ll1l11l_opy_)
                threading.current_thread().current_step_uuid = bstack111ll1l11l_opy_[bstack1l1l1ll_opy_ (u"࠭ࡩࡥࠩ࿾")]
            self.bstack111l1l1lll_opy_.append(bstack111ll1l11l_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1111llll11_opy_()
        self._111l1lll1l_opy_(messages)
        current_test_id = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩ࿿"), None)
        bstack111l111ll1_opy_ = current_test_id if current_test_id else bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫက"), None)
        bstack111l11l1ll_opy_ = bstack111l1l11ll_opy_.get(attrs.get(bstack1l1l1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩခ")), bstack1l1l1ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫဂ"))
        bstack111ll11111_opy_ = attrs.get(bstack1l1l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬဃ"))
        if bstack111l11l1ll_opy_ != bstack1l1l1ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭င") and not attrs.get(bstack1l1l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧစ")) and self._111l1l1ll1_opy_:
            bstack111ll11111_opy_ = self._111l1l1ll1_opy_
        bstack111llll11l_opy_ = Result(result=bstack111l11l1ll_opy_, exception=bstack111ll11111_opy_, bstack111lll1l1l_opy_=[bstack111ll11111_opy_])
        if attrs.get(bstack1l1l1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬဆ"), bstack1l1l1ll_opy_ (u"ࠨࠩဇ")).lower() in [bstack1l1l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨဈ"), bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬဉ")]:
            bstack111l111ll1_opy_ = current_test_id if current_test_id else bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧည"), None)
            if bstack111l111ll1_opy_:
                bstack111ll11l11_opy_ = bstack111l111ll1_opy_ + bstack1l1l1ll_opy_ (u"ࠧ࠳ࠢဋ") + attrs.get(bstack1l1l1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫဌ"), bstack1l1l1ll_opy_ (u"ࠧࠨဍ")).lower()
                self._111l1l11l1_opy_[bstack111ll11l11_opy_][bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫဎ")].stop(time=bstack11lllll1_opy_(), duration=int(attrs.get(bstack1l1l1ll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧဏ"), bstack1l1l1ll_opy_ (u"ࠪ࠴ࠬတ"))), result=bstack111llll11l_opy_)
                bstack1llllll11l_opy_.bstack111ll1llll_opy_(bstack1l1l1ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ထ"), self._111l1l11l1_opy_[bstack111ll11l11_opy_][bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨဒ")])
        else:
            bstack111l111ll1_opy_ = current_test_id if current_test_id else bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤ࡯ࡤࠨဓ"), None)
            if bstack111l111ll1_opy_ and len(self.bstack111l1l1lll_opy_) == 1:
                current_step_uuid = bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫန"), None)
                self._111l1l11l1_opy_[bstack111l111ll1_opy_][bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫပ")].bstack111ll1111l_opy_(current_step_uuid, duration=int(attrs.get(bstack1l1l1ll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧဖ"), bstack1l1l1ll_opy_ (u"ࠪ࠴ࠬဗ"))), result=bstack111llll11l_opy_)
            else:
                self.bstack1111lll111_opy_(attrs)
            self.bstack111l1l1lll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l1l1ll_opy_ (u"ࠫ࡭ࡺ࡭࡭ࠩဘ"), bstack1l1l1ll_opy_ (u"ࠬࡴ࡯ࠨမ")) == bstack1l1l1ll_opy_ (u"࠭ࡹࡦࡵࠪယ"):
                return
            self.messages.push(message)
            logs = []
            if bstack1l1ll1l11l_opy_.bstack111ll1ll11_opy_():
                logs.append({
                    bstack1l1l1ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪရ"): bstack11lllll1_opy_(),
                    bstack1l1l1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩလ"): message.get(bstack1l1l1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဝ")),
                    bstack1l1l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩသ"): message.get(bstack1l1l1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪဟ")),
                    **bstack1l1ll1l11l_opy_.bstack111ll1ll11_opy_()
                })
                if len(logs) > 0:
                    bstack1llllll11l_opy_.bstack1lll1ll11l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1llllll11l_opy_.bstack111l1111l1_opy_()
    def bstack1111lll111_opy_(self, bstack111l11l11l_opy_):
        if not bstack1l1ll1l11l_opy_.bstack111ll1ll11_opy_():
            return
        kwname = bstack1l1l1ll_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫဠ").format(bstack111l11l11l_opy_.get(bstack1l1l1ll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭အ")), bstack111l11l11l_opy_.get(bstack1l1l1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬဢ"), bstack1l1l1ll_opy_ (u"ࠨࠩဣ"))) if bstack111l11l11l_opy_.get(bstack1l1l1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧဤ"), []) else bstack111l11l11l_opy_.get(bstack1l1l1ll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪဥ"))
        error_message = bstack1l1l1ll_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠣࢀࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢ࡟ࠦࢀ࠸ࡽ࡝ࠤࠥဦ").format(kwname, bstack111l11l11l_opy_.get(bstack1l1l1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬဧ")), str(bstack111l11l11l_opy_.get(bstack1l1l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧဨ"))))
        bstack1111lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠢ࡬ࡹࡱࡥࡲ࡫࠺ࠡ࡞ࠥࡿ࠵ࢃ࡜ࠣࠢࡿࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࡢࠢࡼ࠳ࢀࡠࠧࠨဩ").format(kwname, bstack111l11l11l_opy_.get(bstack1l1l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨဪ")))
        bstack111l1ll1ll_opy_ = error_message if bstack111l11l11l_opy_.get(bstack1l1l1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪါ")) else bstack1111lll1ll_opy_
        bstack111l1lll11_opy_ = {
            bstack1l1l1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ာ"): self.bstack111l1l1lll_opy_[-1].get(bstack1l1l1ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨိ"), bstack11lllll1_opy_()),
            bstack1l1l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ီ"): bstack111l1ll1ll_opy_,
            bstack1l1l1ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬု"): bstack1l1l1ll_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭ူ") if bstack111l11l11l_opy_.get(bstack1l1l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨေ")) == bstack1l1l1ll_opy_ (u"ࠩࡉࡅࡎࡒࠧဲ") else bstack1l1l1ll_opy_ (u"ࠪࡍࡓࡌࡏࠨဳ"),
            **bstack1l1ll1l11l_opy_.bstack111ll1ll11_opy_()
        }
        bstack1llllll11l_opy_.bstack1lll1ll11l_opy_([bstack111l1lll11_opy_])
    def _111l1llll1_opy_(self):
        for bstack1111ll1l1l_opy_ in reversed(self._111l1l11l1_opy_):
            bstack111l111l1l_opy_ = bstack1111ll1l1l_opy_
            data = self._111l1l11l1_opy_[bstack1111ll1l1l_opy_][bstack1l1l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧဴ")]
            if isinstance(data, bstack111ll1l1l1_opy_):
                if not bstack1l1l1ll_opy_ (u"ࠬࡋࡁࡄࡊࠪဵ") in data.bstack111l1ll1l1_opy_():
                    return bstack111l111l1l_opy_
            else:
                return bstack111l111l1l_opy_
    def _111l1lll1l_opy_(self, messages):
        try:
            bstack111l11llll_opy_ = BuiltIn().get_variable_value(bstack1l1l1ll_opy_ (u"ࠨࠤࡼࡎࡒࡋࠥࡒࡅࡗࡇࡏࢁࠧံ")) in (bstack111l11l111_opy_.DEBUG, bstack111l11l111_opy_.TRACE)
            for message, bstack1111ll11ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l1l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ့"))
                level = message.get(bstack1l1l1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧး"))
                if level == bstack111l11l111_opy_.FAIL:
                    self._111l1l1ll1_opy_ = name or self._111l1l1ll1_opy_
                    self._1111lll11l_opy_ = bstack1111ll11ll_opy_.get(bstack1l1l1ll_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧ္ࠥ")) if bstack111l11llll_opy_ and bstack1111ll11ll_opy_ else self._1111lll11l_opy_
        except:
            pass
    @classmethod
    def bstack111ll1llll_opy_(self, event: str, bstack111l111l11_opy_: bstack111l1111ll_opy_, bstack1111ll1lll_opy_=False):
        if event == bstack1l1l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨ်ࠬ"):
            bstack111l111l11_opy_.set(hooks=self.store[bstack1l1l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨျ")])
        if event == bstack1l1l1ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ြ"):
            event = bstack1l1l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨွ")
        if bstack1111ll1lll_opy_:
            bstack111l1l1l11_opy_ = {
                bstack1l1l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫှ"): event,
                bstack111l111l11_opy_.bstack1111llllll_opy_(): bstack111l111l11_opy_.bstack1111lllll1_opy_(event)
            }
            with self._lock:
                self.bstack111l111111_opy_.append(bstack111l1l1l11_opy_)
        else:
            bstack1llllll11l_opy_.bstack111ll1llll_opy_(event, bstack111l111l11_opy_)
class bstack1111ll1ll1_opy_:
    def __init__(self):
        self._111l1l1l1l_opy_ = []
    def bstack111l1l1111_opy_(self):
        self._111l1l1l1l_opy_.append([])
    def bstack1111llll11_opy_(self):
        return self._111l1l1l1l_opy_.pop() if self._111l1l1l1l_opy_ else list()
    def push(self, message):
        self._111l1l1l1l_opy_[-1].append(message) if self._111l1l1l1l_opy_ else self._111l1l1l1l_opy_.append([message])
class bstack111l11l111_opy_:
    FAIL = bstack1l1l1ll_opy_ (u"ࠨࡈࡄࡍࡑ࠭ဿ")
    ERROR = bstack1l1l1ll_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ၀")
    WARNING = bstack1l1l1ll_opy_ (u"࡛ࠪࡆࡘࡎࠨ၁")
    bstack1111lll1l1_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡎࡔࡆࡐࠩ၂")
    DEBUG = bstack1l1l1ll_opy_ (u"ࠬࡊࡅࡃࡗࡊࠫ၃")
    TRACE = bstack1l1l1ll_opy_ (u"࠭ࡔࡓࡃࡆࡉࠬ၄")
    bstack1111ll11l1_opy_ = [FAIL, ERROR]
def bstack1111llll1l_opy_(bstack111l1l111l_opy_):
    if not bstack111l1l111l_opy_:
        return None
    if bstack111l1l111l_opy_.get(bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ၅"), None):
        return getattr(bstack111l1l111l_opy_[bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ၆")], bstack1l1l1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ၇"), None)
    return bstack111l1l111l_opy_.get(bstack1l1l1ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ၈"), None)
def bstack111l1ll111_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l1l1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ၉"), bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ၊")]:
        return
    if hook_type.lower() == bstack1l1l1ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ။"):
        if current_test_uuid is None:
            return bstack1l1l1ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ၌")
        else:
            return bstack1l1l1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭၍")
    elif hook_type.lower() == bstack1l1l1ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ၎"):
        if current_test_uuid is None:
            return bstack1l1l1ll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭၏")
        else:
            return bstack1l1l1ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨၐ")