# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
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
from bstack_utils.helper import bstack1l1lll111l1_opy_
bstack11lllll1111_opy_ = 100 * 1024 * 1024 # 100 bstack11llll1ll11_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l1ll1l11l1_opy_ = bstack1l1lll111l1_opy_()
bstack1l1ll1l1111_opy_ = bstack111lll_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᕹ")
bstack1l11111llll_opy_ = bstack111lll_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᕺ")
bstack1l1111l11ll_opy_ = bstack111lll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᕻ")
bstack1l11111lll1_opy_ = bstack111lll_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᕼ")
bstack11lllll1lll_opy_ = bstack111lll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᕽ")
_11llll1lll1_opy_ = threading.local()
def bstack1l111ll11l1_opy_(test_framework_state, test_hook_state):
    bstack111lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡧࡷࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷࡩࡸࡺࠠࡦࡸࡨࡲࡹࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡶ࡫ࡶࡪࡧࡤ࠮࡮ࡲࡧࡦࡲࠠࡴࡶࡲࡶࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡳࡩࡱࡸࡰࡩࠦࡢࡦࠢࡦࡥࡱࡲࡥࡥࠢࡥࡽࠥࡺࡨࡦࠢࡨࡺࡪࡴࡴࠡࡪࡤࡲࡩࡲࡥࡳࠢࠫࡷࡺࡩࡨࠡࡣࡶࠤࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵࠫࠍࠤࠥࠦࠠࡣࡧࡩࡳࡷ࡫ࠠࡢࡰࡼࠤ࡫࡯࡬ࡦࠢࡸࡴࡱࡵࡡࡥࡵࠣࡳࡨࡩࡵࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᕾ")
    _11llll1lll1_opy_.test_framework_state = test_framework_state
    _11llll1lll1_opy_.test_hook_state = test_hook_state
