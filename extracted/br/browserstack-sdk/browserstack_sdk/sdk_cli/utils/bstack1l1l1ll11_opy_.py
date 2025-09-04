# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
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
from bstack_utils.helper import bstack1l1ll1l11l1_opy_
bstack11lll111l11_opy_ = 100 * 1024 * 1024 # 100 bstack11lll1l11ll_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l1ll1l111l_opy_ = bstack1l1ll1l11l1_opy_()
bstack1l1l1lll111_opy_ = bstack1111l1l_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᗲ")
bstack11lllll1111_opy_ = bstack1111l1l_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᗳ")
bstack11llll1ll1l_opy_ = bstack1111l1l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᗴ")
bstack11llll1lll1_opy_ = bstack1111l1l_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᗵ")
bstack11lll11l111_opy_ = bstack1111l1l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᗶ")
_11lll1l1111_opy_ = threading.local()
def bstack1l111l1l111_opy_(test_framework_state, test_hook_state):
    bstack1111l1l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡖࡩࡹࠦࡴࡩࡧࠣࡧࡺࡸࡲࡦࡰࡷࠤࡹ࡫ࡳࡵࠢࡨࡺࡪࡴࡴࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡸ࡭ࡸࡥࡢࡦ࠰ࡰࡴࡩࡡ࡭ࠢࡶࡸࡴࡸࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࡖ࡫࡭ࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡵ࡫ࡳࡺࡲࡤࠡࡤࡨࠤࡨࡧ࡬࡭ࡧࡧࠤࡧࡿࠠࡵࡪࡨࠤࡪࡼࡥ࡯ࡶࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࠭ࡹࡵࡤࡪࠣࡥࡸࠦࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠭ࠏࠦࠠࠡࠢࡥࡩ࡫ࡵࡲࡦࠢࡤࡲࡾࠦࡦࡪ࡮ࡨࠤࡺࡶ࡬ࡰࡣࡧࡷࠥࡵࡣࡤࡷࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᗷ")
    _11lll1l1111_opy_.test_framework_state = test_framework_state
    _11lll1l1111_opy_.test_hook_state = test_hook_state
