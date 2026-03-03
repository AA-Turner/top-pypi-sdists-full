# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
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
from bstack_utils.helper import bstack1l11llll11l_opy_
bstack11l1l1l1111_opy_ = 100 * 1024 * 1024 # 100 bstack11l1l11ll11_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l11lll1111_opy_ = bstack1l11llll11l_opy_()
bstack1l11lll1l11_opy_ = bstack11ll111_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤ៓")
bstack11l1lll1l1l_opy_ = bstack11ll111_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ។")
bstack11l1lll11ll_opy_ = bstack11ll111_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣ៕")
bstack11l1lll11l1_opy_ = bstack11ll111_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣ៖")
bstack11l1l11ll1l_opy_ = bstack11ll111_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧៗ")
_11l1l111ll1_opy_ = threading.local()
def bstack11ll111llll_opy_(test_framework_state, test_hook_state):
    bstack11ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡧࡷࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷࡩࡸࡺࠠࡦࡸࡨࡲࡹࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡶ࡫ࡶࡪࡧࡤ࠮࡮ࡲࡧࡦࡲࠠࡴࡶࡲࡶࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡳࡩࡱࡸࡰࡩࠦࡢࡦࠢࡦࡥࡱࡲࡥࡥࠢࡥࡽࠥࡺࡨࡦࠢࡨࡺࡪࡴࡴࠡࡪࡤࡲࡩࡲࡥࡳࠢࠫࡷࡺࡩࡨࠡࡣࡶࠤࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵࠫࠍࠤࠥࠦࠠࡣࡧࡩࡳࡷ࡫ࠠࡢࡰࡼࠤ࡫࡯࡬ࡦࠢࡸࡴࡱࡵࡡࡥࡵࠣࡳࡨࡩࡵࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ៘")
    _11l1l111ll1_opy_.test_framework_state = test_framework_state
    _11l1l111ll1_opy_.test_hook_state = test_hook_state
