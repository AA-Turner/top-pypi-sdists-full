# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
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
from bstack_utils.helper import bstack11lll11111l_opy_
bstack111l1111ll1_opy_ = 100 * 1024 * 1024 # 100 bstack1111llll11l_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack11lll11l1ll_opy_ = bstack11lll11111l_opy_()
bstack11ll111ll11_opy_ = bstack1l1111l_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᰃ")
bstack111ll1111l1_opy_ = bstack1l1111l_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᰄ")
bstack111l1llllll_opy_ = bstack1l1111l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᰅ")
bstack111ll111111_opy_ = bstack1l1111l_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᰆ")
bstack111l11111l1_opy_ = bstack1l1111l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᰇ")
_111l1111l1l_opy_ = threading.local()
def bstack11l111l111l_opy_(test_framework_state, test_hook_state):
    bstack1l1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡨࡸࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡸࡪࡹࡴࠡࡧࡹࡩࡳࡺࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡࡵࡷࡳࡷࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࡕࡪ࡬ࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡴࡪࡲࡹࡱࡪࠠࡣࡧࠣࡧࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡴࡩࡧࠣࡩࡻ࡫࡮ࡵࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣࠬࡸࡻࡣࡩࠢࡤࡷࠥࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶࠬࠎࠥࠦࠠࠡࡤࡨࡪࡴࡸࡥࠡࡣࡱࡽࠥ࡬ࡩ࡭ࡧࠣࡹࡵࡲ࡯ࡢࡦࡶࠤࡴࡩࡣࡶࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᰈ")
    _111l1111l1l_opy_.test_framework_state = test_framework_state
    _111l1111l1l_opy_.test_hook_state = test_hook_state
