# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
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
from bstack_utils.helper import bstack1l11l11l11l_opy_
bstack11l1l111111_opy_ = 100 * 1024 * 1024 # 100 bstack11l11ll1ll1_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l11l1ll11l_opy_ = bstack1l11l11l11l_opy_()
bstack1l111l1l1l1_opy_ = bstack11l11_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤ៌")
bstack11l1ll11l11_opy_ = bstack11l11_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ៍")
bstack11l1ll111ll_opy_ = bstack11l11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣ៎")
bstack11l1ll11l1l_opy_ = bstack11l11_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠣ៏")
bstack11l1l1111l1_opy_ = bstack11l11_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠧ័")
_11l1l11111l_opy_ = threading.local()
def bstack11ll1l1l1l1_opy_(test_framework_state, test_hook_state):
    bstack11l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡧࡷࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷࡩࡸࡺࠠࡦࡸࡨࡲࡹࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡶ࡫ࡶࡪࡧࡤ࠮࡮ࡲࡧࡦࡲࠠࡴࡶࡲࡶࡦ࡭ࡥ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡳࡩࡱࡸࡰࡩࠦࡢࡦࠢࡦࡥࡱࡲࡥࡥࠢࡥࡽࠥࡺࡨࡦࠢࡨࡺࡪࡴࡴࠡࡪࡤࡲࡩࡲࡥࡳࠢࠫࡷࡺࡩࡨࠡࡣࡶࠤࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵࠫࠍࠤࠥࠦࠠࡣࡧࡩࡳࡷ࡫ࠠࡢࡰࡼࠤ࡫࡯࡬ࡦࠢࡸࡴࡱࡵࡡࡥࡵࠣࡳࡨࡩࡵࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ៑")
    _11l1l11111l_opy_.test_framework_state = test_framework_state
    _11l1l11111l_opy_.test_hook_state = test_hook_state
