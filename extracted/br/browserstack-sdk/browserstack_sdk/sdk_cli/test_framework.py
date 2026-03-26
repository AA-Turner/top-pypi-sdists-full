# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1ll1l1111ll_opy_ import bstack1ll11lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111lll11_opy_ import bstack1ll11llll1l_opy_, bstack1ll11l1l1l1_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll1lll_opy_ (u"ࠤࡗࡩࡸࡺࡈࡰࡱ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᧄ").format(self.name)
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
        return bstack1ll1lll_opy_ (u"ࠥࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᧅ").format(self.name)
class bstack1l1l1lllll1_opy_(bstack1ll11llll1l_opy_):
    bstack1l11l1l11ll_opy_: List[str]
    bstack11l1l111111_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1ll11lll1l1_opy_: datetime
    bstack1ll11ll1ll1_opy_: datetime
    def __init__(
        self,
        context: bstack1ll11l1l1l1_opy_,
        bstack1l11l1l11ll_opy_: List[str],
        bstack11l1l111111_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l11l1l11ll_opy_ = bstack1l11l1l11ll_opy_
        self.bstack11l1l111111_opy_ = bstack11l1l111111_opy_
        self.state = state
        self.bstack1ll11lll1l1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll11ll1ll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll1111ll_opy_(self, bstack1ll11lll11l_opy_: TestFrameworkState):
        bstack1ll11l111l1_opy_ = TestFrameworkState(bstack1ll11lll11l_opy_).name
        if not bstack1ll11l111l1_opy_:
            return False
        if bstack1ll11lll11l_opy_ == self.state:
            return False
        self.state = bstack1ll11lll11l_opy_
        self.bstack1ll11ll1ll1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll1l11lll1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1l1l11lll1l_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1111llll1_opy_: int = None
    bstack1l111l11ll1_opy_: str = None
    bstack111lll_opy_: str = None
    bstack1lll1l1l1l_opy_: str = None
    bstack1l1111lllll_opy_: str = None
    bstack11l1ll11l1l_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l11ll11l1l_opy_ = bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠢᧆ")
    bstack11ll1lll111_opy_ = bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡭ࡩࠨᧇ")
    bstack1l11lll1l1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠤᧈ")
    bstack11l1ll1l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡢࡴࡦࡺࡨࠣᧉ")
    bstack11l1ll1l111_opy_ = bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡴࡢࡩࡶࠦ᧊")
    bstack11lll1111ll_opy_ = bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺࠢ᧋")
    bstack1l1111ll11l_opy_ = bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡷࡺࡲࡴࡠࡣࡷࠦ᧌")
    bstack1l111l1l111_opy_ = bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨ᧍")
    bstack1l111ll1l11_opy_ = bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧ᧎")
    bstack11l11l1ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡣࡢࡶ࡬ࡳࡳࠨ᧏")
    bstack1l11ll1l111_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࠨ᧐")
    bstack1l11111111l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠥ᧑")
    bstack11l11lll11l_opy_ = bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡤࡱࡧࡩࠧ᧒")
    bstack11lll1lllll_opy_ = bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠧ᧓")
    bstack1l11l1ll11l_opy_ = bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧ᧔")
    bstack11ll1llll11_opy_ = bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࠦ᧕")
    bstack11l1l1l1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠥ᧖")
    bstack11l1l1l111l_opy_ = bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡲ࡯ࡨࡵࠥ᧗")
    bstack11l11ll1l1l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡭ࡦࡶࡤࠦ᧘")
    bstack11l11l11lll_opy_ = bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡴࡥࡲࡴࡪࡹࠧ᧙")
    bstack11ll11l1111_opy_ = bstack1ll1lll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦ᧚")
    bstack11l1lll11ll_opy_ = bstack1ll1lll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢ᧛")
    bstack11l1l11l1l1_opy_ = bstack1ll1lll_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡪࡴࡤࡦࡦࡢࡥࡹࠨ᧜")
    bstack11l1l111lll_opy_ = bstack1ll1lll_opy_ (u"ࠨࡨࡰࡱ࡮ࡣ࡮ࡪࠢ᧝")
    bstack11l11ll111l_opy_ = bstack1ll1lll_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡸࡥࡴࡷ࡯ࡸࠧ᧞")
    bstack11l1lll1l1l_opy_ = bstack1ll1lll_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡬ࡰࡩࡶࠦ᧟")
    bstack11l11ll1l11_opy_ = bstack1ll1lll_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠧ᧠")
    bstack11l1l1111ll_opy_ = bstack1ll1lll_opy_ (u"ࠥࡰࡴ࡭ࡳࠣ᧡")
    bstack11l1ll11l11_opy_ = bstack1ll1lll_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨ᧢")
    bstack11l11l1lll1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨ᧣")
    bstack11l1l111l1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢ᧤")
    KIND_SCREENSHOT = bstack1ll1lll_opy_ (u"ࠢࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠤ᧥")
    bstack1l1111l1ll1_opy_ = bstack1ll1lll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡌࡐࡉࠥ᧦")
    bstack11lllll1l11_opy_ = bstack1ll1lll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦ᧧")
    bstack1111l1ll1l_opy_: Dict[str, bstack1l1l1lllll1_opy_] = dict()
    bstack11l1111llll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11l1l11ll_opy_: List[str]
    bstack11l1l111111_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l11l1l11ll_opy_: List[str],
        bstack11l1l111111_opy_: Dict[str, str],
        bstack1ll1l1111ll_opy_: bstack1ll11lllll1_opy_
    ):
        self.bstack1l11l1l11ll_opy_ = bstack1l11l1l11ll_opy_
        self.bstack11l1l111111_opy_ = bstack11l1l111111_opy_
        self.bstack1ll1l1111ll_opy_ = bstack1ll1l1111ll_opy_
    def track_event(
        self,
        context: bstack1ll1l11lll1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࢃࠢ᧨").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11l1l11lll1_opy_(
        self,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l1llll111_opy_ = TestFramework.bstack11l1llll1l1_opy_(bstack1ll11l1l111_opy_)
        if not bstack11l1llll111_opy_ in TestFramework.bstack11l1111llll_opy_:
            return
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠦ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡻࡾࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠧ᧩").format(len(TestFramework.bstack11l1111llll_opy_[bstack11l1llll111_opy_])))
        for callback in TestFramework.bstack11l1111llll_opy_[bstack11l1llll111_opy_]:
            try:
                callback(self, instance, bstack1ll11l1l111_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠧ᧪").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l111l1l1ll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1111111ll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1111ll1ll_opy_(self, instance, bstack1ll11l1l111_opy_):
        return
    @abc.abstractmethod
    def bstack1l111l1ll11_opy_(self, instance, bstack1ll11l1l111_opy_):
        return
    @staticmethod
    def bstack1ll11ll11l1_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1ll11llll1l_opy_.create_context(target)
        instance = TestFramework.bstack1111l1ll1l_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll111ll111_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l11111ll1l_opy_(reverse=True) -> List[bstack1l1l1lllll1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1111l1ll1l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll11lll1l1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll111ll1ll_opy_(ctx: bstack1ll11l1l1l1_opy_, reverse=True) -> List[bstack1l1l1lllll1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1111l1ll1l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll11lll1l1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l1lll1l_opy_(instance: bstack1l1l1lllll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll1l11llll_opy_(instance: bstack1l1l1lllll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll1111ll_opy_(instance: bstack1l1l1lllll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥ᧫").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1l1lllll_opy_(instance: bstack1l1l1lllll1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡳࡺࡲࡪࡧࡶࡁࢀࢃࠢ᧬").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11l1111l11l_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣ᧭").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1ll11ll11l1_opy_(target, strict)
        return TestFramework.bstack1ll1l11llll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1ll11ll11l1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1l11111l_opy_(instance: bstack1l1l1lllll1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11l1lll111l_opy_(instance: bstack1l1l1lllll1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11l1llll1l1_opy_(bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack1ll1lll_opy_ (u"ࠤ࠽ࠦ᧮").join((TestFrameworkState(bstack1ll11l1l111_opy_[0]).name, TestHookState(bstack1ll11l1l111_opy_[1]).name))
    @staticmethod
    def bstack1l11ll11111_opy_(bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11l1llll111_opy_ = TestFramework.bstack11l1llll1l1_opy_(bstack1ll11l1l111_opy_)
        TestFramework.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡷࡪࡺ࡟ࡩࡱࡲ࡯ࡤࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡪࡲࡳࡰࡥࡲࡦࡩ࡬ࡷࡹࡸࡹࡠ࡭ࡨࡽࡂࢁࡽࠣ᧯").format(bstack11l1llll111_opy_))
        if not bstack11l1llll111_opy_ in TestFramework.bstack11l1111llll_opy_:
            TestFramework.bstack11l1111llll_opy_[bstack11l1llll111_opy_] = []
        TestFramework.bstack11l1111llll_opy_[bstack11l1llll111_opy_].append(callback)
    @staticmethod
    def bstack1l111l11lll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1ll1lll_opy_ (u"ࠦࡧࡻࡩ࡭ࡶ࡬ࡲࡸࠨ᧰"):
            return klass.__qualname__
        return module + bstack1ll1lll_opy_ (u"ࠧ࠴ࠢ᧱") + klass.__qualname__
    @staticmethod
    def bstack1l1111lll11_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}