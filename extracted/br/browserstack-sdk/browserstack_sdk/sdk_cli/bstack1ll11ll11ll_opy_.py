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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1lll1llllll_opy_,
    bstack1llllll1l1l_opy_,
    bstack1ll1lllll11_opy_,
    bstack1lll1llll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_, bstack1lllll111ll_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1lll_opy_ import bstack111111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l1l_opy_ import bstack1ll1l1l1111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1llll_opy_ import bstack1ll1lll1l1l_opy_
from bstack_utils.helper import bstack11lllll11ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11lllll1l1_opy_ import bstack1lll1l1l11l_opy_
import grpc
import traceback
import json
class bstack1l111ll11l1_opy_(bstack1lll1lllll1_opy_):
    bstack1lll111ll11_opy_ = False
    bstack1l11111l11l_opy_ = bstack11l1111_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤᔮ")
    bstack1l11111ll1l_opy_ = bstack11l1111_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣᔯ")
    bstack11llll1l1ll_opy_ = bstack11l1111_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩ࡯࡫ࡷࠦᔰ")
    bstack1l1111111l1_opy_ = bstack11l1111_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡵࡢࡷࡨࡧ࡮࡯࡫ࡱ࡫ࠧᔱ")
    bstack11llll11lll_opy_ = bstack11l1111_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲࡠࡪࡤࡷࡤࡻࡲ࡭ࠤᔲ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1llll1l111l_opy_, bstack1llll1ll11l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l11111l1ll_opy_ = False
        self.bstack11llll1ll1l_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1lll1l111ll_opy_ = bstack1llll1ll11l_opy_
        bstack1llll1l111l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1llll1lll11_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack11llll1ll11_opy_)
        TestFramework.bstack1lllll1llll_opy_((bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.PRE), self.bstack1lllll1lll1_opy_)
        TestFramework.bstack1lllll1llll_opy_((bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.POST), self.bstack1lllll11l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1lllll1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._11llllll11l_opy_(instance, args)
        test_framework = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1ll1l11_opy_)
        if self.bstack1l11111l1ll_opy_:
            self.bstack11llll1ll1l_opy_[bstack11l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠤᔳ")] = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1l1ll1l_opy_)
        if bstack11l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᔴ") in instance.bstack1l1l1lll111_opy_:
            platform_index = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1llllll1lll_opy_)
            self.accessibility = self.bstack1l111111ll1_opy_(tags, self.config[bstack11l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᔵ")][platform_index])
        else:
            capabilities = self.bstack1lll1l111ll_opy_.bstack1ll1l11l1l1_opy_(f, instance, bstack1llll11l111_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack11l1111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᔶ") + str(kwargs) + bstack11l1111_opy_ (u"ࠨࠢᔷ"))
                return
            self.accessibility = self.bstack1l111111ll1_opy_(tags, capabilities)
        if self.bstack1lll1l111ll_opy_.pages and self.bstack1lll1l111ll_opy_.pages.values():
            bstack1l11111l111_opy_ = list(self.bstack1lll1l111ll_opy_.pages.values())
            if bstack1l11111l111_opy_ and isinstance(bstack1l11111l111_opy_[0], (list, tuple)) and bstack1l11111l111_opy_[0]:
                bstack11llllll111_opy_ = bstack1l11111l111_opy_[0][0]
                if callable(bstack11llllll111_opy_):
                    page = bstack11llllll111_opy_()
                    def bstack1l11llll11_opy_():
                        self.get_accessibility_results(page, bstack11l1111_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᔸ"))
                    def bstack1l11111lll1_opy_():
                        self.get_accessibility_results_summary(page, bstack11l1111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᔹ"))
                    setattr(page, bstack11l1111_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡷࠧᔺ"), bstack1l11llll11_opy_)
                    setattr(page, bstack11l1111_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡘࡻ࡭࡮ࡣࡵࡽࠧᔻ"), bstack1l11111lll1_opy_)
        self.logger.debug(bstack11l1111_opy_ (u"ࠦࡸ࡮࡯ࡶ࡮ࡧࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰࡺ࡫࠽ࠣᔼ") + str(self.accessibility) + bstack11l1111_opy_ (u"ࠧࠨᔽ"))
    def bstack11llll1ll11_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1ll1l1l1_opy_ = datetime.now()
            self.bstack11lllll1111_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡮ࡴࡩࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᔾ"), datetime.now() - bstack1ll1l1l1_opy_)
            if (
                not f.bstack1lllll11ll1_opy_(method_name)
                or f.bstack1ll111111l1_opy_(method_name, *args)
                or f.bstack1ll11111l11_opy_(method_name, *args)
            ):
                return
            if not f.bstack1lllll1l11l_opy_(instance, bstack1l111ll11l1_opy_.bstack11llll1l1ll_opy_, False):
                if not bstack1l111ll11l1_opy_.bstack1lll111ll11_opy_:
                    self.logger.warning(bstack11l1111_opy_ (u"ࠢ࡜ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥᔿ") + str(f.platform_index) + bstack11l1111_opy_ (u"ࠣ࡟ࠣࡥ࠶࠷ࡹࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡩࡣࡹࡩࠥࡴ࡯ࡵࠢࡥࡩࡪࡴࠠࡴࡧࡷࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᕀ"))
                    bstack1l111ll11l1_opy_.bstack1lll111ll11_opy_ = True
                return
            bstack11llll1l1l1_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack11llll1l1l1_opy_:
                platform_index = f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1llllll1lll_opy_, 0)
                self.logger.debug(bstack11l1111_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᕁ") + str(f.framework_name) + bstack11l1111_opy_ (u"ࠥࠦᕂ"))
                return
            bstack1lll1111ll1_opy_ = f.bstack1lllll1ll11_opy_(*args)
            if not bstack1lll1111ll1_opy_:
                self.logger.debug(bstack11l1111_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࠨᕃ") + str(method_name) + bstack11l1111_opy_ (u"ࠧࠨᕄ"))
                return
            bstack11llll1l11l_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1l111ll11l1_opy_.bstack11llll11lll_opy_, False)
            if bstack1lll1111ll1_opy_ == bstack11l1111_opy_ (u"ࠨࡧࡦࡶࠥᕅ") and not bstack11llll1l11l_opy_:
                f.bstack1llll111l11_opy_(instance, bstack1l111ll11l1_opy_.bstack11llll11lll_opy_, True)
                bstack11llll1l11l_opy_ = True
            if not bstack11llll1l11l_opy_ and not self.bstack1l11111l1ll_opy_:
                self.logger.debug(bstack11l1111_opy_ (u"ࠢ࡯ࡱ࡙ࠣࡗࡒࠠ࡭ࡱࡤࡨࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᕆ") + str(bstack1lll1111ll1_opy_) + bstack11l1111_opy_ (u"ࠣࠤᕇ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1lll1111ll1_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack11l1111_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᕈ") + str(bstack1lll1111ll1_opy_) + bstack11l1111_opy_ (u"ࠥࠦᕉ"))
                return
            self.logger.info(bstack11l1111_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡷࡨࡸࡩࡱࡶࡶࡣࡹࡵ࡟ࡳࡷࡱ࠭ࢂࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᕊ") + str(bstack1lll1111ll1_opy_) + bstack11l1111_opy_ (u"ࠧࠨᕋ"))
            scripts = [(s, bstack11llll1l1l1_opy_[s]) for s in scripts_to_run if s in bstack11llll1l1l1_opy_]
            for script_name, bstack1ll1l11ll11_opy_ in scripts:
                try:
                    bstack1ll1l1l1_opy_ = datetime.now()
                    if script_name == bstack11l1111_opy_ (u"ࠨࡳࡤࡣࡱࠦᕌ"):
                        result = self.perform_scan(driver, method=bstack1lll1111ll1_opy_, framework_name=f.framework_name)
                    instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿ࠨᕍ") + script_name, datetime.now() - bstack1ll1l1l1_opy_)
                    if isinstance(result, dict) and not result.get(bstack11l1111_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᕎ"), True):
                        self.logger.warning(bstack11l1111_opy_ (u"ࠤࡶ࡯࡮ࡶࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡶࡪࡳࡡࡪࡰ࡬ࡲ࡬ࠦࡳࡤࡴ࡬ࡴࡹࡹ࠺ࠡࠤᕏ") + str(result) + bstack11l1111_opy_ (u"ࠥࠦᕐ"))
                        break
                except Exception as e:
                    self.logger.error(bstack11l1111_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡳࡤࡴ࡬ࡴࡹࡃࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࠦࡥࡳࡴࡲࡶࡂࠨᕑ") + str(e) + bstack11l1111_opy_ (u"ࠧࠨᕒ"))
        except Exception as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧࠣࡩࡷࡸ࡯ࡳ࠿ࠥᕓ") + str(e) + bstack11l1111_opy_ (u"ࠢࠣᕔ"))
    def bstack1lllll11l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._11llllll11l_opy_(instance, args)
        capabilities = self.bstack1lll1l111ll_opy_.bstack1ll1l11l1l1_opy_(f, instance, bstack1llll11l111_opy_, *args, **kwargs)
        self.accessibility = self.bstack1l111111ll1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack11l1111_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᕕ"))
            return
        driver = self.bstack1lll1l111ll_opy_.bstack1ll1l11l11l_opy_(f, instance, bstack1llll11l111_opy_, *args, **kwargs)
        test_name = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll11lllll_opy_)
        if not test_name:
            self.logger.debug(bstack11l1111_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᕖ"))
            return
        test_uuid = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1l1ll1l_opy_)
        if not test_uuid:
            self.logger.debug(bstack11l1111_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣᕗ"))
            return
        if isinstance(self.bstack1lll1l111ll_opy_, bstack1ll1l1l1111_opy_):
            framework_name = bstack11l1111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᕘ")
        else:
            framework_name = bstack11l1111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᕙ")
        self.bstack1lllll1lll_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1lll1lll11l_opy_ = bstack1lll1l1l11l_opy_.bstack1llll1lllll_opy_(EVENTS.bstack11l111111_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack11l1111_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࠢᕚ"))
            return
        bstack1ll1l1l1_opy_ = datetime.now()
        bstack1ll1l11ll11_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1111_opy_ (u"ࠢࡴࡥࡤࡲࠧᕛ"), None)
        if not bstack1ll1l11ll11_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡨࡧ࡮ࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᕜ") + str(framework_name) + bstack11l1111_opy_ (u"ࠤࠣࠦᕝ"))
            return
        if self.bstack1l11111l1ll_opy_:
            arg = dict()
            arg[bstack11l1111_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥᕞ")] = method if method else bstack11l1111_opy_ (u"ࠦࠧᕟ")
            arg[bstack11l1111_opy_ (u"ࠧࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠧᕠ")] = self.bstack11llll1ll1l_opy_[bstack11l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᕡ")]
            arg[bstack11l1111_opy_ (u"ࠢࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠧᕢ")] = self.bstack11llll1ll1l_opy_[bstack11l1111_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠨᕣ")]
            arg[bstack11l1111_opy_ (u"ࠤࡤࡹࡹ࡮ࡈࡦࡣࡧࡩࡷࠨᕤ")] = self.bstack11llll1ll1l_opy_[bstack11l1111_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠣᕥ")]
            arg[bstack11l1111_opy_ (u"ࠦࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠣᕦ")] = self.bstack11llll1ll1l_opy_[bstack11l1111_opy_ (u"ࠧࡺࡨࡠ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠦᕧ")]
            arg[bstack11l1111_opy_ (u"ࠨࡳࡤࡣࡱࡘ࡮ࡳࡥࡴࡶࡤࡱࡵࠨᕨ")] = str(int(datetime.now().timestamp() * 1000))
            bstack11llll1llll_opy_ = bstack1ll1l11ll11_opy_ % json.dumps(arg)
            driver.execute_script(bstack11llll1llll_opy_)
            return
        instance = bstack1ll1lllll11_opy_.bstack1l1l1lllll1_opy_(driver)
        if instance:
            if not bstack1ll1lllll11_opy_.bstack1lllll1l11l_opy_(instance, bstack1l111ll11l1_opy_.bstack1l1111111l1_opy_, False):
                bstack1ll1lllll11_opy_.bstack1llll111l11_opy_(instance, bstack1l111ll11l1_opy_.bstack1l1111111l1_opy_, True)
            else:
                self.logger.info(bstack11l1111_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡱࠤࡵࡸ࡯ࡨࡴࡨࡷࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡀࠦᕩ") + str(method) + bstack11l1111_opy_ (u"ࠣࠤᕪ"))
                return
        self.logger.info(bstack11l1111_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢᕫ") + str(method) + bstack11l1111_opy_ (u"ࠥࠦᕬ"))
        if framework_name == bstack11l1111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᕭ"):
            result = self.bstack1lll1l111ll_opy_.bstack1ll11llll11_opy_(driver, bstack1ll1l11ll11_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l11ll11_opy_, {bstack11l1111_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᕮ"): method if method else bstack11l1111_opy_ (u"ࠨࠢᕯ")})
        bstack1lll1l1l11l_opy_.end(EVENTS.bstack11l111111_opy_.value, bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᕰ"), bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᕱ"), True, None, command=method)
        if instance:
            bstack1ll1lllll11_opy_.bstack1llll111l11_opy_(instance, bstack1l111ll11l1_opy_.bstack1l1111111l1_opy_, False)
            instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࠨᕲ"), datetime.now() - bstack1ll1l1l1_opy_)
        return result
        def bstack11llllll1l1_opy_(self, driver: object, framework_name, bstack11l111l11_opy_: str):
            self.bstack1lll1lll1l1_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l111111lll_opy_ = self.bstack11llll1ll1l_opy_[bstack11l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᕳ")]
            req.bstack11l111l11_opy_ = bstack11l111l11_opy_
            req.session_id = self.bin_session_id
            try:
                r = self.bstack1lll1llll1l_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack11l1111_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᕴ") + str(r) + bstack11l1111_opy_ (u"ࠧࠨᕵ"))
                else:
                    bstack11lllll1l11_opy_ = json.loads(r.bstack1l111111111_opy_.decode(bstack11l1111_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᕶ")))
                    if bstack11l111l11_opy_ == bstack11l1111_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫᕷ"):
                        return bstack11lllll1l11_opy_.get(bstack11l1111_opy_ (u"ࠣࡦࡤࡸࡦࠨᕸ"), [])
                    else:
                        return bstack11lllll1l11_opy_.get(bstack11l1111_opy_ (u"ࠤࡧࡥࡹࡧࠢᕹ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack11l1111_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡶࡰࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࠡࡨࡵࡳࡲࠦࡣ࡭࡫࠽ࠤࠧᕺ") + str(e) + bstack11l1111_opy_ (u"ࠦࠧᕻ"))
    @measure(event_name=EVENTS.bstack11llll11_opy_, stage=STAGE.bstack1111llll1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11l1111_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢᕼ"))
            return
        if self.bstack1l11111l1ll_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࡧࡰࡱࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᕽ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack11llllll1l1_opy_(driver, framework_name, bstack11l1111_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦᕾ"))
        bstack1ll1l11ll11_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1111_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧᕿ"), None)
        if not bstack1ll1l11ll11_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᖀ") + str(framework_name) + bstack11l1111_opy_ (u"ࠥࠦᖁ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll1l1l1_opy_ = datetime.now()
        if framework_name == bstack11l1111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᖂ"):
            result = self.bstack1lll1l111ll_opy_.bstack1ll11llll11_opy_(driver, bstack1ll1l11ll11_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l11ll11_opy_)
        instance = bstack1ll1lllll11_opy_.bstack1l1l1lllll1_opy_(driver)
        if instance:
            instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࠣᖃ"), datetime.now() - bstack1ll1l1l1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l11ll1l1_opy_, stage=STAGE.bstack1111llll1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11l1111_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᖄ"))
            return
        if self.bstack1l11111l1ll_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack11llllll1l1_opy_(driver, framework_name, bstack11l1111_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫᖅ"))
        bstack1ll1l11ll11_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1111_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠧᖆ"), None)
        if not bstack1ll1l11ll11_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᖇ") + str(framework_name) + bstack11l1111_opy_ (u"ࠥࠦᖈ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll1l1l1_opy_ = datetime.now()
        if framework_name == bstack11l1111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᖉ"):
            result = self.bstack1lll1l111ll_opy_.bstack1ll11llll11_opy_(driver, bstack1ll1l11ll11_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l11ll11_opy_)
        instance = bstack1ll1lllll11_opy_.bstack1l1l1lllll1_opy_(driver)
        if instance:
            instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺࠤᖊ"), datetime.now() - bstack1ll1l1l1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l11111ll11_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1l1111111ll_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1lll1lll1l1_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1lll1llll1l_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11l1111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᖋ") + str(r) + bstack11l1111_opy_ (u"ࠢࠣᖌ"))
            else:
                self.bstack11llll11ll1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᖍ") + str(e) + bstack11l1111_opy_ (u"ࠤࠥᖎ"))
            traceback.print_exc()
            raise e
    def bstack11llll11ll1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack11l1111_opy_ (u"ࠥࡰࡴࡧࡤࡠࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥᖏ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l11111l1ll_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack11llll1ll1l_opy_[bstack11l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡪࡸࡦࡤࡨࡵࡪ࡮ࡧࡣࡺࡻࡩࡥࠤᖐ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack11llll1ll1l_opy_[bstack11l1111_opy_ (u"ࠧࡺࡨࡠ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠦᖑ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack11llll1ll1l_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l11111111l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l11111l11l_opy_ and command.module == self.bstack1l11111ll1l_opy_:
                        if command.method and not command.method in bstack1l11111111l_opy_:
                            bstack1l11111111l_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l11111111l_opy_[command.method]:
                            bstack1l11111111l_opy_[command.method][command.name] = list()
                        bstack1l11111111l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l11111111l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack11lllll1111_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1lll1l111ll_opy_, bstack1ll1l1l1111_opy_) and method_name != bstack11l1111_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧᖒ"):
            return
        if bstack1ll1lllll11_opy_.bstack1llllll1ll1_opy_(instance, bstack1l111ll11l1_opy_.bstack11llll1l1ll_opy_):
            return
        if f.bstack1ll11l11111_opy_(method_name, *args):
            bstack11llll1l111_opy_ = False
            desired_capabilities = f.bstack1l1llllll11_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1l1lllll111_opy_(instance)
                platform_index = f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1llllll1lll_opy_, 0)
                bstack1l111111l11_opy_ = datetime.now()
                r = self.bstack1l1111111ll_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧᖓ"), datetime.now() - bstack1l111111l11_opy_)
                bstack11llll1l111_opy_ = r.success
            else:
                self.logger.error(bstack11l1111_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡧࡩࡸ࡯ࡲࡦࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠿ࠥᖔ") + str(desired_capabilities) + bstack11l1111_opy_ (u"ࠤࠥᖕ"))
            f.bstack1llll111l11_opy_(instance, bstack1l111ll11l1_opy_.bstack11llll1l1ll_opy_, bstack11llll1l111_opy_)
    def bstack1lll111l1l_opy_(self, test_tags):
        bstack1l1111111ll_opy_ = self.config.get(bstack11l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᖖ"))
        if not bstack1l1111111ll_opy_:
            return True
        try:
            include_tags = bstack1l1111111ll_opy_[bstack11l1111_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᖗ")] if bstack11l1111_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᖘ") in bstack1l1111111ll_opy_ and isinstance(bstack1l1111111ll_opy_[bstack11l1111_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᖙ")], list) else []
            exclude_tags = bstack1l1111111ll_opy_[bstack11l1111_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᖚ")] if bstack11l1111_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᖛ") in bstack1l1111111ll_opy_ and isinstance(bstack1l1111111ll_opy_[bstack11l1111_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᖜ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack11l1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥᖝ") + str(error))
        return False
    def bstack1l11l11l1l_opy_(self, caps):
        try:
            if self.bstack1l11111l1ll_opy_:
                bstack11lllll1lll_opy_ = caps.get(bstack11l1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᖞ"))
                if bstack11lllll1lll_opy_ is not None and str(bstack11lllll1lll_opy_).lower() == bstack11l1111_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨᖟ"):
                    bstack11lllllllll_opy_ = caps.get(bstack11l1111_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᖠ")) or caps.get(bstack11l1111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᖡ"))
                    if bstack11lllllllll_opy_ is not None and int(bstack11lllllllll_opy_) < 11:
                        self.logger.warning(bstack11l1111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡃࡱࡨࡷࡵࡩࡥࠢ࠴࠵ࠥࡧ࡮ࡥࠢࡤࡦࡴࡼࡥ࠯ࠢࡆࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡼࡥࡳࡵ࡬ࡳࡳࠦ࠽ࠣᖢ") + str(bstack11lllllllll_opy_) + bstack11l1111_opy_ (u"ࠤࠥᖣ"))
                        return False
                return True
            bstack11lllll1ll1_opy_ = caps.get(bstack11l1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᖤ"), {}).get(bstack11l1111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᖥ"), caps.get(bstack11l1111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᖦ"), bstack11l1111_opy_ (u"࠭ࠧᖧ")))
            if bstack11lllll1ll1_opy_:
                self.logger.warning(bstack11l1111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᖨ"))
                return False
            browser = caps.get(bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᖩ"), bstack11l1111_opy_ (u"ࠩࠪᖪ")).lower()
            if browser != bstack11l1111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᖫ"):
                self.logger.warning(bstack11l1111_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᖬ"))
                return False
            bstack1l11111l1l1_opy_ = bstack11lllllll1l_opy_
            if not self.config.get(bstack11l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᖭ")) or self.config.get(bstack11l1111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᖮ")):
                bstack1l11111l1l1_opy_ = bstack11llll1lll1_opy_
            browser_version = caps.get(bstack11l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖯ"))
            if not browser_version:
                browser_version = caps.get(bstack11l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᖰ"), {}).get(bstack11l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᖱ"), bstack11l1111_opy_ (u"ࠪࠫᖲ"))
            if browser_version and browser_version != bstack11l1111_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᖳ") and int(browser_version.split(bstack11l1111_opy_ (u"ࠬ࠴ࠧᖴ"))[0]) <= bstack1l11111l1l1_opy_:
                self.logger.warning(bstack11l1111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࠣᖵ") + str(bstack1l11111l1l1_opy_) + bstack11l1111_opy_ (u"ࠢ࠯ࠤᖶ"))
                return False
            bstack11llllll1ll_opy_ = caps.get(bstack11l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᖷ"), {}).get(bstack11l1111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᖸ"))
            if not bstack11llllll1ll_opy_:
                bstack11llllll1ll_opy_ = caps.get(bstack11l1111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᖹ"), {})
            if bstack11llllll1ll_opy_ and bstack11l1111_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᖺ") in bstack11llllll1ll_opy_.get(bstack11l1111_opy_ (u"ࠬࡧࡲࡨࡵࠪᖻ"), []):
                self.logger.warning(bstack11l1111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᖼ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack11l1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᖽ") + str(error))
            return False
    def bstack11llllllll1_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack11lllllll11_opy_ = {
            bstack11l1111_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨᖾ"): test_uuid,
        }
        bstack11lllll11l1_opy_ = {}
        if result.success:
            bstack11lllll11l1_opy_ = json.loads(result.accessibility_execute_params)
        return bstack11lllll11ll_opy_(bstack11lllllll11_opy_, bstack11lllll11l1_opy_)
    def bstack1lllll1lll_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1lll1lll11l_opy_ = None
        try:
            self.bstack1lll1lll1l1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11l1111_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤᖿ")
            req.script_name = bstack11l1111_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣᗀ")
            r = self.bstack1lll1llll1l_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack11l1111_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᗁ") + str(r.error) + bstack11l1111_opy_ (u"ࠧࠨᗂ"))
            else:
                bstack11lllllll11_opy_ = self.bstack11llllllll1_opy_(test_uuid, r)
                bstack1ll1l11ll11_opy_ = r.script
            self.logger.debug(bstack11l1111_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩᗃ") + str(bstack11lllllll11_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll1l11ll11_opy_:
                self.logger.debug(bstack11l1111_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᗄ") + str(framework_name) + bstack11l1111_opy_ (u"ࠣࠢࠥᗅ"))
                return
            bstack1lll1lll11l_opy_ = bstack1lll1l1l11l_opy_.bstack1llll1lllll_opy_(EVENTS.bstack11lllll1l1l_opy_.value)
            self.bstack11lllll111l_opy_(driver, bstack1ll1l11ll11_opy_, bstack11lllllll11_opy_, framework_name)
            self.logger.info(bstack11l1111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧᗆ"))
            bstack1lll1l1l11l_opy_.end(EVENTS.bstack11lllll1l1l_opy_.value, bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᗇ"), bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᗈ"), True, None, command=bstack11l1111_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᗉ"),test_name=name)
        except Exception as bstack1l111111l1l_opy_:
            self.logger.error(bstack11l1111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᗊ") + bstack11l1111_opy_ (u"ࠢࡴࡶࡵࠬࡵࡧࡴࡩࠫࠥᗋ") + bstack11l1111_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᗌ") + str(bstack1l111111l1l_opy_))
            bstack1lll1l1l11l_opy_.end(EVENTS.bstack11lllll1l1l_opy_.value, bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᗍ"), bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᗎ"), False, bstack1l111111l1l_opy_, command=bstack11l1111_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᗏ"),test_name=name)
    def bstack11lllll111l_opy_(self, driver, bstack1ll1l11ll11_opy_, bstack11lllllll11_opy_, framework_name):
        if framework_name == bstack11l1111_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᗐ"):
            self.bstack1lll1l111ll_opy_.bstack1ll11llll11_opy_(driver, bstack1ll1l11ll11_opy_, bstack11lllllll11_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll1l11ll11_opy_, bstack11lllllll11_opy_))
    def _11llllll11l_opy_(self, instance: bstack1lllll111ll_opy_, args: Tuple) -> list:
        bstack11l1111_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡷࡥ࡬ࡹࠠࡣࡣࡶࡩࡩࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࠣࠤࠥᗑ")
        if bstack11l1111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᗒ") in instance.bstack1l1l1lll111_opy_:
            return args[2].tags if hasattr(args[2], bstack11l1111_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᗓ")) else []
        if hasattr(args[0], bstack11l1111_opy_ (u"ࠩࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠧᗔ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l111111ll1_opy_(self, tags, capabilities):
        return self.bstack1lll111l1l_opy_(tags) and self.bstack1l11l11l1l_opy_(capabilities)