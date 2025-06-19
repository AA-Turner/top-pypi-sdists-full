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
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1llllllll1l_opy_ import bstack11111l11ll_opy_, bstack1llllllll11_opy_
import os
import threading
class bstack11111l1ll1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack111lll_opy_ (u"ࠤࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣ၇").format(self.name)
class bstack1111111111_opy_(Enum):
    NONE = 0
    bstack1lllllll1l1_opy_ = 1
    bstack1lllll1lll1_opy_ = 3
    bstack111111lll1_opy_ = 4
    bstack1lllllll1ll_opy_ = 5
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
        return bstack111lll_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥ၈").format(self.name)
class bstack1llllll111l_opy_(bstack11111l11ll_opy_):
    framework_name: str
    framework_version: str
    state: bstack1111111111_opy_
    previous_state: bstack1111111111_opy_
    bstack111111ll1l_opy_: datetime
    bstack1lllll1ll1l_opy_: datetime
    def __init__(
        self,
        context: bstack1llllllll11_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1111111111_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1111111111_opy_.NONE
        self.bstack111111ll1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lllll1ll1l_opy_ = datetime.now(tz=timezone.utc)
    def bstack11111ll111_opy_(self, bstack1lllllll111_opy_: bstack1111111111_opy_):
        bstack111111l1l1_opy_ = bstack1111111111_opy_(bstack1lllllll111_opy_).name
        if not bstack111111l1l1_opy_:
            return False
        if bstack1lllllll111_opy_ == self.state:
            return False
        if self.state == bstack1111111111_opy_.bstack1lllll1lll1_opy_: # bstack1lllll1l1l1_opy_ bstack1111111l1l_opy_ for bstack111111l111_opy_ in bstack1111111lll_opy_, it bstack1llllllllll_opy_ bstack1111111ll1_opy_ bstack111111l1ll_opy_ times bstack111111ll11_opy_ a new state
            return True
        if (
            bstack1lllllll111_opy_ == bstack1111111111_opy_.NONE
            or (self.state != bstack1111111111_opy_.NONE and bstack1lllllll111_opy_ == bstack1111111111_opy_.bstack1lllllll1l1_opy_)
            or (self.state < bstack1111111111_opy_.bstack1lllllll1l1_opy_ and bstack1lllllll111_opy_ == bstack1111111111_opy_.bstack111111lll1_opy_)
            or (self.state < bstack1111111111_opy_.bstack1lllllll1l1_opy_ and bstack1lllllll111_opy_ == bstack1111111111_opy_.QUIT)
        ):
            raise ValueError(bstack111lll_opy_ (u"ࠦ࡮ࡴࡶࡢ࡮࡬ࡨࠥࡹࡴࡢࡶࡨࠤࡹࡸࡡ࡯ࡵ࡬ࡸ࡮ࡵ࡮࠻ࠢࠥ၉") + str(self.state) + bstack111lll_opy_ (u"ࠧࠦ࠽࠿ࠢࠥ၊") + str(bstack1lllllll111_opy_))
        self.previous_state = self.state
        self.state = bstack1lllllll111_opy_
        self.bstack1lllll1ll1l_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1111111l11_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1lllll1ll11_opy_: Dict[str, bstack1llllll111l_opy_] = dict()
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
    def bstack11111111l1_opy_(self, instance: bstack1llllll111l_opy_, method_name: str, bstack111111111l_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1llllll1ll1_opy_(
        self, method_name, previous_state: bstack1111111111_opy_, *args, **kwargs
    ) -> bstack1111111111_opy_:
        return
    @abc.abstractmethod
    def bstack1llllll1lll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1lllll1l1ll_opy_(self, bstack1lllllll11l_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1lllllll11l_opy_:
                bstack1lllllllll1_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1lllllllll1_opy_):
                    self.logger.warning(bstack111lll_opy_ (u"ࠨࡵ࡯ࡲࡤࡸࡨ࡮ࡥࡥࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࠦ။") + str(method_name) + bstack111lll_opy_ (u"ࠢࠣ၌"))
                    continue
                bstack1lllll1llll_opy_ = self.bstack1llllll1ll1_opy_(
                    method_name, previous_state=bstack1111111111_opy_.NONE
                )
                bstack111111llll_opy_ = self.bstack11111l1l1l_opy_(
                    method_name,
                    (bstack1lllll1llll_opy_ if bstack1lllll1llll_opy_ else bstack1111111111_opy_.NONE),
                    bstack1lllllllll1_opy_,
                )
                if not callable(bstack111111llll_opy_):
                    self.logger.warning(bstack111lll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠡࡰࡲࡸࠥࡶࡡࡵࡥ࡫ࡩࡩࡀࠠࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࠩࡽࡶࡩࡱ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾ࠼ࠣࠦ၍") + str(self.framework_version) + bstack111lll_opy_ (u"ࠤࠬࠦ၎"))
                    continue
                setattr(clazz, method_name, bstack111111llll_opy_)
    def bstack11111l1l1l_opy_(
        self,
        method_name: str,
        bstack1lllll1llll_opy_: bstack1111111111_opy_,
        bstack1lllllllll1_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack11ll1ll1_opy_ = datetime.now()
            (bstack1lllll1llll_opy_,) = wrapped.__vars__
            bstack1lllll1llll_opy_ = (
                bstack1lllll1llll_opy_
                if bstack1lllll1llll_opy_ and bstack1lllll1llll_opy_ != bstack1111111111_opy_.NONE
                else self.bstack1llllll1ll1_opy_(method_name, previous_state=bstack1lllll1llll_opy_, *args, **kwargs)
            )
            if bstack1lllll1llll_opy_ == bstack1111111111_opy_.bstack1lllllll1l1_opy_:
                ctx = bstack11111l11ll_opy_.create_context(self.bstack11111l111l_opy_(target))
                if not self.bstack1llllll11l1_opy_() or ctx.id not in bstack1111111l11_opy_.bstack1lllll1ll11_opy_:
                    bstack1111111l11_opy_.bstack1lllll1ll11_opy_[ctx.id] = bstack1llllll111l_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1lllll1llll_opy_
                    )
                self.logger.debug(bstack111lll_opy_ (u"ࠥࡻࡷࡧࡰࡱࡧࡧࠤࡲ࡫ࡴࡩࡱࡧࠤࡨࡸࡥࡢࡶࡨࡨ࠿ࠦࡻࡵࡣࡵ࡫ࡪࡺ࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡥࡷࡼࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦ၏") + str(bstack1111111l11_opy_.bstack1lllll1ll11_opy_.keys()) + bstack111lll_opy_ (u"ࠦࠧၐ"))
            else:
                self.logger.debug(bstack111lll_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡩ࡯ࡸࡲ࡯ࡪࡪ࠺ࠡࡽࡷࡥࡷ࡭ࡥࡵ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢၑ") + str(bstack1111111l11_opy_.bstack1lllll1ll11_opy_.keys()) + bstack111lll_opy_ (u"ࠨࠢၒ"))
            instance = bstack1111111l11_opy_.bstack11111l11l1_opy_(self.bstack11111l111l_opy_(target))
            if bstack1lllll1llll_opy_ == bstack1111111111_opy_.NONE or not instance:
                ctx = bstack11111l11ll_opy_.create_context(self.bstack11111l111l_opy_(target))
                self.logger.warning(bstack111lll_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡷࡱࡸࡷࡧࡣ࡬ࡧࡧ࠾ࠥࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡨࡺࡸ࠾ࡽࡦࡸࡽࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦၓ") + str(bstack1111111l11_opy_.bstack1lllll1ll11_opy_.keys()) + bstack111lll_opy_ (u"ࠣࠤၔ"))
                return bstack1lllllllll1_opy_(target, *args, **kwargs)
            bstack1llllll11ll_opy_ = self.bstack1llllll1lll_opy_(
                target,
                (instance, method_name),
                (bstack1lllll1llll_opy_, bstack11111l1ll1_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack11111ll111_opy_(bstack1lllll1llll_opy_):
                self.logger.debug(bstack111lll_opy_ (u"ࠤࡤࡴࡵࡲࡩࡦࡦࠣࡷࡹࡧࡴࡦ࠯ࡷࡶࡦࡴࡳࡪࡶ࡬ࡳࡳࡀࠠࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡴࡷ࡫ࡶࡪࡱࡸࡷࡤࡹࡴࡢࡶࡨࢁࠥࡃ࠾ࠡࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡸࡺࡡࡵࡧࢀࠤ࠭ࢁࡴࡺࡲࡨࠬࡹࡧࡲࡨࡧࡷ࠭ࢂ࠴ࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡻࡢࡴࡪࡷࢂ࠯ࠠ࡜ࠤၕ") + str(instance.ref()) + bstack111lll_opy_ (u"ࠥࡡࠧၖ"))
            result = (
                bstack1llllll11ll_opy_(target, bstack1lllllllll1_opy_, *args, **kwargs)
                if callable(bstack1llllll11ll_opy_)
                else bstack1lllllllll1_opy_(target, *args, **kwargs)
            )
            bstack111111l11l_opy_ = self.bstack1llllll1lll_opy_(
                target,
                (instance, method_name),
                (bstack1lllll1llll_opy_, bstack11111l1ll1_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack11111111l1_opy_(instance, method_name, datetime.now() - bstack11ll1ll1_opy_, *args, **kwargs)
            return bstack111111l11l_opy_ if bstack111111l11l_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1lllll1llll_opy_,)
        return wrapped
    @staticmethod
    def bstack11111l11l1_opy_(target: object, strict=True):
        ctx = bstack11111l11ll_opy_.create_context(target)
        instance = bstack1111111l11_opy_.bstack1lllll1ll11_opy_.get(ctx.id, None)
        if instance and instance.bstack11111l1111_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1llllll1l11_opy_(
        ctx: bstack1llllllll11_opy_, state: bstack1111111111_opy_, reverse=True
    ) -> List[bstack1llllll111l_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1111111l11_opy_.bstack1lllll1ll11_opy_.values(),
            ),
            key=lambda t: t.bstack111111ll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111111ll_opy_(instance: bstack1llllll111l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llllll1l1l_opy_(instance: bstack1llllll111l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack11111ll111_opy_(instance: bstack1llllll111l_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1111111l11_opy_.logger.debug(bstack111lll_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦ࡫ࡦࡻࡀࡿࡰ࡫ࡹࡾࠢࡹࡥࡱࡻࡥ࠾ࠤၗ") + str(value) + bstack111lll_opy_ (u"ࠧࠨၘ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1111111l11_opy_.bstack11111l11l1_opy_(target, strict)
        return bstack1111111l11_opy_.bstack1llllll1l1l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1111111l11_opy_.bstack11111l11l1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1llllll11l1_opy_(self):
        return self.framework_name == bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪၙ")
    def bstack11111l111l_opy_(self, target):
        return target if not self.bstack1llllll11l1_opy_() else self.bstack11111l1lll_opy_()
    @staticmethod
    def bstack11111l1lll_opy_():
        return str(os.getpid()) + str(threading.get_ident())