# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1lll1l11111_opy_ import bstack1lll11llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1l1l_opy_ import bstack1ll1llllll1_opy_, bstack1lll11l1l11_opy_
class bstack1ll11lll1ll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11l1l11_opy_ (u"ࠢࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥយ").format(self.name)
class bstack1l1llllll1l_opy_(Enum):
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
        return bstack11l1l11_opy_ (u"ࠣࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤរ").format(self.name)
class bstack1l1llll111l_opy_(bstack1ll1llllll1_opy_):
    bstack1l1l1ll1ll1_opy_: List[str]
    bstack11ll111ll1l_opy_: Dict[str, str]
    state: bstack1l1llllll1l_opy_
    bstack1ll1lll1ll1_opy_: datetime
    bstack1ll1ll1lll1_opy_: datetime
    def __init__(
        self,
        context: bstack1lll11l1l11_opy_,
        bstack1l1l1ll1ll1_opy_: List[str],
        bstack11ll111ll1l_opy_: Dict[str, str],
        state=bstack1l1llllll1l_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1l1l1ll1ll1_opy_ = bstack1l1l1ll1ll1_opy_
        self.bstack11ll111ll1l_opy_ = bstack11ll111ll1l_opy_
        self.state = state
        self.bstack1ll1lll1ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll1ll1lll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll111ll11_opy_(self, bstack1ll1lllll1l_opy_: bstack1l1llllll1l_opy_):
        bstack1lll1111ll1_opy_ = bstack1l1llllll1l_opy_(bstack1ll1lllll1l_opy_).name
        if not bstack1lll1111ll1_opy_:
            return False
        if bstack1ll1lllll1l_opy_ == self.state:
            return False
        self.state = bstack1ll1lllll1l_opy_
        self.bstack1ll1ll1lll1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack11ll111l11l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll11l111l1_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l11lll1lll_opy_: int = None
    bstack1l11ll1lll1_opy_: str = None
    bstack1lll1ll_opy_: str = None
    bstack111ll111ll_opy_: str = None
    bstack1l11l1ll11l_opy_: str = None
    bstack11lll111111_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l1l11lll11_opy_ = bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧល")
    bstack11l1lllll1l_opy_ = bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦវ")
    bstack1l1ll11llll_opy_ = bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠢឝ")
    bstack11ll11ll11l_opy_ = bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭ࠨឞ")
    bstack11ll1llll1l_opy_ = bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡹࡧࡧࡴࠤស")
    bstack1l1111l11l1_opy_ = bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࠧហ")
    bstack1l11l1lllll_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࡥࡡࡵࠤឡ")
    bstack1l11l11l11l_opy_ = bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦអ")
    bstack1l11llllll1_opy_ = bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥឣ")
    bstack11ll11l1lll_opy_ = bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳࡨࡧࡴࡪࡱࡱࠦឤ")
    bstack1l1ll1l1lll_opy_ = bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠦឥ")
    bstack1l11l1l11ll_opy_ = bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣឦ")
    bstack11ll1l1l1ll_opy_ = bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡩ࡯ࡥࡧࠥឧ")
    bstack1l111ll1111_opy_ = bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠥឨ")
    bstack1l1l1l1ll11_opy_ = bstack11l1l11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥឩ")
    bstack1l111111lll_opy_ = bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࠤឪ")
    bstack11ll111llll_opy_ = bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠣឫ")
    bstack11l1lllllll_opy_ = bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴ࡭ࡳࠣឬ")
    bstack11lll11111l_opy_ = bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡲ࡫ࡴࡢࠤឭ")
    bstack11l1lll1l1l_opy_ = bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡹࡣࡰࡲࡨࡷࠬឮ")
    bstack11lll1l1lll_opy_ = bstack11l1l11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤឯ")
    bstack11ll1llll11_opy_ = bstack11l1l11_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧឰ")
    bstack11lll111lll_opy_ = bstack11l1l11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦឱ")
    bstack11l1llllll1_opy_ = bstack11l1l11_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡬ࡨࠧឲ")
    bstack11ll1ll1lll_opy_ = bstack11l1l11_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡪࡹࡵ࡭ࡶࠥឳ")
    bstack11ll11lll1l_opy_ = bstack11l1l11_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡱࡵࡧࡴࠤ឴")
    bstack11ll111111l_opy_ = bstack11l1l11_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠥ឵")
    bstack11ll11l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨា")
    bstack11lll1111l1_opy_ = bstack11l1l11_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦិ")
    bstack11ll111ll11_opy_ = bstack11l1l11_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦី")
    bstack11ll11111l1_opy_ = bstack11l1l11_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧឹ")
    bstack1l11l1ll1ll_opy_ = bstack11l1l11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠢឺ")
    bstack1l111lll1ll_opy_ = bstack11l1l11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡑࡕࡇࠣុ")
    bstack1l11ll11ll1_opy_ = bstack11l1l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤូ")
    bstack1ll1ll1ll1l_opy_: Dict[str, bstack1l1llll111l_opy_] = dict()
    bstack11l1ll1ll1l_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l1ll1ll1_opy_: List[str]
    bstack11ll111ll1l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1l1ll1ll1_opy_: List[str],
        bstack11ll111ll1l_opy_: Dict[str, str],
        bstack1lll1l11111_opy_: bstack1lll11llll1_opy_
    ):
        self.bstack1l1l1ll1ll1_opy_ = bstack1l1l1ll1ll1_opy_
        self.bstack11ll111ll1l_opy_ = bstack11ll111ll1l_opy_
        self.bstack1lll1l11111_opy_ = bstack1lll1l11111_opy_
    def track_event(
        self,
        context: bstack11ll111l11l_opy_,
        test_framework_state: bstack1l1llllll1l_opy_,
        test_hook_state: bstack1ll11lll1ll_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧួ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11ll1l111l1_opy_(
        self,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack11lll11lll1_opy_ = TestFramework.bstack11lll11ll11_opy_(bstack1lll11ll111_opy_)
        if not bstack11lll11lll1_opy_ in TestFramework.bstack11l1ll1ll1l_opy_:
            return
        self.logger.debug(bstack11l1l11_opy_ (u"ࠤ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠥើ").format(len(TestFramework.bstack11l1ll1ll1l_opy_[bstack11lll11lll1_opy_])))
        for callback in TestFramework.bstack11l1ll1ll1l_opy_[bstack11lll11lll1_opy_]:
            try:
                callback(self, instance, bstack1lll11ll111_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11l1l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠥឿ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l11ll111l1_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l11ll1l11l_opy_(self, instance, bstack1lll11ll111_opy_):
        return
    @abc.abstractmethod
    def bstack1l11l1ll1l1_opy_(self, instance, bstack1lll11ll111_opy_):
        return
    @staticmethod
    def bstack1lll11ll11l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1ll1llllll1_opy_.create_context(target)
        instance = TestFramework.bstack1ll1ll1ll1l_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll1ll1llll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l11lll1ll1_opy_(reverse=True) -> List[bstack1l1llll111l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1ll1ll1ll1l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1lll1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1ll1ll11_opy_(ctx: bstack1lll11l1l11_opy_, reverse=True) -> List[bstack1l1llll111l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1ll1ll1ll1l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1lll1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll111l111_opy_(instance: bstack1l1llll111l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll1lll111l_opy_(instance: bstack1l1llll111l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll111ll11_opy_(instance: bstack1l1llll111l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣៀ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11ll1l11111_opy_(instance: bstack1l1llll111l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11l1l11_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡱࡸࡷ࡯ࡥࡴ࠿ࡾࢁࠧេ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11l1ll111ll_opy_(instance: bstack1l1llllll1l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l1l11_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨែ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1lll11ll11l_opy_(target, strict)
        return TestFramework.bstack1ll1lll111l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1lll11ll11l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11ll11llll1_opy_(instance: bstack1l1llll111l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11ll1ll11l1_opy_(instance: bstack1l1llll111l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11lll11ll11_opy_(bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_]):
        return bstack11l1l11_opy_ (u"ࠢ࠻ࠤៃ").join((bstack1l1llllll1l_opy_(bstack1lll11ll111_opy_[0]).name, bstack1ll11lll1ll_opy_(bstack1lll11ll111_opy_[1]).name))
    @staticmethod
    def bstack1l1l11lll1l_opy_(bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_], callback: Callable):
        bstack11lll11lll1_opy_ = TestFramework.bstack11lll11ll11_opy_(bstack1lll11ll111_opy_)
        TestFramework.logger.debug(bstack11l1l11_opy_ (u"ࠣࡵࡨࡸࡤ࡮࡯ࡰ࡭ࡢࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡨࡰࡱ࡮ࡣࡷ࡫ࡧࡪࡵࡷࡶࡾࡥ࡫ࡦࡻࡀࡿࢂࠨោ").format(bstack11lll11lll1_opy_))
        if not bstack11lll11lll1_opy_ in TestFramework.bstack11l1ll1ll1l_opy_:
            TestFramework.bstack11l1ll1ll1l_opy_[bstack11lll11lll1_opy_] = []
        TestFramework.bstack11l1ll1ll1l_opy_[bstack11lll11lll1_opy_].append(callback)
    @staticmethod
    def bstack1l11lll1l11_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡴࡪࡰࡶࠦៅ"):
            return klass.__qualname__
        return module + bstack11l1l11_opy_ (u"ࠥ࠲ࠧំ") + klass.__qualname__
    @staticmethod
    def bstack1l11l111111_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}