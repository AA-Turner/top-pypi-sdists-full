# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import bstack111111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack111111l111_opy_ import bstack1llllll1l1l_opy_, bstack1lllllll1l1_opy_
class bstack1ll1l1lll11_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11ll11_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᕊ").format(self.name)
class bstack1llll11111l_opy_(Enum):
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
        return bstack11ll11_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᕋ").format(self.name)
class bstack1llll111l11_opy_(bstack1llllll1l1l_opy_):
    bstack1ll11l11l1l_opy_: List[str]
    bstack1l111l111ll_opy_: Dict[str, str]
    state: bstack1llll11111l_opy_
    bstack1lllll11l11_opy_: datetime
    bstack1lllll1l1l1_opy_: datetime
    def __init__(
        self,
        context: bstack1lllllll1l1_opy_,
        bstack1ll11l11l1l_opy_: List[str],
        bstack1l111l111ll_opy_: Dict[str, str],
        state=bstack1llll11111l_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll11l11l1l_opy_ = bstack1ll11l11l1l_opy_
        self.bstack1l111l111ll_opy_ = bstack1l111l111ll_opy_
        self.state = state
        self.bstack1lllll11l11_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lllll1l1l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1llllllllll_opy_(self, bstack1llllll1lll_opy_: bstack1llll11111l_opy_):
        bstack1lllll111l1_opy_ = bstack1llll11111l_opy_(bstack1llllll1lll_opy_).name
        if not bstack1lllll111l1_opy_:
            return False
        if bstack1llllll1lll_opy_ == self.state:
            return False
        self.state = bstack1llllll1lll_opy_
        self.bstack1lllll1l1l1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11l11l1l1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll11lll11_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1lll1ll1l_opy_: int = None
    bstack1l1ll1l1lll_opy_: str = None
    bstack1llll11_opy_: str = None
    bstack1l1llll1l_opy_: str = None
    bstack1l1l1lllll1_opy_: str = None
    bstack1l11l111l1l_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1l11ll11_opy_ = bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤᕌ")
    bstack1l11l1l1ll1_opy_ = bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᕍ")
    bstack1ll1l111l1l_opy_ = bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦᕎ")
    bstack1l111l11111_opy_ = bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥᕏ")
    bstack1l111l1llll_opy_ = bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨᕐ")
    bstack1l1l11l11l1_opy_ = bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᕑ")
    bstack1l1llll11ll_opy_ = bstack11ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨᕒ")
    bstack1l1lll1lll1_opy_ = bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᕓ")
    bstack1l1lll1l111_opy_ = bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᕔ")
    bstack1l11111l11l_opy_ = bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᕕ")
    bstack1ll11l11lll_opy_ = bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣᕖ")
    bstack1l1ll1l11ll_opy_ = bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᕗ")
    bstack1l111l111l1_opy_ = bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢᕘ")
    bstack1l1l1ll11ll_opy_ = bstack11ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢᕙ")
    bstack1ll1l11111l_opy_ = bstack11ll11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᕚ")
    bstack1l1l11l1lll_opy_ = bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨᕛ")
    bstack1l1111ll1l1_opy_ = bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧᕜ")
    bstack1l111lll1l1_opy_ = bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧᕝ")
    bstack1l11111ll11_opy_ = bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨᕞ")
    bstack1l111111l11_opy_ = bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩᕟ")
    bstack1l11ll1l1ll_opy_ = bstack11ll11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᕠ")
    bstack1l1111ll11l_opy_ = bstack11ll11_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᕡ")
    bstack1l111lll1ll_opy_ = bstack11ll11_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᕢ")
    bstack1l111111ll1_opy_ = bstack11ll11_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤᕣ")
    bstack1l1111l1111_opy_ = bstack11ll11_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢᕤ")
    bstack1l1111lllll_opy_ = bstack11ll11_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨᕥ")
    bstack1l11l1l11ll_opy_ = bstack11ll11_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢᕦ")
    bstack1l111l11lll_opy_ = bstack11ll11_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᕧ")
    bstack1l111ll11l1_opy_ = bstack11ll11_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᕨ")
    bstack1l111111l1l_opy_ = bstack11ll11_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᕩ")
    bstack1l1111l1ll1_opy_ = bstack11ll11_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᕪ")
    bstack1l1lll1111l_opy_ = bstack11ll11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦᕫ")
    bstack1l1ll1111l1_opy_ = bstack11ll11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧᕬ")
    bstack1l1llll111l_opy_ = bstack11ll11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᕭ")
    bstack1lllllll111_opy_: Dict[str, bstack1llll111l11_opy_] = dict()
    bstack11lllllll11_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll11l11l1l_opy_: List[str]
    bstack1l111l111ll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll11l11l1l_opy_: List[str],
        bstack1l111l111ll_opy_: Dict[str, str],
        bstack111111l1ll_opy_: bstack111111ll1l_opy_
    ):
        self.bstack1ll11l11l1l_opy_ = bstack1ll11l11l1l_opy_
        self.bstack1l111l111ll_opy_ = bstack1l111l111ll_opy_
        self.bstack111111l1ll_opy_ = bstack111111l1ll_opy_
    def track_event(
        self,
        context: bstack1l11l11l1l1_opy_,
        test_framework_state: bstack1llll11111l_opy_,
        test_hook_state: bstack1ll1l1lll11_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤᕮ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11111ll1l_opy_(
        self,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11l1l1lll_opy_ = TestFramework.bstack1l11l1ll11l_opy_(bstack111111111l_opy_)
        if not bstack1l11l1l1lll_opy_ in TestFramework.bstack11lllllll11_opy_:
            return
        self.logger.debug(bstack11ll11_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢᕯ").format(len(TestFramework.bstack11lllllll11_opy_[bstack1l11l1l1lll_opy_])))
        for callback in TestFramework.bstack11lllllll11_opy_[bstack1l11l1l1lll_opy_]:
            try:
                callback(self, instance, bstack111111111l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11ll11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢᕰ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1llllllll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1ll1l11l1_opy_(self, instance, bstack111111111l_opy_):
        return
    @abc.abstractmethod
    def bstack1l1ll1l1l11_opy_(self, instance, bstack111111111l_opy_):
        return
    @staticmethod
    def bstack11111111l1_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1llllll1l1l_opy_.create_context(target)
        instance = TestFramework.bstack1lllllll111_opy_.get(ctx.id, None)
        if instance and instance.bstack1lllll1l11l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1ll1ll111_opy_(reverse=True) -> List[bstack1llll111l11_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lllllll111_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll11l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll111l_opy_(ctx: bstack1lllllll1l1_opy_, reverse=True) -> List[bstack1llll111l11_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lllllll111_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll11l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllll1l111_opy_(instance: bstack1llll111l11_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lllll1l1ll_opy_(instance: bstack1llll111l11_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1llllllllll_opy_(instance: bstack1llll111l11_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11ll11_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᕱ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1111lll11_opy_(instance: bstack1llll111l11_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11ll11_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤᕲ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11lllll1l11_opy_(instance: bstack1llll11111l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11ll11_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᕳ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack11111111l1_opy_(target, strict)
        return TestFramework.bstack1lllll1l1ll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack11111111l1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1111l11l1_opy_(instance: bstack1llll111l11_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l111ll111l_opy_(instance: bstack1llll111l11_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11l1ll11l_opy_(bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_]):
        return bstack11ll11_opy_ (u"ࠦ࠿ࠨᕴ").join((bstack1llll11111l_opy_(bstack111111111l_opy_[0]).name, bstack1ll1l1lll11_opy_(bstack111111111l_opy_[1]).name))
    @staticmethod
    def bstack1ll1l11l1l1_opy_(bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_], callback: Callable):
        bstack1l11l1l1lll_opy_ = TestFramework.bstack1l11l1ll11l_opy_(bstack111111111l_opy_)
        TestFramework.logger.debug(bstack11ll11_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥᕵ").format(bstack1l11l1l1lll_opy_))
        if not bstack1l11l1l1lll_opy_ in TestFramework.bstack11lllllll11_opy_:
            TestFramework.bstack11lllllll11_opy_[bstack1l11l1l1lll_opy_] = []
        TestFramework.bstack11lllllll11_opy_[bstack1l11l1l1lll_opy_].append(callback)
    @staticmethod
    def bstack1l1ll11l111_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳࠣᕶ"):
            return klass.__qualname__
        return module + bstack11ll11_opy_ (u"ࠢ࠯ࠤᕷ") + klass.__qualname__
    @staticmethod
    def bstack1l1ll1lll1l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}