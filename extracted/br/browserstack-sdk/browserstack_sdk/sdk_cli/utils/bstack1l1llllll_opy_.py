# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
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
from bstack_utils.helper import bstack11ll11l1lll_opy_
bstack1111llll1ll_opy_ = 100 * 1024 * 1024 # 100 bstack111l111111l_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack11ll11l1ll1_opy_ = bstack11ll11l1lll_opy_()
bstack11ll1ll1l11_opy_ = bstack111ll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᰒ")
bstack111ll1111ll_opy_ = bstack111ll_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᰓ")
bstack111l1llll11_opy_ = bstack111ll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᰔ")
bstack111l1lllll1_opy_ = bstack111ll_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᰕ")
bstack111l1111111_opy_ = bstack111ll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᰖ")
_1111lll1l11_opy_ = threading.local()
def bstack111ll1ll1l1_opy_(test_framework_state, test_hook_state):
    bstack111ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡖࡩࡹࠦࡴࡩࡧࠣࡧࡺࡸࡲࡦࡰࡷࠤࡹ࡫ࡳࡵࠢࡨࡺࡪࡴࡴࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡸ࡭ࡸࡥࡢࡦ࠰ࡰࡴࡩࡡ࡭ࠢࡶࡸࡴࡸࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࡖ࡫࡭ࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡵ࡫ࡳࡺࡲࡤࠡࡤࡨࠤࡨࡧ࡬࡭ࡧࡧࠤࡧࡿࠠࡵࡪࡨࠤࡪࡼࡥ࡯ࡶࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࠭ࡹࡵࡤࡪࠣࡥࡸࠦࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠭ࠏࠦࠠࠡࠢࡥࡩ࡫ࡵࡲࡦࠢࡤࡲࡾࠦࡦࡪ࡮ࡨࠤࡺࡶ࡬ࡰࡣࡧࡷࠥࡵࡣࡤࡷࡵ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᰗ")
    _1111lll1l11_opy_.test_framework_state = test_framework_state
    _1111lll1l11_opy_.test_hook_state = test_hook_state
