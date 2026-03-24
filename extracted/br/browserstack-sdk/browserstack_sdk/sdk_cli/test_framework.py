# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1ll1l11l1l1_opy_ import bstack1ll1l111lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11111l_opy_ import bstack1ll11l1ll1l_opy_, bstack1ll11ll1ll1_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll1lll_opy_ (u"ࠨࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤ᦬").format(self.name)
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
        return bstack1ll1lll_opy_ (u"ࠢࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣ᦭").format(self.name)
class bstack1ll111lllll_opy_(bstack1ll11l1ll1l_opy_):
    bstack1l11ll1l1ll_opy_: List[str]
    bstack11l11lll11l_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1ll11llll1l_opy_: datetime
    bstack1ll11lllll1_opy_: datetime
    def __init__(
        self,
        context: bstack1ll11ll1ll1_opy_,
        bstack1l11ll1l1ll_opy_: List[str],
        bstack11l11lll11l_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l11ll1l1ll_opy_ = bstack1l11ll1l1ll_opy_
        self.bstack11l11lll11l_opy_ = bstack11l11lll11l_opy_
        self.state = state
        self.bstack1ll11llll1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll11lllll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1l1l11lll_opy_(self, bstack1ll11ll1l1l_opy_: TestFrameworkState):
        bstack1ll11l11l11_opy_ = TestFrameworkState(bstack1ll11ll1l1l_opy_).name
        if not bstack1ll11l11l11_opy_:
            return False
        if bstack1ll11ll1l1l_opy_ == self.state:
            return False
        self.state = bstack1ll11ll1l1l_opy_
        self.bstack1ll11lllll1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll1lll1l11_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1l1l1l1l1ll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l111llll1l_opy_: int = None
    bstack11lllll1ll1_opy_: str = None
    bstack1l11111_opy_: str = None
    bstack11l1l11l1_opy_: str = None
    bstack1l111l11l1l_opy_: str = None
    bstack11l1ll111ll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l1l1111l11_opy_ = bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠦ᦮")
    bstack11lll111lll_opy_ = bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡪࡦࠥ᦯")
    bstack1l1l111111l_opy_ = bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡰࡤࡱࡪࠨᦰ")
    bstack11l1l1l1111_opy_ = bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫࡟ࡱࡣࡷ࡬ࠧᦱ")
    bstack11l1l1l1lll_opy_ = bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡸࡦ࡭ࡳࠣᦲ")
    bstack11lll11ll11_opy_ = bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᦳ")
    bstack1l1111ll11l_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࡤࡧࡴࠣᦴ")
    bstack1l111ll11ll_opy_ = bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᦵ")
    bstack1l111ll1l11_opy_ = bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᦶ")
    bstack11l11ll1lll_opy_ = bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᦷ")
    bstack1l11lll111l_opy_ = bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠥᦸ")
    bstack1l1111l1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᦹ")
    bstack11l1l11l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡨࡵࡤࡦࠤᦺ")
    bstack11lllll1111_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠤᦻ")
    bstack1l11llll111_opy_ = bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᦼ")
    bstack11lll11ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠣᦽ")
    bstack11l1l1111ll_opy_ = bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠢᦾ")
    bstack11l1lllll11_opy_ = bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳ࡬ࡹࠢᦿ")
    bstack11l11ll1l11_opy_ = bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡱࡪࡺࡡࠣᧀ")
    bstack11l11ll111l_opy_ = bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡸࡩ࡯ࡱࡧࡶࠫᧁ")
    bstack11ll111llll_opy_ = bstack1ll1lll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᧂ")
    bstack11l11lllll1_opy_ = bstack1ll1lll_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᧃ")
    bstack11l1ll11111_opy_ = bstack1ll1lll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᧄ")
    bstack11l1lllll1l_opy_ = bstack1ll1lll_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡫ࡧࠦᧅ")
    bstack11l1ll1l11l_opy_ = bstack1ll1lll_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡩࡸࡻ࡬ࡵࠤᧆ")
    bstack11l1l11ll11_opy_ = bstack1ll1lll_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡰࡴ࡭ࡳࠣᧇ")
    bstack11l1l1l1l1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠤᧈ")
    bstack11l1ll1ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᧉ")
    bstack11l11lll1ll_opy_ = bstack1ll1lll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥ᧊")
    bstack11l1llll111_opy_ = bstack1ll1lll_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥ᧋")
    bstack11l1l1lll11_opy_ = bstack1ll1lll_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦ᧌")
    KIND_SCREENSHOT = bstack1ll1lll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙ࠨ᧍")
    bstack1l111lll1ll_opy_ = bstack1ll1lll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡐࡔࡍࠢ᧎")
    bstack1l1111l1l1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ᧏")
    bstack111llll1l_opy_: Dict[str, bstack1ll111lllll_opy_] = dict()
    bstack11l111l11l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11ll1l1ll_opy_: List[str]
    bstack11l11lll11l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l11ll1l1ll_opy_: List[str],
        bstack11l11lll11l_opy_: Dict[str, str],
        bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_
    ):
        self.bstack1l11ll1l1ll_opy_ = bstack1l11ll1l1ll_opy_
        self.bstack11l11lll11l_opy_ = bstack11l11lll11l_opy_
        self.bstack1ll1l11l1l1_opy_ = bstack1ll1l11l1l1_opy_
    def track_event(
        self,
        context: bstack1ll1lll1l11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡢࡴࡪࡷࡂࢁࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽࢀࠦ᧐").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11l1ll1l1ll_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11ll111l11l_opy_ = TestFramework.bstack11ll1111ll1_opy_(bstack1ll11l1ll11_opy_)
        if not bstack11ll111l11l_opy_ in TestFramework.bstack11l111l11l1_opy_:
            return
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠣ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡿࢂࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠤ᧑").format(len(TestFramework.bstack11l111l11l1_opy_[bstack11ll111l11l_opy_])))
        for callback in TestFramework.bstack11l111l11l1_opy_[bstack11ll111l11l_opy_]:
            try:
                callback(self, instance, bstack1ll11l1ll11_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠤ᧒").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1111111ll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l111lll11l_opy_(self):
        return
    @abc.abstractmethod
    def bstack11llllll111_opy_(self, instance, bstack1ll11l1ll11_opy_):
        return
    @abc.abstractmethod
    def bstack1l111l1111l_opy_(self, instance, bstack1ll11l1ll11_opy_):
        return
    @staticmethod
    def bstack1ll1l111l1l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1ll11l1ll1l_opy_.create_context(target)
        instance = TestFramework.bstack111llll1l_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll11l11111_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l111l1llll_opy_(reverse=True) -> List[bstack1ll111lllll_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack111llll1l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll11llll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll11l11ll1_opy_(ctx: bstack1ll11ll1ll1_opy_, reverse=True) -> List[bstack1ll111lllll_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack111llll1l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll11llll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(instance: bstack1ll111lllll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll1lll11ll_opy_(instance: bstack1ll111lllll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1l1l11lll_opy_(instance: bstack1ll111lllll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢ᧓").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1l11l1ll_opy_(instance: bstack1ll111lllll_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠࡦࡰࡷࡶ࡮࡫ࡳ࠾ࡽࢀࠦ᧔").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11l111l111l_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧ᧕").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1ll1l111l1l_opy_(target, strict)
        return TestFramework.bstack1ll1lll11ll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1ll1l111l1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l11ll1ll1_opy_(instance: bstack1ll111lllll_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11l1l111111_opy_(instance: bstack1ll111lllll_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11ll1111ll1_opy_(bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack1ll1lll_opy_ (u"ࠨ࠺ࠣ᧖").join((TestFrameworkState(bstack1ll11l1ll11_opy_[0]).name, TestHookState(bstack1ll11l1ll11_opy_[1]).name))
    @staticmethod
    def bstack1l11l1lllll_opy_(bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11ll111l11l_opy_ = TestFramework.bstack11ll1111ll1_opy_(bstack1ll11l1ll11_opy_)
        TestFramework.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡴࡧࡷࡣ࡭ࡵ࡯࡬ࡡࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥ࡮࡯ࡰ࡭ࡢࡶࡪ࡭ࡩࡴࡶࡵࡽࡤࡱࡥࡺ࠿ࡾࢁࠧ᧗").format(bstack11ll111l11l_opy_))
        if not bstack11ll111l11l_opy_ in TestFramework.bstack11l111l11l1_opy_:
            TestFramework.bstack11l111l11l1_opy_[bstack11ll111l11l_opy_] = []
        TestFramework.bstack11l111l11l1_opy_[bstack11ll111l11l_opy_].append(callback)
    @staticmethod
    def bstack1l111l111ll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1ll1lll_opy_ (u"ࠣࡤࡸ࡭ࡱࡺࡩ࡯ࡵࠥ᧘"):
            return klass.__qualname__
        return module + bstack1ll1lll_opy_ (u"ࠤ࠱ࠦ᧙") + klass.__qualname__
    @staticmethod
    def bstack1l111l11lll_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}