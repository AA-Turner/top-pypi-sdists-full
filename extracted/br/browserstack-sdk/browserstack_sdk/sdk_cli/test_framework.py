# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1lll1111111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111l1_opy_ import bstack1ll1llll1l1_opy_, bstack1ll1ll11l11_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1111_opy_ (u"ࠤࡗࡩࡸࡺࡈࡰࡱ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᣁ").format(self.name)
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
        return bstack1111_opy_ (u"ࠥࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᣂ").format(self.name)
class bstack1ll11ll111l_opy_(bstack1ll1llll1l1_opy_):
    bstack1l1ll111l11_opy_: List[str]
    bstack11ll11l1l1l_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1ll1l1llll1_opy_: datetime
    bstack1ll1l1lll11_opy_: datetime
    def __init__(
        self,
        context: bstack1ll1ll11l11_opy_,
        bstack1l1ll111l11_opy_: List[str],
        bstack11ll11l1l1l_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l1ll111l11_opy_ = bstack1l1ll111l11_opy_
        self.bstack11ll11l1l1l_opy_ = bstack11ll11l1l1l_opy_
        self.state = state
        self.bstack1ll1l1llll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll1l1lll11_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll1l11l1l_opy_(self, bstack1ll1lll111l_opy_: TestFrameworkState):
        bstack1ll1lll1l1l_opy_ = TestFrameworkState(bstack1ll1lll111l_opy_).name
        if not bstack1ll1lll1l1l_opy_:
            return False
        if bstack1ll1lll111l_opy_ == self.state:
            return False
        self.state = bstack1ll1lll111l_opy_
        self.bstack1ll1l1lll11_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1lll1l1l1ll_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll11lllll1_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l111l11ll1_opy_: int = None
    bstack1l11ll1l111_opy_: str = None
    bstack1llll_opy_: str = None
    bstack1ll111ll1l_opy_: str = None
    bstack1l111l1111l_opy_: str = None
    bstack11ll11l1111_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l1l11l1l1l_opy_ = bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠢᣃ")
    bstack11llll1ll1l_opy_ = bstack1111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡭ࡩࠨᣄ")
    bstack1l1l11lll11_opy_ = bstack1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠤᣅ")
    bstack11l1lll11l1_opy_ = bstack1111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡢࡴࡦࡺࡨࠣᣆ")
    bstack11l1ll11l1l_opy_ = bstack1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡴࡢࡩࡶࠦᣇ")
    bstack11lllll111l_opy_ = bstack1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᣈ")
    bstack1l111ll1l11_opy_ = bstack1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡷࡺࡲࡴࡠࡣࡷࠦᣉ")
    bstack1l11l1lllll_opy_ = bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᣊ")
    bstack1l11l1l111l_opy_ = bstack1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧᣋ")
    bstack11l1llll11l_opy_ = bstack1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᣌ")
    bstack1l1l1111l11_opy_ = bstack1111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࠨᣍ")
    bstack1l111llll11_opy_ = bstack1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠥᣎ")
    bstack11ll111lll1_opy_ = bstack1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡤࡱࡧࡩࠧᣏ")
    bstack1l1111lll11_opy_ = bstack1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠧᣐ")
    bstack1l1l11l1ll1_opy_ = bstack1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧᣑ")
    bstack11lllll11l1_opy_ = bstack1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࠦᣒ")
    bstack11l1ll1ll11_opy_ = bstack1111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠥᣓ")
    bstack11ll1l11lll_opy_ = bstack1111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡲ࡯ࡨࡵࠥᣔ")
    bstack11ll11l1ll1_opy_ = bstack1111_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡭ࡦࡶࡤࠦᣕ")
    bstack11l1l1lll1l_opy_ = bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡴࡥࡲࡴࡪࡹࠧᣖ")
    bstack11ll1lll1l1_opy_ = bstack1111_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦᣗ")
    bstack11ll1111111_opy_ = bstack1111_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᣘ")
    bstack11ll111l111_opy_ = bstack1111_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡪࡴࡤࡦࡦࡢࡥࡹࠨᣙ")
    bstack11l1lll1l1l_opy_ = bstack1111_opy_ (u"ࠨࡨࡰࡱ࡮ࡣ࡮ࡪࠢᣚ")
    bstack11l1ll1l111_opy_ = bstack1111_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡸࡥࡴࡷ࡯ࡸࠧᣛ")
    bstack11l1ll11l11_opy_ = bstack1111_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡬ࡰࡩࡶࠦᣜ")
    bstack11ll1l1ll1l_opy_ = bstack1111_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠧᣝ")
    bstack11ll1l111l1_opy_ = bstack1111_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᣞ")
    bstack11ll1l1l11l_opy_ = bstack1111_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᣟ")
    bstack11l1ll11ll1_opy_ = bstack1111_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨᣠ")
    bstack11ll1l11l1l_opy_ = bstack1111_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢᣡ")
    KIND_SCREENSHOT = bstack1111_opy_ (u"ࠢࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠤᣢ")
    bstack1l111l1l1l1_opy_ = bstack1111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡌࡐࡉࠥᣣ")
    bstack1l11l111ll1_opy_ = bstack1111_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᣤ")
    bstack1lll1111lll_opy_: Dict[str, bstack1ll11ll111l_opy_] = dict()
    bstack11l1l111l11_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1ll111l11_opy_: List[str]
    bstack11ll11l1l1l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1ll111l11_opy_: List[str],
        bstack11ll11l1l1l_opy_: Dict[str, str],
        bstack1ll1lllll1l_opy_: bstack1lll1111111_opy_
    ):
        self.bstack1l1ll111l11_opy_ = bstack1l1ll111l11_opy_
        self.bstack11ll11l1l1l_opy_ = bstack11ll11l1l1l_opy_
        self.bstack1ll1lllll1l_opy_ = bstack1ll1lllll1l_opy_
    def track_event(
        self,
        context: bstack1lll1l1l1ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1111_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࢃࠢᣥ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11ll1111l11_opy_(
        self,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11ll1ll11ll_opy_ = TestFramework.bstack11ll1ll1l11_opy_(bstack1ll1ll1ll1l_opy_)
        if not bstack11ll1ll11ll_opy_ in TestFramework.bstack11l1l111l11_opy_:
            return
        self.logger.debug(bstack1111_opy_ (u"ࠦ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡻࡾࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠧᣦ").format(len(TestFramework.bstack11l1l111l11_opy_[bstack11ll1ll11ll_opy_])))
        for callback in TestFramework.bstack11l1l111l11_opy_[bstack11ll1ll11ll_opy_]:
            try:
                callback(self, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠧᣧ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l111l1ll11_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l11l11l111_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l11l11111l_opy_(self, instance, bstack1ll1ll1ll1l_opy_):
        return
    @abc.abstractmethod
    def bstack1l11l11ll11_opy_(self, instance, bstack1ll1ll1ll1l_opy_):
        return
    @staticmethod
    def bstack1ll1l1l1lll_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1ll1llll1l1_opy_.create_context(target)
        instance = TestFramework.bstack1lll1111lll_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll1l1l1l11_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l11l1llll1_opy_(reverse=True) -> List[bstack1ll11ll111l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lll1111lll_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1l1llll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l1ll11l_opy_(ctx: bstack1ll1ll11l11_opy_, reverse=True) -> List[bstack1ll11ll111l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lll1111lll_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1l1llll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(instance: bstack1ll11ll111l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lll1l11111_opy_(instance: bstack1ll11ll111l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll1l11l1l_opy_(instance: bstack1ll11ll111l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1111_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᣨ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1llll111_opy_(instance: bstack1ll11ll111l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1111_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡳࡺࡲࡪࡧࡶࡁࢀࢃࠢᣩ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11l1l11111l_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack1111_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣᣪ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1ll1l1l1lll_opy_(target, strict)
        return TestFramework.bstack1lll1l11111_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1ll1l1l1lll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11ll11ll11l_opy_(instance: bstack1ll11ll111l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11ll11111ll_opy_(instance: bstack1ll11ll111l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11ll1ll1l11_opy_(bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack1111_opy_ (u"ࠤ࠽ࠦᣫ").join((TestFrameworkState(bstack1ll1ll1ll1l_opy_[0]).name, TestHookState(bstack1ll1ll1ll1l_opy_[1]).name))
    @staticmethod
    def bstack1l1ll1111ll_opy_(bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11ll1ll11ll_opy_ = TestFramework.bstack11ll1ll1l11_opy_(bstack1ll1ll1ll1l_opy_)
        TestFramework.logger.debug(bstack1111_opy_ (u"ࠥࡷࡪࡺ࡟ࡩࡱࡲ࡯ࡤࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡪࡲࡳࡰࡥࡲࡦࡩ࡬ࡷࡹࡸࡹࡠ࡭ࡨࡽࡂࢁࡽࠣᣬ").format(bstack11ll1ll11ll_opy_))
        if not bstack11ll1ll11ll_opy_ in TestFramework.bstack11l1l111l11_opy_:
            TestFramework.bstack11l1l111l11_opy_[bstack11ll1ll11ll_opy_] = []
        TestFramework.bstack11l1l111l11_opy_[bstack11ll1ll11ll_opy_].append(callback)
    @staticmethod
    def bstack1l11l1l1111_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡶ࡬ࡲࡸࠨᣭ"):
            return klass.__qualname__
        return module + bstack1111_opy_ (u"ࠧ࠴ࠢᣮ") + klass.__qualname__
    @staticmethod
    def bstack1l111ll11ll_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}