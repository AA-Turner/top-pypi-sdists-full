# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
bstack1l1llll_opy_ (u"ࠦࠧࠨࡔࡦࡵࡷࡇࡱ࡯ࡥ࡯ࡶࠣࡅࡕࡏࠠࡧࡱࡵࠤࡻࡧ࡮ࡪ࡮࡯ࡥࠥࡖࡹࡵࡪࡲࡲࠥࡺࡥࡴࡶࡶࠤࡼ࡯ࡴࡩࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳ࠴ࠊࡕࡪ࡬ࡷࠥࡳ࡯ࡥࡷ࡯ࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡹࠠࡶࡵࡨࡶࠥ࡫ࡸࡱࡱࡶࡩࡩࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡴࠢࡩࡳࡷࠦࡶࡢࡰ࡬ࡰࡱࡧࠠࡑࡻࡷ࡬ࡴࡴࠠࡶࡵࡨࡶࡸࠦࠨࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡲࡼࡸࡪࡹࡴࠡࡱࡵࠤࡴࡺࡨࡦࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡷ࠮ࠐࡴࡰࠢࡰࡥࡳࡻࡡ࡭࡮ࡼࠤ࡮ࡴࡳࡵࡴࡸࡱࡪࡴࡴࠡࡶ࡫ࡩ࡮ࡸࠠࡵࡧࡶࡸࡸࠦࡡ࡯ࡦࠣࡷࡪࡴࡤࠡࡶࡨࡷࡹࠦ࡬ࡪࡨࡨࡧࡾࡩ࡬ࡦࠢࡨࡺࡪࡴࡴࡴࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡙࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࠍࡘ࡭࡫ࠠࡕࡧࡶࡸࡈࡲࡩࡦࡰࡷࠤࡨࡲࡡࡴࡵࠣࡥࡱࡲ࡯ࡸࡵࠣࡹࡸ࡫ࡲࡴࠢࡷࡳ࠿ࠐ࠭ࠡࡕࡨࡸࠥࡺࡥࡴࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࠮࡮ࡢ࡯ࡨ࠰ࠥ࡮ࡩࡦࡴࡤࡶࡨ࡮ࡹ࠭ࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬࠮ࠐ࠭ࠡࡏࡤࡶࡰࠦࡴࡦࡵࡷࠤࡸࡺࡡࡳࡶ࠲ࡪ࡮ࡴࡩࡴࡪࠣࡩࡻ࡫࡮ࡵࡵࠍ࠱ࠥࡓࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦ࡯࡯ࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡸࡸࡴࡳࡡࡵࡧ࠲ࡅࡵࡶࠠࡂࡷࡷࡳࡲࡧࡴࡦࠌ࠰ࠤࡘ࡫࡮ࡥࠢࡷࡩࡸࡺࠠࡳࡧࡶࡹࡱࡺࡳࠡࠪࡓࡥࡸࡹ࠯ࡇࡣ࡬ࡰ࠮ࠦࡴࡰࠢࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࠋࡇࡻࡥࡲࡶ࡬ࡦࠢࡸࡷࡦ࡭ࡥ࠻ࠌࠣࠤࠥࠦࡠࡡࡢࡳࡽࡹ࡮࡯࡯ࠌࠣࠤࠥࠦࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱ࠮ࡤ࡮࡬ࡩࡳࡺࠠࡪ࡯ࡳࡳࡷࡺࠠࡕࡧࡶࡸࡈࡲࡩࡦࡰࡷࠎࠥࠦࠠࠡࡨࡵࡳࡲࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡ࡫ࡰࡴࡴࡸࡴࠡࡹࡨࡦࡩࡸࡩࡷࡧࡵࠎࠥࠦࠠࠡࡨࡵࡳࡲࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡨ࡮ࡲࡰ࡯ࡨ࠲ࡴࡶࡴࡪࡱࡱࡷࠥ࡯࡭ࡱࡱࡵࡸࠥࡕࡰࡵ࡫ࡲࡲࡸࠐࠠࠡࠢࠣࡸࡪࡹࡴࡠࡥ࡯࡭ࡪࡴࡴࠡ࠿ࠣࡘࡪࡹࡴࡄ࡮࡬ࡩࡳࡺࠨࠪࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠴ࡳࡦࡶࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠮ࠢ࡮ࡻࡢࡸࡪࡹࡴࠣࠫࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠮ࡴࡧࡷࡣࡹ࡫ࡳࡵࡡ࡫࡭ࡪࡸࡡࡳࡥ࡫ࡽ࠭ࡡࠢࡵࡧࡶࡸࡸࠨࠬࠡࠤࡐࡽ࡙࡫ࡳࡵࡕࡸ࡭ࡹ࡫ࠢ࡞ࠫࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠮ࡴࡧࡷࡣ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠨࠣࡶࡨࡷࡹࡹ࠯࡮ࡻࡢࡸࡪࡹࡴ࠯ࡲࡼࠦ࠮ࠐࠠࠡࠢࠣࡸࡪࡹࡴࡠࡥ࡯࡭ࡪࡴࡴ࠯ࡵࡷࡥࡷࡺࠨࠪࠌࠣࠤࠥࠦࡴࡳࡻ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡵࡰࡵࡵࠣࡁࠥࡕࡰࡵ࡫ࡲࡲࡸ࠮ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧࡶ࡮ࡼࡥࡳࠢࡀࠤࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡓࡧࡰࡳࡹ࡫ࠨࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࡀࠦ࡭ࡻࡢࡠࡷࡵࡰࠧ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡳ࠾ࡱࡳࡸࡸ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡩࡨࡸ࠭࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡦࡺࡤࡱࡵࡲࡥ࠯ࡥࡲࡱࠬ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡣࡶࡷࡪࡸࡴࠡࡦࡵ࡭ࡻ࡫ࡲ࠯ࡶ࡬ࡸࡱ࡫ࠠ࠾࠿ࠣࠦࡊࡾࡡ࡮ࡲ࡯ࡩࠥࡊ࡯࡮ࡣ࡬ࡲࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡧࡶࡸࡤࡩ࡬ࡪࡧࡱࡸ࠳ࡳࡡࡳ࡭ࡢࡴࡦࡹࡳࡦࡦࠫ࠭ࠏࠦࠠࠡࠢࡨࡼࡨ࡫ࡰࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡳࠡࡧ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡧࡱ࡯ࡥ࡯ࡶ࠱ࡱࡦࡸ࡫ࡠࡨࡤ࡭ࡱ࡫ࡤࠩࡧࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࡸࡡࡪࡵࡨࠎࠥࠦࠠࠡࡨ࡬ࡲࡦࡲ࡬ࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡮࡬ࠠࡥࡴ࡬ࡺࡪࡸ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡳ࡫ࡹࡩࡷ࠴ࡱࡶ࡫ࡷࠬ࠮ࠐࠠࠡࠢࠣࡤࡥࡦࠊࠣࠤࠥ૟")
import threading
import logging
import os
import traceback
import inspect
import ast
from dataclasses import dataclass
from typing import Optional, List
from bstack_utils.config import Config
from bstack_utils.helper import bstack1l1111ll_opy_, bstack1ll1l11ll_opy_, Result
from bstack_utils.test_data import bstack1l1l1111_opy_
from bstack_utils.testhub_handler import TestHubHandler
from bstack_utils.bstack1l1ll1ll1_opy_ import bstack1lll111ll_opy_
from bstack_utils.constants import bstack1ll1111ll_opy_, MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
from bstack_utils import accessibility as a11y
from bstack_utils.accessibility_scripts import accessibility_scripts
logger = logging.getLogger(__name__)
@dataclass
class bstack1ll11llll_opy_:
    bstack1l1llll_opy_ (u"ࠧࠨࠢࡊࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧࡢࡰࡷࡷࠤࡹ࡮ࡥࠡࡥࡤࡰࡱ࡯࡮ࡨࠢࡩࡹࡳࡩࡴࡪࡱࡱ࠳ࡲ࡫ࡴࡩࡱࡧ࠲ࠏࠦࠠࠡࠢࡖ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡊࡢࡸࡤࠫࡸࠦࡤࡦࡶࡨࡧࡹࡉࡡ࡭࡮ࡨࡶࡎࡴࡦࡰࡕࡦࡥࡱࡧࡢ࡭ࡧࠫ࠭ࠥࡸࡥࡴࡷ࡯ࡸ࠳ࠐࠠࠡࠢࠣࠦࠧࠨૠ")
    module_name: Optional[str] = None
    class_name: Optional[str] = None
    function_name: Optional[str] = None
    bstack1ll111ll1_opy_: Optional[str] = None
    line_number: Optional[int] = None