def bstack11lll11l1ll_opy_():
    bstack1111l1l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡖࡪࡺࡲࡪࡧࡹࡩࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡸࡪࡹࡴࠡࡧࡹࡩࡳࡺࠠࡴࡶࡤࡸࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡲࡦࡣࡧ࠱ࡱࡵࡣࡢ࡮ࠣࡷࡹࡵࡲࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡥࠥࡺࡵࡱ࡮ࡨࠤ࠭ࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩ࠱ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࠪࠢࡲࡶࠥ࠮ࡎࡰࡰࡨ࠰ࠥࡔ࡯࡯ࡧࠬࠤ࡮࡬ࠠ࡯ࡱࡷࠤࡸ࡫ࡴ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᗸ")
    return (
        getattr(_11lll1l1111_opy_, bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࠫᗹ"), None),
        getattr(_11lll1l1111_opy_, bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࠧᗺ"), None)
    )
class bstack1llllllll_opy_:
    bstack1111l1l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡆࡪ࡮ࡨ࡙ࡵࡲ࡯ࡢࡦࡨࡶࠥࡶࡲࡰࡸ࡬ࡨࡪࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࡣ࡯࡭ࡹࡿࠠࡵࡱࠣࡹࡵࡲ࡯ࡢࡦࠣࡥࡳࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡦࡦࡹࡥࡥࠢࡲࡲࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࡌࡸࠥࡹࡵࡱࡲࡲࡶࡹࡹࠠࡣࡱࡷ࡬ࠥࡲ࡯ࡤࡣ࡯ࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳࠡࡣࡱࡨࠥࡎࡔࡕࡒ࠲ࡌ࡙࡚ࡐࡔࠢࡘࡖࡑࡹࠬࠡࡣࡱࡨࠥࡩ࡯ࡱ࡫ࡨࡷࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫ࠠࡪࡰࡷࡳࠥࡧࠠࡥࡧࡶ࡭࡬ࡴࡡࡵࡧࡧࠎࠥࠦࠠࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡼ࡯ࡴࡩ࡫ࡱࠤࡹ࡮ࡥࠡࡷࡶࡩࡷ࠭ࡳࠡࡪࡲࡱࡪࠦࡦࡰ࡮ࡧࡩࡷࠦࡵ࡯ࡦࡨࡶࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࡎ࡬ࠠࡢࡰࠣࡳࡵࡺࡩࡰࡰࡤࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡳࡥࡷࡧ࡭ࡦࡶࡨࡶࠥ࠮ࡩ࡯ࠢࡍࡗࡔࡔࠠࡧࡱࡵࡱࡦࡺࠩࠡ࡫ࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡡ࡯ࡦࠣࡧࡴࡴࡴࡢ࡫ࡱࡷࠥࡧࠠࡵࡴࡸࡸ࡭ࡿࠠࡷࡣ࡯ࡹࡪࠐࠠࠡࠢࠣࡪࡴࡸࠠࡵࡪࡨࠤࡰ࡫ࡹࠡࠤࡥࡹ࡮ࡲࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦ࠱ࠦࡴࡩࡧࠣࡪ࡮ࡲࡥࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡳࡰࡦࡩࡥࡥࠢ࡬ࡲࠥࡺࡨࡦࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡨࡲࡰࡩ࡫ࡲ࠼ࠢࡲࡸ࡭࡫ࡲࡸ࡫ࡶࡩ࠱ࠐࠠࠡࠢࠣ࡭ࡹࠦࡤࡦࡨࡤࡹࡱࡺࡳࠡࡶࡲࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣ࠰ࠍࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡼࡥࡳࡵ࡬ࡳࡳࠦ࡯ࡧࠢࡤࡨࡩࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣ࡭ࡸࠦࡡࠡࡸࡲ࡭ࡩࠦ࡭ࡦࡶ࡫ࡳࡩ⠚ࡩࡵࠢ࡫ࡥࡳࡪ࡬ࡦࡵࠣࡥࡱࡲࠠࡦࡴࡵࡳࡷࡹࠠࡨࡴࡤࡧࡪ࡬ࡵ࡭࡮ࡼࠤࡧࡿࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠋࠢࠣࠤࠥࡺࡨࡦ࡯ࠣࡥࡳࡪࠠࡴ࡫ࡰࡴࡱࡿࠠࡳࡧࡷࡹࡷࡴࡩ࡯ࡩࠣࡻ࡮ࡺࡨࡰࡷࡷࠤࡹ࡮ࡲࡰࡹ࡬ࡲ࡬ࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡵ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᗻ")
    @staticmethod
    def upload_attachment(bstack11lll1l11l1_opy_: str, *bstack11lll11l11l_opy_) -> None:
        if not bstack11lll1l11l1_opy_ or not bstack11lll1l11l1_opy_.strip():
            logger.error(bstack1111l1l_opy_ (u"ࠢࡢࡦࡧࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡓࡶࡴࡼࡩࡥࡧࡧࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࠠࡪࡵࠣࡩࡲࡶࡴࡺࠢࡲࡶࠥࡔ࡯࡯ࡧ࠱ࠦᗼ"))
            return
        bstack11lll11lll1_opy_ = bstack11lll11l11l_opy_[0] if bstack11lll11l11l_opy_ and len(bstack11lll11l11l_opy_) > 0 else None
        bstack11lll111lll_opy_ = None
        test_framework_state, test_hook_state = bstack11lll11l1ll_opy_()
        try:
            if bstack11lll1l11l1_opy_.startswith(bstack1111l1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᗽ")) or bstack11lll1l11l1_opy_.startswith(bstack1111l1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᗾ")):
                logger.debug(bstack1111l1l_opy_ (u"ࠥࡔࡦࡺࡨࠡ࡫ࡶࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡤࠡࡣࡶࠤ࡚ࡘࡌ࠼ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠥᗿ"))
                url = bstack11lll1l11l1_opy_
                bstack11lll11ll11_opy_ = str(uuid.uuid4())
                bstack11lll1l111l_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11lll1l111l_opy_ or not bstack11lll1l111l_opy_.strip():
                    bstack11lll1l111l_opy_ = bstack11lll11ll11_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1111l1l_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࡣࠧᘀ") + bstack11lll11ll11_opy_ + bstack1111l1l_opy_ (u"ࠧࡥࠢᘁ"),
                                                        suffix=bstack1111l1l_opy_ (u"ࠨ࡟ࠣᘂ") + bstack11lll1l111l_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1111l1l_opy_ (u"ࠧࡸࡤࠪᘃ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11lll111lll_opy_ = Path(temp_file.name)
                logger.debug(bstack1111l1l_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥ࡬ࡩ࡭ࡧࠣࡸࡴࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢ࡯ࡳࡨࡧࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᘄ").format(bstack11lll111lll_opy_))
            else:
                bstack11lll111lll_opy_ = Path(bstack11lll1l11l1_opy_)
                logger.debug(bstack1111l1l_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡪࡵࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡪࠠࡢࡵࠣࡰࡴࡩࡡ࡭ࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠦᘅ").format(bstack11lll111lll_opy_))
        except Exception as e:
            logger.error(bstack1111l1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡯ࡣࡶࡤ࡭ࡳࠦࡦࡪ࡮ࡨࠤ࡫ࡸ࡯࡮ࠢࡳࡥࡹ࡮࠯ࡖࡔࡏ࠾ࠥࢁࡽࠣᘆ").format(e))
            return
        if bstack11lll111lll_opy_ is None or not bstack11lll111lll_opy_.exists():
            logger.error(bstack1111l1l_opy_ (u"ࠦࡘࡵࡵࡳࡥࡨࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠢᘇ").format(bstack11lll111lll_opy_))
            return
        if bstack11lll111lll_opy_.stat().st_size > bstack11lll111l11_opy_:
            logger.error(bstack1111l1l_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡷ࡮ࢀࡥࠡࡧࡻࡧࡪ࡫ࡤࡴࠢࡰࡥࡽ࡯࡭ࡶ࡯ࠣࡥࡱࡲ࡯ࡸࡧࡧࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࢁࡽࠣᘈ").format(bstack11lll111l11_opy_))
            return
        bstack11lll11ll1l_opy_ = bstack1111l1l_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᘉ")
        if bstack11lll11lll1_opy_:
            try:
                params = json.loads(bstack11lll11lll1_opy_)
                if bstack1111l1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᘊ") in params and params.get(bstack1111l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᘋ")) is True:
                    bstack11lll11ll1l_opy_ = bstack1111l1l_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᘌ")
            except Exception as bstack11lll1l1l1l_opy_:
                logger.error(bstack1111l1l_opy_ (u"ࠥࡎࡘࡕࡎࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡑࡣࡵࡥࡲࡹ࠺ࠡࡽࢀࠦᘍ").format(bstack11lll1l1l1l_opy_))
        bstack11lll11l1l1_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1lll1llll11_opy_ import bstack1lll111llll_opy_
        if test_framework_state in bstack1lll111llll_opy_.bstack11llllll111_opy_:
            if bstack11lll11ll1l_opy_ == bstack11llll1ll1l_opy_:
                bstack11lll11l1l1_opy_ = True
            bstack11lll11ll1l_opy_ = bstack11llll1lll1_opy_
        try:
            platform_index = os.environ[bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᘎ")]
            target_dir = os.path.join(bstack1l1ll1l111l_opy_, bstack1l1l1lll111_opy_ + str(platform_index),
                                      bstack11lll11ll1l_opy_)
            if bstack11lll11l1l1_opy_:
                target_dir = os.path.join(target_dir, bstack11lll11l111_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1111l1l_opy_ (u"ࠧࡉࡲࡦࡣࡷࡩࡩ࠵ࡶࡦࡴ࡬ࡪ࡮࡫ࡤࠡࡶࡤࡶ࡬࡫ࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᘏ").format(target_dir))
            file_name = os.path.basename(bstack11lll111lll_opy_)
            bstack11lll111l1l_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11lll111l1l_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11lll111ll1_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11lll111ll1_opy_) + extension)):
                    bstack11lll111ll1_opy_ += 1
                bstack11lll111l1l_opy_ = os.path.join(target_dir, base_name + str(bstack11lll111ll1_opy_) + extension)
            shutil.copy(bstack11lll111lll_opy_, bstack11lll111l1l_opy_)
            logger.info(bstack1111l1l_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡧࡴࡶࡩࡦࡦࠣࡸࡴࡀࠠࡼࡿࠥᘐ").format(bstack11lll111l1l_opy_))
        except Exception as e:
            logger.error(bstack1111l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡭ࡰࡸ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࡹࡵࠠࡵࡣࡵ࡫ࡪࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᘑ").format(e))
            return
        finally:
            if bstack11lll1l11l1_opy_.startswith(bstack1111l1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᘒ")) or bstack11lll1l11l1_opy_.startswith(bstack1111l1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᘓ")):
                try:
                    if bstack11lll111lll_opy_ is not None and bstack11lll111lll_opy_.exists():
                        bstack11lll111lll_opy_.unlink()
                        logger.debug(bstack1111l1l_opy_ (u"ࠥࡘࡪࡳࡰࡰࡴࡤࡶࡾࠦࡦࡪ࡮ࡨࠤࡩ࡫࡬ࡦࡶࡨࡨ࠿ࠦࡻࡾࠤᘔ").format(bstack11lll111lll_opy_))
                except Exception as ex:
                    logger.error(bstack1111l1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠥᘕ").format(ex))
    @staticmethod
    def bstack11l111l1ll_opy_() -> None:
        bstack1111l1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡇࡩࡱ࡫ࡴࡦࡵࠣࡥࡱࡲࠠࡧࡱ࡯ࡨࡪࡸࡳࠡࡹ࡫ࡳࡸ࡫ࠠ࡯ࡣࡰࡩࡸࠦࡳࡵࡣࡵࡸࠥࡽࡩࡵࡪ࡚ࠣࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦࠥ࡬࡯࡭࡮ࡲࡻࡪࡪࠠࡣࡻࠣࡥࠥࡴࡵ࡮ࡤࡨࡶࠥ࡯࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷ࡬ࡪࠦࡵࡴࡧࡵࠫࡸࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᘖ")
        bstack11lll1l1l11_opy_ = bstack1l1ll1l11l1_opy_()
        pattern = re.compile(bstack1111l1l_opy_ (u"ࡸࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳࡜ࡥ࠭ࠥᘗ"))
        if os.path.exists(bstack11lll1l1l11_opy_):
            for item in os.listdir(bstack11lll1l1l11_opy_):
                bstack11lll11llll_opy_ = os.path.join(bstack11lll1l1l11_opy_, item)
                if os.path.isdir(bstack11lll11llll_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11lll11llll_opy_)
                    except Exception as e:
                        logger.error(bstack1111l1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᘘ").format(e))
        else:
            logger.info(bstack1111l1l_opy_ (u"ࠣࡖ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨᘙ").format(bstack11lll1l1l11_opy_))