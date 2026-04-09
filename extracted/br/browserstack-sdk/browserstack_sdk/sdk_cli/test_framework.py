# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1l1lll11ll1_opy_ import bstack1l1lll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1l1ll11111l_opy_, bstack1l1ll1l1l1l_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11ll11_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᬈ").format(self.name)
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
        return bstack11ll11_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᬉ").format(self.name)
class bstack1l1l111ll1l_opy_(bstack1l1ll11111l_opy_):
    bstack1l1l11l1l11_opy_: List[str]
    bstack1l1l1ll111l_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1l1ll1lll1l_opy_: datetime
    bstack1l1ll1111l1_opy_: datetime
    def __init__(
        self,
        context: bstack1l1ll1l1l1l_opy_,
        bstack1l1l11l1l11_opy_: List[str],
        bstack1l1l1ll111l_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l1l11l1l11_opy_ = bstack1l1l11l1l11_opy_
        self.bstack1l1l1ll111l_opy_ = bstack1l1l1ll111l_opy_
        self.state = state
        self.bstack1l1ll1lll1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1ll1111l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1l1l1111l1_opy_(self, bstack1l1ll1l1l11_opy_: TestFrameworkState):
        bstack1l1ll1111ll_opy_ = TestFrameworkState(bstack1l1ll1l1l11_opy_).name
        if not bstack1l1ll1111ll_opy_:
            return False
        if bstack1l1ll1l1l11_opy_ == self.state:
            return False
        self.state = bstack1l1ll1l1l11_opy_
        self.bstack1l1ll1111l1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll1ll1ll1l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1111lll111_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack11lll1111l1_opy_: int = None
    bstack11ll1llllll_opy_: str = None
    bstack1l1l1l1_opy_: str = None
    bstack111l1l11_opy_: str = None
    bstack11lll111lll_opy_: str = None
    bstack11l111l11l1_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l111l11l1l_opy_ = bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤᬊ")
    bstack11l1ll1llll_opy_ = bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᬋ")
    bstack1l11111l111_opy_ = bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦᬌ")
    bstack111ll1llll1_opy_ = bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥᬍ")
    bstack111llll1ll1_opy_ = bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨᬎ")
    bstack11l1l1lll1l_opy_ = bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᬏ")
    bstack11ll1l11111_opy_ = bstack11ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨᬐ")
    bstack11ll11lll1l_opy_ = bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᬑ")
    bstack11ll1l1111l_opy_ = bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᬒ")
    bstack11l1111111l_opy_ = bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᬓ")
    bstack1l111ll1111_opy_ = bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣᬔ")
    bstack11lll1l111l_opy_ = bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᬕ")
    bstack11l111l1l1l_opy_ = bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢᬖ")
    bstack11ll111ll11_opy_ = bstack11ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢᬗ")
    bstack1l111l1lll1_opy_ = bstack11ll11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᬘ")
    bstack11l1ll1lll1_opy_ = bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨᬙ")
    bstack11l111l111l_opy_ = bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧᬚ")
    bstack11l1111lll1_opy_ = bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧᬛ")
    bstack111llllll1l_opy_ = bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨᬜ")
    bstack111ll11ll1l_opy_ = bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩᬝ")
    bstack11l11ll111l_opy_ = bstack11ll11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᬞ")
    bstack111llllll11_opy_ = bstack11ll11_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᬟ")
    bstack111lll11ll1_opy_ = bstack11ll11_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᬠ")
    bstack111ll1lll1l_opy_ = bstack11ll11_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤᬡ")
    bstack111lll1l111_opy_ = bstack11ll11_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢᬢ")
    bstack111ll1lll11_opy_ = bstack11ll11_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨᬣ")
    bstack11l111ll1l1_opy_ = bstack11ll11_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢᬤ")
    bstack111lll1ll11_opy_ = bstack11ll11_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᬥ")
    bstack11l111l1lll_opy_ = bstack11ll11_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᬦ")
    bstack11l111l1ll1_opy_ = bstack11ll11_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᬧ")
    bstack111lll1111l_opy_ = bstack11ll11_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᬨ")
    KIND_SCREENSHOT = bstack11ll11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦᬩ")
    bstack11lll111l1l_opy_ = bstack11ll11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧᬪ")
    bstack11ll11l1lll_opy_ = bstack11ll11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᬫ")
    bstack11111l111l_opy_: Dict[str, bstack1l1l111ll1l_opy_] = dict()
    bstack111l1ll1ll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11l1l11_opy_: List[str]
    bstack1l1l1ll111l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1l11l1l11_opy_: List[str],
        bstack1l1l1ll111l_opy_: Dict[str, str],
        bstack1l1lll11ll1_opy_: bstack1l1lll1l11l_opy_
    ):
        self.bstack1l1l11l1l11_opy_ = bstack1l1l11l1l11_opy_
        self.bstack1l1l1ll111l_opy_ = bstack1l1l1ll111l_opy_
        self.bstack1l1lll11ll1_opy_ = bstack1l1lll11ll1_opy_
    def track_event(
        self,
        context: bstack1ll1ll1ll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤᬬ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11l111ll11l_opy_(
        self,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l11l11l11_opy_ = TestFramework.bstack11l11l11lll_opy_(bstack1l1ll1l11l1_opy_)
        if not bstack11l11l11l11_opy_ in TestFramework.bstack111l1ll1ll1_opy_:
            return
        self.logger.debug(bstack11ll11_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢᬭ").format(len(TestFramework.bstack111l1ll1ll1_opy_[bstack11l11l11l11_opy_])))
        for callback in TestFramework.bstack111l1ll1ll1_opy_[bstack11l11l11l11_opy_]:
            try:
                callback(self, instance, bstack1l1ll1l11l1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11ll11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢᬮ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack11ll11l11l1_opy_(self):
        return
    @abc.abstractmethod
    def bstack11ll1lll11l_opy_(self):
        return
    @abc.abstractmethod
    def bstack11lll1ll11l_opy_(self, instance, bstack1l1ll1l11l1_opy_):
        return
    @abc.abstractmethod
    def bstack11ll11llll1_opy_(self, instance, bstack1l1ll1l11l1_opy_):
        return
    @staticmethod
    def bstack1l1ll1ll111_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1l1ll11111l_opy_.create_context(target)
        instance = TestFramework.bstack11111l111l_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1ll111111_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack11ll1l11l1l_opy_(reverse=True) -> List[bstack1l1l111ll1l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack11111l111l_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll1lll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1ll11ll1l_opy_(ctx: bstack1l1ll1l1l1l_opy_, reverse=True) -> List[bstack1l1l111ll1l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack11111l111l_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll1lll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1llll1l1l_opy_(instance: bstack1l1l111ll1l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll111l1111_opy_(instance: bstack1l1l111ll1l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1l1l1111l1_opy_(instance: bstack1l1l111ll1l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11ll11_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᬯ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1111llll_opy_(instance: bstack1l1l111ll1l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11ll11_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤᬰ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack111l1l1llll_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack11ll11_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᬱ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1l1ll1ll111_opy_(target, strict)
        return TestFramework.bstack1ll111l1111_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1l1ll1ll111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l111l11ll_opy_(instance: bstack1l1l111ll1l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack111llll1l1l_opy_(instance: bstack1l1l111ll1l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11l11l11lll_opy_(bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack11ll11_opy_ (u"ࠦ࠿ࠨᬲ").join((TestFrameworkState(bstack1l1ll1l11l1_opy_[0]).name, TestHookState(bstack1l1ll1l11l1_opy_[1]).name))
    @staticmethod
    def bstack1l111l11l11_opy_(bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11l11l11l11_opy_ = TestFramework.bstack11l11l11lll_opy_(bstack1l1ll1l11l1_opy_)
        TestFramework.logger.debug(bstack11ll11_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥᬳ").format(bstack11l11l11l11_opy_))
        if not bstack11l11l11l11_opy_ in TestFramework.bstack111l1ll1ll1_opy_:
            TestFramework.bstack111l1ll1ll1_opy_[bstack11l11l11l11_opy_] = []
        TestFramework.bstack111l1ll1ll1_opy_[bstack11l11l11l11_opy_].append(callback)
    @staticmethod
    def bstack11ll11ll11l_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳ᬴ࠣ"):
            return klass.__qualname__
        return module + bstack11ll11_opy_ (u"ࠢ࠯ࠤᬵ") + klass.__qualname__
    @staticmethod
    def bstack11lll111l11_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}