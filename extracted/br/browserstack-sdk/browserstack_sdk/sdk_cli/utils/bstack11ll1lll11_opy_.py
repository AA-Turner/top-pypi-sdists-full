# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
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
from bstack_utils.helper import bstack1l1l1lll1l1_opy_
bstack11lll1l111l_opy_ = 100 * 1024 * 1024 # 100 bstack11lll1l1l11_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l1ll1llll1_opy_ = bstack1l1l1lll1l1_opy_()
bstack1l1ll11111l_opy_ = bstack1ll11ll_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᗱ")
bstack11llll1llll_opy_ = bstack1ll11ll_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᗲ")
bstack11llll1ll11_opy_ = bstack1ll11ll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᗳ")
bstack11llll1lll1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᗴ")
bstack11lll111ll1_opy_ = bstack1ll11ll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᗵ")
_11lll11l1l1_opy_ = threading.local()
def bstack1l1111lll11_opy_(test_framework_state, test_hook_state):
    bstack1ll11ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡨࡸࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡸࡪࡹࡴࠡࡧࡹࡩࡳࡺࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡࡵࡷࡳࡷࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࡕࡪ࡬ࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡴࡪࡲࡹࡱࡪࠠࡣࡧࠣࡧࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡴࡩࡧࠣࡩࡻ࡫࡮ࡵࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣࠬࡸࡻࡣࡩࠢࡤࡷࠥࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶࠬࠎࠥࠦࠠࠡࡤࡨࡪࡴࡸࡥࠡࡣࡱࡽࠥ࡬ࡩ࡭ࡧࠣࡹࡵࡲ࡯ࡢࡦࡶࠤࡴࡩࡣࡶࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᗶ")
    _11lll11l1l1_opy_.test_framework_state = test_framework_state
    _11lll11l1l1_opy_.test_hook_state = test_hook_state
def bstack11lll111l11_opy_():
    bstack1ll11ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡕࡩࡹࡸࡩࡦࡸࡨࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷࡩࡸࡺࠠࡦࡸࡨࡲࡹࠦࡳࡵࡣࡷࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭ࡸࡥࡢࡦ࠰ࡰࡴࡩࡡ࡭ࠢࡶࡸࡴࡸࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡤࠤࡹࡻࡰ࡭ࡧࠣࠬࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨ࠰ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࠩࠡࡱࡵࠤ࠭ࡔ࡯࡯ࡧ࠯ࠤࡓࡵ࡮ࡦࠫࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡷࡪࡺ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᗷ")
    return (
        getattr(_11lll11l1l1_opy_, bstack1ll11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࠪᗸ"), None),
        getattr(_11lll11l1l1_opy_, bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪ࠭ᗹ"), None)
    )
class bstack111lll1ll_opy_:
    bstack1ll11ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡌࡩ࡭ࡧࡘࡴࡱࡵࡡࡥࡧࡵࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡢ࡮࡬ࡸࡾࠦࡴࡰࠢࡸࡴࡱࡵࡡࡥࠢࡤࡲࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡥࡥࡸ࡫ࡤࠡࡱࡱࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࡋࡷࠤࡸࡻࡰࡱࡱࡵࡸࡸࠦࡢࡰࡶ࡫ࠤࡱࡵࡣࡢ࡮ࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹࠠࡢࡰࡧࠤࡍ࡚ࡔࡑ࠱ࡋࡘ࡙ࡖࡓࠡࡗࡕࡐࡸ࠲ࠠࡢࡰࡧࠤࡨࡵࡰࡪࡧࡶࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪࠦࡩ࡯ࡶࡲࠤࡦࠦࡤࡦࡵ࡬࡫ࡳࡧࡴࡦࡦࠍࠤࠥࠦࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡻ࡮ࡺࡨࡪࡰࠣࡸ࡭࡫ࠠࡶࡵࡨࡶࠬࡹࠠࡩࡱࡰࡩࠥ࡬࡯࡭ࡦࡨࡶࠥࡻ࡮ࡥࡧࡵࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࡍ࡫ࠦࡡ࡯ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡲࡤࡶࡦࡳࡥࡵࡧࡵࠤ࠭࡯࡮ࠡࡌࡖࡓࡓࠦࡦࡰࡴࡰࡥࡹ࠯ࠠࡪࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࡧ࡮ࡥࠢࡦࡳࡳࡺࡡࡪࡰࡶࠤࡦࠦࡴࡳࡷࡷ࡬ࡾࠦࡶࡢ࡮ࡸࡩࠏࠦࠠࠡࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡯ࡪࡿࠠࠣࡤࡸ࡭ࡱࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥ࠰ࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫ࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡲ࡯ࡥࡨ࡫ࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡧࡱ࡯ࡨࡪࡸ࠻ࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨ࠰ࠏࠦࠠࠡࠢ࡬ࡸࠥࡪࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡵࡦࠡࡣࡧࡨࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢ࡬ࡷࠥࡧࠠࡷࡱ࡬ࡨࠥࡳࡥࡵࡪࡲࡨ⠙࡯ࡴࠡࡪࡤࡲࡩࡲࡥࡴࠢࡤࡰࡱࠦࡥࡳࡴࡲࡶࡸࠦࡧࡳࡣࡦࡩ࡫ࡻ࡬࡭ࡻࠣࡦࡾࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠊࠡࠢࠣࠤࡹ࡮ࡥ࡮ࠢࡤࡲࡩࠦࡳࡪ࡯ࡳࡰࡾࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡸ࡭ࡸ࡯ࡸ࡫ࡱ࡫ࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࡴ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᗺ")
    @staticmethod
    def upload_attachment(bstack11lll11l111_opy_: str, *bstack11lll111lll_opy_) -> None:
        if not bstack11lll11l111_opy_ or not bstack11lll11l111_opy_.strip():
            logger.error(bstack1ll11ll_opy_ (u"ࠨࡡࡥࡦࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡒࡵࡳࡻ࡯ࡤࡦࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࠦࡩࡴࠢࡨࡱࡵࡺࡹࠡࡱࡵࠤࡓࡵ࡮ࡦ࠰ࠥᗻ"))
            return
        bstack11lll11lll1_opy_ = bstack11lll111lll_opy_[0] if bstack11lll111lll_opy_ and len(bstack11lll111lll_opy_) > 0 else None
        bstack11lll111l1l_opy_ = None
        test_framework_state, test_hook_state = bstack11lll111l11_opy_()
        try:
            if bstack11lll11l111_opy_.startswith(bstack1ll11ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᗼ")) or bstack11lll11l111_opy_.startswith(bstack1ll11ll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᗽ")):
                logger.debug(bstack1ll11ll_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡪࡵࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡪࠠࡢࡵ࡙ࠣࡗࡒ࠻ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠤᗾ"))
                url = bstack11lll11l111_opy_
                bstack11lll1l11ll_opy_ = str(uuid.uuid4())
                bstack11lll1l11l1_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11lll1l11l1_opy_ or not bstack11lll1l11l1_opy_.strip():
                    bstack11lll1l11l1_opy_ = bstack11lll1l11ll_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1ll11ll_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࡢࠦᗿ") + bstack11lll1l11ll_opy_ + bstack1ll11ll_opy_ (u"ࠦࡤࠨᘀ"),
                                                        suffix=bstack1ll11ll_opy_ (u"ࠧࡥࠢᘁ") + bstack11lll1l11l1_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1ll11ll_opy_ (u"࠭ࡷࡣࠩᘂ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11lll111l1l_opy_ = Path(temp_file.name)
                logger.debug(bstack1ll11ll_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤ࡫࡯࡬ࡦࠢࡷࡳࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࡮ࡲࡧࡦࡺࡩࡰࡰ࠽ࠤࢀࢃࠢᘃ").format(bstack11lll111l1l_opy_))
            else:
                bstack11lll111l1l_opy_ = Path(bstack11lll11l111_opy_)
                logger.debug(bstack1ll11ll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡩࡴࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡩࠦࡡࡴࠢ࡯ࡳࡨࡧ࡬ࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠥᘄ").format(bstack11lll111l1l_opy_))
        except Exception as e:
            logger.error(bstack1ll11ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡵࡢࡵࡣ࡬ࡲࠥ࡬ࡩ࡭ࡧࠣࡪࡷࡵ࡭ࠡࡲࡤࡸ࡭࠵ࡕࡓࡎ࠽ࠤࢀࢃࠢᘅ").format(e))
            return
        if bstack11lll111l1l_opy_ is None or not bstack11lll111l1l_opy_.exists():
            logger.error(bstack1ll11ll_opy_ (u"ࠥࡗࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨᘆ").format(bstack11lll111l1l_opy_))
            return
        if bstack11lll111l1l_opy_.stat().st_size > bstack11lll1l111l_opy_:
            logger.error(bstack1ll11ll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡶ࡭ࡿ࡫ࠠࡦࡺࡦࡩࡪࡪࡳࠡ࡯ࡤࡼ࡮ࡳࡵ࡮ࠢࡤࡰࡱࡵࡷࡦࡦࠣࡷ࡮ࢀࡥࠡࡱࡩࠤࢀࢃࠢᘇ").format(bstack11lll1l111l_opy_))
            return
        bstack11lll11l1ll_opy_ = bstack1ll11ll_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᘈ")
        if bstack11lll11lll1_opy_:
            try:
                params = json.loads(bstack11lll11lll1_opy_)
                if bstack1ll11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᘉ") in params and params.get(bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᘊ")) is True:
                    bstack11lll11l1ll_opy_ = bstack1ll11ll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᘋ")
            except Exception as bstack11lll11l11l_opy_:
                logger.error(bstack1ll11ll_opy_ (u"ࠤࡍࡗࡔࡔࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡐࡢࡴࡤࡱࡸࡀࠠࡼࡿࠥᘌ").format(bstack11lll11l11l_opy_))
        bstack11lll11ll11_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1lll11l111l_opy_ import bstack1ll1llll111_opy_
        if test_framework_state in bstack1ll1llll111_opy_.bstack11lllll11ll_opy_:
            if bstack11lll11l1ll_opy_ == bstack11llll1ll11_opy_:
                bstack11lll11ll11_opy_ = True
            bstack11lll11l1ll_opy_ = bstack11llll1lll1_opy_
        try:
            platform_index = os.environ[bstack1ll11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᘍ")]
            target_dir = os.path.join(bstack1l1ll1llll1_opy_, bstack1l1ll11111l_opy_ + str(platform_index),
                                      bstack11lll11l1ll_opy_)
            if bstack11lll11ll11_opy_:
                target_dir = os.path.join(target_dir, bstack11lll111ll1_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1ll11ll_opy_ (u"ࠦࡈࡸࡥࡢࡶࡨࡨ࠴ࡼࡥࡳ࡫ࡩ࡭ࡪࡪࠠࡵࡣࡵ࡫ࡪࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᘎ").format(target_dir))
            file_name = os.path.basename(bstack11lll111l1l_opy_)
            bstack11lll11ll1l_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11lll11ll1l_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11lll11llll_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11lll11llll_opy_) + extension)):
                    bstack11lll11llll_opy_ += 1
                bstack11lll11ll1l_opy_ = os.path.join(target_dir, base_name + str(bstack11lll11llll_opy_) + extension)
            shutil.copy(bstack11lll111l1l_opy_, bstack11lll11ll1l_opy_)
            logger.info(bstack1ll11ll_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡦࡳࡵ࡯ࡥࡥࠢࡷࡳ࠿ࠦࡻࡾࠤᘏ").format(bstack11lll11ll1l_opy_))
        except Exception as e:
            logger.error(bstack1ll11ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡳ࡯ࡷ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࡸࡴࠦࡴࡢࡴࡪࡩࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᘐ").format(e))
            return
        finally:
            if bstack11lll11l111_opy_.startswith(bstack1ll11ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᘑ")) or bstack11lll11l111_opy_.startswith(bstack1ll11ll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᘒ")):
                try:
                    if bstack11lll111l1l_opy_ is not None and bstack11lll111l1l_opy_.exists():
                        bstack11lll111l1l_opy_.unlink()
                        logger.debug(bstack1ll11ll_opy_ (u"ࠤࡗࡩࡲࡶ࡯ࡳࡣࡵࡽࠥ࡬ࡩ࡭ࡧࠣࡨࡪࡲࡥࡵࡧࡧ࠾ࠥࢁࡽࠣᘓ").format(bstack11lll111l1l_opy_))
                except Exception as ex:
                    logger.error(bstack1ll11ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤᘔ").format(ex))
    @staticmethod
    def bstack1lllll11ll_opy_() -> None:
        bstack1ll11ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡆࡨࡰࡪࡺࡥࡴࠢࡤࡰࡱࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࡸࡪࡲࡷࡪࠦ࡮ࡢ࡯ࡨࡷࠥࡹࡴࡢࡴࡷࠤࡼ࡯ࡴࡩ࡙ࠢࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥࠤ࡫ࡵ࡬࡭ࡱࡺࡩࡩࠦࡢࡺࠢࡤࠤࡳࡻ࡭ࡣࡧࡵࠤ࡮ࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࡶ࡫ࡩࠥࡻࡳࡦࡴࠪࡷࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᘕ")
        bstack11lll1l1111_opy_ = bstack1l1l1lll1l1_opy_()
        pattern = re.compile(bstack1ll11ll_opy_ (u"ࡷࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࡢࡤࠬࠤᘖ"))
        if os.path.exists(bstack11lll1l1111_opy_):
            for item in os.listdir(bstack11lll1l1111_opy_):
                bstack11lll1111ll_opy_ = os.path.join(bstack11lll1l1111_opy_, item)
                if os.path.isdir(bstack11lll1111ll_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11lll1111ll_opy_)
                    except Exception as e:
                        logger.error(bstack1ll11ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᘗ").format(e))
        else:
            logger.info(bstack1ll11ll_opy_ (u"ࠢࡕࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧᘘ").format(bstack11lll1l1111_opy_))