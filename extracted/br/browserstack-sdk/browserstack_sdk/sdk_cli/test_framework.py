# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1l1lll11ll1_opy_ import bstack1l1lll11l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11111l_opy_ import bstack1l1ll1l1l11_opy_, bstack1l1ll1llll1_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll_opy_ (u"ࠢࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᬋ").format(self.name)
class TestFrameworkState(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack1ll_opy_ (u"ࠣࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᬌ").format(self.name)
class bstack1l1l11l11ll_opy_(bstack1l1ll1l1l11_opy_):
    bstack1l1l111111l_opy_: List[str]
    bstack1l11ll1ll1l_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1l1ll111ll1_opy_: datetime
    bstack1l1ll1ll1ll_opy_: datetime
    def __init__(
        self,
        context: bstack1l1ll1llll1_opy_,
        bstack1l1l111111l_opy_: List[str],
        bstack1l11ll1ll1l_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l1l111111l_opy_ = bstack1l1l111111l_opy_
        self.bstack1l11ll1ll1l_opy_ = bstack1l11ll1ll1l_opy_
        self.state = state
        self.bstack1l1ll111ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1ll1ll1ll_opy_ = datetime.now(tz=timezone.utc)
    def bstack1l1l1l1l_opy_(self, bstack1l1ll1l1ll1_opy_: TestFrameworkState):
        bstack1l1ll1l1lll_opy_ = TestFrameworkState(bstack1l1ll1l1ll1_opy_).name
        if not bstack1l1ll1l1lll_opy_:
            return False
        if bstack1l1ll1l1ll1_opy_ == self.state:
            return False
        self.state = bstack1l1ll1l1ll1_opy_
        self.bstack1l1ll1ll1ll_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll1ll1ll11_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack111l1111ll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack11ll1ll1111_opy_: int = None
    bstack11ll11lllll_opy_: str = None
    bstack1ll11l1_opy_: str = None
    bstack11ll11l1ll_opy_: str = None
    bstack11lll1l11l1_opy_: str = None
    bstack11l111l111l_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l1111ll1l1_opy_ = bstack1ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧᬍ")
    bstack11l1ll11111_opy_ = bstack1ll_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦᬎ")
    bstack1l111111lll_opy_ = bstack1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠢᬏ")
    bstack111llllllll_opy_ = bstack1ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭ࠨᬐ")
    bstack11l111l1l11_opy_ = bstack1ll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡹࡧࡧࡴࠤᬑ")
    bstack11l1ll11lll_opy_ = bstack1ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᬒ")
    bstack11ll1ll1l1l_opy_ = bstack1ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࡥࡡࡵࠤᬓ")
    bstack11ll1l11ll1_opy_ = bstack1ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᬔ")
    bstack11lll111111_opy_ = bstack1ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᬕ")
    bstack111lll1ll1l_opy_ = bstack1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᬖ")
    bstack1l11111111l_opy_ = bstack1ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠦᬗ")
    bstack11ll11l11ll_opy_ = bstack1ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᬘ")
    bstack111ll1ll1ll_opy_ = bstack1ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡩ࡯ࡥࡧࠥᬙ")
    bstack11ll111l1ll_opy_ = bstack1ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠥᬚ")
    bstack1l1111l11l1_opy_ = bstack1ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥᬛ")
    bstack11l1ll11l11_opy_ = bstack1ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࠤᬜ")
    bstack111ll1l1l11_opy_ = bstack1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠣᬝ")
    bstack111ll11llll_opy_ = bstack1ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴ࡭ࡳࠣᬞ")
    bstack111ll1l11ll_opy_ = bstack1ll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡲ࡫ࡴࡢࠤᬟ")
    bstack111ll11l11l_opy_ = bstack1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡹࡣࡰࡲࡨࡷࠬᬠ")
    bstack11l11l1l1ll_opy_ = bstack1ll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᬡ")
    bstack11l11111ll1_opy_ = bstack1ll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᬢ")
    bstack111lllll1ll_opy_ = bstack1ll_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᬣ")
    bstack111lllll111_opy_ = bstack1ll_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡬ࡨࠧᬤ")
    bstack11l1111lll1_opy_ = bstack1ll_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡪࡹࡵ࡭ࡶࠥᬥ")
    bstack11l111l11ll_opy_ = bstack1ll_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡱࡵࡧࡴࠤᬦ")
    bstack111ll1llll1_opy_ = bstack1ll_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠥᬧ")
    bstack111llll1111_opy_ = bstack1ll_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᬨ")
    bstack11l111l1ll1_opy_ = bstack1ll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᬩ")
    bstack11l111ll111_opy_ = bstack1ll_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦᬪ")
    bstack11l1111ll1l_opy_ = bstack1ll_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧᬫ")
    KIND_SCREENSHOT = bstack1ll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠢᬬ")
    bstack11ll11ll11l_opy_ = bstack1ll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡑࡕࡇࠣᬭ")
    bstack11ll1l1l1l1_opy_ = bstack1ll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᬮ")
    bstack1l111l11l_opy_: Dict[str, bstack1l1l11l11ll_opy_] = dict()
    bstack111l1ll1l1l_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l111111l_opy_: List[str]
    bstack1l11ll1ll1l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1l111111l_opy_: List[str],
        bstack1l11ll1ll1l_opy_: Dict[str, str],
        bstack1l1lll11ll1_opy_: bstack1l1lll11l11_opy_
    ):
        self.bstack1l1l111111l_opy_ = bstack1l1l111111l_opy_
        self.bstack1l11ll1ll1l_opy_ = bstack1l11ll1ll1l_opy_
        self.bstack1l1lll11ll1_opy_ = bstack1l1lll11ll1_opy_
    def track_event(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧᬯ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack111ll1ll1l1_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l111lllll_opy_ = TestFramework.bstack11l111ll11l_opy_(bstack1l1ll1lll11_opy_)
        if not bstack11l111lllll_opy_ in TestFramework.bstack111l1ll1l1l_opy_:
            return
        self.logger.debug(bstack1ll_opy_ (u"ࠤ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠥᬰ").format(len(TestFramework.bstack111l1ll1l1l_opy_[bstack11l111lllll_opy_])))
        for callback in TestFramework.bstack111l1ll1l1l_opy_[bstack11l111lllll_opy_]:
            try:
                callback(self, instance, bstack1l1ll1lll11_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠥᬱ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack11ll1l11lll_opy_(self):
        return
    @abc.abstractmethod
    def bstack11ll1ll1l11_opy_(self):
        return
    @abc.abstractmethod
    def bstack11ll11llll1_opy_(self, instance, bstack1l1ll1lll11_opy_):
        return
    @abc.abstractmethod
    def bstack11ll1l1lll1_opy_(self, instance, bstack1l1ll1lll11_opy_):
        return
    @staticmethod
    def bstack1l1ll1lll1l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1l1ll1l1l11_opy_.create_context(target)
        instance = TestFramework.bstack1l111l11l_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1l1llllll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack11ll1l11l11_opy_(reverse=True) -> List[bstack1l1l11l11ll_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1l111l11l_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll111ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1ll111111_opy_(ctx: bstack1l1ll1llll1_opy_, reverse=True) -> List[bstack1l1l11l11ll_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1l111l11l_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll111ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll11111lll_opy_(instance: bstack1l1l11l11ll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll11111l11_opy_(instance: bstack1l1l11l11ll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1l1l1l1l_opy_(instance: bstack1l1l11l11ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣᬲ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack111lllllll1_opy_(instance: bstack1l1l11l11ll_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1ll_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡱࡸࡷ࡯ࡥࡴ࠿ࡾࢁࠧᬳ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack111l1l1l1l1_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨ᬴").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1l1ll1lll1l_opy_(target, strict)
        return TestFramework.bstack1ll11111l11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1l1ll1lll1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1111l1l1_opy_(instance: bstack1l1l11l11ll_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack111ll1ll111_opy_(instance: bstack1l1l11l11ll_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11l111ll11l_opy_(bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack1ll_opy_ (u"ࠢ࠻ࠤᬵ").join((TestFrameworkState(bstack1l1ll1lll11_opy_[0]).name, TestHookState(bstack1l1ll1lll11_opy_[1]).name))
    @staticmethod
    def bstack1l1111111l1_opy_(bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11l111lllll_opy_ = TestFramework.bstack11l111ll11l_opy_(bstack1l1ll1lll11_opy_)
        TestFramework.logger.debug(bstack1ll_opy_ (u"ࠣࡵࡨࡸࡤ࡮࡯ࡰ࡭ࡢࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡨࡰࡱ࡮ࡣࡷ࡫ࡧࡪࡵࡷࡶࡾࡥ࡫ࡦࡻࡀࡿࢂࠨᬶ").format(bstack11l111lllll_opy_))
        if not bstack11l111lllll_opy_ in TestFramework.bstack111l1ll1l1l_opy_:
            TestFramework.bstack111l1ll1l1l_opy_[bstack11l111lllll_opy_] = []
        TestFramework.bstack111l1ll1l1l_opy_[bstack11l111lllll_opy_].append(callback)
    @staticmethod
    def bstack11ll11ll1l1_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡴࡪࡰࡶࠦᬷ"):
            return klass.__qualname__
        return module + bstack1ll_opy_ (u"ࠥ࠲ࠧᬸ") + klass.__qualname__
    @staticmethod
    def bstack11lll11llll_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}