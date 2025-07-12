# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
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
from bstack_utils.helper import bstack1lllllll1l1_opy_
bstack11lll1l1l11_opy_ = 100 * 1024 * 1024 # 100 bstack11lll1ll11l_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1lllllll111_opy_ = bstack1lllllll1l1_opy_()
bstack1111111lll_opy_ = bstack11l1111_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᗡ")
bstack1l1l11lllll_opy_ = bstack11l1111_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧᗢ")
bstack1l1l11lll11_opy_ = bstack11l1111_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᗣ")
bstack1l1l11ll1ll_opy_ = bstack11l1111_opy_ (u"ࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢᗤ")
bstack11lll1ll1ll_opy_ = bstack11l1111_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦᗥ")
_11lll1ll1l1_opy_ = threading.local()
def bstack1l1ll1l111l_opy_(test_framework_state, test_hook_state):
    bstack11l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡓࡦࡶࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶࡨࡷࡹࠦࡥࡷࡧࡱࡸࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡵࡪࡵࡩࡦࡪ࠭࡭ࡱࡦࡥࡱࠦࡳࡵࡱࡵࡥ࡬࡫࠮ࠋࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࡹࡨࡰࡷ࡯ࡨࠥࡨࡥࠡࡥࡤࡰࡱ࡫ࡤࠡࡤࡼࠤࡹ࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡩࡣࡱࡨࡱ࡫ࡲࠡࠪࡶࡹࡨ࡮ࠠࡢࡵࠣࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴࠪࠌࠣࠤࠥࠦࡢࡦࡨࡲࡶࡪࠦࡡ࡯ࡻࠣࡪ࡮ࡲࡥࠡࡷࡳࡰࡴࡧࡤࡴࠢࡲࡧࡨࡻࡲ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᗦ")
    _11lll1ll1l1_opy_.test_framework_state = test_framework_state
    _11lll1ll1l1_opy_.test_hook_state = test_hook_state
