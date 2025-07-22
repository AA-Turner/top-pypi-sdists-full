# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
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
from bstack_utils.helper import bstack1l1lll11111_opy_
bstack11lll1l111l_opy_ = 100 * 1024 * 1024 # 100 bstack11lll1l1ll1_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l1ll1ll111_opy_ = bstack1l1lll11111_opy_()
bstack1l1ll11l11l_opy_ = bstack111l111_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᗥ")
bstack11lllll1111_opy_ = bstack111l111_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᗦ")
bstack11lllll1l1l_opy_ = bstack111l111_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᗧ")
bstack11lllll1l11_opy_ = bstack111l111_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦᗨ")
bstack11lll1l1l1l_opy_ = bstack111l111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣᗩ")
_11lll1l1lll_opy_ = threading.local()
def bstack11llllll111_opy_(test_framework_state, test_hook_state):
    bstack111l111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡗࡪࡺࠠࡵࡪࡨࠤࡨࡻࡲࡳࡧࡱࡸࠥࡺࡥࡴࡶࠣࡩࡻ࡫࡮ࡵࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡹ࡮ࡲࡦࡣࡧ࠱ࡱࡵࡣࡢ࡮ࠣࡷࡹࡵࡲࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࡗ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡶ࡬ࡴࡻ࡬ࡥࠢࡥࡩࠥࡩࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡶ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥ࠮ࡳࡶࡥ࡫ࠤࡦࡹࠠࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠮ࠐࠠࠡࠢࠣࡦࡪ࡬࡯ࡳࡧࠣࡥࡳࡿࠠࡧ࡫࡯ࡩࠥࡻࡰ࡭ࡱࡤࡨࡸࠦ࡯ࡤࡥࡸࡶ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᗪ")
    _11lll1l1lll_opy_.test_framework_state = test_framework_state
    _11lll1l1lll_opy_.test_hook_state = test_hook_state
