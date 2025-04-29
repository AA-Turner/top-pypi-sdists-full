# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l1ll11_opy_ import bstack1111l1l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import bstack111111llll_opy_, bstack1lllllllll1_opy_
class bstack1lll1lll1l1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1llllll_opy_ (u"ࠨࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᓱ").format(self.name)
class bstack1lllll1lll1_opy_(Enum):
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
        return bstack1llllll_opy_ (u"ࠢࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᓲ").format(self.name)
class bstack1lll1ll111l_opy_(bstack111111llll_opy_):
    bstack1ll1l1l11l1_opy_: List[str]
    bstack1l11lll1lll_opy_: Dict[str, str]
    state: bstack1lllll1lll1_opy_
    bstack1111111111_opy_: datetime
    bstack1111l11ll1_opy_: datetime
    def __init__(
        self,
        context: bstack1lllllllll1_opy_,
        bstack1ll1l1l11l1_opy_: List[str],
        bstack1l11lll1lll_opy_: Dict[str, str],
        state=bstack1lllll1lll1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l1l11l1_opy_ = bstack1ll1l1l11l1_opy_
        self.bstack1l11lll1lll_opy_ = bstack1l11lll1lll_opy_
        self.state = state
        self.bstack1111111111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1111l11ll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1111l11lll_opy_(self, bstack11111111l1_opy_: bstack1lllll1lll1_opy_):
        bstack1111l11l1l_opy_ = bstack1lllll1lll1_opy_(bstack11111111l1_opy_).name
        if not bstack1111l11l1l_opy_:
            return False
        if bstack11111111l1_opy_ == self.state:
            return False
        self.state = bstack11111111l1_opy_
        self.bstack1111l11ll1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11l1111ll_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll1ll1lll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1lll111ll_opy_: int = None
    bstack1ll111l1ll1_opy_: str = None
    bstack11l11_opy_: str = None
    bstack1lll1l1111_opy_: str = None
    bstack1l1lll1l1ll_opy_: str = None
    bstack1l11ll111ll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1l11l1ll_opy_ = bstack1llllll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠦᓳ")
    bstack1l11ll1111l_opy_ = bstack1llllll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡪࡦࠥᓴ")
    bstack1ll1ll11ll1_opy_ = bstack1llllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡰࡤࡱࡪࠨᓵ")
    bstack1l11lll1111_opy_ = bstack1llllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫࡟ࡱࡣࡷ࡬ࠧᓶ")
    bstack1l11lll1ll1_opy_ = bstack1llllll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡸࡦ࡭ࡳࠣᓷ")
    bstack1l1l1l1lll1_opy_ = bstack1llllll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᓸ")
    bstack1l1lll1l11l_opy_ = bstack1llllll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࡤࡧࡴࠣᓹ")
    bstack1ll111lllll_opy_ = bstack1llllll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᓺ")
    bstack1ll11111111_opy_ = bstack1llllll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᓻ")
    bstack1l11ll11111_opy_ = bstack1llllll_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᓼ")
    bstack1ll1ll1l1l1_opy_ = bstack1llllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠥᓽ")
    bstack1l1lll11l11_opy_ = bstack1llllll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᓾ")
    bstack1l111lllll1_opy_ = bstack1llllll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡨࡵࡤࡦࠤᓿ")
    bstack1l1ll1l11ll_opy_ = bstack1llllll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠤᔀ")
    bstack1ll11lll1l1_opy_ = bstack1llllll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᔁ")
    bstack1l1l1lll11l_opy_ = bstack1llllll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠣᔂ")
    bstack1l11l111111_opy_ = bstack1llllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠢᔃ")
    bstack1l11l1lllll_opy_ = bstack1llllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳ࡬ࡹࠢᔄ")
    bstack1l11l1l1lll_opy_ = bstack1llllll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡱࡪࡺࡡࠣᔅ")
    bstack1l111l11l1l_opy_ = bstack1llllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡸࡩ࡯ࡱࡧࡶࠫᔆ")
    bstack1l1l1111l11_opy_ = bstack1llllll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᔇ")
    bstack1l111l1l1ll_opy_ = bstack1llllll_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᔈ")
    bstack1l111ll111l_opy_ = bstack1llllll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᔉ")
    bstack1l11l1ll1ll_opy_ = bstack1llllll_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡫ࡧࠦᔊ")
    bstack1l11l1l1l1l_opy_ = bstack1llllll_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡩࡸࡻ࡬ࡵࠤᔋ")
    bstack1l11l1l111l_opy_ = bstack1llllll_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡰࡴ࡭ࡳࠣᔌ")
    bstack1l111llll1l_opy_ = bstack1llllll_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠤᔍ")
    bstack1l11llll111_opy_ = bstack1llllll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᔎ")
    bstack1l111ll1lll_opy_ = bstack1llllll_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᔏ")
    bstack1l111l1ll1l_opy_ = bstack1llllll_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᔐ")
    bstack1l11l111ll1_opy_ = bstack1llllll_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦᔑ")
    bstack1l1llll1l11_opy_ = bstack1llllll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙ࠨᔒ")
    bstack1l1lllll111_opy_ = bstack1llllll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡐࡔࡍࠢᔓ")
    bstack1l1llll11ll_opy_ = bstack1llllll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᔔ")
    bstack1111l11l11_opy_: Dict[str, bstack1lll1ll111l_opy_] = dict()
    bstack1l1111lll11_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l1l11l1_opy_: List[str]
    bstack1l11lll1lll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l1l11l1_opy_: List[str],
        bstack1l11lll1lll_opy_: Dict[str, str],
        bstack1111l1ll11_opy_: bstack1111l1l1ll_opy_
    ):
        self.bstack1ll1l1l11l1_opy_ = bstack1ll1l1l11l1_opy_
        self.bstack1l11lll1lll_opy_ = bstack1l11lll1lll_opy_
        self.bstack1111l1ll11_opy_ = bstack1111l1ll11_opy_
    def track_event(
        self,
        context: bstack1l11l1111ll_opy_,
        test_framework_state: bstack1lllll1lll1_opy_,
        test_hook_state: bstack1lll1lll1l1_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1llllll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡢࡴࡪࡷࡂࢁࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽࢀࠦᔕ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11ll1l1l1_opy_(
        self,
        instance: bstack1lll1ll111l_opy_,
        bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11llllll1_opy_ = TestFramework.bstack1l1l11111l1_opy_(bstack1111111lll_opy_)
        if not bstack1l11llllll1_opy_ in TestFramework.bstack1l1111lll11_opy_:
            return
        self.logger.debug(bstack1llllll_opy_ (u"ࠣ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡿࢂࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠤᔖ").format(len(TestFramework.bstack1l1111lll11_opy_[bstack1l11llllll1_opy_])))
        for callback in TestFramework.bstack1l1111lll11_opy_[bstack1l11llllll1_opy_]:
            try:
                callback(self, instance, bstack1111111lll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1llllll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠤᔗ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1ll11111lll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1lll111l1_opy_(self, instance, bstack1111111lll_opy_):
        return
    @abc.abstractmethod
    def bstack1l1llll1ll1_opy_(self, instance, bstack1111111lll_opy_):
        return
    @staticmethod
    def bstack11111ll1ll_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack111111llll_opy_.create_context(target)
        instance = TestFramework.bstack1111l11l11_opy_.get(ctx.id, None)
        if instance and instance.bstack11111ll1l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1ll111lll1l_opy_(reverse=True) -> List[bstack1lll1ll111l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1111l11l11_opy_.values(),
            ),
            key=lambda t: t.bstack1111111111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllllll1ll_opy_(ctx: bstack1lllllllll1_opy_, reverse=True) -> List[bstack1lll1ll111l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1111l11l11_opy_.values(),
            ),
            key=lambda t: t.bstack1111111111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111lll1l_opy_(instance: bstack1lll1ll111l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack111111lll1_opy_(instance: bstack1lll1ll111l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1111l11lll_opy_(instance: bstack1lll1ll111l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1llllll_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢᔘ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l1lll1l_opy_(instance: bstack1lll1ll111l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1llllll_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠࡦࡰࡷࡶ࡮࡫ࡳ࠾ࡽࢀࠦᔙ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l1111l1lll_opy_(instance: bstack1lllll1lll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1llllll_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᔚ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack11111ll1ll_opy_(target, strict)
        return TestFramework.bstack111111lll1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack11111ll1ll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11ll1ll11_opy_(instance: bstack1lll1ll111l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l111lll111_opy_(instance: bstack1lll1ll111l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l1l11111l1_opy_(bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_]):
        return bstack1llllll_opy_ (u"ࠨ࠺ࠣᔛ").join((bstack1lllll1lll1_opy_(bstack1111111lll_opy_[0]).name, bstack1lll1lll1l1_opy_(bstack1111111lll_opy_[1]).name))
    @staticmethod
    def bstack1ll1l111l1l_opy_(bstack1111111lll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1lll1lll1l1_opy_], callback: Callable):
        bstack1l11llllll1_opy_ = TestFramework.bstack1l1l11111l1_opy_(bstack1111111lll_opy_)
        TestFramework.logger.debug(bstack1llllll_opy_ (u"ࠢࡴࡧࡷࡣ࡭ࡵ࡯࡬ࡡࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥ࡮࡯ࡰ࡭ࡢࡶࡪ࡭ࡩࡴࡶࡵࡽࡤࡱࡥࡺ࠿ࡾࢁࠧᔜ").format(bstack1l11llllll1_opy_))
        if not bstack1l11llllll1_opy_ in TestFramework.bstack1l1111lll11_opy_:
            TestFramework.bstack1l1111lll11_opy_[bstack1l11llllll1_opy_] = []
        TestFramework.bstack1l1111lll11_opy_[bstack1l11llllll1_opy_].append(callback)
    @staticmethod
    def bstack1l1lll1ll11_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1llllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡺࡩ࡯ࡵࠥᔝ"):
            return klass.__qualname__
        return module + bstack1llllll_opy_ (u"ࠤ࠱ࠦᔞ") + klass.__qualname__
    @staticmethod
    def bstack1ll11111l11_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}