def bstack11l1l111l11_opy_():
    bstack11l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡔࡨࡸࡷ࡯ࡥࡷࡧࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶࡨࡷࡹࠦࡥࡷࡧࡱࡸࠥࡹࡴࡢࡶࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡࡵࡷࡳࡷࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡣࠣࡸࡺࡶ࡬ࡦࠢࠫࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧ࠯ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪ࠯ࠠࡰࡴࠣࠬࡓࡵ࡮ࡦ࠮ࠣࡒࡴࡴࡥࠪࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡶࡩࡹ࠴ࠊࠡࠢࠣࠤࠧࠨ្ࠢ")
    return (
        getattr(_11l1l11111l_opy_, bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࠩ៓"), None),
        getattr(_11l1l11111l_opy_, bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࠬ។"), None)
    )
class bstack1l1ll111l_opy_:
    bstack11l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡋ࡯࡬ࡦࡗࡳࡰࡴࡧࡤࡦࡴࠣࡴࡷࡵࡶࡪࡦࡨࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡡ࡭࡫ࡷࡽࠥࡺ࡯ࠡࡷࡳࡰࡴࡧࡤࠡࡣࡱࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࡊࡶࠣࡷࡺࡶࡰࡰࡴࡷࡷࠥࡨ࡯ࡵࡪࠣࡰࡴࡩࡡ࡭ࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࡸࠦࡡ࡯ࡦࠣࡌ࡙࡚ࡐ࠰ࡊࡗࡘࡕ࡙ࠠࡖࡔࡏࡷ࠱ࠦࡡ࡯ࡦࠣࡧࡴࡶࡩࡦࡵࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࡵࡱࠣࡥࠥࡪࡥࡴ࡫ࡪࡲࡦࡺࡥࡥࠌࠣࠤࠥࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡺ࡭ࡹ࡮ࡩ࡯ࠢࡷ࡬ࡪࠦࡵࡴࡧࡵࠫࡸࠦࡨࡰ࡯ࡨࠤ࡫ࡵ࡬ࡥࡧࡵࠤࡺࡴࡤࡦࡴࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࡌࡪࠥࡧ࡮ࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࠣࠬ࡮ࡴࠠࡋࡕࡒࡒࠥ࡬࡯ࡳ࡯ࡤࡸ࠮ࠦࡩࡴࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡦࡴࡤࠡࡥࡲࡲࡹࡧࡩ࡯ࡵࠣࡥࠥࡺࡲࡶࡶ࡫ࡽࠥࡼࡡ࡭ࡷࡨࠎࠥࠦࠠࠡࡨࡲࡶࠥࡺࡨࡦࠢ࡮ࡩࡾࠦࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤ࠯ࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡱ࡮ࡤࡧࡪࡪࠠࡪࡰࠣࡸ࡭࡫ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡦࡰ࡮ࡧࡩࡷࡁࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧ࠯ࠎࠥࠦࠠࠡ࡫ࡷࠤࡩ࡫ࡦࡢࡷ࡯ࡸࡸࠦࡴࡰࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ࠮ࠋࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡺࡪࡸࡳࡪࡱࡱࠤࡴ࡬ࠠࡢࡦࡧࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡ࡫ࡶࠤࡦࠦࡶࡰ࡫ࡧࠤࡲ࡫ࡴࡩࡱࡧ⠘࡮ࡺࠠࡩࡣࡱࡨࡱ࡫ࡳࠡࡣ࡯ࡰࠥ࡫ࡲࡳࡱࡵࡷࠥ࡭ࡲࡢࡥࡨࡪࡺࡲ࡬ࡺࠢࡥࡽࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠐࠠࠡࠢࠣࡸ࡭࡫࡭ࠡࡣࡱࡨࠥࡹࡩ࡮ࡲ࡯ࡽࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡷ࡬ࡷࡵࡷࡪࡰࡪࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࡳ࠯ࠌࠣࠤࠥࠦࠢࠣࠤ៕")
    @staticmethod
    def upload_attachment(bstack11l11lll111_opy_: str, *bstack11l11llll11_opy_) -> None:
        if not bstack11l11lll111_opy_ or not bstack11l11lll111_opy_.strip():
            logger.error(bstack11l11_opy_ (u"ࠧࡧࡤࡥࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡑࡴࡲࡺ࡮ࡪࡥࡥࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡯ࡳࠡࡧࡰࡴࡹࡿࠠࡰࡴࠣࡒࡴࡴࡥ࠯ࠤ៖"))
            return
        bstack11l11llllll_opy_ = bstack11l11llll11_opy_[0] if bstack11l11llll11_opy_ and len(bstack11l11llll11_opy_) > 0 else None
        bstack11l11lll11l_opy_ = None
        test_framework_state, test_hook_state = bstack11l1l111l11_opy_()
        try:
            if bstack11l11lll111_opy_.startswith(bstack11l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢៗ")) or bstack11l11lll111_opy_.startswith(bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ៘")):
                logger.debug(bstack11l11_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡩࡴࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡩࠦࡡࡴࠢࡘࡖࡑࡁࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠣ៙"))
                url = bstack11l11lll111_opy_
                bstack11l11ll1l1l_opy_ = str(uuid.uuid4())
                bstack11l1l111l1l_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11l1l111l1l_opy_ or not bstack11l1l111l1l_opy_.strip():
                    bstack11l1l111l1l_opy_ = bstack11l11ll1l1l_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack11l11_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࡡࠥ៚") + bstack11l11ll1l1l_opy_ + bstack11l11_opy_ (u"ࠥࡣࠧ៛"),
                                                        suffix=bstack11l11_opy_ (u"ࠦࡤࠨៜ") + bstack11l1l111l1l_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack11l11_opy_ (u"ࠬࡽࡢࠨ៝")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11l11lll11l_opy_ = Path(temp_file.name)
                logger.debug(bstack11l11_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡪ࡮ࡲࡥࠡࡶࡲࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࡭ࡱࡦࡥࡹ࡯࡯࡯࠼ࠣࡿࢂࠨ៞").format(bstack11l11lll11l_opy_))
            else:
                bstack11l11lll11l_opy_ = Path(bstack11l11lll111_opy_)
                logger.debug(bstack11l11_opy_ (u"ࠢࡑࡣࡷ࡬ࠥ࡯ࡳࠡ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡨࠥࡧࡳࠡ࡮ࡲࡧࡦࡲࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤ៟").format(bstack11l11lll11l_opy_))
        except Exception as e:
            logger.error(bstack11l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡴࡨࡴࡢ࡫ࡱࠤ࡫࡯࡬ࡦࠢࡩࡶࡴࡳࠠࡱࡣࡷ࡬࠴࡛ࡒࡍ࠼ࠣࡿࢂࠨ០").format(e))
            return
        if bstack11l11lll11l_opy_ is None or not bstack11l11lll11l_opy_.exists():
            logger.error(bstack11l11_opy_ (u"ࠤࡖࡳࡺࡸࡣࡦࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧ១").format(bstack11l11lll11l_opy_))
            return
        if bstack11l11lll11l_opy_.stat().st_size > bstack11l1l111111_opy_:
            logger.error(bstack11l11_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡵ࡬ࡾࡪࠦࡥࡹࡥࡨࡩࡩࡹࠠ࡮ࡣࡻ࡭ࡲࡻ࡭ࠡࡣ࡯ࡰࡴࡽࡥࡥࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡿࢂࠨ២").format(bstack11l1l111111_opy_))
            return
        bstack11l11lll1ll_opy_ = bstack11l11_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢ៣")
        if bstack11l11llllll_opy_:
            try:
                params = json.loads(bstack11l11llllll_opy_)
                if bstack11l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢ៤") in params and params.get(bstack11l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣ៥")) is True:
                    bstack11l11lll1ll_opy_ = bstack11l11_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦ៦")
            except Exception as bstack11l11lll1l1_opy_:
                logger.error(bstack11l11_opy_ (u"ࠣࡌࡖࡓࡓࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡖࡡࡳࡣࡰࡷ࠿ࠦࡻࡾࠤ៧").format(bstack11l11lll1l1_opy_))
        bstack11l1l111lll_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1ll11l1l1l1_opy_ import bstack1ll111lll1l_opy_
        if test_framework_state in bstack1ll111lll1l_opy_.bstack11l1ll1l1l1_opy_:
            if bstack11l11lll1ll_opy_ == bstack11l1ll111ll_opy_:
                bstack11l1l111lll_opy_ = True
            bstack11l11lll1ll_opy_ = bstack11l1ll11l1l_opy_
        try:
            platform_index = os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ៨")]
            target_dir = os.path.join(bstack1l11l1ll11l_opy_, bstack1l111l1l1l1_opy_ + str(platform_index),
                                      bstack11l11lll1ll_opy_)
            if bstack11l1l111lll_opy_:
                target_dir = os.path.join(target_dir, bstack11l1l1111l1_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack11l11_opy_ (u"ࠥࡇࡷ࡫ࡡࡵࡧࡧ࠳ࡻ࡫ࡲࡪࡨ࡬ࡩࡩࠦࡴࡢࡴࡪࡩࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨ៩").format(target_dir))
            file_name = os.path.basename(bstack11l11lll11l_opy_)
            bstack11l11llll1l_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11l11llll1l_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11l11lllll1_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11l11lllll1_opy_) + extension)):
                    bstack11l11lllll1_opy_ += 1
                bstack11l11llll1l_opy_ = os.path.join(target_dir, base_name + str(bstack11l11lllll1_opy_) + extension)
            shutil.copy(bstack11l11lll11l_opy_, bstack11l11llll1l_opy_)
            logger.info(bstack11l11_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡥࡲࡴ࡮࡫ࡤࠡࡶࡲ࠾ࠥࢁࡽࠣ៪").format(bstack11l11llll1l_opy_))
        except Exception as e:
            logger.error(bstack11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡲࡵࡶࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࡷࡳࠥࡺࡡࡳࡩࡨࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧ៫").format(e))
            return
        finally:
            if bstack11l11lll111_opy_.startswith(bstack11l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ៬")) or bstack11l11lll111_opy_.startswith(bstack11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ៭")):
                try:
                    if bstack11l11lll11l_opy_ is not None and bstack11l11lll11l_opy_.exists():
                        bstack11l11lll11l_opy_.unlink()
                        logger.debug(bstack11l11_opy_ (u"ࠣࡖࡨࡱࡵࡵࡲࡢࡴࡼࠤ࡫࡯࡬ࡦࠢࡧࡩࡱ࡫ࡴࡦࡦ࠽ࠤࢀࢃࠢ៮").format(bstack11l11lll11l_opy_))
                except Exception as ex:
                    logger.error(bstack11l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦࡦࡪ࡮ࡨ࠾ࠥࢁࡽࠣ៯").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack11l1l1111ll_opy_, stage=STAGE.bstack111ll11l1_opy_, bstack11l111l11l_opy_=None)
    def bstack11l1lll1l_opy_() -> None:
        bstack11l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡅࡧ࡯ࡩࡹ࡫ࡳࠡࡣ࡯ࡰࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࡷࡩࡱࡶࡩࠥࡴࡡ࡮ࡧࡶࠤࡸࡺࡡࡳࡶࠣࡻ࡮ࡺࡨࠡࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤࠣࡪࡴࡲ࡬ࡰࡹࡨࡨࠥࡨࡹࠡࡣࠣࡲࡺࡳࡢࡦࡴࠣ࡭ࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪࡨࠤࡺࡹࡥࡳࠩࡶࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ៰")
        bstack11l11ll1lll_opy_ = bstack1l11l11l11l_opy_()
        pattern = re.compile(bstack11l11_opy_ (u"ࡶ࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࡡࡪࠫࠣ៱"))
        if os.path.exists(bstack11l11ll1lll_opy_):
            for item in os.listdir(bstack11l11ll1lll_opy_):
                bstack11l1l111ll1_opy_ = os.path.join(bstack11l11ll1lll_opy_, item)
                if os.path.isdir(bstack11l1l111ll1_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11l1l111ll1_opy_)
                    except Exception as e:
                        logger.error(bstack11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨ៲").format(e))
        else:
            logger.info(bstack11l11_opy_ (u"ࠨࡔࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠦ៳").format(bstack11l11ll1lll_opy_))