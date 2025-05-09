# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l1l1ll_opy_ import bstack1111l1ll11_opy_
from browserstack_sdk.sdk_cli.bstack111111ll1l_opy_ import bstack111111l111_opy_, bstack1111l111ll_opy_
class bstack1lll1l111l1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11lll_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᓶ").format(self.name)
class bstack1lll111ll11_opy_(Enum):
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
        return bstack11lll_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᓷ").format(self.name)
class bstack1lll1ll1ll1_opy_(bstack111111l111_opy_):
    bstack1ll1l111l1l_opy_: List[str]
    bstack1l11l1111l1_opy_: Dict[str, str]
    state: bstack1lll111ll11_opy_
    bstack111111ll11_opy_: datetime
    bstack1111l1111l_opy_: datetime
    def __init__(
        self,
        context: bstack1111l111ll_opy_,
        bstack1ll1l111l1l_opy_: List[str],
        bstack1l11l1111l1_opy_: Dict[str, str],
        state=bstack1lll111ll11_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l111l1l_opy_ = bstack1ll1l111l1l_opy_
        self.bstack1l11l1111l1_opy_ = bstack1l11l1111l1_opy_
        self.state = state
        self.bstack111111ll11_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1111l1111l_opy_ = datetime.now(tz=timezone.utc)
    def bstack11111llll1_opy_(self, bstack11111l11ll_opy_: bstack1lll111ll11_opy_):
        bstack11111l11l1_opy_ = bstack1lll111ll11_opy_(bstack11111l11ll_opy_).name
        if not bstack11111l11l1_opy_:
            return False
        if bstack11111l11ll_opy_ == self.state:
            return False
        self.state = bstack11111l11ll_opy_
        self.bstack1111l1111l_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l111lll111_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll1111ll1_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1llll111l_opy_: int = None
    bstack1ll111l11l1_opy_: str = None
    bstack111ll11_opy_: str = None
    bstack1l11ll1111_opy_: str = None
    bstack1l1llll1lll_opy_: str = None
    bstack1l11l1l11ll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1l1ll1ll_opy_ = bstack11lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤᓸ")
    bstack1l11l1lll1l_opy_ = bstack11lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᓹ")
    bstack1ll1ll1l1ll_opy_ = bstack11lll_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦᓺ")
    bstack1l11l11l11l_opy_ = bstack11lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥᓻ")
    bstack1l11l1lllll_opy_ = bstack11lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨᓼ")
    bstack1l1l1lll111_opy_ = bstack11lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᓽ")
    bstack1ll1111l1ll_opy_ = bstack11lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨᓾ")
    bstack1l1lll1ll1l_opy_ = bstack11lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᓿ")
    bstack1ll111l11ll_opy_ = bstack11lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᔀ")
    bstack1l111ll111l_opy_ = bstack11lll_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᔁ")
    bstack1ll1l1111l1_opy_ = bstack11lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣᔂ")
    bstack1ll111l1111_opy_ = bstack11lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᔃ")
    bstack1l11l11llll_opy_ = bstack11lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢᔄ")
    bstack1l1ll1l11ll_opy_ = bstack11lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢᔅ")
    bstack1ll1l1l111l_opy_ = bstack11lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᔆ")
    bstack1l1l1lll11l_opy_ = bstack11lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨᔇ")
    bstack1l11ll11ll1_opy_ = bstack11lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧᔈ")
    bstack1l111l1l1ll_opy_ = bstack11lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧᔉ")
    bstack1l11ll1lll1_opy_ = bstack11lll_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨᔊ")
    bstack1l111l111l1_opy_ = bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩᔋ")
    bstack1l1l111l111_opy_ = bstack11lll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᔌ")
    bstack1l111ll1ll1_opy_ = bstack11lll_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᔍ")
    bstack1l11l1lll11_opy_ = bstack11lll_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᔎ")
    bstack1l11ll111l1_opy_ = bstack11lll_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤᔏ")
    bstack1l11l1ll1l1_opy_ = bstack11lll_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢᔐ")
    bstack1l111l1l11l_opy_ = bstack11lll_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨᔑ")
    bstack1l11l11111l_opy_ = bstack11lll_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢᔒ")
    bstack1l11l1111ll_opy_ = bstack11lll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᔓ")
    bstack1l11l111l11_opy_ = bstack11lll_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᔔ")
    bstack1l11ll11111_opy_ = bstack11lll_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᔕ")
    bstack1l11l1l1111_opy_ = bstack11lll_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᔖ")
    bstack1l1lll1l1ll_opy_ = bstack11lll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦᔗ")
    bstack1ll111l1l1l_opy_ = bstack11lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧᔘ")
    bstack1ll11111l1l_opy_ = bstack11lll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᔙ")
    bstack111111111l_opy_: Dict[str, bstack1lll1ll1ll1_opy_] = dict()
    bstack1l1111l1lll_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l111l1l_opy_: List[str]
    bstack1l11l1111l1_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l111l1l_opy_: List[str],
        bstack1l11l1111l1_opy_: Dict[str, str],
        bstack1111l1l1ll_opy_: bstack1111l1ll11_opy_
    ):
        self.bstack1ll1l111l1l_opy_ = bstack1ll1l111l1l_opy_
        self.bstack1l11l1111l1_opy_ = bstack1l11l1111l1_opy_
        self.bstack1111l1l1ll_opy_ = bstack1111l1l1ll_opy_
    def track_event(
        self,
        context: bstack1l111lll111_opy_,
        test_framework_state: bstack1lll111ll11_opy_,
        test_hook_state: bstack1lll1l111l1_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤᔚ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11ll1l111_opy_(
        self,
        instance: bstack1lll1ll1ll1_opy_,
        bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11llll1l1_opy_ = TestFramework.bstack1l11llll11l_opy_(bstack1111111ll1_opy_)
        if not bstack1l11llll1l1_opy_ in TestFramework.bstack1l1111l1lll_opy_:
            return
        self.logger.debug(bstack11lll_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢᔛ").format(len(TestFramework.bstack1l1111l1lll_opy_[bstack1l11llll1l1_opy_])))
        for callback in TestFramework.bstack1l1111l1lll_opy_[bstack1l11llll1l1_opy_]:
            try:
                callback(self, instance, bstack1111111ll1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11lll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢᔜ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1ll11111ll1_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1lll11lll_opy_(self, instance, bstack1111111ll1_opy_):
        return
    @abc.abstractmethod
    def bstack1ll111ll1l1_opy_(self, instance, bstack1111111ll1_opy_):
        return
    @staticmethod
    def bstack1111111l11_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack111111l111_opy_.create_context(target)
        instance = TestFramework.bstack111111111l_opy_.get(ctx.id, None)
        if instance and instance.bstack1111l11l1l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1llll1l11_opy_(reverse=True) -> List[bstack1lll1ll1ll1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack111111111l_opy_.values(),
            ),
            key=lambda t: t.bstack111111ll11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1111l11l11_opy_(ctx: bstack1111l111ll_opy_, reverse=True) -> List[bstack1lll1ll1ll1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack111111111l_opy_.values(),
            ),
            key=lambda t: t.bstack111111ll11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111ll111_opy_(instance: bstack1lll1ll1ll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack111111l1l1_opy_(instance: bstack1lll1ll1ll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack11111llll1_opy_(instance: bstack1lll1ll1ll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11lll_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᔝ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l1l1l11_opy_(instance: bstack1lll1ll1ll1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11lll_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤᔞ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l1111l1l1l_opy_(instance: bstack1lll111ll11_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11lll_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᔟ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1111111l11_opy_(target, strict)
        return TestFramework.bstack111111l1l1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1111111l11_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11lll1lll_opy_(instance: bstack1lll1ll1ll1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l111l11ll1_opy_(instance: bstack1lll1ll1ll1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11llll11l_opy_(bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_]):
        return bstack11lll_opy_ (u"ࠦ࠿ࠨᔠ").join((bstack1lll111ll11_opy_(bstack1111111ll1_opy_[0]).name, bstack1lll1l111l1_opy_(bstack1111111ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll1ll1l_opy_(bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_], callback: Callable):
        bstack1l11llll1l1_opy_ = TestFramework.bstack1l11llll11l_opy_(bstack1111111ll1_opy_)
        TestFramework.logger.debug(bstack11lll_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥᔡ").format(bstack1l11llll1l1_opy_))
        if not bstack1l11llll1l1_opy_ in TestFramework.bstack1l1111l1lll_opy_:
            TestFramework.bstack1l1111l1lll_opy_[bstack1l11llll1l1_opy_] = []
        TestFramework.bstack1l1111l1lll_opy_[bstack1l11llll1l1_opy_].append(callback)
    @staticmethod
    def bstack1ll1111llll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳࠣᔢ"):
            return klass.__qualname__
        return module + bstack11lll_opy_ (u"ࠢ࠯ࠤᔣ") + klass.__qualname__
    @staticmethod
    def bstack1ll11111lll_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}