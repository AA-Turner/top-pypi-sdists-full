# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1ll1ll1l111_opy_ import bstack1ll1ll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll11lll1ll_opy_, bstack1ll11llll1l_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll111_opy_ (u"ࠣࡖࡨࡷࡹࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᤩ").format(self.name)
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
        return bstack1ll111_opy_ (u"ࠤࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᤪ").format(self.name)
class bstack1ll11l1ll1l_opy_(bstack1ll11lll1ll_opy_):
    bstack1l11lll1l1l_opy_: List[str]
    bstack11l1lll11ll_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1ll1l1l1ll1_opy_: datetime
    bstack1ll1l1ll111_opy_: datetime
    def __init__(
        self,
        context: bstack1ll11llll1l_opy_,
        bstack1l11lll1l1l_opy_: List[str],
        bstack11l1lll11ll_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l11lll1l1l_opy_ = bstack1l11lll1l1l_opy_
        self.bstack11l1lll11ll_opy_ = bstack11l1lll11ll_opy_
        self.state = state
        self.bstack1ll1l1l1ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll1l1ll111_opy_ = datetime.now(tz=timezone.utc)
    def bstack1ll1ll1lll1_opy_(self, bstack1ll1l111lll_opy_: TestFrameworkState):
        bstack1ll1l111ll1_opy_ = TestFrameworkState(bstack1ll1l111lll_opy_).name
        if not bstack1ll1l111ll1_opy_:
            return False
        if bstack1ll1l111lll_opy_ == self.state:
            return False
        self.state = bstack1ll1l111lll_opy_
        self.bstack1ll1l1ll111_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1lll11l1l1l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1l1ll11l111_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l111lll111_opy_: int = None
    bstack1l111lllll1_opy_: str = None
    bstack11l111_opy_: str = None
    bstack11ll11ll1_opy_: str = None
    bstack1l11l1l11ll_opy_: str = None
    bstack11l1lllll11_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l1l1ll11ll_opy_ = bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨᤫ")
    bstack11llll1lll1_opy_ = bstack1ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧ᤬")
    bstack1l1l11llll1_opy_ = bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡲࡦࡳࡥࠣ᤭")
    bstack11ll111l111_opy_ = bstack1ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠢ᤮")
    bstack11ll111llll_opy_ = bstack1ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡺࡡࡨࡵࠥ᤯")
    bstack11lll1llll1_opy_ = bstack1ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࠨᤰ")
    bstack1l111llll11_opy_ = bstack1ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺ࡟ࡢࡶࠥᤱ")
    bstack1l1111ll111_opy_ = bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᤲ")
    bstack1l111l1l1ll_opy_ = bstack1ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᤳ")
    bstack11ll111l11l_opy_ = bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᤴ")
    bstack1l11llllll1_opy_ = bstack1ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠧᤵ")
    bstack1l111l111ll_opy_ = bstack1ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᤶ")
    bstack11l1lll1l11_opy_ = bstack1ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡣࡰࡦࡨࠦᤷ")
    bstack1l11111l1l1_opy_ = bstack1ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠦᤸ")
    bstack1l1l1l1ll11_opy_ = bstack1ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻ᤹ࠦ")
    bstack11llll11111_opy_ = bstack1ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࠥ᤺")
    bstack11l1llllll1_opy_ = bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠤ᤻")
    bstack11l1lll1ll1_opy_ = bstack1ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡧࡴࠤ᤼")
    bstack11l1lll1lll_opy_ = bstack1ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡳࡥࡵࡣࠥ᤽")
    bstack11l1l11ll1l_opy_ = bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡳࡤࡱࡳࡩࡸ࠭᤾")
    bstack11ll1l1l1ll_opy_ = bstack1ll111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥ᤿")
    bstack11l1ll11l1l_opy_ = bstack1ll111_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨ᥀")
    bstack11l1llll1ll_opy_ = bstack1ll111_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧ᥁")
    bstack11l1l1lll1l_opy_ = bstack1ll111_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢ࡭ࡩࠨ᥂")
    bstack11l1ll11111_opy_ = bstack1ll111_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷ࡫ࡳࡶ࡮ࡷࠦ᥃")
    bstack11ll1111111_opy_ = bstack1ll111_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡲ࡯ࡨࡵࠥ᥄")
    bstack11l1llll111_opy_ = bstack1ll111_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠦ᥅")
    bstack11l1lll111l_opy_ = bstack1ll111_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢ᥆")
    bstack11l1ll1l1l1_opy_ = bstack1ll111_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧ᥇")
    bstack11l1lll1111_opy_ = bstack1ll111_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ᥈")
    bstack11l1l1l1l11_opy_ = bstack1ll111_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨ᥉")
    KIND_SCREENSHOT = bstack1ll111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠣ᥊")
    bstack1l11l11ll1l_opy_ = bstack1ll111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡒࡏࡈࠤ᥋")
    bstack1l11111ll11_opy_ = bstack1ll111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥ᥌")
    bstack1ll1llllll1_opy_: Dict[str, bstack1ll11l1ll1l_opy_] = dict()
    bstack11l11lll1l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11lll1l1l_opy_: List[str]
    bstack11l1lll11ll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l11lll1l1l_opy_: List[str],
        bstack11l1lll11ll_opy_: Dict[str, str],
        bstack1ll1ll1l111_opy_: bstack1ll1ll1l11l_opy_
    ):
        self.bstack1l11lll1l1l_opy_ = bstack1l11lll1l1l_opy_
        self.bstack11l1lll11ll_opy_ = bstack11l1lll11ll_opy_
        self.bstack1ll1ll1l111_opy_ = bstack1ll1ll1l111_opy_
    def track_event(
        self,
        context: bstack1lll11l1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1ll111_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࢂࠨ᥍").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11ll11l1111_opy_(
        self,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11ll1l1111l_opy_ = TestFramework.bstack11ll1l11l11_opy_(bstack1ll1l1l1l1l_opy_)
        if not bstack11ll1l1111l_opy_ in TestFramework.bstack11l11lll1l1_opy_:
            return
        self.logger.debug(bstack1ll111_opy_ (u"ࠥ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࢁࡽࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠦ᥎").format(len(TestFramework.bstack11l11lll1l1_opy_[bstack11ll1l1111l_opy_])))
        for callback in TestFramework.bstack11l11lll1l1_opy_[bstack11ll1l1111l_opy_]:
            try:
                callback(self, instance, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll111_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠦ᥏").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l111ll111l_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1111lllll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l11111l1ll_opy_(self, instance, bstack1ll1l1l1l1l_opy_):
        return
    @abc.abstractmethod
    def bstack1l11l11111l_opy_(self, instance, bstack1ll1l1l1l1l_opy_):
        return
    @staticmethod
    def bstack1ll1l1ll1l1_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1ll11lll1ll_opy_.create_context(target)
        instance = TestFramework.bstack1ll1llllll1_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll1ll11l1l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l11111lll1_opy_(reverse=True) -> List[bstack1ll11l1ll1l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1ll1llllll1_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1l1l1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l1111ll_opy_(ctx: bstack1ll11llll1l_opy_, reverse=True) -> List[bstack1ll11l1ll1l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1ll1llllll1_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1l1l1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l1lllll_opy_(instance: bstack1ll11l1ll1l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lll111lll1_opy_(instance: bstack1ll11l1ll1l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1ll1ll1lll1_opy_(instance: bstack1ll11l1ll1l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll111_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡬ࡧࡼࡁࢀࢃࠠࡷࡣ࡯ࡹࡪࡃࡻࡾࠤᥐ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1ll1lll1_opy_(instance: bstack1ll11l1ll1l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1ll111_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡲࡹࡸࡩࡦࡵࡀࡿࢂࠨᥑ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11l11ll1111_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll111_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢᥒ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1ll1l1ll1l1_opy_(target, strict)
        return TestFramework.bstack1lll111lll1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1ll1l1ll1l1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1ll1ll11_opy_(instance: bstack1ll11l1ll1l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11l1llll1l1_opy_(instance: bstack1ll11l1ll1l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11ll1l11l11_opy_(bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack1ll111_opy_ (u"ࠣ࠼ࠥᥓ").join((TestFrameworkState(bstack1ll1l1l1l1l_opy_[0]).name, TestHookState(bstack1ll1l1l1l1l_opy_[1]).name))
    @staticmethod
    def bstack1l1l1111111_opy_(bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11ll1l1111l_opy_ = TestFramework.bstack11ll1l11l11_opy_(bstack1ll1l1l1l1l_opy_)
        TestFramework.logger.debug(bstack1ll111_opy_ (u"ࠤࡶࡩࡹࡥࡨࡰࡱ࡮ࡣࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡩࡱࡲ࡯ࡤࡸࡥࡨ࡫ࡶࡸࡷࡿ࡟࡬ࡧࡼࡁࢀࢃࠢᥔ").format(bstack11ll1l1111l_opy_))
        if not bstack11ll1l1111l_opy_ in TestFramework.bstack11l11lll1l1_opy_:
            TestFramework.bstack11l11lll1l1_opy_[bstack11ll1l1111l_opy_] = []
        TestFramework.bstack11l11lll1l1_opy_[bstack11ll1l1111l_opy_].append(callback)
    @staticmethod
    def bstack1l111llllll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡵ࡫ࡱࡷࠧᥕ"):
            return klass.__qualname__
        return module + bstack1ll111_opy_ (u"ࠦ࠳ࠨᥖ") + klass.__qualname__
    @staticmethod
    def bstack1l11l1111l1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}