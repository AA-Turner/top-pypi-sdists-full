# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack11111lll11_opy_ import bstack11111ll11l_opy_
from browserstack_sdk.sdk_cli.bstack1llllllll1l_opy_ import bstack11111l11ll_opy_, bstack1llllllll11_opy_
class bstack1lllll1111l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack111lll_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᔼ").format(self.name)
class bstack1lll11lllll_opy_(Enum):
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
        return bstack111lll_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᔽ").format(self.name)
class bstack1lll1111l1l_opy_(bstack11111l11ll_opy_):
    bstack1ll11l1ll1l_opy_: List[str]
    bstack1l111l11l11_opy_: Dict[str, str]
    state: bstack1lll11lllll_opy_
    bstack111111ll1l_opy_: datetime
    bstack1lllll1ll1l_opy_: datetime
    def __init__(
        self,
        context: bstack1llllllll11_opy_,
        bstack1ll11l1ll1l_opy_: List[str],
        bstack1l111l11l11_opy_: Dict[str, str],
        state=bstack1lll11lllll_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll11l1ll1l_opy_ = bstack1ll11l1ll1l_opy_
        self.bstack1l111l11l11_opy_ = bstack1l111l11l11_opy_
        self.state = state
        self.bstack111111ll1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lllll1ll1l_opy_ = datetime.now(tz=timezone.utc)
    def bstack11111ll111_opy_(self, bstack1lllllll111_opy_: bstack1lll11lllll_opy_):
        bstack111111l1l1_opy_ = bstack1lll11lllll_opy_(bstack1lllllll111_opy_).name
        if not bstack111111l1l1_opy_:
            return False
        if bstack1lllllll111_opy_ == self.state:
            return False
        self.state = bstack1lllllll111_opy_
        self.bstack1lllll1ll1l_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11l1l1lll_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll11111l1_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1ll1ll1ll_opy_: int = None
    bstack1l1lll1llll_opy_: str = None
    bstack11ll1_opy_: str = None
    bstack1ll1ll1111_opy_: str = None
    bstack1ll11111l11_opy_: str = None
    bstack1l111l1ll1l_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll11lll11l_opy_ = bstack111lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤᔾ")
    bstack1l111l1llll_opy_ = bstack111lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᔿ")
    bstack1ll11l1l1ll_opy_ = bstack111lll_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦᕀ")
    bstack1l111l11lll_opy_ = bstack111lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥᕁ")
    bstack1l111ll11ll_opy_ = bstack111lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨᕂ")
    bstack1l1l1l1l1l1_opy_ = bstack111lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᕃ")
    bstack1l1ll1l1l1l_opy_ = bstack111lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨᕄ")
    bstack1l1llll11ll_opy_ = bstack111lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᕅ")
    bstack1ll11111l1l_opy_ = bstack111lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᕆ")
    bstack1l11l111lll_opy_ = bstack111lll_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᕇ")
    bstack1ll11ll11ll_opy_ = bstack111lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣᕈ")
    bstack1l1lll1l1ll_opy_ = bstack111lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᕉ")
    bstack1l1111lll1l_opy_ = bstack111lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢᕊ")
    bstack1l1ll111ll1_opy_ = bstack111lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢᕋ")
    bstack1ll1l11ll1l_opy_ = bstack111lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᕌ")
    bstack1l1l11ll1ll_opy_ = bstack111lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨᕍ")
    bstack1l111l11111_opy_ = bstack111lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧᕎ")
    bstack1l11l1l11l1_opy_ = bstack111lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧᕏ")
    bstack1l1111ll1ll_opy_ = bstack111lll_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨᕐ")
    bstack1l1111l111l_opy_ = bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩᕑ")
    bstack1l11lllll11_opy_ = bstack111lll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᕒ")
    bstack1l111l11ll1_opy_ = bstack111lll_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᕓ")
    bstack1l111l111l1_opy_ = bstack111lll_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᕔ")
    bstack1l11l1111l1_opy_ = bstack111lll_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤᕕ")
    bstack1l11ll11l1l_opy_ = bstack111lll_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢᕖ")
    bstack1l111ll1ll1_opy_ = bstack111lll_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨᕗ")
    bstack1l11l1l1l1l_opy_ = bstack111lll_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢᕘ")
    bstack1l11l111111_opy_ = bstack111lll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᕙ")
    bstack1l11l1111ll_opy_ = bstack111lll_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᕚ")
    bstack1l11ll11111_opy_ = bstack111lll_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᕛ")
    bstack1l11l11l1ll_opy_ = bstack111lll_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᕜ")
    bstack1l1ll1llll1_opy_ = bstack111lll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦᕝ")
    bstack1l1lll1111l_opy_ = bstack111lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧᕞ")
    bstack1ll111111l1_opy_ = bstack111lll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᕟ")
    bstack1lllll1ll11_opy_: Dict[str, bstack1lll1111l1l_opy_] = dict()
    bstack1l11111l111_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll11l1ll1l_opy_: List[str]
    bstack1l111l11l11_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll11l1ll1l_opy_: List[str],
        bstack1l111l11l11_opy_: Dict[str, str],
        bstack11111lll11_opy_: bstack11111ll11l_opy_
    ):
        self.bstack1ll11l1ll1l_opy_ = bstack1ll11l1ll1l_opy_
        self.bstack1l111l11l11_opy_ = bstack1l111l11l11_opy_
        self.bstack11111lll11_opy_ = bstack11111lll11_opy_
    def track_event(
        self,
        context: bstack1l11l1l1lll_opy_,
        test_framework_state: bstack1lll11lllll_opy_,
        test_hook_state: bstack1lllll1111l_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack111lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤᕠ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l111l1ll11_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11ll1ll1l_opy_ = TestFramework.bstack1l11ll11ll1_opy_(bstack11111l1l11_opy_)
        if not bstack1l11ll1ll1l_opy_ in TestFramework.bstack1l11111l111_opy_:
            return
        self.logger.debug(bstack111lll_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢᕡ").format(len(TestFramework.bstack1l11111l111_opy_[bstack1l11ll1ll1l_opy_])))
        for callback in TestFramework.bstack1l11111l111_opy_[bstack1l11ll1ll1l_opy_]:
            try:
                callback(self, instance, bstack11111l1l11_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack111lll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢᕢ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1llll1l1l_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1lll1ll1l_opy_(self, instance, bstack11111l1l11_opy_):
        return
    @abc.abstractmethod
    def bstack1l1lllll1ll_opy_(self, instance, bstack11111l1l11_opy_):
        return
    @staticmethod
    def bstack11111l11l1_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack11111l11ll_opy_.create_context(target)
        instance = TestFramework.bstack1lllll1ll11_opy_.get(ctx.id, None)
        if instance and instance.bstack11111l1111_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1lll11111_opy_(reverse=True) -> List[bstack1lll1111l1l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lllll1ll11_opy_.values(),
            ),
            key=lambda t: t.bstack111111ll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll1l11_opy_(ctx: bstack1llllllll11_opy_, reverse=True) -> List[bstack1lll1111l1l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lllll1ll11_opy_.values(),
            ),
            key=lambda t: t.bstack111111ll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111111ll_opy_(instance: bstack1lll1111l1l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llllll1l1l_opy_(instance: bstack1lll1111l1l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack11111ll111_opy_(instance: bstack1lll1111l1l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack111lll_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᕣ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l111l11_opy_(instance: bstack1lll1111l1l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack111lll_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤᕤ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l1111111ll_opy_(instance: bstack1lll11lllll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack111lll_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᕥ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack11111l11l1_opy_(target, strict)
        return TestFramework.bstack1llllll1l1l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack11111l11l1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111ll1111_opy_(instance: bstack1lll1111l1l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l111ll111l_opy_(instance: bstack1lll1111l1l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11ll11ll1_opy_(bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_]):
        return bstack111lll_opy_ (u"ࠦ࠿ࠨᕦ").join((bstack1lll11lllll_opy_(bstack11111l1l11_opy_[0]).name, bstack1lllll1111l_opy_(bstack11111l1l11_opy_[1]).name))
    @staticmethod
    def bstack1ll11ll1l1l_opy_(bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_], callback: Callable):
        bstack1l11ll1ll1l_opy_ = TestFramework.bstack1l11ll11ll1_opy_(bstack11111l1l11_opy_)
        TestFramework.logger.debug(bstack111lll_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥᕧ").format(bstack1l11ll1ll1l_opy_))
        if not bstack1l11ll1ll1l_opy_ in TestFramework.bstack1l11111l111_opy_:
            TestFramework.bstack1l11111l111_opy_[bstack1l11ll1ll1l_opy_] = []
        TestFramework.bstack1l11111l111_opy_[bstack1l11ll1ll1l_opy_].append(callback)
    @staticmethod
    def bstack1ll1111ll11_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳࠣᕨ"):
            return klass.__qualname__
        return module + bstack111lll_opy_ (u"ࠢ࠯ࠤᕩ") + klass.__qualname__
    @staticmethod
    def bstack1ll1111l1l1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}