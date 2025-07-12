# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1ll1lll1lll_opy_ import bstack1l1lll111ll_opy_, bstack1ll1ll1l11l_opy_
import os
import threading
class bstack1llllll1l1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11l1111_opy_ (u"ࠣࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᑄ").format(self.name)
class bstack1lll1llllll_opy_(Enum):
    NONE = 0
    bstack1ll1ll1ll1l_opy_ = 1
    bstack1ll1l1ll11l_opy_ = 3
    bstack1llll1lll11_opy_ = 4
    bstack1l11lllll11_opy_ = 5
    QUIT = 6
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11l1111_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᑅ").format(self.name)
class bstack1lll1llll11_opy_(bstack1l1lll111ll_opy_):
    framework_name: str
    framework_version: str
    state: bstack1lll1llllll_opy_
    previous_state: bstack1lll1llllll_opy_
    bstack1ll1lll1l11_opy_: datetime
    bstack1l1l111ll11_opy_: datetime
    def __init__(
        self,
        context: bstack1ll1ll1l11l_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1lll1llllll_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1lll1llllll_opy_.NONE
        self.bstack1ll1lll1l11_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1l111ll11_opy_ = datetime.now(tz=timezone.utc)
    def bstack1llll111l11_opy_(self, bstack1l1l111l1l1_opy_: bstack1lll1llllll_opy_):
        bstack1l1l111ll1l_opy_ = bstack1lll1llllll_opy_(bstack1l1l111l1l1_opy_).name
        if not bstack1l1l111ll1l_opy_:
            return False
        if bstack1l1l111l1l1_opy_ == self.state:
            return False
        if self.state == bstack1lll1llllll_opy_.bstack1ll1l1ll11l_opy_: # bstack1l11lll1l1l_opy_ bstack1l11lll11l1_opy_ for bstack1l11lllllll_opy_ in bstack1l1l11111l1_opy_, it bstack1l11lll1ll1_opy_ bstack1l11llllll1_opy_ bstack1l11llll111_opy_ times bstack1l11llll11l_opy_ a new state
            return True
        if (
            bstack1l1l111l1l1_opy_ == bstack1lll1llllll_opy_.NONE
            or (self.state != bstack1lll1llllll_opy_.NONE and bstack1l1l111l1l1_opy_ == bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_)
            or (self.state < bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_ and bstack1l1l111l1l1_opy_ == bstack1lll1llllll_opy_.bstack1llll1lll11_opy_)
            or (self.state < bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_ and bstack1l1l111l1l1_opy_ == bstack1lll1llllll_opy_.QUIT)
        ):
            raise ValueError(bstack11l1111_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡺࡡࡵࡧࠣࡸࡷࡧ࡮ࡴ࡫ࡷ࡭ࡴࡴ࠺ࠡࠤᑆ") + str(self.state) + bstack11l1111_opy_ (u"ࠦࠥࡃ࠾ࠡࠤᑇ") + str(bstack1l1l111l1l1_opy_))
        self.previous_state = self.state
        self.state = bstack1l1l111l1l1_opy_
        self.bstack1l1l111ll11_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1ll1lllll11_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll11llllll_opy_: Dict[str, bstack1lll1llll11_opy_] = dict()
    framework_name: str
    framework_version: str
    classes: List[Type]
    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
    ):
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.classes = classes
    @abc.abstractmethod
    def bstack1ll1111l11l_opy_(self, instance: bstack1lll1llll11_opy_, method_name: str, bstack1ll11111l1l_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1ll1111111l_opy_(
        self, method_name, previous_state: bstack1lll1llllll_opy_, *args, **kwargs
    ) -> bstack1lll1llllll_opy_:
        return
    @abc.abstractmethod
    def bstack1ll11111ll1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1l1lllllll1_opy_(self, bstack1l11llll1ll_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1l11llll1ll_opy_:
                bstack1l11lll1lll_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1l11lll1lll_opy_):
                    self.logger.warning(bstack11l1111_opy_ (u"ࠧࡻ࡮ࡱࡣࡷࡧ࡭࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࠥᑈ") + str(method_name) + bstack11l1111_opy_ (u"ࠨࠢᑉ"))
                    continue
                bstack1l1lllll1ll_opy_ = self.bstack1ll1111111l_opy_(
                    method_name, previous_state=bstack1lll1llllll_opy_.NONE
                )
                bstack1l11lll11ll_opy_ = self.bstack1l1l111111l_opy_(
                    method_name,
                    (bstack1l1lllll1ll_opy_ if bstack1l1lllll1ll_opy_ else bstack1lll1llllll_opy_.NONE),
                    bstack1l11lll1lll_opy_,
                )
                if not callable(bstack1l11lll11ll_opy_):
                    self.logger.warning(bstack11l1111_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠠ࡯ࡱࡷࠤࡵࡧࡴࡤࡪࡨࡨ࠿ࠦࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࠨࡼࡵࡨࡰ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽ࠻ࠢࠥᑊ") + str(self.framework_version) + bstack11l1111_opy_ (u"ࠣࠫࠥᑋ"))
                    continue
                setattr(clazz, method_name, bstack1l11lll11ll_opy_)
    def bstack1l1l111111l_opy_(
        self,
        method_name: str,
        bstack1l1lllll1ll_opy_: bstack1lll1llllll_opy_,
        bstack1l11lll1lll_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1ll1l1l1_opy_ = datetime.now()
            (bstack1l1lllll1ll_opy_,) = wrapped.__vars__
            bstack1l1lllll1ll_opy_ = (
                bstack1l1lllll1ll_opy_
                if bstack1l1lllll1ll_opy_ and bstack1l1lllll1ll_opy_ != bstack1lll1llllll_opy_.NONE
                else self.bstack1ll1111111l_opy_(method_name, previous_state=bstack1l1lllll1ll_opy_, *args, **kwargs)
            )
            if bstack1l1lllll1ll_opy_ == bstack1lll1llllll_opy_.bstack1ll1ll1ll1l_opy_:
                ctx = bstack1l1lll111ll_opy_.create_context(self.bstack1l11lllll1l_opy_(target))
                if not self.bstack1l11llll1l1_opy_() or ctx.id not in bstack1ll1lllll11_opy_.bstack1ll11llllll_opy_:
                    bstack1ll1lllll11_opy_.bstack1ll11llllll_opy_[ctx.id] = bstack1lll1llll11_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1l1lllll1ll_opy_
                    )
                self.logger.debug(bstack11l1111_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣࡧࡷ࡫ࡡࡵࡧࡧ࠾ࠥࢁࡴࡢࡴࡪࡩࡹ࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡤࡶࡻࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᑌ") + str(bstack1ll1lllll11_opy_.bstack1ll11llllll_opy_.keys()) + bstack11l1111_opy_ (u"ࠥࠦᑍ"))
            else:
                self.logger.debug(bstack11l1111_opy_ (u"ࠦࡼࡸࡡࡱࡲࡨࡨࠥࡳࡥࡵࡪࡲࡨࠥ࡯࡮ࡷࡱ࡮ࡩࡩࡀࠠࡼࡶࡤࡶ࡬࡫ࡴ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᑎ") + str(bstack1ll1lllll11_opy_.bstack1ll11llllll_opy_.keys()) + bstack11l1111_opy_ (u"ࠧࠨᑏ"))
            instance = bstack1ll1lllll11_opy_.bstack1l1l1lllll1_opy_(self.bstack1l11lllll1l_opy_(target))
            if bstack1l1lllll1ll_opy_ == bstack1lll1llllll_opy_.NONE or not instance:
                ctx = bstack1l1lll111ll_opy_.create_context(self.bstack1l11lllll1l_opy_(target))
                self.logger.warning(bstack11l1111_opy_ (u"ࠨࡷࡳࡣࡳࡴࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡶࡰࡷࡶࡦࡩ࡫ࡦࡦ࠽ࠤࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡧࡹࡾ࠽ࡼࡥࡷࡼࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᑐ") + str(bstack1ll1lllll11_opy_.bstack1ll11llllll_opy_.keys()) + bstack11l1111_opy_ (u"ࠢࠣᑑ"))
                return bstack1l11lll1lll_opy_(target, *args, **kwargs)
            bstack1lll11111l1_opy_ = self.bstack1ll11111ll1_opy_(
                target,
                (instance, method_name),
                (bstack1l1lllll1ll_opy_, bstack1llllll1l1l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1llll111l11_opy_(bstack1l1lllll1ll_opy_):
                self.logger.debug(bstack11l1111_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡥࡥࠢࡶࡸࡦࡺࡥ࠮ࡶࡵࡥࡳࡹࡩࡵ࡫ࡲࡲ࠿ࠦࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡳࡶࡪࡼࡩࡰࡷࡶࡣࡸࡺࡡࡵࡧࢀࠤࡂࡄࠠࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡷࡹࡧࡴࡦࡿࠣࠬࢀࡺࡹࡱࡧࠫࡸࡦࡸࡧࡦࡶࠬࢁ࠳ࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥࢁࡡࡳࡩࡶࢁ࠮࡛ࠦࠣᑒ") + str(instance.ref()) + bstack11l1111_opy_ (u"ࠤࡠࠦᑓ"))
            result = (
                bstack1lll11111l1_opy_(target, bstack1l11lll1lll_opy_, *args, **kwargs)
                if callable(bstack1lll11111l1_opy_)
                else bstack1l11lll1lll_opy_(target, *args, **kwargs)
            )
            bstack1l11lll1l11_opy_ = self.bstack1ll11111ll1_opy_(
                target,
                (instance, method_name),
                (bstack1l1lllll1ll_opy_, bstack1llllll1l1l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1ll1111l11l_opy_(instance, method_name, datetime.now() - bstack1ll1l1l1_opy_, *args, **kwargs)
            return bstack1l11lll1l11_opy_ if bstack1l11lll1l11_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1l1lllll1ll_opy_,)
        return wrapped
    @staticmethod
    def bstack1l1l1lllll1_opy_(target: object, strict=True):
        ctx = bstack1l1lll111ll_opy_.create_context(target)
        instance = bstack1ll1lllll11_opy_.bstack1ll11llllll_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1l111l11l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1lllll1111l_opy_(
        ctx: bstack1ll1ll1l11l_opy_, state: bstack1lll1llllll_opy_, reverse=True
    ) -> List[bstack1lll1llll11_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1ll1lllll11_opy_.bstack1ll11llllll_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1lll1l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll1ll1_opy_(instance: bstack1lll1llll11_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lllll1l11l_opy_(instance: bstack1lll1llll11_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1llll111l11_opy_(instance: bstack1lll1llll11_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1ll1lllll11_opy_.logger.debug(bstack11l1111_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥࡱࡥࡺ࠿ࡾ࡯ࡪࡿࡽࠡࡸࡤࡰࡺ࡫࠽ࠣᑔ") + str(value) + bstack11l1111_opy_ (u"ࠦࠧᑕ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1ll1lllll11_opy_.bstack1l1l1lllll1_opy_(target, strict)
        return bstack1ll1lllll11_opy_.bstack1lllll1l11l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1ll1lllll11_opy_.bstack1l1l1lllll1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1l11llll1l1_opy_(self):
        return self.framework_name == bstack11l1111_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᑖ")
    def bstack1l11lllll1l_opy_(self, target):
        return target if not self.bstack1l11llll1l1_opy_() else self.bstack1l1l1111111_opy_()
    @staticmethod
    def bstack1l1l1111111_opy_():
        return str(os.getpid()) + str(threading.get_ident())