def bstack11lll11ll11_opy_():
    bstack11l1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡓࡧࡷࡶ࡮࡫ࡶࡦࠢࡷ࡬ࡪࠦࡣࡶࡴࡵࡩࡳࡺࠠࡵࡧࡶࡸࠥ࡫ࡶࡦࡰࡷࠤࡸࡺࡡࡵࡧࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡶࡪࡧࡤ࠮࡮ࡲࡧࡦࡲࠠࡴࡶࡲࡶࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡢࠢࡷࡹࡵࡲࡥࠡࠪࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠮ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩ࠮ࠦ࡯ࡳࠢࠫࡒࡴࡴࡥ࠭ࠢࡑࡳࡳ࡫ࠩࠡ࡫ࡩࠤࡳࡵࡴࠡࡵࡨࡸ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᗧ")
    return (
        getattr(_11lll1ll1l1_opy_, bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࠨᗨ"), None),
        getattr(_11lll1ll1l1_opy_, bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࠫᗩ"), None)
    )
class bstack11ll1ll11l_opy_:
    bstack11l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡊ࡮ࡲࡥࡖࡲ࡯ࡳࡦࡪࡥࡳࠢࡳࡶࡴࡼࡩࡥࡧࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡧ࡬ࡪࡶࡼࠤࡹࡵࠠࡶࡲ࡯ࡳࡦࡪࠠࡢࡰࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡣࡣࡶࡩࡩࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࡉࡵࠢࡶࡹࡵࡶ࡯ࡳࡶࡶࠤࡧࡵࡴࡩࠢ࡯ࡳࡨࡧ࡬ࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࡷࠥࡧ࡮ࡥࠢࡋࡘ࡙ࡖ࠯ࡉࡖࡗࡔࡘࠦࡕࡓࡎࡶ࠰ࠥࡧ࡮ࡥࠢࡦࡳࡵ࡯ࡥࡴࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨࠤ࡮ࡴࡴࡰࠢࡤࠤࡩ࡫ࡳࡪࡩࡱࡥࡹ࡫ࡤࠋࠢࠣࠤࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡹ࡬ࡸ࡭࡯࡮ࠡࡶ࡫ࡩࠥࡻࡳࡦࡴࠪࡷࠥ࡮࡯࡮ࡧࠣࡪࡴࡲࡤࡦࡴࠣࡹࡳࡪࡥࡳࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠳࡚ࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠱ࠎࠥࠦࠠࠡࡋࡩࠤࡦࡴࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡰࡢࡴࡤࡱࡪࡺࡥࡳࠢࠫ࡭ࡳࠦࡊࡔࡑࡑࠤ࡫ࡵࡲ࡮ࡣࡷ࠭ࠥ࡯ࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡥࡳࡪࠠࡤࡱࡱࡸࡦ࡯࡮ࡴࠢࡤࠤࡹࡸࡵࡵࡪࡼࠤࡻࡧ࡬ࡶࡧࠍࠤࠥࠦࠠࡧࡱࡵࠤࡹ࡮ࡥࠡ࡭ࡨࡽࠥࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣ࠮ࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡰ࡭ࡣࡦࡩࡩࠦࡩ࡯ࠢࡷ࡬ࡪࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥ࡬࡯࡭ࡦࡨࡶࡀࠦ࡯ࡵࡪࡨࡶࡼ࡯ࡳࡦ࠮ࠍࠤࠥࠦࠠࡪࡶࠣࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧ࠴ࠊࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡹࡩࡷࡹࡩࡰࡰࠣࡳ࡫ࠦࡡࡥࡦࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡪࡵࠣࡥࠥࡼ࡯ࡪࡦࠣࡱࡪࡺࡨࡰࡦ⠗࡭ࡹࠦࡨࡢࡰࡧࡰࡪࡹࠠࡢ࡮࡯ࠤࡪࡸࡲࡰࡴࡶࠤ࡬ࡸࡡࡤࡧࡩࡹࡱࡲࡹࠡࡤࡼࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠏࠦࠠࠡࠢࡷ࡬ࡪࡳࠠࡢࡰࡧࠤࡸ࡯࡭ࡱ࡮ࡼࠤࡷ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡶ࡫ࡶࡴࡽࡩ࡯ࡩࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡹ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᗪ")
    @staticmethod
    def upload_attachment(bstack11lll1l1l1l_opy_: str, *bstack11lll1l1111_opy_) -> None:
        if not bstack11lll1l1l1l_opy_ or not bstack11lll1l1l1l_opy_.strip():
            logger.error(bstack11l1111_opy_ (u"ࠦࡦࡪࡤࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡐࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࠤ࡮ࡹࠠࡦ࡯ࡳࡸࡾࠦ࡯ࡳࠢࡑࡳࡳ࡫࠮ࠣᗫ"))
            return
        bstack11lll1l11l1_opy_ = bstack11lll1l1111_opy_[0] if bstack11lll1l1111_opy_ and len(bstack11lll1l1111_opy_) > 0 else None
        bstack11lll11lll1_opy_ = None
        test_framework_state, test_hook_state = bstack11lll11ll11_opy_()
        try:
            if bstack11lll1l1l1l_opy_.startswith(bstack11l1111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᗬ")) or bstack11lll1l1l1l_opy_.startswith(bstack11l1111_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᗭ")):
                logger.debug(bstack11l1111_opy_ (u"ࠢࡑࡣࡷ࡬ࠥ࡯ࡳࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡨࠥࡧࡳࠡࡗࡕࡐࡀࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠢᗮ"))
                url = bstack11lll1l1l1l_opy_
                bstack11lll1ll111_opy_ = str(uuid.uuid4())
                bstack11lll1l111l_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11lll1l111l_opy_ or not bstack11lll1l111l_opy_.strip():
                    bstack11lll1l111l_opy_ = bstack11lll1ll111_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack11l1111_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࡠࠤᗯ") + bstack11lll1ll111_opy_ + bstack11l1111_opy_ (u"ࠤࡢࠦᗰ"),
                                                        suffix=bstack11l1111_opy_ (u"ࠥࡣࠧᗱ") + bstack11lll1l111l_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack11l1111_opy_ (u"ࠫࡼࡨࠧᗲ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11lll11lll1_opy_ = Path(temp_file.name)
                logger.debug(bstack11l1111_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡩ࡭ࡱ࡫ࠠࡵࡱࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦ࡬ࡰࡥࡤࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᗳ").format(bstack11lll11lll1_opy_))
            else:
                bstack11lll11lll1_opy_ = Path(bstack11lll1l1l1l_opy_)
                logger.debug(bstack11l1111_opy_ (u"ࠨࡐࡢࡶ࡫ࠤ࡮ࡹࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡧࠤࡦࡹࠠ࡭ࡱࡦࡥࡱࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣᗴ").format(bstack11lll11lll1_opy_))
        except Exception as e:
            logger.error(bstack11l1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡳࡧࡺࡡࡪࡰࠣࡪ࡮ࡲࡥࠡࡨࡵࡳࡲࠦࡰࡢࡶ࡫࠳࡚ࡘࡌ࠻ࠢࡾࢁࠧᗵ").format(e))
            return
        if bstack11lll11lll1_opy_ is None or not bstack11lll11lll1_opy_.exists():
            logger.error(bstack11l1111_opy_ (u"ࠣࡕࡲࡹࡷࡩࡥࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠦᗶ").format(bstack11lll11lll1_opy_))
            return
        if bstack11lll11lll1_opy_.stat().st_size > bstack11lll1l1l11_opy_:
            logger.error(bstack11l1111_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࡴ࡫ࡽࡩࠥ࡫ࡸࡤࡧࡨࡨࡸࠦ࡭ࡢࡺ࡬ࡱࡺࡳࠠࡢ࡮࡯ࡳࡼ࡫ࡤࠡࡵ࡬ࡾࡪࠦ࡯ࡧࠢࡾࢁࠧᗷ").format(bstack11lll1l1l11_opy_))
            return
        bstack11lll11ll1l_opy_ = bstack11l1111_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᗸ")
        if bstack11lll1l11l1_opy_:
            try:
                params = json.loads(bstack11lll1l11l1_opy_)
                if bstack11l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᗹ") in params and params.get(bstack11l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᗺ")) is True:
                    bstack11lll11ll1l_opy_ = bstack11l1111_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᗻ")
            except Exception as bstack11lll1l1lll_opy_:
                logger.error(bstack11l1111_opy_ (u"ࠢࡋࡕࡒࡒࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡕࡧࡲࡢ࡯ࡶ࠾ࠥࢁࡽࠣᗼ").format(bstack11lll1l1lll_opy_))
        bstack11lll11llll_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1l1l11ll11l_opy_ import bstack1l1l11ll1l1_opy_
        if test_framework_state in bstack1l1l11ll1l1_opy_.bstack1l1l1l1lll1_opy_:
            if bstack11lll11ll1l_opy_ == bstack1l1l11lll11_opy_:
                bstack11lll11llll_opy_ = True
            bstack11lll11ll1l_opy_ = bstack1l1l11ll1ll_opy_
        try:
            platform_index = os.environ[bstack11l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᗽ")]
            target_dir = os.path.join(bstack1lllllll111_opy_, bstack1111111lll_opy_ + str(platform_index),
                                      bstack11lll11ll1l_opy_)
            if bstack11lll11llll_opy_:
                target_dir = os.path.join(target_dir, bstack11lll1ll1ll_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack11l1111_opy_ (u"ࠤࡆࡶࡪࡧࡴࡦࡦ࠲ࡺࡪࡸࡩࡧ࡫ࡨࡨࠥࡺࡡࡳࡩࡨࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᗾ").format(target_dir))
            file_name = os.path.basename(bstack11lll11lll1_opy_)
            bstack11lll1l1ll1_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11lll1l1ll1_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11lll1l11ll_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11lll1l11ll_opy_) + extension)):
                    bstack11lll1l11ll_opy_ += 1
                bstack11lll1l1ll1_opy_ = os.path.join(target_dir, base_name + str(bstack11lll1l11ll_opy_) + extension)
            shutil.copy(bstack11lll11lll1_opy_, bstack11lll1l1ll1_opy_)
            logger.info(bstack11l1111_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡤࡱࡳ࡭ࡪࡪࠠࡵࡱ࠽ࠤࢀࢃࠢᗿ").format(bstack11lll1l1ll1_opy_))
        except Exception as e:
            logger.error(bstack11l1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡱࡴࡼࡩ࡯ࡩࠣࡪ࡮ࡲࡥࠡࡶࡲࠤࡹࡧࡲࡨࡧࡷࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᘀ").format(e))
            return
        finally:
            if bstack11lll1l1l1l_opy_.startswith(bstack11l1111_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᘁ")) or bstack11lll1l1l1l_opy_.startswith(bstack11l1111_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᘂ")):
                try:
                    if bstack11lll11lll1_opy_ is not None and bstack11lll11lll1_opy_.exists():
                        bstack11lll11lll1_opy_.unlink()
                        logger.debug(bstack11l1111_opy_ (u"ࠢࡕࡧࡰࡴࡴࡸࡡࡳࡻࠣࡪ࡮ࡲࡥࠡࡦࡨࡰࡪࡺࡥࡥ࠼ࠣࡿࢂࠨᘃ").format(bstack11lll11lll1_opy_))
                except Exception as ex:
                    logger.error(bstack11l1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡷࡩࡲࡶ࡯ࡳࡣࡵࡽࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠢᘄ").format(ex))
    @staticmethod
    def bstack1l1lll1ll1_opy_() -> None:
        bstack11l1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡄࡦ࡮ࡨࡸࡪࡹࠠࡢ࡮࡯ࠤ࡫ࡵ࡬ࡥࡧࡵࡷࠥࡽࡨࡰࡵࡨࠤࡳࡧ࡭ࡦࡵࠣࡷࡹࡧࡲࡵࠢࡺ࡭ࡹ࡮ࠠࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣࠢࡩࡳࡱࡲ࡯ࡸࡧࡧࠤࡧࡿࠠࡢࠢࡱࡹࡲࡨࡥࡳࠢ࡬ࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩࡧࠣࡹࡸ࡫ࡲࠨࡵࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᘅ")
        bstack11lll11l1ll_opy_ = bstack1lllllll1l1_opy_()
        pattern = re.compile(bstack11l1111_opy_ (u"ࡵ࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࡠࡩ࠱ࠢᘆ"))
        if os.path.exists(bstack11lll11l1ll_opy_):
            for item in os.listdir(bstack11lll11l1ll_opy_):
                bstack11lll11l1l1_opy_ = os.path.join(bstack11lll11l1ll_opy_, item)
                if os.path.isdir(bstack11lll11l1l1_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11lll11l1l1_opy_)
                    except Exception as e:
                        logger.error(bstack11l1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᘇ").format(e))
        else:
            logger.info(bstack11l1111_opy_ (u"࡚ࠧࡨࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠥᘈ").format(bstack11lll11l1ll_opy_))