def bstack11lll11l111_opy_():
    bstack111l111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡗ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡴࡩࡧࠣࡧࡺࡸࡲࡦࡰࡷࠤࡹ࡫ࡳࡵࠢࡨࡺࡪࡴࡴࠡࡵࡷࡥࡹ࡫ࠠࡧࡴࡲࡱࠥࡺࡨࡳࡧࡤࡨ࠲ࡲ࡯ࡤࡣ࡯ࠤࡸࡺ࡯ࡳࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡦࠦࡴࡶࡲ࡯ࡩࠥ࠮ࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪ࠲ࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࠫࠣࡳࡷࠦࠨࡏࡱࡱࡩ࠱ࠦࡎࡰࡰࡨ࠭ࠥ࡯ࡦࠡࡰࡲࡸࠥࡹࡥࡵ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᗫ")
    return (
        getattr(_11lll1l1lll_opy_, bstack111l111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࠬᗬ"), None),
        getattr(_11lll1l1lll_opy_, bstack111l111_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࠨᗭ"), None)
    )
class bstack1lll1ll1ll_opy_:
    bstack111l111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡇ࡫࡯ࡩ࡚ࡶ࡬ࡰࡣࡧࡩࡷࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰࡤࡰ࡮ࡺࡹࠡࡶࡲࠤࡺࡶ࡬ࡰࡣࡧࠤࡦࡴࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡧࡧࡳࡦࡦࠣࡳࡳࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࡍࡹࠦࡳࡶࡲࡳࡳࡷࡺࡳࠡࡤࡲࡸ࡭ࠦ࡬ࡰࡥࡤࡰࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࡴࠢࡤࡲࡩࠦࡈࡕࡖࡓ࠳ࡍ࡚ࡔࡑࡕ࡙ࠣࡗࡒࡳ࠭ࠢࡤࡲࡩࠦࡣࡰࡲ࡬ࡩࡸࠦࡴࡩࡧࠣࡪ࡮ࡲࡥࠡ࡫ࡱࡸࡴࠦࡡࠡࡦࡨࡷ࡮࡭࡮ࡢࡶࡨࡨࠏࠦࠠࠡࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡽࡩࡵࡪ࡬ࡲࠥࡺࡨࡦࠢࡸࡷࡪࡸࠧࡴࠢ࡫ࡳࡲ࡫ࠠࡧࡱ࡯ࡨࡪࡸࠠࡶࡰࡧࡩࡷࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࡏࡦࠡࡣࡱࠤࡴࡶࡴࡪࡱࡱࡥࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࠦࠨࡪࡰࠣࡎࡘࡕࡎࠡࡨࡲࡶࡲࡧࡴࠪࠢ࡬ࡷࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡢࡰࡧࠤࡨࡵ࡮ࡵࡣ࡬ࡲࡸࠦࡡࠡࡶࡵࡹࡹ࡮ࡹࠡࡸࡤࡰࡺ࡫ࠊࠡࠢࠣࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡱࡥࡺࠢࠥࡦࡺ࡯࡬ࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧ࠲ࠠࡵࡪࡨࠤ࡫࡯࡬ࡦࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡴࡱࡧࡣࡦࡦࠣ࡭ࡳࠦࡴࡩࡧࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡩࡳࡱࡪࡥࡳ࠽ࠣࡳࡹ࡮ࡥࡳࡹ࡬ࡷࡪ࠲ࠊࠡࠢࠣࠤ࡮ࡺࠠࡥࡧࡩࡥࡺࡲࡴࡴࠢࡷࡳࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤ࠱ࠎࠥࠦࠠࠡࡖ࡫࡭ࡸࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡰࡨࠣࡥࡩࡪ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤ࡮ࡹࠠࡢࠢࡹࡳ࡮ࡪࠠ࡮ࡧࡷ࡬ࡴࡪ⠔ࡪࡶࠣ࡬ࡦࡴࡤ࡭ࡧࡶࠤࡦࡲ࡬ࠡࡧࡵࡶࡴࡸࡳࠡࡩࡵࡥࡨ࡫ࡦࡶ࡮࡯ࡽࠥࡨࡹࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠌࠣࠤࠥࠦࡴࡩࡧࡰࠤࡦࡴࡤࠡࡵ࡬ࡱࡵࡲࡹࠡࡴࡨࡸࡺࡸ࡮ࡪࡰࡪࠤࡼ࡯ࡴࡩࡱࡸࡸࠥࡺࡨࡳࡱࡺ࡭ࡳ࡭ࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࡶ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᗮ")
    @staticmethod
    def upload_attachment(bstack11lll1l11ll_opy_: str, *bstack11lll11l11l_opy_) -> None:
        if not bstack11lll1l11ll_opy_ or not bstack11lll1l11ll_opy_.strip():
            logger.error(bstack111l111_opy_ (u"ࠣࡣࡧࡨࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡔࡷࡵࡶࡪࡦࡨࡨࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࠡ࡫ࡶࠤࡪࡳࡰࡵࡻࠣࡳࡷࠦࡎࡰࡰࡨ࠲ࠧᗯ"))
            return
        bstack11lll1l1111_opy_ = bstack11lll11l11l_opy_[0] if bstack11lll11l11l_opy_ and len(bstack11lll11l11l_opy_) > 0 else None
        bstack11lll11lll1_opy_ = None
        test_framework_state, test_hook_state = bstack11lll11l111_opy_()
        try:
            if bstack11lll1l11ll_opy_.startswith(bstack111l111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᗰ")) or bstack11lll1l11ll_opy_.startswith(bstack111l111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᗱ")):
                logger.debug(bstack111l111_opy_ (u"ࠦࡕࡧࡴࡩࠢ࡬ࡷࠥ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡥࠢࡤࡷ࡛ࠥࡒࡍ࠽ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠦᗲ"))
                url = bstack11lll1l11ll_opy_
                bstack11lll11ll1l_opy_ = str(uuid.uuid4())
                bstack11lll1l1l11_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11lll1l1l11_opy_ or not bstack11lll1l1l11_opy_.strip():
                    bstack11lll1l1l11_opy_ = bstack11lll11ll1l_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack111l111_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࡤࠨᗳ") + bstack11lll11ll1l_opy_ + bstack111l111_opy_ (u"ࠨ࡟ࠣᗴ"),
                                                        suffix=bstack111l111_opy_ (u"ࠢࡠࠤᗵ") + bstack11lll1l1l11_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack111l111_opy_ (u"ࠨࡹࡥࠫᗶ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11lll11lll1_opy_ = Path(temp_file.name)
                logger.debug(bstack111l111_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡦࡪ࡮ࡨࠤࡹࡵࠠࡵࡧࡰࡴࡴࡸࡡࡳࡻࠣࡰࡴࡩࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᗷ").format(bstack11lll11lll1_opy_))
            else:
                bstack11lll11lll1_opy_ = Path(bstack11lll1l11ll_opy_)
                logger.debug(bstack111l111_opy_ (u"ࠥࡔࡦࡺࡨࠡ࡫ࡶࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡤࠡࡣࡶࠤࡱࡵࡣࡢ࡮ࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠧᗸ").format(bstack11lll11lll1_opy_))
        except Exception as e:
            logger.error(bstack111l111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡰࡤࡷࡥ࡮ࡴࠠࡧ࡫࡯ࡩࠥ࡬ࡲࡰ࡯ࠣࡴࡦࡺࡨ࠰ࡗࡕࡐ࠿ࠦࡻࡾࠤᗹ").format(e))
            return
        if bstack11lll11lll1_opy_ is None or not bstack11lll11lll1_opy_.exists():
            logger.error(bstack111l111_opy_ (u"࡙ࠧ࡯ࡶࡴࡦࡩࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠣᗺ").format(bstack11lll11lll1_opy_))
            return
        if bstack11lll11lll1_opy_.stat().st_size > bstack11lll1l111l_opy_:
            logger.error(bstack111l111_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡸ࡯ࡺࡦࠢࡨࡼࡨ࡫ࡥࡥࡵࠣࡱࡦࡾࡩ࡮ࡷࡰࠤࡦࡲ࡬ࡰࡹࡨࡨࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡻࡾࠤᗻ").format(bstack11lll1l111l_opy_))
            return
        bstack11lll1l11l1_opy_ = bstack111l111_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᗼ")
        if bstack11lll1l1111_opy_:
            try:
                params = json.loads(bstack11lll1l1111_opy_)
                if bstack111l111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᗽ") in params and params.get(bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᗾ")) is True:
                    bstack11lll1l11l1_opy_ = bstack111l111_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᗿ")
            except Exception as bstack11lll1ll11l_opy_:
                logger.error(bstack111l111_opy_ (u"ࠦࡏ࡙ࡏࡏࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡒࡤࡶࡦࡳࡳ࠻ࠢࡾࢁࠧᘀ").format(bstack11lll1ll11l_opy_))
        bstack11lll11l1ll_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1lll1111111_opy_ import bstack1lll1l111ll_opy_
        if test_framework_state in bstack1lll1l111ll_opy_.bstack1l111ll1l1l_opy_:
            if bstack11lll1l11l1_opy_ == bstack11lllll1l1l_opy_:
                bstack11lll11l1ll_opy_ = True
            bstack11lll1l11l1_opy_ = bstack11lllll1l11_opy_
        try:
            platform_index = os.environ[bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᘁ")]
            target_dir = os.path.join(bstack1l1ll1ll111_opy_, bstack1l1ll11l11l_opy_ + str(platform_index),
                                      bstack11lll1l11l1_opy_)
            if bstack11lll11l1ll_opy_:
                target_dir = os.path.join(target_dir, bstack11lll1l1l1l_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack111l111_opy_ (u"ࠨࡃࡳࡧࡤࡸࡪࡪ࠯ࡷࡧࡵ࡭࡫࡯ࡥࡥࠢࡷࡥࡷ࡭ࡥࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᘂ").format(target_dir))
            file_name = os.path.basename(bstack11lll11lll1_opy_)
            bstack11lll11l1l1_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11lll11l1l1_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11lll11llll_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11lll11llll_opy_) + extension)):
                    bstack11lll11llll_opy_ += 1
                bstack11lll11l1l1_opy_ = os.path.join(target_dir, base_name + str(bstack11lll11llll_opy_) + extension)
            shutil.copy(bstack11lll11lll1_opy_, bstack11lll11l1l1_opy_)
            logger.info(bstack111l111_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡨࡵࡰࡪࡧࡧࠤࡹࡵ࠺ࠡࡽࢀࠦᘃ").format(bstack11lll11l1l1_opy_))
        except Exception as e:
            logger.error(bstack111l111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠ࡮ࡱࡹ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩࠥࡺ࡯ࠡࡶࡤࡶ࡬࡫ࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᘄ").format(e))
            return
        finally:
            if bstack11lll1l11ll_opy_.startswith(bstack111l111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᘅ")) or bstack11lll1l11ll_opy_.startswith(bstack111l111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᘆ")):
                try:
                    if bstack11lll11lll1_opy_ is not None and bstack11lll11lll1_opy_.exists():
                        bstack11lll11lll1_opy_.unlink()
                        logger.debug(bstack111l111_opy_ (u"࡙ࠦ࡫࡭ࡱࡱࡵࡥࡷࡿࠠࡧ࡫࡯ࡩࠥࡪࡥ࡭ࡧࡷࡩࡩࡀࠠࡼࡿࠥᘇ").format(bstack11lll11lll1_opy_))
                except Exception as ex:
                    logger.error(bstack111l111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠦᘈ").format(ex))
    @staticmethod
    def bstack1l1l1ll111_opy_() -> None:
        bstack111l111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡈࡪࡲࡥࡵࡧࡶࠤࡦࡲ࡬ࠡࡨࡲࡰࡩ࡫ࡲࡴࠢࡺ࡬ࡴࡹࡥࠡࡰࡤࡱࡪࡹࠠࡴࡶࡤࡶࡹࠦࡷࡪࡶ࡫ࠤ࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧࠦࡦࡰ࡮࡯ࡳࡼ࡫ࡤࠡࡤࡼࠤࡦࠦ࡮ࡶ࡯ࡥࡩࡷࠦࡩ࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡫ࠠࡶࡵࡨࡶࠬࡹࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᘉ")
        bstack11lll1ll111_opy_ = bstack1l1lll11111_opy_()
        pattern = re.compile(bstack111l111_opy_ (u"ࡲࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭࡝ࡦ࠮ࠦᘊ"))
        if os.path.exists(bstack11lll1ll111_opy_):
            for item in os.listdir(bstack11lll1ll111_opy_):
                bstack11lll11ll11_opy_ = os.path.join(bstack11lll1ll111_opy_, item)
                if os.path.isdir(bstack11lll11ll11_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11lll11ll11_opy_)
                    except Exception as e:
                        logger.error(bstack111l111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᘋ").format(e))
        else:
            logger.info(bstack111l111_opy_ (u"ࠤࡗ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠢᘌ").format(bstack11lll1ll111_opy_))