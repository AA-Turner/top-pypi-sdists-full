# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111l11l11l_opy_ import RobotHandler
from bstack_utils.capture import bstack111ll1ll1l_opy_
from bstack_utils.bstack111ll1l1ll_opy_ import bstack111l111l1l_opy_, bstack111lll1l11_opy_, bstack111l1lllll_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack1ll11lll1_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack11l1lllll1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l11l1lll_opy_, bstack1ll111ll1l_opy_, Result, \
    error_handler, bstack1111l1lll1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1111l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ྇"): [],
        bstack1111l1l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ྈ"): [],
        bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬྉ"): []
    }
    bstack1111lllll1_opy_ = []
    bstack111l111l11_opy_ = []
    @staticmethod
    def bstack111ll1llll_opy_(log):
        if not ((isinstance(log[bstack1111l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྊ")], list) or (isinstance(log[bstack1111l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྋ")], dict)) and len(log[bstack1111l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྌ")])>0) or (isinstance(log[bstack1111l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ྍ")], str) and log[bstack1111l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྎ")].strip())):
            return
        active = bstack1ll11lll1_opy_.bstack111ll1l1l1_opy_()
        log = {
            bstack1111l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ྏ"): log[bstack1111l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧྐ")],
            bstack1111l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬྑ"): bstack1111l1lll1_opy_().isoformat() + bstack1111l1l_opy_ (u"ࠪ࡞ࠬྒ"),
            bstack1111l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྒྷ"): log[bstack1111l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ྔ")],
        }
        if active:
            if active[bstack1111l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫྕ")] == bstack1111l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬྖ"):
                log[bstack1111l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨྗ")] = active[bstack1111l1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ྘")]
            elif active[bstack1111l1l_opy_ (u"ࠪࡸࡾࡶࡥࠨྙ")] == bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩྚ"):
                log[bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬྛ")] = active[bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ྜ")]
        bstack11l1lllll1_opy_.bstack11l11l1l1l_opy_([log])
    def __init__(self):
        self.messages = bstack1111llll1l_opy_()
        self._111l11l1ll_opy_ = None
        self._1111llll11_opy_ = None
        self._111l1l1l1l_opy_ = OrderedDict()
        self.bstack111lll11l1_opy_ = bstack111ll1ll1l_opy_(self.bstack111ll1llll_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l111ll1_opy_()
        if not self._111l1l1l1l_opy_.get(attrs.get(bstack1111l1l_opy_ (u"ࠧࡪࡦࠪྜྷ")), None):
            self._111l1l1l1l_opy_[attrs.get(bstack1111l1l_opy_ (u"ࠨ࡫ࡧࠫྞ"))] = {}
        bstack1111lll1ll_opy_ = bstack111l1lllll_opy_(
                bstack1111ll11ll_opy_=attrs.get(bstack1111l1l_opy_ (u"ࠩ࡬ࡨࠬྟ")),
                name=name,
                started_at=bstack1ll111ll1l_opy_(),
                file_path=os.path.relpath(attrs[bstack1111l1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪྠ")], start=os.getcwd()) if attrs.get(bstack1111l1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫྡ")) != bstack1111l1l_opy_ (u"ࠬ࠭ྡྷ") else bstack1111l1l_opy_ (u"࠭ࠧྣ"),
                framework=bstack1111l1l_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ྤ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1111l1l_opy_ (u"ࠨ࡫ࡧࠫྥ"), None)
        self._111l1l1l1l_opy_[attrs.get(bstack1111l1l_opy_ (u"ࠩ࡬ࡨࠬྦ"))][bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྦྷ")] = bstack1111lll1ll_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1111ll1lll_opy_()
        self._111l1111ll_opy_(messages)
        with self._lock:
            for bstack111l11111l_opy_ in self.bstack1111lllll1_opy_:
                bstack111l11111l_opy_[bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ྨ")][bstack1111l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫྩ")].extend(self.store[bstack1111l1l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬྪ")])
                bstack11l1lllll1_opy_.bstack111lll1l_opy_(bstack111l11111l_opy_)
            self.bstack1111lllll1_opy_ = []
            self.store[bstack1111l1l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ྫ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111lll11l1_opy_.start()
        if not self._111l1l1l1l_opy_.get(attrs.get(bstack1111l1l_opy_ (u"ࠨ࡫ࡧࠫྫྷ")), None):
            self._111l1l1l1l_opy_[attrs.get(bstack1111l1l_opy_ (u"ࠩ࡬ࡨࠬྭ"))] = {}
        driver = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩྮ"), None)
        bstack111ll1l1ll_opy_ = bstack111l1lllll_opy_(
            bstack1111ll11ll_opy_=attrs.get(bstack1111l1l_opy_ (u"ࠫ࡮ࡪࠧྯ")),
            name=name,
            started_at=bstack1ll111ll1l_opy_(),
            file_path=os.path.relpath(attrs[bstack1111l1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬྰ")], start=os.getcwd()),
            scope=RobotHandler.bstack1111lll111_opy_(attrs.get(bstack1111l1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ྱ"), None)),
            framework=bstack1111l1l_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ྲ"),
            tags=attrs[bstack1111l1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ླ")],
            hooks=self.store[bstack1111l1l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨྴ")],
            bstack111lll11ll_opy_=bstack11l1lllll1_opy_.bstack111ll11ll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1111l1l_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧྵ").format(bstack1111l1l_opy_ (u"ࠦࠥࠨྶ").join(attrs[bstack1111l1l_opy_ (u"ࠬࡺࡡࡨࡵࠪྷ")]), name) if attrs[bstack1111l1l_opy_ (u"࠭ࡴࡢࡩࡶࠫྸ")] else name
        )
        self._111l1l1l1l_opy_[attrs.get(bstack1111l1l_opy_ (u"ࠧࡪࡦࠪྐྵ"))][bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྺ")] = bstack111ll1l1ll_opy_
        threading.current_thread().current_test_uuid = bstack111ll1l1ll_opy_.bstack111l11ll11_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1111l1l_opy_ (u"ࠩ࡬ࡨࠬྻ"), None)
        self.bstack111ll11111_opy_(bstack1111l1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫྼ"), bstack111ll1l1ll_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111lll11l1_opy_.reset()
        bstack111l11llll_opy_ = bstack1111ll111l_opy_.get(attrs.get(bstack1111l1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ྽")), bstack1111l1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭྾"))
        self._111l1l1l1l_opy_[attrs.get(bstack1111l1l_opy_ (u"࠭ࡩࡥࠩ྿"))][bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ࿀")].stop(time=bstack1ll111ll1l_opy_(), duration=int(attrs.get(bstack1111l1l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭࿁"), bstack1111l1l_opy_ (u"ࠩ࠳ࠫ࿂"))), result=Result(result=bstack111l11llll_opy_, exception=attrs.get(bstack1111l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿃")), bstack111ll1111l_opy_=[attrs.get(bstack1111l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿄"))]))
        self.bstack111ll11111_opy_(bstack1111l1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ࿅"), self._111l1l1l1l_opy_[attrs.get(bstack1111l1l_opy_ (u"࠭ࡩࡥ࿆ࠩ"))][bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ࿇")], True)
        with self._lock:
            self.store[bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ࿈")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l111ll1_opy_()
        current_test_id = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ࿉"), None)
        bstack1111lll11l_opy_ = current_test_id if bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬ࿊"), None) else bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧ࿋"), None)
        if attrs.get(bstack1111l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿌"), bstack1111l1l_opy_ (u"࠭ࠧ࿍")).lower() in [bstack1111l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭࿎"), bstack1111l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ࿏")]:
            hook_type = bstack111l1l11l1_opy_(attrs.get(bstack1111l1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ࿐")), bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ࿑"), None))
            hook_name = bstack1111l1l_opy_ (u"ࠫࢀࢃࠧ࿒").format(attrs.get(bstack1111l1l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ࿓"), bstack1111l1l_opy_ (u"࠭ࠧ࿔")))
            if hook_type in [bstack1111l1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ࿕"), bstack1111l1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫ࿖")]:
                hook_name = bstack1111l1l_opy_ (u"ࠩ࡞ࡿࢂࡣࠠࡼࡿࠪ࿗").format(bstack111l1ll1ll_opy_.get(hook_type), attrs.get(bstack1111l1l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ࿘"), bstack1111l1l_opy_ (u"ࠫࠬ࿙")))
            bstack111l1l1lll_opy_ = bstack111lll1l11_opy_(
                bstack1111ll11ll_opy_=bstack1111lll11l_opy_ + bstack1111l1l_opy_ (u"ࠬ࠳ࠧ࿚") + attrs.get(bstack1111l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫ࿛"), bstack1111l1l_opy_ (u"ࠧࠨ࿜")).lower(),
                name=hook_name,
                started_at=bstack1ll111ll1l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1111l1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ࿝")), start=os.getcwd()),
                framework=bstack1111l1l_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ࿞"),
                tags=attrs[bstack1111l1l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ࿟")],
                scope=RobotHandler.bstack1111lll111_opy_(attrs.get(bstack1111l1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ࿠"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l1l1lll_opy_.bstack111l11ll11_opy_()
            threading.current_thread().current_hook_id = bstack1111lll11l_opy_ + bstack1111l1l_opy_ (u"ࠬ࠳ࠧ࿡") + attrs.get(bstack1111l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫ࿢"), bstack1111l1l_opy_ (u"ࠧࠨ࿣")).lower()
            with self._lock:
                self.store[bstack1111l1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ࿤")] = [bstack111l1l1lll_opy_.bstack111l11ll11_opy_()]
                if bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭࿥"), None):
                    self.store[bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ࿦")].append(bstack111l1l1lll_opy_.bstack111l11ll11_opy_())
                else:
                    self.store[bstack1111l1l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ࿧")].append(bstack111l1l1lll_opy_.bstack111l11ll11_opy_())
            if bstack1111lll11l_opy_:
                self._111l1l1l1l_opy_[bstack1111lll11l_opy_ + bstack1111l1l_opy_ (u"ࠬ࠳ࠧ࿨") + attrs.get(bstack1111l1l_opy_ (u"࠭ࡴࡺࡲࡨࠫ࿩"), bstack1111l1l_opy_ (u"ࠧࠨ࿪")).lower()] = { bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿫"): bstack111l1l1lll_opy_ }
            bstack11l1lllll1_opy_.bstack111ll11111_opy_(bstack1111l1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ࿬"), bstack111l1l1lll_opy_)
        else:
            bstack111ll11l11_opy_ = {
                bstack1111l1l_opy_ (u"ࠪ࡭ࡩ࠭࿭"): uuid4().__str__(),
                bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ࿮"): bstack1111l1l_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫ࿯").format(attrs.get(bstack1111l1l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭࿰")), attrs.get(bstack1111l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ࿱"), bstack1111l1l_opy_ (u"ࠨࠩ࿲"))) if attrs.get(bstack1111l1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ࿳"), []) else attrs.get(bstack1111l1l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ࿴")),
                bstack1111l1l_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫ࿵"): attrs.get(bstack1111l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪ࿶"), []),
                bstack1111l1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ࿷"): bstack1ll111ll1l_opy_(),
                bstack1111l1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ࿸"): bstack1111l1l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ࿹"),
                bstack1111l1l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ࿺"): attrs.get(bstack1111l1l_opy_ (u"ࠪࡨࡴࡩࠧ࿻"), bstack1111l1l_opy_ (u"ࠫࠬ࿼"))
            }
            if attrs.get(bstack1111l1l_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭࿽"), bstack1111l1l_opy_ (u"࠭ࠧ࿾")) != bstack1111l1l_opy_ (u"ࠧࠨ࿿"):
                bstack111ll11l11_opy_[bstack1111l1l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩက")] = attrs.get(bstack1111l1l_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪခ"))
            if not self.bstack111l111l11_opy_:
                self._111l1l1l1l_opy_[self._1111l1llll_opy_()][bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ဂ")].add_step(bstack111ll11l11_opy_)
                threading.current_thread().current_step_uuid = bstack111ll11l11_opy_[bstack1111l1l_opy_ (u"ࠫ࡮ࡪࠧဃ")]
            self.bstack111l111l11_opy_.append(bstack111ll11l11_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1111ll1lll_opy_()
        self._111l1111ll_opy_(messages)
        current_test_id = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧင"), None)
        bstack1111lll11l_opy_ = current_test_id if current_test_id else bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩစ"), None)
        bstack111l11ll1l_opy_ = bstack1111ll111l_opy_.get(attrs.get(bstack1111l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧဆ")), bstack1111l1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩဇ"))
        bstack111l1l1l11_opy_ = attrs.get(bstack1111l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဈ"))
        if bstack111l11ll1l_opy_ != bstack1111l1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫဉ") and not attrs.get(bstack1111l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬည")) and self._111l11l1ll_opy_:
            bstack111l1l1l11_opy_ = self._111l11l1ll_opy_
        bstack111ll1lll1_opy_ = Result(result=bstack111l11ll1l_opy_, exception=bstack111l1l1l11_opy_, bstack111ll1111l_opy_=[bstack111l1l1l11_opy_])
        if attrs.get(bstack1111l1l_opy_ (u"ࠬࡺࡹࡱࡧࠪဋ"), bstack1111l1l_opy_ (u"࠭ࠧဌ")).lower() in [bstack1111l1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ဍ"), bstack1111l1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪဎ")]:
            bstack1111lll11l_opy_ = current_test_id if current_test_id else bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬဏ"), None)
            if bstack1111lll11l_opy_:
                bstack111lll1111_opy_ = bstack1111lll11l_opy_ + bstack1111l1l_opy_ (u"ࠥ࠱ࠧတ") + attrs.get(bstack1111l1l_opy_ (u"ࠫࡹࡿࡰࡦࠩထ"), bstack1111l1l_opy_ (u"ࠬ࠭ဒ")).lower()
                self._111l1l1l1l_opy_[bstack111lll1111_opy_][bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩဓ")].stop(time=bstack1ll111ll1l_opy_(), duration=int(attrs.get(bstack1111l1l_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬန"), bstack1111l1l_opy_ (u"ࠨ࠲ࠪပ"))), result=bstack111ll1lll1_opy_)
                bstack11l1lllll1_opy_.bstack111ll11111_opy_(bstack1111l1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫဖ"), self._111l1l1l1l_opy_[bstack111lll1111_opy_][bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ဗ")])
        else:
            bstack1111lll11l_opy_ = current_test_id if current_test_id else bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢ࡭ࡩ࠭ဘ"), None)
            if bstack1111lll11l_opy_ and len(self.bstack111l111l11_opy_) == 1:
                current_step_uuid = bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩမ"), None)
                self._111l1l1l1l_opy_[bstack1111lll11l_opy_][bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩယ")].bstack111ll1l11l_opy_(current_step_uuid, duration=int(attrs.get(bstack1111l1l_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬရ"), bstack1111l1l_opy_ (u"ࠨ࠲ࠪလ"))), result=bstack111ll1lll1_opy_)
            else:
                self.bstack111l1111l1_opy_(attrs)
            self.bstack111l111l11_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1111l1l_opy_ (u"ࠩ࡫ࡸࡲࡲࠧဝ"), bstack1111l1l_opy_ (u"ࠪࡲࡴ࠭သ")) == bstack1111l1l_opy_ (u"ࠫࡾ࡫ࡳࠨဟ"):
                return
            self.messages.push(message)
            logs = []
            if bstack1ll11lll1_opy_.bstack111ll1l1l1_opy_():
                logs.append({
                    bstack1111l1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨဠ"): bstack1ll111ll1l_opy_(),
                    bstack1111l1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧအ"): message.get(bstack1111l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨဢ")),
                    bstack1111l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧဣ"): message.get(bstack1111l1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨဤ")),
                    **bstack1ll11lll1_opy_.bstack111ll1l1l1_opy_()
                })
                if len(logs) > 0:
                    bstack11l1lllll1_opy_.bstack11l11l1l1l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack11l1lllll1_opy_.bstack111l1l11ll_opy_()
    def bstack111l1111l1_opy_(self, bstack111l111lll_opy_):
        if not bstack1ll11lll1_opy_.bstack111ll1l1l1_opy_():
            return
        kwname = bstack1111l1l_opy_ (u"ࠪࡿࢂࠦࡻࡾࠩဥ").format(bstack111l111lll_opy_.get(bstack1111l1l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫဦ")), bstack111l111lll_opy_.get(bstack1111l1l_opy_ (u"ࠬࡧࡲࡨࡵࠪဧ"), bstack1111l1l_opy_ (u"࠭ࠧဨ"))) if bstack111l111lll_opy_.get(bstack1111l1l_opy_ (u"ࠧࡢࡴࡪࡷࠬဩ"), []) else bstack111l111lll_opy_.get(bstack1111l1l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨဪ"))
        error_message = bstack1111l1l_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠡࡾࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠ࡝ࠤࡾ࠶ࢂࡢࠢࠣါ").format(kwname, bstack111l111lll_opy_.get(bstack1111l1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪာ")), str(bstack111l111lll_opy_.get(bstack1111l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬိ"))))
        bstack111l11lll1_opy_ = bstack1111l1l_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠦီ").format(kwname, bstack111l111lll_opy_.get(bstack1111l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ု")))
        bstack111l111111_opy_ = error_message if bstack111l111lll_opy_.get(bstack1111l1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨူ")) else bstack111l11lll1_opy_
        bstack1111llllll_opy_ = {
            bstack1111l1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫေ"): self.bstack111l111l11_opy_[-1].get(bstack1111l1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ဲ"), bstack1ll111ll1l_opy_()),
            bstack1111l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫဳ"): bstack111l111111_opy_,
            bstack1111l1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪဴ"): bstack1111l1l_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫဵ") if bstack111l111lll_opy_.get(bstack1111l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ံ")) == bstack1111l1l_opy_ (u"ࠧࡇࡃࡌࡐ့ࠬ") else bstack1111l1l_opy_ (u"ࠨࡋࡑࡊࡔ࠭း"),
            **bstack1ll11lll1_opy_.bstack111ll1l1l1_opy_()
        }
        bstack11l1lllll1_opy_.bstack11l11l1l1l_opy_([bstack1111llllll_opy_])
    def _1111l1llll_opy_(self):
        for bstack1111ll11ll_opy_ in reversed(self._111l1l1l1l_opy_):
            bstack1111ll11l1_opy_ = bstack1111ll11ll_opy_
            data = self._111l1l1l1l_opy_[bstack1111ll11ll_opy_][bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥ္ࠬ")]
            if isinstance(data, bstack111lll1l11_opy_):
                if not bstack1111l1l_opy_ (u"ࠪࡉࡆࡉࡈࠨ်") in data.bstack111l1ll1l1_opy_():
                    return bstack1111ll11l1_opy_
            else:
                return bstack1111ll11l1_opy_
    def _111l1111ll_opy_(self, messages):
        try:
            bstack1111l1ll1l_opy_ = BuiltIn().get_variable_value(bstack1111l1l_opy_ (u"ࠦࠩࢁࡌࡐࡉࠣࡐࡊ࡜ࡅࡍࡿࠥျ")) in (bstack111l11l111_opy_.DEBUG, bstack111l11l111_opy_.TRACE)
            for message, bstack111l11l1l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1111l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ြ"))
                level = message.get(bstack1111l1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬွ"))
                if level == bstack111l11l111_opy_.FAIL:
                    self._111l11l1ll_opy_ = name or self._111l11l1ll_opy_
                    self._1111llll11_opy_ = bstack111l11l1l1_opy_.get(bstack1111l1l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣှ")) if bstack1111l1ll1l_opy_ and bstack111l11l1l1_opy_ else self._1111llll11_opy_
        except:
            pass
    @classmethod
    def bstack111ll11111_opy_(self, event: str, bstack111l1l111l_opy_: bstack111l111l1l_opy_, bstack111l1ll11l_opy_=False):
        if event == bstack1111l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪဿ"):
            bstack111l1l111l_opy_.set(hooks=self.store[bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭၀")])
        if event == bstack1111l1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ၁"):
            event = bstack1111l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭၂")
        if bstack111l1ll11l_opy_:
            bstack111l1ll111_opy_ = {
                bstack1111l1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ၃"): event,
                bstack111l1l111l_opy_.bstack1111ll1111_opy_(): bstack111l1l111l_opy_.bstack1111lll1l1_opy_(event)
            }
            with self._lock:
                self.bstack1111lllll1_opy_.append(bstack111l1ll111_opy_)
        else:
            bstack11l1lllll1_opy_.bstack111ll11111_opy_(event, bstack111l1l111l_opy_)
class bstack1111llll1l_opy_:
    def __init__(self):
        self._1111ll1l1l_opy_ = []
    def bstack111l111ll1_opy_(self):
        self._1111ll1l1l_opy_.append([])
    def bstack1111ll1lll_opy_(self):
        return self._1111ll1l1l_opy_.pop() if self._1111ll1l1l_opy_ else list()
    def push(self, message):
        self._1111ll1l1l_opy_[-1].append(message) if self._1111ll1l1l_opy_ else self._1111ll1l1l_opy_.append([message])
class bstack111l11l111_opy_:
    FAIL = bstack1111l1l_opy_ (u"࠭ࡆࡂࡋࡏࠫ၄")
    ERROR = bstack1111l1l_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭၅")
    WARNING = bstack1111l1l_opy_ (u"ࠨ࡙ࡄࡖࡓ࠭၆")
    bstack111l1l1ll1_opy_ = bstack1111l1l_opy_ (u"ࠩࡌࡒࡋࡕࠧ၇")
    DEBUG = bstack1111l1l_opy_ (u"ࠪࡈࡊࡈࡕࡈࠩ၈")
    TRACE = bstack1111l1l_opy_ (u"࡙ࠫࡘࡁࡄࡇࠪ၉")
    bstack1111ll1l11_opy_ = [FAIL, ERROR]
def bstack1111ll1ll1_opy_(bstack111l1l1111_opy_):
    if not bstack111l1l1111_opy_:
        return None
    if bstack111l1l1111_opy_.get(bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ၊"), None):
        return getattr(bstack111l1l1111_opy_[bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ။")], bstack1111l1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ၌"), None)
    return bstack111l1l1111_opy_.get(bstack1111l1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭၍"), None)
def bstack111l1l11l1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1111l1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ၎"), bstack1111l1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ၏")]:
        return
    if hook_type.lower() == bstack1111l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪၐ"):
        if current_test_uuid is None:
            return bstack1111l1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩၑ")
        else:
            return bstack1111l1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫၒ")
    elif hook_type.lower() == bstack1111l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩၓ"):
        if current_test_uuid is None:
            return bstack1111l1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫၔ")
        else:
            return bstack1111l1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ၕ")