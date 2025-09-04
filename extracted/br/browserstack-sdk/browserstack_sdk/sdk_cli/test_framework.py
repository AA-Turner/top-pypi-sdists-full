# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack1111111lll_opy_
from browserstack_sdk.sdk_cli.bstack111111111l_opy_ import bstack1lllll11lll_opy_, bstack1llll1l1ll1_opy_
class bstack1ll1llll1ll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1111l1l_opy_ (u"ࠨࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᖵ").format(self.name)
class bstack1lll1lllll1_opy_(Enum):
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
        return bstack1111l1l_opy_ (u"ࠢࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᖶ").format(self.name)
class bstack1lll1l1ll1l_opy_(bstack1lllll11lll_opy_):
    bstack1ll11ll1111_opy_: List[str]
    bstack1l11111l111_opy_: Dict[str, str]
    state: bstack1lll1lllll1_opy_
    bstack1llll1l1l11_opy_: datetime
    bstack1lllll111l1_opy_: datetime
    def __init__(
        self,
        context: bstack1llll1l1ll1_opy_,
        bstack1ll11ll1111_opy_: List[str],
        bstack1l11111l111_opy_: Dict[str, str],
        state=bstack1lll1lllll1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll11ll1111_opy_ = bstack1ll11ll1111_opy_
        self.bstack1l11111l111_opy_ = bstack1l11111l111_opy_
        self.state = state
        self.bstack1llll1l1l11_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lllll111l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lllllllll1_opy_(self, bstack1llll1ll111_opy_: bstack1lll1lllll1_opy_):
        bstack1llll1lll1l_opy_ = bstack1lll1lllll1_opy_(bstack1llll1ll111_opy_).name
        if not bstack1llll1lll1l_opy_:
            return False
        if bstack1llll1ll111_opy_ == self.state:
            return False
        self.state = bstack1llll1ll111_opy_
        self.bstack1lllll111l1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l111ll111l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll1l1llll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1l1ll1111_opy_: int = None
    bstack1l1ll1l1ll1_opy_: str = None
    bstack1l1llll_opy_: str = None
    bstack1lll1ll11l_opy_: str = None
    bstack1l1lll11ll1_opy_: str = None
    bstack1l11l1111ll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1111ll1l_opy_ = bstack1111l1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠦᖷ")
    bstack1l111l111l1_opy_ = bstack1111l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡪࡦࠥᖸ")
    bstack1ll111l1l11_opy_ = bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡰࡤࡱࡪࠨᖹ")
    bstack1l111l11lll_opy_ = bstack1111l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫࡟ࡱࡣࡷ࡬ࠧᖺ")
    bstack11lllll11l1_opy_ = bstack1111l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡸࡦ࡭ࡳࠣᖻ")
    bstack1l1l1111l1l_opy_ = bstack1111l1l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᖼ")
    bstack1l1lll111l1_opy_ = bstack1111l1l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࡤࡧࡴࠣᖽ")
    bstack1l1ll1ll11l_opy_ = bstack1111l1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᖾ")
    bstack1l1l1l1ll11_opy_ = bstack1111l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᖿ")
    bstack11llllllll1_opy_ = bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᗀ")
    bstack1ll111lll11_opy_ = bstack1111l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠥᗁ")
    bstack1l1ll11llll_opy_ = bstack1111l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᗂ")
    bstack1l111ll11ll_opy_ = bstack1111l1l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡨࡵࡤࡦࠤᗃ")
    bstack1l1l1l11lll_opy_ = bstack1111l1l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠤᗄ")
    bstack1ll11l1ll1l_opy_ = bstack1111l1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᗅ")
    bstack1l1l11111l1_opy_ = bstack1111l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠣᗆ")
    bstack1l1111111ll_opy_ = bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠢᗇ")
    bstack1l111ll1ll1_opy_ = bstack1111l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳ࡬ࡹࠢᗈ")
    bstack11lllllllll_opy_ = bstack1111l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡱࡪࡺࡡࠣᗉ")
    bstack11llll1llll_opy_ = bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡸࡩ࡯ࡱࡧࡶࠫᗊ")
    bstack1l11l1l111l_opy_ = bstack1111l1l_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᗋ")
    bstack1l1111lll1l_opy_ = bstack1111l1l_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᗌ")
    bstack11lllll1l1l_opy_ = bstack1111l1l_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᗍ")
    bstack1l111111111_opy_ = bstack1111l1l_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡫ࡧࠦᗎ")
    bstack1l111l1l1ll_opy_ = bstack1111l1l_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡩࡸࡻ࡬ࡵࠤᗏ")
    bstack1l11l11111l_opy_ = bstack1111l1l_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡰࡴ࡭ࡳࠣᗐ")
    bstack1l111ll11l1_opy_ = bstack1111l1l_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠤᗑ")
    bstack1l1111l11ll_opy_ = bstack1111l1l_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᗒ")
    bstack1l111111l11_opy_ = bstack1111l1l_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᗓ")
    bstack1l111lllll1_opy_ = bstack1111l1l_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᗔ")
    bstack1l1111ll111_opy_ = bstack1111l1l_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦᗕ")
    bstack1l1ll1111l1_opy_ = bstack1111l1l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙ࠨᗖ")
    bstack1l1lll11l11_opy_ = bstack1111l1l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡐࡔࡍࠢᗗ")
    bstack1l1ll11ll11_opy_ = bstack1111l1l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᗘ")
    bstack1111111111_opy_: Dict[str, bstack1lll1l1ll1l_opy_] = dict()
    bstack11llll1l1ll_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll11ll1111_opy_: List[str]
    bstack1l11111l111_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll11ll1111_opy_: List[str],
        bstack1l11111l111_opy_: Dict[str, str],
        bstack1111111ll1_opy_: bstack1111111lll_opy_
    ):
        self.bstack1ll11ll1111_opy_ = bstack1ll11ll1111_opy_
        self.bstack1l11111l111_opy_ = bstack1l11111l111_opy_
        self.bstack1111111ll1_opy_ = bstack1111111ll1_opy_
    def track_event(
        self,
        context: bstack1l111ll111l_opy_,
        test_framework_state: bstack1lll1lllll1_opy_,
        test_hook_state: bstack1ll1llll1ll_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡢࡴࡪࡷࡂࢁࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽࢀࠦᗙ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11lllll1l11_opy_(
        self,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11l111l11_opy_ = TestFramework.bstack1l11l111lll_opy_(bstack1lllll11ll1_opy_)
        if not bstack1l11l111l11_opy_ in TestFramework.bstack11llll1l1ll_opy_:
            return
        self.logger.debug(bstack1111l1l_opy_ (u"ࠣ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡿࢂࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠤᗚ").format(len(TestFramework.bstack11llll1l1ll_opy_[bstack1l11l111l11_opy_])))
        for callback in TestFramework.bstack11llll1l1ll_opy_[bstack1l11l111l11_opy_]:
            try:
                callback(self, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1111l1l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠤᗛ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1l1llll11_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1ll1l11ll_opy_(self, instance, bstack1lllll11ll1_opy_):
        return
    @abc.abstractmethod
    def bstack1l1ll1ll1l1_opy_(self, instance, bstack1lllll11ll1_opy_):
        return
    @staticmethod
    def bstack1lllll1111l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1lllll11lll_opy_.create_context(target)
        instance = TestFramework.bstack1111111111_opy_.get(ctx.id, None)
        if instance and instance.bstack1llllll1l11_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1l1ll1l1l_opy_(reverse=True) -> List[bstack1lll1l1ll1l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1111111111_opy_.values(),
            ),
            key=lambda t: t.bstack1llll1l1l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll1lll_opy_(ctx: bstack1llll1l1ll1_opy_, reverse=True) -> List[bstack1lll1l1ll1l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1111111111_opy_.values(),
            ),
            key=lambda t: t.bstack1llll1l1l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llll1l11ll_opy_(instance: bstack1lll1l1ll1l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lllll1l11l_opy_(instance: bstack1lll1l1ll1l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lllllllll1_opy_(instance: bstack1lll1l1ll1l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1111l1l_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢᗜ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l111111_opy_(instance: bstack1lll1l1ll1l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1111l1l_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠࡦࡰࡷࡶ࡮࡫ࡳ࠾ࡽࢀࠦᗝ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11llll1111l_opy_(instance: bstack1lll1lllll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1111l1l_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᗞ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1lllll1111l_opy_(target, strict)
        return TestFramework.bstack1lllll1l11l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1lllll1111l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1111l1ll1_opy_(instance: bstack1lll1l1ll1l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l111l1111l_opy_(instance: bstack1lll1l1ll1l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11l111lll_opy_(bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_]):
        return bstack1111l1l_opy_ (u"ࠨ࠺ࠣᗟ").join((bstack1lll1lllll1_opy_(bstack1lllll11ll1_opy_[0]).name, bstack1ll1llll1ll_opy_(bstack1lllll11ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll111lll1l_opy_(bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_], callback: Callable):
        bstack1l11l111l11_opy_ = TestFramework.bstack1l11l111lll_opy_(bstack1lllll11ll1_opy_)
        TestFramework.logger.debug(bstack1111l1l_opy_ (u"ࠢࡴࡧࡷࡣ࡭ࡵ࡯࡬ࡡࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥ࡮࡯ࡰ࡭ࡢࡶࡪ࡭ࡩࡴࡶࡵࡽࡤࡱࡥࡺ࠿ࡾࢁࠧᗠ").format(bstack1l11l111l11_opy_))
        if not bstack1l11l111l11_opy_ in TestFramework.bstack11llll1l1ll_opy_:
            TestFramework.bstack11llll1l1ll_opy_[bstack1l11l111l11_opy_] = []
        TestFramework.bstack11llll1l1ll_opy_[bstack1l11l111l11_opy_].append(callback)
    @staticmethod
    def bstack1l1ll11lll1_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1111l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡺࡩ࡯ࡵࠥᗡ"):
            return klass.__qualname__
        return module + bstack1111l1l_opy_ (u"ࠤ࠱ࠦᗢ") + klass.__qualname__
    @staticmethod
    def bstack1l1l1l1lll1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}