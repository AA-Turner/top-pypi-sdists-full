# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1lll11l111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1ll_opy_ import bstack1ll1llll111_opy_, bstack1ll1ll1llll_opy_
class bstack1l1lllll1ll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11l11_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢត").format(self.name)
class bstack1l1lllllll1_opy_(Enum):
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
        return bstack11l11_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨថ").format(self.name)
class bstack1ll11l111ll_opy_(bstack1ll1llll111_opy_):
    bstack1l1l1l11l1l_opy_: List[str]
    bstack11ll111lll1_opy_: Dict[str, str]
    state: bstack1l1lllllll1_opy_
    bstack1ll1llll11l_opy_: datetime
    bstack1ll1ll111l1_opy_: datetime
    def __init__(
        self,
        context: bstack1ll1ll1llll_opy_,
        bstack1l1l1l11l1l_opy_: List[str],
        bstack11ll111lll1_opy_: Dict[str, str],
        state=bstack1l1lllllll1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1l1l1l11l1l_opy_ = bstack1l1l1l11l1l_opy_
        self.bstack11ll111lll1_opy_ = bstack11ll111lll1_opy_
        self.state = state
        self.bstack1ll1llll11l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll1ll111l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1ll1lll111l_opy_(self, bstack1ll1ll1ll11_opy_: bstack1l1lllllll1_opy_):
        bstack1lll11111l1_opy_ = bstack1l1lllllll1_opy_(bstack1ll1ll1ll11_opy_).name
        if not bstack1lll11111l1_opy_:
            return False
        if bstack1ll1ll1ll11_opy_ == self.state:
            return False
        self.state = bstack1ll1ll1ll11_opy_
        self.bstack1ll1ll111l1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack11ll1l1llll_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1l1lll1l11l_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l111ll11l1_opy_: int = None
    bstack1l11l11ll1l_opy_: str = None
    bstack1111l1_opy_: str = None
    bstack1ll1l1111l_opy_: str = None
    bstack1l111lll1l1_opy_: str = None
    bstack11ll1ll1l11_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l1l11l11l1_opy_ = bstack11l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤទ")
    bstack11ll1ll11ll_opy_ = bstack11l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣធ")
    bstack1l1ll11111l_opy_ = bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦន")
    bstack11ll111l1l1_opy_ = bstack11l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥប")
    bstack11ll1l11lll_opy_ = bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨផ")
    bstack1l111111l1l_opy_ = bstack11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤព")
    bstack1l111llll1l_opy_ = bstack11l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨភ")
    bstack1l111ll1l1l_opy_ = bstack11l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣម")
    bstack1l11l1ll111_opy_ = bstack11l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢយ")
    bstack11ll1l111ll_opy_ = bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣរ")
    bstack1l1l1l11l11_opy_ = bstack11l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣល")
    bstack1l11l111l11_opy_ = bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧវ")
    bstack11ll11l1l11_opy_ = bstack11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢឝ")
    bstack1l111l11111_opy_ = bstack11l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢឞ")
    bstack1l1l111l11l_opy_ = bstack11l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢស")
    bstack1l111111111_opy_ = bstack11l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨហ")
    bstack11ll11l11l1_opy_ = bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧឡ")
    bstack11ll111llll_opy_ = bstack11l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧអ")
    bstack11ll1l1ll1l_opy_ = bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨឣ")
    bstack11l1ll11111_opy_ = bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩឤ")
    bstack11lll11ll11_opy_ = bstack11l11_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨឥ")
    bstack11ll11l1l1l_opy_ = bstack11l11_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤឦ")
    bstack11l1llll111_opy_ = bstack11l11_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣឧ")
    bstack11l1ll1l11l_opy_ = bstack11l11_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤឨ")
    bstack11ll111ll1l_opy_ = bstack11l11_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢឩ")
    bstack11l1ll1ll1l_opy_ = bstack11l11_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨឪ")
    bstack11l1llll11l_opy_ = bstack11l11_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢឫ")
    bstack11ll11ll1l1_opy_ = bstack11l11_opy_ (u"ࠧࡲ࡯ࡨࡵࠥឬ")
    bstack11ll1ll1111_opy_ = bstack11l11_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣឭ")
    bstack11ll11lll11_opy_ = bstack11l11_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣឮ")
    bstack11ll1lll111_opy_ = bstack11l11_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤឯ")
    bstack1l111lll111_opy_ = bstack11l11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦឰ")
    bstack1l11ll1l111_opy_ = bstack11l11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧឱ")
    bstack1l111ll1l11_opy_ = bstack11l11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨឲ")
    bstack1lll111l1l1_opy_: Dict[str, bstack1ll11l111ll_opy_] = dict()
    bstack11l1l1l1l1l_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l1l11l1l_opy_: List[str]
    bstack11ll111lll1_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1l1l11l1l_opy_: List[str],
        bstack11ll111lll1_opy_: Dict[str, str],
        bstack1lll111lll1_opy_: bstack1lll11l111l_opy_
    ):
        self.bstack1l1l1l11l1l_opy_ = bstack1l1l1l11l1l_opy_
        self.bstack11ll111lll1_opy_ = bstack11ll111lll1_opy_
        self.bstack1lll111lll1_opy_ = bstack1lll111lll1_opy_
    def track_event(
        self,
        context: bstack11ll1l1llll_opy_,
        test_framework_state: bstack1l1lllllll1_opy_,
        test_hook_state: bstack1l1lllll1ll_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11l11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤឳ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11l1lll1lll_opy_(
        self,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack11ll1llll11_opy_ = TestFramework.bstack11ll1llll1l_opy_(bstack1ll1l1lll1l_opy_)
        if not bstack11ll1llll11_opy_ in TestFramework.bstack11l1l1l1l1l_opy_:
            return
        self.logger.debug(bstack11l11_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢ឴").format(len(TestFramework.bstack11l1l1l1l1l_opy_[bstack11ll1llll11_opy_])))
        for callback in TestFramework.bstack11l1l1l1l1l_opy_[bstack11ll1llll11_opy_]:
            try:
                callback(self, instance, bstack1ll1l1lll1l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢ឵").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l11l1lll1l_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l11l11lll1_opy_(self, instance, bstack1ll1l1lll1l_opy_):
        return
    @abc.abstractmethod
    def bstack1l111llll11_opy_(self, instance, bstack1ll1l1lll1l_opy_):
        return
    @staticmethod
    def bstack1ll1ll11111_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1ll1llll111_opy_.create_context(target)
        instance = TestFramework.bstack1lll111l1l1_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll1lll1111_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l11ll1111l_opy_(reverse=True) -> List[bstack1ll11l111ll_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lll111l1l1_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1llll11l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1ll1l1l1_opy_(ctx: bstack1ll1ll1llll_opy_, reverse=True) -> List[bstack1ll11l111ll_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lll111l1l1_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1llll11l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l1lll11_opy_(instance: bstack1ll11l111ll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lll111111l_opy_(instance: bstack1ll11l111ll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1ll1lll111l_opy_(instance: bstack1ll11l111ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l11_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧា").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11ll1l11l1l_opy_(instance: bstack1ll11l111ll_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11l11_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤិ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11l1l1l11ll_opy_(instance: bstack1l1lllllll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l11_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥី").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1ll1ll11111_opy_(target, strict)
        return TestFramework.bstack1lll111111l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1ll1ll11111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11ll1111lll_opy_(instance: bstack1ll11l111ll_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11ll1111l11_opy_(instance: bstack1ll11l111ll_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11ll1llll1l_opy_(bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_]):
        return bstack11l11_opy_ (u"ࠦ࠿ࠨឹ").join((bstack1l1lllllll1_opy_(bstack1ll1l1lll1l_opy_[0]).name, bstack1l1lllll1ll_opy_(bstack1ll1l1lll1l_opy_[1]).name))
    @staticmethod
    def bstack1l1l1l111ll_opy_(bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_], callback: Callable):
        bstack11ll1llll11_opy_ = TestFramework.bstack11ll1llll1l_opy_(bstack1ll1l1lll1l_opy_)
        TestFramework.logger.debug(bstack11l11_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥឺ").format(bstack11ll1llll11_opy_))
        if not bstack11ll1llll11_opy_ in TestFramework.bstack11l1l1l1l1l_opy_:
            TestFramework.bstack11l1l1l1l1l_opy_[bstack11ll1llll11_opy_] = []
        TestFramework.bstack11l1l1l1l1l_opy_[bstack11ll1llll11_opy_].append(callback)
    @staticmethod
    def bstack1l11ll1l1l1_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳࠣុ"):
            return klass.__qualname__
        return module + bstack11l11_opy_ (u"ࠢ࠯ࠤូ") + klass.__qualname__
    @staticmethod
    def bstack1l11ll1ll11_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}