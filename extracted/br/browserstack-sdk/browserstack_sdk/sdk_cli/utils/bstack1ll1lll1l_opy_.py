# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import os
import json
import shutil
import tempfile
import threading
import urllib.request
import uuid
from pathlib import Path
import logging
import re
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.helper import bstack11ll1ll11ll_opy_
bstack111l11111ll_opy_ = 100 * 1024 * 1024 # 100 bstack111l1111l1l_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack11ll1llll1l_opy_ = bstack11ll1ll11ll_opy_()
bstack11ll1l1llll_opy_ = bstack11ll11_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᯥ")
bstack111ll11l1ll_opy_ = bstack11ll11_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰ᯦ࠧ")
bstack111ll11l11l_opy_ = bstack11ll11_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᯧ")
bstack111ll11l111_opy_ = bstack11ll11_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᯨ")
bstack111l111l11l_opy_ = bstack11ll11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᯩ")
_111l1111lll_opy_ = threading.local()
def bstack11l111l1l11_opy_(test_framework_state, test_hook_state):
    bstack11ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡦࡶࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶࡨࡷࡹࠦࡥࡷࡧࡱࡸࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡵࡪࡵࡩࡦࡪ࠭࡭ࡱࡦࡥࡱࠦࡳࡵࡱࡵࡥ࡬࡫࠮ࠋࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡹࡨࡰࡷ࡯ࡨࠥࡨࡥࠡࡥࡤࡰࡱ࡫ࡤࠡࡤࡼࠤࡹ࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡩࡣࡱࡨࡱ࡫ࡲࠡࠪࡶࡹࡨ࡮ࠠࡢࡵࠣࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴࠪࠌࠣࠤࠥࠦࡢࡦࡨࡲࡶࡪࠦࡡ࡯ࡻࠣࡪ࡮ࡲࡥࠡࡷࡳࡰࡴࡧࡤࡴࠢࡲࡧࡨࡻࡲ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᯪ")
    _111l1111lll_opy_.test_framework_state = test_framework_state
    _111l1111lll_opy_.test_hook_state = test_hook_state
