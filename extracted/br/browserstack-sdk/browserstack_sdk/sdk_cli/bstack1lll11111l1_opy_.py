# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1lll11l1l1l_opy_ import bstack1ll1llllll1_opy_, bstack1lll11l1l11_opy_
import os
import threading
from browserstack_sdk.browserstack_helper import BrowserStackHelper
class bstack1lll11l111l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11l1l11_opy_ (u"ࠦࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᇘ").format(self.name)
class bstack1ll1lll1lll_opy_(Enum):
    NONE = 0
    bstack1lll111ll1l_opy_ = 1
    bstack1lll11l11l1_opy_ = 3
    bstack1lll11111ll_opy_ = 4
    bstack1lll1111lll_opy_ = 5
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
        return bstack11l1l11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᇙ").format(self.name)
class bstack1ll1llll111_opy_(bstack1ll1llllll1_opy_):
    framework_name: str
    framework_version: str
    state: bstack1ll1lll1lll_opy_
    previous_state: bstack1ll1lll1lll_opy_
    bstack1ll1lll1ll1_opy_: datetime
    bstack1ll1ll1lll1_opy_: datetime
    def __init__(
        self,
        context: bstack1lll11l1l11_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1ll1lll1lll_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1ll1lll1lll_opy_.NONE
        self.bstack1ll1lll1ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll1ll1lll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll111ll11_opy_(self, bstack1ll1lllll1l_opy_: bstack1ll1lll1lll_opy_):
        bstack1lll1111ll1_opy_ = bstack1ll1lll1lll_opy_(bstack1ll1lllll1l_opy_).name
        if not bstack1lll1111ll1_opy_:
            return False
        if bstack1ll1lllll1l_opy_ == self.state:
            return False
        if self.state == bstack1ll1lll1lll_opy_.bstack1lll11l11l1_opy_: # bstack1ll1lllll11_opy_ bstack1ll1llll1l1_opy_ for bstack1lll111lll1_opy_ in bstack1ll1lll1l1l_opy_, it bstack1ll1llll11l_opy_ bstack1lll111l1ll_opy_ bstack1ll1lll1l11_opy_ times bstack1lll111llll_opy_ a new state
            return True
        if (
            bstack1ll1lllll1l_opy_ == bstack1ll1lll1lll_opy_.NONE
            or (self.state != bstack1ll1lll1lll_opy_.NONE and bstack1ll1lllll1l_opy_ == bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_)
            or (self.state < bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_ and bstack1ll1lllll1l_opy_ == bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_)
            or (self.state < bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_ and bstack1ll1lllll1l_opy_ == bstack1ll1lll1lll_opy_.QUIT)
        ):
            raise ValueError(bstack11l1l11_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡶࡤࡸࡪࠦࡴࡳࡣࡱࡷ࡮ࡺࡩࡰࡰ࠽ࠤࠧᇚ") + str(self.state) + bstack11l1l11_opy_ (u"ࠢࠡ࠿ࡁࠤࠧᇛ") + str(bstack1ll1lllll1l_opy_))
        self.previous_state = self.state
        self.state = bstack1ll1lllll1l_opy_
        self.bstack1ll1ll1lll1_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1lll11ll1l1_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1ll1ll1l_opy_: Dict[str, bstack1ll1llll111_opy_] = dict()
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
    def bstack1ll1ll1l1l1_opy_(self, instance: bstack1ll1llll111_opy_, method_name: str, bstack1lll11l1111_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1lll11l1lll_opy_(
        self, method_name, previous_state: bstack1ll1lll1lll_opy_, *args, **kwargs
    ) -> bstack1ll1lll1lll_opy_:
        return
    @abc.abstractmethod
    def bstack1ll1lll11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1ll1lll11l1_opy_(self, bstack1lll11l1ll1_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1lll11l1ll1_opy_:
                bstack1ll1ll1l1ll_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1ll1ll1l1ll_opy_):
                    self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡷࡱࡴࡦࡺࡣࡩࡧࡧࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨᇜ") + str(method_name) + bstack11l1l11_opy_ (u"ࠤࠥᇝ"))
                    continue
                bstack1lll111111l_opy_ = self.bstack1lll11l1lll_opy_(
                    method_name, previous_state=bstack1ll1lll1lll_opy_.NONE
                )
                bstack1lll1111111_opy_ = self.bstack1lll111l1l1_opy_(
                    method_name,
                    (bstack1lll111111l_opy_ if bstack1lll111111l_opy_ else bstack1ll1lll1lll_opy_.NONE),
                    bstack1ll1ll1l1ll_opy_,
                )
                if not callable(bstack1lll1111111_opy_):
                    self.logger.warning(bstack11l1l11_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠣࡲࡴࡺࠠࡱࡣࡷࡧ࡭࡫ࡤ࠻ࠢࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࠫࡿࡸ࡫࡬ࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨᇞ") + str(self.framework_version) + bstack11l1l11_opy_ (u"ࠦ࠮ࠨᇟ"))
                    continue
                setattr(clazz, method_name, bstack1lll1111111_opy_)
    def bstack1lll111l1l1_opy_(
        self,
        method_name: str,
        bstack1lll111111l_opy_: bstack1ll1lll1lll_opy_,
        bstack1ll1ll1l1ll_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack111l11l1l1_opy_ = datetime.now()
            (bstack1lll111111l_opy_,) = wrapped.__vars__
            bstack1lll111111l_opy_ = (
                bstack1lll111111l_opy_
                if bstack1lll111111l_opy_ and bstack1lll111111l_opy_ != bstack1ll1lll1lll_opy_.NONE
                else self.bstack1lll11l1lll_opy_(method_name, previous_state=bstack1lll111111l_opy_, *args, **kwargs)
            )
            if bstack1lll111111l_opy_ == bstack1ll1lll1lll_opy_.bstack1lll111ll1l_opy_:
                ctx = bstack1ll1llllll1_opy_.create_context(self.bstack1ll1ll1l11l_opy_(target))
                if not self.bstack1lll111l11l_opy_() or ctx.id not in bstack1lll11ll1l1_opy_.bstack1ll1ll1ll1l_opy_:
                    bstack1lll11ll1l1_opy_.bstack1ll1ll1ll1l_opy_[ctx.id] = bstack1ll1llll111_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1lll111111l_opy_
                    )
                    label = BrowserStackHelper.get_driver_label()
                    bstack1lll1111l11_opy_ = None
                    if label:
                        if bstack11l1l11_opy_ (u"ࠧࠩࠢᇠ") in label:
                            suffix = label.rsplit(bstack11l1l11_opy_ (u"ࠨࠣࠣᇡ"), 1)[-1]
                            if suffix.isdigit():
                                bstack1lll1111l11_opy_ = int(suffix)
                            else:
                                self.logger.debug(
                                    bstack1lll11l11ll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲࠠࡴࡷࡩࡪ࡮ࡾࠠࠨࡽࡶࡹ࡫࡬ࡩࡹࡿࠪࠤ࡮ࡴࠠ࡭ࡣࡥࡩࡱࠦࠧࡼ࡮ࡤࡦࡪࡲࡽࠨ࠽ࠣࡩࡽࡶࡥࡤࡶࡨࡨࠥࡴࡵ࡮ࡧࡵ࡭ࡨࠦࡲࡢࡰ࡮࠲ࠧᇢ")
                                )
                        else:
                            self.logger.debug(
                                bstack1lll11l11ll_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲࠠࠨࡽ࡯ࡥࡧ࡫࡬ࡾࠩࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳࠦࠧࠤࠩ࠾ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡲࡢࡰ࡮ࠤࡦࡹࡳࡪࡩࡱࡱࡪࡴࡴ࠯ࠤᇣ")
                            )
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠣࡲࡪࡽࠠࡵࡴࡤࡧࡰ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠽ࠤࢀࡺࡡࡳࡩࡨࡸ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟ࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡣࡵࡺࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡸࡡ࡯࡭ࡀࡿࡷࡧ࡮࡬ࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢᇤ") + str(bstack1lll11ll1l1_opy_.bstack1ll1ll1ll1l_opy_.keys()) + bstack11l1l11_opy_ (u"ࠥࠦᇥ"))
                    bstack1ll1lllllll_opy_ = bstack1lll11ll1l1_opy_.bstack1lll11ll11l_opy_(self.bstack1ll1ll1l11l_opy_(target))
                    bstack1ll1lllllll_opy_.data[bstack11l1l11_opy_ (u"ࠫࡷࡧ࡮࡬ࠩᇦ")] = bstack1lll1111l11_opy_
                self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࡷࡥࡷ࡭ࡥࡵ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡧࡹࡾ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᇧ") + str(bstack1lll11ll1l1_opy_.bstack1ll1ll1ll1l_opy_.keys()) + bstack11l1l11_opy_ (u"ࠨࠢᇨ"))
            else:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡ࡫ࡱࡺࡴࡱࡥࡥ࠼ࠣࡿࡹࡧࡲࡨࡧࡷ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᇩ") + str(bstack1lll11ll1l1_opy_.bstack1ll1ll1ll1l_opy_.keys()) + bstack11l1l11_opy_ (u"ࠣࠤᇪ"))
            instance = bstack1lll11ll1l1_opy_.bstack1lll11ll11l_opy_(self.bstack1ll1ll1l11l_opy_(target))
            if bstack1lll111111l_opy_ == bstack1ll1lll1lll_opy_.NONE or not instance:
                ctx = bstack1ll1llllll1_opy_.create_context(self.bstack1ll1ll1l11l_opy_(target))
                self.logger.warning(bstack11l1l11_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣࡹࡳࡺࡲࡢࡥ࡮ࡩࡩࡀࠠࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡣࡵࡺࡀࡿࡨࡺࡸࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᇫ") + str(bstack1lll11ll1l1_opy_.bstack1ll1ll1ll1l_opy_.keys()) + bstack11l1l11_opy_ (u"ࠥࠦᇬ"))
                return bstack1ll1ll1l1ll_opy_(target, *args, **kwargs)
            bstack1lll1111l1l_opy_ = self.bstack1ll1lll11ll_opy_(
                target,
                (instance, method_name),
                (bstack1lll111111l_opy_, bstack1lll11l111l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1lll111ll11_opy_(bstack1lll111111l_opy_):
                self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡨࡨࠥࡹࡴࡢࡶࡨ࠱ࡹࡸࡡ࡯ࡵ࡬ࡸ࡮ࡵ࡮࠻ࠢࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡶࡲࡦࡸ࡬ࡳࡺࡹ࡟ࡴࡶࡤࡸࡪࢃࠠ࠾ࡀࠣࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡳࡵࡣࡷࡩࢂࠦࠨࡼࡶࡼࡴࡪ࠮ࡴࡢࡴࡪࡩࡹ࠯ࡽ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡽࡤࡶ࡬ࡹࡽࠪࠢ࡞ࠦᇭ") + str(instance.ref()) + bstack11l1l11_opy_ (u"ࠧࡣࠢᇮ"))
            result = (
                bstack1lll1111l1l_opy_(target, bstack1ll1ll1l1ll_opy_, *args, **kwargs)
                if callable(bstack1lll1111l1l_opy_)
                else bstack1ll1ll1l1ll_opy_(target, *args, **kwargs)
            )
            bstack1ll1llll1ll_opy_ = self.bstack1ll1lll11ll_opy_(
                target,
                (instance, method_name),
                (bstack1lll111111l_opy_, bstack1lll11l111l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1ll1ll1l1l1_opy_(instance, method_name, datetime.now() - bstack111l11l1l1_opy_, *args, **kwargs)
            return bstack1ll1llll1ll_opy_ if bstack1ll1llll1ll_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1lll111111l_opy_,)
        return wrapped
    @staticmethod
    def bstack1lll11ll11l_opy_(target: object, strict=True):
        ctx = bstack1ll1llllll1_opy_.create_context(target)
        instance = bstack1lll11ll1l1_opy_.bstack1ll1ll1ll1l_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll1ll1llll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1ll1ll1ll11_opy_(
        ctx: bstack1lll11l1l11_opy_, state: bstack1ll1lll1lll_opy_, reverse=True
    ) -> List[bstack1ll1llll111_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1lll11ll1l1_opy_.bstack1ll1ll1ll1l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1lll1ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll111l111_opy_(instance: bstack1ll1llll111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll1lll111l_opy_(instance: bstack1ll1llll111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll111ll11_opy_(instance: bstack1ll1llll111_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1lll11ll1l1_opy_.logger.debug(bstack11l1l11_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡ࡭ࡨࡽࡂࢁ࡫ࡦࡻࢀࠤࡻࡧ࡬ࡶࡧࡀࠦᇯ") + str(value) + bstack11l1l11_opy_ (u"ࠢࠣᇰ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1lll11ll1l1_opy_.bstack1lll11ll11l_opy_(target, strict)
        return bstack1lll11ll1l1_opy_.bstack1ll1lll111l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1lll11ll1l1_opy_.bstack1lll11ll11l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1lll111l11l_opy_(self):
        return self.framework_name == bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᇱ")
    def bstack1ll1ll1l11l_opy_(self, target):
        return target if not self.bstack1lll111l11l_opy_() else self.bstack1ll1lll1111_opy_()
    @staticmethod
    def bstack1ll1lll1111_opy_():
        return str(os.getpid()) + str(threading.get_ident())