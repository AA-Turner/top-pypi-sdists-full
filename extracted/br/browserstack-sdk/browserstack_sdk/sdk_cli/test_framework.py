# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1l1lll11l11_opy_ import bstack1l1lll11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11ll1l_opy_ import bstack1l1ll11l1l1_opy_, bstack1l1ll11lll1_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll1l11_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᬈ").format(self.name)
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
        return bstack1ll1l11_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᬉ").format(self.name)
class bstack1l11l1ll1ll_opy_(bstack1l1ll11l1l1_opy_):
    bstack1l111llllll_opy_: List[str]
    bstack1l1l1l1l111_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1l1ll1l1lll_opy_: datetime
    bstack1l1ll1l111l_opy_: datetime
    def __init__(
        self,
        context: bstack1l1ll11lll1_opy_,
        bstack1l111llllll_opy_: List[str],
        bstack1l1l1l1l111_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l111llllll_opy_ = bstack1l111llllll_opy_
        self.bstack1l1l1l1l111_opy_ = bstack1l1l1l1l111_opy_
        self.state = state
        self.bstack1l1ll1l1lll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1ll1l111l_opy_ = datetime.now(tz=timezone.utc)
    def bstack1ll11l1ll_opy_(self, bstack1l1ll111l1l_opy_: TestFrameworkState):
        bstack1l1ll1ll111_opy_ = TestFrameworkState(bstack1l1ll111l1l_opy_).name
        if not bstack1l1ll1ll111_opy_:
            return False
        if bstack1l1ll111l1l_opy_ == self.state:
            return False
        self.state = bstack1l1ll111l1l_opy_
        self.bstack1l1ll1l111l_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1lll11l111l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack111l1111l_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack11lll1l111l_opy_: int = None
    bstack11ll1l1l1l1_opy_: str = None
    bstack11ll_opy_: str = None
    bstack1l1l1l1l_opy_: str = None
    bstack11ll1ll1l1l_opy_: str = None
    bstack11l111l1l11_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l111l1lll1_opy_ = bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤᬊ")
    bstack11l1ll1llll_opy_ = bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᬋ")
    bstack1l111ll11l1_opy_ = bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦᬌ")
    bstack11l1111ll11_opy_ = bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥᬍ")
    bstack111ll1l111l_opy_ = bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨᬎ")
    bstack11l1ll1ll11_opy_ = bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᬏ")
    bstack11ll1lll1ll_opy_ = bstack1ll1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨᬐ")
    bstack11ll1l1ll11_opy_ = bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᬑ")
    bstack11lll1111ll_opy_ = bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᬒ")
    bstack111ll1l1l11_opy_ = bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᬓ")
    bstack11llllll1l1_opy_ = bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣᬔ")
    bstack11ll11l11l1_opy_ = bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᬕ")
    bstack111lll11111_opy_ = bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢᬖ")
    bstack11ll111ll11_opy_ = bstack1ll1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢᬗ")
    bstack1l111ll1l1l_opy_ = bstack1ll1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᬘ")
    bstack11l1ll11l1l_opy_ = bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨᬙ")
    bstack111llllll1l_opy_ = bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧᬚ")
    bstack111llll1l1l_opy_ = bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧᬛ")
    bstack111ll1ll111_opy_ = bstack1ll1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨᬜ")
    bstack111ll1l1111_opy_ = bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩᬝ")
    bstack11l11l1l11l_opy_ = bstack1ll1l11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᬞ")
    bstack111ll1llll1_opy_ = bstack1ll1l11_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᬟ")
    bstack111llll11ll_opy_ = bstack1ll1l11_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᬠ")
    bstack111llll111l_opy_ = bstack1ll1l11_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤᬡ")
    bstack11l1111llll_opy_ = bstack1ll1l11_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢᬢ")
    bstack111ll1l1lll_opy_ = bstack1ll1l11_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨᬣ")
    bstack111ll1l11l1_opy_ = bstack1ll1l11_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢᬤ")
    bstack111lll111l1_opy_ = bstack1ll1l11_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᬥ")
    bstack11l1111111l_opy_ = bstack1ll1l11_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᬦ")
    bstack11l111l11ll_opy_ = bstack1ll1l11_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᬧ")
    bstack11l1111l1l1_opy_ = bstack1ll1l11_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᬨ")
    KIND_SCREENSHOT = bstack1ll1l11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦᬩ")
    bstack11lll11l111_opy_ = bstack1ll1l11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧᬪ")
    bstack11ll1l11l11_opy_ = bstack1ll1l11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᬫ")
    bstack11l111111_opy_: Dict[str, bstack1l11l1ll1ll_opy_] = dict()
    bstack111l1ll1lll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l111llllll_opy_: List[str]
    bstack1l1l1l1l111_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l111llllll_opy_: List[str],
        bstack1l1l1l1l111_opy_: Dict[str, str],
        bstack1l1lll11l11_opy_: bstack1l1lll11ll1_opy_
    ):
        self.bstack1l111llllll_opy_ = bstack1l111llllll_opy_
        self.bstack1l1l1l1l111_opy_ = bstack1l1l1l1l111_opy_
        self.bstack1l1lll11l11_opy_ = bstack1l1lll11l11_opy_
    def track_event(
        self,
        context: bstack1lll11l111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤᬬ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack111llllllll_opy_(
        self,
        instance: bstack1l11l1ll1ll_opy_,
        bstack1l1ll1ll1ll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l11l11l11_opy_ = TestFramework.bstack11l11l1l111_opy_(bstack1l1ll1ll1ll_opy_)
        if not bstack11l11l11l11_opy_ in TestFramework.bstack111l1ll1lll_opy_:
            return
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢᬭ").format(len(TestFramework.bstack111l1ll1lll_opy_[bstack11l11l11l11_opy_])))
        for callback in TestFramework.bstack111l1ll1lll_opy_[bstack11l11l11l11_opy_]:
            try:
                callback(self, instance, bstack1l1ll1ll1ll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll1l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢᬮ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack11ll1l11lll_opy_(self):
        return
    @abc.abstractmethod
    def bstack11ll1lll1l1_opy_(self):
        return
    @abc.abstractmethod
    def bstack11ll1l1l1ll_opy_(self, instance, bstack1l1ll1ll1ll_opy_):
        return
    @abc.abstractmethod
    def bstack11lll11ll1l_opy_(self, instance, bstack1l1ll1ll1ll_opy_):
        return
    @staticmethod
    def bstack1l1ll1l1l1l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1l1ll11l1l1_opy_.create_context(target)
        instance = TestFramework.bstack11l111111_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1ll1lll11_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack11ll1l111ll_opy_(reverse=True) -> List[bstack1l11l1ll1ll_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack11l111111_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll1l1lll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1ll11l1ll_opy_(ctx: bstack1l1ll11lll1_opy_, reverse=True) -> List[bstack1l11l1ll1ll_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack11l111111_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll1l1lll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1llll1111_opy_(instance: bstack1l11l1ll1ll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1l1lll1ll11_opy_(instance: bstack1l11l1ll1ll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1ll11l1ll_opy_(instance: bstack1l11l1ll1ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᬯ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l111lll1l_opy_(instance: bstack1l11l1ll1ll_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤᬰ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack111l1ll1111_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᬱ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1l1ll1l1l1l_opy_(target, strict)
        return TestFramework.bstack1l1lll1ll11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1l1ll1l1l1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack111llll1ll1_opy_(instance: bstack1l11l1ll1ll_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack111lllll1l1_opy_(instance: bstack1l11l1ll1ll_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11l11l1l111_opy_(bstack1l1ll1ll1ll_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack1ll1l11_opy_ (u"ࠦ࠿ࠨᬲ").join((TestFrameworkState(bstack1l1ll1ll1ll_opy_[0]).name, TestHookState(bstack1l1ll1ll1ll_opy_[1]).name))
    @staticmethod
    def bstack1l1111ll11l_opy_(bstack1l1ll1ll1ll_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11l11l11l11_opy_ = TestFramework.bstack11l11l1l111_opy_(bstack1l1ll1ll1ll_opy_)
        TestFramework.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥᬳ").format(bstack11l11l11l11_opy_))
        if not bstack11l11l11l11_opy_ in TestFramework.bstack111l1ll1lll_opy_:
            TestFramework.bstack111l1ll1lll_opy_[bstack11l11l11l11_opy_] = []
        TestFramework.bstack111l1ll1lll_opy_[bstack11l11l11l11_opy_].append(callback)
    @staticmethod
    def bstack11ll1ll1l11_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳ᬴ࠣ"):
            return klass.__qualname__
        return module + bstack1ll1l11_opy_ (u"ࠢ࠯ࠤᬵ") + klass.__qualname__
    @staticmethod
    def bstack11ll1l1111l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}