class TestClient:
    bstack1l1llll_opy_ (u"ࠨࠢࠣࡗࡶࡩࡷࠦࡥࡹࡲࡲࡷࡪࡪࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࡵࠣࡪࡴࡸࠠࡷࡣࡱ࡭ࡱࡲࡡࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡶࡨࡷࡹࠦࡩ࡯ࡵࡷࡶࡺࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡨࡲࡡࡴࡵࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥࡧࠠࡣࡷ࡬ࡰࡩ࡫ࡲࠡࡲࡤࡸࡹ࡫ࡲ࡯ࠢ࡬ࡲࡹ࡫ࡲࡧࡣࡦࡩࠥ࡬࡯ࡳࠢࡦࡳࡳ࡬ࡩࡨࡷࡵ࡭ࡳ࡭ࠠࡢࡰࡧࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠏࠦࠠࠡࠢࡹࡥࡳ࡯࡬࡭ࡣࠣࡔࡾࡺࡨࡰࡰࠣࡸࡪࡹࡴࡴࠢࡺ࡭ࡹ࡮ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱ࠲ࠥࡏࡴࠡࡪࡤࡲࡩࡲࡥࡴ࠼ࠍࠤࠥࠦࠠ࠮ࠢࡗࡩࡸࡺࠠ࡭࡫ࡩࡩࡨࡿࡣ࡭ࡧࠣࡩࡻ࡫࡮ࡵࡵࠣࠬࡸࡺࡡࡳࡶ࠯ࠤ࡫࡯࡮ࡪࡵ࡫࠭ࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠊࠡࠢࠣࠤ࠲ࠦࡓࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦ࡯࡯ࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠍࠤࠥࠦࠠ࠮ࠢࡖࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡱࡦࡸ࡫ࡪࡰࡪࠤ࠭ࡶࡡࡴࡵࡨࡨ࠴࡬ࡡࡪ࡮ࡨࡨ࠮ࠐࠠࠡࠢࠣࡅࡹࡺࡲࡪࡤࡸࡸࡪࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪࠦࠨࡴࡶࡵ࠭࠿ࠦࡎࡢ࡯ࡨࠤࡴ࡬ࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠌࠣࠤࠥࠦࠠࠡࠢࠣࡣࡹ࡫ࡳࡵࡡ࡫࡭ࡪࡸࡡࡳࡥ࡫ࡽࠥ࠮࡬ࡪࡵࡷ࠭࠿ࠦࡈࡪࡧࡵࡥࡷࡩࡨࡪࡥࡤࡰࠥࡹࡣࡰࡲࡨࠤࡴ࡬ࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࠫࡩ࠳࡭࠮࠭ࠢ࡞ࠦࡲࡵࡤࡶ࡮ࡨࠦ࠱ࠦࠢࡤ࡮ࡤࡷࡸࠨ࡝ࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࡣ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠠࠩࡵࡷࡶ࠮ࡀࠠࡇ࡫࡯ࡩࠥࡶࡡࡵࡪࠣࡻ࡭࡫ࡲࡦࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡮ࡹࠠ࡭ࡱࡦࡥࡹ࡫ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࡢࡸࡪࡹࡴࡠࡦࡤࡸࡦࠦࠨࡕࡧࡶࡸࡉࡧࡴࡢࠫ࠽ࠤࡎࡴࡴࡦࡴࡱࡥࡱࠦࡴࡦࡵࡷࠤࡩࡧࡴࡢࠢࡲࡦ࡯࡫ࡣࡵࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠥ࠮ࡳࡵࡴࠬ࠾ࠥࡏࡓࡐࠢࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠥࡽࡨࡦࡰࠣࡸࡪࡹࡴࠡࡵࡷࡥࡷࡺࡥࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࡣࡩࡸࡩࡷࡧࡵࠤ࠭࡝ࡥࡣࡆࡵ࡭ࡻ࡫ࡲࠪ࠼ࠣࡖࡪ࡬ࡥࡳࡧࡱࡧࡪࠦࡴࡰࠢࡷ࡬ࡪࠦࡓࡦ࡮ࡨࡲ࡮ࡻ࡭࡙ࠡࡨࡦࡉࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠐࠠࠡࠢࠣࠦࠧࠨૡ")
    def __init__(self):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࠦࡡࠡࡰࡨࡻ࡚ࠥࡥࡴࡶࡆࡰ࡮࡫࡮ࡵࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠧࠨࠢૢ")
        self._1ll11ll1l_opy_ = None
        self._1l1l1l111_opy_ = []
        self._file_path = None
        self._1l1l1l1ll_opy_ = None
        self._1l1l1llll_opy_ = None
        self._driver = None
        self._1l1ll11ll_opy_ = False
        self._1l1llll11_opy_ = None
        self._started = False
        self._1l1ll1l1l_opy_ = False
        self._1ll11lll1_opy_ = None
        self._1l11llll1_opy_ = None
        self._a11y_started = False
        self._a11y_stop_done = False
        self._1l1l11lll_opy_ = None
    def _1lll111l1_opy_(self) -> bstack1ll11llll_opy_:
        bstack1l1llll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡣࡢ࡮ࡤࡦࡱ࡫ࠠࡢࡲࡳࡶࡴࡧࡣࡩࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡩࡡ࡭࡮ࡨࡶࠥ࡯࡮ࡧࡱࠣࡹࡸ࡯࡮ࡨࠢ࡬ࡲࡸࡶࡥࡤࡶࠣࡱࡴࡪࡵ࡭ࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡝࡯ࡳ࡭ࡶࠤࡷ࡫ࡧࡢࡴࡧࡰࡪࡹࡳࠡࡱࡩࠤࡵࡸ࡯࡫ࡧࡦࡸࠥࡹࡴࡳࡷࡦࡸࡺࡸࡥࠡࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠ࡭ࡱࡦࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡈࡧ࡬࡭ࡧࡵࡍࡳ࡬࡯ࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡳ࡯ࡥࡷ࡯ࡩ࠱ࠦࡣ࡭ࡣࡶࡷ࠱ࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡡ࡯ࡦࠣࡷࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥૣ")
        try:
            stack = inspect.stack()
            caller_frame = None
            for i, bstack1l1l111l1_opy_ in enumerate(stack):
                if bstack1l1llll_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵ࠰ࡳࡽࠬ૤") not in bstack1l1l111l1_opy_.filename and \
                   bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰ࠭૥") not in bstack1l1l111l1_opy_.filename:
                    caller_frame = bstack1l1l111l1_opy_
                    break
            if caller_frame is None:
                caller_frame = stack[2] if len(stack) > 2 else stack[-1]
            bstack1ll11l1l1_opy_ = caller_frame.filename
            function_name = caller_frame.function
            line_number = caller_frame.lineno
            if bstack1ll11l1l1_opy_ and os.path.exists(bstack1ll11l1l1_opy_):
                bstack1ll11l1l1_opy_ = os.path.abspath(bstack1ll11l1l1_opy_)
            class_name = None
            try:
                local_vars = caller_frame.frame.f_locals
                if bstack1l1llll_opy_ (u"ࠫࡸ࡫࡬ࡧࠩ૦") in local_vars:
                    class_name = type(local_vars[bstack1l1llll_opy_ (u"ࠬࡹࡥ࡭ࡨࠪ૧")]).__name__
                elif bstack1l1llll_opy_ (u"࠭ࡣ࡭ࡵࠪ૨") in local_vars:
                    class_name = local_vars[bstack1l1llll_opy_ (u"ࠧࡤ࡮ࡶࠫ૩")].__name__
            except (AttributeError, TypeError, KeyError):
                pass
            module_name = None
            try:
                module = inspect.getmodule(caller_frame.frame)
                if module:
                    module_name = module.__name__
            except (AttributeError, TypeError):
                pass
            logger.debug(bstack1l1llll_opy_ (u"ࠣࡅࡤࡰࡱ࡫ࡲࡊࡰࡩࡳ࠿ࠦ࡭ࡰࡦࡸࡰࡪࡃࡻࡾ࠮ࠣࡧࡱࡧࡳࡴ࠿ࡾࢁ࠱ࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮࠾ࡽࢀ࠰ࠥ࡬ࡩ࡭ࡧࡀࡿࢂࠨ૪").format(
                        module_name, class_name, function_name, bstack1ll11l1l1_opy_))
            return bstack1ll11llll_opy_(
                module_name=module_name,
                class_name=class_name,
                function_name=function_name,
                bstack1ll111ll1_opy_=bstack1ll11l1l1_opy_,
                line_number=line_number
            )
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡦࡨࡸࡪࡩࡴࡪࡰࡪࠤࡨࡧ࡬࡭ࡧࡵࠤ࡮ࡴࡦࡰ࠼ࠣࡿࢂࠨ૫").format(e))
            return bstack1ll11llll_opy_()
    def _1ll1l1l11_opy_(self, file_path: str, function_name: Optional[str] = None,
                                       class_name: Optional[str] = None) -> Optional[str]:
        bstack1l1llll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡆࡺࡷࡶࡦࡩࡴࡴࠢࡷ࡬ࡪࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡢࡰࡦࡼࠤ࡫ࡸ࡯࡮ࠢࡤࠤࡕࡿࡴࡩࡱࡱࠤࡸࡵࡵࡳࡥࡨࠤ࡫࡯࡬ࡦࠢࡸࡷ࡮ࡴࡧࠡࡃࡖࡘࠥࡶࡡࡳࡵ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡋࡩࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠤ࡮ࡹࠠࡏࡱࡱࡩࠥࡵࡲࠡࠩ࠿ࡱࡴࡪࡵ࡭ࡧࡁࠫࠥ࠮࡭ࡰࡦࡸࡰࡪ࠳࡬ࡦࡸࡨࡰࠥࡩ࡯ࡥࡧࠬ࠰ࠥࡸࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡫࡯࡬ࡦࠢࡦࡳࡳࡺࡥ࡯ࡶࠣࡩࡽࡩ࡬ࡶࡦ࡬ࡲ࡬ࠦࡩ࡮ࡲࡲࡶࡹࠦࡳࡵࡣࡷࡩࡲ࡫࡮ࡵࡵࠣࡥࡹࠦࡴࡩࡧࠣࡸࡴࡶ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡦࡪ࡮ࡨࡣࡵࡧࡴࡩ࠼ࠣࡔࡦࡺࡨࠡࡶࡲࠤࡹ࡮ࡥࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡵࡲࡹࡷࡩࡥࠡࡨ࡬ࡰࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨ࠾ࠥࡔࡡ࡮ࡧࠣࡳ࡫ࠦࡴࡩࡧࠣࡪࡺࡴࡣࡵ࡫ࡲࡲ࠴ࡳࡥࡵࡪࡲࡨࠥࡺ࡯ࠡࡧࡻࡸࡷࡧࡣࡵ࠮ࠣࡳࡷࠦࡎࡰࡰࡨ࠳ࡁࡳ࡯ࡥࡷ࡯ࡩࡃࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺ࡯ࠡࡴࡨࡸࡺࡸ࡮ࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧࠣࡧࡴࡴࡴࡦࡰࡷࠤࡼ࡯ࡴࡩࡱࡸࡸࠥ࡯࡭ࡱࡱࡵࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡲࡡࡴࡵࡢࡲࡦࡳࡥ࠻ࠢࡒࡴࡹ࡯࡯࡯ࡣ࡯ࠤࡨࡲࡡࡴࡵࠣࡲࡦࡳࡥࠡ࡫ࡩࠤࡪࡾࡴࡳࡣࡦࡸ࡮ࡴࡧࠡࡣࠣࡱࡪࡺࡨࡰࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡥࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡤࡲࡨࡾࠦࡡࡴࠢࡤࠤࡸࡺࡲࡪࡰࡪ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡨࡼࡹࡸࡡࡤࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ૬")
        if not file_path or not os.path.exists(file_path):
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡈࡧ࡮࡯ࡱࡷࠤࡪࡾࡴࡳࡣࡦࡸࠥࡳࡥࡵࡪࡲࡨࠥ࠳ࠠࡧ࡫࡯ࡩࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠻ࠢࡾࢁࠧ૭").format(file_path))
            return None
        try:
            with open(file_path, bstack1l1llll_opy_ (u"ࠬࡸࠧ૮"), encoding=bstack1l1llll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ૯")) as f:
                bstack1l1ll1111_opy_ = f.read()
            if not function_name or function_name == bstack1l1llll_opy_ (u"ࠧ࠽࡯ࡲࡨࡺࡲࡥ࠿ࠩ૰"):
                try:
                    tree = ast.parse(bstack1l1ll1111_opy_)
                    bstack1ll1l1lll_opy_ = None
                    for node in tree.body:
                        if not isinstance(node, (ast.Import, ast.ImportFrom)):
                            bstack1ll1l1lll_opy_ = getattr(node, bstack1l1llll_opy_ (u"ࠨ࡮࡬ࡲࡪࡴ࡯ࠨ૱"), None)
                            break
                    if bstack1ll1l1lll_opy_ is not None:
                        source_lines = bstack1l1ll1111_opy_.split(bstack1l1llll_opy_ (u"ࠩ࡟ࡲࠬ૲"))
                        bstack1l1llll1l_opy_ = bstack1l1llll_opy_ (u"ࠪࡠࡳ࠭૳").join(source_lines[bstack1ll1l1lll_opy_ - 1:])
                        logger.debug(bstack1l1llll_opy_ (u"ࠦࡊࡾࡴࡳࡣࡦࡸࡪࡪࠠ࡮ࡱࡧࡹࡱ࡫࠭࡭ࡧࡹࡩࡱࠦࡣࡰࡦࡨࠤࡼ࡯ࡴࡩࡱࡸࡸࠥ࡯࡭ࡱࡱࡵࡸࡸࠦࠨࡼࡿࠣࡧ࡭ࡧࡲࡴࠫࠥ૴").format(len(bstack1l1llll1l_opy_)))
                        return bstack1l1llll1l_opy_
                    else:
                        logger.debug(bstack1l1llll_opy_ (u"ࠧࡔ࡯ࠡࡰࡲࡲ࠲࡯࡭ࡱࡱࡵࡸࠥࡩ࡯ࡥࡧࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࡳ࡯ࡥࡷ࡯ࡩ࠲ࡲࡥࡷࡧ࡯ࠤࡪࡾࡴࡳࡣࡦࡸ࡮ࡵ࡮࠯ࠤ૵"))
                        return bstack1l1llll_opy_ (u"࠭ࠧ૶")
                except Exception as e:
                    logger.debug(bstack1l1llll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡂࡕࡗࠤ࡫ࡵࡲࠡ࡯ࡲࡨࡺࡲࡥ࠮࡮ࡨࡺࡪࡲࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤ૷").format(e))
                    return None
            tree = ast.parse(bstack1l1ll1111_opy_)
            bstack1ll11ll11_opy_ = None
            for node in ast.walk(tree):
                if class_name:
                    if isinstance(node, ast.ClassDef) and node.name == class_name:
                        for item in node.body:
                            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                if item.name == function_name:
                                    bstack1ll11ll11_opy_ = item
                                    break
                else:
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if node.name == function_name:
                            bstack1ll11ll11_opy_ = node
                            break
            if bstack1ll11ll11_opy_ is None:
                logger.debug(bstack1l1llll_opy_ (u"ࠣࡈࡸࡲࡨࡺࡩࡰࡰࠣࠫࢀࢃࠧࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿࠥ૸").format(function_name, file_path))
                return None
            bstack1l1l1ll1l_opy_ = bstack1ll11ll11_opy_.lineno - 1
            bstack1l1llllll_opy_ = bstack1ll11ll11_opy_.end_lineno if hasattr(bstack1ll11ll11_opy_, bstack1l1llll_opy_ (u"ࠩࡨࡲࡩࡥ࡬ࡪࡰࡨࡲࡴ࠭ૹ")) else None
            if bstack1l1llllll_opy_ is None:
                bstack1l1llllll_opy_ = self._1l1l11111_opy_(bstack1l1ll1111_opy_.split(bstack1l1llll_opy_ (u"ࠪࡠࡳ࠭ૺ")), bstack1l1l1ll1l_opy_)
            source_lines = bstack1l1ll1111_opy_.split(bstack1l1llll_opy_ (u"ࠫࡡࡴࠧૻ"))
            bstack1l1lll1l1_opy_ = source_lines[bstack1l1l1ll1l_opy_:bstack1l1llllll_opy_]
            bstack1l1l1ll11_opy_ = bstack1l1llll_opy_ (u"ࠬࡢ࡮ࠨૼ").join(bstack1l1lll1l1_opy_)
            logger.debug(bstack1l1llll_opy_ (u"ࠨࡅࡹࡶࡵࡥࡨࡺࡥࡥࠢࡾࢁࠥࡩࡨࡢࡴࡤࡧࡹ࡫ࡲࡴࠢࡲࡪࠥࡳࡥࡵࡪࡲࡨࠥࡨ࡯ࡥࡻࠥ૽").format(len(bstack1l1l1ll11_opy_)))
            return bstack1l1l1ll11_opy_
        except SyntaxError as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠢࡔࡻࡱࡸࡦࡾࠠࡦࡴࡵࡳࡷࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡼࡿ࠽ࠤࢀࢃࠢ૾").format(file_path, e))
            return None
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡦࡺࡷࡶࡦࡩࡴࡪࡰࡪࠤࡲ࡫ࡴࡩࡱࡧࠤࡧࡵࡤࡺ࠼ࠣࡿࢂࠨ૿").format(e))
            return None
    def _1l1l11111_opy_(self, lines: List[str], bstack1l1l1ll1l_opy_: int) -> int:
        bstack1l1llll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡢ࡮࡯ࡦࡦࡩ࡫ࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡪࡴࡤࠡࡤࡼࠤࡦࡴࡡ࡭ࡻࡽ࡭ࡳ࡭ࠠࡪࡰࡧࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ଀")
        if bstack1l1l1ll1l_opy_ >= len(lines):
            return len(lines)
        bstack1l11lllll_opy_ = lines[bstack1l1l1ll1l_opy_]
        bstack1ll1l1111_opy_ = len(bstack1l11lllll_opy_) - len(bstack1l11lllll_opy_.lstrip())
        for i in range(bstack1l1l1ll1l_opy_ + 1, len(lines)):
            line = lines[i]
            stripped = line.strip()
            if not stripped or stripped.startswith(bstack1l1llll_opy_ (u"ࠪࠧࠬଁ")):
                continue
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= bstack1ll1l1111_opy_ and stripped:
                return i
        return len(lines)
    def _1lll1111l_opy_(self) -> dict:
        bstack1l1llll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡆࡆ࡙ࠦࠨࡄ࡮ࡲࡹࡩࠦࡂࡳࡱࡺࡷࡪࡸࠠࡕࡧࡶࡸ࡮ࡴࡧࠪࠢࡶࡩࡸࡹࡩࡰࡰࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡨࡼࡹࡸࡡࡤࡶࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴ࡙ࠡࡨࡦࡉࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡆ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡤࡲࡩࠦࡃࡃࡖࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡴࡦࡰࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨଂ")
        meta = {
            bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ଃ"): bstack1l1llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧ଄"),
            bstack1l1llll_opy_ (u"ࠧ࡮ࡣࡱࡹࡦࡲ࡟ࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࠬଅ"): True,
            bstack1l1llll_opy_ (u"ࠨࡣࡪࡩࡳࡺ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨଆ"): self._1ll111l11_opy_(),
            bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡵࡻࡳࡩࠬଇ"): bstack1l1llll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡦࡲࠧଈ")
        }
        driver = self._1ll1111l1_opy_()
        if driver is None:
            meta[bstack1l1llll_opy_ (u"ࠫࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡯࡭ࡳࡱࡥࡥࠩଉ")] = False
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡔ࡯࡙ࠡࡨࡦࡉࡸࡩࡷࡧࡵࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡄࡄࡗࠤ࡮ࡴࡦࡰࠢࡨࡼࡹࡸࡡࡤࡶ࡬ࡳࡳࠨଊ"))
            return meta
        try:
            session_id = getattr(driver, bstack1l1llll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪଋ"), None)
            if session_id:
                meta[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪଌ")] = str(session_id)
                meta[bstack1l1llll_opy_ (u"ࠨࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡬ࡪࡰ࡮ࡩࡩ࠭଍")] = True
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡈࡼࡹࡸࡡࡤࡶࡨࡨࠥࡉࡂࡕࠢࡶࡩࡸࡹࡩࡰࡰࠣࡍࡉࡀࠠࡼࡿࠥ଎").format(session_id))
                try:
                    caps = driver.capabilities if hasattr(driver, bstack1l1llll_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩଏ")) else {}
                    browser_name = caps.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଐ"))
                    if browser_name:
                        meta[bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭଑")] = browser_name
                    browser_version = caps.get(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ଒")) or caps.get(bstack1l1llll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨଓ"))
                    if browser_version:
                        meta[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪଔ")] = browser_version
                    platform = caps.get(bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨକ")) or caps.get(bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬଖ")) or caps.get(bstack1l1llll_opy_ (u"ࠫࡴࡹࠧଗ"))
                    if platform:
                        meta[bstack1l1llll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧଘ")] = str(platform)
                    logger.debug(bstack1l1llll_opy_ (u"ࠨࡅࡹࡶࡵࡥࡨࡺࡥࡥࠢࡥࡶࡴࡽࡳࡦࡴࠣ࡭ࡳ࡬࡯࠻ࠢࡾࢁ࠴ࢁࡽ࠰ࡽࢀࠦଙ").format(browser_name, browser_version, platform))
                except Exception as bstack1l1lllll1_opy_:
                    logger.debug(bstack1l1llll_opy_ (u"ࠢࡄࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡩࡽࡺࡲࡢࡥࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠾ࠥࢁࡽࠣଚ").format(bstack1l1lllll1_opy_))
            else:
                meta[bstack1l1llll_opy_ (u"ࠨࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡬ࡪࡰ࡮ࡩࡩ࠭ଛ")] = False
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡑࡳࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡉࡅࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥ࡬ࡲࡰ࡯࡛ࠣࡪࡨࡄࡳ࡫ࡹࡩࡷࠨଜ"))
        except Exception as e:
            meta[bstack1l1llll_opy_ (u"ࠪࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡮࡬ࡲࡰ࡫ࡤࠨଝ")] = False
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡩࡽࡺࡲࡢࡥࡷ࡭ࡳ࡭ࠠࡄࡄࡗࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯࡮ࡧࡱ࠽ࠤࢀࢃࠢଞ").format(e))
        return meta
    def _1l1ll111l_opy_(self) -> dict:
        bstack1l1llll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡅࡹ࡮ࡲࡤࠡ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠠࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡇࡇ࡚ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࡵࠣࡻ࡭࡫ࡴࡩࡧࡵࠤࡹ࡫ࡳࡵࠢࡶ࡬ࡴࡽࡳࠡࡣࡶࠤ࡚ࠧࡥࡴࡶࠣࡶࡦࡴࠠࡰࡰࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠧࠦ࡯ࡳࠢࠥࡉࡽࡺࡥࡳࡰࡤࡰࠥࡍࡲࡪࡦࠥࠤ࡮ࡴࠠࡕࡔࡄ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡄࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡻ࡮ࡺࡨࠡࡲࡵࡳࡻ࡯ࡤࡦࡴࠣ࡯ࡪࡿࠠࠩࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨࠢࡲࡶࠥ࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬ࠯ࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯࡮ࡧࡱࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢଟ")
        driver = self._1ll1111l1_opy_()
        if driver is None:
            logger.debug(bstack1l1llll_opy_ (u"ࠨࡎࡰ࡚ࠢࡩࡧࡊࡲࡪࡸࡨࡶࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠠࡥࡣࡷࡥࠧଠ"))
            return {}
        try:
            bstack1l1l11ll1_opy_ = {}
            session_id = getattr(driver, bstack1l1llll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫଡ"), None)
            if session_id:
                bstack1l1l11ll1_opy_[bstack1l1llll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬଢ")] = str(session_id)
            caps = getattr(driver, bstack1l1llll_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨଣ"), {}) or {}
            if caps:
                bstack1l1l11ll1_opy_[bstack1l1llll_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩତ")] = caps
                bstack1l1l11ll1_opy_[bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬଥ")] = caps.get(bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଦ"))
                bstack1l1l11ll1_opy_[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨଧ")] = caps.get(bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨନ"))
                bstack1l1l11ll1_opy_[bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ଩")] = caps.get(bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨପ"))
                bstack1l1l11ll1_opy_[bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ଫ")] = caps.get(bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ବ"))
            bstack1l1l11l1l_opy_ = caps.get(bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ଭ"), {})
            if bstack1l1l11l1l_opy_.get(bstack1l1llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪମ"), False):
                bstack1l1l11ll1_opy_[bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨଯ")] = bstack1l1llll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬର")
            elif os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ଱"), bstack1l1llll_opy_ (u"ࠪࠫଲ")).lower() == bstack1l1llll_opy_ (u"ࠫࡹࡸࡵࡦࠩଳ"):
                bstack1l1l11ll1_opy_[bstack1l1llll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭଴")] = bstack1l1llll_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬଵ")
            else:
                bstack1l1l11ll1_opy_[bstack1l1llll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨଶ")] = bstack1l1llll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪଷ")
            try:
                from bstack_utils.config import Config
                global_config = Config.bstack1lll1l11_opy_()
                bstack1ll1l1l1l_opy_ = global_config.get_property(bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪସ"), False)
            except (ImportError, AttributeError):
                bstack1ll1l1l1l_opy_ = False
            if not bstack1ll1l1l1l_opy_:
                try:
                    command_executor = getattr(driver, bstack1l1llll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭ହ"), None)
                    if command_executor:
                        remote_url = getattr(command_executor, bstack1l1llll_opy_ (u"ࠫࡤࡻࡲ࡭ࠩ଺"), bstack1l1llll_opy_ (u"ࠬ࠭଻")) or bstack1l1llll_opy_ (u"଼࠭ࠧ")
                        if bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ଽ") in remote_url.lower():
                            bstack1ll1l1l1l_opy_ = True
                except AttributeError:
                    pass
            if bstack1ll1l1l1l_opy_:
                return {bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧା"): bstack1l1l11ll1_opy_}
            else:
                return {bstack1l1llll_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨି"): bstack1l1l11ll1_opy_}
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡥࡹ࡮ࡲࡤࡪࡰࡪࠤ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧୀ").format(e))
            return {}
    def _1ll111l11_opy_(self) -> str:
        bstack1l1llll_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡰࡳࡧࡩ࡭ࡽ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡩࡳࡷࡳࡡࡵࠢࡰࡥࡹࡩࡨࡪࡰࡪࠤࡏࡧࡶࡢࠩࡶࠤࡦ࡭ࡥ࡯ࡶࡢࡺࡪࡸࡳࡪࡱࡱ࠾ࠥ࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩ࠭ࡴࡦ࡮࠳ࢀࡼࡥࡳࡵ࡬ࡳࡳࢃࠧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧୁ")
        try:
            from browserstack_sdk import __version__
            return bstack1l1llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠳ࡳࡥ࡭࠲ࡿࢂ࠭ୂ").format(__version__)
        except (ImportError, AttributeError):
            return bstack1l1llll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩ࠭ࡴࡦ࡮࠳ࡺࡴ࡫࡯ࡱࡺࡲࠬୃ")
    def _1ll11111l_opy_(self, bstack1l1l111ll_opy_: str) -> str:
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡆࡳࡳࡼࡥࡳࡶࠣࡥࡧࡹ࡯࡭ࡷࡷࡩࠥࡶࡡࡵࡪࠣࡸࡴࠦࡲࡦ࡮ࡤࡸ࡮ࡼࡥࠡࡲࡤࡸ࡭ࠦࡦࡳࡱࡰࠤࡵࡸ࡯࡫ࡧࡦࡸࠥࡸ࡯ࡰࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡍࡥࡻࡧࠧࡴࠢࡈࡺࡪࡴࡴࡅࡣࡷࡥ࠳ࡹࡥࡵࡈ࡬ࡰࡪࡖࡡࡵࡪࡉࡶࡴࡳࡁࡣࡵࡲࡰࡺࡺࡥࡑࡣࡷ࡬࠭࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧୄ")
        if not bstack1l1l111ll_opy_:
            return self._file_path or bstack1l1llll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ୅")
        try:
            cwd = os.getcwd()
            if bstack1l1l111ll_opy_.startswith(cwd):
                return bstack1l1l111ll_opy_[len(cwd):].lstrip(os.sep)
            return bstack1l1l111ll_opy_
        except (OSError, ValueError):
            return bstack1l1l111ll_opy_
    def _1l1lll1ll_opy_(self, bstack1l1lll111_opy_: str) -> bool:
        bstack1l1llll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡦࡰࡧࠤࡹ࡫ࡳࡵࠢࡨࡺࡪࡴࡴࠡࡸ࡬ࡥࠥ࡭ࡒࡑࡅࠣࡸ࡭ࡸ࡯ࡶࡩ࡫ࠤ࡛ࡧ࡮ࡪ࡮࡯ࡥࡕࡿࡴࡩࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩࡧࠢࡆࡐࡎࠦࡩࡴࠢࡵࡹࡳࡴࡩ࡯ࡩ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦࠣࡥࡹࡺࡥ࡮ࡲࡷࡷࠥࡺ࡯ࠡࡷࡶࡩࠥࡺࡨࡦࠢࡖࡈࡐࠦࡃࡍࡋࠪࡷࠥ࡭ࡒࡑࡅࠣࡧࡴࡳ࡭ࡶࡰ࡬ࡧࡦࡺࡩࡰࡰࠣࡴࡦࡺࡨࠋࠢࠣࠤ࡚ࠥࠦࠠࠡࠢࠫࡦࡴࡩ࡭࡮ࡤࡔࡾࡺࡨࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࠳࠾ࠡࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦࠢ࠰ࡂࠥࡨࡩ࡯ࡣࡵࡽࠥ࠳࠾ࠡࡖࡨࡷࡹࡎࡵࡣࠢࡄࡔࡎ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡷࡹ࡫ࡡࡥࠢࡲࡪࠥࡪࡩࡳࡧࡦࡸࠥࡎࡔࡕࡒࠣࡧࡦࡲ࡬ࡴࠢࡹ࡭ࡦࠦࡔࡦࡵࡷࡌࡺࡨࡈࡢࡰࡧࡰࡪࡸ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤ࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ࠠࡰࡴ࡙ࠣࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡖࡵࡹࡪࠦࡩࡧࠢࡨࡺࡪࡴࡴࠡࡹࡤࡷࠥࡹࡥ࡯ࡶࠣࡺ࡮ࡧࠠࡨࡔࡓࡇ࠱ࠦࡆࡢ࡮ࡶࡩࠥ࡯ࡦࠡࡅࡏࡍࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ୆")
        try:
            from browserstack_sdk.sdk_cli.cli import cli as sdk_cli
            if not sdk_cli or not sdk_cli.is_running():
                logger.debug(bstack1l1llll_opy_ (u"ࠥࡘࡪࡹࡴࡄ࡮࡬ࡩࡳࡺ࠺ࠡࡕࡇࡏࠥࡉࡌࡊࠢࡱࡳࡹࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣ࡫ࡗࡖࡃࠣେ"))
                return False
            if not sdk_cli.test_framework:
                sdk_cli.bstack1ll11l111_opy_(bstack1l1llll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬୈ"))
            if not sdk_cli.test_framework:
                logger.debug(bstack1l1llll_opy_ (u"࡚ࠧࡥࡴࡶࡆࡰ࡮࡫࡮ࡵ࠼ࠣࡒࡴࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠥ୉"))
                return False
            from browserstack_sdk.sdk_cli.test_framework import (
                TestFrameworkState,
                TestHookState,
                TestFrameworkContext
            )
            platform_index = int(os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭୊"), bstack1l1llll_opy_ (u"ࠧ࠱ࠩୋ")))
            context = TestFrameworkContext(
                test_framework_name=bstack1l1llll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩୌ"),
                test_framework_version=self._1ll111l11_opy_(),
                platform_index=platform_index
            )
            if bstack1l1lll111_opy_ == bstack1l1llll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦ୍ࠪ"):
                sdk_cli.test_framework.track_event(
                    context,
                    TestFrameworkState.INIT_TEST,
                    TestHookState.PRE,
                    self._1l1l1l1ll_opy_
                )
                sdk_cli.test_framework.track_event(
                    context,
                    TestFrameworkState.TEST,
                    TestHookState.PRE,
                    self._1l1l1l1ll_opy_
                )
            elif bstack1l1lll111_opy_ == bstack1l1llll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ୎"):
                sdk_cli.test_framework.track_event(
                    context,
                    TestFrameworkState.TEST,
                    TestHookState.POST,
                    self._1l1l1l1ll_opy_
                )
            return True
        except ImportError:
            logger.debug(bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡳࡵࡅ࡯࡭ࡪࡴࡴ࠻ࠢࡖࡈࡐࠦࡃࡍࡋࠣࡲࡴࡺࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠥ୏"))
            return False
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"࡚ࠧࡥࡴࡶࡆࡰ࡮࡫࡮ࡵ࠼ࠣࡉࡷࡸ࡯ࡳࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡩࡻ࡫࡮ࡵࠢࡹ࡭ࡦࠦࡧࡓࡒࡆ࠾ࠥࢁࡽࠣ୐").format(e))
            return False
    def _1ll1111l1_opy_(self):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦ࡚ࠢࡩࡧࡊࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡧࡴࡲࡱࠥࡳࡵ࡭ࡶ࡬ࡴࡱ࡫ࠠࡱࡱࡶࡷ࡮ࡨ࡬ࡦࠢ࡯ࡳࡨࡧࡴࡪࡱࡱࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡵࡶࡪࡴࡴࠡࡶ࡫ࡶࡪࡧࡤࠨࡵࠣࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤ࡛ࠥࠦࠠࠡࠢࠣࡪࡨࡄࡳ࡫ࡹࡩࡷࡀࠠࡕࡪࡨࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡ࡫ࡩࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ୑")
        if self._driver:
            return self._driver
        logger.debug(bstack1l1llll_opy_ (u"ࠢࡕࡧࡶࡸࡈࡲࡩࡦࡰࡷ࠾࡙ࠥࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡥࡴ࡬ࡺࡪࡸࠠࡴࡧࡤࡶࡨ࡮࠮࠯࠰ࠥ୒"))
        driver = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ୓"), None)
        if driver:
            self._driver = driver
            logger.info(bstack1l1llll_opy_ (u"ࠤࡗࡩࡸࡺࡃ࡭࡫ࡨࡲࡹࡀࠠࡇࡱࡸࡲࡩࠦࡤࡳ࡫ࡹࡩࡷࠦ࡯࡯ࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡸ࡭ࡸࡥࡢࡦࠥ୔"))
            return driver
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡘࡪࡹࡴࡄ࡮࡬ࡩࡳࡺ࠺ࠡࡐࡲࠤࡩࡸࡩࡷࡧࡵࠤࡴࡴࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶ࡫ࡶࡪࡧࡤࠣ୕"))
        logger.debug(bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡳࡵࡅ࡯࡭ࡪࡴࡴ࠻ࠢࡑࡳࠥࡪࡲࡪࡸࡨࡶࠥࡵ࡮ࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷ࡬ࡷ࡫ࡡࡥࠤୖ"))
        return None
    def _1ll1llll1_opy_(self):
        bstack1l1llll_opy_ (u"ࠧࠨࠢࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡨࡧࡰࡵࡷࡵࡩࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷ࠲ࠧࠨࠢୗ")
        if self._a11y_started:
            return
        self._a11y_started = True
        logger.info(bstack1l1llll_opy_ (u"ࠨࡔࡦࡵࡷࡇࡱ࡯ࡥ࡯ࡶ࠽ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡴࡷࡩࡩࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠻ࠢࡾࢁࠧ୘").format(self._1ll11ll1l_opy_))
    def _1ll111l1l_opy_(self):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡖࡥࡻ࡫ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡣࡷࠤࡹ࡫ࡳࡵࠢࡨࡲࡩ࠴ࠢࠣࠤ୙")
        if self._a11y_stop_done:
            return
        self._a11y_stop_done = True
        driver = self._1ll1111l1_opy_()
        if not driver:
            logger.debug(bstack1l1llll_opy_ (u"ࠣࡖࡨࡷࡹࡉ࡬ࡪࡧࡱࡸ࠿ࠦࡎࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥ࡬࡯ࡳࠢࡶࡥࡻ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠥ୚"))
            return
        try:
            bstack1ll1ll111_opy_ = accessibility_scripts.save_test_results
            if not bstack1ll1ll111_opy_:
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡗࡩࡸࡺࡃ࡭࡫ࡨࡲࡹࡀࠠࡔࡣࡹࡩࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡤࡴ࡬ࡴࡹࠦ࡮ࡰࡶࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠨ୛"))
                return
            bstack1lll11111_opy_ = {
                bstack1l1llll_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪଡ଼"): self._1ll11lll1_opy_ or self._1l1llll11_opy_,
                bstack1l1llll_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩଢ଼"): self._1l11llll1_opy_ or os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ୞"), bstack1l1llll_opy_ (u"࠭ࠧୟ")),
                bstack1l1llll_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫୠ"): os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬୡ"), bstack1l1llll_opy_ (u"ࠩࠪୢ"))
            }
            result = driver.execute_async_script(bstack1ll1ll111_opy_, bstack1lll11111_opy_)
            logger.info(bstack1l1llll_opy_ (u"ࠥࡘࡪࡹࡴࡄ࡮࡬ࡩࡳࡺ࠺ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡥࡻ࡫ࡤ࠻ࠢࡾࢁࠧୣ").format(result))
            logger.info(bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡳࡵࡅ࡯࡭ࡪࡴࡴ࠻ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧ୤"))
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"࡚ࠧࡥࡴࡶࡆࡰ࡮࡫࡮ࡵ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡢࡸࡨࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠿ࠦࡻࡾࠤ୥").format(e))
    def set_test_name(self, name):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡕࡨࡸࠥࡺࡨࡦࠢࡱࡥࡲ࡫ࠠࡰࡨࠣࡸ࡭࡫ࠠࡵࡧࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡳࡧ࡭ࡦࠢࠫࡷࡹࡸࠩ࠻ࠢࡗ࡬ࡪࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠢࠫࡩ࠳࡭࠮࠭ࠢࠥࡥࡩࡪࡐࡳࡱࡧࡹࡨࡺࡔࡰࡅࡤࡶࡹࠨࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗࡩࡸࡺࡃ࡭࡫ࡨࡲࡹࡀࠠࡔࡧ࡯ࡪࠥ࡬࡯ࡳࠢࡰࡩࡹ࡮࡯ࡥࠢࡦ࡬ࡦ࡯࡮ࡪࡰࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ୦")
        self._1ll11ll1l_opy_ = name
        return self
    def set_test_hierarchy(self, bstack1l1ll11l1_opy_):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡖࡩࡹࠦࡴࡩࡧࠣ࡬࡮࡫ࡲࡢࡴࡦ࡬࡮ࡩࡡ࡭ࠢࡶࡧࡴࡶࡥࠡࡱࡩࠤࡹ࡮ࡥࠡࡶࡨࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮ࡩࡦࡴࡤࡶࡨ࡮ࡹࠡࠪ࡯࡭ࡸࡺࠩ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡷࡨࡵࡰࡦࠢ࡯ࡩࡻ࡫࡬ࡴࠢࠫࡩ࠳࡭࠮࠭ࠢ࡞ࠦࡹ࡫ࡳࡵࡵࠥ࠰ࠥࠨࡂࡔࡶࡤࡧࡰࡊࡥ࡮ࡱࡗࡩࡸࡺࠢ࡞ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡫ࡳࡵࡅ࡯࡭ࡪࡴࡴ࠻ࠢࡖࡩࡱ࡬ࠠࡧࡱࡵࠤࡲ࡫ࡴࡩࡱࡧࠤࡨ࡮ࡡࡪࡰ࡬ࡲ࡬ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ୧")
        self._1l1l1l111_opy_ = bstack1l1ll11l1_opy_ if bstack1l1ll11l1_opy_ else []
        return self
    def set_file_path(self, file_path):
        bstack1l1llll_opy_ (u"ࠣࠤࠥࡗࡪࡺࠠࡵࡪࡨࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࠠࡸࡪࡨࡶࡪࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡ࡫ࡶࠤࡱࡵࡣࡢࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠠࠩࡵࡷࡶ࠮ࡀࠠࡓࡧ࡯ࡥࡹ࡯ࡶࡦࠢࡲࡶࠥࡧࡢࡴࡱ࡯ࡹࡹ࡫ࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࠣࠬࡪ࠴ࡧ࠯࠮ࠣࠦࡹ࡫ࡳࡵࡵ࠲ࡺࡦࡴࡩ࡭࡮ࡤࡣࡸࡧ࡭ࡱ࡮ࡨࡣࡹ࡫ࡳࡵ࠰ࡳࡽࠧ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡖࡨࡷࡹࡉ࡬ࡪࡧࡱࡸ࠿ࠦࡓࡦ࡮ࡩࠤ࡫ࡵࡲࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡥ࡫ࡥ࡮ࡴࡩ࡯ࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ୨")
        self._file_path = file_path
        return self
    def start(self):
        bstack1l1llll_opy_ (u"ࠤࠥࠦࡘࡺࡡࡳࡶࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡧ࡮ࡥࠢࡶࡩࡳࡪࠠࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠡࡧࡹࡩࡳࡺࠠࡵࡱࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࠶࠴ࠠࡅࡧࡷࡩࡨࡺࡳࠡࡥࡤࡰࡱ࡫ࡲࠡ࡫ࡱࡪࡴࠦࡩࡧࠢࡷࡩࡸࡺ࡟࡯ࡣࡰࡩ࠴࡬ࡩ࡭ࡧࡢࡴࡦࡺࡨࠡࡰࡲࡸࠥ࡫ࡸࡱ࡮࡬ࡧ࡮ࡺ࡬ࡺࠢࡶࡩࡹࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠳࠰ࠣࡉࡽࡺࡲࡢࡥࡷࡷࠥࡺࡥࡴࡶࠣࡱࡪࡺࡨࡰࡦࠣࡦࡴࡪࡹࠡࡨࡵࡳࡲࠦࡳࡰࡷࡵࡧࡪࠦࡦࡪ࡮ࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠹࠮ࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤ࡙࡫ࡳࡵࡆࡤࡸࡦࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡥࡳࡪࠠࡤࡱࡧࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠴࠯ࠢࡖࡩࡳࡪࡳࠡࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠢࡨࡺࡪࡴࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࠫ࡭࡫ࠦࡥ࡯ࡣࡥࡰࡪࡪࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢ࠸࠲࡙ࠥࡴࡰࡴࡨࡷࠥࡺࡥࡴࡶ࡙࡚ࠣࡏࡄࠡࡱࡱࠤࡨࡻࡲࡳࡧࡱࡸࠥࡺࡨࡳࡧࡤࡨࠥ࡬࡯ࡳࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠸࠱ࠤࡒࡧࡲ࡬ࡵࠣࡸ࡭ࡸࡥࡢࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳࠡࡣࡶࠤࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡏࡸࡷࡹࠦࡢࡦࠢࡦࡥࡱࡲࡥࡥࠢࡥࡩ࡫ࡵࡲࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡮ࡥ࡙ࠡࡨࡦࡉࡸࡩࡷࡧࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ୩")
        if not self._1ll11ll1l_opy_:
            logger.warning(bstack1l1llll_opy_ (u"ࠥࡘࡪࡹࡴࡄ࡮࡬ࡩࡳࡺ࠺ࠡࡵࡷࡥࡷࡺࠨࠪࠢࡦࡥࡱࡲࡥࡥࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠴ࠠࡖࡵࡨࠤࡸ࡫ࡴࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠬ࠮ࠦࡦࡪࡴࡶࡸ࠳ࠨ୪"))
            return
        if not self._1l1l1l111_opy_:
            logger.warning(bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡳࡵࡅ࡯࡭ࡪࡴࡴ࠻ࠢࡶࡸࡦࡸࡴࠩࠫࠣࡧࡦࡲ࡬ࡦࡦࠣࡻ࡮ࡺࡨࡰࡷࡷࠤࡹ࡫ࡳࡵࡡ࡫࡭ࡪࡸࡡࡳࡥ࡫ࡽ࠳ࠦࡕࡴࡧࠣࡷࡪࡺ࡟ࡵࡧࡶࡸࡤ࡮ࡩࡦࡴࡤࡶࡨ࡮ࡹࠩࠫࠣࡸࡴࠦࡳࡦࡶࠣ࡭ࡹ࠴ࠢ୫"))
            return
        if self._started:
            logger.warning(bstack1l1llll_opy_ (u"࡚ࠧࡥࡴࡶࡆࡰ࡮࡫࡮ࡵ࠼ࠣࡷࡹࡧࡲࡵࠪࠬࠤࡦࡲࡲࡦࡣࡧࡽࠥࡩࡡ࡭࡮ࡨࡨࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࠨࡽࢀࠫ࠳ࠦࡉࡨࡰࡲࡶ࡮ࡴࡧࠡࡦࡸࡴࡱ࡯ࡣࡢࡶࡨࠤࡨࡧ࡬࡭࠰ࠥ୬").format(self._1ll11ll1l_opy_))
            return
        self._started = True
        bstack1ll1lll1l_opy_ = self._1lll111l1_opy_()
        if not self._1ll11ll1l_opy_:
            logger.warning(bstack1l1llll_opy_ (u"ࠨࡔࡦࡵࡷࡇࡱ࡯ࡥ࡯ࡶ࠱ࡷࡹࡧࡲࡵࠪࠬࠤࡨࡧ࡬࡭ࡧࡧࠤࡼ࡯ࡴࡩࡱࡸࡸࠥࡺࡥࡴࡶࡢࡲࡦࡳࡥ࠯ࠢࡘࡷࡪࠦࡳࡦࡶࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠮ࠩࠡࡨ࡬ࡶࡸࡺ࠮ࠣ୭"))
            return
        bstack1ll1l111l_opy_ = self._1l1l1l111_opy_
        self._1l1l1llll_opy_ = bstack1l1111ll_opy_()
        bstack1l1l1111l_opy_ = None
        if self._file_path:
            bstack1ll1lll11_opy_ = bstack1ll1lll1l_opy_.function_name
            bstack1l1l1111l_opy_ = self._1ll1l1l11_opy_(
                self._file_path,
                bstack1ll1lll11_opy_,
                bstack1ll1lll1l_opy_.class_name
            )
            if bstack1l1l1111l_opy_:
                logger.debug(bstack1l1llll_opy_ (u"ࠢࡕࡧࡶࡸࡈࡲࡩࡦࡰࡷ࠾ࠥࡋࡸࡵࡴࡤࡧࡹ࡫ࡤࠡࡽࢀࠤࡨ࡮ࡡࡳࡵࠣࡳ࡫ࠦࡴࡦࡵࡷࠤࡨࡵࡤࡦࠤ୮").format(len(bstack1l1l1111l_opy_)))
        bstack1ll1l1ll1_opy_ = {
            bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ୯"): bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ୰"),
            bstack1l1llll_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࡢ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࠨୱ"): True,
            bstack1l1llll_opy_ (u"ࠫࡦ࡭ࡥ࡯ࡶࡢࡺࡪࡸࡳࡪࡱࡱࠫ୲"): self._1ll111l11_opy_(),
            bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡸࡾࡶࡥࠨ୳"): bstack1l1llll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡢ࡮ࠪ୴")
        }
        if bstack1ll1lll1l_opy_.line_number:
            bstack1ll1l1ll1_opy_[bstack1l1llll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫࡟࡭࡫ࡱࡩࠬ୵")] = bstack1ll1lll1l_opy_.line_number
        self._1l1l1l1ll_opy_ = bstack1l1l1111_opy_(
            name=self._1ll11ll1l_opy_,
            code=bstack1l1l1111l_opy_,
            file_path=self._file_path or bstack1l1llll_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ୶"),
            started_at=self._1l1l1llll_opy_,
            framework=bstack1l1llll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ୷"),
            scope=bstack1ll1l111l_opy_,
            tags=[],
            integrations={},
            meta=bstack1ll1l1ll1_opy_
        )
        self._1l1llll11_opy_ = self._1l1l1l1ll_opy_.uuid
        threading.current_thread().current_test_uuid = self._1l1l1l1ll_opy_.uuid
        threading.current_thread().bstackTestMeta = {bstack1l1llll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ୸"): bstack1l1llll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ୹")}
        logger.debug(bstack1l1llll_opy_ (u"࡚ࠧࡥࡴࡶࡆࡰ࡮࡫࡮ࡵ࠼ࠣࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࠫࢀࢃࠧࠡࠪࡘ࡙ࡎࡊ࠺ࠡࡽࢀ࠭ࠧ୺").format(self._1ll11ll1l_opy_, self._1l1llll11_opy_))
        if self._1l1lll1ll_opy_(bstack1l1llll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ୻")):
            logger.debug(bstack1l1llll_opy_ (u"ࠢࡕࡧࡶࡸࡈࡲࡩࡦࡰࡷ࠾࡙ࠥࡥ࡯ࡶࠣࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠤࡪࡼࡥ࡯ࡶࠣࡺ࡮ࡧࠠࡨࡔࡓࡇࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࠨࡽࢀࠫࠧ୼").format(self._1ll11ll1l_opy_))
        else:
            try:
                TestHubHandler.bstack11lll1ll_opy_(bstack1l1llll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ୽"), self._1l1l1l1ll_opy_)
                logger.debug(bstack1l1llll_opy_ (u"ࠤࡗࡩࡸࡺࡃ࡭࡫ࡨࡲࡹࡀࠠࡔࡧࡱࡸ࡚ࠥࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩࠦࡥࡷࡧࡱࡸࠥࡼࡩࡢࠢࡋࡘ࡙ࡖࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢࠪࡿࢂ࠭ࠢ୾").format(self._1ll11ll1l_opy_))
            except Exception as e:
                logger.error(bstack1l1llll_opy_ (u"ࠥࡘࡪࡹࡴࡄ࡮࡬ࡩࡳࡺ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠣࡩࡻ࡫࡮ࡵ࠼ࠣࡿࢂࠨ୿").format(e))
        try:
            from browserstack_sdk.sdk_cli.cli import cli as sdk_cli
            if sdk_cli and hasattr(sdk_cli, bstack1l1llll_opy_ (u"ࠫࡨࡵ࡮ࡧ࡫ࡪࠫ஀")) and sdk_cli.config:
                self._1l1l11lll_opy_ = sdk_cli.config
                bstack1ll1ll11l_opy_ = self._1l1l11lll_opy_.get(bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ஁"), False) if self._1l1l11lll_opy_ else False
                logger.info(bstack1l1llll_opy_ (u"ࠨࡔࡦࡵࡷࡇࡱ࡯ࡥ࡯ࡶ࠽ࠤࡘࡺ࡯ࡳࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡨࡵࡳࡲࠦࡓࡅࡍࠣࡇࡑࡏࠠࠩࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠾ࡽࢀ࠭ࠧஂ").format(bstack1ll1ll11l_opy_))
        except Exception as e:
            logger.info(bstack1l1llll_opy_ (u"ࠢࡕࡧࡶࡸࡈࡲࡩࡦࡰࡷ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡩࡨࡸࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠼ࠣࡿࢂࠨஃ").format(e))
            self._1l1l11lll_opy_ = {}
        try:
            platform_index = int(os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ஄"), bstack1l1llll_opy_ (u"ࠩ࠳ࠫஅ")))
            bstack1ll1lllll_opy_ = a11y.is_enabled_platform(self._1l1l11lll_opy_, platform_index) if self._1l1l11lll_opy_ else False
            if bstack1ll1lllll_opy_ and a11y.on():
                bstack1ll11ll1_opy_ = self._1l1l11lll_opy_.get(bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ஆ"), []) if self._1l1l11lll_opy_ else []
                _1ll111111_opy_ = max(0, platform_index)
                bstack1ll11l1ll_opy_ = bstack1ll11ll1_opy_[_1ll111111_opy_] if _1ll111111_opy_ < len(bstack1ll11ll1_opy_) else {}
                bstack1l1ll1l11_opy_ = (bstack1ll11l1ll_opy_.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩஇ"), bstack1l1llll_opy_ (u"ࠬ࠭ஈ")) or bstack1l1llll_opy_ (u"࠭ࠧஉ")).lower()
                bstack1l1l1lll1_opy_ = str(bstack1ll11l1ll_opy_.get(bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨஊ"), bstack1l1llll_opy_ (u"ࠨࠩ஋")) or bstack1ll11l1ll_opy_.get(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ஌"), bstack1l1llll_opy_ (u"ࠪࠫ஍")) or bstack1l1llll_opy_ (u"ࠫࠬஎ"))
                bstack1l1l11l11_opy_ = (
                    bstack1ll11l1ll_opy_.get(bstack1l1llll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪஏ"))
                    or bstack1ll11l1ll_opy_.get(bstack1l1llll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ஐ"))
                    or {}
                )
                bstack1l1ll1lll_opy_ = bstack1l1l11l11_opy_.get(bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࡷࠬ஑"), []) if isinstance(bstack1l1l11l11_opy_, dict) else []
                bstack1l1l1l1l1_opy_ = any(
                    arg == bstack1l1llll_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬஒ") or (arg.startswith(bstack1l1llll_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸࡃࠧஓ")) and arg != bstack1l1llll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽࡯ࡧࡺࠫஔ"))
                    for arg in bstack1l1ll1lll_opy_
                )
                bstack1l1l1l11l_opy_ = True
                if bstack1l1l1l1l1_opy_:
                    logger.info(bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡳࡵࡅ࡯࡭ࡪࡴࡴ࠻ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠤ࠲ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡷࡶࡩࡸࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦࠨࡥࡧࡷࡩࡨࡺࡥࡥࠢࡩࡶࡴࡳࠠࡤࡱࡱࡪ࡮࡭ࠠࡤࡣࡳࡷ࠮ࠨக"))
                    bstack1l1l1l11l_opy_ = False
                elif bstack1l1ll1l11_opy_ and bstack1l1ll1l11_opy_ not in (bstack1l1llll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ஖"), bstack1l1llll_opy_ (u"࠭ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠨ஗")):
                    logger.info(bstack1l1llll_opy_ (u"ࠢࡕࡧࡶࡸࡈࡲࡩࡦࡰࡷ࠾ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡪࡩࡴࡣࡥࡰࡪࡪࠠ࠮ࠢࡥࡶࡴࡽࡳࡦࡴࠣࠫࢀࢃࠧࠡ࡫ࡶࠤࡳࡵࡴࠡࡅ࡫ࡶࡴࡳࡥ࠰ࡅ࡫ࡶࡴࡳࡩࡶ࡯ࠥ஘").format(bstack1l1ll1l11_opy_))
                    bstack1l1l1l11l_opy_ = False
                elif bstack1l1l1lll1_opy_ and bstack1l1l1lll1_opy_ != bstack1l1llll_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨங"):
                    try:
                        if int(bstack1l1l1lll1_opy_.split(bstack1l1llll_opy_ (u"ࠩ࠱ࠫச"))[0]) <= MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION:
                            logger.info(bstack1l1llll_opy_ (u"ࠥࡘࡪࡹࡴࡄ࡮࡬ࡩࡳࡺ࠺ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠣ࠱ࠥࡉࡨࡳࡱࡰࡩࠥࢁࡽࠡ࡫ࡶࠤࡧ࡫࡬ࡰࡹࠣࡱ࡮ࡴࡩ࡮ࡷࡰࠤࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡽࢀࠦ஛").format(
                                bstack1l1l1lll1_opy_, MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION))
                            bstack1l1l1l11l_opy_ = False
                    except (ValueError, IndexError):
                        pass
                if bstack1l1l1l11l_opy_:
                    if self._1l1l11lll_opy_.get(bstack1l1llll_opy_ (u"ࠫࡦࡶࡰࠨஜ")):
                        threading.current_thread().isAppA11yTest = True
                        logger.info(bstack1l1llll_opy_ (u"࡚ࠧࡥࡴࡶࡆࡰ࡮࡫࡮ࡵ࠼ࠣࡗࡪࡺࠠࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺ࠽ࡕࡴࡸࡩࠥࡵ࡮ࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷ࡬ࡷ࡫ࡡࡥࠢࠫࡥࡵࡶࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡩ࡫ࡴࡦࡥࡷࡩࡩ࠯ࠢ஝"))
                    else:
                        threading.current_thread().isA11yTest = True
                        logger.info(bstack1l1llll_opy_ (u"ࠨࡔࡦࡵࡷࡇࡱ࡯ࡥ࡯ࡶ࠽ࠤࡘ࡫ࡴࠡ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࡂ࡚ࡲࡶࡧࠣࡳࡳࠦࡣࡶࡴࡵࡩࡳࡺࠠࡵࡪࡵࡩࡦࡪࠠࡧࡱࡵࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡥࡤࡲࡳ࡯࡮ࡨࠤஞ"))
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠢࡕࡧࡶࡸࡈࡲࡩࡦࡰࡷ࠾ࠥࡋࡲࡳࡱࡵࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠢࡩࡰࡦ࡭࠺ࠡࡽࢀࠦட").format(e))
    def _1ll1ll1l1_opy_(self):
        bstack1l1llll_opy_ (u"ࠣࠤࠥࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡪࡨࠣࡩࡳࡧࡢ࡭ࡧࡧࠤࡦࡴࡤࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡸࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡧ࡬࡭ࡧࡧࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡩࡡ࡭࡮ࡼࠤࡼ࡮ࡥ࡯ࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡨࡷࡺࡲࡴࠡࠪࡺ࡬ࡪࡴࠠࡥࡴ࡬ࡺࡪࡸࠠࡪࡵࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ஠")
        if self._1l1ll1l1l_opy_ or self._a11y_started:
            logger.info(bstack1l1llll_opy_ (u"ࠤࡗࡩࡸࡺࡃ࡭࡫ࡨࡲࡹࡀࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡩࠦࠨࡦࡰࡤࡦࡱ࡫ࡤ࠾ࡽࢀ࠰ࠥࡹࡴࡢࡴࡷࡩࡩࡃࡻࡾࠫࠥ஡").format(
                self._1l1ll1l1l_opy_, self._a11y_started))
            return
        if not self._1l1l11lll_opy_:
            logger.info(bstack1l1llll_opy_ (u"ࠥࡘࡪࡹࡴࡄ࡮࡬ࡩࡳࡺ࠺ࠡࡐࡲࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡨ࡮ࡥࡤ࡭ࠥ஢"))
            return
        try:
            platform_index = int(os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫண"), bstack1l1llll_opy_ (u"ࠬ࠶ࠧத")))
            bstack1ll111lll_opy_ = a11y.is_enabled_platform(self._1l1l11lll_opy_, platform_index)
            if not bstack1ll111lll_opy_:
                logger.info(bstack1l1llll_opy_ (u"ࠨࡔࡦࡵࡷࡇࡱ࡯ࡥ࡯ࡶ࠽ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࠨࡪࡵࡢࡩࡳࡧࡢ࡭ࡧࡧࡣࡵࡲࡡࡵࡨࡲࡶࡲࠦࡲࡦࡶࡸࡶࡳ࡫ࡤࠡࡈࡤࡰࡸ࡫ࠩࠣ஥"))
                return
            driver = self._1ll1111l1_opy_()
            if not driver:
                logger.info(bstack1l1llll_opy_ (u"ࠢࡕࡧࡶࡸࡈࡲࡩࡦࡰࡷ࠾ࠥࡔ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡩࡨࡦࡥ࡮ࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡶࡲࡳࡳࡷࡺࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦ஦"))
                return
            try:
                caps = getattr(driver, bstack1l1llll_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ஧"), {}) or {}
                browser_name = caps.get(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧந"), bstack1l1llll_opy_ (u"ࠪࠫன")).lower()
                logger.info(bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡳࡵࡅ࡯࡭ࡪࡴࡴ࠻ࠢࡆ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥ࠳ࠠࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩ࠿ࠦࡻࡾࠤப").format(browser_name))
                if browser_name == bstack1l1llll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩ࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠭ࡴࡪࡨࡰࡱ࠭஫"):
                    logger.info(bstack1l1llll_opy_ (u"ࠨࡔࡦࡵࡷࡇࡱ࡯ࡥ࡯ࡶ࠽ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࠬࡨ࡮ࡲࡰ࡯ࡨ࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠳ࡳࡩࡧ࡯ࡰ࠮࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤ஬"))
                    return
                if browser_name and browser_name not in (bstack1l1llll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ஭"), bstack1l1llll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡩࡶ࡯ࠪம"), bstack1l1llll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦ࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶ࠱ࡸ࡮ࡥ࡭࡮ࠪய")):
                    logger.info(bstack1l1llll_opy_ (u"ࠥࡘࡪࡹࡴࡄ࡮࡬ࡩࡳࡺ࠺ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࠣࠬ࡬ࡵࡴࠡࠩࡾࢁࠬ࠯ࠢர").format(browser_name))
                    return
                browser_version = str(caps.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬற"), bstack1l1llll_opy_ (u"ࠬ࠭ல")) or caps.get(bstack1l1llll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧள"), bstack1l1llll_opy_ (u"ࠧࠨழ")) or bstack1l1llll_opy_ (u"ࠨࠩவ"))
                if browser_version and browser_version != bstack1l1llll_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩஶ"):
                    try:
                        if int(browser_version.split(bstack1l1llll_opy_ (u"ࠪ࠲ࠬஷ"))[0]) <= MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION:
                            logger.info(bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡳࡵࡅ࡯࡭ࡪࡴࡴ࠻ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࡿࢂࠦࠨࡨࡱࡷࠤࢀࢃࠩࠣஸ").format(
                                MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION, browser_version))
                            return
                    except (ValueError, IndexError):
                        pass
            except Exception as e:
                logger.warning(bstack1l1llll_opy_ (u"࡚ࠧࡥࡴࡶࡆࡰ࡮࡫࡮ࡵ࠼ࠣࡉࡷࡸ࡯ࡳࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡹࡵࡱࡲࡲࡶࡹ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠼ࠣࡿࢂࠨஹ").format(e))
                return
            self._1l1ll1l1l_opy_ = True
            self._1ll11lll1_opy_ = self._1l1llll11_opy_
            self._1l11llll1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ஺"), bstack1l1llll_opy_ (u"ࠧࠨ஻"))
            self._1ll1llll1_opy_()
            driver = self._1ll1111l1_opy_()
            if driver:
                a11y.start_test_capture(driver, True)
                logger.info(bstack1l1llll_opy_ (u"ࠣࡖࡨࡷࡹࡉ࡬ࡪࡧࡱࡸ࠿ࠦࡃࡢ࡮࡯ࡩࡩࠦࡳࡵࡣࡵࡸࡤࡺࡥࡴࡶࡢࡧࡦࡶࡴࡶࡴࡨࠤࡹࡵࠠࡦࡰࡤࡦࡱ࡫ࠠࡢࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫ࠥࡵ࡮ࠡࡦࡵ࡭ࡻ࡫ࡲࠣ஼"))
            logger.info(bstack1l1llll_opy_ (u"ࠤࡗࡩࡸࡺࡃ࡭࡫ࡨࡲࡹࡀࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡦࡰࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࠫࢀࢃࠧࠣ஽").format(self._1ll11ll1l_opy_))
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠥࡘࡪࡹࡴࡄ࡮࡬ࡩࡳࡺ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡀࠠࡼࡿࠥா").format(e))
            import traceback
            logger.error(bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡳࡵࡅ࡯࡭ࡪࡴࡴ࠻ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢ࡬ࡲ࡮ࡺࠠࡵࡴࡤࡧࡪࡨࡡࡤ࡭࠽ࠤࢀࢃࠢி").format(traceback.format_exc()))
    def _1ll1l11l1_opy_(self):
        bstack1l1llll_opy_ (u"ࠧࠨࠢࡎࡣࡵ࡯ࠥࡺࡨࡦࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡱࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡶࡩࡹࠦࡴࡰࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࡩࠦࡶࡪࡣࠣࡷࡪࡺ࡟ࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠫ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡶࡴࡪࡩࡴࡴࠢࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤீ")
        global_config = Config.bstack1lll1l11_opy_()
        if global_config.bstack11lll1l1_opy_():
            logger.debug(bstack1l1llll_opy_ (u"ࠨࡔࡦࡵࡷࡇࡱ࡯ࡥ࡯ࡶ࠽ࠤࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࠨࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩ࠯ࠢு"))
            return
        driver = self._1ll1111l1_opy_()
        if not driver or not self._1ll11ll1l_opy_:
            return
        try:
            bstack1l1lll11l_opy_ = bstack1lll111ll_opy_(bstack1l1llll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨூ"), self._1ll11ll1l_opy_, bstack1l1llll_opy_ (u"ࠨࠩ௃"), bstack1l1llll_opy_ (u"ࠩࠪ௄"), bstack1l1llll_opy_ (u"ࠪࠫ௅"), bstack1l1llll_opy_ (u"ࠫࠬெ"))
            driver.execute_script(bstack1l1lll11l_opy_)
            logger.debug(bstack1l1llll_opy_ (u"࡚ࠧࡥࡴࡶࡆࡰ࡮࡫࡮ࡵ࠼ࠣࡗࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡴࡰࠢࠪࡿࢂ࠭ࠢே").format(self._1ll11ll1l_opy_))
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠨࡔࡦࡵࡷࡇࡱ࡯ࡥ࡯ࡶ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀࢃࠢை").format(e))
    def _1ll11l11l_opy_(self, status, reason=bstack1l1llll_opy_ (u"ࠧࠨ௉")):
        bstack1l1llll_opy_ (u"ࠣࠤࠥࡑࡦࡸ࡫ࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡶࡪࡹࡵ࡭ࡶࠣࡥࡳࡪࠠࡴࡧࡱࡨࠥ࡫ࡶࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡸࡺࡡࡵࡷࡶࠤ࠭ࡹࡴࡳࠫ࠽ࠤࠬࡶࡡࡴࡵࡨࡨࠬࠦ࡯ࡳࠢࠪࡪࡦ࡯࡬ࡦࡦࠪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡦࡹ࡯࡯ࠢࠫࡷࡹࡸࠩ࠻ࠢࡉࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠲ࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࠨࡧࡱࡵࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣொ")
        if self._1l1ll11ll_opy_:
            logger.warning(bstack1l1llll_opy_ (u"ࠤࡗࡩࡸࡺࡃ࡭࡫ࡨࡲࡹࡀࠠࡓࡧࡶࡹࡱࡺࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࠫࢀࢃࠧ࠯ࠢࡖ࡯࡮ࡶࡰࡪࡰࡪ࠲ࠧோ").format(self._1ll11ll1l_opy_))
            return
        self._1l1ll11ll_opy_ = True
        self._1ll1ll1l1_opy_()
        if self._1l1ll1l1l_opy_:
            self._1ll111l1l_opy_()
        self._1ll1l11l1_opy_()
        if status == bstack1l1llll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪௌ"):
            result = Result.passed()
        else:
            result = Result.failed(exception=reason)
        bstack1ll1ll1ll_opy_ = bstack1l1111ll_opy_()
        duration = bstack1ll1l11ll_opy_(self._1l1l1llll_opy_, bstack1ll1ll1ll_opy_) if self._1l1l1llll_opy_ else 0
        if self._1l1l1l1ll_opy_:
            bstack1l11lll1l_opy_ = self._1lll1111l_opy_()
            if self._1l1l1l1ll_opy_.meta:
                self._1l1l1l1ll_opy_.meta.update(bstack1l11lll1l_opy_)
            else:
                self._1l1l1l1ll_opy_.meta = bstack1l11lll1l_opy_
            integrations = self._1l1ll111l_opy_()
            if integrations:
                self._1l1l1l1ll_opy_.integrations = integrations
                logger.debug(bstack1l1llll_opy_ (u"࡙ࠦ࡫ࡳࡵࡅ࡯࡭ࡪࡴࡴ࠻ࠢࡘࡴࡩࡧࡴࡦࡦࠣ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠢࡺ࡭ࡹ࡮ࠠࡱࡴࡲࡺ࡮ࡪࡥࡳ࠼ࠣࡿࢂࠨ்").format(list(integrations.keys())))
            self._1l1l1l1ll_opy_.stop(time=bstack1ll1ll1ll_opy_, duration=duration, result=result)
            if self._1l1lll1ll_opy_(bstack1l1llll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ௎")):
                logger.debug(bstack1l1llll_opy_ (u"ࠨࡔࡦࡵࡷࡇࡱ࡯ࡥ࡯ࡶ࠽ࠤࡘ࡫࡮ࡵࠢࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠤࡪࡼࡥ࡯ࡶࠣࡺ࡮ࡧࠠࡨࡔࡓࡇࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࠨࡽࢀࠫࠥࡽࡩࡵࡪࠣࡶࡪࡹࡵ࡭ࡶࠣࠫࢀࢃࠧࠣ௏").format(self._1ll11ll1l_opy_, status))
            else:
                try:
                    TestHubHandler.bstack11lll1ll_opy_(bstack1l1llll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩௐ"), self._1l1l1l1ll_opy_)
                    logger.debug(bstack1l1llll_opy_ (u"ࠣࡖࡨࡷࡹࡉ࡬ࡪࡧࡱࡸ࠿ࠦࡓࡦࡰࡷࠤ࡙࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩࠦࡥࡷࡧࡱࡸࠥࡼࡩࡢࠢࡋࡘ࡙ࡖࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢࠪࡿࢂ࠭ࠠࡸ࡫ࡷ࡬ࠥࡸࡥࡴࡷ࡯ࡸࠥ࠭ࡻࡾࠩࠥ௑").format(self._1ll11ll1l_opy_, status))
                except Exception as e:
                    logger.error(bstack1l1llll_opy_ (u"ࠤࡗࡩࡸࡺࡃ࡭࡫ࡨࡲࡹࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠣࡩࡻ࡫࡮ࡵ࠼ࠣࡿࢂࠨ௒").format(e))
        global_config = Config.bstack1lll1l11_opy_()
        if global_config.bstack11l11l1l_opy_():
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡘࡪࡹࡴࡄ࡮࡬ࡩࡳࡺ࠺ࠡࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥ࠮ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠣ࡭ࡸࠦࡥ࡯ࡣࡥࡰࡪࡪࠩࠣ௓"))
        else:
            driver = self._1ll1111l1_opy_()
            if driver:
                try:
                    bstack1l1lll11l_opy_ = bstack1lll111ll_opy_(bstack1l1llll_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧ௔"), bstack1l1llll_opy_ (u"ࠬ࠭௕"), status, reason, bstack1l1llll_opy_ (u"࠭ࠧ௖"), bstack1l1llll_opy_ (u"ࠧࠨௗ"))
                    driver.execute_script(bstack1l1lll11l_opy_)
                    logger.debug(bstack1l1llll_opy_ (u"ࠣࡖࡨࡷࡹࡉ࡬ࡪࡧࡱࡸ࠿ࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡳࡡࡳ࡭ࡨࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡡࡴࠢࠪࡿࢂ࠭ࠢ௘").format(status))
                except Exception as e:
                    logger.error(bstack1l1llll_opy_ (u"ࠤࡗࡩࡸࡺࡃ࡭࡫ࡨࡲࡹࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂࠨ௙").format(e))
            else:
                logger.debug(bstack1l1llll_opy_ (u"ࠥࡘࡪࡹࡴࡄ࡮࡬ࡩࡳࡺ࠺ࠡࡐࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠥ௚"))
        threading.current_thread().bstackTestMeta = {bstack1l1llll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ௛"): status}
    def mark_passed(self):
        bstack1l1llll_opy_ (u"ࠧࠨࠢࡎࡣࡵ࡯ࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡢࡵࠣࡴࡦࡹࡳࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠷࠮ࠡࡕࡨࡸࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࡺ࡯ࠡࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠤࡴࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡶࡶࡲࡱࡦࡺࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢ࠵࠲࡙ࠥࡥ࡯ࡦࡶࠤ࡙࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩࠦࡥࡷࡧࡱࡸࠥࡽࡩࡵࡪࠣࠫࡵࡧࡳࡴࡧࡧࠫࠥࡹࡴࡢࡶࡸࡷࠥࡺ࡯ࠡࡖࡨࡷࡹࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠐࠠࠡࠢࠣࠤࠥࠦࠠ࠴࠰ࠣࡑࡦࡸ࡫ࡴࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡥࡸࠦࠧࡱࡣࡶࡷࡪࡪࠧࠡࡱࡱࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡩࡱࡸࡰࡩࠦࡢࡦࠢࡦࡥࡱࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡶࡨࡷࡹࠦࡡࡴࡵࡨࡶࡹ࡯࡯࡯ࡵࠣࡴࡦࡹࡳ࠭ࠢࡥࡩ࡫ࡵࡲࡦࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡴࡹ࡮ࡺࠨࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ௜")
        self._1ll11l11l_opy_(bstack1l1llll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭௝"))
    def mark_failed(self, exception=None):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡐࡥࡷࡱࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡤࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࠩࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠭࠿ࠦࡔࡩࡧࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡴࡩࡣࡷࠤࡨࡧࡵࡴࡧࡧࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡴࡰࠢࡩࡥ࡮ࡲࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡ࠳࠱ࠤࡘ࡫ࡴࡴࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡶࡲࠤࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠸࠮ࠡࡕࡨࡲࡩࡹࠠࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠢࡨࡺࡪࡴࡴࠡࡹ࡬ࡸ࡭ࠦࠧࡧࡣ࡬ࡰࡪࡪࠧࠡࡵࡷࡥࡹࡻࡳࠡࡶࡲࠤ࡙࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠌࠣࠤࠥࠦࠠࠡࠢࠣ࠷࠳ࠦࡍࡢࡴ࡮ࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡡࡴࠢࠪࡪࡦ࡯࡬ࡦࡦࠪࠤࡴࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡶࡶࡲࡱࡦࡺࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢ࠷࠲ࠥࡏ࡮ࡤ࡮ࡸࡨࡪࡹࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠲ࡸࡷࡧࡣࡦࡤࡤࡧࡰࠦࡩ࡯ࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡮࡯ࡶ࡮ࡧࠤࡧ࡫ࠠࡤࡣ࡯ࡰࡪࡪࠠࡪࡰࠣࡸ࡭࡫ࠠࡦࡺࡦࡩࡵࡺࠠࡣ࡮ࡲࡧࡰࠦࡷࡩࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡳ࠭ࠢࡥࡩ࡫ࡵࡲࡦࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡴࡹ࡮ࡺࠨࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ௞")
        reason = bstack1l1llll_opy_ (u"ࠨࠩ௟")
        if exception:
            if isinstance(exception, str):
                reason = exception
            else:
                try:
                    import sys
                    if sys.version_info >= (3, 10):
                        reason = bstack1l1llll_opy_ (u"ࠩࠪ௠").join(traceback.format_exception(exception))
                    else:
                        reason = bstack1l1llll_opy_ (u"ࠪࠫ௡").join(traceback.format_exception(type(exception), exception, exception.__traceback__))
                except (TypeError, AttributeError):
                    reason = str(exception)
        self._1ll11l11l_opy_(bstack1l1llll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ௢"), reason)