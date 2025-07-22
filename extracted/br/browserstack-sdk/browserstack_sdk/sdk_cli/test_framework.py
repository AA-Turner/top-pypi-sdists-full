# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111111lll_opy_ import bstack111111l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll11_opy_ import bstack1lllllll1ll_opy_, bstack1llll1ll11l_opy_
class bstack1lll111llll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack111l111_opy_ (u"ࠢࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᖨ").format(self.name)
class bstack1ll1lll1lll_opy_(Enum):
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
        return bstack111l111_opy_ (u"ࠣࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᖩ").format(self.name)
class bstack1lll1lllll1_opy_(bstack1lllllll1ll_opy_):
    bstack1ll11l11ll1_opy_: List[str]
    bstack1l111111ll1_opy_: Dict[str, str]
    state: bstack1ll1lll1lll_opy_
    bstack1lllll111ll_opy_: datetime
    bstack1llllllllll_opy_: datetime
    def __init__(
        self,
        context: bstack1llll1ll11l_opy_,
        bstack1ll11l11ll1_opy_: List[str],
        bstack1l111111ll1_opy_: Dict[str, str],
        state=bstack1ll1lll1lll_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll11l11ll1_opy_ = bstack1ll11l11ll1_opy_
        self.bstack1l111111ll1_opy_ = bstack1l111111ll1_opy_
        self.state = state
        self.bstack1lllll111ll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1llllllllll_opy_ = datetime.now(tz=timezone.utc)
    def bstack1111111111_opy_(self, bstack1lllll1111l_opy_: bstack1ll1lll1lll_opy_):
        bstack1llll1llll1_opy_ = bstack1ll1lll1lll_opy_(bstack1lllll1111l_opy_).name
        if not bstack1llll1llll1_opy_:
            return False
        if bstack1lllll1111l_opy_ == self.state:
            return False
        self.state = bstack1lllll1111l_opy_
        self.bstack1llllllllll_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l111111l11_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1lll1l11_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1ll111lll_opy_: int = None
    bstack1l1ll1l1lll_opy_: str = None
    bstack11l111_opy_: str = None
    bstack1l111111l1_opy_: str = None
    bstack1l1ll1l11ll_opy_: str = None
    bstack1l11l111111_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll11l11l1l_opy_ = bstack111l111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧᖪ")
    bstack1l111l1111l_opy_ = bstack111l111_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦᖫ")
    bstack1ll111l111l_opy_ = bstack111l111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠢᖬ")
    bstack1l111ll1l11_opy_ = bstack111l111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭ࠨᖭ")
    bstack1l111llll11_opy_ = bstack111l111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡹࡧࡧࡴࠤᖮ")
    bstack1l1l1111111_opy_ = bstack111l111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᖯ")
    bstack1l1ll11ll11_opy_ = bstack111l111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࡥࡡࡵࠤᖰ")
    bstack1l1l1l1lll1_opy_ = bstack111l111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᖱ")
    bstack1l1ll1ll1l1_opy_ = bstack111l111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᖲ")
    bstack1l11111111l_opy_ = bstack111l111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᖳ")
    bstack1ll111ll1l1_opy_ = bstack111l111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠦᖴ")
    bstack1l1l1ll1ll1_opy_ = bstack111l111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᖵ")
    bstack1l111111111_opy_ = bstack111l111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡩ࡯ࡥࡧࠥᖶ")
    bstack1l1l1l1l111_opy_ = bstack111l111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠥᖷ")
    bstack1ll11l1lll1_opy_ = bstack111l111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥᖸ")
    bstack1l11lllll11_opy_ = bstack111l111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࠤᖹ")
    bstack1l11111l111_opy_ = bstack111l111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠣᖺ")
    bstack1l1111lllll_opy_ = bstack111l111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴ࡭ࡳࠣᖻ")
    bstack1l11111l11l_opy_ = bstack111l111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡲ࡫ࡴࡢࠤᖼ")
    bstack11lllll11ll_opy_ = bstack111l111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡹࡣࡰࡲࡨࡷࠬᖽ")
    bstack1l11l1l1l11_opy_ = bstack111l111_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᖾ")
    bstack11lllllll11_opy_ = bstack111l111_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᖿ")
    bstack1l11l111lll_opy_ = bstack111l111_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᗀ")
    bstack1l111111lll_opy_ = bstack111l111_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡬ࡨࠧᗁ")
    bstack11llllll11l_opy_ = bstack111l111_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡪࡹࡵ࡭ࡶࠥᗂ")
    bstack1l11111l1l1_opy_ = bstack111l111_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡱࡵࡧࡴࠤᗃ")
    bstack1l1111l1111_opy_ = bstack111l111_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠥᗄ")
    bstack1l111l1l1ll_opy_ = bstack111l111_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᗅ")
    bstack1l111l11l11_opy_ = bstack111l111_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᗆ")
    bstack1l111llll1l_opy_ = bstack111l111_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦᗇ")
    bstack1l111l1l1l1_opy_ = bstack111l111_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧᗈ")
    bstack1l1ll1l111l_opy_ = bstack111l111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠢᗉ")
    bstack1l1ll11lll1_opy_ = bstack111l111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡑࡕࡇࠣᗊ")
    bstack1l1l1ll111l_opy_ = bstack111l111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᗋ")
    bstack1lllll1llll_opy_: Dict[str, bstack1lll1lllll1_opy_] = dict()
    bstack11llll1ll1l_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll11l11ll1_opy_: List[str]
    bstack1l111111ll1_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll11l11ll1_opy_: List[str],
        bstack1l111111ll1_opy_: Dict[str, str],
        bstack1111111lll_opy_: bstack111111l1l1_opy_
    ):
        self.bstack1ll11l11ll1_opy_ = bstack1ll11l11ll1_opy_
        self.bstack1l111111ll1_opy_ = bstack1l111111ll1_opy_
        self.bstack1111111lll_opy_ = bstack1111111lll_opy_
    def track_event(
        self,
        context: bstack1l111111l11_opy_,
        test_framework_state: bstack1ll1lll1lll_opy_,
        test_hook_state: bstack1lll111llll_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack111l111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧᗌ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l1111111ll_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11l11l1l1_opy_ = TestFramework.bstack1l11l11ll1l_opy_(bstack1llllll111l_opy_)
        if not bstack1l11l11l1l1_opy_ in TestFramework.bstack11llll1ll1l_opy_:
            return
        self.logger.debug(bstack111l111_opy_ (u"ࠤ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠥᗍ").format(len(TestFramework.bstack11llll1ll1l_opy_[bstack1l11l11l1l1_opy_])))
        for callback in TestFramework.bstack11llll1ll1l_opy_[bstack1l11l11l1l1_opy_]:
            try:
                callback(self, instance, bstack1llllll111l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack111l111_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠥᗎ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1lll1ll11_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1ll1ll11l_opy_(self, instance, bstack1llllll111l_opy_):
        return
    @abc.abstractmethod
    def bstack1l1lll1ll1l_opy_(self, instance, bstack1llllll111l_opy_):
        return
    @staticmethod
    def bstack1lllll11l1l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1lllllll1ll_opy_.create_context(target)
        instance = TestFramework.bstack1lllll1llll_opy_.get(ctx.id, None)
        if instance and instance.bstack1lllll111l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1ll11l111_opy_(reverse=True) -> List[bstack1lll1lllll1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lllll1llll_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll111ll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111111l1_opy_(ctx: bstack1llll1ll11l_opy_, reverse=True) -> List[bstack1lll1lllll1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lllll1llll_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll111ll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllll1l111_opy_(instance: bstack1lll1lllll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1111111l1l_opy_(instance: bstack1lll1lllll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1111111111_opy_(instance: bstack1lll1lllll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack111l111_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣᗏ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1111ll1l1_opy_(instance: bstack1lll1lllll1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack111l111_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡱࡸࡷ࡯ࡥࡴ࠿ࡾࢁࠧᗐ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11llll11l1l_opy_(instance: bstack1ll1lll1lll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack111l111_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨᗑ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1lllll11l1l_opy_(target, strict)
        return TestFramework.bstack1111111l1l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1lllll11l1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111ll1lll_opy_(instance: bstack1lll1lllll1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l11l1111l1_opy_(instance: bstack1lll1lllll1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11l11ll1l_opy_(bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_]):
        return bstack111l111_opy_ (u"ࠢ࠻ࠤᗒ").join((bstack1ll1lll1lll_opy_(bstack1llllll111l_opy_[0]).name, bstack1lll111llll_opy_(bstack1llllll111l_opy_[1]).name))
    @staticmethod
    def bstack1ll11l1l11l_opy_(bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_], callback: Callable):
        bstack1l11l11l1l1_opy_ = TestFramework.bstack1l11l11ll1l_opy_(bstack1llllll111l_opy_)
        TestFramework.logger.debug(bstack111l111_opy_ (u"ࠣࡵࡨࡸࡤ࡮࡯ࡰ࡭ࡢࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡨࡰࡱ࡮ࡣࡷ࡫ࡧࡪࡵࡷࡶࡾࡥ࡫ࡦࡻࡀࡿࢂࠨᗓ").format(bstack1l11l11l1l1_opy_))
        if not bstack1l11l11l1l1_opy_ in TestFramework.bstack11llll1ll1l_opy_:
            TestFramework.bstack11llll1ll1l_opy_[bstack1l11l11l1l1_opy_] = []
        TestFramework.bstack11llll1ll1l_opy_[bstack1l11l11l1l1_opy_].append(callback)
    @staticmethod
    def bstack1l1lll1l111_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡴࡪࡰࡶࠦᗔ"):
            return klass.__qualname__
        return module + bstack111l111_opy_ (u"ࠥ࠲ࠧᗕ") + klass.__qualname__
    @staticmethod
    def bstack1l1ll11l1l1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}