# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack111111l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11l1_opy_ import bstack1llllll11ll_opy_, bstack1lllll1ll1l_opy_
class bstack1lll1lll111_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1l1l1_opy_ (u"࡚ࠧࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᕋ").format(self.name)
class bstack1ll1ll11l11_opy_(Enum):
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
        return bstack1l1l1l1_opy_ (u"ࠨࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᕌ").format(self.name)
class bstack1lll1l1l1l1_opy_(bstack1llllll11ll_opy_):
    bstack1ll1l111ll1_opy_: List[str]
    bstack1l11l11111l_opy_: Dict[str, str]
    state: bstack1ll1ll11l11_opy_
    bstack1lllll111ll_opy_: datetime
    bstack1lllll11l11_opy_: datetime
    def __init__(
        self,
        context: bstack1lllll1ll1l_opy_,
        bstack1ll1l111ll1_opy_: List[str],
        bstack1l11l11111l_opy_: Dict[str, str],
        state=bstack1ll1ll11l11_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l111ll1_opy_ = bstack1ll1l111ll1_opy_
        self.bstack1l11l11111l_opy_ = bstack1l11l11111l_opy_
        self.state = state
        self.bstack1lllll111ll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lllll11l11_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lllll1111l_opy_(self, bstack1llllll111l_opy_: bstack1ll1ll11l11_opy_):
        bstack111111111l_opy_ = bstack1ll1ll11l11_opy_(bstack1llllll111l_opy_).name
        if not bstack111111111l_opy_:
            return False
        if bstack1llllll111l_opy_ == self.state:
            return False
        self.state = bstack1llllll111l_opy_
        self.bstack1lllll11l11_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l1111l1l1l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll111l1l1_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1ll11llll_opy_: int = None
    bstack1l1llll1l1l_opy_: str = None
    bstack111l1l1_opy_: str = None
    bstack1l1ll11ll_opy_: str = None
    bstack1l1ll1ll11l_opy_: str = None
    bstack1l11l1l1l11_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1l11lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥᕍ")
    bstack1l11l111l11_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡩࡥࠤᕎ")
    bstack1ll111llll1_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠧᕏ")
    bstack1l11l11l11l_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠦᕐ")
    bstack1l1111ll111_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡷࡥ࡬ࡹࠢᕑ")
    bstack1l1l111ll11_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᕒ")
    bstack1l1lll1l11l_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡣࡦࡺࠢᕓ")
    bstack1l1l1llll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᕔ")
    bstack1l1lll1l111_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᕕ")
    bstack1l11l11l111_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᕖ")
    bstack1ll1l11l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠤᕗ")
    bstack1l1ll1111l1_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᕘ")
    bstack1l11l1l11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡧࡴࡪࡥࠣᕙ")
    bstack1l1l1lll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠣᕚ")
    bstack1ll111ll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᕛ")
    bstack1l1l111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠢᕜ")
    bstack1l111lllll1_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪࠨᕝ")
    bstack1l111l1lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲ࡫ࡸࠨᕞ")
    bstack1l111ll1l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡰࡩࡹࡧࠢᕟ")
    bstack1l1111111ll_opy_ = bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡷࡨࡵࡰࡦࡵࠪᕠ")
    bstack1l11ll1l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢᕡ")
    bstack1l1111ll1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᕢ")
    bstack1l1111l111l_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᕣ")
    bstack1l11l11l1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡪࡦࠥᕤ")
    bstack1l111l1l111_opy_ = bstack1l1l1l1_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡨࡷࡺࡲࡴࠣᕥ")
    bstack1l11111ll11_opy_ = bstack1l1l1l1_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡯ࡳ࡬ࡹࠢᕦ")
    bstack1l11l1111l1_opy_ = bstack1l1l1l1_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠣᕧ")
    bstack1l1111lll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᕨ")
    bstack1l111ll1lll_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᕩ")
    bstack1l11l11ll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᕪ")
    bstack1l111l1ll11_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᕫ")
    bstack1l1ll1lllll_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠧᕬ")
    bstack1l1ll111lll_opy_ = bstack1l1l1l1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡏࡓࡌࠨᕭ")
    bstack1l1ll1l1lll_opy_ = bstack1l1l1l1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᕮ")
    bstack1llllllll11_opy_: Dict[str, bstack1lll1l1l1l1_opy_] = dict()
    bstack11lllll1l1l_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l111ll1_opy_: List[str]
    bstack1l11l11111l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l111ll1_opy_: List[str],
        bstack1l11l11111l_opy_: Dict[str, str],
        bstack111111lll1_opy_: bstack111111l1l1_opy_
    ):
        self.bstack1ll1l111ll1_opy_ = bstack1ll1l111ll1_opy_
        self.bstack1l11l11111l_opy_ = bstack1l11l11111l_opy_
        self.bstack111111lll1_opy_ = bstack111111lll1_opy_
    def track_event(
        self,
        context: bstack1l1111l1l1l_opy_,
        test_framework_state: bstack1ll1ll11l11_opy_,
        test_hook_state: bstack1lll1lll111_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡡࡳࡩࡶࡁࢀࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼࡿࠥᕯ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l111l11l11_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11l1ll1ll_opy_ = TestFramework.bstack1l11l1lllll_opy_(bstack1lllll11ll1_opy_)
        if not bstack1l11l1ll1ll_opy_ in TestFramework.bstack11lllll1l1l_opy_:
            return
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡾࢁࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠣᕰ").format(len(TestFramework.bstack11lllll1l1l_opy_[bstack1l11l1ll1ll_opy_])))
        for callback in TestFramework.bstack11lllll1l1l_opy_[bstack1l11l1ll1ll_opy_]:
            try:
                callback(self, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࢁࡽࠣᕱ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1ll1l1l11_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1lll1111l_opy_(self, instance, bstack1lllll11ll1_opy_):
        return
    @abc.abstractmethod
    def bstack1l1lll11l11_opy_(self, instance, bstack1lllll11ll1_opy_):
        return
    @staticmethod
    def bstack1llllllllll_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1llllll11ll_opy_.create_context(target)
        instance = TestFramework.bstack1llllllll11_opy_.get(ctx.id, None)
        if instance and instance.bstack1llllll1ll1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1ll111l11_opy_(reverse=True) -> List[bstack1lll1l1l1l1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1llllllll11_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll111ll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llll1lll11_opy_(ctx: bstack1lllll1ll1l_opy_, reverse=True) -> List[bstack1lll1l1l1l1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1llllllll11_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll111ll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllllll1ll_opy_(instance: bstack1lll1l1l1l1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lllll1ll11_opy_(instance: bstack1lll1l1l1l1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lllll1111l_opy_(instance: bstack1lll1l1l1l1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨᕲ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11111ll1l_opy_(instance: bstack1lll1l1l1l1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦࡥ࡯ࡶࡵ࡭ࡪࡹ࠽ࡼࡿࠥᕳ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11lllll1l11_opy_(instance: bstack1ll1ll11l11_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢ࡮ࡩࡾࡃࡻࡾࠢࡹࡥࡱࡻࡥ࠾ࡽࢀࠦᕴ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1llllllllll_opy_(target, strict)
        return TestFramework.bstack1lllll1ll11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1llllllllll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l111l1l_opy_(instance: bstack1lll1l1l1l1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l111l1l1ll_opy_(instance: bstack1lll1l1l1l1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11l1lllll_opy_(bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_]):
        return bstack1l1l1l1_opy_ (u"ࠧࡀࠢᕵ").join((bstack1ll1ll11l11_opy_(bstack1lllll11ll1_opy_[0]).name, bstack1lll1lll111_opy_(bstack1lllll11ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll111lll1l_opy_(bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_], callback: Callable):
        bstack1l11l1ll1ll_opy_ = TestFramework.bstack1l11l1lllll_opy_(bstack1lllll11ll1_opy_)
        TestFramework.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡶࡢ࡬ࡴࡵ࡫ࡠࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤ࡭ࡵ࡯࡬ࡡࡵࡩ࡬࡯ࡳࡵࡴࡼࡣࡰ࡫ࡹ࠾ࡽࢀࠦᕶ").format(bstack1l11l1ll1ll_opy_))
        if not bstack1l11l1ll1ll_opy_ in TestFramework.bstack11lllll1l1l_opy_:
            TestFramework.bstack11lllll1l1l_opy_[bstack1l11l1ll1ll_opy_] = []
        TestFramework.bstack11lllll1l1l_opy_[bstack1l11l1ll1ll_opy_].append(callback)
    @staticmethod
    def bstack1l1llllllll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡹ࡯࡮ࡴࠤᕷ"):
            return klass.__qualname__
        return module + bstack1l1l1l1_opy_ (u"ࠣ࠰ࠥᕸ") + klass.__qualname__
    @staticmethod
    def bstack1l1ll1ll1ll_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}