def bstack111l11l1111_opy_():
    bstack11ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡓࡧࡷࡶ࡮࡫ࡶࡦࠢࡷ࡬ࡪࠦࡣࡶࡴࡵࡩࡳࡺࠠࡵࡧࡶࡸࠥ࡫ࡶࡦࡰࡷࠤࡸࡺࡡࡵࡧࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡶࡪࡧࡤ࠮࡮ࡲࡧࡦࡲࠠࡴࡶࡲࡶࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡢࠢࡷࡹࡵࡲࡥࠡࠪࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠮ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩ࠮ࠦ࡯ࡳࠢࠫࡒࡴࡴࡥ࠭ࠢࡑࡳࡳ࡫ࠩࠡ࡫ࡩࠤࡳࡵࡴࠡࡵࡨࡸ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᯫ")
    return (
        getattr(_111l1111lll_opy_, bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࠨᯬ"), None),
        getattr(_111l1111lll_opy_, bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࠫᯭ"), None)
    )
class bstack1ll111l1l1_opy_:
    bstack11ll11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡊ࡮ࡲࡥࡖࡲ࡯ࡳࡦࡪࡥࡳࠢࡳࡶࡴࡼࡩࡥࡧࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡧ࡬ࡪࡶࡼࠤࡹࡵࠠࡶࡲ࡯ࡳࡦࡪࠠࡢࡰࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡣࡣࡶࡩࡩࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࡉࡵࠢࡶࡹࡵࡶ࡯ࡳࡶࡶࠤࡧࡵࡴࡩࠢ࡯ࡳࡨࡧ࡬ࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࡷࠥࡧ࡮ࡥࠢࡋࡘ࡙ࡖ࠯ࡉࡖࡗࡔࡘࠦࡕࡓࡎࡶ࠰ࠥࡧ࡮ࡥࠢࡦࡳࡵ࡯ࡥࡴࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨࠤ࡮ࡴࡴࡰࠢࡤࠤࡩ࡫ࡳࡪࡩࡱࡥࡹ࡫ࡤࠋࠢࠣࠤࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡹ࡬ࡸ࡭࡯࡮ࠡࡶ࡫ࡩࠥࡻࡳࡦࡴࠪࡷࠥ࡮࡯࡮ࡧࠣࡪࡴࡲࡤࡦࡴࠣࡹࡳࡪࡥࡳࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࡋࡩࠤࡦࡴࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡰࡢࡴࡤࡱࡪࡺࡥࡳࠢࠫ࡭ࡳࠦࡊࡔࡑࡑࠤ࡫ࡵࡲ࡮ࡣࡷ࠭ࠥ࡯ࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡥࡳࡪࠠࡤࡱࡱࡸࡦ࡯࡮ࡴࠢࡤࠤࡹࡸࡵࡵࡪࡼࠤࡻࡧ࡬ࡶࡧࠍࠤࠥࠦࠠࡧࡱࡵࠤࡹ࡮ࡥࠡ࡭ࡨࡽࠥࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣ࠮ࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡰ࡭ࡣࡦࡩࡩࠦࡩ࡯ࠢࡷ࡬ࡪࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥ࡬࡯࡭ࡦࡨࡶࡀࠦ࡯ࡵࡪࡨࡶࡼ࡯ࡳࡦ࠮ࠍࠤࠥࠦࠠࡪࡶࠣࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧ࠴ࠊࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡹࡩࡷࡹࡩࡰࡰࠣࡳ࡫ࠦࡡࡥࡦࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡪࡵࠣࡥࠥࡼ࡯ࡪࡦࠣࡱࡪࡺࡨࡰࡦ⠗࡭ࡹࠦࡨࡢࡰࡧࡰࡪࡹࠠࡢ࡮࡯ࠤࡪࡸࡲࡰࡴࡶࠤ࡬ࡸࡡࡤࡧࡩࡹࡱࡲࡹࠡࡤࡼࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠏࠦࠠࠡࠢࡷ࡬ࡪࡳࠠࡢࡰࡧࠤࡸ࡯࡭ࡱ࡮ࡼࠤࡷ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡶ࡫ࡶࡴࡽࡩ࡯ࡩࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡹ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᯮ")
    @staticmethod
    def upload_attachment(bstack111l111ll1l_opy_: str, *bstack111l111ll11_opy_) -> None:
        if not bstack111l111ll1l_opy_ or not bstack111l111ll1l_opy_.strip():
            logger.error(bstack11ll11_opy_ (u"ࠦࡦࡪࡤࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡐࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࠤ࡮ࡹࠠࡦ࡯ࡳࡸࡾࠦ࡯ࡳࠢࡑࡳࡳ࡫࠮ࠣᯯ"))
            return
        bstack111l111l1ll_opy_ = bstack111l111ll11_opy_[0] if bstack111l111ll11_opy_ and len(bstack111l111ll11_opy_) > 0 else None
        bstack1lll111ll11_opy_ = None
        test_framework_state, test_hook_state = bstack111l11l1111_opy_()
        try:
            if bstack111l111ll1l_opy_.startswith(bstack11ll11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᯰ")) or bstack111l111ll1l_opy_.startswith(bstack11ll11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᯱ")):
                logger.debug(bstack11ll11_opy_ (u"ࠢࡑࡣࡷ࡬ࠥ࡯ࡳࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡨࠥࡧࡳࠡࡗࡕࡐࡀࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴᯲ࠢ"))
                url = bstack111l111ll1l_opy_
                bstack111l111l1l1_opy_ = str(uuid.uuid4())
                bstack111l1111111_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack111l1111111_opy_ or not bstack111l1111111_opy_.strip():
                    bstack111l1111111_opy_ = bstack111l111l1l1_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack11ll11_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࡠࠤ᯳") + bstack111l111l1l1_opy_ + bstack11ll11_opy_ (u"ࠤࡢࠦ᯴"),
                                                        suffix=bstack11ll11_opy_ (u"ࠥࡣࠧ᯵") + bstack111l1111111_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack11ll11_opy_ (u"ࠫࡼࡨࠧ᯶")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack1lll111ll11_opy_ = Path(temp_file.name)
                logger.debug(bstack11ll11_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡩ࡭ࡱ࡫ࠠࡵࡱࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦ࡬ࡰࡥࡤࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧ᯷").format(bstack1lll111ll11_opy_))
            else:
                bstack1lll111ll11_opy_ = Path(bstack111l111ll1l_opy_)
                logger.debug(bstack11ll11_opy_ (u"ࠨࡐࡢࡶ࡫ࠤ࡮ࡹࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡧࠤࡦࡹࠠ࡭ࡱࡦࡥࡱࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣ᯸").format(bstack1lll111ll11_opy_))
        except Exception as e:
            logger.error(bstack11ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡳࡧࡺࡡࡪࡰࠣࡪ࡮ࡲࡥࠡࡨࡵࡳࡲࠦࡰࡢࡶ࡫࠳࡚ࡘࡌ࠻ࠢࡾࢁࠧ᯹").format(e))
            return
        if bstack1lll111ll11_opy_ is None or not bstack1lll111ll11_opy_.exists():
            logger.error(bstack11ll11_opy_ (u"ࠣࡕࡲࡹࡷࡩࡥࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠦ᯺").format(bstack1lll111ll11_opy_))
            return
        if bstack1lll111ll11_opy_.stat().st_size > bstack111l11111ll_opy_:
            logger.error(bstack11ll11_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࡴ࡫ࡽࡩࠥ࡫ࡸࡤࡧࡨࡨࡸࠦ࡭ࡢࡺ࡬ࡱࡺࡳࠠࡢ࡮࡯ࡳࡼ࡫ࡤࠡࡵ࡬ࡾࡪࠦ࡯ࡧࠢࡾࢁࠧ᯻").format(bstack111l11111ll_opy_))
            return
        bstack111l111llll_opy_ = bstack11ll11_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ᯼")
        if bstack111l111l1ll_opy_:
            try:
                params = json.loads(bstack111l111l1ll_opy_)
                if bstack11ll11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨ᯽") in params and params.get(bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢ᯾")) is True:
                    bstack111l111llll_opy_ = bstack11ll11_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥ᯿")
            except Exception as bstack111l11111l1_opy_:
                logger.error(bstack11ll11_opy_ (u"ࠢࡋࡕࡒࡒࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡕࡧࡲࡢ࡯ࡶ࠾ࠥࢁࡽࠣᰀ").format(bstack111l11111l1_opy_))
        bstack111l111111l_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1l1l11lll1l_opy_ import bstack1l11l1ll11l_opy_
        if test_framework_state in bstack1l11l1ll11l_opy_.bstack11l111ll1ll_opy_:
            if bstack111l111llll_opy_ == bstack111ll11l11l_opy_:
                bstack111l111111l_opy_ = True
            bstack111l111llll_opy_ = bstack111ll11l111_opy_
        try:
            platform_index = os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᰁ")]
            target_dir = os.path.join(bstack11ll1llll1l_opy_, bstack11ll1l1llll_opy_ + str(platform_index),
                                      bstack111l111llll_opy_)
            if bstack111l111111l_opy_:
                target_dir = os.path.join(target_dir, bstack111l111l11l_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack11ll11_opy_ (u"ࠤࡆࡶࡪࡧࡴࡦࡦ࠲ࡺࡪࡸࡩࡧ࡫ࡨࡨࠥࡺࡡࡳࡩࡨࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᰂ").format(target_dir))
            file_name = os.path.basename(bstack1lll111ll11_opy_)
            bstack111l1111ll1_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack111l1111ll1_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack1111lllllll_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack1111lllllll_opy_) + extension)):
                    bstack1111lllllll_opy_ += 1
                bstack111l1111ll1_opy_ = os.path.join(target_dir, base_name + str(bstack1111lllllll_opy_) + extension)
            shutil.copy(bstack1lll111ll11_opy_, bstack111l1111ll1_opy_)
            logger.info(bstack11ll11_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡤࡱࡳ࡭ࡪࡪࠠࡵࡱ࠽ࠤࢀࢃࠢᰃ").format(bstack111l1111ll1_opy_))
        except Exception as e:
            logger.error(bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡱࡴࡼࡩ࡯ࡩࠣࡪ࡮ࡲࡥࠡࡶࡲࠤࡹࡧࡲࡨࡧࡷࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᰄ").format(e))
            return
        finally:
            if bstack111l111ll1l_opy_.startswith(bstack11ll11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᰅ")) or bstack111l111ll1l_opy_.startswith(bstack11ll11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᰆ")):
                try:
                    if bstack1lll111ll11_opy_ is not None and bstack1lll111ll11_opy_.exists():
                        bstack1lll111ll11_opy_.unlink()
                        logger.debug(bstack11ll11_opy_ (u"ࠢࡕࡧࡰࡴࡴࡸࡡࡳࡻࠣࡪ࡮ࡲࡥࠡࡦࡨࡰࡪࡺࡥࡥ࠼ࠣࡿࢂࠨᰇ").format(bstack1lll111ll11_opy_))
                except Exception as ex:
                    logger.error(bstack11ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡷࡩࡲࡶ࡯ࡳࡣࡵࡽࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠢᰈ").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack111l111lll1_opy_, stage=STAGE.bstack1111l1111l_opy_, bstack1l111l1111_opy_=None)
    def bstack11l111l111_opy_() -> None:
        bstack11ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡄࡦ࡮ࡨࡸࡪࡹࠠࡢ࡮࡯ࠤ࡫ࡵ࡬ࡥࡧࡵࡷࠥࡽࡨࡰࡵࡨࠤࡳࡧ࡭ࡦࡵࠣࡷࡹࡧࡲࡵࠢࡺ࡭ࡹ࡮ࠠࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣࠢࡩࡳࡱࡲ࡯ࡸࡧࡧࠤࡧࡿࠠࡢࠢࡱࡹࡲࡨࡥࡳࠢ࡬ࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩࡧࠣࡹࡸ࡫ࡲࠨࡵࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᰉ")
        bstack111l111l111_opy_ = bstack11ll1ll11ll_opy_()
        pattern = re.compile(bstack11ll11_opy_ (u"ࡵ࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࡠࡩ࠱ࠢᰊ"))
        if os.path.exists(bstack111l111l111_opy_):
            for item in os.listdir(bstack111l111l111_opy_):
                bstack111l1111l11_opy_ = os.path.join(bstack111l111l111_opy_, item)
                if os.path.isdir(bstack111l1111l11_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack111l1111l11_opy_)
                    except Exception as e:
                        logger.error(bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᰋ").format(e))
        else:
            logger.info(bstack11ll11_opy_ (u"࡚ࠧࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠥᰌ").format(bstack111l111l111_opy_))