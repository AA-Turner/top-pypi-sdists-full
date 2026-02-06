# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1lll11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1ll1lllll1l_opy_, bstack1lll1llll1l_opy_
class bstack1ll11l1l11l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11lllll_opy_ (u"ࠤࡗࡩࡸࡺࡈࡰࡱ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᛥ").format(self.name)
class bstack1ll11111l1l_opy_(Enum):
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
        return bstack11lllll_opy_ (u"ࠥࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᛦ").format(self.name)
class bstack1ll11111ll1_opy_(bstack1ll1lllll1l_opy_):
    bstack1l1ll1l111l_opy_: List[str]
    bstack11llll1ll11_opy_: Dict[str, str]
    state: bstack1ll11111l1l_opy_
    bstack1lll11llll1_opy_: datetime
    bstack1ll1lll1l11_opy_: datetime
    def __init__(
        self,
        context: bstack1lll1llll1l_opy_,
        bstack1l1ll1l111l_opy_: List[str],
        bstack11llll1ll11_opy_: Dict[str, str],
        state=bstack1ll11111l1l_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1l1ll1l111l_opy_ = bstack1l1ll1l111l_opy_
        self.bstack11llll1ll11_opy_ = bstack11llll1ll11_opy_
        self.state = state
        self.bstack1lll11llll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll1lll1l11_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll1ll1lll_opy_(self, bstack1ll1lllll11_opy_: bstack1ll11111l1l_opy_):
        bstack1lll111l111_opy_ = bstack1ll11111l1l_opy_(bstack1ll1lllll11_opy_).name
        if not bstack1lll111l111_opy_:
            return False
        if bstack1ll1lllll11_opy_ == self.state:
            return False
        self.state = bstack1ll1lllll11_opy_
        self.bstack1ll1lll1l11_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack11lll1l1lll_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1l11ll11_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1l111l11l_opy_: int = None
    bstack1l1l11l1l1l_opy_: str = None
    bstack1111ll1_opy_: str = None
    bstack1l1l11l111_opy_: str = None
    bstack1l11lll1111_opy_: str = None
    bstack11llll1l1ll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l1lll1l111_opy_ = bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠢᛧ")
    bstack11ll1l111l1_opy_ = bstack11lllll_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡭ࡩࠨᛨ")
    bstack1l1lll11111_opy_ = bstack11lllll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠤᛩ")
    bstack11ll1ll1lll_opy_ = bstack11lllll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡢࡴࡦࡺࡨࠣᛪ")
    bstack11lll11ll11_opy_ = bstack11lllll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡴࡢࡩࡶࠦ᛫")
    bstack1l111l1ll11_opy_ = bstack11lllll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺࠢ᛬")
    bstack1l1l111ll11_opy_ = bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡷࡺࡲࡴࡠࡣࡷࠦ᛭")
    bstack1l11ll11l11_opy_ = bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᛮ")
    bstack1l1l1111l1l_opy_ = bstack11lllll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧᛯ")
    bstack11ll1ll111l_opy_ = bstack11lllll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᛰ")
    bstack1l1ll111ll1_opy_ = bstack11lllll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࠨᛱ")
    bstack1l11ll1ll1l_opy_ = bstack11lllll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠥᛲ")
    bstack11lll1l1l11_opy_ = bstack11lllll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡤࡱࡧࡩࠧᛳ")
    bstack1l11l1l1111_opy_ = bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠧᛴ")
    bstack1l1l1lllll1_opy_ = bstack11lllll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧᛵ")
    bstack1l111ll1111_opy_ = bstack11lllll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࠦᛶ")
    bstack11lll111ll1_opy_ = bstack11lllll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠥᛷ")
    bstack11llll11l1l_opy_ = bstack11lllll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡲ࡯ࡨࡵࠥᛸ")
    bstack11lll1llll1_opy_ = bstack11lllll_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡭ࡦࡶࡤࠦ᛹")
    bstack11ll11l1l1l_opy_ = bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡴࡥࡲࡴࡪࡹࠧ᛺")
    bstack11lllllll11_opy_ = bstack11lllll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦ᛻")
    bstack11ll1l11lll_opy_ = bstack11lllll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢ᛼")
    bstack11lll111l1l_opy_ = bstack11lllll_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡪࡴࡤࡦࡦࡢࡥࡹࠨ᛽")
    bstack11ll1l11l1l_opy_ = bstack11lllll_opy_ (u"ࠨࡨࡰࡱ࡮ࡣ࡮ࡪࠢ᛾")
    bstack11lll1l1ll1_opy_ = bstack11lllll_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡸࡥࡴࡷ࡯ࡸࠧ᛿")
    bstack11ll1l11l11_opy_ = bstack11lllll_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡬ࡰࡩࡶࠦᜀ")
    bstack11lll1ll1ll_opy_ = bstack11lllll_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠧᜁ")
    bstack11ll1l1l11l_opy_ = bstack11lllll_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᜂ")
    bstack11lll11llll_opy_ = bstack11lllll_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᜃ")
    bstack11lll1ll111_opy_ = bstack11lllll_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨᜄ")
    bstack11lll11111l_opy_ = bstack11lllll_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢᜅ")
    bstack1l1l1111ll1_opy_ = bstack11lllll_opy_ (u"ࠢࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠤᜆ")
    bstack1l11ll111l1_opy_ = bstack11lllll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡌࡐࡉࠥᜇ")
    bstack1l11ll1ll11_opy_ = bstack11lllll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᜈ")
    bstack1ll1llll11l_opy_: Dict[str, bstack1ll11111ll1_opy_] = dict()
    bstack11ll111llll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1ll1l111l_opy_: List[str]
    bstack11llll1ll11_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1ll1l111l_opy_: List[str],
        bstack11llll1ll11_opy_: Dict[str, str],
        bstack1lll11ll111_opy_: bstack1lll11l1lll_opy_
    ):
        self.bstack1l1ll1l111l_opy_ = bstack1l1ll1l111l_opy_
        self.bstack11llll1ll11_opy_ = bstack11llll1ll11_opy_
        self.bstack1lll11ll111_opy_ = bstack1lll11ll111_opy_
    def track_event(
        self,
        context: bstack11lll1l1lll_opy_,
        test_framework_state: bstack1ll11111l1l_opy_,
        test_hook_state: bstack1ll11l1l11l_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11lllll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࢃࠢᜉ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11ll1lll1ll_opy_(
        self,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        bstack11lllll11l1_opy_ = TestFramework.bstack11lllll111l_opy_(bstack1lll1l11lll_opy_)
        if not bstack11lllll11l1_opy_ in TestFramework.bstack11ll111llll_opy_:
            return
        self.logger.debug(bstack11lllll_opy_ (u"ࠦ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡻࡾࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠧᜊ").format(len(TestFramework.bstack11ll111llll_opy_[bstack11lllll11l1_opy_])))
        for callback in TestFramework.bstack11ll111llll_opy_[bstack11lllll11l1_opy_]:
            try:
                callback(self, instance, bstack1lll1l11lll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11lllll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠧᜋ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1l11ll1l1_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l11ll1111l_opy_(self, instance, bstack1lll1l11lll_opy_):
        return
    @abc.abstractmethod
    def bstack1l1l11111l1_opy_(self, instance, bstack1lll1l11lll_opy_):
        return
    @staticmethod
    def bstack1lll111ll1l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1ll1lllll1l_opy_.create_context(target)
        instance = TestFramework.bstack1ll1llll11l_opy_.get(ctx.id, None)
        if instance and instance.bstack1lll111l11l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l11ll11l1l_opy_(reverse=True) -> List[bstack1ll11111ll1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1ll1llll11l_opy_.values(),
            ),
            key=lambda t: t.bstack1lll11llll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll11l1111_opy_(ctx: bstack1lll1llll1l_opy_, reverse=True) -> List[bstack1ll11111ll1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1ll1llll11l_opy_.values(),
            ),
            key=lambda t: t.bstack1lll11llll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll111ll11_opy_(instance: bstack1ll11111ll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lll1l1l111_opy_(instance: bstack1ll11111ll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll1ll1lll_opy_(instance: bstack1ll11111ll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11lllll_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᜌ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11ll11lll11_opy_(instance: bstack1ll11111ll1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11lllll_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡳࡺࡲࡪࡧࡶࡁࢀࢃࠢᜍ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11ll1111ll1_opy_(instance: bstack1ll11111l1l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11lllll_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣᜎ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1lll111ll1l_opy_(target, strict)
        return TestFramework.bstack1lll1l1l111_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1lll111ll1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11lll1lll1l_opy_(instance: bstack1ll11111ll1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11ll1lll111_opy_(instance: bstack1ll11111ll1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11lllll111l_opy_(bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_]):
        return bstack11lllll_opy_ (u"ࠤ࠽ࠦᜏ").join((bstack1ll11111l1l_opy_(bstack1lll1l11lll_opy_[0]).name, bstack1ll11l1l11l_opy_(bstack1lll1l11lll_opy_[1]).name))
    @staticmethod
    def bstack1lll1l1l1ll_opy_(bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_], callback: Callable):
        bstack11lllll11l1_opy_ = TestFramework.bstack11lllll111l_opy_(bstack1lll1l11lll_opy_)
        TestFramework.logger.debug(bstack11lllll_opy_ (u"ࠥࡷࡪࡺ࡟ࡩࡱࡲ࡯ࡤࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡪࡲࡳࡰࡥࡲࡦࡩ࡬ࡷࡹࡸࡹࡠ࡭ࡨࡽࡂࢁࡽࠣᜐ").format(bstack11lllll11l1_opy_))
        if not bstack11lllll11l1_opy_ in TestFramework.bstack11ll111llll_opy_:
            TestFramework.bstack11ll111llll_opy_[bstack11lllll11l1_opy_] = []
        TestFramework.bstack11ll111llll_opy_[bstack11lllll11l1_opy_].append(callback)
    @staticmethod
    def bstack1l11llll1ll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡶ࡬ࡲࡸࠨᜑ"):
            return klass.__qualname__
        return module + bstack11lllll_opy_ (u"ࠧ࠴ࠢᜒ") + klass.__qualname__
    @staticmethod
    def bstack1l1l11ll11l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}