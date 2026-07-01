# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11111l11_opy_ import RobotHandler
from bstack_utils.capture import bstack111ll1l1_opy_
from bstack_utils.test_data import bstack1lll1l1ll_opy_, bstack11ll1l1l_opy_, bstack1l1l1111_opy_
from bstack_utils.bstack11l111ll_opy_ import bstack1ll111ll_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.constants import *
from bstack_utils.helper import bstack11llll11_opy_, bstack1l1111ll_opy_, Result, \
    error_handler, bstack1llllllll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1l1llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪਏ"): [],
        bstack1l1llll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ਐ"): [],
        bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ਑"): []
    }
    bstack111111ll_opy_ = []
    bstack1lll1ll11_opy_ = []
    @staticmethod
    def log_handler(log):
        if not ((isinstance(log[bstack1l1llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ਒")], list) or (isinstance(log[bstack1l1llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫਓ")], dict)) and len(log[bstack1l1llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬਔ")])>0) or (isinstance(log[bstack1l1llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ਕ")], str) and log[bstack1l1llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧਖ")].strip())):
            return
        active = bstack1ll111ll_opy_.bstack11llll1l_opy_()
        log = {
            bstack1l1llll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ਗ"): log[bstack1l1llll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧਘ")],
            bstack1l1llll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬਙ"): bstack1llllllll_opy_().isoformat() + bstack1l1llll_opy_ (u"ࠪ࡞ࠬਚ"),
            bstack1l1llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬਛ"): log[bstack1l1llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ਜ")],
        }
        if active:
            if active[bstack1l1llll_opy_ (u"࠭ࡴࡺࡲࡨࠫਝ")] == bstack1l1llll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬਞ"):
                log[bstack1l1llll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨਟ")] = active[bstack1l1llll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩਠ")]
            elif active[bstack1l1llll_opy_ (u"ࠪࡸࡾࡶࡥࠨਡ")] == bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩਢ"):
                log[bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬਣ")] = active[bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ਤ")]
        TestHubHandler.bstack1ll11111_opy_([log])
    def __init__(self):
        self.messages = bstack1llll111l_opy_()
        self._1lll1l111_opy_ = None
        self._11111l1l_opy_ = None
        self._1llll11ll_opy_ = OrderedDict()
        self.bstack11l1l111_opy_ = bstack111ll1l1_opy_(self.log_handler)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1lllllll1_opy_()
        if not self._1llll11ll_opy_.get(attrs.get(bstack1l1llll_opy_ (u"ࠧࡪࡦࠪਥ")), None):
            self._1llll11ll_opy_[attrs.get(bstack1l1llll_opy_ (u"ࠨ࡫ࡧࠫਦ"))] = {}
        bstack1111l11l_opy_ = bstack1l1l1111_opy_(
                bstack1111l111_opy_=attrs.get(bstack1l1llll_opy_ (u"ࠩ࡬ࡨࠬਧ")),
                name=name,
                started_at=bstack1l1111ll_opy_(),
                file_path=os.path.relpath(attrs[bstack1l1llll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪਨ")], start=os.getcwd()) if attrs.get(bstack1l1llll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ਩")) != bstack1l1llll_opy_ (u"ࠬ࠭ਪ") else bstack1l1llll_opy_ (u"࠭ࠧਫ"),
                framework=bstack1l1llll_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ਬ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l1llll_opy_ (u"ࠨ࡫ࡧࠫਭ"), None)
        self._1llll11ll_opy_[attrs.get(bstack1l1llll_opy_ (u"ࠩ࡬ࡨࠬਮ"))][bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ਯ")] = bstack1111l11l_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1lll11lll_opy_()
        self._1111ll11_opy_(messages)
        with self._lock:
            for bstack1lllll11l_opy_ in self.bstack111111ll_opy_:
                bstack1lllll11l_opy_[bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ਰ")][bstack1l1llll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ਱")].extend(self.store[bstack1l1llll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬਲ")])
                TestHubHandler.bstack1lll11ll1_opy_(bstack1lllll11l_opy_)
            self.bstack111111ll_opy_ = []
            self.store[bstack1l1llll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ਲ਼")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11l1l111_opy_.start()
        if not self._1llll11ll_opy_.get(attrs.get(bstack1l1llll_opy_ (u"ࠨ࡫ࡧࠫ਴")), None):
            self._1llll11ll_opy_[attrs.get(bstack1l1llll_opy_ (u"ࠩ࡬ࡨࠬਵ"))] = {}
        driver = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩਸ਼"), None)
        test_data = bstack1l1l1111_opy_(
            bstack1111l111_opy_=attrs.get(bstack1l1llll_opy_ (u"ࠫ࡮ࡪࠧ਷")),
            name=name,
            started_at=bstack1l1111ll_opy_(),
            file_path=os.path.relpath(attrs[bstack1l1llll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬਸ")], start=os.getcwd()),
            scope=RobotHandler.bstack1llll1ll1_opy_(attrs.get(bstack1l1llll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ਹ"), None)),
            framework=bstack1l1llll_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭਺"),
            tags=attrs[bstack1l1llll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭਻")],
            hooks=self.store[bstack1l1llll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨ਼")],
            integrations=TestHubHandler.bstack1l11111l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l1llll_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧ਽").format(bstack1l1llll_opy_ (u"ࠦࠥࠨਾ").join(attrs[bstack1l1llll_opy_ (u"ࠬࡺࡡࡨࡵࠪਿ")]), name) if attrs[bstack1l1llll_opy_ (u"࠭ࡴࡢࡩࡶࠫੀ")] else name
        )
        self._1llll11ll_opy_[attrs.get(bstack1l1llll_opy_ (u"ࠧࡪࡦࠪੁ"))][bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫੂ")] = test_data
        threading.current_thread().current_test_uuid = test_data.bstack1lllll111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l1llll_opy_ (u"ࠩ࡬ࡨࠬ੃"), None)
        self.bstack11lll1ll_opy_(bstack1l1llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ੄"), test_data)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11l1l111_opy_.reset()
        bstack1111llll_opy_ = bstack111l111l_opy_.get(attrs.get(bstack1l1llll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ੅")), bstack1l1llll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭੆"))
        self._1llll11ll_opy_[attrs.get(bstack1l1llll_opy_ (u"࠭ࡩࡥࠩੇ"))][bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪੈ")].stop(time=bstack1l1111ll_opy_(), duration=int(attrs.get(bstack1l1llll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭੉"), bstack1l1llll_opy_ (u"ࠩ࠳ࠫ੊"))), result=Result(result=bstack1111llll_opy_, exception=attrs.get(bstack1l1llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫੋ")), bstack1l1l1ll1_opy_=[attrs.get(bstack1l1llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬੌ"))]))
        self.bstack11lll1ll_opy_(bstack1l1llll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪ੍ࠧ"), self._1llll11ll_opy_[attrs.get(bstack1l1llll_opy_ (u"࠭ࡩࡥࠩ੎"))][bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ੏")], True)
        with self._lock:
            self.store[bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ੐")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1lllllll1_opy_()
        current_test_id = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫੑ"), None)
        bstack1lll1llll_opy_ = current_test_id if bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬ੒"), None) else bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧ੓"), None)
        if attrs.get(bstack1l1llll_opy_ (u"ࠬࡺࡹࡱࡧࠪ੔"), bstack1l1llll_opy_ (u"࠭ࠧ੕")).lower() in [bstack1l1llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭੖"), bstack1l1llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ੗")]:
            hook_type = bstack11111lll_opy_(attrs.get(bstack1l1llll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ੘")), bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧਖ਼"), None))
            hook_name = bstack1l1llll_opy_ (u"ࠫࢀࢃࠧਗ਼").format(attrs.get(bstack1l1llll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬਜ਼"), bstack1l1llll_opy_ (u"࠭ࠧੜ")))
            if hook_type in [bstack1l1llll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ੝"), bstack1l1llll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫਫ਼")]:
                hook_name = bstack1l1llll_opy_ (u"ࠩ࡞ࡿࢂࡣࠠࡼࡿࠪ੟").format(bstack1llllll11_opy_.get(hook_type), attrs.get(bstack1l1llll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ੠"), bstack1l1llll_opy_ (u"ࠫࠬ੡")))
            bstack1lllll1l1_opy_ = bstack11ll1l1l_opy_(
                bstack1111l111_opy_=bstack1lll1llll_opy_ + bstack1l1llll_opy_ (u"ࠬ࠳ࠧ੢") + attrs.get(bstack1l1llll_opy_ (u"࠭ࡴࡺࡲࡨࠫ੣"), bstack1l1llll_opy_ (u"ࠧࠨ੤")).lower(),
                name=hook_name,
                started_at=bstack1l1111ll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l1llll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ੥")), start=os.getcwd()),
                framework=bstack1l1llll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ੦"),
                tags=attrs[bstack1l1llll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ੧")],
                scope=RobotHandler.bstack1llll1ll1_opy_(attrs.get(bstack1l1llll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ੨"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1lllll1l1_opy_.bstack1lllll111_opy_()
            threading.current_thread().current_hook_id = bstack1lll1llll_opy_ + bstack1l1llll_opy_ (u"ࠬ࠳ࠧ੩") + attrs.get(bstack1l1llll_opy_ (u"࠭ࡴࡺࡲࡨࠫ੪"), bstack1l1llll_opy_ (u"ࠧࠨ੫")).lower()
            with self._lock:
                self.store[bstack1l1llll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ੬")] = [bstack1lllll1l1_opy_.bstack1lllll111_opy_()]
                if bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭੭"), None):
                    self.store[bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ੮")].append(bstack1lllll1l1_opy_.bstack1lllll111_opy_())
                else:
                    self.store[bstack1l1llll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ੯")].append(bstack1lllll1l1_opy_.bstack1lllll111_opy_())
            if bstack1lll1llll_opy_:
                self._1llll11ll_opy_[bstack1lll1llll_opy_ + bstack1l1llll_opy_ (u"ࠬ࠳ࠧੰ") + attrs.get(bstack1l1llll_opy_ (u"࠭ࡴࡺࡲࡨࠫੱ"), bstack1l1llll_opy_ (u"ࠧࠨੲ")).lower()] = { bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫੳ"): bstack1lllll1l1_opy_ }
            TestHubHandler.bstack11lll1ll_opy_(bstack1l1llll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪੴ"), bstack1lllll1l1_opy_)
        else:
            bstack11ll111l_opy_ = {
                bstack1l1llll_opy_ (u"ࠪ࡭ࡩ࠭ੵ"): uuid4().__str__(),
                bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ੶"): bstack1l1llll_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫ੷").format(attrs.get(bstack1l1llll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭੸")), attrs.get(bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࡷࠬ੹"), bstack1l1llll_opy_ (u"ࠨࠩ੺"))) if attrs.get(bstack1l1llll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ੻"), []) else attrs.get(bstack1l1llll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪ੼")),
                bstack1l1llll_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫ੽"): attrs.get(bstack1l1llll_opy_ (u"ࠬࡧࡲࡨࡵࠪ੾"), []),
                bstack1l1llll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ੿"): bstack1l1111ll_opy_(),
                bstack1l1llll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ઀"): bstack1l1llll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩઁ"),
                bstack1l1llll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧં"): attrs.get(bstack1l1llll_opy_ (u"ࠪࡨࡴࡩࠧઃ"), bstack1l1llll_opy_ (u"ࠫࠬ઄"))
            }
            if attrs.get(bstack1l1llll_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭અ"), bstack1l1llll_opy_ (u"࠭ࠧઆ")) != bstack1l1llll_opy_ (u"ࠧࠨઇ"):
                bstack11ll111l_opy_[bstack1l1llll_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩઈ")] = attrs.get(bstack1l1llll_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪઉ"))
            if not self.bstack1lll1ll11_opy_:
                self._1llll11ll_opy_[self._111l11l1_opy_()][bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ઊ")].add_step(bstack11ll111l_opy_)
                threading.current_thread().current_step_uuid = bstack11ll111l_opy_[bstack1l1llll_opy_ (u"ࠫ࡮ࡪࠧઋ")]
            self.bstack1lll1ll11_opy_.append(bstack11ll111l_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1lll11lll_opy_()
        self._1111ll11_opy_(messages)
        current_test_id = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧઌ"), None)
        bstack1lll1llll_opy_ = current_test_id if current_test_id else bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩઍ"), None)
        bstack1llll1111_opy_ = bstack111l111l_opy_.get(attrs.get(bstack1l1llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ઎")), bstack1l1llll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩએ"))
        bstack11111ll1_opy_ = attrs.get(bstack1l1llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪઐ"))
        if bstack1llll1111_opy_ != bstack1l1llll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫઑ") and not attrs.get(bstack1l1llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ઒")) and self._1lll1l111_opy_:
            bstack11111ll1_opy_ = self._1lll1l111_opy_
        bstack111lll1l_opy_ = Result(result=bstack1llll1111_opy_, exception=bstack11111ll1_opy_, bstack1l1l1ll1_opy_=[bstack11111ll1_opy_])
        if attrs.get(bstack1l1llll_opy_ (u"ࠬࡺࡹࡱࡧࠪઓ"), bstack1l1llll_opy_ (u"࠭ࠧઔ")).lower() in [bstack1l1llll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ક"), bstack1l1llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪખ")]:
            bstack1lll1llll_opy_ = current_test_id if current_test_id else bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬગ"), None)
            if bstack1lll1llll_opy_:
                bstack1ll111l1_opy_ = bstack1lll1llll_opy_ + bstack1l1llll_opy_ (u"ࠥ࠱ࠧઘ") + attrs.get(bstack1l1llll_opy_ (u"ࠫࡹࡿࡰࡦࠩઙ"), bstack1l1llll_opy_ (u"ࠬ࠭ચ")).lower()
                self._1llll11ll_opy_[bstack1ll111l1_opy_][bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩછ")].stop(time=bstack1l1111ll_opy_(), duration=int(attrs.get(bstack1l1llll_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬજ"), bstack1l1llll_opy_ (u"ࠨ࠲ࠪઝ"))), result=bstack111lll1l_opy_)
                TestHubHandler.bstack11lll1ll_opy_(bstack1l1llll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫઞ"), self._1llll11ll_opy_[bstack1ll111l1_opy_][bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ટ")])
        else:
            bstack1lll1llll_opy_ = current_test_id if current_test_id else bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢ࡭ࡩ࠭ઠ"), None)
            if bstack1lll1llll_opy_ and len(self.bstack1lll1ll11_opy_) == 1:
                current_step_uuid = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩડ"), None)
                self._1llll11ll_opy_[bstack1lll1llll_opy_][bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩઢ")].bstack1l111111_opy_(current_step_uuid, duration=int(attrs.get(bstack1l1llll_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬણ"), bstack1l1llll_opy_ (u"ࠨ࠲ࠪત"))), result=bstack111lll1l_opy_)
            else:
                self.bstack1llllll1l_opy_(attrs)
            self.bstack1lll1ll11_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l1llll_opy_ (u"ࠩ࡫ࡸࡲࡲࠧથ"), bstack1l1llll_opy_ (u"ࠪࡲࡴ࠭દ")) == bstack1l1llll_opy_ (u"ࠫࡾ࡫ࡳࠨધ"):
                return
            self.messages.push(message)
            logs = []
            if bstack1ll111ll_opy_.bstack11llll1l_opy_():
                logs.append({
                    bstack1l1llll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨન"): bstack1l1111ll_opy_(),
                    bstack1l1llll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ઩"): message.get(bstack1l1llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨપ")),
                    bstack1l1llll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧફ"): message.get(bstack1l1llll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨબ")),
                    **bstack1ll111ll_opy_.bstack11llll1l_opy_()
                })
                if len(logs) > 0:
                    TestHubHandler.bstack1ll11111_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        TestHubHandler.bstack1111111l_opy_()
    def bstack1llllll1l_opy_(self, bstack1lll11l11_opy_):
        if not bstack1ll111ll_opy_.bstack11llll1l_opy_():
            return
        kwname = bstack1l1llll_opy_ (u"ࠪࡿࢂࠦࡻࡾࠩભ").format(bstack1lll11l11_opy_.get(bstack1l1llll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫમ")), bstack1lll11l11_opy_.get(bstack1l1llll_opy_ (u"ࠬࡧࡲࡨࡵࠪય"), bstack1l1llll_opy_ (u"࠭ࠧર"))) if bstack1lll11l11_opy_.get(bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࡷࠬ઱"), []) else bstack1lll11l11_opy_.get(bstack1l1llll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨલ"))
        error_message = bstack1l1llll_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠡࡾࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠ࡝ࠤࡾ࠶ࢂࡢࠢࠣળ").format(kwname, bstack1lll11l11_opy_.get(bstack1l1llll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ઴")), str(bstack1lll11l11_opy_.get(bstack1l1llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬવ"))))
        bstack111l11ll_opy_ = bstack1l1llll_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠦશ").format(kwname, bstack1lll11l11_opy_.get(bstack1l1llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ષ")))
        bstack1111ll1l_opy_ = error_message if bstack1lll11l11_opy_.get(bstack1l1llll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨસ")) else bstack111l11ll_opy_
        bstack1111lll1_opy_ = {
            bstack1l1llll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫહ"): self.bstack1lll1ll11_opy_[-1].get(bstack1l1llll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭઺"), bstack1l1111ll_opy_()),
            bstack1l1llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ઻"): bstack1111ll1l_opy_,
            bstack1l1llll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮઼ࠪ"): bstack1l1llll_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫઽ") if bstack1lll11l11_opy_.get(bstack1l1llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ા")) == bstack1l1llll_opy_ (u"ࠧࡇࡃࡌࡐࠬિ") else bstack1l1llll_opy_ (u"ࠨࡋࡑࡊࡔ࠭ી"),
            **bstack1ll111ll_opy_.bstack11llll1l_opy_()
        }
        TestHubHandler.bstack1ll11111_opy_([bstack1111lll1_opy_])
    def _111l11l1_opy_(self):
        for bstack1111l111_opy_ in reversed(self._1llll11ll_opy_):
            bstack1lll11l1l_opy_ = bstack1111l111_opy_
            data = self._1llll11ll_opy_[bstack1111l111_opy_][bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬુ")]
            if isinstance(data, bstack11ll1l1l_opy_):
                if not bstack1l1llll_opy_ (u"ࠪࡉࡆࡉࡈࠨૂ") in data.bstack1llll1l1l_opy_():
                    return bstack1lll11l1l_opy_
            else:
                return bstack1lll11l1l_opy_
    def _1111ll11_opy_(self, messages):
        try:
            bstack11111111_opy_ = BuiltIn().get_variable_value(bstack1l1llll_opy_ (u"ࠦࠩࢁࡌࡐࡉࠣࡐࡊ࡜ࡅࡍࡿࠥૃ")) in (bstack1111l1l1_opy_.DEBUG, bstack1111l1l1_opy_.TRACE)
            for message, bstack1llll1lll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l1llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ૄ"))
                level = message.get(bstack1l1llll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬૅ"))
                if level == bstack1111l1l1_opy_.FAIL:
                    self._1lll1l111_opy_ = name or self._1lll1l111_opy_
                    self._11111l1l_opy_ = bstack1llll1lll_opy_.get(bstack1l1llll_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ૆")) if bstack11111111_opy_ and bstack1llll1lll_opy_ else self._11111l1l_opy_
        except Exception as e:
            from bstack_utils import logger_utils
            logger_utils.get_logger(__name__).debug(bstack1l1llll_opy_ (u"ࠣࡴࡲࡦࡴࡺࠠࡧࡣ࡬ࡰ࠲ࡳࡥࡴࡵࡤ࡫ࡪࠦࡥࡹࡶࡵࡥࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃ࠺ࠡࡽࢀࠦે").format(type(e).__name__, e), exc_info=True)
    @classmethod
    def bstack11lll1ll_opy_(self, event: str, bstack1llll1l11_opy_: bstack1lll1l1ll_opy_, bstack1llll11l1_opy_=False):
        if event == bstack1l1llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫૈ"):
            bstack1llll1l11_opy_.set(hooks=self.store[bstack1l1llll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧૉ")])
        if event == bstack1l1llll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ૊"):
            event = bstack1l1llll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧો")
        if bstack1llll11l1_opy_:
            bstack111l1111_opy_ = {
                bstack1l1llll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪૌ"): event,
                bstack1llll1l11_opy_.bstack1lll1l11l_opy_(): bstack1llll1l11_opy_.bstack1111l1ll_opy_(event)
            }
            with self._lock:
                self.bstack111111ll_opy_.append(bstack111l1111_opy_)
        else:
            TestHubHandler.bstack11lll1ll_opy_(event, bstack1llll1l11_opy_)
class bstack1llll111l_opy_:
    def __init__(self):
        self._1lll1lll1_opy_ = []
    def bstack1lllllll1_opy_(self):
        self._1lll1lll1_opy_.append([])
    def bstack1lll11lll_opy_(self):
        return self._1lll1lll1_opy_.pop() if self._1lll1lll1_opy_ else list()
    def push(self, message):
        self._1lll1lll1_opy_[-1].append(message) if self._1lll1lll1_opy_ else self._1lll1lll1_opy_.append([message])
class bstack1111l1l1_opy_:
    FAIL = bstack1l1llll_opy_ (u"ࠧࡇࡃࡌࡐ્ࠬ")
    ERROR = bstack1l1llll_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧ૎")
    WARNING = bstack1l1llll_opy_ (u"࡚ࠩࡅࡗࡔࠧ૏")
    bstack1lll1ll1l_opy_ = bstack1l1llll_opy_ (u"ࠪࡍࡓࡌࡏࠨૐ")
    DEBUG = bstack1l1llll_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪ૑")
    TRACE = bstack1l1llll_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫ૒")
    bstack1lll1l1l1_opy_ = [FAIL, ERROR]
def bstack1lllll1ll_opy_(bstack111111l1_opy_):
    if not bstack111111l1_opy_:
        return None
    if bstack111111l1_opy_.get(bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ૓"), None):
        return getattr(bstack111111l1_opy_[bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ૔")], bstack1l1llll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭૕"), None)
    return bstack111111l1_opy_.get(bstack1l1llll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ૖"), None)
def bstack11111lll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l1llll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ૗"), bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭૘")]:
        return
    if hook_type.lower() == bstack1l1llll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ૙"):
        if current_test_uuid is None:
            return bstack1l1llll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪ૚")
        else:
            return bstack1l1llll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ૛")
    elif hook_type.lower() == bstack1l1llll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ૜"):
        if current_test_uuid is None:
            return bstack1l1llll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ૝")
        else:
            return bstack1l1llll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ૞")