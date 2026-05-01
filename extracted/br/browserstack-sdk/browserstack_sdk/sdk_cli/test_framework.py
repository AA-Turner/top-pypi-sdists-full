# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1l1ll1llll1_opy_ import bstack1l1lll1111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l1lll_opy_ import bstack1l1ll1l1l1l_opy_, bstack1l1ll1111l1_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack111ll_opy_ (u"ࠢࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᬵ").format(self.name)
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
        return bstack111ll_opy_ (u"ࠣࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᬶ").format(self.name)
class bstack1l1l1ll11l1_opy_(bstack1l1ll1l1l1l_opy_):
    bstack1l1l11l1111_opy_: List[str]
    bstack1l11llll11l_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1l1ll1111ll_opy_: datetime
    bstack1l1ll111l11_opy_: datetime
    def __init__(
        self,
        context: bstack1l1ll1111l1_opy_,
        bstack1l1l11l1111_opy_: List[str],
        bstack1l11llll11l_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l1l11l1111_opy_ = bstack1l1l11l1111_opy_
        self.bstack1l11llll11l_opy_ = bstack1l11llll11l_opy_
        self.state = state
        self.bstack1l1ll1111ll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1ll111l11_opy_ = datetime.now(tz=timezone.utc)
    def bstack11ll11l1_opy_(self, bstack1l1ll11111l_opy_: TestFrameworkState):
        bstack1l1l1llll11_opy_ = TestFrameworkState(bstack1l1ll11111l_opy_).name
        if not bstack1l1l1llll11_opy_:
            return False
        if bstack1l1ll11111l_opy_ == self.state:
            return False
        self.state = bstack1l1ll11111l_opy_
        self.bstack1l1ll111l11_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll1lllll1l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack11l1l1l1ll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack11ll1lll111_opy_: int = None
    bstack11ll11ll111_opy_: str = None
    bstack111l1_opy_: str = None
    bstack1lllllllll_opy_: str = None
    bstack11lll11ll1l_opy_: str = None
    bstack111llllll11_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l11111111l_opy_ = bstack111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧᬷ")
    bstack11l1l1ll11l_opy_ = bstack111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦᬸ")
    bstack1l1111lll11_opy_ = bstack111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠢᬹ")
    bstack11l1111l1ll_opy_ = bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭ࠨᬺ")
    bstack111ll1llll1_opy_ = bstack111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡹࡧࡧࡴࠤᬻ")
    bstack11l1ll11l11_opy_ = bstack111ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᬼ")
    bstack11lll11111l_opy_ = bstack111ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࡥࡡࡵࠤᬽ")
    bstack11ll1l1lll1_opy_ = bstack111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᬾ")
    bstack11lll11llll_opy_ = bstack111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᬿ")
    bstack11l1111l1l1_opy_ = bstack111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᭀ")
    bstack1l1111l111l_opy_ = bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠦᭁ")
    bstack11ll1l11l1l_opy_ = bstack111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᭂ")
    bstack111ll11l1ll_opy_ = bstack111ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡩ࡯ࡥࡧࠥᭃ")
    bstack11l1llll111_opy_ = bstack111ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧ᭄ࠥ")
    bstack1l111111111_opy_ = bstack111ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥᭅ")
    bstack11l1l1ll1ll_opy_ = bstack111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࠤᭆ")
    bstack111lll1l1l1_opy_ = bstack111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠣᭇ")
    bstack111lll1ll1l_opy_ = bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴ࡭ࡳࠣᭈ")
    bstack111ll111ll1_opy_ = bstack111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡲ࡫ࡴࡢࠤᭉ")
    bstack111ll111111_opy_ = bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡹࡣࡰࡲࡨࡷࠬᭊ")
    bstack11l11l1111l_opy_ = bstack111ll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᭋ")
    bstack111lll1llll_opy_ = bstack111ll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᭌ")
    bstack111llll1l11_opy_ = bstack111ll_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦ᭍")
    bstack111llll1111_opy_ = bstack111ll_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡬ࡨࠧ᭎")
    bstack111ll1l11l1_opy_ = bstack111ll_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡪࡹࡵ࡭ࡶࠥ᭏")
    bstack111ll11l111_opy_ = bstack111ll_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡱࡵࡧࡴࠤ᭐")
    bstack111ll11ll1l_opy_ = bstack111ll_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠥ᭑")
    bstack111ll111lll_opy_ = bstack111ll_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨ᭒")
    bstack11l11111l1l_opy_ = bstack111ll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦ᭓")
    bstack11l11111111_opy_ = bstack111ll_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦ᭔")
    bstack111lll1lll1_opy_ = bstack111ll_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ᭕")
    KIND_SCREENSHOT = bstack111ll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠢ᭖")
    bstack11ll1l1l1ll_opy_ = bstack111ll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡑࡕࡇࠣ᭗")
    bstack11ll111l1ll_opy_ = bstack111ll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤ᭘")
    bstack111l11l1l1_opy_: Dict[str, bstack1l1l1ll11l1_opy_] = dict()
    bstack111l1l1ll11_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11l1111_opy_: List[str]
    bstack1l11llll11l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1l11l1111_opy_: List[str],
        bstack1l11llll11l_opy_: Dict[str, str],
        bstack1l1ll1llll1_opy_: bstack1l1lll1111l_opy_
    ):
        self.bstack1l1l11l1111_opy_ = bstack1l1l11l1111_opy_
        self.bstack1l11llll11l_opy_ = bstack1l11llll11l_opy_
        self.bstack1l1ll1llll1_opy_ = bstack1l1ll1llll1_opy_
    def track_event(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack111ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧ᭙").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack111ll1l1l11_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l111l1l11_opy_ = TestFramework.bstack11l111ll1l1_opy_(bstack1l1l1lll11l_opy_)
        if not bstack11l111l1l11_opy_ in TestFramework.bstack111l1l1ll11_opy_:
            return
        self.logger.debug(bstack111ll_opy_ (u"ࠤ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠥ᭚").format(len(TestFramework.bstack111l1l1ll11_opy_[bstack11l111l1l11_opy_])))
        for callback in TestFramework.bstack111l1l1ll11_opy_[bstack11l111l1l11_opy_]:
            try:
                callback(self, instance, bstack1l1l1lll11l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack111ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠥ᭛").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack11ll1l111ll_opy_(self):
        return
    @abc.abstractmethod
    def bstack11ll1ll1l1l_opy_(self):
        return
    @abc.abstractmethod
    def bstack11lll111l1l_opy_(self, instance, bstack1l1l1lll11l_opy_):
        return
    @abc.abstractmethod
    def bstack11lll11l1ll_opy_(self, instance, bstack1l1l1lll11l_opy_):
        return
    @staticmethod
    def bstack1l1l1llllll_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1l1ll1l1l1l_opy_.create_context(target)
        instance = TestFramework.bstack111l11l1l1_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1ll1l1l11_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack11ll1l1111l_opy_(reverse=True) -> List[bstack1l1l1ll11l1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack111l11l1l1_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll1111ll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1ll11llll_opy_(ctx: bstack1l1ll1111l1_opy_, reverse=True) -> List[bstack1l1l1ll11l1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack111l11l1l1_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll1111ll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1lllll1l1_opy_(instance: bstack1l1l1ll11l1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1l1llll1111_opy_(instance: bstack1l1l1ll11l1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack11ll11l1_opy_(instance: bstack1l1l1ll11l1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack111ll_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣ᭜").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l11111l11_opy_(instance: bstack1l1l1ll11l1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack111ll_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡱࡸࡷ࡯ࡥࡴ࠿ࡾࢁࠧ᭝").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack111l1l111ll_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack111ll_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨ᭞").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1l1l1llllll_opy_(target, strict)
        return TestFramework.bstack1l1llll1111_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1l1l1llllll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack111ll1l1l1l_opy_(instance: bstack1l1l1ll11l1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack111ll1lllll_opy_(instance: bstack1l1l1ll11l1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11l111ll1l1_opy_(bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack111ll_opy_ (u"ࠢ࠻ࠤ᭟").join((TestFrameworkState(bstack1l1l1lll11l_opy_[0]).name, TestHookState(bstack1l1l1lll11l_opy_[1]).name))
    @staticmethod
    def bstack1l111l1111l_opy_(bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11l111l1l11_opy_ = TestFramework.bstack11l111ll1l1_opy_(bstack1l1l1lll11l_opy_)
        TestFramework.logger.debug(bstack111ll_opy_ (u"ࠣࡵࡨࡸࡤ࡮࡯ࡰ࡭ࡢࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡨࡰࡱ࡮ࡣࡷ࡫ࡧࡪࡵࡷࡶࡾࡥ࡫ࡦࡻࡀࡿࢂࠨ᭠").format(bstack11l111l1l11_opy_))
        if not bstack11l111l1l11_opy_ in TestFramework.bstack111l1l1ll11_opy_:
            TestFramework.bstack111l1l1ll11_opy_[bstack11l111l1l11_opy_] = []
        TestFramework.bstack111l1l1ll11_opy_[bstack11l111l1l11_opy_].append(callback)
    @staticmethod
    def bstack11ll1l11l11_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack111ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡴࡪࡰࡶࠦ᭡"):
            return klass.__qualname__
        return module + bstack111ll_opy_ (u"ࠥ࠲ࠧ᭢") + klass.__qualname__
    @staticmethod
    def bstack11lll1111ll_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}