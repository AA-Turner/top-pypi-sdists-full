# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
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
from bstack_utils.helper import bstack1l11ll1ll1l_opy_
bstack11l1lll1111_opy_ = 100 * 1024 * 1024 # 100 bstack11l1lllllll_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l1l111ll1l_opy_ = bstack1l11ll1ll1l_opy_()
bstack1l11ll1l111_opy_ = bstack11l1ll1_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᜂ")
bstack11ll1l11111_opy_ = bstack11l1ll1_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᜃ")
bstack11ll1l1111l_opy_ = bstack11l1ll1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᜄ")
bstack11ll11llll1_opy_ = bstack11l1ll1_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᜅ")
bstack11l1llll11l_opy_ = bstack11l1ll1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᜆ")
_11l1llll1l1_opy_ = threading.local()
def bstack11ll1ll1111_opy_(test_framework_state, test_hook_state):
    bstack11l1ll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡨࡸࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡸࡪࡹࡴࠡࡧࡹࡩࡳࡺࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡࡵࡷࡳࡷࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࡕࡪ࡬ࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡴࡪࡲࡹࡱࡪࠠࡣࡧࠣࡧࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡴࡩࡧࠣࡩࡻ࡫࡮ࡵࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣࠬࡸࡻࡣࡩࠢࡤࡷࠥࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶࠬࠎࠥࠦࠠࠡࡤࡨࡪࡴࡸࡥࠡࡣࡱࡽࠥ࡬ࡩ࡭ࡧࠣࡹࡵࡲ࡯ࡢࡦࡶࠤࡴࡩࡣࡶࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᜇ")
    _11l1llll1l1_opy_.test_framework_state = test_framework_state
    _11l1llll1l1_opy_.test_hook_state = test_hook_state
