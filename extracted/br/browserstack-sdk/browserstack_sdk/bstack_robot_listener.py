# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1111ll1l1l_opy_ import RobotHandler
from bstack_utils.capture import bstack111lll1111_opy_
from bstack_utils.bstack111ll1llll_opy_ import bstack1111llllll_opy_, bstack111ll11lll_opy_, bstack111ll1ll1l_opy_
from bstack_utils.bstack111ll1l11l_opy_ import bstack11llllll1_opy_
from bstack_utils.bstack111lll1l11_opy_ import bstack11lll111ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l1llllll_opy_, bstack1l111ll1_opy_, Result, \
    error_handler, bstack111l11111l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1ll1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩོ࠭"): [],
        bstack1ll1ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴཽࠩ"): [],
        bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨཾ"): []
    }
    bstack1111lll11l_opy_ = []
    bstack1111lll1l1_opy_ = []
    @staticmethod
    def bstack111lll1lll_opy_(log):
        if not ((isinstance(log[bstack1ll1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཿ")], list) or (isinstance(log[bstack1ll1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ྀࠧ")], dict)) and len(log[bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཱྀ")])>0) or (isinstance(log[bstack1ll1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྂ")], str) and log[bstack1ll1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྃ")].strip())):
            return
        active = bstack11llllll1_opy_.bstack111lll11l1_opy_()
        log = {
            bstack1ll1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭྄ࠩ"): log[bstack1ll1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ྅")],
            bstack1ll1ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ྆"): bstack111l11111l_opy_().isoformat() + bstack1ll1ll_opy_ (u"࡚࠭ࠨ྇"),
            bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྈ"): log[bstack1ll1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྉ")],
        }
        if active:
            if active[bstack1ll1ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧྊ")] == bstack1ll1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨྋ"):
                log[bstack1ll1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫྌ")] = active[bstack1ll1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬྍ")]
            elif active[bstack1ll1ll_opy_ (u"࠭ࡴࡺࡲࡨࠫྎ")] == bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࠬྏ"):
                log[bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨྐ")] = active[bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩྑ")]
        bstack11lll111ll_opy_.bstack1l11l11l_opy_([log])
    def __init__(self):
        self.messages = bstack111l11ll11_opy_()
        self._111l111l1l_opy_ = None
        self._111l11lll1_opy_ = None
        self._111l1lllll_opy_ = OrderedDict()
        self.bstack111lll1l1l_opy_ = bstack111lll1111_opy_(self.bstack111lll1lll_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1l1lll_opy_()
        if not self._111l1lllll_opy_.get(attrs.get(bstack1ll1ll_opy_ (u"ࠪ࡭ࡩ࠭ྒ")), None):
            self._111l1lllll_opy_[attrs.get(bstack1ll1ll_opy_ (u"ࠫ࡮ࡪࠧྒྷ"))] = {}
        bstack111l1l11l1_opy_ = bstack111ll1ll1l_opy_(
                bstack111l1111l1_opy_=attrs.get(bstack1ll1ll_opy_ (u"ࠬ࡯ࡤࠨྔ")),
                name=name,
                started_at=bstack1l111ll1_opy_(),
                file_path=os.path.relpath(attrs[bstack1ll1ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ྕ")], start=os.getcwd()) if attrs.get(bstack1ll1ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧྖ")) != bstack1ll1ll_opy_ (u"ࠨࠩྗ") else bstack1ll1ll_opy_ (u"ࠩࠪ྘"),
                framework=bstack1ll1ll_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩྙ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll1ll_opy_ (u"ࠫ࡮ࡪࠧྚ"), None)
        self._111l1lllll_opy_[attrs.get(bstack1ll1ll_opy_ (u"ࠬ࡯ࡤࠨྛ"))][bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩྜ")] = bstack111l1l11l1_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111ll111l1_opy_()
        self._1111lll111_opy_(messages)
        with self._lock:
            for bstack111l111ll1_opy_ in self.bstack1111lll11l_opy_:
                bstack111l111ll1_opy_[bstack1ll1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩྜྷ")][bstack1ll1ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧྞ")].extend(self.store[bstack1ll1ll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨྟ")])
                bstack11lll111ll_opy_.bstack1lll11ll1l_opy_(bstack111l111ll1_opy_)
            self.bstack1111lll11l_opy_ = []
            self.store[bstack1ll1ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩྠ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111lll1l1l_opy_.start()
        if not self._111l1lllll_opy_.get(attrs.get(bstack1ll1ll_opy_ (u"ࠫ࡮ࡪࠧྡ")), None):
            self._111l1lllll_opy_[attrs.get(bstack1ll1ll_opy_ (u"ࠬ࡯ࡤࠨྡྷ"))] = {}
        driver = bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬྣ"), None)
        bstack111ll1llll_opy_ = bstack111ll1ll1l_opy_(
            bstack111l1111l1_opy_=attrs.get(bstack1ll1ll_opy_ (u"ࠧࡪࡦࠪྤ")),
            name=name,
            started_at=bstack1l111ll1_opy_(),
            file_path=os.path.relpath(attrs[bstack1ll1ll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨྥ")], start=os.getcwd()),
            scope=RobotHandler.bstack111l1ll1ll_opy_(attrs.get(bstack1ll1ll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩྦ"), None)),
            framework=bstack1ll1ll_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩྦྷ"),
            tags=attrs[bstack1ll1ll_opy_ (u"ࠫࡹࡧࡧࡴࠩྨ")],
            hooks=self.store[bstack1ll1ll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫྩ")],
            bstack111ll111ll_opy_=bstack11lll111ll_opy_.bstack111llll1ll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll1ll_opy_ (u"ࠨࡻࡾࠢ࡟ࡲࠥࢁࡽࠣྪ").format(bstack1ll1ll_opy_ (u"ࠢࠡࠤྫ").join(attrs[bstack1ll1ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ྫྷ")]), name) if attrs[bstack1ll1ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧྭ")] else name
        )
        self._111l1lllll_opy_[attrs.get(bstack1ll1ll_opy_ (u"ࠪ࡭ࡩ࠭ྮ"))][bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧྯ")] = bstack111ll1llll_opy_
        threading.current_thread().current_test_uuid = bstack111ll1llll_opy_.bstack111l111111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll1ll_opy_ (u"ࠬ࡯ࡤࠨྰ"), None)
        self.bstack111ll11ll1_opy_(bstack1ll1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧྱ"), bstack111ll1llll_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111lll1l1l_opy_.reset()
        bstack111l11l111_opy_ = bstack111l1l1ll1_opy_.get(attrs.get(bstack1ll1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧྲ")), bstack1ll1ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩླ"))
        self._111l1lllll_opy_[attrs.get(bstack1ll1ll_opy_ (u"ࠩ࡬ࡨࠬྴ"))][bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྵ")].stop(time=bstack1l111ll1_opy_(), duration=int(attrs.get(bstack1ll1ll_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩྶ"), bstack1ll1ll_opy_ (u"ࠬ࠶ࠧྷ"))), result=Result(result=bstack111l11l111_opy_, exception=attrs.get(bstack1ll1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྸ")), bstack111lll11ll_opy_=[attrs.get(bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྐྵ"))]))
        self.bstack111ll11ll1_opy_(bstack1ll1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪྺ"), self._111l1lllll_opy_[attrs.get(bstack1ll1ll_opy_ (u"ࠩ࡬ࡨࠬྻ"))][bstack1ll1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྼ")], True)
        with self._lock:
            self.store[bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ྽")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1l1lll_opy_()
        current_test_id = bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ྾"), None)
        bstack111l1ll11l_opy_ = current_test_id if bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨ྿"), None) else bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪ࿀"), None)
        if attrs.get(bstack1ll1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭࿁"), bstack1ll1ll_opy_ (u"ࠩࠪ࿂")).lower() in [bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ࿃"), bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭࿄")]:
            hook_type = bstack1111ll1l11_opy_(attrs.get(bstack1ll1ll_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿅")), bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦ࿆ࠪ"), None))
            hook_name = bstack1ll1ll_opy_ (u"ࠧࡼࡿࠪ࿇").format(attrs.get(bstack1ll1ll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ࿈"), bstack1ll1ll_opy_ (u"ࠩࠪ࿉")))
            if hook_type in [bstack1ll1ll_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ࿊"), bstack1ll1ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ࿋")]:
                hook_name = bstack1ll1ll_opy_ (u"ࠬࡡࡻࡾ࡟ࠣࡿࢂ࠭࿌").format(bstack1111lllll1_opy_.get(hook_type), attrs.get(bstack1ll1ll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭࿍"), bstack1ll1ll_opy_ (u"ࠧࠨ࿎")))
            bstack111ll11111_opy_ = bstack111ll11lll_opy_(
                bstack111l1111l1_opy_=bstack111l1ll11l_opy_ + bstack1ll1ll_opy_ (u"ࠨ࠯ࠪ࿏") + attrs.get(bstack1ll1ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ࿐"), bstack1ll1ll_opy_ (u"ࠪࠫ࿑")).lower(),
                name=hook_name,
                started_at=bstack1l111ll1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1ll1ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ࿒")), start=os.getcwd()),
                framework=bstack1ll1ll_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫ࿓"),
                tags=attrs[bstack1ll1ll_opy_ (u"࠭ࡴࡢࡩࡶࠫ࿔")],
                scope=RobotHandler.bstack111l1ll1ll_opy_(attrs.get(bstack1ll1ll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ࿕"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111ll11111_opy_.bstack111l111111_opy_()
            threading.current_thread().current_hook_id = bstack111l1ll11l_opy_ + bstack1ll1ll_opy_ (u"ࠨ࠯ࠪ࿖") + attrs.get(bstack1ll1ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ࿗"), bstack1ll1ll_opy_ (u"ࠪࠫ࿘")).lower()
            with self._lock:
                self.store[bstack1ll1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ࿙")] = [bstack111ll11111_opy_.bstack111l111111_opy_()]
                if bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ࿚"), None):
                    self.store[bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ࿛")].append(bstack111ll11111_opy_.bstack111l111111_opy_())
                else:
                    self.store[bstack1ll1ll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭࿜")].append(bstack111ll11111_opy_.bstack111l111111_opy_())
            if bstack111l1ll11l_opy_:
                self._111l1lllll_opy_[bstack111l1ll11l_opy_ + bstack1ll1ll_opy_ (u"ࠨ࠯ࠪ࿝") + attrs.get(bstack1ll1ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ࿞"), bstack1ll1ll_opy_ (u"ࠪࠫ࿟")).lower()] = { bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࿠"): bstack111ll11111_opy_ }
            bstack11lll111ll_opy_.bstack111ll11ll1_opy_(bstack1ll1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭࿡"), bstack111ll11111_opy_)
        else:
            bstack111llll111_opy_ = {
                bstack1ll1ll_opy_ (u"࠭ࡩࡥࠩ࿢"): uuid4().__str__(),
                bstack1ll1ll_opy_ (u"ࠧࡵࡧࡻࡸࠬ࿣"): bstack1ll1ll_opy_ (u"ࠨࡽࢀࠤࢀࢃࠧ࿤").format(attrs.get(bstack1ll1ll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ࿥")), attrs.get(bstack1ll1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ࿦"), bstack1ll1ll_opy_ (u"ࠫࠬ࿧"))) if attrs.get(bstack1ll1ll_opy_ (u"ࠬࡧࡲࡨࡵࠪ࿨"), []) else attrs.get(bstack1ll1ll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭࿩")),
                bstack1ll1ll_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧ࿪"): attrs.get(bstack1ll1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭࿫"), []),
                bstack1ll1ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭࿬"): bstack1l111ll1_opy_(),
                bstack1ll1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ࿭"): bstack1ll1ll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ࿮"),
                bstack1ll1ll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ࿯"): attrs.get(bstack1ll1ll_opy_ (u"࠭ࡤࡰࡥࠪ࿰"), bstack1ll1ll_opy_ (u"ࠧࠨ࿱"))
            }
            if attrs.get(bstack1ll1ll_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩ࿲"), bstack1ll1ll_opy_ (u"ࠩࠪ࿳")) != bstack1ll1ll_opy_ (u"ࠪࠫ࿴"):
                bstack111llll111_opy_[bstack1ll1ll_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬ࿵")] = attrs.get(bstack1ll1ll_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭࿶"))
            if not self.bstack1111lll1l1_opy_:
                self._111l1lllll_opy_[self._1111llll1l_opy_()][bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿷")].add_step(bstack111llll111_opy_)
                threading.current_thread().current_step_uuid = bstack111llll111_opy_[bstack1ll1ll_opy_ (u"ࠧࡪࡦࠪ࿸")]
            self.bstack1111lll1l1_opy_.append(bstack111llll111_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111ll111l1_opy_()
        self._1111lll111_opy_(messages)
        current_test_id = bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪ࿹"), None)
        bstack111l1ll11l_opy_ = current_test_id if current_test_id else bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬ࿺"), None)
        bstack111l1l11ll_opy_ = bstack111l1l1ll1_opy_.get(attrs.get(bstack1ll1ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ࿻")), bstack1ll1ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ࿼"))
        bstack111l1llll1_opy_ = attrs.get(bstack1ll1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿽"))
        if bstack111l1l11ll_opy_ != bstack1ll1ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ࿾") and not attrs.get(bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿿")) and self._111l111l1l_opy_:
            bstack111l1llll1_opy_ = self._111l111l1l_opy_
        bstack111ll1l1l1_opy_ = Result(result=bstack111l1l11ll_opy_, exception=bstack111l1llll1_opy_, bstack111lll11ll_opy_=[bstack111l1llll1_opy_])
        if attrs.get(bstack1ll1ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭က"), bstack1ll1ll_opy_ (u"ࠩࠪခ")).lower() in [bstack1ll1ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩဂ"), bstack1ll1ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ဃ")]:
            bstack111l1ll11l_opy_ = current_test_id if current_test_id else bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨင"), None)
            if bstack111l1ll11l_opy_:
                bstack111ll1l111_opy_ = bstack111l1ll11l_opy_ + bstack1ll1ll_opy_ (u"ࠨ࠭ࠣစ") + attrs.get(bstack1ll1ll_opy_ (u"ࠧࡵࡻࡳࡩࠬဆ"), bstack1ll1ll_opy_ (u"ࠨࠩဇ")).lower()
                self._111l1lllll_opy_[bstack111ll1l111_opy_][bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬဈ")].stop(time=bstack1l111ll1_opy_(), duration=int(attrs.get(bstack1ll1ll_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨဉ"), bstack1ll1ll_opy_ (u"ࠫ࠵࠭ည"))), result=bstack111ll1l1l1_opy_)
                bstack11lll111ll_opy_.bstack111ll11ll1_opy_(bstack1ll1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧဋ"), self._111l1lllll_opy_[bstack111ll1l111_opy_][bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩဌ")])
        else:
            bstack111l1ll11l_opy_ = current_test_id if current_test_id else bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡩࡥࠩဍ"), None)
            if bstack111l1ll11l_opy_ and len(self.bstack1111lll1l1_opy_) == 1:
                current_step_uuid = bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡸࡪࡶ࡟ࡶࡷ࡬ࡨࠬဎ"), None)
                self._111l1lllll_opy_[bstack111l1ll11l_opy_][bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬဏ")].bstack111ll1l1ll_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll1ll_opy_ (u"ࠪࡩࡱࡧࡰࡴࡧࡧࡸ࡮ࡳࡥࠨတ"), bstack1ll1ll_opy_ (u"ࠫ࠵࠭ထ"))), result=bstack111ll1l1l1_opy_)
            else:
                self.bstack111l1111ll_opy_(attrs)
            self.bstack1111lll1l1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll1ll_opy_ (u"ࠬ࡮ࡴ࡮࡮ࠪဒ"), bstack1ll1ll_opy_ (u"࠭࡮ࡰࠩဓ")) == bstack1ll1ll_opy_ (u"ࠧࡺࡧࡶࠫန"):
                return
            self.messages.push(message)
            logs = []
            if bstack11llllll1_opy_.bstack111lll11l1_opy_():
                logs.append({
                    bstack1ll1ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫပ"): bstack1l111ll1_opy_(),
                    bstack1ll1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဖ"): message.get(bstack1ll1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫဗ")),
                    bstack1ll1ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪဘ"): message.get(bstack1ll1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫမ")),
                    **bstack11llllll1_opy_.bstack111lll11l1_opy_()
                })
                if len(logs) > 0:
                    bstack11lll111ll_opy_.bstack1l11l11l_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack11lll111ll_opy_.bstack1111ll1ll1_opy_()
    def bstack111l1111ll_opy_(self, bstack111l111lll_opy_):
        if not bstack11llllll1_opy_.bstack111lll11l1_opy_():
            return
        kwname = bstack1ll1ll_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬယ").format(bstack111l111lll_opy_.get(bstack1ll1ll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧရ")), bstack111l111lll_opy_.get(bstack1ll1ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭လ"), bstack1ll1ll_opy_ (u"ࠩࠪဝ"))) if bstack111l111lll_opy_.get(bstack1ll1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨသ"), []) else bstack111l111lll_opy_.get(bstack1ll1ll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫဟ"))
        error_message = bstack1ll1ll_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠤࢁࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡠࠧࢁ࠲ࡾ࡞ࠥࠦဠ").format(kwname, bstack111l111lll_opy_.get(bstack1ll1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭အ")), str(bstack111l111lll_opy_.get(bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨဢ"))))
        bstack111l11l11l_opy_ = bstack1ll1ll_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠢဣ").format(kwname, bstack111l111lll_opy_.get(bstack1ll1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩဤ")))
        bstack111l11ll1l_opy_ = error_message if bstack111l111lll_opy_.get(bstack1ll1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫဥ")) else bstack111l11l11l_opy_
        bstack111l1lll11_opy_ = {
            bstack1ll1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧဦ"): self.bstack1111lll1l1_opy_[-1].get(bstack1ll1ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩဧ"), bstack1l111ll1_opy_()),
            bstack1ll1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧဨ"): bstack111l11ll1l_opy_,
            bstack1ll1ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ဩ"): bstack1ll1ll_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧဪ") if bstack111l111lll_opy_.get(bstack1ll1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩါ")) == bstack1ll1ll_opy_ (u"ࠪࡊࡆࡏࡌࠨာ") else bstack1ll1ll_opy_ (u"ࠫࡎࡔࡆࡐࠩိ"),
            **bstack11llllll1_opy_.bstack111lll11l1_opy_()
        }
        bstack11lll111ll_opy_.bstack1l11l11l_opy_([bstack111l1lll11_opy_])
    def _1111llll1l_opy_(self):
        for bstack111l1111l1_opy_ in reversed(self._111l1lllll_opy_):
            bstack1111lll1ll_opy_ = bstack111l1111l1_opy_
            data = self._111l1lllll_opy_[bstack111l1111l1_opy_][bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨီ")]
            if isinstance(data, bstack111ll11lll_opy_):
                if not bstack1ll1ll_opy_ (u"࠭ࡅࡂࡅࡋࠫု") in data.bstack111l1l1111_opy_():
                    return bstack1111lll1ll_opy_
            else:
                return bstack1111lll1ll_opy_
    def _1111lll111_opy_(self, messages):
        try:
            bstack111l1l111l_opy_ = BuiltIn().get_variable_value(bstack1ll1ll_opy_ (u"ࠢࠥࡽࡏࡓࡌࠦࡌࡆࡘࡈࡐࢂࠨူ")) in (bstack111l1ll111_opy_.DEBUG, bstack111l1ll111_opy_.TRACE)
            for message, bstack1111llll11_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩေ"))
                level = message.get(bstack1ll1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨဲ"))
                if level == bstack111l1ll111_opy_.FAIL:
                    self._111l111l1l_opy_ = name or self._111l111l1l_opy_
                    self._111l11lll1_opy_ = bstack1111llll11_opy_.get(bstack1ll1ll_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦဳ")) if bstack111l1l111l_opy_ and bstack1111llll11_opy_ else self._111l11lll1_opy_
        except:
            pass
    @classmethod
    def bstack111ll11ll1_opy_(self, event: str, bstack111l1lll1l_opy_: bstack1111llllll_opy_, bstack111ll1111l_opy_=False):
        if event == bstack1ll1ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ဴ"):
            bstack111l1lll1l_opy_.set(hooks=self.store[bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩဵ")])
        if event == bstack1ll1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧံ"):
            event = bstack1ll1ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥ့ࠩ")
        if bstack111ll1111l_opy_:
            bstack111l1ll1l1_opy_ = {
                bstack1ll1ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬး"): event,
                bstack111l1lll1l_opy_.bstack111l11llll_opy_(): bstack111l1lll1l_opy_.bstack1111ll1lll_opy_(event)
            }
            with self._lock:
                self.bstack1111lll11l_opy_.append(bstack111l1ll1l1_opy_)
        else:
            bstack11lll111ll_opy_.bstack111ll11ll1_opy_(event, bstack111l1lll1l_opy_)
class bstack111l11ll11_opy_:
    def __init__(self):
        self._111l11l1l1_opy_ = []
    def bstack111l1l1lll_opy_(self):
        self._111l11l1l1_opy_.append([])
    def bstack111ll111l1_opy_(self):
        return self._111l11l1l1_opy_.pop() if self._111l11l1l1_opy_ else list()
    def push(self, message):
        self._111l11l1l1_opy_[-1].append(message) if self._111l11l1l1_opy_ else self._111l11l1l1_opy_.append([message])
class bstack111l1ll111_opy_:
    FAIL = bstack1ll1ll_opy_ (u"ࠩࡉࡅࡎࡒ္ࠧ")
    ERROR = bstack1ll1ll_opy_ (u"ࠪࡉࡗࡘࡏࡓ်ࠩ")
    WARNING = bstack1ll1ll_opy_ (u"ࠫ࡜ࡇࡒࡏࠩျ")
    bstack111l11l1ll_opy_ = bstack1ll1ll_opy_ (u"ࠬࡏࡎࡇࡑࠪြ")
    DEBUG = bstack1ll1ll_opy_ (u"࠭ࡄࡆࡄࡘࡋࠬွ")
    TRACE = bstack1ll1ll_opy_ (u"ࠧࡕࡔࡄࡇࡊ࠭ှ")
    bstack111l1l1l11_opy_ = [FAIL, ERROR]
def bstack111l111l11_opy_(bstack111l1l1l1l_opy_):
    if not bstack111l1l1l1l_opy_:
        return None
    if bstack111l1l1l1l_opy_.get(bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫဿ"), None):
        return getattr(bstack111l1l1l1l_opy_[bstack1ll1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ၀")], bstack1ll1ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ၁"), None)
    return bstack111l1l1l1l_opy_.get(bstack1ll1ll_opy_ (u"ࠫࡺࡻࡩࡥࠩ၂"), None)
def bstack1111ll1l11_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll1ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ၃"), bstack1ll1ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ၄")]:
        return
    if hook_type.lower() == bstack1ll1ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭၅"):
        if current_test_uuid is None:
            return bstack1ll1ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ၆")
        else:
            return bstack1ll1ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ၇")
    elif hook_type.lower() == bstack1ll1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬ၈"):
        if current_test_uuid is None:
            return bstack1ll1ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧ၉")
        else:
            return bstack1ll1ll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩ၊")