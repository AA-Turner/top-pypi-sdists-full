# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
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
from bstack_utils.helper import bstack1l1ll11ll1l_opy_
bstack11lll111l11_opy_ = 100 * 1024 * 1024 # 100 bstack11lll111lll_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l1lll1lll1_opy_ = bstack1l1ll11ll1l_opy_()
bstack1l1ll1l11ll_opy_ = bstack1l11ll1_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᗰ")
bstack11lllll1111_opy_ = bstack1l11ll1_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᗱ")
bstack11llll1ll1l_opy_ = bstack1l11ll1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᗲ")
bstack11llll1lll1_opy_ = bstack1l11ll1_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᗳ")
bstack11lll1111ll_opy_ = bstack1l11ll1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᗴ")
_11lll1l1111_opy_ = threading.local()
def bstack1l1111lllll_opy_(test_framework_state, test_hook_state):
    bstack1l11ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡧࡷࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷࡩࡸࡺࠠࡦࡸࡨࡲࡹࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡶ࡫ࡶࡪࡧࡤ࠮࡮ࡲࡧࡦࡲࠠࡴࡶࡲࡶࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡳࡩࡱࡸࡰࡩࠦࡢࡦࠢࡦࡥࡱࡲࡥࡥࠢࡥࡽࠥࡺࡨࡦࠢࡨࡺࡪࡴࡴࠡࡪࡤࡲࡩࡲࡥࡳࠢࠫࡷࡺࡩࡨࠡࡣࡶࠤࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵࠫࠍࠤࠥࠦࠠࡣࡧࡩࡳࡷ࡫ࠠࡢࡰࡼࠤ࡫࡯࡬ࡦࠢࡸࡴࡱࡵࡡࡥࡵࠣࡳࡨࡩࡵࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᗵ")
    _11lll1l1111_opy_.test_framework_state = test_framework_state
    _11lll1l1111_opy_.test_hook_state = test_hook_state
def bstack11lll111ll1_opy_():
    bstack1l11ll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡔࡨࡸࡷ࡯ࡥࡷࡧࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶࡨࡷࡹࠦࡥࡷࡧࡱࡸࠥࡹࡴࡢࡶࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡࡵࡷࡳࡷࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡣࠣࡸࡺࡶ࡬ࡦࠢࠫࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧ࠯ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪ࠯ࠠࡰࡴࠣࠬࡓࡵ࡮ࡦ࠮ࠣࡒࡴࡴࡥࠪࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᗶ")
    return (
        getattr(_11lll1l1111_opy_, bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࠩᗷ"), None),
        getattr(_11lll1l1111_opy_, bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࠬᗸ"), None)
    )
class bstack1111l1l11_opy_:
    bstack1l11ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡋ࡯࡬ࡦࡗࡳࡰࡴࡧࡤࡦࡴࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡡ࡭࡫ࡷࡽࠥࡺ࡯ࠡࡷࡳࡰࡴࡧࡤࠡࡣࡱࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࡊࡶࠣࡷࡺࡶࡰࡰࡴࡷࡷࠥࡨ࡯ࡵࡪࠣࡰࡴࡩࡡ࡭ࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࡸࠦࡡ࡯ࡦࠣࡌ࡙࡚ࡐ࠰ࡊࡗࡘࡕ࡙ࠠࡖࡔࡏࡷ࠱ࠦࡡ࡯ࡦࠣࡧࡴࡶࡩࡦࡵࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࡵࡱࠣࡥࠥࡪࡥࡴ࡫ࡪࡲࡦࡺࡥࡥࠌࠣࠤࠥࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡺ࡭ࡹ࡮ࡩ࡯ࠢࡷ࡬ࡪࠦࡵࡴࡧࡵࠫࡸࠦࡨࡰ࡯ࡨࠤ࡫ࡵ࡬ࡥࡧࡵࠤࡺࡴࡤࡦࡴࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࡌࡪࠥࡧ࡮ࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࠣࠬ࡮ࡴࠠࡋࡕࡒࡒࠥ࡬࡯ࡳ࡯ࡤࡸ࠮ࠦࡩࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡦࡴࡤࠡࡥࡲࡲࡹࡧࡩ࡯ࡵࠣࡥࠥࡺࡲࡶࡶ࡫ࡽࠥࡼࡡ࡭ࡷࡨࠎࠥࠦࠠࠡࡨࡲࡶࠥࡺࡨࡦࠢ࡮ࡩࡾࠦࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤ࠯ࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡱ࡮ࡤࡧࡪࡪࠠࡪࡰࠣࡸ࡭࡫ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡦࡰ࡮ࡧࡩࡷࡁࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧ࠯ࠎࠥࠦࠠࠡ࡫ࡷࠤࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ࠮ࠋࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡺࡪࡸࡳࡪࡱࡱࠤࡴ࡬ࠠࡢࡦࡧࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡ࡫ࡶࠤࡦࠦࡶࡰ࡫ࡧࠤࡲ࡫ࡴࡩࡱࡧ⠘࡮ࡺࠠࡩࡣࡱࡨࡱ࡫ࡳࠡࡣ࡯ࡰࠥ࡫ࡲࡳࡱࡵࡷࠥ࡭ࡲࡢࡥࡨࡪࡺࡲ࡬ࡺࠢࡥࡽࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠐࠠࠡࠢࠣࡸ࡭࡫࡭ࠡࡣࡱࡨࠥࡹࡩ࡮ࡲ࡯ࡽࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡷ࡬ࡷࡵࡷࡪࡰࡪࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࡳ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᗹ")
    @staticmethod
    def upload_attachment(bstack11lll11l11l_opy_: str, *bstack11lll11lll1_opy_) -> None:
        if not bstack11lll11l11l_opy_ or not bstack11lll11l11l_opy_.strip():
            logger.error(bstack1l11ll1_opy_ (u"ࠧࡧࡤࡥࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡑࡴࡲࡺ࡮ࡪࡥࡥࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡯ࡳࠡࡧࡰࡴࡹࡿࠠࡰࡴࠣࡒࡴࡴࡥ࠯ࠤᗺ"))
            return
        bstack11lll1l111l_opy_ = bstack11lll11lll1_opy_[0] if bstack11lll11lll1_opy_ and len(bstack11lll11lll1_opy_) > 0 else None
        bstack11lll111l1l_opy_ = None
        test_framework_state, test_hook_state = bstack11lll111ll1_opy_()
        try:
            if bstack11lll11l11l_opy_.startswith(bstack1l11ll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᗻ")) or bstack11lll11l11l_opy_.startswith(bstack1l11ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᗼ")):
                logger.debug(bstack1l11ll1_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡩࡴࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡩࠦࡡࡴࠢࡘࡖࡑࡁࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠣᗽ"))
                url = bstack11lll11l11l_opy_
                bstack11lll1l1l11_opy_ = str(uuid.uuid4())
                bstack11lll11l111_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11lll11l111_opy_ or not bstack11lll11l111_opy_.strip():
                    bstack11lll11l111_opy_ = bstack11lll1l1l11_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1l11ll1_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࡡࠥᗾ") + bstack11lll1l1l11_opy_ + bstack1l11ll1_opy_ (u"ࠥࡣࠧᗿ"),
                                                        suffix=bstack1l11ll1_opy_ (u"ࠦࡤࠨᘀ") + bstack11lll11l111_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1l11ll1_opy_ (u"ࠬࡽࡢࠨᘁ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11lll111l1l_opy_ = Path(temp_file.name)
                logger.debug(bstack1l11ll1_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡪ࡮ࡲࡥࠡࡶࡲࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࡭ࡱࡦࡥࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᘂ").format(bstack11lll111l1l_opy_))
            else:
                bstack11lll111l1l_opy_ = Path(bstack11lll11l11l_opy_)
                logger.debug(bstack1l11ll1_opy_ (u"ࠢࡑࡣࡷ࡬ࠥ࡯ࡳࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡨࠥࡧࡳࠡ࡮ࡲࡧࡦࡲࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤᘃ").format(bstack11lll111l1l_opy_))
        except Exception as e:
            logger.error(bstack1l11ll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡴࡨࡴࡢ࡫ࡱࠤ࡫࡯࡬ࡦࠢࡩࡶࡴࡳࠠࡱࡣࡷ࡬࠴࡛ࡒࡍ࠼ࠣࡿࢂࠨᘄ").format(e))
            return
        if bstack11lll111l1l_opy_ is None or not bstack11lll111l1l_opy_.exists():
            logger.error(bstack1l11ll1_opy_ (u"ࠤࡖࡳࡺࡸࡣࡦࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧᘅ").format(bstack11lll111l1l_opy_))
            return
        if bstack11lll111l1l_opy_.stat().st_size > bstack11lll111l11_opy_:
            logger.error(bstack1l11ll1_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡵ࡬ࡾࡪࠦࡥࡹࡥࡨࡩࡩࡹࠠ࡮ࡣࡻ࡭ࡲࡻ࡭ࠡࡣ࡯ࡰࡴࡽࡥࡥࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡿࢂࠨᘆ").format(bstack11lll111l11_opy_))
            return
        bstack11lll1l11ll_opy_ = bstack1l11ll1_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᘇ")
        if bstack11lll1l111l_opy_:
            try:
                params = json.loads(bstack11lll1l111l_opy_)
                if bstack1l11ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᘈ") in params and params.get(bstack1l11ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᘉ")) is True:
                    bstack11lll1l11ll_opy_ = bstack1l11ll1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᘊ")
            except Exception as bstack11lll11ll1l_opy_:
                logger.error(bstack1l11ll1_opy_ (u"ࠣࡌࡖࡓࡓࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡖࡡࡳࡣࡰࡷ࠿ࠦࡻࡾࠤᘋ").format(bstack11lll11ll1l_opy_))
        bstack11lll11l1ll_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1llll111l1l_opy_
        if test_framework_state in bstack1llll111l1l_opy_.bstack1l111l1llll_opy_:
            if bstack11lll1l11ll_opy_ == bstack11llll1ll1l_opy_:
                bstack11lll11l1ll_opy_ = True
            bstack11lll1l11ll_opy_ = bstack11llll1lll1_opy_
        try:
            platform_index = os.environ[bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᘌ")]
            target_dir = os.path.join(bstack1l1lll1lll1_opy_, bstack1l1ll1l11ll_opy_ + str(platform_index),
                                      bstack11lll1l11ll_opy_)
            if bstack11lll11l1ll_opy_:
                target_dir = os.path.join(target_dir, bstack11lll1111ll_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1l11ll1_opy_ (u"ࠥࡇࡷ࡫ࡡࡵࡧࡧ࠳ࡻ࡫ࡲࡪࡨ࡬ࡩࡩࠦࡴࡢࡴࡪࡩࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᘍ").format(target_dir))
            file_name = os.path.basename(bstack11lll111l1l_opy_)
            bstack11lll1l11l1_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11lll1l11l1_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11lll11l1l1_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11lll11l1l1_opy_) + extension)):
                    bstack11lll11l1l1_opy_ += 1
                bstack11lll1l11l1_opy_ = os.path.join(target_dir, base_name + str(bstack11lll11l1l1_opy_) + extension)
            shutil.copy(bstack11lll111l1l_opy_, bstack11lll1l11l1_opy_)
            logger.info(bstack1l11ll1_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡥࡲࡴ࡮࡫ࡤࠡࡶࡲ࠾ࠥࢁࡽࠣᘎ").format(bstack11lll1l11l1_opy_))
        except Exception as e:
            logger.error(bstack1l11ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡲࡵࡶࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࡷࡳࠥࡺࡡࡳࡩࡨࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᘏ").format(e))
            return
        finally:
            if bstack11lll11l11l_opy_.startswith(bstack1l11ll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᘐ")) or bstack11lll11l11l_opy_.startswith(bstack1l11ll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᘑ")):
                try:
                    if bstack11lll111l1l_opy_ is not None and bstack11lll111l1l_opy_.exists():
                        bstack11lll111l1l_opy_.unlink()
                        logger.debug(bstack1l11ll1_opy_ (u"ࠣࡖࡨࡱࡵࡵࡲࡢࡴࡼࠤ࡫࡯࡬ࡦࠢࡧࡩࡱ࡫ࡴࡦࡦ࠽ࠤࢀࢃࠢᘒ").format(bstack11lll111l1l_opy_))
                except Exception as ex:
                    logger.error(bstack1l11ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣᘓ").format(ex))
    @staticmethod
    def bstack1l1llllll_opy_() -> None:
        bstack1l11ll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡧ࡯ࡩࡹ࡫ࡳࠡࡣ࡯ࡰࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࡷࡩࡱࡶࡩࠥࡴࡡ࡮ࡧࡶࠤࡸࡺࡡࡳࡶࠣࡻ࡮ࡺࡨࠡࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤࠣࡪࡴࡲ࡬ࡰࡹࡨࡨࠥࡨࡹࠡࡣࠣࡲࡺࡳࡢࡦࡴࠣ࡭ࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪࡨࠤࡺࡹࡥࡳࠩࡶࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᘔ")
        bstack11lll11llll_opy_ = bstack1l1ll11ll1l_opy_()
        pattern = re.compile(bstack1l11ll1_opy_ (u"ࡶ࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࡡࡪࠫࠣᘕ"))
        if os.path.exists(bstack11lll11llll_opy_):
            for item in os.listdir(bstack11lll11llll_opy_):
                bstack11lll11ll11_opy_ = os.path.join(bstack11lll11llll_opy_, item)
                if os.path.isdir(bstack11lll11ll11_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11lll11ll11_opy_)
                    except Exception as e:
                        logger.error(bstack1l11ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᘖ").format(e))
        else:
            logger.info(bstack1l11ll1_opy_ (u"ࠨࡔࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠦᘗ").format(bstack11lll11llll_opy_))