def bstack11l1lll1ll1_opy_():
    bstack11l1ll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡕࡩࡹࡸࡩࡦࡸࡨࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷࡩࡸࡺࠠࡦࡸࡨࡲࡹࠦࡳࡵࡣࡷࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭ࡸࡥࡢࡦ࠰ࡰࡴࡩࡡ࡭ࠢࡶࡸࡴࡸࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡤࠤࡹࡻࡰ࡭ࡧࠣࠬࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨ࠰ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࠩࠡࡱࡵࠤ࠭ࡔ࡯࡯ࡧ࠯ࠤࡓࡵ࡮ࡦࠫࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡷࡪࡺ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᜈ")
    return (
        getattr(_11l1llll1l1_opy_, bstack11l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࠪᜉ"), None),
        getattr(_11l1llll1l1_opy_, bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪ࠭ᜊ"), None)
    )
class bstack11l1l1lll_opy_:
    bstack11l1ll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡌࡩ࡭ࡧࡘࡴࡱࡵࡡࡥࡧࡵࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡢ࡮࡬ࡸࡾࠦࡴࡰࠢࡸࡴࡱࡵࡡࡥࠢࡤࡲࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡥࡥࡸ࡫ࡤࠡࡱࡱࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࡋࡷࠤࡸࡻࡰࡱࡱࡵࡸࡸࠦࡢࡰࡶ࡫ࠤࡱࡵࡣࡢ࡮ࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹࠠࡢࡰࡧࠤࡍ࡚ࡔࡑ࠱ࡋࡘ࡙ࡖࡓࠡࡗࡕࡐࡸ࠲ࠠࡢࡰࡧࠤࡨࡵࡰࡪࡧࡶࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪࠦࡩ࡯ࡶࡲࠤࡦࠦࡤࡦࡵ࡬࡫ࡳࡧࡴࡦࡦࠍࠤࠥࠦࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡻ࡮ࡺࡨࡪࡰࠣࡸ࡭࡫ࠠࡶࡵࡨࡶࠬࡹࠠࡩࡱࡰࡩࠥ࡬࡯࡭ࡦࡨࡶࠥࡻ࡮ࡥࡧࡵࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࡍ࡫ࠦࡡ࡯ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡲࡤࡶࡦࡳࡥࡵࡧࡵࠤ࠭࡯࡮ࠡࡌࡖࡓࡓࠦࡦࡰࡴࡰࡥࡹ࠯ࠠࡪࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࡧ࡮ࡥࠢࡦࡳࡳࡺࡡࡪࡰࡶࠤࡦࠦࡴࡳࡷࡷ࡬ࡾࠦࡶࡢ࡮ࡸࡩࠏࠦࠠࠡࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡯ࡪࡿࠠࠣࡤࡸ࡭ࡱࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥ࠰ࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫ࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡲ࡯ࡥࡨ࡫ࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡧࡱ࡯ࡨࡪࡸ࠻ࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨ࠰ࠏࠦࠠࠡࠢ࡬ࡸࠥࡪࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡵࡦࠡࡣࡧࡨࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢ࡬ࡷࠥࡧࠠࡷࡱ࡬ࡨࠥࡳࡥࡵࡪࡲࡨ⠙࡯ࡴࠡࡪࡤࡲࡩࡲࡥࡴࠢࡤࡰࡱࠦࡥࡳࡴࡲࡶࡸࠦࡧࡳࡣࡦࡩ࡫ࡻ࡬࡭ࡻࠣࡦࡾࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠊࠡࠢࠣࠤࡹ࡮ࡥ࡮ࠢࡤࡲࡩࠦࡳࡪ࡯ࡳࡰࡾࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡸ࡭ࡸ࡯ࡸ࡫ࡱ࡫ࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࡴ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᜋ")
    @staticmethod
    def upload_attachment(bstack11l1lll11l1_opy_: str, *bstack11l1llll111_opy_) -> None:
        if not bstack11l1lll11l1_opy_ or not bstack11l1lll11l1_opy_.strip():
            logger.error(bstack11l1ll1_opy_ (u"ࠨࡡࡥࡦࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡒࡵࡳࡻ࡯ࡤࡦࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࠦࡩࡴࠢࡨࡱࡵࡺࡹࠡࡱࡵࠤࡓࡵ࡮ࡦ࠰ࠥᜌ"))
            return
        bstack11l1llllll1_opy_ = bstack11l1llll111_opy_[0] if bstack11l1llll111_opy_ and len(bstack11l1llll111_opy_) > 0 else None
        bstack11l1lll111l_opy_ = None
        test_framework_state, test_hook_state = bstack11l1lll1ll1_opy_()
        try:
            if bstack11l1lll11l1_opy_.startswith(bstack11l1ll1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᜍ")) or bstack11l1lll11l1_opy_.startswith(bstack11l1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᜎ")):
                logger.debug(bstack11l1ll1_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡪࡵࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡪࠠࡢࡵ࡙ࠣࡗࡒ࠻ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠤᜏ"))
                url = bstack11l1lll11l1_opy_
                bstack11l1lll1lll_opy_ = str(uuid.uuid4())
                bstack11l1lll1l11_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11l1lll1l11_opy_ or not bstack11l1lll1l11_opy_.strip():
                    bstack11l1lll1l11_opy_ = bstack11l1lll1lll_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack11l1ll1_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࡢࠦᜐ") + bstack11l1lll1lll_opy_ + bstack11l1ll1_opy_ (u"ࠦࡤࠨᜑ"),
                                                        suffix=bstack11l1ll1_opy_ (u"ࠧࡥࠢᜒ") + bstack11l1lll1l11_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack11l1ll1_opy_ (u"࠭ࡷࡣࠩᜓ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11l1lll111l_opy_ = Path(temp_file.name)
                logger.debug(bstack11l1ll1_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤ࡫࡯࡬ࡦࠢࡷࡳࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࡮ࡲࡧࡦࡺࡩࡰࡰ࠽ࠤࢀࢃ᜔ࠢ").format(bstack11l1lll111l_opy_))
            else:
                bstack11l1lll111l_opy_ = Path(bstack11l1lll11l1_opy_)
                logger.debug(bstack11l1ll1_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡩࡴࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡩࠦࡡࡴࠢ࡯ࡳࡨࡧ࡬ࠡࡨ࡬ࡰࡪࡀࠠࡼࡿ᜕ࠥ").format(bstack11l1lll111l_opy_))
        except Exception as e:
            logger.error(bstack11l1ll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡵࡢࡵࡣ࡬ࡲࠥ࡬ࡩ࡭ࡧࠣࡪࡷࡵ࡭ࠡࡲࡤࡸ࡭࠵ࡕࡓࡎ࠽ࠤࢀࢃࠢ᜖").format(e))
            return
        if bstack11l1lll111l_opy_ is None or not bstack11l1lll111l_opy_.exists():
            logger.error(bstack11l1ll1_opy_ (u"ࠥࡗࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨ᜗").format(bstack11l1lll111l_opy_))
            return
        if bstack11l1lll111l_opy_.stat().st_size > bstack11l1lll1111_opy_:
            logger.error(bstack11l1ll1_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡶ࡭ࡿ࡫ࠠࡦࡺࡦࡩࡪࡪࡳࠡ࡯ࡤࡼ࡮ࡳࡵ࡮ࠢࡤࡰࡱࡵࡷࡦࡦࠣࡷ࡮ࢀࡥࠡࡱࡩࠤࢀࢃࠢ᜘").format(bstack11l1lll1111_opy_))
            return
        bstack11l1lll1l1l_opy_ = bstack11l1ll1_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣ᜙")
        if bstack11l1llllll1_opy_:
            try:
                params = json.loads(bstack11l1llllll1_opy_)
                if bstack11l1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣ᜚") in params and params.get(bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤ᜛")) is True:
                    bstack11l1lll1l1l_opy_ = bstack11l1ll1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧ᜜")
            except Exception as bstack11l1lllll11_opy_:
                logger.error(bstack11l1ll1_opy_ (u"ࠤࡍࡗࡔࡔࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡐࡢࡴࡤࡱࡸࡀࠠࡼࡿࠥ᜝").format(bstack11l1lllll11_opy_))
        bstack11l1llll1ll_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1ll111lllll_opy_ import bstack1ll1l1ll1l1_opy_
        if test_framework_state in bstack1ll1l1ll1l1_opy_.bstack11llll1llll_opy_:
            if bstack11l1lll1l1l_opy_ == bstack11ll1l1111l_opy_:
                bstack11l1llll1ll_opy_ = True
            bstack11l1lll1l1l_opy_ = bstack11ll11llll1_opy_
        try:
            platform_index = os.environ[bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ᜞")]
            target_dir = os.path.join(bstack1l1l111ll1l_opy_, bstack1l11ll1l111_opy_ + str(platform_index),
                                      bstack11l1lll1l1l_opy_)
            if bstack11l1llll1ll_opy_:
                target_dir = os.path.join(target_dir, bstack11l1llll11l_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack11l1ll1_opy_ (u"ࠦࡈࡸࡥࡢࡶࡨࡨ࠴ࡼࡥࡳ࡫ࡩ࡭ࡪࡪࠠࡵࡣࡵ࡫ࡪࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᜟ").format(target_dir))
            file_name = os.path.basename(bstack11l1lll111l_opy_)
            bstack11ll111111l_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11ll111111l_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11ll1111111_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11ll1111111_opy_) + extension)):
                    bstack11ll1111111_opy_ += 1
                bstack11ll111111l_opy_ = os.path.join(target_dir, base_name + str(bstack11ll1111111_opy_) + extension)
            shutil.copy(bstack11l1lll111l_opy_, bstack11ll111111l_opy_)
            logger.info(bstack11l1ll1_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡦࡳࡵ࡯ࡥࡥࠢࡷࡳ࠿ࠦࡻࡾࠤᜠ").format(bstack11ll111111l_opy_))
        except Exception as e:
            logger.error(bstack11l1ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡳ࡯ࡷ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࡸࡴࠦࡴࡢࡴࡪࡩࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᜡ").format(e))
            return
        finally:
            if bstack11l1lll11l1_opy_.startswith(bstack11l1ll1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᜢ")) or bstack11l1lll11l1_opy_.startswith(bstack11l1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᜣ")):
                try:
                    if bstack11l1lll111l_opy_ is not None and bstack11l1lll111l_opy_.exists():
                        bstack11l1lll111l_opy_.unlink()
                        logger.debug(bstack11l1ll1_opy_ (u"ࠤࡗࡩࡲࡶ࡯ࡳࡣࡵࡽࠥ࡬ࡩ࡭ࡧࠣࡨࡪࡲࡥࡵࡧࡧ࠾ࠥࢁࡽࠣᜤ").format(bstack11l1lll111l_opy_))
                except Exception as ex:
                    logger.error(bstack11l1ll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤᜥ").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack11l1lllll1l_opy_, stage=STAGE.bstack11lll1l1l1_opy_, bstack1ll1l111l_opy_=None)
    def bstack11l1l11lll_opy_() -> None:
        bstack11l1ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡆࡨࡰࡪࡺࡥࡴࠢࡤࡰࡱࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࡸࡪࡲࡷࡪࠦ࡮ࡢ࡯ࡨࡷࠥࡹࡴࡢࡴࡷࠤࡼ࡯ࡴࡩ࡙ࠢࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥࠤ࡫ࡵ࡬࡭ࡱࡺࡩࡩࠦࡢࡺࠢࡤࠤࡳࡻ࡭ࡣࡧࡵࠤ࡮ࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࡶ࡫ࡩࠥࡻࡳࡦࡴࠪࡷࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᜦ")
        bstack11l1ll1llll_opy_ = bstack1l11ll1ll1l_opy_()
        pattern = re.compile(bstack11l1ll1_opy_ (u"ࡷࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࡢࡤࠬࠤᜧ"))
        if os.path.exists(bstack11l1ll1llll_opy_):
            for item in os.listdir(bstack11l1ll1llll_opy_):
                bstack11l1lll11ll_opy_ = os.path.join(bstack11l1ll1llll_opy_, item)
                if os.path.isdir(bstack11l1lll11ll_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11l1lll11ll_opy_)
                    except Exception as e:
                        logger.error(bstack11l1ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᜨ").format(e))
        else:
            logger.info(bstack11l1ll1_opy_ (u"ࠢࡕࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧᜩ").format(bstack11l1ll1llll_opy_))