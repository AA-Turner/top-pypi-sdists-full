# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
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
from bstack_utils.helper import bstack1l1lll1111l_opy_
bstack1l111111l1l_opy_ = 100 * 1024 * 1024 # 100 bstack1l11111111l_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1ll111l1l1l_opy_ = bstack1l1lll1111l_opy_()
bstack1l1ll1lll1l_opy_ = bstack1l1lll_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᔳ")
bstack1l111l11l1l_opy_ = bstack1l1lll_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᔴ")
bstack1l111l11ll1_opy_ = bstack1l1lll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᔵ")
bstack1l111l111ll_opy_ = bstack1l1lll_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣᔶ")
bstack11llllllll1_opy_ = bstack1l1lll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧᔷ")
_1l11111l1l1_opy_ = threading.local()
def bstack1l111lll1l1_opy_(test_framework_state, test_hook_state):
    bstack1l1lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡧࡷࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷࡩࡸࡺࠠࡦࡸࡨࡲࡹࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡶ࡫ࡶࡪࡧࡤ࠮࡮ࡲࡧࡦࡲࠠࡴࡶࡲࡶࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡳࡩࡱࡸࡰࡩࠦࡢࡦࠢࡦࡥࡱࡲࡥࡥࠢࡥࡽࠥࡺࡨࡦࠢࡨࡺࡪࡴࡴࠡࡪࡤࡲࡩࡲࡥࡳࠢࠫࡷࡺࡩࡨࠡࡣࡶࠤࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵࠫࠍࠤࠥࠦࠠࡣࡧࡩࡳࡷ࡫ࠠࡢࡰࡼࠤ࡫࡯࡬ࡦࠢࡸࡴࡱࡵࡡࡥࡵࠣࡳࡨࡩࡵࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᔸ")
    _1l11111l1l1_opy_.test_framework_state = test_framework_state
    _1l11111l1l1_opy_.test_hook_state = test_hook_state