def bstack1111lllll1l_opy_():
    bstack111ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡖࡪࡺࡲࡪࡧࡹࡩࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡸࡪࡹࡴࠡࡧࡹࡩࡳࡺࠠࡴࡶࡤࡸࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡲࡦࡣࡧ࠱ࡱࡵࡣࡢ࡮ࠣࡷࡹࡵࡲࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡥࠥࡺࡵࡱ࡮ࡨࠤ࠭ࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩ࠱ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࠪࠢࡲࡶࠥ࠮ࡎࡰࡰࡨ࠰ࠥࡔ࡯࡯ࡧࠬࠤ࡮࡬ࠠ࡯ࡱࡷࠤࡸ࡫ࡴ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᰘ")
    return (
        getattr(_1111lll1l11_opy_, bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࠫᰙ"), None),
        getattr(_1111lll1l11_opy_, bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࠧᰚ"), None)
    )
class bstack1l11111ll_opy_:
    bstack111ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡆࡪ࡮ࡨ࡙ࡵࡲ࡯ࡢࡦࡨࡶࠥࡶࡲࡰࡸ࡬ࡨࡪࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࡣ࡯࡭ࡹࡿࠠࡵࡱࠣࡹࡵࡲ࡯ࡢࡦࠣࡥࡳࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡦࡦࡹࡥࡥࠢࡲࡲࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࡌࡸࠥࡹࡵࡱࡲࡲࡶࡹࡹࠠࡣࡱࡷ࡬ࠥࡲ࡯ࡤࡣ࡯ࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳࠡࡣࡱࡨࠥࡎࡔࡕࡒ࠲ࡌ࡙࡚ࡐࡔࠢࡘࡖࡑࡹࠬࠡࡣࡱࡨࠥࡩ࡯ࡱ࡫ࡨࡷࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫ࠠࡪࡰࡷࡳࠥࡧࠠࡥࡧࡶ࡭࡬ࡴࡡࡵࡧࡧࠎࠥࠦࠠࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡼ࡯ࡴࡩ࡫ࡱࠤࡹ࡮ࡥࠡࡷࡶࡩࡷ࠭ࡳࠡࡪࡲࡱࡪࠦࡦࡰ࡮ࡧࡩࡷࠦࡵ࡯ࡦࡨࡶࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࡎ࡬ࠠࡢࡰࠣࡳࡵࡺࡩࡰࡰࡤࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡳࡥࡷࡧ࡭ࡦࡶࡨࡶࠥ࠮ࡩ࡯ࠢࡍࡗࡔࡔࠠࡧࡱࡵࡱࡦࡺࠩࠡ࡫ࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡡ࡯ࡦࠣࡧࡴࡴࡴࡢ࡫ࡱࡷࠥࡧࠠࡵࡴࡸࡸ࡭ࡿࠠࡷࡣ࡯ࡹࡪࠐࠠࠡࠢࠣࡪࡴࡸࠠࡵࡪࡨࠤࡰ࡫ࡹࠡࠤࡥࡹ࡮ࡲࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦ࠱ࠦࡴࡩࡧࠣࡪ࡮ࡲࡥࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡳࡰࡦࡩࡥࡥࠢ࡬ࡲࠥࡺࡨࡦࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡨࡲࡰࡩ࡫ࡲ࠼ࠢࡲࡸ࡭࡫ࡲࡸ࡫ࡶࡩ࠱ࠐࠠࠡࠢࠣ࡭ࡹࠦࡤࡦࡨࡤࡹࡱࡺࡳࠡࡶࡲࠤ࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣ࠰ࠍࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡼࡥࡳࡵ࡬ࡳࡳࠦ࡯ࡧࠢࡤࡨࡩࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣ࡭ࡸࠦࡡࠡࡸࡲ࡭ࡩࠦ࡭ࡦࡶ࡫ࡳࡩ⠚ࡩࡵࠢ࡫ࡥࡳࡪ࡬ࡦࡵࠣࡥࡱࡲࠠࡦࡴࡵࡳࡷࡹࠠࡨࡴࡤࡧࡪ࡬ࡵ࡭࡮ࡼࠤࡧࡿࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠋࠢࠣࠤࠥࡺࡨࡦ࡯ࠣࡥࡳࡪࠠࡴ࡫ࡰࡴࡱࡿࠠࡳࡧࡷࡹࡷࡴࡩ࡯ࡩࠣࡻ࡮ࡺࡨࡰࡷࡷࠤࡹ࡮ࡲࡰࡹ࡬ࡲ࡬ࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡵ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᰛ")
    @staticmethod
    def upload_attachment(bstack111l11111ll_opy_: str, *bstack1111lll11ll_opy_) -> None:
        if not bstack111l11111ll_opy_ or not bstack111l11111ll_opy_.strip():
            logger.error(bstack111ll_opy_ (u"ࠢࡢࡦࡧࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡓࡶࡴࡼࡩࡥࡧࡧࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࠠࡪࡵࠣࡩࡲࡶࡴࡺࠢࡲࡶࠥࡔ࡯࡯ࡧ࠱ࠦᰜ"))
            return
        bstack1111llll1l1_opy_ = bstack1111lll11ll_opy_[0] if bstack1111lll11ll_opy_ and len(bstack1111lll11ll_opy_) > 0 else None
        bstack1ll1l1ll1l1_opy_ = None
        test_framework_state, test_hook_state = bstack1111lllll1l_opy_()
        try:
            if bstack111l11111ll_opy_.startswith(bstack111ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᰝ")) or bstack111l11111ll_opy_.startswith(bstack111ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᰞ")):
                logger.debug(bstack111ll_opy_ (u"ࠥࡔࡦࡺࡨࠡ࡫ࡶࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡤࠡࡣࡶࠤ࡚ࡘࡌ࠼ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠥᰟ"))
                url = bstack111l11111ll_opy_
                bstack1111llll11l_opy_ = str(uuid.uuid4())
                bstack1111llllll1_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack1111llllll1_opy_ or not bstack1111llllll1_opy_.strip():
                    bstack1111llllll1_opy_ = bstack1111llll11l_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack111ll_opy_ (u"ࠦࡺࡶ࡬ࡰࡣࡧࡣࠧᰠ") + bstack1111llll11l_opy_ + bstack111ll_opy_ (u"ࠧࡥࠢᰡ"),
                                                        suffix=bstack111ll_opy_ (u"ࠨ࡟ࠣᰢ") + bstack1111llllll1_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack111ll_opy_ (u"ࠧࡸࡤࠪᰣ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack1ll1l1ll1l1_opy_ = Path(temp_file.name)
                logger.debug(bstack111ll_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥ࡬ࡩ࡭ࡧࠣࡸࡴࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢ࡯ࡳࡨࡧࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᰤ").format(bstack1ll1l1ll1l1_opy_))
            else:
                bstack1ll1l1ll1l1_opy_ = Path(bstack111l11111ll_opy_)
                logger.debug(bstack111ll_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡪࡵࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡪࠠࡢࡵࠣࡰࡴࡩࡡ࡭ࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠦᰥ").format(bstack1ll1l1ll1l1_opy_))
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡯ࡣࡶࡤ࡭ࡳࠦࡦࡪ࡮ࡨࠤ࡫ࡸ࡯࡮ࠢࡳࡥࡹ࡮࠯ࡖࡔࡏ࠾ࠥࢁࡽࠣᰦ").format(e))
            return
        if bstack1ll1l1ll1l1_opy_ is None or not bstack1ll1l1ll1l1_opy_.exists():
            logger.error(bstack111ll_opy_ (u"ࠦࡘࡵࡵࡳࡥࡨࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠢᰧ").format(bstack1ll1l1ll1l1_opy_))
            return
        if bstack1ll1l1ll1l1_opy_.stat().st_size > bstack1111llll1ll_opy_:
            logger.error(bstack111ll_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡷ࡮ࢀࡥࠡࡧࡻࡧࡪ࡫ࡤࡴࠢࡰࡥࡽ࡯࡭ࡶ࡯ࠣࡥࡱࡲ࡯ࡸࡧࡧࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࢁࡽࠣᰨ").format(bstack1111llll1ll_opy_))
            return
        bstack1111lllll11_opy_ = bstack111ll_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᰩ")
        if bstack1111llll1l1_opy_:
            try:
                params = json.loads(bstack1111llll1l1_opy_)
                if bstack111ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᰪ") in params and params.get(bstack111ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᰫ")) is True:
                    bstack1111lllll11_opy_ = bstack111ll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᰬ")
            except Exception as bstack111l11111l1_opy_:
                logger.error(bstack111ll_opy_ (u"ࠥࡎࡘࡕࡎࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡨࡶࡷࡵࡲࠡ࡫ࡱࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡑࡣࡵࡥࡲࡹ࠺ࠡࡽࢀࠦᰭ").format(bstack111l11111l1_opy_))
        bstack1111lll1l1l_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1l1l111111l_opy_ import bstack1l11lll11l1_opy_
        if test_framework_state in bstack1l11lll11l1_opy_.bstack111llll111l_opy_:
            if bstack1111lllll11_opy_ == bstack111l1llll11_opy_:
                bstack1111lll1l1l_opy_ = True
            bstack1111lllll11_opy_ = bstack111l1lllll1_opy_
        try:
            platform_index = os.environ[bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᰮ")]
            target_dir = os.path.join(bstack11ll11l1ll1_opy_, bstack11ll1ll1l11_opy_ + str(platform_index),
                                      bstack1111lllll11_opy_)
            if bstack1111lll1l1l_opy_:
                target_dir = os.path.join(target_dir, bstack111l1111111_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack111ll_opy_ (u"ࠧࡉࡲࡦࡣࡷࡩࡩ࠵ࡶࡦࡴ࡬ࡪ࡮࡫ࡤࠡࡶࡤࡶ࡬࡫ࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᰯ").format(target_dir))
            file_name = os.path.basename(bstack1ll1l1ll1l1_opy_)
            bstack1111lll1lll_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack1111lll1lll_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack1111llll111_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack1111llll111_opy_) + extension)):
                    bstack1111llll111_opy_ += 1
                bstack1111lll1lll_opy_ = os.path.join(target_dir, base_name + str(bstack1111llll111_opy_) + extension)
            shutil.copy(bstack1ll1l1ll1l1_opy_, bstack1111lll1lll_opy_)
            logger.info(bstack111ll_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡧࡴࡶࡩࡦࡦࠣࡸࡴࡀࠠࡼࡿࠥᰰ").format(bstack1111lll1lll_opy_))
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡭ࡰࡸ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࡹࡵࠠࡵࡣࡵ࡫ࡪࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᰱ").format(e))
            return
        finally:
            if bstack111l11111ll_opy_.startswith(bstack111ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᰲ")) or bstack111l11111ll_opy_.startswith(bstack111ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᰳ")):
                try:
                    if bstack1ll1l1ll1l1_opy_ is not None and bstack1ll1l1ll1l1_opy_.exists():
                        bstack1ll1l1ll1l1_opy_.unlink()
                        logger.debug(bstack111ll_opy_ (u"ࠥࡘࡪࡳࡰࡰࡴࡤࡶࡾࠦࡦࡪ࡮ࡨࠤࡩ࡫࡬ࡦࡶࡨࡨ࠿ࠦࡻࡾࠤᰴ").format(bstack1ll1l1ll1l1_opy_))
                except Exception as ex:
                    logger.error(bstack111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠥᰵ").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack111l1111l11_opy_, stage=STAGE.bstack1l1l11l1l_opy_, bstack1111l11lll_opy_=None)
    def bstack11111ll1ll_opy_() -> None:
        bstack111ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡇࡩࡱ࡫ࡴࡦࡵࠣࡥࡱࡲࠠࡧࡱ࡯ࡨࡪࡸࡳࠡࡹ࡫ࡳࡸ࡫ࠠ࡯ࡣࡰࡩࡸࠦࡳࡵࡣࡵࡸࠥࡽࡩࡵࡪ࡚ࠣࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦࠥ࡬࡯࡭࡮ࡲࡻࡪࡪࠠࡣࡻࠣࡥࠥࡴࡵ࡮ࡤࡨࡶࠥ࡯࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷ࡬ࡪࠦࡵࡴࡧࡵࠫࡸࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᰶ")
        bstack1111lll1ll1_opy_ = bstack11ll11l1lll_opy_()
        pattern = re.compile(bstack111ll_opy_ (u"ࡸࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳࡜ࡥ᰷࠭ࠥ"))
        if os.path.exists(bstack1111lll1ll1_opy_):
            for item in os.listdir(bstack1111lll1ll1_opy_):
                bstack1111lllllll_opy_ = os.path.join(bstack1111lll1ll1_opy_, item)
                if os.path.isdir(bstack1111lllllll_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack1111lllllll_opy_)
                    except Exception as e:
                        logger.error(bstack111ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣ᰸").format(e))
        else:
            logger.info(bstack111ll_opy_ (u"ࠣࡖ࡫ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨ᰹").format(bstack1111lll1ll1_opy_))