# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1l1ll111111_opy_ import bstack1l1l1ll1l1l_opy_, bstack1l1lll111ll_opy_
import os
import threading
from browserstack_sdk.browserstack_helper import BrowserStackHelper
class bstack1lll1l11l1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack111l_opy_ (u"ࠦࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᓯ").format(self.name)
class bstack11l1ll1l1_opy_(Enum):
    NONE = 0
    bstack11llll111l_opy_ = 1
    bstack1l11lll1ll1_opy_ = 3
    bstack1ll1111l1l1_opy_ = 4
    bstack1l1l11111l1_opy_ = 5
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
        return bstack111l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᓰ").format(self.name)
class bstack1l1l111l1l1_opy_(bstack1l1l1ll1l1l_opy_):
    framework_name: str
    framework_version: str
    state: bstack11l1ll1l1_opy_
    previous_state: bstack11l1ll1l1_opy_
    bstack1l11lll1l1l_opy_: datetime
    bstack1l1l11l11l1_opy_: datetime
    def __init__(
        self,
        context: bstack1l1lll111ll_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack11l1ll1l1_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack11l1ll1l1_opy_.NONE
        self.bstack1l11lll1l1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1l11l11l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1l11l1ll11_opy_(self, bstack1l1l111l11l_opy_: bstack11l1ll1l1_opy_):
        bstack1l11lll1lll_opy_ = bstack11l1ll1l1_opy_(bstack1l1l111l11l_opy_).name
        if not bstack1l11lll1lll_opy_:
            return False
        if bstack1l1l111l11l_opy_ == self.state:
            return False
        if self.state == bstack11l1ll1l1_opy_.bstack1l11lll1ll1_opy_: # bstack1l1l11l111l_opy_ bstack1l11llll1ll_opy_ for bstack1l1l111ll1l_opy_ in Playwright, it bstack1l1l11111ll_opy_ bstack1l1l1111ll1_opy_ bstack1l11lllllll_opy_ times bstack1l11llll11l_opy_ a new state
            return True
        if (
            bstack1l1l111l11l_opy_ == bstack11l1ll1l1_opy_.NONE
            or (self.state != bstack11l1ll1l1_opy_.NONE and bstack1l1l111l11l_opy_ == bstack11l1ll1l1_opy_.bstack11llll111l_opy_)
            or (self.state < bstack11l1ll1l1_opy_.bstack11llll111l_opy_ and bstack1l1l111l11l_opy_ == bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_)
            or (self.state < bstack11l1ll1l1_opy_.bstack11llll111l_opy_ and bstack1l1l111l11l_opy_ == bstack11l1ll1l1_opy_.QUIT)
        ):
            raise ValueError(bstack111l_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡶࡤࡸࡪࠦࡴࡳࡣࡱࡷ࡮ࡺࡩࡰࡰ࠽ࠤࠧᓱ") + str(self.state) + bstack111l_opy_ (u"ࠢࠡ࠿ࡁࠤࠧᓲ") + str(bstack1l1l111l11l_opy_))
        self.previous_state = self.state
        self.state = bstack1l1l111l11l_opy_
        self.bstack1l1l11l11l1_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1l1l1ll11l_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l111l111_opy_: Dict[str, bstack1l1l111l1l1_opy_] = dict()
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
    def bstack1l1l11l1111_opy_(self, instance: bstack1l1l111l1l1_opy_, method_name: str, bstack1l1l111lll1_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1l11lll1l11_opy_(
        self, method_name, previous_state: bstack11l1ll1l1_opy_, *args, **kwargs
    ) -> bstack11l1ll1l1_opy_:
        return
    @abc.abstractmethod
    def bstack11l11ll1l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1l1l111ll11_opy_(self, bstack1l1l111l111_opy_: List[str]):
        if not self.classes or len(self.classes) == 0:
            return
        for clazz in self.classes:
            for method_name in bstack1l1l111l111_opy_:
                bstack1l1l1111l11_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1l1l1111l11_opy_):
                    self.logger.warning(bstack111l_opy_ (u"ࠣࡷࡱࡴࡦࡺࡣࡩࡧࡧࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨᓳ") + str(method_name) + bstack111l_opy_ (u"ࠤࠥᓴ"))
                    continue
                bstack1l1l1111lll_opy_ = self.bstack1l11lll1l11_opy_(
                    method_name, previous_state=bstack11l1ll1l1_opy_.NONE
                )
                bstack1l11lllll11_opy_ = self.bstack1l11llll1l1_opy_(
                    method_name,
                    (bstack1l1l1111lll_opy_ if bstack1l1l1111lll_opy_ else bstack11l1ll1l1_opy_.NONE),
                    bstack1l1l1111l11_opy_,
                )
                if not callable(bstack1l11lllll11_opy_):
                    self.logger.warning(bstack111l_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠣࡲࡴࡺࠠࡱࡣࡷࡧ࡭࡫ࡤ࠻ࠢࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࠫࡿࡸ࡫࡬ࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨᓵ") + str(self.framework_version) + bstack111l_opy_ (u"ࠦ࠮ࠨᓶ"))
                    continue
                setattr(clazz, method_name, bstack1l11lllll11_opy_)
    def bstack1l11llll1l1_opy_(
        self,
        method_name: str,
        bstack1l1l1111lll_opy_: bstack11l1ll1l1_opy_,
        bstack1l1l1111l11_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1lllllll1ll_opy_ = datetime.now()
            (bstack1l1l1111lll_opy_,) = wrapped.__vars__
            bstack1l1l1111lll_opy_ = (
                bstack1l1l1111lll_opy_
                if bstack1l1l1111lll_opy_ and bstack1l1l1111lll_opy_ != bstack11l1ll1l1_opy_.NONE
                else self.bstack1l11lll1l11_opy_(method_name, previous_state=bstack1l1l1111lll_opy_, *args, **kwargs)
            )
            if bstack1l1l1111lll_opy_ == bstack11l1ll1l1_opy_.bstack11llll111l_opy_:
                ctx = bstack1l1l1ll1l1l_opy_.create_context(self.bstack1l1l1111l1l_opy_(target))
                if not self.bstack1l1l1111111_opy_() or ctx.id not in bstack1l1l1ll11l_opy_.bstack1l111l111_opy_:
                    bstack1l1l1ll11l_opy_.bstack1l111l111_opy_[ctx.id] = bstack1l1l111l1l1_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1l1l1111lll_opy_
                    )
                    label = BrowserStackHelper.get_driver_label()
                    bstack1l11llll111_opy_ = None
                    if label:
                        if bstack111l_opy_ (u"ࠧࠩࠢᓷ") in label:
                            suffix = label.rsplit(bstack111l_opy_ (u"ࠨࠣࠣᓸ"), 1)[-1]
                            if suffix.isdigit():
                                bstack1l11llll111_opy_ = int(suffix)
                            else:
                                self.logger.debug(
                                    bstack1l11lll11ll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲࠠࡴࡷࡩࡪ࡮ࡾࠠࠨࡽࡶࡹ࡫࡬ࡩࡹࡿࠪࠤ࡮ࡴࠠ࡭ࡣࡥࡩࡱࠦࠧࡼ࡮ࡤࡦࡪࡲࡽࠨ࠽ࠣࡩࡽࡶࡥࡤࡶࡨࡨࠥࡴࡵ࡮ࡧࡵ࡭ࡨࠦࡲࡢࡰ࡮࠲ࠧᓹ")
                                )
                        else:
                            self.logger.debug(
                                bstack1l11lll11ll_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲࠠࠨࡽ࡯ࡥࡧ࡫࡬ࡾࠩࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳࠦࠧࠤࠩ࠾ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡲࡢࡰ࡮ࠤࡦࡹࡳࡪࡩࡱࡱࡪࡴࡴ࠯ࠤᓺ")
                            )
                    self.logger.debug(bstack111l_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠣࡲࡪࡽࠠࡵࡴࡤࡧࡰ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠽ࠤࢀࡺࡡࡳࡩࡨࡸ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟ࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡣࡵࡺࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡸࡡ࡯࡭ࡀࡿࡷࡧ࡮࡬ࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᓻ") + str(bstack1l1l1ll11l_opy_.bstack1l111l111_opy_.keys()) + bstack111l_opy_ (u"ࠥࠦᓼ"))
                    bstack1l11llllll1_opy_ = bstack1l1l1ll11l_opy_.bstack1l1l1l1l11l_opy_(self.bstack1l1l1111l1l_opy_(target))
                    bstack1l11llllll1_opy_.data[bstack111l_opy_ (u"ࠫࡷࡧ࡮࡬ࠩᓽ")] = bstack1l11llll111_opy_
                self.logger.debug(bstack111l_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࡷࡥࡷ࡭ࡥࡵ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡧࡹࡾ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᓾ") + str(bstack1l1l1ll11l_opy_.bstack1l111l111_opy_.keys()) + bstack111l_opy_ (u"ࠨࠢᓿ"))
            else:
                self.logger.debug(bstack111l_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡ࡫ࡱࡺࡴࡱࡥࡥ࠼ࠣࡿࡹࡧࡲࡨࡧࡷ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᔀ") + str(bstack1l1l1ll11l_opy_.bstack1l111l111_opy_.keys()) + bstack111l_opy_ (u"ࠣࠤᔁ"))
            instance = bstack1l1l1ll11l_opy_.bstack1l1l1l1l11l_opy_(self.bstack1l1l1111l1l_opy_(target))
            if bstack1l1l1111lll_opy_ == bstack11l1ll1l1_opy_.NONE or not instance:
                ctx = bstack1l1l1ll1l1l_opy_.create_context(self.bstack1l1l1111l1l_opy_(target))
                self.logger.warning(bstack111l_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣࡹࡳࡺࡲࡢࡥ࡮ࡩࡩࡀࠠࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡣࡵࡺࡀࡿࡨࡺࡸࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᔂ") + str(bstack1l1l1ll11l_opy_.bstack1l111l111_opy_.keys()) + bstack111l_opy_ (u"ࠥࠦᔃ"))
                return bstack1l1l1111l11_opy_(target, *args, **kwargs)
            bstack1l1l111llll_opy_ = self.bstack11l11ll1l_opy_(
                target,
                (instance, method_name),
                (bstack1l1l1111lll_opy_, bstack1lll1l11l1_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1l11l1ll11_opy_(bstack1l1l1111lll_opy_):
                self.logger.debug(bstack111l_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡨࡨࠥࡹࡴࡢࡶࡨ࠱ࡹࡸࡡ࡯ࡵ࡬ࡸ࡮ࡵ࡮࠻ࠢࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡶࡲࡦࡸ࡬ࡳࡺࡹ࡟ࡴࡶࡤࡸࡪࢃࠠ࠾ࡀࠣࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡳࡵࡣࡷࡩࢂࠦࠨࡼࡶࡼࡴࡪ࠮ࡴࡢࡴࡪࡩࡹ࠯ࡽ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡽࡤࡶ࡬ࡹࡽࠪࠢ࡞ࠦᔄ") + str(instance.ref()) + bstack111l_opy_ (u"ࠧࡣࠢᔅ"))
            result = (
                bstack1l1l111llll_opy_(target, bstack1l1l1111l11_opy_, *args, **kwargs)
                if callable(bstack1l1l111llll_opy_)
                else bstack1l1l1111l11_opy_(target, *args, **kwargs)
            )
            bstack1l11lllll1l_opy_ = self.bstack11l11ll1l_opy_(
                target,
                (instance, method_name),
                (bstack1l1l1111lll_opy_, bstack1lll1l11l1_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1l1l11l1111_opy_(instance, method_name, datetime.now() - bstack1lllllll1ll_opy_, *args, **kwargs)
            return bstack1l11lllll1l_opy_ if bstack1l11lllll1l_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1l1l1111lll_opy_,)
        return wrapped
    @staticmethod
    def bstack1l1l1l1l11l_opy_(target: object, strict=True):
        ctx = bstack1l1l1ll1l1l_opy_.create_context(target)
        instance = bstack1l1l1ll11l_opy_.bstack1l111l111_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1l111l1ll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1l111111l_opy_(
        ctx: bstack1l1lll111ll_opy_, state: bstack11l1ll1l1_opy_, reverse=True
    ) -> List[bstack1l1l111l1l1_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1l1l1ll11l_opy_.bstack1l111l111_opy_.values(),
            ),
            key=lambda t: t.bstack1l11lll1l1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1111ll1l_opy_(instance: bstack1l1l111l1l1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll111111ll_opy_(instance: bstack1l1l111l1l1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1l11l1ll11_opy_(instance: bstack1l1l111l1l1_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1l1l1ll11l_opy_.logger.debug(bstack111l_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡ࡭ࡨࡽࡂࢁ࡫ࡦࡻࢀࠤࡻࡧ࡬ࡶࡧࡀࠦᔆ") + str(value) + bstack111l_opy_ (u"ࠢࠣᔇ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1l1l1ll11l_opy_.bstack1l1l1l1l11l_opy_(target, strict)
        return bstack1l1l1ll11l_opy_.bstack1ll111111ll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1l1l1ll11l_opy_.bstack1l1l1l1l11l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1l1l1111111_opy_(self):
        return self.framework_name == bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᔈ")
    def bstack1l1l1111l1l_opy_(self, target):
        return target if not self.bstack1l1l1111111_opy_() else self.bstack1l1l11l11ll_opy_()
    @staticmethod
    def bstack1l1l11l11ll_opy_():
        return str(os.getpid()) + str(threading.get_ident())