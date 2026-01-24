# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
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
from bstack_utils.helper import bstack1l1l1111l11_opy_
bstack11l1llll1ll_opy_ = 100 * 1024 * 1024 # 100 bstack11ll1111111_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l11ll111ll_opy_ = bstack1l1l1111l11_opy_()
bstack1l1l11l11l1_opy_ = bstack1l1111_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦ᛼")
bstack11ll11lllll_opy_ = bstack1l1111_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣ᛽")
bstack11ll11lll1l_opy_ = bstack1l1111_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥ᛾")
bstack11ll1l11l11_opy_ = bstack1l1111_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥ᛿")
bstack11l1llll111_opy_ = bstack1l1111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᜀ")
_11l1lllll11_opy_ = threading.local()
def bstack11llll11lll_opy_(test_framework_state, test_hook_state):
    bstack1l1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡖࡩࡹࠦࡴࡩࡧࠣࡧࡺࡸࡲࡦࡰࡷࠤࡹ࡫ࡳࡵࠢࡨࡺࡪࡴࡴࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡸ࡭ࡸࡥࡢࡦ࠰ࡰࡴࡩࡡ࡭ࠢࡶࡸࡴࡸࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࡖ࡫࡭ࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡵ࡫ࡳࡺࡲࡤࠡࡤࡨࠤࡨࡧ࡬࡭ࡧࡧࠤࡧࡿࠠࡵࡪࡨࠤࡪࡼࡥ࡯ࡶࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࠭ࡹࡵࡤࡪࠣࡥࡸࠦࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠭ࠏࠦࠠࠡࠢࡥࡩ࡫ࡵࡲࡦࠢࡤࡲࡾࠦࡦࡪ࡮ࡨࠤࡺࡶ࡬ࡰࡣࡧࡷࠥࡵࡣࡤࡷࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᜁ")
    _11l1lllll11_opy_.test_framework_state = test_framework_state
    _11l1lllll11_opy_.test_hook_state = test_hook_state
def bstack11l1llll11l_opy_():
    bstack1l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡖࡪࡺࡲࡪࡧࡹࡩࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡸࡪࡹࡴࠡࡧࡹࡩࡳࡺࠠࡴࡶࡤࡸࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡲࡦࡣࡧ࠱ࡱࡵࡣࡢ࡮ࠣࡷࡹࡵࡲࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡥࠥࡺࡵࡱ࡮ࡨࠤ࠭ࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩ࠱ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࠪࠢࡲࡶࠥ࠮ࡎࡰࡰࡨ࠰ࠥࡔ࡯࡯ࡧࠬࠤ࡮࡬ࠠ࡯ࡱࡷࠤࡸ࡫ࡴ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᜂ")
    return (
        getattr(_11l1lllll11_opy_, bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࠫᜃ"), None),
        getattr(_11l1lllll11_opy_, bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࠧᜄ"), None)
    )
class bstack11ll1lll1_opy_:
    bstack1l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡆࡪ࡮ࡨ࡙ࡵࡲ࡯ࡢࡦࡨࡶࠥࡶࡲࡰࡸ࡬ࡨࡪࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࡣ࡯࡭ࡹࡿࠠࡵࡱࠣࡹࡵࡲ࡯ࡢࡦࠣࡥࡳࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡦࡦࡹࡥࡥࠢࡲࡲࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࡌࡸࠥࡹࡵࡱࡲࡲࡶࡹࡹࠠࡣࡱࡷ࡬ࠥࡲ࡯ࡤࡣ࡯ࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳࠡࡣࡱࡨࠥࡎࡔࡕࡒ࠲ࡌ࡙࡚ࡐࡔࠢࡘࡖࡑࡹࠬࠡࡣࡱࡨࠥࡩ࡯ࡱ࡫ࡨࡷࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫ࠠࡪࡰࡷࡳࠥࡧࠠࡥࡧࡶ࡭࡬ࡴࡡࡵࡧࡧࠎࠥࠦࠠࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡼ࡯ࡴࡩ࡫ࡱࠤࡹ࡮ࡥࠡࡷࡶࡩࡷ࠭ࡳࠡࡪࡲࡱࡪࠦࡦࡰ࡮ࡧࡩࡷࠦࡵ࡯ࡦࡨࡶࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࡎ࡬ࠠࡢࡰࠣࡳࡵࡺࡩࡰࡰࡤࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡳࡥࡷࡧ࡭ࡦࡶࡨࡶࠥ࠮ࡩ࡯ࠢࡍࡗࡔࡔࠠࡧࡱࡵࡱࡦࡺࠩࠡ࡫ࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡡ࡯ࡦࠣࡧࡴࡴࡴࡢ࡫ࡱࡷࠥࡧࠠࡵࡴࡸࡸ࡭ࡿࠠࡷࡣ࡯ࡹࡪࠐࠠࠡࠢࠣࡪࡴࡸࠠࡵࡪࡨࠤࡰ࡫ࡹࠡࠤࡥࡹ࡮ࡲࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦ࠱ࠦࡴࡩࡧࠣࡪ࡮ࡲࡥࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡳࡰࡦࡩࡥࡥࠢ࡬ࡲࠥࡺࡨࡦࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡨࡲࡰࡩ࡫ࡲ࠼ࠢࡲࡸ࡭࡫ࡲࡸ࡫ࡶࡩ࠱ࠐࠠࠡࠢࠣ࡭ࡹࠦࡤࡦࡨࡤࡹࡱࡺࡳࠡࡶࡲࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣ࠰ࠍࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡼࡥࡳࡵ࡬ࡳࡳࠦ࡯ࡧࠢࡤࡨࡩࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣ࡭ࡸࠦࡡࠡࡸࡲ࡭ࡩࠦ࡭ࡦࡶ࡫ࡳࡩ⠚ࡩࡵࠢ࡫ࡥࡳࡪ࡬ࡦࡵࠣࡥࡱࡲࠠࡦࡴࡵࡳࡷࡹࠠࡨࡴࡤࡧࡪ࡬ࡵ࡭࡮ࡼࠤࡧࡿࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠋࠢࠣࠤࠥࡺࡨࡦ࡯ࠣࡥࡳࡪࠠࡴ࡫ࡰࡴࡱࡿࠠࡳࡧࡷࡹࡷࡴࡩ࡯ࡩࠣࡻ࡮ࡺࡨࡰࡷࡷࠤࡹ࡮ࡲࡰࡹ࡬ࡲ࡬ࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡵ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᜅ")
    @staticmethod
    def upload_attachment(bstack11ll1111l11_opy_: str, *bstack11l1lll1ll1_opy_) -> None:
        if not bstack11ll1111l11_opy_ or not bstack11ll1111l11_opy_.strip():
            logger.error(bstack1l1111_opy_ (u"ࠢࡢࡦࡧࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡓࡶࡴࡼࡩࡥࡧࡧࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࠠࡪࡵࠣࡩࡲࡶࡴࡺࠢࡲࡶࠥࡔ࡯࡯ࡧ࠱ࠦᜆ"))
            return
        bstack11l1lll1l1l_opy_ = bstack11l1lll1ll1_opy_[0] if bstack11l1lll1ll1_opy_ and len(bstack11l1lll1ll1_opy_) > 0 else None
        bstack11l1lll1lll_opy_ = None
        test_framework_state, test_hook_state = bstack11l1llll11l_opy_()
        try:
            if bstack11ll1111l11_opy_.startswith(bstack1l1111_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᜇ")) or bstack11ll1111l11_opy_.startswith(bstack1l1111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᜈ")):
                logger.debug(bstack1l1111_opy_ (u"ࠥࡔࡦࡺࡨࠡ࡫ࡶࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡤࠡࡣࡶࠤ࡚ࡘࡌ࠼ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠥᜉ"))
                url = bstack11ll1111l11_opy_
                bstack11l1llll1l1_opy_ = str(uuid.uuid4())
                bstack11ll11111ll_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11ll11111ll_opy_ or not bstack11ll11111ll_opy_.strip():
                    bstack11ll11111ll_opy_ = bstack11l1llll1l1_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1l1111_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࡣࠧᜊ") + bstack11l1llll1l1_opy_ + bstack1l1111_opy_ (u"ࠧࡥࠢᜋ"),
                                                        suffix=bstack1l1111_opy_ (u"ࠨ࡟ࠣᜌ") + bstack11ll11111ll_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1l1111_opy_ (u"ࠧࡸࡤࠪᜍ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11l1lll1lll_opy_ = Path(temp_file.name)
                logger.debug(bstack1l1111_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥ࡬ࡩ࡭ࡧࠣࡸࡴࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢ࡯ࡳࡨࡧࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᜎ").format(bstack11l1lll1lll_opy_))
            else:
                bstack11l1lll1lll_opy_ = Path(bstack11ll1111l11_opy_)
                logger.debug(bstack1l1111_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡪࡵࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡪࠠࡢࡵࠣࡰࡴࡩࡡ࡭ࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠦᜏ").format(bstack11l1lll1lll_opy_))
        except Exception as e:
            logger.error(bstack1l1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡯ࡣࡶࡤ࡭ࡳࠦࡦࡪ࡮ࡨࠤ࡫ࡸ࡯࡮ࠢࡳࡥࡹ࡮࠯ࡖࡔࡏ࠾ࠥࢁࡽࠣᜐ").format(e))
            return
        if bstack11l1lll1lll_opy_ is None or not bstack11l1lll1lll_opy_.exists():
            logger.error(bstack1l1111_opy_ (u"ࠦࡘࡵࡵࡳࡥࡨࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠢᜑ").format(bstack11l1lll1lll_opy_))
            return
        if bstack11l1lll1lll_opy_.stat().st_size > bstack11l1llll1ll_opy_:
            logger.error(bstack1l1111_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡷ࡮ࢀࡥࠡࡧࡻࡧࡪ࡫ࡤࡴࠢࡰࡥࡽ࡯࡭ࡶ࡯ࠣࡥࡱࡲ࡯ࡸࡧࡧࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࢁࡽࠣᜒ").format(bstack11l1llll1ll_opy_))
            return
        bstack11l1llllll1_opy_ = bstack1l1111_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᜓ")
        if bstack11l1lll1l1l_opy_:
            try:
                params = json.loads(bstack11l1lll1l1l_opy_)
                if bstack1l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤ᜔") in params and params.get(bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶ᜕ࠥ")) is True:
                    bstack11l1llllll1_opy_ = bstack1l1111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨ᜖")
            except Exception as bstack11l1lllll1l_opy_:
                logger.error(bstack1l1111_opy_ (u"ࠥࡎࡘࡕࡎࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡑࡣࡵࡥࡲࡹ࠺ࠡࡽࢀࠦ᜗").format(bstack11l1lllll1l_opy_))
        bstack11l1lllllll_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1ll11ll1l11_opy_ import bstack1ll1l1lllll_opy_
        if test_framework_state in bstack1ll1l1lllll_opy_.bstack11lll1ll1ll_opy_:
            if bstack11l1llllll1_opy_ == bstack11ll11lll1l_opy_:
                bstack11l1lllllll_opy_ = True
            bstack11l1llllll1_opy_ = bstack11ll1l11l11_opy_
        try:
            platform_index = os.environ[bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ᜘")]
            target_dir = os.path.join(bstack1l11ll111ll_opy_, bstack1l1l11l11l1_opy_ + str(platform_index),
                                      bstack11l1llllll1_opy_)
            if bstack11l1lllllll_opy_:
                target_dir = os.path.join(target_dir, bstack11l1llll111_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1l1111_opy_ (u"ࠧࡉࡲࡦࡣࡷࡩࡩ࠵ࡶࡦࡴ࡬ࡪ࡮࡫ࡤࠡࡶࡤࡶ࡬࡫ࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣ᜙").format(target_dir))
            file_name = os.path.basename(bstack11l1lll1lll_opy_)
            bstack11l1lll11ll_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11l1lll11ll_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11ll11111l1_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11ll11111l1_opy_) + extension)):
                    bstack11ll11111l1_opy_ += 1
                bstack11l1lll11ll_opy_ = os.path.join(target_dir, base_name + str(bstack11ll11111l1_opy_) + extension)
            shutil.copy(bstack11l1lll1lll_opy_, bstack11l1lll11ll_opy_)
            logger.info(bstack1l1111_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡧࡴࡶࡩࡦࡦࠣࡸࡴࡀࠠࡼࡿࠥ᜚").format(bstack11l1lll11ll_opy_))
        except Exception as e:
            logger.error(bstack1l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡭ࡰࡸ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࡹࡵࠠࡵࡣࡵ࡫ࡪࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢ᜛").format(e))
            return
        finally:
            if bstack11ll1111l11_opy_.startswith(bstack1l1111_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ᜜")) or bstack11ll1111l11_opy_.startswith(bstack1l1111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ᜝")):
                try:
                    if bstack11l1lll1lll_opy_ is not None and bstack11l1lll1lll_opy_.exists():
                        bstack11l1lll1lll_opy_.unlink()
                        logger.debug(bstack1l1111_opy_ (u"ࠥࡘࡪࡳࡰࡰࡴࡤࡶࡾࠦࡦࡪ࡮ࡨࠤࡩ࡫࡬ࡦࡶࡨࡨ࠿ࠦࡻࡾࠤ᜞").format(bstack11l1lll1lll_opy_))
                except Exception as ex:
                    logger.error(bstack1l1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠥᜟ").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack11ll111111l_opy_, stage=STAGE.bstack1111lll11_opy_, bstack1l1l111l_opy_=None)
    def bstack1llll1l1ll_opy_() -> None:
        bstack1l1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡇࡩࡱ࡫ࡴࡦࡵࠣࡥࡱࡲࠠࡧࡱ࡯ࡨࡪࡸࡳࠡࡹ࡫ࡳࡸ࡫ࠠ࡯ࡣࡰࡩࡸࠦࡳࡵࡣࡵࡸࠥࡽࡩࡵࡪ࡚ࠣࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦࠥ࡬࡯࡭࡮ࡲࡻࡪࡪࠠࡣࡻࠣࡥࠥࡴࡵ࡮ࡤࡨࡶࠥ࡯࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷ࡬ࡪࠦࡵࡴࡧࡵࠫࡸࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᜠ")
        bstack11l1lll1l11_opy_ = bstack1l1l1111l11_opy_()
        pattern = re.compile(bstack1l1111_opy_ (u"ࡸࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳࡜ࡥ࠭ࠥᜡ"))
        if os.path.exists(bstack11l1lll1l11_opy_):
            for item in os.listdir(bstack11l1lll1l11_opy_):
                bstack11l1lll11l1_opy_ = os.path.join(bstack11l1lll1l11_opy_, item)
                if os.path.isdir(bstack11l1lll11l1_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11l1lll11l1_opy_)
                    except Exception as e:
                        logger.error(bstack1l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᜢ").format(e))
        else:
            logger.info(bstack1l1111_opy_ (u"ࠣࡖ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨᜣ").format(bstack11l1lll1l11_opy_))