# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1lll111111l_opy_ import bstack1ll1lllll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll11ll_opy_ import bstack1ll1ll1l1ll_opy_, bstack1ll1ll11lll_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1lll1l_opy_ (u"ࠣࡖࡨࡷࡹࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᣀ").format(self.name)
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
        return bstack1lll1l_opy_ (u"ࠤࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᣁ").format(self.name)
class bstack1ll111l1l1l_opy_(bstack1ll1ll1l1ll_opy_):
    bstack1l1l1ll1l1l_opy_: List[str]
    bstack11l1llll1ll_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1ll1lll1111_opy_: datetime
    bstack1ll1ll1lll1_opy_: datetime
    def __init__(
        self,
        context: bstack1ll1ll11lll_opy_,
        bstack1l1l1ll1l1l_opy_: List[str],
        bstack11l1llll1ll_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l1l1ll1l1l_opy_ = bstack1l1l1ll1l1l_opy_
        self.bstack11l1llll1ll_opy_ = bstack11l1llll1ll_opy_
        self.state = state
        self.bstack1ll1lll1111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll1ll1lll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll1l11lll_opy_(self, bstack1ll1l1ll1ll_opy_: TestFrameworkState):
        bstack1ll1lll1lll_opy_ = TestFrameworkState(bstack1ll1l1ll1ll_opy_).name
        if not bstack1ll1lll1lll_opy_:
            return False
        if bstack1ll1l1ll1ll_opy_ == self.state:
            return False
        self.state = bstack1ll1l1ll1ll_opy_
        self.bstack1ll1ll1lll1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1lll1l11l1l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll11ll1l1l_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l11l11llll_opy_: int = None
    bstack1l111l1l11l_opy_: str = None
    bstack1ll11ll_opy_: str = None
    bstack1ll11lllll_opy_: str = None
    bstack1l111llll1l_opy_: str = None
    bstack11ll11l111l_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l1l1l1ll1l_opy_ = bstack1lll1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨᣂ")
    bstack11lllll1111_opy_ = bstack1lll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧᣃ")
    bstack1l1l111llll_opy_ = bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡲࡦࡳࡥࠣᣄ")
    bstack11ll111lll1_opy_ = bstack1lll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠢᣅ")
    bstack11l1lllll1l_opy_ = bstack1lll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡺࡡࡨࡵࠥᣆ")
    bstack1l1111111l1_opy_ = bstack1lll1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࠨᣇ")
    bstack1l11l1l11ll_opy_ = bstack1lll1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺ࡟ࡢࡶࠥᣈ")
    bstack1l111l11l1l_opy_ = bstack1lll1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᣉ")
    bstack1l11l11ll1l_opy_ = bstack1lll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᣊ")
    bstack11ll11lll11_opy_ = bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᣋ")
    bstack1l1l111ll1l_opy_ = bstack1lll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠧᣌ")
    bstack1l11l11l1ll_opy_ = bstack1lll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᣍ")
    bstack11ll1l11ll1_opy_ = bstack1lll1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡣࡰࡦࡨࠦᣎ")
    bstack1l1111ll1l1_opy_ = bstack1lll1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠦᣏ")
    bstack1l1l1lll111_opy_ = bstack1lll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦᣐ")
    bstack11llllll1l1_opy_ = bstack1lll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࠥᣑ")
    bstack11ll111ll11_opy_ = bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠤᣒ")
    bstack11l1ll11l1l_opy_ = bstack1lll1l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡧࡴࠤᣓ")
    bstack11ll11lllll_opy_ = bstack1lll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡳࡥࡵࡣࠥᣔ")
    bstack11l1ll11111_opy_ = bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡳࡤࡱࡳࡩࡸ࠭ᣕ")
    bstack11lll1111l1_opy_ = bstack1lll1l_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᣖ")
    bstack11ll1l1l1ll_opy_ = bstack1lll1l_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᣗ")
    bstack11l1llll1l1_opy_ = bstack1lll1l_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧᣘ")
    bstack11ll1111lll_opy_ = bstack1lll1l_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢ࡭ࡩࠨᣙ")
    bstack11l1llll11l_opy_ = bstack1lll1l_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷ࡫ࡳࡶ࡮ࡷࠦᣚ")
    bstack11ll1l111l1_opy_ = bstack1lll1l_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡲ࡯ࡨࡵࠥᣛ")
    bstack11ll1111l1l_opy_ = bstack1lll1l_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠦᣜ")
    bstack11l1ll11ll1_opy_ = bstack1lll1l_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᣝ")
    bstack11ll11l11ll_opy_ = bstack1lll1l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᣞ")
    bstack11l1ll1llll_opy_ = bstack1lll1l_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧᣟ")
    bstack11ll11ll1ll_opy_ = bstack1lll1l_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨᣠ")
    KIND_SCREENSHOT = bstack1lll1l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠣᣡ")
    bstack1l111l1l1ll_opy_ = bstack1lll1l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡒࡏࡈࠤᣢ")
    bstack1l11l1l1ll1_opy_ = bstack1lll1l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᣣ")
    bstack1lll1l1111l_opy_: Dict[str, bstack1ll111l1l1l_opy_] = dict()
    bstack11l1l11l111_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l1ll1l1l_opy_: List[str]
    bstack11l1llll1ll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1l1ll1l1l_opy_: List[str],
        bstack11l1llll1ll_opy_: Dict[str, str],
        bstack1lll111111l_opy_: bstack1ll1lllll1l_opy_
    ):
        self.bstack1l1l1ll1l1l_opy_ = bstack1l1l1ll1l1l_opy_
        self.bstack11l1llll1ll_opy_ = bstack11l1llll1ll_opy_
        self.bstack1lll111111l_opy_ = bstack1lll111111l_opy_
    def track_event(
        self,
        context: bstack1lll1l11l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࢂࠨᣤ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11l1ll1l11l_opy_(
        self,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11ll1lll1ll_opy_ = TestFramework.bstack11ll1ll1lll_opy_(bstack1ll1ll1ll1l_opy_)
        if not bstack11ll1lll1ll_opy_ in TestFramework.bstack11l1l11l111_opy_:
            return
        self.logger.debug(bstack1lll1l_opy_ (u"ࠥ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࢁࡽࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠦᣥ").format(len(TestFramework.bstack11l1l11l111_opy_[bstack11ll1lll1ll_opy_])))
        for callback in TestFramework.bstack11l1l11l111_opy_[bstack11ll1lll1ll_opy_]:
            try:
                callback(self, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1lll1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠦᣦ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l11l111lll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l11l1l11l1_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l11ll1l11l_opy_(self, instance, bstack1ll1ll1ll1l_opy_):
        return
    @abc.abstractmethod
    def bstack1l11l1lll11_opy_(self, instance, bstack1ll1ll1ll1l_opy_):
        return
    @staticmethod
    def bstack1ll1l1l111l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1ll1ll1l1ll_opy_.create_context(target)
        instance = TestFramework.bstack1lll1l1111l_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll1llll1l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l111ll1l11_opy_(reverse=True) -> List[bstack1ll111l1l1l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lll1l1111l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1lll1111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1lll1l1l_opy_(ctx: bstack1ll1ll11lll_opy_, reverse=True) -> List[bstack1ll111l1l1l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lll1l1111l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1lll1111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l1l1l1l_opy_(instance: bstack1ll111l1l1l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lll111l1l1_opy_(instance: bstack1ll111l1l1l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll1l11lll_opy_(instance: bstack1ll111l1l1l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1lll1l_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡬ࡧࡼࡁࢀࢃࠠࡷࡣ࡯ࡹࡪࡃࡻࡾࠤᣧ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11ll1l111ll_opy_(instance: bstack1ll111l1l1l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1lll1l_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡲࡹࡸࡩࡦࡵࡀࡿࢂࠨᣨ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11l1l1111ll_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack1lll1l_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢᣩ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1ll1l1l111l_opy_(target, strict)
        return TestFramework.bstack1lll111l1l1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1ll1l1l111l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11ll1l11l1l_opy_(instance: bstack1ll111l1l1l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11ll111111l_opy_(instance: bstack1ll111l1l1l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11ll1ll1lll_opy_(bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack1lll1l_opy_ (u"ࠣ࠼ࠥᣪ").join((TestFrameworkState(bstack1ll1ll1ll1l_opy_[0]).name, TestHookState(bstack1ll1ll1ll1l_opy_[1]).name))
    @staticmethod
    def bstack1l1l1lll1ll_opy_(bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11ll1lll1ll_opy_ = TestFramework.bstack11ll1ll1lll_opy_(bstack1ll1ll1ll1l_opy_)
        TestFramework.logger.debug(bstack1lll1l_opy_ (u"ࠤࡶࡩࡹࡥࡨࡰࡱ࡮ࡣࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡩࡱࡲ࡯ࡤࡸࡥࡨ࡫ࡶࡸࡷࡿ࡟࡬ࡧࡼࡁࢀࢃࠢᣫ").format(bstack11ll1lll1ll_opy_))
        if not bstack11ll1lll1ll_opy_ in TestFramework.bstack11l1l11l111_opy_:
            TestFramework.bstack11l1l11l111_opy_[bstack11ll1lll1ll_opy_] = []
        TestFramework.bstack11l1l11l111_opy_[bstack11ll1lll1ll_opy_].append(callback)
    @staticmethod
    def bstack1l11l11l111_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡵ࡫ࡱࡷࠧᣬ"):
            return klass.__qualname__
        return module + bstack1lll1l_opy_ (u"ࠦ࠳ࠨᣭ") + klass.__qualname__
    @staticmethod
    def bstack1l111l1l1l1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}