def bstack11lllll11l1_opy_():
    bstack111lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡔࡨࡸࡷ࡯ࡥࡷࡧࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶࡨࡷࡹࠦࡥࡷࡧࡱࡸࠥࡹࡴࡢࡶࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡࡵࡷࡳࡷࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡣࠣࡸࡺࡶ࡬ࡦࠢࠫࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧ࠯ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪ࠯ࠠࡰࡴࠣࠬࡓࡵ࡮ࡦ࠮ࠣࡒࡴࡴࡥࠪࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᕿ")
    return (
        getattr(_11llll1lll1_opy_, bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࠩᖀ"), None),
        getattr(_11llll1lll1_opy_, bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࠬᖁ"), None)
    )
class bstack1lllllll1l_opy_:
    bstack111lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡋ࡯࡬ࡦࡗࡳࡰࡴࡧࡤࡦࡴࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡡ࡭࡫ࡷࡽࠥࡺ࡯ࠡࡷࡳࡰࡴࡧࡤࠡࡣࡱࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࡊࡶࠣࡷࡺࡶࡰࡰࡴࡷࡷࠥࡨ࡯ࡵࡪࠣࡰࡴࡩࡡ࡭ࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࡸࠦࡡ࡯ࡦࠣࡌ࡙࡚ࡐ࠰ࡊࡗࡘࡕ࡙ࠠࡖࡔࡏࡷ࠱ࠦࡡ࡯ࡦࠣࡧࡴࡶࡩࡦࡵࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࡵࡱࠣࡥࠥࡪࡥࡴ࡫ࡪࡲࡦࡺࡥࡥࠌࠣࠤࠥࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡺ࡭ࡹ࡮ࡩ࡯ࠢࡷ࡬ࡪࠦࡵࡴࡧࡵࠫࡸࠦࡨࡰ࡯ࡨࠤ࡫ࡵ࡬ࡥࡧࡵࠤࡺࡴࡤࡦࡴࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࡌࡪࠥࡧ࡮ࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࠣࠬ࡮ࡴࠠࡋࡕࡒࡒࠥ࡬࡯ࡳ࡯ࡤࡸ࠮ࠦࡩࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡦࡴࡤࠡࡥࡲࡲࡹࡧࡩ࡯ࡵࠣࡥࠥࡺࡲࡶࡶ࡫ࡽࠥࡼࡡ࡭ࡷࡨࠎࠥࠦࠠࠡࡨࡲࡶࠥࡺࡨࡦࠢ࡮ࡩࡾࠦࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤ࠯ࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡱ࡮ࡤࡧࡪࡪࠠࡪࡰࠣࡸ࡭࡫ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡦࡰ࡮ࡧࡩࡷࡁࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧ࠯ࠎࠥࠦࠠࠡ࡫ࡷࠤࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ࠮ࠋࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡺࡪࡸࡳࡪࡱࡱࠤࡴ࡬ࠠࡢࡦࡧࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡ࡫ࡶࠤࡦࠦࡶࡰ࡫ࡧࠤࡲ࡫ࡴࡩࡱࡧ⠘࡮ࡺࠠࡩࡣࡱࡨࡱ࡫ࡳࠡࡣ࡯ࡰࠥ࡫ࡲࡳࡱࡵࡷࠥ࡭ࡲࡢࡥࡨࡪࡺࡲ࡬ࡺࠢࡥࡽࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠐࠠࠡࠢࠣࡸ࡭࡫࡭ࠡࡣࡱࡨࠥࡹࡩ࡮ࡲ࡯ࡽࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡷ࡬ࡷࡵࡷࡪࡰࡪࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࡳ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᖂ")
    @staticmethod
    def upload_attachment(bstack11lllll11ll_opy_: str, *bstack11lllll1l1l_opy_) -> None:
        if not bstack11lllll11ll_opy_ or not bstack11lllll11ll_opy_.strip():
            logger.error(bstack111lll_opy_ (u"ࠧࡧࡤࡥࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡑࡴࡲࡺ࡮ࡪࡥࡥࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡯ࡳࠡࡧࡰࡴࡹࡿࠠࡰࡴࠣࡒࡴࡴࡥ࠯ࠤᖃ"))
            return
        bstack11llll1ll1l_opy_ = bstack11lllll1l1l_opy_[0] if bstack11lllll1l1l_opy_ and len(bstack11lllll1l1l_opy_) > 0 else None
        bstack11llll1l111_opy_ = None
        test_framework_state, test_hook_state = bstack11lllll11l1_opy_()
        try:
            if bstack11lllll11ll_opy_.startswith(bstack111lll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᖄ")) or bstack11lllll11ll_opy_.startswith(bstack111lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᖅ")):
                logger.debug(bstack111lll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡩࡴࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡩࠦࡡࡴࠢࡘࡖࡑࡁࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠣᖆ"))
                url = bstack11lllll11ll_opy_
                bstack11llll1l11l_opy_ = str(uuid.uuid4())
                bstack11lllll1ll1_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11lllll1ll1_opy_ or not bstack11lllll1ll1_opy_.strip():
                    bstack11lllll1ll1_opy_ = bstack11llll1l11l_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack111lll_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࡡࠥᖇ") + bstack11llll1l11l_opy_ + bstack111lll_opy_ (u"ࠥࡣࠧᖈ"),
                                                        suffix=bstack111lll_opy_ (u"ࠦࡤࠨᖉ") + bstack11lllll1ll1_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack111lll_opy_ (u"ࠬࡽࡢࠨᖊ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11llll1l111_opy_ = Path(temp_file.name)
                logger.debug(bstack111lll_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡪ࡮ࡲࡥࠡࡶࡲࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࡭ࡱࡦࡥࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᖋ").format(bstack11llll1l111_opy_))
            else:
                bstack11llll1l111_opy_ = Path(bstack11lllll11ll_opy_)
                logger.debug(bstack111lll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥ࡯ࡳࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡨࠥࡧࡳࠡ࡮ࡲࡧࡦࡲࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤᖌ").format(bstack11llll1l111_opy_))
        except Exception as e:
            logger.error(bstack111lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡴࡨࡴࡢ࡫ࡱࠤ࡫࡯࡬ࡦࠢࡩࡶࡴࡳࠠࡱࡣࡷ࡬࠴࡛ࡒࡍ࠼ࠣࡿࢂࠨᖍ").format(e))
            return
        if bstack11llll1l111_opy_ is None or not bstack11llll1l111_opy_.exists():
            logger.error(bstack111lll_opy_ (u"ࠤࡖࡳࡺࡸࡣࡦࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧᖎ").format(bstack11llll1l111_opy_))
            return
        if bstack11llll1l111_opy_.stat().st_size > bstack11lllll1111_opy_:
            logger.error(bstack111lll_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡵ࡬ࡾࡪࠦࡥࡹࡥࡨࡩࡩࡹࠠ࡮ࡣࡻ࡭ࡲࡻ࡭ࠡࡣ࡯ࡰࡴࡽࡥࡥࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡿࢂࠨᖏ").format(bstack11lllll1111_opy_))
            return
        bstack11llll1l1ll_opy_ = bstack111lll_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᖐ")
        if bstack11llll1ll1l_opy_:
            try:
                params = json.loads(bstack11llll1ll1l_opy_)
                if bstack111lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᖑ") in params and params.get(bstack111lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᖒ")) is True:
                    bstack11llll1l1ll_opy_ = bstack111lll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᖓ")
            except Exception as bstack11llll1l1l1_opy_:
                logger.error(bstack111lll_opy_ (u"ࠣࡌࡖࡓࡓࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡖࡡࡳࡣࡰࡷ࠿ࠦࡻࡾࠤᖔ").format(bstack11llll1l1l1_opy_))
        bstack11llll11lll_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import bstack1lllll11l1l_opy_
        if test_framework_state in bstack1lllll11l1l_opy_.bstack1l11l11lll1_opy_:
            if bstack11llll1l1ll_opy_ == bstack1l1111l11ll_opy_:
                bstack11llll11lll_opy_ = True
            bstack11llll1l1ll_opy_ = bstack1l11111lll1_opy_
        try:
            platform_index = os.environ[bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᖕ")]
            target_dir = os.path.join(bstack1l1ll1l11l1_opy_, bstack1l1ll1l1111_opy_ + str(platform_index),
                                      bstack11llll1l1ll_opy_)
            if bstack11llll11lll_opy_:
                target_dir = os.path.join(target_dir, bstack11lllll1lll_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack111lll_opy_ (u"ࠥࡇࡷ࡫ࡡࡵࡧࡧ࠳ࡻ࡫ࡲࡪࡨ࡬ࡩࡩࠦࡴࡢࡴࡪࡩࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᖖ").format(target_dir))
            file_name = os.path.basename(bstack11llll1l111_opy_)
            bstack11llll1llll_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11llll1llll_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11lllll1l11_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11lllll1l11_opy_) + extension)):
                    bstack11lllll1l11_opy_ += 1
                bstack11llll1llll_opy_ = os.path.join(target_dir, base_name + str(bstack11lllll1l11_opy_) + extension)
            shutil.copy(bstack11llll1l111_opy_, bstack11llll1llll_opy_)
            logger.info(bstack111lll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡥࡲࡴ࡮࡫ࡤࠡࡶࡲ࠾ࠥࢁࡽࠣᖗ").format(bstack11llll1llll_opy_))
        except Exception as e:
            logger.error(bstack111lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡲࡵࡶࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࡷࡳࠥࡺࡡࡳࡩࡨࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᖘ").format(e))
            return
        finally:
            if bstack11lllll11ll_opy_.startswith(bstack111lll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᖙ")) or bstack11lllll11ll_opy_.startswith(bstack111lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᖚ")):
                try:
                    if bstack11llll1l111_opy_ is not None and bstack11llll1l111_opy_.exists():
                        bstack11llll1l111_opy_.unlink()
                        logger.debug(bstack111lll_opy_ (u"ࠣࡖࡨࡱࡵࡵࡲࡢࡴࡼࠤ࡫࡯࡬ࡦࠢࡧࡩࡱ࡫ࡴࡦࡦ࠽ࠤࢀࢃࠢᖛ").format(bstack11llll1l111_opy_))
                except Exception as ex:
                    logger.error(bstack111lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣᖜ").format(ex))
    @staticmethod
    def bstack1111l111_opy_() -> None:
        bstack111lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡧ࡯ࡩࡹ࡫ࡳࠡࡣ࡯ࡰࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࡷࡩࡱࡶࡩࠥࡴࡡ࡮ࡧࡶࠤࡸࡺࡡࡳࡶࠣࡻ࡮ࡺࡨࠡࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤࠣࡪࡴࡲ࡬ࡰࡹࡨࡨࠥࡨࡹࠡࡣࠣࡲࡺࡳࡢࡦࡴࠣ࡭ࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪࡨࠤࡺࡹࡥࡳࠩࡶࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᖝ")
        bstack11lllll111l_opy_ = bstack1l1lll111l1_opy_()
        pattern = re.compile(bstack111lll_opy_ (u"ࡶ࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࡡࡪࠫࠣᖞ"))
        if os.path.exists(bstack11lllll111l_opy_):
            for item in os.listdir(bstack11lllll111l_opy_):
                bstack11llll11ll1_opy_ = os.path.join(bstack11lllll111l_opy_, item)
                if os.path.isdir(bstack11llll11ll1_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11llll11ll1_opy_)
                    except Exception as e:
                        logger.error(bstack111lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᖟ").format(e))
        else:
            logger.info(bstack111lll_opy_ (u"ࠨࡔࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠦᖠ").format(bstack11lllll111l_opy_))