def bstack1111llllll1_opy_():
    bstack1l1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡕࡩࡹࡸࡩࡦࡸࡨࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷࡩࡸࡺࠠࡦࡸࡨࡲࡹࠦࡳࡵࡣࡷࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭ࡸࡥࡢࡦ࠰ࡰࡴࡩࡡ࡭ࠢࡶࡸࡴࡸࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡤࠤࡹࡻࡰ࡭ࡧࠣࠬࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨ࠰ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࠩࠡࡱࡵࠤ࠭ࡔ࡯࡯ࡧ࠯ࠤࡓࡵ࡮ࡦࠫࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡷࡪࡺ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᰉ")
    return (
        getattr(_111l1111l1l_opy_, bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࠪᰊ"), None),
        getattr(_111l1111l1l_opy_, bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪ࠭ᰋ"), None)
    )
class bstack1l1l1ll1l1_opy_:
    bstack1l1111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡌࡩ࡭ࡧࡘࡴࡱࡵࡡࡥࡧࡵࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡢ࡮࡬ࡸࡾࠦࡴࡰࠢࡸࡴࡱࡵࡡࡥࠢࡤࡲࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡥࡥࡸ࡫ࡤࠡࡱࡱࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࡋࡷࠤࡸࡻࡰࡱࡱࡵࡸࡸࠦࡢࡰࡶ࡫ࠤࡱࡵࡣࡢ࡮ࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹࠠࡢࡰࡧࠤࡍ࡚ࡔࡑ࠱ࡋࡘ࡙ࡖࡓࠡࡗࡕࡐࡸ࠲ࠠࡢࡰࡧࠤࡨࡵࡰࡪࡧࡶࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪࠦࡩ࡯ࡶࡲࠤࡦࠦࡤࡦࡵ࡬࡫ࡳࡧࡴࡦࡦࠍࠤࠥࠦࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡻ࡮ࡺࡨࡪࡰࠣࡸ࡭࡫ࠠࡶࡵࡨࡶࠬࡹࠠࡩࡱࡰࡩࠥ࡬࡯࡭ࡦࡨࡶࠥࡻ࡮ࡥࡧࡵࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࡍ࡫ࠦࡡ࡯ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡲࡤࡶࡦࡳࡥࡵࡧࡵࠤ࠭࡯࡮ࠡࡌࡖࡓࡓࠦࡦࡰࡴࡰࡥࡹ࠯ࠠࡪࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࡧ࡮ࡥࠢࡦࡳࡳࡺࡡࡪࡰࡶࠤࡦࠦࡴࡳࡷࡷ࡬ࡾࠦࡶࡢ࡮ࡸࡩࠏࠦࠠࠡࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡯ࡪࡿࠠࠣࡤࡸ࡭ࡱࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥ࠰ࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫ࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡲ࡯ࡥࡨ࡫ࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡧࡱ࡯ࡨࡪࡸ࠻ࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨ࠰ࠏࠦࠠࠡࠢ࡬ࡸࠥࡪࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡵࡦࠡࡣࡧࡨࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢ࡬ࡷࠥࡧࠠࡷࡱ࡬ࡨࠥࡳࡥࡵࡪࡲࡨ⠙࡯ࡴࠡࡪࡤࡲࡩࡲࡥࡴࠢࡤࡰࡱࠦࡥࡳࡴࡲࡶࡸࠦࡧࡳࡣࡦࡩ࡫ࡻ࡬࡭ࡻࠣࡦࡾࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠊࠡࠢࠣࠤࡹ࡮ࡥ࡮ࠢࡤࡲࡩࠦࡳࡪ࡯ࡳࡰࡾࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡸ࡭ࡸ࡯ࡸ࡫ࡱ࡫ࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࡴ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᰌ")
    @staticmethod
    def upload_attachment(bstack1111lllll11_opy_: str, *bstack111l1111111_opy_) -> None:
        if not bstack1111lllll11_opy_ or not bstack1111lllll11_opy_.strip():
            logger.error(bstack1l1111l_opy_ (u"ࠨࡡࡥࡦࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡒࡵࡳࡻ࡯ࡤࡦࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࠦࡩࡴࠢࡨࡱࡵࡺࡹࠡࡱࡵࠤࡓࡵ࡮ࡦ࠰ࠥᰍ"))
            return
        bstack111l1111lll_opy_ = bstack111l1111111_opy_[0] if bstack111l1111111_opy_ and len(bstack111l1111111_opy_) > 0 else None
        bstack1ll1l1ll1l1_opy_ = None
        test_framework_state, test_hook_state = bstack1111llllll1_opy_()
        try:
            if bstack1111lllll11_opy_.startswith(bstack1l1111l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᰎ")) or bstack1111lllll11_opy_.startswith(bstack1l1111l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᰏ")):
                logger.debug(bstack1l1111l_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡪࡵࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡪࠠࡢࡵ࡙ࠣࡗࡒ࠻ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠤᰐ"))
                url = bstack1111lllll11_opy_
                bstack1111lllll1l_opy_ = str(uuid.uuid4())
                bstack1111llll1l1_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack1111llll1l1_opy_ or not bstack1111llll1l1_opy_.strip():
                    bstack1111llll1l1_opy_ = bstack1111lllll1l_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1l1111l_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࡢࠦᰑ") + bstack1111lllll1l_opy_ + bstack1l1111l_opy_ (u"ࠦࡤࠨᰒ"),
                                                        suffix=bstack1l1111l_opy_ (u"ࠧࡥࠢᰓ") + bstack1111llll1l1_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1l1111l_opy_ (u"࠭ࡷࡣࠩᰔ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack1ll1l1ll1l1_opy_ = Path(temp_file.name)
                logger.debug(bstack1l1111l_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤ࡫࡯࡬ࡦࠢࡷࡳࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࡮ࡲࡧࡦࡺࡩࡰࡰ࠽ࠤࢀࢃࠢᰕ").format(bstack1ll1l1ll1l1_opy_))
            else:
                bstack1ll1l1ll1l1_opy_ = Path(bstack1111lllll11_opy_)
                logger.debug(bstack1l1111l_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡩࡴࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡩࠦࡡࡴࠢ࡯ࡳࡨࡧ࡬ࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠥᰖ").format(bstack1ll1l1ll1l1_opy_))
        except Exception as e:
            logger.error(bstack1l1111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡵࡢࡵࡣ࡬ࡲࠥ࡬ࡩ࡭ࡧࠣࡪࡷࡵ࡭ࠡࡲࡤࡸ࡭࠵ࡕࡓࡎ࠽ࠤࢀࢃࠢᰗ").format(e))
            return
        if bstack1ll1l1ll1l1_opy_ is None or not bstack1ll1l1ll1l1_opy_.exists():
            logger.error(bstack1l1111l_opy_ (u"ࠥࡗࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨᰘ").format(bstack1ll1l1ll1l1_opy_))
            return
        if bstack1ll1l1ll1l1_opy_.stat().st_size > bstack111l1111ll1_opy_:
            logger.error(bstack1l1111l_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡶ࡭ࡿ࡫ࠠࡦࡺࡦࡩࡪࡪࡳࠡ࡯ࡤࡼ࡮ࡳࡵ࡮ࠢࡤࡰࡱࡵࡷࡦࡦࠣࡷ࡮ࢀࡥࠡࡱࡩࠤࢀࢃࠢᰙ").format(bstack111l1111ll1_opy_))
            return
        bstack1111llll111_opy_ = bstack1l1111l_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᰚ")
        if bstack111l1111lll_opy_:
            try:
                params = json.loads(bstack111l1111lll_opy_)
                if bstack1l1111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᰛ") in params and params.get(bstack1l1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᰜ")) is True:
                    bstack1111llll111_opy_ = bstack1l1111l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᰝ")
            except Exception as bstack1111lll1lll_opy_:
                logger.error(bstack1l1111l_opy_ (u"ࠤࡍࡗࡔࡔࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡐࡢࡴࡤࡱࡸࡀࠠࡼࡿࠥᰞ").format(bstack1111lll1lll_opy_))
        bstack1111lllllll_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1l1l111ll1l_opy_ import bstack1l11l1l111l_opy_
        if test_framework_state in bstack1l11l1l111l_opy_.bstack111ll11ll11_opy_:
            if bstack1111llll111_opy_ == bstack111l1llllll_opy_:
                bstack1111lllllll_opy_ = True
            bstack1111llll111_opy_ = bstack111ll111111_opy_
        try:
            platform_index = os.environ[bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᰟ")]
            target_dir = os.path.join(bstack11lll11l1ll_opy_, bstack11ll111ll11_opy_ + str(platform_index),
                                      bstack1111llll111_opy_)
            if bstack1111lllllll_opy_:
                target_dir = os.path.join(target_dir, bstack111l11111l1_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1l1111l_opy_ (u"ࠦࡈࡸࡥࡢࡶࡨࡨ࠴ࡼࡥࡳ࡫ࡩ࡭ࡪࡪࠠࡵࡣࡵ࡫ࡪࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᰠ").format(target_dir))
            file_name = os.path.basename(bstack1ll1l1ll1l1_opy_)
            bstack111l11111ll_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack111l11111ll_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack111l1111l11_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack111l1111l11_opy_) + extension)):
                    bstack111l1111l11_opy_ += 1
                bstack111l11111ll_opy_ = os.path.join(target_dir, base_name + str(bstack111l1111l11_opy_) + extension)
            shutil.copy(bstack1ll1l1ll1l1_opy_, bstack111l11111ll_opy_)
            logger.info(bstack1l1111l_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡦࡳࡵ࡯ࡥࡥࠢࡷࡳ࠿ࠦࡻࡾࠤᰡ").format(bstack111l11111ll_opy_))
        except Exception as e:
            logger.error(bstack1l1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡳ࡯ࡷ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࡸࡴࠦࡴࡢࡴࡪࡩࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᰢ").format(e))
            return
        finally:
            if bstack1111lllll11_opy_.startswith(bstack1l1111l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᰣ")) or bstack1111lllll11_opy_.startswith(bstack1l1111l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᰤ")):
                try:
                    if bstack1ll1l1ll1l1_opy_ is not None and bstack1ll1l1ll1l1_opy_.exists():
                        bstack1ll1l1ll1l1_opy_.unlink()
                        logger.debug(bstack1l1111l_opy_ (u"ࠤࡗࡩࡲࡶ࡯ࡳࡣࡵࡽࠥ࡬ࡩ࡭ࡧࠣࡨࡪࡲࡥࡵࡧࡧ࠾ࠥࢁࡽࠣᰥ").format(bstack1ll1l1ll1l1_opy_))
                except Exception as ex:
                    logger.error(bstack1l1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤᰦ").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack1111llll1ll_opy_, stage=STAGE.bstack111ll11111_opy_, bstack1l111l111_opy_=None)
    def bstack11l1l1l1l1_opy_() -> None:
        bstack1l1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡆࡨࡰࡪࡺࡥࡴࠢࡤࡰࡱࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࡸࡪࡲࡷࡪࠦ࡮ࡢ࡯ࡨࡷࠥࡹࡴࡢࡴࡷࠤࡼ࡯ࡴࡩ࡙ࠢࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥࠤ࡫ࡵ࡬࡭ࡱࡺࡩࡩࠦࡢࡺࠢࡤࠤࡳࡻ࡭ࡣࡧࡵࠤ࡮ࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࡶ࡫ࡩࠥࡻࡳࡦࡴࠪࡷࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᰧ")
        bstack111l111111l_opy_ = bstack11lll11111l_opy_()
        pattern = re.compile(bstack1l1111l_opy_ (u"ࡷࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࡢࡤࠬࠤᰨ"))
        if os.path.exists(bstack111l111111l_opy_):
            for item in os.listdir(bstack111l111111l_opy_):
                bstack1111lll1ll1_opy_ = os.path.join(bstack111l111111l_opy_, item)
                if os.path.isdir(bstack1111lll1ll1_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack1111lll1ll1_opy_)
                    except Exception as e:
                        logger.error(bstack1l1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᰩ").format(e))
        else:
            logger.info(bstack1l1111l_opy_ (u"ࠢࡕࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧᰪ").format(bstack111l111111l_opy_))