def bstack11lllllllll_opy_():
    bstack1l1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡔࡨࡸࡷ࡯ࡥࡷࡧࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶࡨࡷࡹࠦࡥࡷࡧࡱࡸࠥࡹࡴࡢࡶࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡࡵࡷࡳࡷࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡣࠣࡸࡺࡶ࡬ࡦࠢࠫࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧ࠯ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪ࠯ࠠࡰࡴࠣࠬࡓࡵ࡮ࡦ࠮ࠣࡒࡴࡴࡥࠪࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᔹ")
    return (
        getattr(_1l11111l1l1_opy_, bstack1l1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࠩᔺ"), None),
        getattr(_1l11111l1l1_opy_, bstack1l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࠬᔻ"), None)
    )
class bstack1l11l1lll_opy_:
    bstack1l1lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡋ࡯࡬ࡦࡗࡳࡰࡴࡧࡤࡦࡴࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡡ࡭࡫ࡷࡽࠥࡺ࡯ࠡࡷࡳࡰࡴࡧࡤࠡࡣࡱࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࡊࡶࠣࡷࡺࡶࡰࡰࡴࡷࡷࠥࡨ࡯ࡵࡪࠣࡰࡴࡩࡡ࡭ࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࡸࠦࡡ࡯ࡦࠣࡌ࡙࡚ࡐ࠰ࡊࡗࡘࡕ࡙ࠠࡖࡔࡏࡷ࠱ࠦࡡ࡯ࡦࠣࡧࡴࡶࡩࡦࡵࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࡵࡱࠣࡥࠥࡪࡥࡴ࡫ࡪࡲࡦࡺࡥࡥࠌࠣࠤࠥࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡺ࡭ࡹ࡮ࡩ࡯ࠢࡷ࡬ࡪࠦࡵࡴࡧࡵࠫࡸࠦࡨࡰ࡯ࡨࠤ࡫ࡵ࡬ࡥࡧࡵࠤࡺࡴࡤࡦࡴࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࡌࡪࠥࡧ࡮ࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࠣࠬ࡮ࡴࠠࡋࡕࡒࡒࠥ࡬࡯ࡳ࡯ࡤࡸ࠮ࠦࡩࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡦࡴࡤࠡࡥࡲࡲࡹࡧࡩ࡯ࡵࠣࡥࠥࡺࡲࡶࡶ࡫ࡽࠥࡼࡡ࡭ࡷࡨࠎࠥࠦࠠࠡࡨࡲࡶࠥࡺࡨࡦࠢ࡮ࡩࡾࠦࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤ࠯ࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡱ࡮ࡤࡧࡪࡪࠠࡪࡰࠣࡸ࡭࡫ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡦࡰ࡮ࡧࡩࡷࡁࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧ࠯ࠎࠥࠦࠠࠡ࡫ࡷࠤࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ࠮ࠋࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡺࡪࡸࡳࡪࡱࡱࠤࡴ࡬ࠠࡢࡦࡧࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡ࡫ࡶࠤࡦࠦࡶࡰ࡫ࡧࠤࡲ࡫ࡴࡩࡱࡧ⠘࡮ࡺࠠࡩࡣࡱࡨࡱ࡫ࡳࠡࡣ࡯ࡰࠥ࡫ࡲࡳࡱࡵࡷࠥ࡭ࡲࡢࡥࡨࡪࡺࡲ࡬ࡺࠢࡥࡽࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠐࠠࠡࠢࠣࡸ࡭࡫࡭ࠡࡣࡱࡨࠥࡹࡩ࡮ࡲ࡯ࡽࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡷ࡬ࡷࡵࡷࡪࡰࡪࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࡳ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᔼ")
    @staticmethod
    def upload_attachment(bstack1l111111l11_opy_: str, *bstack1l11111l11l_opy_) -> None:
        if not bstack1l111111l11_opy_ or not bstack1l111111l11_opy_.strip():
            logger.error(bstack1l1lll_opy_ (u"ࠧࡧࡤࡥࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡑࡴࡲࡺ࡮ࡪࡥࡥࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡯ࡳࠡࡧࡰࡴࡹࡿࠠࡰࡴࠣࡒࡴࡴࡥ࠯ࠤᔽ"))
            return
        bstack1l1111111l1_opy_ = bstack1l11111l11l_opy_[0] if bstack1l11111l11l_opy_ and len(bstack1l11111l11l_opy_) > 0 else None
        bstack1l111111111_opy_ = None
        test_framework_state, test_hook_state = bstack11lllllllll_opy_()
        try:
            if bstack1l111111l11_opy_.startswith(bstack1l1lll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᔾ")) or bstack1l111111l11_opy_.startswith(bstack1l1lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᔿ")):
                logger.debug(bstack1l1lll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡩࡴࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡩࠦࡡࡴࠢࡘࡖࡑࡁࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠣᕀ"))
                url = bstack1l111111l11_opy_
                bstack11llllll1l1_opy_ = str(uuid.uuid4())
                bstack1l1111111ll_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack1l1111111ll_opy_ or not bstack1l1111111ll_opy_.strip():
                    bstack1l1111111ll_opy_ = bstack11llllll1l1_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1l1lll_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࡡࠥᕁ") + bstack11llllll1l1_opy_ + bstack1l1lll_opy_ (u"ࠥࡣࠧᕂ"),
                                                        suffix=bstack1l1lll_opy_ (u"ࠦࡤࠨᕃ") + bstack1l1111111ll_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1l1lll_opy_ (u"ࠬࡽࡢࠨᕄ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack1l111111111_opy_ = Path(temp_file.name)
                logger.debug(bstack1l1lll_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡪ࡮ࡲࡥࠡࡶࡲࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࡭ࡱࡦࡥࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᕅ").format(bstack1l111111111_opy_))
            else:
                bstack1l111111111_opy_ = Path(bstack1l111111l11_opy_)
                logger.debug(bstack1l1lll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥ࡯ࡳࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡨࠥࡧࡳࠡ࡮ࡲࡧࡦࡲࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤᕆ").format(bstack1l111111111_opy_))
        except Exception as e:
            logger.error(bstack1l1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡴࡨࡴࡢ࡫ࡱࠤ࡫࡯࡬ࡦࠢࡩࡶࡴࡳࠠࡱࡣࡷ࡬࠴࡛ࡒࡍ࠼ࠣࡿࢂࠨᕇ").format(e))
            return
        if bstack1l111111111_opy_ is None or not bstack1l111111111_opy_.exists():
            logger.error(bstack1l1lll_opy_ (u"ࠤࡖࡳࡺࡸࡣࡦࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧᕈ").format(bstack1l111111111_opy_))
            return
        if bstack1l111111111_opy_.stat().st_size > bstack1l111111l1l_opy_:
            logger.error(bstack1l1lll_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡵ࡬ࡾࡪࠦࡥࡹࡥࡨࡩࡩࡹࠠ࡮ࡣࡻ࡭ࡲࡻ࡭ࠡࡣ࡯ࡰࡴࡽࡥࡥࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡿࢂࠨᕉ").format(bstack1l111111l1l_opy_))
            return
        bstack1l111111ll1_opy_ = bstack1l1lll_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᕊ")
        if bstack1l1111111l1_opy_:
            try:
                params = json.loads(bstack1l1111111l1_opy_)
                if bstack1l1lll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᕋ") in params and params.get(bstack1l1lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᕌ")) is True:
                    bstack1l111111ll1_opy_ = bstack1l1lll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᕍ")
            except Exception as bstack1l11111l111_opy_:
                logger.error(bstack1l1lll_opy_ (u"ࠣࡌࡖࡓࡓࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡖࡡࡳࡣࡰࡷ࠿ࠦࡻࡾࠤᕎ").format(bstack1l11111l111_opy_))
        bstack11lllllll1l_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1lllll1l1l1_opy_ import bstack1lll11l11ll_opy_
        if test_framework_state in bstack1lll11l11ll_opy_.bstack1l111ll11ll_opy_:
            if bstack1l111111ll1_opy_ == bstack1l111l11ll1_opy_:
                bstack11lllllll1l_opy_ = True
            bstack1l111111ll1_opy_ = bstack1l111l111ll_opy_
        try:
            platform_index = os.environ[bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᕏ")]
            target_dir = os.path.join(bstack1ll111l1l1l_opy_, bstack1l1ll1lll1l_opy_ + str(platform_index),
                                      bstack1l111111ll1_opy_)
            if bstack11lllllll1l_opy_:
                target_dir = os.path.join(target_dir, bstack11llllllll1_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1l1lll_opy_ (u"ࠥࡇࡷ࡫ࡡࡵࡧࡧ࠳ࡻ࡫ࡲࡪࡨ࡬ࡩࡩࠦࡴࡢࡴࡪࡩࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᕐ").format(target_dir))
            file_name = os.path.basename(bstack1l111111111_opy_)
            bstack1l11111l1ll_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack1l11111l1ll_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11lllllll11_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11lllllll11_opy_) + extension)):
                    bstack11lllllll11_opy_ += 1
                bstack1l11111l1ll_opy_ = os.path.join(target_dir, base_name + str(bstack11lllllll11_opy_) + extension)
            shutil.copy(bstack1l111111111_opy_, bstack1l11111l1ll_opy_)
            logger.info(bstack1l1lll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡥࡲࡴ࡮࡫ࡤࠡࡶࡲ࠾ࠥࢁࡽࠣᕑ").format(bstack1l11111l1ll_opy_))
        except Exception as e:
            logger.error(bstack1l1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡲࡵࡶࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࡷࡳࠥࡺࡡࡳࡩࡨࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᕒ").format(e))
            return
        finally:
            if bstack1l111111l11_opy_.startswith(bstack1l1lll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᕓ")) or bstack1l111111l11_opy_.startswith(bstack1l1lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᕔ")):
                try:
                    if bstack1l111111111_opy_ is not None and bstack1l111111111_opy_.exists():
                        bstack1l111111111_opy_.unlink()
                        logger.debug(bstack1l1lll_opy_ (u"ࠣࡖࡨࡱࡵࡵࡲࡢࡴࡼࠤ࡫࡯࡬ࡦࠢࡧࡩࡱ࡫ࡴࡦࡦ࠽ࠤࢀࢃࠢᕕ").format(bstack1l111111111_opy_))
                except Exception as ex:
                    logger.error(bstack1l1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣᕖ").format(ex))
    @staticmethod
    def bstack1111ll111_opy_() -> None:
        bstack1l1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡧ࡯ࡩࡹ࡫ࡳࠡࡣ࡯ࡰࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࡷࡩࡱࡶࡩࠥࡴࡡ࡮ࡧࡶࠤࡸࡺࡡࡳࡶࠣࡻ࡮ࡺࡨࠡࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤࠣࡪࡴࡲ࡬ࡰࡹࡨࡨࠥࡨࡹࠡࡣࠣࡲࡺࡳࡢࡦࡴࠣ࡭ࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪࡨࠤࡺࡹࡥࡳࠩࡶࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᕗ")
        bstack11llllll1ll_opy_ = bstack1l1lll1111l_opy_()
        pattern = re.compile(bstack1l1lll_opy_ (u"ࡶ࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࡡࡪࠫࠣᕘ"))
        if os.path.exists(bstack11llllll1ll_opy_):
            for item in os.listdir(bstack11llllll1ll_opy_):
                bstack1l111111lll_opy_ = os.path.join(bstack11llllll1ll_opy_, item)
                if os.path.isdir(bstack1l111111lll_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack1l111111lll_opy_)
                    except Exception as e:
                        logger.error(bstack1l1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᕙ").format(e))
        else:
            logger.info(bstack1l1lll_opy_ (u"ࠨࡔࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠦᕚ").format(bstack11llllll1ll_opy_))