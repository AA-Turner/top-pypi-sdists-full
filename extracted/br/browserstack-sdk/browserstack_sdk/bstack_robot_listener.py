# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111l111ll1_opy_ import RobotHandler
from bstack_utils.capture import bstack111ll1lll1_opy_
from bstack_utils.bstack111lll1ll1_opy_ import bstack111l111lll_opy_, bstack111lll11ll_opy_, bstack111ll11ll1_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack11l1ll11_opy_
from bstack_utils.bstack111lllll1l_opy_ import bstack1l1l1l1ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack111ll1lll_opy_, bstack1l11l11ll_opy_, Result, \
    bstack111l1lll11_opy_, bstack1111llll11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪཁ"): [],
        bstack11ll11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ག"): [],
        bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬགྷ"): []
    }
    bstack111l111l1l_opy_ = []
    bstack111l1l1l1l_opy_ = []
    @staticmethod
    def bstack111ll1l1l1_opy_(log):
        if not ((isinstance(log[bstack11ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪང")], list) or (isinstance(log[bstack11ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫཅ")], dict)) and len(log[bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཆ")])>0) or (isinstance(log[bstack11ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཇ")], str) and log[bstack11ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ཈")].strip())):
            return
        active = bstack11l1ll11_opy_.bstack111llll1l1_opy_()
        log = {
            bstack11ll11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ཉ"): log[bstack11ll11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧཊ")],
            bstack11ll11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬཋ"): bstack1111llll11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠪ࡞ࠬཌ"),
            bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཌྷ"): log[bstack11ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཎ")],
        }
        if active:
            if active[bstack11ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫཏ")] == bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬཐ"):
                log[bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨད")] = active[bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩདྷ")]
            elif active[bstack11ll11_opy_ (u"ࠪࡸࡾࡶࡥࠨན")] == bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩཔ"):
                log[bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬཕ")] = active[bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭བ")]
        bstack1l1l1l1ll_opy_.bstack11ll1lllll_opy_([log])
    def __init__(self):
        self.messages = bstack1111llllll_opy_()
        self._111l111l11_opy_ = None
        self._111l1l1111_opy_ = None
        self._1111lll111_opy_ = OrderedDict()
        self.bstack111ll1llll_opy_ = bstack111ll1lll1_opy_(self.bstack111ll1l1l1_opy_)
    @bstack111l1lll11_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111ll111l1_opy_()
        if not self._1111lll111_opy_.get(attrs.get(bstack11ll11_opy_ (u"ࠧࡪࡦࠪབྷ")), None):
            self._1111lll111_opy_[attrs.get(bstack11ll11_opy_ (u"ࠨ࡫ࡧࠫམ"))] = {}
        bstack1111ll1l1l_opy_ = bstack111ll11ll1_opy_(
                bstack111l11l1ll_opy_=attrs.get(bstack11ll11_opy_ (u"ࠩ࡬ࡨࠬཙ")),
                name=name,
                started_at=bstack1l11l11ll_opy_(),
                file_path=os.path.relpath(attrs[bstack11ll11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪཚ")], start=os.getcwd()) if attrs.get(bstack11ll11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫཛ")) != bstack11ll11_opy_ (u"ࠬ࠭ཛྷ") else bstack11ll11_opy_ (u"࠭ࠧཝ"),
                framework=bstack11ll11_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ཞ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11ll11_opy_ (u"ࠨ࡫ࡧࠫཟ"), None)
        self._1111lll111_opy_[attrs.get(bstack11ll11_opy_ (u"ࠩ࡬ࡨࠬའ"))][bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ཡ")] = bstack1111ll1l1l_opy_
    @bstack111l1lll11_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1111lll1l1_opy_()
        self._111ll11l11_opy_(messages)
        for bstack111ll11111_opy_ in self.bstack111l111l1l_opy_:
            bstack111ll11111_opy_[bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ར")][bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫལ")].extend(self.store[bstack11ll11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬཤ")])
            bstack1l1l1l1ll_opy_.bstack1l1l11lll1_opy_(bstack111ll11111_opy_)
        self.bstack111l111l1l_opy_ = []
        self.store[bstack11ll11_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ཥ")] = []
    @bstack111l1lll11_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111ll1llll_opy_.start()
        if not self._1111lll111_opy_.get(attrs.get(bstack11ll11_opy_ (u"ࠨ࡫ࡧࠫས")), None):
            self._1111lll111_opy_[attrs.get(bstack11ll11_opy_ (u"ࠩ࡬ࡨࠬཧ"))] = {}
        driver = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩཨ"), None)
        bstack111lll1ll1_opy_ = bstack111ll11ll1_opy_(
            bstack111l11l1ll_opy_=attrs.get(bstack11ll11_opy_ (u"ࠫ࡮ࡪࠧཀྵ")),
            name=name,
            started_at=bstack1l11l11ll_opy_(),
            file_path=os.path.relpath(attrs[bstack11ll11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬཪ")], start=os.getcwd()),
            scope=RobotHandler.bstack111ll111ll_opy_(attrs.get(bstack11ll11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ཫ"), None)),
            framework=bstack11ll11_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ཬ"),
            tags=attrs[bstack11ll11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭཭")],
            hooks=self.store[bstack11ll11_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨ཮")],
            bstack111lll11l1_opy_=bstack1l1l1l1ll_opy_.bstack111ll1l111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11ll11_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧ཯").format(bstack11ll11_opy_ (u"ࠦࠥࠨ཰").join(attrs[bstack11ll11_opy_ (u"ࠬࡺࡡࡨࡵཱࠪ")]), name) if attrs[bstack11ll11_opy_ (u"࠭ࡴࡢࡩࡶིࠫ")] else name
        )
        self._1111lll111_opy_[attrs.get(bstack11ll11_opy_ (u"ࠧࡪࡦཱིࠪ"))][bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤུࠫ")] = bstack111lll1ll1_opy_
        threading.current_thread().current_test_uuid = bstack111lll1ll1_opy_.bstack111l1ll1l1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11ll11_opy_ (u"ࠩ࡬ࡨཱུࠬ"), None)
        self.bstack111ll1l11l_opy_(bstack11ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫྲྀ"), bstack111lll1ll1_opy_)
    @bstack111l1lll11_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111ll1llll_opy_.reset()
        bstack111l11l1l1_opy_ = bstack111l1llll1_opy_.get(attrs.get(bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫཷ")), bstack11ll11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ླྀ"))
        self._1111lll111_opy_[attrs.get(bstack11ll11_opy_ (u"࠭ࡩࡥࠩཹ"))][bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣེࠪ")].stop(time=bstack1l11l11ll_opy_(), duration=int(attrs.get(bstack11ll11_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪཻ࠭"), bstack11ll11_opy_ (u"ࠩ࠳ོࠫ"))), result=Result(result=bstack111l11l1l1_opy_, exception=attrs.get(bstack11ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨཽࠫ")), bstack111ll1ll1l_opy_=[attrs.get(bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཾ"))]))
        self.bstack111ll1l11l_opy_(bstack11ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧཿ"), self._1111lll111_opy_[attrs.get(bstack11ll11_opy_ (u"࠭ࡩࡥྀࠩ"))][bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣཱྀࠪ")], True)
        self.store[bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬྂ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111l1lll11_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111ll111l1_opy_()
        current_test_id = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫྃ"), None)
        bstack111l11llll_opy_ = current_test_id if bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨ྄ࠬ"), None) else bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧ྅"), None)
        if attrs.get(bstack11ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪ྆"), bstack11ll11_opy_ (u"࠭ࠧ྇")).lower() in [bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ྈ"), bstack11ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪྉ")]:
            hook_type = bstack111l11ll1l_opy_(attrs.get(bstack11ll11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧྊ")), bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧྋ"), None))
            hook_name = bstack11ll11_opy_ (u"ࠫࢀࢃࠧྌ").format(attrs.get(bstack11ll11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬྍ"), bstack11ll11_opy_ (u"࠭ࠧྎ")))
            if hook_type in [bstack11ll11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫྏ"), bstack11ll11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫྐ")]:
                hook_name = bstack11ll11_opy_ (u"ࠩ࡞ࡿࢂࡣࠠࡼࡿࠪྑ").format(bstack1111lllll1_opy_.get(hook_type), attrs.get(bstack11ll11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪྒ"), bstack11ll11_opy_ (u"ࠫࠬྒྷ")))
            bstack111l1l1lll_opy_ = bstack111lll11ll_opy_(
                bstack111l11l1ll_opy_=bstack111l11llll_opy_ + bstack11ll11_opy_ (u"ࠬ࠳ࠧྔ") + attrs.get(bstack11ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫྕ"), bstack11ll11_opy_ (u"ࠧࠨྖ")).lower(),
                name=hook_name,
                started_at=bstack1l11l11ll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11ll11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨྗ")), start=os.getcwd()),
                framework=bstack11ll11_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ྘"),
                tags=attrs[bstack11ll11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨྙ")],
                scope=RobotHandler.bstack111ll111ll_opy_(attrs.get(bstack11ll11_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫྚ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l1l1lll_opy_.bstack111l1ll1l1_opy_()
            threading.current_thread().current_hook_id = bstack111l11llll_opy_ + bstack11ll11_opy_ (u"ࠬ࠳ࠧྛ") + attrs.get(bstack11ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫྜ"), bstack11ll11_opy_ (u"ࠧࠨྜྷ")).lower()
            self.store[bstack11ll11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬྞ")] = [bstack111l1l1lll_opy_.bstack111l1ll1l1_opy_()]
            if bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ྟ"), None):
                self.store[bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧྠ")].append(bstack111l1l1lll_opy_.bstack111l1ll1l1_opy_())
            else:
                self.store[bstack11ll11_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪྡ")].append(bstack111l1l1lll_opy_.bstack111l1ll1l1_opy_())
            if bstack111l11llll_opy_:
                self._1111lll111_opy_[bstack111l11llll_opy_ + bstack11ll11_opy_ (u"ࠬ࠳ࠧྡྷ") + attrs.get(bstack11ll11_opy_ (u"࠭ࡴࡺࡲࡨࠫྣ"), bstack11ll11_opy_ (u"ࠧࠨྤ")).lower()] = { bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྥ"): bstack111l1l1lll_opy_ }
            bstack1l1l1l1ll_opy_.bstack111ll1l11l_opy_(bstack11ll11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪྦ"), bstack111l1l1lll_opy_)
        else:
            bstack111ll1l1ll_opy_ = {
                bstack11ll11_opy_ (u"ࠪ࡭ࡩ࠭ྦྷ"): uuid4().__str__(),
                bstack11ll11_opy_ (u"ࠫࡹ࡫ࡸࡵࠩྨ"): bstack11ll11_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫྩ").format(attrs.get(bstack11ll11_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ྪ")), attrs.get(bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬྫ"), bstack11ll11_opy_ (u"ࠨࠩྫྷ"))) if attrs.get(bstack11ll11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧྭ"), []) else attrs.get(bstack11ll11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪྮ")),
                bstack11ll11_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫྯ"): attrs.get(bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪྰ"), []),
                bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪྱ"): bstack1l11l11ll_opy_(),
                bstack11ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧྲ"): bstack11ll11_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩླ"),
                bstack11ll11_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧྴ"): attrs.get(bstack11ll11_opy_ (u"ࠪࡨࡴࡩࠧྵ"), bstack11ll11_opy_ (u"ࠫࠬྶ"))
            }
            if attrs.get(bstack11ll11_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭ྷ"), bstack11ll11_opy_ (u"࠭ࠧྸ")) != bstack11ll11_opy_ (u"ࠧࠨྐྵ"):
                bstack111ll1l1ll_opy_[bstack11ll11_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩྺ")] = attrs.get(bstack11ll11_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪྻ"))
            if not self.bstack111l1l1l1l_opy_:
                self._1111lll111_opy_[self._1111ll1ll1_opy_()][bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྼ")].add_step(bstack111ll1l1ll_opy_)
                threading.current_thread().current_step_uuid = bstack111ll1l1ll_opy_[bstack11ll11_opy_ (u"ࠫ࡮ࡪࠧ྽")]
            self.bstack111l1l1l1l_opy_.append(bstack111ll1l1ll_opy_)
    @bstack111l1lll11_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1111lll1l1_opy_()
        self._111ll11l11_opy_(messages)
        current_test_id = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ྾"), None)
        bstack111l11llll_opy_ = current_test_id if current_test_id else bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ྿"), None)
        bstack111l1ll111_opy_ = bstack111l1llll1_opy_.get(attrs.get(bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ࿀")), bstack11ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ࿁"))
        bstack111l1ll1ll_opy_ = attrs.get(bstack11ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿂"))
        if bstack111l1ll111_opy_ != bstack11ll11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫ࿃") and not attrs.get(bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿄")) and self._111l111l11_opy_:
            bstack111l1ll1ll_opy_ = self._111l111l11_opy_
        bstack111lll1l11_opy_ = Result(result=bstack111l1ll111_opy_, exception=bstack111l1ll1ll_opy_, bstack111ll1ll1l_opy_=[bstack111l1ll1ll_opy_])
        if attrs.get(bstack11ll11_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿅"), bstack11ll11_opy_ (u"࿆࠭ࠧ")).lower() in [bstack11ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭࿇"), bstack11ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ࿈")]:
            bstack111l11llll_opy_ = current_test_id if current_test_id else bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬ࿉"), None)
            if bstack111l11llll_opy_:
                bstack111ll11lll_opy_ = bstack111l11llll_opy_ + bstack11ll11_opy_ (u"ࠥ࠱ࠧ࿊") + attrs.get(bstack11ll11_opy_ (u"ࠫࡹࡿࡰࡦࠩ࿋"), bstack11ll11_opy_ (u"ࠬ࠭࿌")).lower()
                self._1111lll111_opy_[bstack111ll11lll_opy_][bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿍")].stop(time=bstack1l11l11ll_opy_(), duration=int(attrs.get(bstack11ll11_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬ࿎"), bstack11ll11_opy_ (u"ࠨ࠲ࠪ࿏"))), result=bstack111lll1l11_opy_)
                bstack1l1l1l1ll_opy_.bstack111ll1l11l_opy_(bstack11ll11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ࿐"), self._1111lll111_opy_[bstack111ll11lll_opy_][bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿑")])
        else:
            bstack111l11llll_opy_ = current_test_id if current_test_id else bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢ࡭ࡩ࠭࿒"), None)
            if bstack111l11llll_opy_ and len(self.bstack111l1l1l1l_opy_) == 1:
                current_step_uuid = bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩ࿓"), None)
                self._1111lll111_opy_[bstack111l11llll_opy_][bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿔")].bstack111ll1ll11_opy_(current_step_uuid, duration=int(attrs.get(bstack11ll11_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬ࿕"), bstack11ll11_opy_ (u"ࠨ࠲ࠪ࿖"))), result=bstack111lll1l11_opy_)
            else:
                self.bstack111l11l11l_opy_(attrs)
            self.bstack111l1l1l1l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11ll11_opy_ (u"ࠩ࡫ࡸࡲࡲࠧ࿗"), bstack11ll11_opy_ (u"ࠪࡲࡴ࠭࿘")) == bstack11ll11_opy_ (u"ࠫࡾ࡫ࡳࠨ࿙"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l1ll11_opy_.bstack111llll1l1_opy_():
                logs.append({
                    bstack11ll11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ࿚"): bstack1l11l11ll_opy_(),
                    bstack11ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ࿛"): message.get(bstack11ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿜")),
                    bstack11ll11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ࿝"): message.get(bstack11ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ࿞")),
                    **bstack11l1ll11_opy_.bstack111llll1l1_opy_()
                })
                if len(logs) > 0:
                    bstack1l1l1l1ll_opy_.bstack11ll1lllll_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1l1l1l1ll_opy_.bstack111l111111_opy_()
    def bstack111l11l11l_opy_(self, bstack111l1l11l1_opy_):
        if not bstack11l1ll11_opy_.bstack111llll1l1_opy_():
            return
        kwname = bstack11ll11_opy_ (u"ࠪࡿࢂࠦࡻࡾࠩ࿟").format(bstack111l1l11l1_opy_.get(bstack11ll11_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ࿠")), bstack111l1l11l1_opy_.get(bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪ࿡"), bstack11ll11_opy_ (u"࠭ࠧ࿢"))) if bstack111l1l11l1_opy_.get(bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬ࿣"), []) else bstack111l1l11l1_opy_.get(bstack11ll11_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ࿤"))
        error_message = bstack11ll11_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠡࡾࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠ࡝ࠤࡾ࠶ࢂࡢࠢࠣ࿥").format(kwname, bstack111l1l11l1_opy_.get(bstack11ll11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ࿦")), str(bstack111l1l11l1_opy_.get(bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿧"))))
        bstack1111lll1ll_opy_ = bstack11ll11_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠦ࿨").format(kwname, bstack111l1l11l1_opy_.get(bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭࿩")))
        bstack111l1lll1l_opy_ = error_message if bstack111l1l11l1_opy_.get(bstack11ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿪")) else bstack1111lll1ll_opy_
        bstack111l1111ll_opy_ = {
            bstack11ll11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ࿫"): self.bstack111l1l1l1l_opy_[-1].get(bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭࿬"), bstack1l11l11ll_opy_()),
            bstack11ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿭"): bstack111l1lll1l_opy_,
            bstack11ll11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ࿮"): bstack11ll11_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫ࿯") if bstack111l1l11l1_opy_.get(bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭࿰")) == bstack11ll11_opy_ (u"ࠧࡇࡃࡌࡐࠬ࿱") else bstack11ll11_opy_ (u"ࠨࡋࡑࡊࡔ࠭࿲"),
            **bstack11l1ll11_opy_.bstack111llll1l1_opy_()
        }
        bstack1l1l1l1ll_opy_.bstack11ll1lllll_opy_([bstack111l1111ll_opy_])
    def _1111ll1ll1_opy_(self):
        for bstack111l11l1ll_opy_ in reversed(self._1111lll111_opy_):
            bstack1111ll1lll_opy_ = bstack111l11l1ll_opy_
            data = self._1111lll111_opy_[bstack111l11l1ll_opy_][bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿳")]
            if isinstance(data, bstack111lll11ll_opy_):
                if not bstack11ll11_opy_ (u"ࠪࡉࡆࡉࡈࠨ࿴") in data.bstack111l1111l1_opy_():
                    return bstack1111ll1lll_opy_
            else:
                return bstack1111ll1lll_opy_
    def _111ll11l11_opy_(self, messages):
        try:
            bstack111ll1111l_opy_ = BuiltIn().get_variable_value(bstack11ll11_opy_ (u"ࠦࠩࢁࡌࡐࡉࠣࡐࡊ࡜ࡅࡍࡿࠥ࿵")) in (bstack111l1lllll_opy_.DEBUG, bstack111l1lllll_opy_.TRACE)
            for message, bstack111l11111l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿶"))
                level = message.get(bstack11ll11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ࿷"))
                if level == bstack111l1lllll_opy_.FAIL:
                    self._111l111l11_opy_ = name or self._111l111l11_opy_
                    self._111l1l1111_opy_ = bstack111l11111l_opy_.get(bstack11ll11_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ࿸")) if bstack111ll1111l_opy_ and bstack111l11111l_opy_ else self._111l1l1111_opy_
        except:
            pass
    @classmethod
    def bstack111ll1l11l_opy_(self, event: str, bstack111l1l111l_opy_: bstack111l111lll_opy_, bstack111l1l1l11_opy_=False):
        if event == bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ࿹"):
            bstack111l1l111l_opy_.set(hooks=self.store[bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭࿺")])
        if event == bstack11ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ࿻"):
            event = bstack11ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭࿼")
        if bstack111l1l1l11_opy_:
            bstack111l1l1ll1_opy_ = {
                bstack11ll11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ࿽"): event,
                bstack111l1l111l_opy_.bstack111l1ll11l_opy_(): bstack111l1l111l_opy_.bstack111l1l11ll_opy_(event)
            }
            self.bstack111l111l1l_opy_.append(bstack111l1l1ll1_opy_)
        else:
            bstack1l1l1l1ll_opy_.bstack111ll1l11l_opy_(event, bstack111l1l111l_opy_)
class bstack1111llllll_opy_:
    def __init__(self):
        self._1111lll11l_opy_ = []
    def bstack111ll111l1_opy_(self):
        self._1111lll11l_opy_.append([])
    def bstack1111lll1l1_opy_(self):
        return self._1111lll11l_opy_.pop() if self._1111lll11l_opy_ else list()
    def push(self, message):
        self._1111lll11l_opy_[-1].append(message) if self._1111lll11l_opy_ else self._1111lll11l_opy_.append([message])
class bstack111l1lllll_opy_:
    FAIL = bstack11ll11_opy_ (u"࠭ࡆࡂࡋࡏࠫ࿾")
    ERROR = bstack11ll11_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭࿿")
    WARNING = bstack11ll11_opy_ (u"ࠨ࡙ࡄࡖࡓ࠭က")
    bstack111l11lll1_opy_ = bstack11ll11_opy_ (u"ࠩࡌࡒࡋࡕࠧခ")
    DEBUG = bstack11ll11_opy_ (u"ࠪࡈࡊࡈࡕࡈࠩဂ")
    TRACE = bstack11ll11_opy_ (u"࡙ࠫࡘࡁࡄࡇࠪဃ")
    bstack1111llll1l_opy_ = [FAIL, ERROR]
def bstack111l11l111_opy_(bstack111l11ll11_opy_):
    if not bstack111l11ll11_opy_:
        return None
    if bstack111l11ll11_opy_.get(bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨင"), None):
        return getattr(bstack111l11ll11_opy_[bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩစ")], bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬဆ"), None)
    return bstack111l11ll11_opy_.get(bstack11ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ဇ"), None)
def bstack111l11ll1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨဈ"), bstack11ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬဉ")]:
        return
    if hook_type.lower() == bstack11ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪည"):
        if current_test_uuid is None:
            return bstack11ll11_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩဋ")
        else:
            return bstack11ll11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫဌ")
    elif hook_type.lower() == bstack11ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩဍ"):
        if current_test_uuid is None:
            return bstack11ll11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫဎ")
        else:
            return bstack11ll11_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ဏ")