def bstack11l1l111l1l_opy_():
    bstack11ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡔࡨࡸࡷ࡯ࡥࡷࡧࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶࡨࡷࡹࠦࡥࡷࡧࡱࡸࠥࡹࡴࡢࡶࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡࡵࡷࡳࡷࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡣࠣࡸࡺࡶ࡬ࡦࠢࠫࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧ࠯ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪ࠯ࠠࡰࡴࠣࠬࡓࡵ࡮ࡦ࠮ࠣࡒࡴࡴࡥࠪࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ៙")
    return (
        getattr(_11l1l111ll1_opy_, bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࠩ៚"), None),
        getattr(_11l1l111ll1_opy_, bstack11ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࠬ៛"), None)
    )
class bstack11l1ll11l1_opy_:
    bstack11ll111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡋ࡯࡬ࡦࡗࡳࡰࡴࡧࡤࡦࡴࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡡ࡭࡫ࡷࡽࠥࡺ࡯ࠡࡷࡳࡰࡴࡧࡤࠡࡣࡱࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࡊࡶࠣࡷࡺࡶࡰࡰࡴࡷࡷࠥࡨ࡯ࡵࡪࠣࡰࡴࡩࡡ࡭ࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࡸࠦࡡ࡯ࡦࠣࡌ࡙࡚ࡐ࠰ࡊࡗࡘࡕ࡙ࠠࡖࡔࡏࡷ࠱ࠦࡡ࡯ࡦࠣࡧࡴࡶࡩࡦࡵࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࡵࡱࠣࡥࠥࡪࡥࡴ࡫ࡪࡲࡦࡺࡥࡥࠌࠣࠤࠥࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡺ࡭ࡹ࡮ࡩ࡯ࠢࡷ࡬ࡪࠦࡵࡴࡧࡵࠫࡸࠦࡨࡰ࡯ࡨࠤ࡫ࡵ࡬ࡥࡧࡵࠤࡺࡴࡤࡦࡴࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࡌࡪࠥࡧ࡮ࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࠣࠬ࡮ࡴࠠࡋࡕࡒࡒࠥ࡬࡯ࡳ࡯ࡤࡸ࠮ࠦࡩࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡦࡴࡤࠡࡥࡲࡲࡹࡧࡩ࡯ࡵࠣࡥࠥࡺࡲࡶࡶ࡫ࡽࠥࡼࡡ࡭ࡷࡨࠎࠥࠦࠠࠡࡨࡲࡶࠥࡺࡨࡦࠢ࡮ࡩࡾࠦࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤ࠯ࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡱ࡮ࡤࡧࡪࡪࠠࡪࡰࠣࡸ࡭࡫ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡦࡰ࡮ࡧࡩࡷࡁࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧ࠯ࠎࠥࠦࠠࠡ࡫ࡷࠤࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ࠮ࠋࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡺࡪࡸࡳࡪࡱࡱࠤࡴ࡬ࠠࡢࡦࡧࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡ࡫ࡶࠤࡦࠦࡶࡰ࡫ࡧࠤࡲ࡫ࡴࡩࡱࡧ⠘࡮ࡺࠠࡩࡣࡱࡨࡱ࡫ࡳࠡࡣ࡯ࡰࠥ࡫ࡲࡳࡱࡵࡷࠥ࡭ࡲࡢࡥࡨࡪࡺࡲ࡬ࡺࠢࡥࡽࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠐࠠࠡࠢࠣࡸ࡭࡫࡭ࠡࡣࡱࡨࠥࡹࡩ࡮ࡲ࡯ࡽࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡷ࡬ࡷࡵࡷࡪࡰࡪࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࡳ࠯ࠌࠣࠤࠥࠦࠢࠣࠤៜ")
    @staticmethod
    def upload_attachment(bstack11l1l11l1ll_opy_: str, *bstack11l1l1l111l_opy_) -> None:
        if not bstack11l1l11l1ll_opy_ or not bstack11l1l11l1ll_opy_.strip():
            logger.error(bstack11ll111_opy_ (u"ࠧࡧࡤࡥࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡑࡴࡲࡺ࡮ࡪࡥࡥࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡯ࡳࠡࡧࡰࡴࡹࡿࠠࡰࡴࠣࡒࡴࡴࡥ࠯ࠤ៝"))
            return
        bstack11l1l1l11l1_opy_ = bstack11l1l1l111l_opy_[0] if bstack11l1l1l111l_opy_ and len(bstack11l1l1l111l_opy_) > 0 else None
        bstack11l1l11l1l1_opy_ = None
        test_framework_state, test_hook_state = bstack11l1l111l1l_opy_()
        try:
            if bstack11l1l11l1ll_opy_.startswith(bstack11ll111_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ៞")) or bstack11l1l11l1ll_opy_.startswith(bstack11ll111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ៟")):
                logger.debug(bstack11ll111_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡩࡴࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡩࠦࡡࡴࠢࡘࡖࡑࡁࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠣ០"))
                url = bstack11l1l11l1ll_opy_
                bstack11l1l1l1l1l_opy_ = str(uuid.uuid4())
                bstack11l1l111l11_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11l1l111l11_opy_ or not bstack11l1l111l11_opy_.strip():
                    bstack11l1l111l11_opy_ = bstack11l1l1l1l1l_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack11ll111_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࡡࠥ១") + bstack11l1l1l1l1l_opy_ + bstack11ll111_opy_ (u"ࠥࡣࠧ២"),
                                                        suffix=bstack11ll111_opy_ (u"ࠦࡤࠨ៣") + bstack11l1l111l11_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack11ll111_opy_ (u"ࠬࡽࡢࠨ៤")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11l1l11l1l1_opy_ = Path(temp_file.name)
                logger.debug(bstack11ll111_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡪ࡮ࡲࡥࠡࡶࡲࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࡭ࡱࡦࡥࡹ࡯࡯࡯࠼ࠣࡿࢂࠨ៥").format(bstack11l1l11l1l1_opy_))
            else:
                bstack11l1l11l1l1_opy_ = Path(bstack11l1l11l1ll_opy_)
                logger.debug(bstack11ll111_opy_ (u"ࠢࡑࡣࡷ࡬ࠥ࡯ࡳࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡨࠥࡧࡳࠡ࡮ࡲࡧࡦࡲࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤ៦").format(bstack11l1l11l1l1_opy_))
        except Exception as e:
            logger.error(bstack11ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡴࡨࡴࡢ࡫ࡱࠤ࡫࡯࡬ࡦࠢࡩࡶࡴࡳࠠࡱࡣࡷ࡬࠴࡛ࡒࡍ࠼ࠣࡿࢂࠨ៧").format(e))
            return
        if bstack11l1l11l1l1_opy_ is None or not bstack11l1l11l1l1_opy_.exists():
            logger.error(bstack11ll111_opy_ (u"ࠤࡖࡳࡺࡸࡣࡦࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧ៨").format(bstack11l1l11l1l1_opy_))
            return
        if bstack11l1l11l1l1_opy_.stat().st_size > bstack11l1l1l1111_opy_:
            logger.error(bstack11ll111_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡵ࡬ࡾࡪࠦࡥࡹࡥࡨࡩࡩࡹࠠ࡮ࡣࡻ࡭ࡲࡻ࡭ࠡࡣ࡯ࡰࡴࡽࡥࡥࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡿࢂࠨ៩").format(bstack11l1l1l1111_opy_))
            return
        bstack11l1l111lll_opy_ = bstack11ll111_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢ៪")
        if bstack11l1l1l11l1_opy_:
            try:
                params = json.loads(bstack11l1l1l11l1_opy_)
                if bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢ៫") in params and params.get(bstack11ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣ៬")) is True:
                    bstack11l1l111lll_opy_ = bstack11ll111_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦ៭")
            except Exception as bstack11l1l11l11l_opy_:
                logger.error(bstack11ll111_opy_ (u"ࠣࡌࡖࡓࡓࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡖࡡࡳࡣࡰࡷ࠿ࠦࡻࡾࠤ៮").format(bstack11l1l11l11l_opy_))
        bstack11l1l1l1ll1_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1ll111111ll_opy_ import bstack1ll11l1llll_opy_
        if test_framework_state in bstack1ll11l1llll_opy_.bstack11ll1l1l11l_opy_:
            if bstack11l1l111lll_opy_ == bstack11l1lll11ll_opy_:
                bstack11l1l1l1ll1_opy_ = True
            bstack11l1l111lll_opy_ = bstack11l1lll11l1_opy_
        try:
            platform_index = os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ៯")]
            target_dir = os.path.join(bstack1l11lll1111_opy_, bstack1l11lll1l11_opy_ + str(platform_index),
                                      bstack11l1l111lll_opy_)
            if bstack11l1l1l1ll1_opy_:
                target_dir = os.path.join(target_dir, bstack11l1l11ll1l_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack11ll111_opy_ (u"ࠥࡇࡷ࡫ࡡࡵࡧࡧ࠳ࡻ࡫ࡲࡪࡨ࡬ࡩࡩࠦࡴࡢࡴࡪࡩࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨ៰").format(target_dir))
            file_name = os.path.basename(bstack11l1l11l1l1_opy_)
            bstack11l1l11llll_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11l1l11llll_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11l1l1l11ll_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11l1l1l11ll_opy_) + extension)):
                    bstack11l1l1l11ll_opy_ += 1
                bstack11l1l11llll_opy_ = os.path.join(target_dir, base_name + str(bstack11l1l1l11ll_opy_) + extension)
            shutil.copy(bstack11l1l11l1l1_opy_, bstack11l1l11llll_opy_)
            logger.info(bstack11ll111_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡥࡲࡴ࡮࡫ࡤࠡࡶࡲ࠾ࠥࢁࡽࠣ៱").format(bstack11l1l11llll_opy_))
        except Exception as e:
            logger.error(bstack11ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡲࡵࡶࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࡷࡳࠥࡺࡡࡳࡩࡨࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧ៲").format(e))
            return
        finally:
            if bstack11l1l11l1ll_opy_.startswith(bstack11ll111_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ៳")) or bstack11l1l11l1ll_opy_.startswith(bstack11ll111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ៴")):
                try:
                    if bstack11l1l11l1l1_opy_ is not None and bstack11l1l11l1l1_opy_.exists():
                        bstack11l1l11l1l1_opy_.unlink()
                        logger.debug(bstack11ll111_opy_ (u"ࠣࡖࡨࡱࡵࡵࡲࡢࡴࡼࠤ࡫࡯࡬ࡦࠢࡧࡩࡱ࡫ࡴࡦࡦ࠽ࠤࢀࢃࠢ៵").format(bstack11l1l11l1l1_opy_))
                except Exception as ex:
                    logger.error(bstack11ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣ៶").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack11l1l1l1l11_opy_, stage=STAGE.bstack1111l1111_opy_, bstack11ll11ll11_opy_=None)
    def bstack1ll11ll1ll_opy_() -> None:
        bstack11ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡧ࡯ࡩࡹ࡫ࡳࠡࡣ࡯ࡰࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࡷࡩࡱࡶࡩࠥࡴࡡ࡮ࡧࡶࠤࡸࡺࡡࡳࡶࠣࡻ࡮ࡺࡨࠡࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤࠣࡪࡴࡲ࡬ࡰࡹࡨࡨࠥࡨࡹࠡࡣࠣࡲࡺࡳࡢࡦࡴࠣ࡭ࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪࡨࠤࡺࡹࡥࡳࠩࡶࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ៷")
        bstack11l1l11lll1_opy_ = bstack1l11llll11l_opy_()
        pattern = re.compile(bstack11ll111_opy_ (u"ࡶ࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࡡࡪࠫࠣ៸"))
        if os.path.exists(bstack11l1l11lll1_opy_):
            for item in os.listdir(bstack11l1l11lll1_opy_):
                bstack11l1l11l111_opy_ = os.path.join(bstack11l1l11lll1_opy_, item)
                if os.path.isdir(bstack11l1l11l111_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11l1l11l111_opy_)
                    except Exception as e:
                        logger.error(bstack11ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨ៹").format(e))
        else:
            logger.info(bstack11ll111_opy_ (u"ࠨࡔࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠦ៺").format(bstack11l1l11lll1_opy_))