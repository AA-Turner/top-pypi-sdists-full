# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111l1l11ll_opy_ import RobotHandler
from bstack_utils.capture import bstack111lll1l11_opy_
from bstack_utils.bstack111lll1ll1_opy_ import bstack1111ll1l1l_opy_, bstack111lll111l_opy_, bstack111lll1111_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack11l1l111l1_opy_
from bstack_utils.bstack111ll1ll1l_opy_ import bstack1ll111lll1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll11lll1l_opy_, bstack111ll11ll_opy_, Result, \
    bstack1111ll1lll_opy_, bstack111l1l111l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪཹ"): [],
        bstack1l1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸེ࠭"): [],
        bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷཻࠬ"): []
    }
    bstack111l11llll_opy_ = []
    bstack1111ll11l1_opy_ = []
    @staticmethod
    def bstack111ll1l111_opy_(log):
        if not ((isinstance(log[bstack1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧོࠪ")], list) or (isinstance(log[bstack1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨཽࠫ")], dict)) and len(log[bstack1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཾ")])>0) or (isinstance(log[bstack1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཿ")], str) and log[bstack1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ྀࠧ")].strip())):
            return
        active = bstack11l1l111l1_opy_.bstack111lll1lll_opy_()
        log = {
            bstack1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱཱྀ࠭"): log[bstack1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧྂ")],
            bstack1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬྃ"): bstack111l1l111l_opy_().isoformat() + bstack1l1_opy_ (u"ࠪ࡞྄ࠬ"),
            bstack1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ྅"): log[bstack1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭྆")],
        }
        if active:
            if active[bstack1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ྇")] == bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬྈ"):
                log[bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨྉ")] = active[bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩྊ")]
            elif active[bstack1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨྋ")] == bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࠩྌ"):
                log[bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬྍ")] = active[bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ྎ")]
        bstack1ll111lll1_opy_.bstack1ll11lll1_opy_([log])
    def __init__(self):
        self.messages = bstack1111llll1l_opy_()
        self._1111ll1l11_opy_ = None
        self._111l1l1111_opy_ = None
        self._111l11l11l_opy_ = OrderedDict()
        self.bstack111ll11ll1_opy_ = bstack111lll1l11_opy_(self.bstack111ll1l111_opy_)
    @bstack1111ll1lll_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1l1ll1_opy_()
        if not self._111l11l11l_opy_.get(attrs.get(bstack1l1_opy_ (u"ࠧࡪࡦࠪྏ")), None):
            self._111l11l11l_opy_[attrs.get(bstack1l1_opy_ (u"ࠨ࡫ࡧࠫྐ"))] = {}
        bstack111l11ll11_opy_ = bstack111lll1111_opy_(
                bstack111l1ll1ll_opy_=attrs.get(bstack1l1_opy_ (u"ࠩ࡬ࡨࠬྑ")),
                name=name,
                started_at=bstack111ll11ll_opy_(),
                file_path=os.path.relpath(attrs[bstack1l1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪྒ")], start=os.getcwd()) if attrs.get(bstack1l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫྒྷ")) != bstack1l1_opy_ (u"ࠬ࠭ྔ") else bstack1l1_opy_ (u"࠭ࠧྕ"),
                framework=bstack1l1_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ྖ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l1_opy_ (u"ࠨ࡫ࡧࠫྗ"), None)
        self._111l11l11l_opy_[attrs.get(bstack1l1_opy_ (u"ࠩ࡬ࡨࠬ྘"))][bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྙ")] = bstack111l11ll11_opy_
    @bstack1111ll1lll_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111l11ll1l_opy_()
        self._1111ll11ll_opy_(messages)
        with self._lock:
            for bstack111l1l1lll_opy_ in self.bstack111l11llll_opy_:
                bstack111l1l1lll_opy_[bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ྚ")][bstack1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫྛ")].extend(self.store[bstack1l1_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬྜ")])
                bstack1ll111lll1_opy_.bstack11l1111l1l_opy_(bstack111l1l1lll_opy_)
            self.bstack111l11llll_opy_ = []
            self.store[bstack1l1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ྜྷ")] = []
    @bstack1111ll1lll_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111ll11ll1_opy_.start()
        if not self._111l11l11l_opy_.get(attrs.get(bstack1l1_opy_ (u"ࠨ࡫ࡧࠫྞ")), None):
            self._111l11l11l_opy_[attrs.get(bstack1l1_opy_ (u"ࠩ࡬ࡨࠬྟ"))] = {}
        driver = bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩྠ"), None)
        bstack111lll1ll1_opy_ = bstack111lll1111_opy_(
            bstack111l1ll1ll_opy_=attrs.get(bstack1l1_opy_ (u"ࠫ࡮ࡪࠧྡ")),
            name=name,
            started_at=bstack111ll11ll_opy_(),
            file_path=os.path.relpath(attrs[bstack1l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬྡྷ")], start=os.getcwd()),
            scope=RobotHandler.bstack1111lllll1_opy_(attrs.get(bstack1l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ྣ"), None)),
            framework=bstack1l1_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ྤ"),
            tags=attrs[bstack1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ྥ")],
            hooks=self.store[bstack1l1_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨྦ")],
            bstack111ll1l1ll_opy_=bstack1ll111lll1_opy_.bstack111ll1lll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l1_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧྦྷ").format(bstack1l1_opy_ (u"ࠦࠥࠨྨ").join(attrs[bstack1l1_opy_ (u"ࠬࡺࡡࡨࡵࠪྩ")]), name) if attrs[bstack1l1_opy_ (u"࠭ࡴࡢࡩࡶࠫྪ")] else name
        )
        self._111l11l11l_opy_[attrs.get(bstack1l1_opy_ (u"ࠧࡪࡦࠪྫ"))][bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྫྷ")] = bstack111lll1ll1_opy_
        threading.current_thread().current_test_uuid = bstack111lll1ll1_opy_.bstack111l11l111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l1_opy_ (u"ࠩ࡬ࡨࠬྭ"), None)
        self.bstack111ll111l1_opy_(bstack1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫྮ"), bstack111lll1ll1_opy_)
    @bstack1111ll1lll_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111ll11ll1_opy_.reset()
        bstack1111ll1ll1_opy_ = bstack111l11l1ll_opy_.get(attrs.get(bstack1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫྯ")), bstack1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ྰ"))
        self._111l11l11l_opy_[attrs.get(bstack1l1_opy_ (u"࠭ࡩࡥࠩྱ"))][bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪྲ")].stop(time=bstack111ll11ll_opy_(), duration=int(attrs.get(bstack1l1_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ླ"), bstack1l1_opy_ (u"ࠩ࠳ࠫྴ"))), result=Result(result=bstack1111ll1ll1_opy_, exception=attrs.get(bstack1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྵ")), bstack111ll1l11l_opy_=[attrs.get(bstack1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྶ"))]))
        self.bstack111ll111l1_opy_(bstack1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧྷ"), self._111l11l11l_opy_[attrs.get(bstack1l1_opy_ (u"࠭ࡩࡥࠩྸ"))][bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪྐྵ")], True)
        with self._lock:
            self.store[bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬྺ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1111ll1lll_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1l1ll1_opy_()
        current_test_id = bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫྻ"), None)
        bstack111l111ll1_opy_ = current_test_id if bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬྼ"), None) else bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧ྽"), None)
        if attrs.get(bstack1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ྾"), bstack1l1_opy_ (u"࠭ࠧ྿")).lower() in [bstack1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭࿀"), bstack1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ࿁")]:
            hook_type = bstack111ll11111_opy_(attrs.get(bstack1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ࿂")), bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ࿃"), None))
            hook_name = bstack1l1_opy_ (u"ࠫࢀࢃࠧ࿄").format(attrs.get(bstack1l1_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ࿅"), bstack1l1_opy_ (u"࿆࠭ࠧ")))
            if hook_type in [bstack1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ࿇"), bstack1l1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ࿈")]:
                hook_name = bstack1l1_opy_ (u"ࠩ࡞ࡿࢂࡣࠠࡼࡿࠪ࿉").format(bstack111l1ll11l_opy_.get(hook_type), attrs.get(bstack1l1_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ࿊"), bstack1l1_opy_ (u"ࠫࠬ࿋")))
            bstack111l1ll1l1_opy_ = bstack111lll111l_opy_(
                bstack111l1ll1ll_opy_=bstack111l111ll1_opy_ + bstack1l1_opy_ (u"ࠬ࠳ࠧ࿌") + attrs.get(bstack1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ࿍"), bstack1l1_opy_ (u"ࠧࠨ࿎")).lower(),
                name=hook_name,
                started_at=bstack111ll11ll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ࿏")), start=os.getcwd()),
                framework=bstack1l1_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ࿐"),
                tags=attrs[bstack1l1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ࿑")],
                scope=RobotHandler.bstack1111lllll1_opy_(attrs.get(bstack1l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ࿒"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l1ll1l1_opy_.bstack111l11l111_opy_()
            threading.current_thread().current_hook_id = bstack111l111ll1_opy_ + bstack1l1_opy_ (u"ࠬ࠳ࠧ࿓") + attrs.get(bstack1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ࿔"), bstack1l1_opy_ (u"ࠧࠨ࿕")).lower()
            with self._lock:
                self.store[bstack1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ࿖")] = [bstack111l1ll1l1_opy_.bstack111l11l111_opy_()]
                if bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭࿗"), None):
                    self.store[bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ࿘")].append(bstack111l1ll1l1_opy_.bstack111l11l111_opy_())
                else:
                    self.store[bstack1l1_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ࿙")].append(bstack111l1ll1l1_opy_.bstack111l11l111_opy_())
            if bstack111l111ll1_opy_:
                self._111l11l11l_opy_[bstack111l111ll1_opy_ + bstack1l1_opy_ (u"ࠬ࠳ࠧ࿚") + attrs.get(bstack1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ࿛"), bstack1l1_opy_ (u"ࠧࠨ࿜")).lower()] = { bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿝"): bstack111l1ll1l1_opy_ }
            bstack1ll111lll1_opy_.bstack111ll111l1_opy_(bstack1l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ࿞"), bstack111l1ll1l1_opy_)
        else:
            bstack111ll11l1l_opy_ = {
                bstack1l1_opy_ (u"ࠪ࡭ࡩ࠭࿟"): uuid4().__str__(),
                bstack1l1_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ࿠"): bstack1l1_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫ࿡").format(attrs.get(bstack1l1_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭࿢")), attrs.get(bstack1l1_opy_ (u"ࠧࡢࡴࡪࡷࠬ࿣"), bstack1l1_opy_ (u"ࠨࠩ࿤"))) if attrs.get(bstack1l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ࿥"), []) else attrs.get(bstack1l1_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ࿦")),
                bstack1l1_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫ࿧"): attrs.get(bstack1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪ࿨"), []),
                bstack1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ࿩"): bstack111ll11ll_opy_(),
                bstack1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ࿪"): bstack1l1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ࿫"),
                bstack1l1_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ࿬"): attrs.get(bstack1l1_opy_ (u"ࠪࡨࡴࡩࠧ࿭"), bstack1l1_opy_ (u"ࠫࠬ࿮"))
            }
            if attrs.get(bstack1l1_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭࿯"), bstack1l1_opy_ (u"࠭ࠧ࿰")) != bstack1l1_opy_ (u"ࠧࠨ࿱"):
                bstack111ll11l1l_opy_[bstack1l1_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩ࿲")] = attrs.get(bstack1l1_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪ࿳"))
            if not self.bstack1111ll11l1_opy_:
                self._111l11l11l_opy_[self._1111lll111_opy_()][bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿴")].add_step(bstack111ll11l1l_opy_)
                threading.current_thread().current_step_uuid = bstack111ll11l1l_opy_[bstack1l1_opy_ (u"ࠫ࡮ࡪࠧ࿵")]
            self.bstack1111ll11l1_opy_.append(bstack111ll11l1l_opy_)
    @bstack1111ll1lll_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111l11ll1l_opy_()
        self._1111ll11ll_opy_(messages)
        current_test_id = bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ࿶"), None)
        bstack111l111ll1_opy_ = current_test_id if current_test_id else bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ࿷"), None)
        bstack1111llllll_opy_ = bstack111l11l1ll_opy_.get(attrs.get(bstack1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ࿸")), bstack1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ࿹"))
        bstack1111lll11l_opy_ = attrs.get(bstack1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿺"))
        if bstack1111llllll_opy_ != bstack1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ࿻") and not attrs.get(bstack1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿼")) and self._1111ll1l11_opy_:
            bstack1111lll11l_opy_ = self._1111ll1l11_opy_
        bstack111ll1111l_opy_ = Result(result=bstack1111llllll_opy_, exception=bstack1111lll11l_opy_, bstack111ll1l11l_opy_=[bstack1111lll11l_opy_])
        if attrs.get(bstack1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿽"), bstack1l1_opy_ (u"࠭ࠧ࿾")).lower() in [bstack1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭࿿"), bstack1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪက")]:
            bstack111l111ll1_opy_ = current_test_id if current_test_id else bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬခ"), None)
            if bstack111l111ll1_opy_:
                bstack111lll11l1_opy_ = bstack111l111ll1_opy_ + bstack1l1_opy_ (u"ࠥ࠱ࠧဂ") + attrs.get(bstack1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩဃ"), bstack1l1_opy_ (u"ࠬ࠭င")).lower()
                self._111l11l11l_opy_[bstack111lll11l1_opy_][bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩစ")].stop(time=bstack111ll11ll_opy_(), duration=int(attrs.get(bstack1l1_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬဆ"), bstack1l1_opy_ (u"ࠨ࠲ࠪဇ"))), result=bstack111ll1111l_opy_)
                bstack1ll111lll1_opy_.bstack111ll111l1_opy_(bstack1l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫဈ"), self._111l11l11l_opy_[bstack111lll11l1_opy_][bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ဉ")])
        else:
            bstack111l111ll1_opy_ = current_test_id if current_test_id else bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢ࡭ࡩ࠭ည"), None)
            if bstack111l111ll1_opy_ and len(self.bstack1111ll11l1_opy_) == 1:
                current_step_uuid = bstack1ll11lll1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩဋ"), None)
                self._111l11l11l_opy_[bstack111l111ll1_opy_][bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩဌ")].bstack111llll111_opy_(current_step_uuid, duration=int(attrs.get(bstack1l1_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬဍ"), bstack1l1_opy_ (u"ࠨ࠲ࠪဎ"))), result=bstack111ll1111l_opy_)
            else:
                self.bstack111l111l1l_opy_(attrs)
            self.bstack1111ll11l1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l1_opy_ (u"ࠩ࡫ࡸࡲࡲࠧဏ"), bstack1l1_opy_ (u"ࠪࡲࡴ࠭တ")) == bstack1l1_opy_ (u"ࠫࡾ࡫ࡳࠨထ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l1l111l1_opy_.bstack111lll1lll_opy_():
                logs.append({
                    bstack1l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨဒ"): bstack111ll11ll_opy_(),
                    bstack1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧဓ"): message.get(bstack1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨန")),
                    bstack1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧပ"): message.get(bstack1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨဖ")),
                    **bstack11l1l111l1_opy_.bstack111lll1lll_opy_()
                })
                if len(logs) > 0:
                    bstack1ll111lll1_opy_.bstack1ll11lll1_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1ll111lll1_opy_.bstack111l11111l_opy_()
    def bstack111l111l1l_opy_(self, bstack1111lll1ll_opy_):
        if not bstack11l1l111l1_opy_.bstack111lll1lll_opy_():
            return
        kwname = bstack1l1_opy_ (u"ࠪࡿࢂࠦࡻࡾࠩဗ").format(bstack1111lll1ll_opy_.get(bstack1l1_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫဘ")), bstack1111lll1ll_opy_.get(bstack1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪမ"), bstack1l1_opy_ (u"࠭ࠧယ"))) if bstack1111lll1ll_opy_.get(bstack1l1_opy_ (u"ࠧࡢࡴࡪࡷࠬရ"), []) else bstack1111lll1ll_opy_.get(bstack1l1_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨလ"))
        error_message = bstack1l1_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠡࡾࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠ࡝ࠤࡾ࠶ࢂࡢࠢࠣဝ").format(kwname, bstack1111lll1ll_opy_.get(bstack1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪသ")), str(bstack1111lll1ll_opy_.get(bstack1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬဟ"))))
        bstack111l111lll_opy_ = bstack1l1_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠦဠ").format(kwname, bstack1111lll1ll_opy_.get(bstack1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭အ")))
        bstack111l1l1l11_opy_ = error_message if bstack1111lll1ll_opy_.get(bstack1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨဢ")) else bstack111l111lll_opy_
        bstack111l1111l1_opy_ = {
            bstack1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫဣ"): self.bstack1111ll11l1_opy_[-1].get(bstack1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ဤ"), bstack111ll11ll_opy_()),
            bstack1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫဥ"): bstack111l1l1l11_opy_,
            bstack1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪဦ"): bstack1l1_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫဧ") if bstack1111lll1ll_opy_.get(bstack1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ဨ")) == bstack1l1_opy_ (u"ࠧࡇࡃࡌࡐࠬဩ") else bstack1l1_opy_ (u"ࠨࡋࡑࡊࡔ࠭ဪ"),
            **bstack11l1l111l1_opy_.bstack111lll1lll_opy_()
        }
        bstack1ll111lll1_opy_.bstack1ll11lll1_opy_([bstack111l1111l1_opy_])
    def _1111lll111_opy_(self):
        for bstack111l1ll1ll_opy_ in reversed(self._111l11l11l_opy_):
            bstack1111llll11_opy_ = bstack111l1ll1ll_opy_
            data = self._111l11l11l_opy_[bstack111l1ll1ll_opy_][bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬါ")]
            if isinstance(data, bstack111lll111l_opy_):
                if not bstack1l1_opy_ (u"ࠪࡉࡆࡉࡈࠨာ") in data.bstack111l111111_opy_():
                    return bstack1111llll11_opy_
            else:
                return bstack1111llll11_opy_
    def _1111ll11ll_opy_(self, messages):
        try:
            bstack111l1lll1l_opy_ = BuiltIn().get_variable_value(bstack1l1_opy_ (u"ࠦࠩࢁࡌࡐࡉࠣࡐࡊ࡜ࡅࡍࡿࠥိ")) in (bstack111l11l1l1_opy_.DEBUG, bstack111l11l1l1_opy_.TRACE)
            for message, bstack111l1l11l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ီ"))
                level = message.get(bstack1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬု"))
                if level == bstack111l11l1l1_opy_.FAIL:
                    self._1111ll1l11_opy_ = name or self._1111ll1l11_opy_
                    self._111l1l1111_opy_ = bstack111l1l11l1_opy_.get(bstack1l1_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣူ")) if bstack111l1lll1l_opy_ and bstack111l1l11l1_opy_ else self._111l1l1111_opy_
        except:
            pass
    @classmethod
    def bstack111ll111l1_opy_(self, event: str, bstack111l1l1l1l_opy_: bstack1111ll1l1l_opy_, bstack111l1lll11_opy_=False):
        if event == bstack1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪေ"):
            bstack111l1l1l1l_opy_.set(hooks=self.store[bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ဲ")])
        if event == bstack1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫဳ"):
            event = bstack1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ဴ")
        if bstack111l1lll11_opy_:
            bstack111l11lll1_opy_ = {
                bstack1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩဵ"): event,
                bstack111l1l1l1l_opy_.bstack111l1llll1_opy_(): bstack111l1l1l1l_opy_.bstack111l1111ll_opy_(event)
            }
            with self._lock:
                self.bstack111l11llll_opy_.append(bstack111l11lll1_opy_)
        else:
            bstack1ll111lll1_opy_.bstack111ll111l1_opy_(event, bstack111l1l1l1l_opy_)
class bstack1111llll1l_opy_:
    def __init__(self):
        self._111l111l11_opy_ = []
    def bstack111l1l1ll1_opy_(self):
        self._111l111l11_opy_.append([])
    def bstack111l11ll1l_opy_(self):
        return self._111l111l11_opy_.pop() if self._111l111l11_opy_ else list()
    def push(self, message):
        self._111l111l11_opy_[-1].append(message) if self._111l111l11_opy_ else self._111l111l11_opy_.append([message])
class bstack111l11l1l1_opy_:
    FAIL = bstack1l1_opy_ (u"࠭ࡆࡂࡋࡏࠫံ")
    ERROR = bstack1l1_opy_ (u"ࠧࡆࡔࡕࡓࡗ့࠭")
    WARNING = bstack1l1_opy_ (u"ࠨ࡙ࡄࡖࡓ࠭း")
    bstack1111lll1l1_opy_ = bstack1l1_opy_ (u"ࠩࡌࡒࡋࡕ္ࠧ")
    DEBUG = bstack1l1_opy_ (u"ࠪࡈࡊࡈࡕࡈ်ࠩ")
    TRACE = bstack1l1_opy_ (u"࡙ࠫࡘࡁࡄࡇࠪျ")
    bstack1111ll111l_opy_ = [FAIL, ERROR]
def bstack111l1lllll_opy_(bstack111l1ll111_opy_):
    if not bstack111l1ll111_opy_:
        return None
    if bstack111l1ll111_opy_.get(bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨြ"), None):
        return getattr(bstack111l1ll111_opy_[bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩွ")], bstack1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬှ"), None)
    return bstack111l1ll111_opy_.get(bstack1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ဿ"), None)
def bstack111ll11111_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ၀"), bstack1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ၁")]:
        return
    if hook_type.lower() == bstack1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ၂"):
        if current_test_uuid is None:
            return bstack1l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩ၃")
        else:
            return bstack1l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ၄")
    elif hook_type.lower() == bstack1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ၅"):
        if current_test_uuid is None:
            return bstack1l1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ၆")
        else:
            return bstack1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭၇")