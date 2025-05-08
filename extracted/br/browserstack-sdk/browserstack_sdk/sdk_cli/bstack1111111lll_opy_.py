# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import bstack11111111ll_opy_, bstack11111l1ll1_opy_
import os
import threading
class bstack11111lll1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1lll_opy_ (u"ࠦࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥဘ").format(self.name)
class bstack1llllllllll_opy_(Enum):
    NONE = 0
    bstack1111l11lll_opy_ = 1
    bstack11111111l1_opy_ = 3
    bstack1111l11111_opy_ = 4
    bstack11111ll1l1_opy_ = 5
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
        return bstack1l1lll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧမ").format(self.name)
class bstack11111ll111_opy_(bstack11111111ll_opy_):
    framework_name: str
    framework_version: str
    state: bstack1llllllllll_opy_
    previous_state: bstack1llllllllll_opy_
    bstack1111l11l11_opy_: datetime
    bstack111111llll_opy_: datetime
    def __init__(
        self,
        context: bstack11111l1ll1_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1llllllllll_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1llllllllll_opy_.NONE
        self.bstack1111l11l11_opy_ = datetime.now(tz=timezone.utc)
        self.bstack111111llll_opy_ = datetime.now(tz=timezone.utc)
    def bstack1111l11l1l_opy_(self, bstack1111111l1l_opy_: bstack1llllllllll_opy_):
        bstack1111l11ll1_opy_ = bstack1llllllllll_opy_(bstack1111111l1l_opy_).name
        if not bstack1111l11ll1_opy_:
            return False
        if bstack1111111l1l_opy_ == self.state:
            return False
        if self.state == bstack1llllllllll_opy_.bstack11111111l1_opy_: # bstack111111l111_opy_ bstack1lllllllll1_opy_ for bstack1lllllll11l_opy_ in bstack1llllllll1l_opy_, it bstack11111l1111_opy_ bstack11111ll11l_opy_ bstack1111111ll1_opy_ times bstack1111l111ll_opy_ a new state
            return True
        if (
            bstack1111111l1l_opy_ == bstack1llllllllll_opy_.NONE
            or (self.state != bstack1llllllllll_opy_.NONE and bstack1111111l1l_opy_ == bstack1llllllllll_opy_.bstack1111l11lll_opy_)
            or (self.state < bstack1llllllllll_opy_.bstack1111l11lll_opy_ and bstack1111111l1l_opy_ == bstack1llllllllll_opy_.bstack1111l11111_opy_)
            or (self.state < bstack1llllllllll_opy_.bstack1111l11lll_opy_ and bstack1111111l1l_opy_ == bstack1llllllllll_opy_.QUIT)
        ):
            raise ValueError(bstack1l1lll_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡶࡤࡸࡪࠦࡴࡳࡣࡱࡷ࡮ࡺࡩࡰࡰ࠽ࠤࠧယ") + str(self.state) + bstack1l1lll_opy_ (u"ࠢࠡ࠿ࡁࠤࠧရ") + str(bstack1111111l1l_opy_))
        self.previous_state = self.state
        self.state = bstack1111111l1l_opy_
        self.bstack111111llll_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack111111ll11_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack111111l11l_opy_: Dict[str, bstack11111ll111_opy_] = dict()
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
    def bstack11111lll11_opy_(self, instance: bstack11111ll111_opy_, method_name: str, bstack1lllllll1ll_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack111111l1ll_opy_(
        self, method_name, previous_state: bstack1llllllllll_opy_, *args, **kwargs
    ) -> bstack1llllllllll_opy_:
        return
    @abc.abstractmethod
    def bstack111111l1l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack11111ll111_opy_, str],
        bstack1lllllll1l1_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack11111ll1ll_opy_(self, bstack11111l1lll_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack11111l1lll_opy_:
                bstack111111ll1l_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack111111ll1l_opy_):
                    self.logger.warning(bstack1l1lll_opy_ (u"ࠣࡷࡱࡴࡦࡺࡣࡩࡧࡧࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨလ") + str(method_name) + bstack1l1lll_opy_ (u"ࠤࠥဝ"))
                    continue
                bstack11111llll1_opy_ = self.bstack111111l1ll_opy_(
                    method_name, previous_state=bstack1llllllllll_opy_.NONE
                )
                bstack1111111111_opy_ = self.bstack11111l111l_opy_(
                    method_name,
                    (bstack11111llll1_opy_ if bstack11111llll1_opy_ else bstack1llllllllll_opy_.NONE),
                    bstack111111ll1l_opy_,
                )
                if not callable(bstack1111111111_opy_):
                    self.logger.warning(bstack1l1lll_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠣࡲࡴࡺࠠࡱࡣࡷࡧ࡭࡫ࡤ࠻ࠢࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࠫࡿࡸ࡫࡬ࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨသ") + str(self.framework_version) + bstack1l1lll_opy_ (u"ࠦ࠮ࠨဟ"))
                    continue
                setattr(clazz, method_name, bstack1111111111_opy_)
    def bstack11111l111l_opy_(
        self,
        method_name: str,
        bstack11111llll1_opy_: bstack1llllllllll_opy_,
        bstack111111ll1l_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1ll1l11l_opy_ = datetime.now()
            (bstack11111llll1_opy_,) = wrapped.__vars__
            bstack11111llll1_opy_ = (
                bstack11111llll1_opy_
                if bstack11111llll1_opy_ and bstack11111llll1_opy_ != bstack1llllllllll_opy_.NONE
                else self.bstack111111l1ll_opy_(method_name, previous_state=bstack11111llll1_opy_, *args, **kwargs)
            )
            if bstack11111llll1_opy_ == bstack1llllllllll_opy_.bstack1111l11lll_opy_:
                ctx = bstack11111111ll_opy_.create_context(self.bstack1111l1111l_opy_(target))
                if not self.bstack1111l111l1_opy_() or ctx.id not in bstack111111ll11_opy_.bstack111111l11l_opy_:
                    bstack111111ll11_opy_.bstack111111l11l_opy_[ctx.id] = bstack11111ll111_opy_(
                        ctx, self.framework_name, self.framework_version, bstack11111llll1_opy_
                    )
                self.logger.debug(bstack1l1lll_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࡷࡥࡷ࡭ࡥࡵ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡧࡹࡾ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨဠ") + str(bstack111111ll11_opy_.bstack111111l11l_opy_.keys()) + bstack1l1lll_opy_ (u"ࠨࠢအ"))
            else:
                self.logger.debug(bstack1l1lll_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡ࡫ࡱࡺࡴࡱࡥࡥ࠼ࠣࡿࡹࡧࡲࡨࡧࡷ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤဢ") + str(bstack111111ll11_opy_.bstack111111l11l_opy_.keys()) + bstack1l1lll_opy_ (u"ࠣࠤဣ"))
            instance = bstack111111ll11_opy_.bstack1111111l11_opy_(self.bstack1111l1111l_opy_(target))
            if bstack11111llll1_opy_ == bstack1llllllllll_opy_.NONE or not instance:
                ctx = bstack11111111ll_opy_.create_context(self.bstack1111l1111l_opy_(target))
                self.logger.warning(bstack1l1lll_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣࡹࡳࡺࡲࡢࡥ࡮ࡩࡩࡀࠠࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡣࡵࡺࡀࡿࡨࡺࡸࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨဤ") + str(bstack111111ll11_opy_.bstack111111l11l_opy_.keys()) + bstack1l1lll_opy_ (u"ࠥࠦဥ"))
                return bstack111111ll1l_opy_(target, *args, **kwargs)
            bstack11111l1l1l_opy_ = self.bstack111111l1l1_opy_(
                target,
                (instance, method_name),
                (bstack11111llll1_opy_, bstack11111lll1l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1111l11l1l_opy_(bstack11111llll1_opy_):
                self.logger.debug(bstack1l1lll_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡨࡨࠥࡹࡴࡢࡶࡨ࠱ࡹࡸࡡ࡯ࡵ࡬ࡸ࡮ࡵ࡮࠻ࠢࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡶࡲࡦࡸ࡬ࡳࡺࡹ࡟ࡴࡶࡤࡸࡪࢃࠠ࠾ࡀࠣࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡳࡵࡣࡷࡩࢂࠦࠨࡼࡶࡼࡴࡪ࠮ࡴࡢࡴࡪࡩࡹ࠯ࡽ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡽࡤࡶ࡬ࡹࡽࠪࠢ࡞ࠦဦ") + str(instance.ref()) + bstack1l1lll_opy_ (u"ࠧࡣࠢဧ"))
            result = (
                bstack11111l1l1l_opy_(target, bstack111111ll1l_opy_, *args, **kwargs)
                if callable(bstack11111l1l1l_opy_)
                else bstack111111ll1l_opy_(target, *args, **kwargs)
            )
            bstack111111lll1_opy_ = self.bstack111111l1l1_opy_(
                target,
                (instance, method_name),
                (bstack11111llll1_opy_, bstack11111lll1l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack11111lll11_opy_(instance, method_name, datetime.now() - bstack1ll1l11l_opy_, *args, **kwargs)
            return bstack111111lll1_opy_ if bstack111111lll1_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack11111llll1_opy_,)
        return wrapped
    @staticmethod
    def bstack1111111l11_opy_(target: object, strict=True):
        ctx = bstack11111111ll_opy_.create_context(target)
        instance = bstack111111ll11_opy_.bstack111111l11l_opy_.get(ctx.id, None)
        if instance and instance.bstack11111lllll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack111111111l_opy_(
        ctx: bstack11111l1ll1_opy_, state: bstack1llllllllll_opy_, reverse=True
    ) -> List[bstack11111ll111_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack111111ll11_opy_.bstack111111l11l_opy_.values(),
            ),
            key=lambda t: t.bstack1111l11l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111l11ll_opy_(instance: bstack11111ll111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack11111l11l1_opy_(instance: bstack11111ll111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1111l11l1l_opy_(instance: bstack11111ll111_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack111111ll11_opy_.logger.debug(bstack1l1lll_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡ࡭ࡨࡽࡂࢁ࡫ࡦࡻࢀࠤࡻࡧ࡬ࡶࡧࡀࠦဨ") + str(value) + bstack1l1lll_opy_ (u"ࠢࠣဩ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack111111ll11_opy_.bstack1111111l11_opy_(target, strict)
        return bstack111111ll11_opy_.bstack11111l11l1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack111111ll11_opy_.bstack1111111l11_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1111l111l1_opy_(self):
        return self.framework_name == bstack1l1lll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬဪ")
    def bstack1111l1111l_opy_(self, target):
        return target if not self.bstack1111l111l1_opy_() else self.bstack1llllllll11_opy_()
    @staticmethod
    def bstack1llllllll11_opy_():
        return str(os.getpid()) + str(threading.get_ident())