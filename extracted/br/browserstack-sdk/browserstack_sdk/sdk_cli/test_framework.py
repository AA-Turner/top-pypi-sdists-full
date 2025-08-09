# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack111111ll11_opy_ import bstack111111l11l_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import bstack1lllllll1l1_opy_, bstack1llllllll11_opy_
class bstack1lll1ll1l1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11l1_opy_ (u"ࠤࡗࡩࡸࡺࡈࡰࡱ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᖪ").format(self.name)
class bstack1lll1l111ll_opy_(Enum):
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
        return bstack11l1_opy_ (u"ࠥࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᖫ").format(self.name)
class bstack1lll1111l1l_opy_(bstack1lllllll1l1_opy_):
    bstack1ll11l11ll1_opy_: List[str]
    bstack1l1111l111l_opy_: Dict[str, str]
    state: bstack1lll1l111ll_opy_
    bstack1lllll11ll1_opy_: datetime
    bstack1lllll111l1_opy_: datetime
    def __init__(
        self,
        context: bstack1llllllll11_opy_,
        bstack1ll11l11ll1_opy_: List[str],
        bstack1l1111l111l_opy_: Dict[str, str],
        state=bstack1lll1l111ll_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll11l11ll1_opy_ = bstack1ll11l11ll1_opy_
        self.bstack1l1111l111l_opy_ = bstack1l1111l111l_opy_
        self.state = state
        self.bstack1lllll11ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lllll111l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1111111lll_opy_(self, bstack1llllllll1l_opy_: bstack1lll1l111ll_opy_):
        bstack1lllll11l1l_opy_ = bstack1lll1l111ll_opy_(bstack1llllllll1l_opy_).name
        if not bstack1lllll11l1l_opy_:
            return False
        if bstack1llllllll1l_opy_ == self.state:
            return False
        self.state = bstack1llllllll1l_opy_
        self.bstack1lllll111l1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l1111lllll_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1llll111l1l_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1ll1lllll_opy_: int = None
    bstack1l1ll11lll1_opy_: str = None
    bstack1l111ll_opy_: str = None
    bstack1llll1lll1_opy_: str = None
    bstack1l1l1lll1ll_opy_: str = None
    bstack1l111l1ll11_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1l111l1l_opy_ = bstack11l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠢᖬ")
    bstack1l11l111l1l_opy_ = bstack11l1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡭ࡩࠨᖭ")
    bstack1ll11lll1ll_opy_ = bstack11l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠤᖮ")
    bstack11llllll11l_opy_ = bstack11l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡢࡴࡦࡺࡨࠣᖯ")
    bstack1l11111ll11_opy_ = bstack11l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡴࡢࡩࡶࠦᖰ")
    bstack1l1l111lll1_opy_ = bstack11l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᖱ")
    bstack1l1l1ll11ll_opy_ = bstack11l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡷࡺࡲࡴࡠࡣࡷࠦᖲ")
    bstack1l1llll1l11_opy_ = bstack11l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᖳ")
    bstack1l1llll11l1_opy_ = bstack11l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧᖴ")
    bstack1l1111l11l1_opy_ = bstack11l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᖵ")
    bstack1ll111lll1l_opy_ = bstack11l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࠨᖶ")
    bstack1l1lll1ll1l_opy_ = bstack11l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠥᖷ")
    bstack1l111111ll1_opy_ = bstack11l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡤࡱࡧࡩࠧᖸ")
    bstack1l1l1l1ll11_opy_ = bstack11l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠧᖹ")
    bstack1ll11l1ll1l_opy_ = bstack11l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧᖺ")
    bstack1l1l111111l_opy_ = bstack11l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࠦᖻ")
    bstack1l111ll11ll_opy_ = bstack11l1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠥᖼ")
    bstack1l111ll11l1_opy_ = bstack11l1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡲ࡯ࡨࡵࠥᖽ")
    bstack1l111l1l111_opy_ = bstack11l1_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡭ࡦࡶࡤࠦᖾ")
    bstack11lllll1ll1_opy_ = bstack11l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡴࡥࡲࡴࡪࡹࠧᖿ")
    bstack1l11l1l1l1l_opy_ = bstack11l1_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦᗀ")
    bstack1l1111ll1ll_opy_ = bstack11l1_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᗁ")
    bstack1l11111l1ll_opy_ = bstack11l1_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡪࡴࡤࡦࡦࡢࡥࡹࠨᗂ")
    bstack1l111lllll1_opy_ = bstack11l1_opy_ (u"ࠨࡨࡰࡱ࡮ࡣ࡮ࡪࠢᗃ")
    bstack1l111lll1l1_opy_ = bstack11l1_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡸࡥࡴࡷ࡯ࡸࠧᗄ")
    bstack1l111l1llll_opy_ = bstack11l1_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡬ࡰࡩࡶࠦᗅ")
    bstack1l11l11l111_opy_ = bstack11l1_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠧᗆ")
    bstack1l11l11111l_opy_ = bstack11l1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᗇ")
    bstack1l111ll1lll_opy_ = bstack11l1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᗈ")
    bstack1l111l1l1ll_opy_ = bstack11l1_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨᗉ")
    bstack1l111l1l1l1_opy_ = bstack11l1_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢᗊ")
    bstack1l1l1llll11_opy_ = bstack11l1_opy_ (u"ࠢࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠤᗋ")
    bstack1l1ll111l11_opy_ = bstack11l1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡌࡐࡉࠥᗌ")
    bstack1l1ll1l1l11_opy_ = bstack11l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᗍ")
    bstack1lllll1llll_opy_: Dict[str, bstack1lll1111l1l_opy_] = dict()
    bstack11llll1l1l1_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll11l11ll1_opy_: List[str]
    bstack1l1111l111l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll11l11ll1_opy_: List[str],
        bstack1l1111l111l_opy_: Dict[str, str],
        bstack111111ll11_opy_: bstack111111l11l_opy_
    ):
        self.bstack1ll11l11ll1_opy_ = bstack1ll11l11ll1_opy_
        self.bstack1l1111l111l_opy_ = bstack1l1111l111l_opy_
        self.bstack111111ll11_opy_ = bstack111111ll11_opy_
    def track_event(
        self,
        context: bstack1l1111lllll_opy_,
        test_framework_state: bstack1lll1l111ll_opy_,
        test_hook_state: bstack1lll1ll1l1l_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࢃࠢᗎ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11l1111l1_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11l1l11l1_opy_ = TestFramework.bstack1l11l1l1111_opy_(bstack1lllllll11l_opy_)
        if not bstack1l11l1l11l1_opy_ in TestFramework.bstack11llll1l1l1_opy_:
            return
        self.logger.debug(bstack11l1_opy_ (u"ࠦ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡻࡾࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠧᗏ").format(len(TestFramework.bstack11llll1l1l1_opy_[bstack1l11l1l11l1_opy_])))
        for callback in TestFramework.bstack11llll1l1l1_opy_[bstack1l11l1l11l1_opy_]:
            try:
                callback(self, instance, bstack1lllllll11l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11l1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠧᗐ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1l1llllll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1ll11l1ll_opy_(self, instance, bstack1lllllll11l_opy_):
        return
    @abc.abstractmethod
    def bstack1l1ll11111l_opy_(self, instance, bstack1lllllll11l_opy_):
        return
    @staticmethod
    def bstack1lllll11111_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1lllllll1l1_opy_.create_context(target)
        instance = TestFramework.bstack1lllll1llll_opy_.get(ctx.id, None)
        if instance and instance.bstack111111l111_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1ll1ll1l1_opy_(reverse=True) -> List[bstack1lll1111l1l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lllll1llll_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll11ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllllll1ll_opy_(ctx: bstack1llllllll11_opy_, reverse=True) -> List[bstack1lll1111l1l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lllll1llll_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll11ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llll1llll1_opy_(instance: bstack1lll1111l1l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lllllllll1_opy_(instance: bstack1lll1111l1l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1111111lll_opy_(instance: bstack1lll1111l1l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l1_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᗑ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111llllll_opy_(instance: bstack1lll1111l1l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11l1_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡳࡺࡲࡪࡧࡶࡁࢀࢃࠢᗒ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11llll1l111_opy_(instance: bstack1lll1l111ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l1_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣᗓ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1lllll11111_opy_(target, strict)
        return TestFramework.bstack1lllllllll1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1lllll11111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111l11l11_opy_(instance: bstack1lll1111l1l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l11111l11l_opy_(instance: bstack1lll1111l1l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11l1l1111_opy_(bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_]):
        return bstack11l1_opy_ (u"ࠤ࠽ࠦᗔ").join((bstack1lll1l111ll_opy_(bstack1lllllll11l_opy_[0]).name, bstack1lll1ll1l1l_opy_(bstack1lllllll11l_opy_[1]).name))
    @staticmethod
    def bstack1ll11lll111_opy_(bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_], callback: Callable):
        bstack1l11l1l11l1_opy_ = TestFramework.bstack1l11l1l1111_opy_(bstack1lllllll11l_opy_)
        TestFramework.logger.debug(bstack11l1_opy_ (u"ࠥࡷࡪࡺ࡟ࡩࡱࡲ࡯ࡤࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡪࡲࡳࡰࡥࡲࡦࡩ࡬ࡷࡹࡸࡹࡠ࡭ࡨࡽࡂࢁࡽࠣᗕ").format(bstack1l11l1l11l1_opy_))
        if not bstack1l11l1l11l1_opy_ in TestFramework.bstack11llll1l1l1_opy_:
            TestFramework.bstack11llll1l1l1_opy_[bstack1l11l1l11l1_opy_] = []
        TestFramework.bstack11llll1l1l1_opy_[bstack1l11l1l11l1_opy_].append(callback)
    @staticmethod
    def bstack1l1lll1111l_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡶ࡬ࡲࡸࠨᗖ"):
            return klass.__qualname__
        return module + bstack11l1_opy_ (u"ࠧ࠴ࠢᗗ") + klass.__qualname__
    @staticmethod
    def bstack1l1lll11ll1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}