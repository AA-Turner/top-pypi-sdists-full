# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1l1lll111ll_opy_ import bstack1l1lll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l1111_opy_ import bstack1l1l1llllll_opy_, bstack1l1ll111l11_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l111l_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᬤ").format(self.name)
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
        return bstack1l111l_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᬥ").format(self.name)
class bstack1l11l11111l_opy_(bstack1l1l1llllll_opy_):
    bstack1l11llllll1_opy_: List[str]
    bstack1l11lll1lll_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1l1ll11ll1l_opy_: datetime
    bstack1l1lll1111l_opy_: datetime
    def __init__(
        self,
        context: bstack1l1ll111l11_opy_,
        bstack1l11llllll1_opy_: List[str],
        bstack1l11lll1lll_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l11llllll1_opy_ = bstack1l11llllll1_opy_
        self.bstack1l11lll1lll_opy_ = bstack1l11lll1lll_opy_
        self.state = state
        self.bstack1l1ll11ll1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1lll1111l_opy_ = datetime.now(tz=timezone.utc)
    def bstack11111ll11l_opy_(self, bstack1l1ll1l1ll1_opy_: TestFrameworkState):
        bstack1l1ll11l111_opy_ = TestFrameworkState(bstack1l1ll1l1ll1_opy_).name
        if not bstack1l1ll11l111_opy_:
            return False
        if bstack1l1ll1l1ll1_opy_ == self.state:
            return False
        self.state = bstack1l1ll1l1ll1_opy_
        self.bstack1l1lll1111l_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll1l1ll111_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1llll11ll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack11lll11llll_opy_: int = None
    bstack11ll1l1l111_opy_: str = None
    bstack111l11l_opy_: str = None
    bstack111l1ll11_opy_: str = None
    bstack11ll1ll11ll_opy_: str = None
    bstack111ll1ll111_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l11111llll_opy_ = bstack1l111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤᬦ")
    bstack11l1l1lllll_opy_ = bstack1l111l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᬧ")
    bstack11llllll11l_opy_ = bstack1l111l_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦᬨ")
    bstack11l111111ll_opy_ = bstack1l111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥᬩ")
    bstack111lll11l1l_opy_ = bstack1l111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨᬪ")
    bstack11l1l1ll1l1_opy_ = bstack1l111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᬫ")
    bstack11ll11llll1_opy_ = bstack1l111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨᬬ")
    bstack11ll1ll1l1l_opy_ = bstack1l111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᬭ")
    bstack11lll11ll11_opy_ = bstack1l111l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᬮ")
    bstack11l111l111l_opy_ = bstack1l111l_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᬯ")
    bstack11lllllll1l_opy_ = bstack1l111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣᬰ")
    bstack11ll11l11ll_opy_ = bstack1l111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᬱ")
    bstack111llll111l_opy_ = bstack1l111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢᬲ")
    bstack11ll1111l11_opy_ = bstack1l111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢᬳ")
    bstack1l111l1111l_opy_ = bstack1l111l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ᬴ࠢ")
    bstack11l1ll1l111_opy_ = bstack1l111l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨᬵ")
    bstack111ll1l1lll_opy_ = bstack1l111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧᬶ")
    bstack111llllll11_opy_ = bstack1l111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧᬷ")
    bstack111ll1l1l11_opy_ = bstack1l111l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨᬸ")
    bstack111ll1111ll_opy_ = bstack1l111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩᬹ")
    bstack11l11l11lll_opy_ = bstack1l111l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᬺ")
    bstack11l1111l11l_opy_ = bstack1l111l_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᬻ")
    bstack111ll1l1111_opy_ = bstack1l111l_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᬼ")
    bstack111ll1ll1ll_opy_ = bstack1l111l_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤᬽ")
    bstack111lll1l111_opy_ = bstack1l111l_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢᬾ")
    bstack111lll1llll_opy_ = bstack1l111l_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨᬿ")
    bstack111lll11ll1_opy_ = bstack1l111l_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢᭀ")
    bstack111ll1l1l1l_opy_ = bstack1l111l_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᭁ")
    bstack111ll1lllll_opy_ = bstack1l111l_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᭂ")
    bstack111ll1ll11l_opy_ = bstack1l111l_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᭃ")
    bstack11l1111l111_opy_ = bstack1l111l_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤ᭄")
    KIND_SCREENSHOT = bstack1l111l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦᭅ")
    bstack11ll1lll11l_opy_ = bstack1l111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧᭆ")
    bstack11ll111llll_opy_ = bstack1l111l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᭇ")
    bstack1l1l1111l_opy_: Dict[str, bstack1l11l11111l_opy_] = dict()
    bstack111l1ll111l_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11llllll1_opy_: List[str]
    bstack1l11lll1lll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l11llllll1_opy_: List[str],
        bstack1l11lll1lll_opy_: Dict[str, str],
        bstack1l1lll111ll_opy_: bstack1l1lll111l1_opy_
    ):
        self.bstack1l11llllll1_opy_ = bstack1l11llllll1_opy_
        self.bstack1l11lll1lll_opy_ = bstack1l11lll1lll_opy_
        self.bstack1l1lll111ll_opy_ = bstack1l1lll111ll_opy_
    def track_event(
        self,
        context: bstack1ll1l1ll111_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤᭈ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack111llll1111_opy_(
        self,
        instance: bstack1l11l11111l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l11l1111l_opy_ = TestFramework.bstack11l111ll1l1_opy_(bstack1l1l1lllll1_opy_)
        if not bstack11l11l1111l_opy_ in TestFramework.bstack111l1ll111l_opy_:
            return
        self.logger.debug(bstack1l111l_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢᭉ").format(len(TestFramework.bstack111l1ll111l_opy_[bstack11l11l1111l_opy_])))
        for callback in TestFramework.bstack111l1ll111l_opy_[bstack11l11l1111l_opy_]:
            try:
                callback(self, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l111l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢᭊ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack11lll1l111l_opy_(self):
        return
    @abc.abstractmethod
    def bstack11ll1llllll_opy_(self):
        return
    @abc.abstractmethod
    def bstack11ll1l1lll1_opy_(self, instance, bstack1l1l1lllll1_opy_):
        return
    @abc.abstractmethod
    def bstack11ll1l111ll_opy_(self, instance, bstack1l1l1lllll1_opy_):
        return
    @staticmethod
    def bstack1l1ll111l1l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1l1l1llllll_opy_.create_context(target)
        instance = TestFramework.bstack1l1l1111l_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1ll1l11ll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack11ll11l1lll_opy_(reverse=True) -> List[bstack1l11l11111l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1l1l1111l_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll11ll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1ll11111l_opy_(ctx: bstack1l1ll111l11_opy_, reverse=True) -> List[bstack1l11l11111l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1l1l1111l_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll11ll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1lll1l1l1_opy_(instance: bstack1l11l11111l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll111111ll_opy_(instance: bstack1l11l11111l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack11111ll11l_opy_(instance: bstack1l11l11111l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l111l_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᭋ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack111lllll1l1_opy_(instance: bstack1l11l11111l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l111l_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤᭌ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack111l1l1l111_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack1l111l_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥ᭍").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1l1ll111l1l_opy_(target, strict)
        return TestFramework.bstack1ll111111ll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1l1ll111l1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack111llll1ll1_opy_(instance: bstack1l11l11111l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack111lll1lll1_opy_(instance: bstack1l11l11111l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11l111ll1l1_opy_(bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack1l111l_opy_ (u"ࠦ࠿ࠨ᭎").join((TestFrameworkState(bstack1l1l1lllll1_opy_[0]).name, TestHookState(bstack1l1l1lllll1_opy_[1]).name))
    @staticmethod
    def bstack1l11111ll11_opy_(bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11l11l1111l_opy_ = TestFramework.bstack11l111ll1l1_opy_(bstack1l1l1lllll1_opy_)
        TestFramework.logger.debug(bstack1l111l_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥ᭏").format(bstack11l11l1111l_opy_))
        if not bstack11l11l1111l_opy_ in TestFramework.bstack111l1ll111l_opy_:
            TestFramework.bstack111l1ll111l_opy_[bstack11l11l1111l_opy_] = []
        TestFramework.bstack111l1ll111l_opy_[bstack11l11l1111l_opy_].append(callback)
    @staticmethod
    def bstack11ll111ll1l_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳࠣ᭐"):
            return klass.__qualname__
        return module + bstack1l111l_opy_ (u"ࠢ࠯ࠤ᭑") + klass.__qualname__
    @staticmethod
    def bstack11lll1l11ll_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}