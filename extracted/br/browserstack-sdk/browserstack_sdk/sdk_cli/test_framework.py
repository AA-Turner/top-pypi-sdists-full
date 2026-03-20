# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
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
from browserstack_sdk.sdk_cli.bstack1ll1l11l1l1_opy_ import bstack1ll1l111lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll11ll1111_opy_, bstack1ll11lll1ll_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11lll1_opy_ (u"ࠥࡘࡪࡹࡴࡉࡱࡲ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᦩ").format(self.name)
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
        return bstack11lll1_opy_ (u"࡙ࠦ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᦪ").format(self.name)
class bstack1ll111l1111_opy_(bstack1ll11ll1111_opy_):
    bstack1l11ll1l11l_opy_: List[str]
    bstack11l1llll111_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1ll1l111l1l_opy_: datetime
    bstack1ll11l11111_opy_: datetime
    def __init__(
        self,
        context: bstack1ll11lll1ll_opy_,
        bstack1l11ll1l11l_opy_: List[str],
        bstack11l1llll111_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l11ll1l11l_opy_ = bstack1l11ll1l11l_opy_
        self.bstack11l1llll111_opy_ = bstack11l1llll111_opy_
        self.state = state
        self.bstack1ll1l111l1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll11l11111_opy_ = datetime.now(tz=timezone.utc)
    def bstack1ll1ll1l1l_opy_(self, bstack1ll11l111ll_opy_: TestFrameworkState):
        bstack1ll11lll111_opy_ = TestFrameworkState(bstack1ll11l111ll_opy_).name
        if not bstack1ll11lll111_opy_:
            return False
        if bstack1ll11l111ll_opy_ == self.state:
            return False
        self.state = bstack1ll11l111ll_opy_
        self.bstack1ll11l11111_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll1ll111ll_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1l1ll1111ll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l11111111l_opy_: int = None
    bstack1l1111l1111_opy_: str = None
    bstack11111l1_opy_: str = None
    bstack1l11l1lll_opy_: str = None
    bstack1l111l111ll_opy_: str = None
    bstack11l1l11ll11_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l11llll11l_opy_ = bstack11lll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠣᦫ")
    bstack11lll111lll_opy_ = bstack11lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡮ࡪࠢ᦬")
    bstack1l11ll1llll_opy_ = bstack11lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠥ᦭")
    bstack11l1lll1111_opy_ = bstack11lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡣࡵࡧࡴࡩࠤ᦮")
    bstack11l1ll1l11l_opy_ = bstack11lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡵࡣࡪࡷࠧ᦯")
    bstack11lll11111l_opy_ = bstack11lll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡷࡺࡲࡴࠣᦰ")
    bstack1l111l1ll11_opy_ = bstack11lll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࡡࡤࡸࠧᦱ")
    bstack1l111l1llll_opy_ = bstack11lll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᦲ")
    bstack1l111l1111l_opy_ = bstack11lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡪࡴࡤࡦࡦࡢࡥࡹࠨᦳ")
    bstack11l11lll11l_opy_ = bstack11lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠢᦴ")
    bstack1l11lll111l_opy_ = bstack11lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠢᦵ")
    bstack1l111l11lll_opy_ = bstack11lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠦᦶ")
    bstack11l1l111l11_opy_ = bstack11lll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡥࡲࡨࡪࠨᦷ")
    bstack11lllll1111_opy_ = bstack11lll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪࠨᦸ")
    bstack1l11lll1ll1_opy_ = bstack11lll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࠨᦹ")
    bstack11lll1l1111_opy_ = bstack11lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡧࡩ࡭ࡷࡵࡩࠧᦺ")
    bstack11l11llll11_opy_ = bstack11lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠦᦻ")
    bstack11l1l11ll1l_opy_ = bstack11lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡩࡶࠦᦼ")
    bstack11l1lll1l11_opy_ = bstack11lll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡮ࡧࡷࡥࠧᦽ")
    bstack11l11ll1l11_opy_ = bstack11lll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡵࡦࡳࡵ࡫ࡳࠨᦾ")
    bstack11ll11ll11l_opy_ = bstack11lll1_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟࡯ࡣࡰࡩࠧᦿ")
    bstack11l1ll1l1ll_opy_ = bstack11lll1_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᧀ")
    bstack11l1l1l11l1_opy_ = bstack11lll1_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᧁ")
    bstack11l1l1ll11l_opy_ = bstack11lll1_opy_ (u"ࠢࡩࡱࡲ࡯ࡤ࡯ࡤࠣᧂ")
    bstack11l1ll1ll1l_opy_ = bstack11lll1_opy_ (u"ࠣࡪࡲࡳࡰࡥࡲࡦࡵࡸࡰࡹࠨᧃ")
    bstack11l1llllll1_opy_ = bstack11lll1_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟࡭ࡱࡪࡷࠧᧄ")
    bstack11l1lll11ll_opy_ = bstack11lll1_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪࠨᧅ")
    bstack11l1l1ll1l1_opy_ = bstack11lll1_opy_ (u"ࠦࡱࡵࡧࡴࠤᧆ")
    bstack11l1l1l1111_opy_ = bstack11lll1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠢᧇ")
    bstack11l11ll1lll_opy_ = bstack11lll1_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢᧈ")
    bstack11l1l111ll1_opy_ = bstack11lll1_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᧉ")
    KIND_SCREENSHOT = bstack11lll1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠥ᧊")
    bstack11lllll1l11_opy_ = bstack11lll1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡍࡑࡊࠦ᧋")
    bstack1l111ll1ll1_opy_ = bstack11lll1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧ᧌")
    bstack11l1lll111_opy_: Dict[str, bstack1ll111l1111_opy_] = dict()
    bstack11l111lll1l_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11ll1l11l_opy_: List[str]
    bstack11l1llll111_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l11ll1l11l_opy_: List[str],
        bstack11l1llll111_opy_: Dict[str, str],
        bstack1ll1l11l1l1_opy_: bstack1ll1l111lll_opy_
    ):
        self.bstack1l11ll1l11l_opy_ = bstack1l11ll1l11l_opy_
        self.bstack11l1llll111_opy_ = bstack11l1llll111_opy_
        self.bstack1ll1l11l1l1_opy_ = bstack1ll1l11l1l1_opy_
    def track_event(
        self,
        context: bstack1ll1ll111ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11lll1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡦࡸࡧࡴ࠿ࡾࢁࠥࡱࡷࡢࡴࡪࡷࡂࢁࡽࠣ᧍").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11l1ll1l111_opy_(
        self,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11ll11111ll_opy_ = TestFramework.bstack11ll1111l11_opy_(bstack1ll1l111111_opy_)
        if not bstack11ll11111ll_opy_ in TestFramework.bstack11l111lll1l_opy_:
            return
        self.logger.debug(bstack11lll1_opy_ (u"ࠧ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡼࡿࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸࠨ᧎").format(len(TestFramework.bstack11l111lll1l_opy_[bstack11ll11111ll_opy_])))
        for callback in TestFramework.bstack11l111lll1l_opy_[bstack11ll11111ll_opy_]:
            try:
                callback(self, instance, bstack1ll1l111111_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11lll1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࡿࢂࠨ᧏").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l111ll1l11_opy_(self):
        return
    @abc.abstractmethod
    def bstack11lllll1l1l_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1111111l1_opy_(self, instance, bstack1ll1l111111_opy_):
        return
    @abc.abstractmethod
    def bstack1l1111llll1_opy_(self, instance, bstack1ll1l111111_opy_):
        return
    @staticmethod
    def bstack1ll11l11l11_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1ll11ll1111_opy_.create_context(target)
        instance = TestFramework.bstack11l1lll111_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll11lll1l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l111l1l11l_opy_(reverse=True) -> List[bstack1ll111l1111_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack11l1lll111_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1l111l1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll11lllll1_opy_(ctx: bstack1ll11lll1ll_opy_, reverse=True) -> List[bstack1ll111l1111_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack11l1lll111_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1l111l1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1lll1l11_opy_(instance: bstack1ll111l1111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll1l1l1111_opy_(instance: bstack1ll111l1111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1ll1ll1l1l_opy_(instance: bstack1ll111l1111_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11lll1_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢ࡮ࡩࡾࡃࡻࡾࠢࡹࡥࡱࡻࡥ࠾ࡽࢀࠦ᧐").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1l11lll1_opy_(instance: bstack1ll111l1111_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11lll1_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡪࡴࡴࡳ࡫ࡨࡷࡂࢁࡽࠣ᧑").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11l111l1l11_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack11lll1_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡬ࡧࡼࡁࢀࢃࠠࡷࡣ࡯ࡹࡪࡃࡻࡾࠤ᧒").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1ll11l11l11_opy_(target, strict)
        return TestFramework.bstack1ll1l1l1111_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1ll11l11l11_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1l1lll11_opy_(instance: bstack1ll111l1111_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11l1l1l1l11_opy_(instance: bstack1ll111l1111_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11ll1111l11_opy_(bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack11lll1_opy_ (u"ࠥ࠾ࠧ᧓").join((TestFrameworkState(bstack1ll1l111111_opy_[0]).name, TestHookState(bstack1ll1l111111_opy_[1]).name))
    @staticmethod
    def bstack1l1l111lll1_opy_(bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11ll11111ll_opy_ = TestFramework.bstack11ll1111l11_opy_(bstack1ll1l111111_opy_)
        TestFramework.logger.debug(bstack11lll1_opy_ (u"ࠦࡸ࡫ࡴࡠࡪࡲࡳࡰࡥࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢ࡫ࡳࡴࡱ࡟ࡳࡧࡪ࡭ࡸࡺࡲࡺࡡ࡮ࡩࡾࡃࡻࡾࠤ᧔").format(bstack11ll11111ll_opy_))
        if not bstack11ll11111ll_opy_ in TestFramework.bstack11l111lll1l_opy_:
            TestFramework.bstack11l111lll1l_opy_[bstack11ll11111ll_opy_] = []
        TestFramework.bstack11l111lll1l_opy_[bstack11ll11111ll_opy_].append(callback)
    @staticmethod
    def bstack1l1111lll1l_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11lll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡷ࡭ࡳࡹࠢ᧕"):
            return klass.__qualname__
        return module + bstack11lll1_opy_ (u"ࠨ࠮ࠣ᧖") + klass.__qualname__
    @staticmethod
    def bstack1l1111ll111_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}