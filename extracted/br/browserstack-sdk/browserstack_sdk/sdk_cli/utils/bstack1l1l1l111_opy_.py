# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
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
from bstack_utils.helper import bstack1l11ll1111l_opy_
bstack11l1l1l1l1l_opy_ = 100 * 1024 * 1024 # 100 bstack11l1l1l1111_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l111lll1l1_opy_ = bstack1l11ll1111l_opy_()
bstack1l11lll1111_opy_ = bstack11l1l11_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧ៖")
bstack11l1lll1l11_opy_ = bstack11l1l11_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤៗ")
bstack11l1lll111l_opy_ = bstack11l1l11_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦ៘")
bstack11l1lll1111_opy_ = bstack11l1l11_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦ៙")
bstack11l1l11l111_opy_ = bstack11l1l11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ៚")
_11l1l111lll_opy_ = threading.local()
def bstack11ll1l11ll1_opy_(test_framework_state, test_hook_state):
    bstack11l1l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡗࡪࡺࠠࡵࡪࡨࠤࡨࡻࡲࡳࡧࡱࡸࠥࡺࡥࡴࡶࠣࡩࡻ࡫࡮ࡵࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡹ࡮ࡲࡦࡣࡧ࠱ࡱࡵࡣࡢ࡮ࠣࡷࡹࡵࡲࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࡗ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡶ࡬ࡴࡻ࡬ࡥࠢࡥࡩࠥࡩࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡶ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥ࠮ࡳࡶࡥ࡫ࠤࡦࡹࠠࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠮ࠐࠠࠡࠢࠣࡦࡪ࡬࡯ࡳࡧࠣࡥࡳࡿࠠࡧ࡫࡯ࡩࠥࡻࡰ࡭ࡱࡤࡨࡸࠦ࡯ࡤࡥࡸࡶ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ៛")
    _11l1l111lll_opy_.test_framework_state = test_framework_state
    _11l1l111lll_opy_.test_hook_state = test_hook_state
def bstack11l1l11l11l_opy_():
    bstack11l1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡗ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡴࡩࡧࠣࡧࡺࡸࡲࡦࡰࡷࠤࡹ࡫ࡳࡵࠢࡨࡺࡪࡴࡴࠡࡵࡷࡥࡹ࡫ࠠࡧࡴࡲࡱࠥࡺࡨࡳࡧࡤࡨ࠲ࡲ࡯ࡤࡣ࡯ࠤࡸࡺ࡯ࡳࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡦࠦࡴࡶࡲ࡯ࡩࠥ࠮ࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪ࠲ࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࠫࠣࡳࡷࠦࠨࡏࡱࡱࡩ࠱ࠦࡎࡰࡰࡨ࠭ࠥ࡯ࡦࠡࡰࡲࡸࠥࡹࡥࡵ࠰ࠍࠤࠥࠦࠠࠣࠤࠥៜ")
    return (
        getattr(_11l1l111lll_opy_, bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࠬ៝"), None),
        getattr(_11l1l111lll_opy_, bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࠨ៞"), None)
    )
class bstack1ll11l1ll_opy_:
    bstack11l1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡇ࡫࡯ࡩ࡚ࡶ࡬ࡰࡣࡧࡩࡷࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰࡤࡰ࡮ࡺࡹࠡࡶࡲࠤࡺࡶ࡬ࡰࡣࡧࠤࡦࡴࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡧࡧࡳࡦࡦࠣࡳࡳࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࡍࡹࠦࡳࡶࡲࡳࡳࡷࡺࡳࠡࡤࡲࡸ࡭ࠦ࡬ࡰࡥࡤࡰࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࡴࠢࡤࡲࡩࠦࡈࡕࡖࡓ࠳ࡍ࡚ࡔࡑࡕ࡙ࠣࡗࡒࡳ࠭ࠢࡤࡲࡩࠦࡣࡰࡲ࡬ࡩࡸࠦࡴࡩࡧࠣࡪ࡮ࡲࡥࠡ࡫ࡱࡸࡴࠦࡡࠡࡦࡨࡷ࡮࡭࡮ࡢࡶࡨࡨࠏࠦࠠࠡࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡽࡩࡵࡪ࡬ࡲࠥࡺࡨࡦࠢࡸࡷࡪࡸࠧࡴࠢ࡫ࡳࡲ࡫ࠠࡧࡱ࡯ࡨࡪࡸࠠࡶࡰࡧࡩࡷࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࡏࡦࠡࡣࡱࠤࡴࡶࡴࡪࡱࡱࡥࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࠦࠨࡪࡰࠣࡎࡘࡕࡎࠡࡨࡲࡶࡲࡧࡴࠪࠢ࡬ࡷࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡢࡰࡧࠤࡨࡵ࡮ࡵࡣ࡬ࡲࡸࠦࡡࠡࡶࡵࡹࡹ࡮ࡹࠡࡸࡤࡰࡺ࡫ࠊࠡࠢࠣࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡱࡥࡺࠢࠥࡦࡺ࡯࡬ࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧ࠲ࠠࡵࡪࡨࠤ࡫࡯࡬ࡦࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡴࡱࡧࡣࡦࡦࠣ࡭ࡳࠦࡴࡩࡧࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡩࡳࡱࡪࡥࡳ࠽ࠣࡳࡹ࡮ࡥࡳࡹ࡬ࡷࡪ࠲ࠊࠡࠢࠣࠤ࡮ࡺࠠࡥࡧࡩࡥࡺࡲࡴࡴࠢࡷࡳࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤ࠱ࠎࠥࠦࠠࠡࡖ࡫࡭ࡸࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡰࡨࠣࡥࡩࡪ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤ࡮ࡹࠠࡢࠢࡹࡳ࡮ࡪࠠ࡮ࡧࡷ࡬ࡴࡪ⠔ࡪࡶࠣ࡬ࡦࡴࡤ࡭ࡧࡶࠤࡦࡲ࡬ࠡࡧࡵࡶࡴࡸࡳࠡࡩࡵࡥࡨ࡫ࡦࡶ࡮࡯ࡽࠥࡨࡹࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠌࠣࠤࠥࠦࡴࡩࡧࡰࠤࡦࡴࡤࠡࡵ࡬ࡱࡵࡲࡹࠡࡴࡨࡸࡺࡸ࡮ࡪࡰࡪࠤࡼ࡯ࡴࡩࡱࡸࡸࠥࡺࡨࡳࡱࡺ࡭ࡳ࡭ࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࡶ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ៟")
    @staticmethod
    def upload_attachment(bstack11l1l11ll11_opy_: str, *bstack11l1l1l11ll_opy_) -> None:
        if not bstack11l1l11ll11_opy_ or not bstack11l1l11ll11_opy_.strip():
            logger.error(bstack11l1l11_opy_ (u"ࠣࡣࡧࡨࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡔࡷࡵࡶࡪࡦࡨࡨࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࠡ࡫ࡶࠤࡪࡳࡰࡵࡻࠣࡳࡷࠦࡎࡰࡰࡨ࠲ࠧ០"))
            return
        bstack11l1l1l111l_opy_ = bstack11l1l1l11ll_opy_[0] if bstack11l1l1l11ll_opy_ and len(bstack11l1l1l11ll_opy_) > 0 else None
        bstack11l1l11llll_opy_ = None
        test_framework_state, test_hook_state = bstack11l1l11l11l_opy_()
        try:
            if bstack11l1l11ll11_opy_.startswith(bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ១")) or bstack11l1l11ll11_opy_.startswith(bstack11l1l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ២")):
                logger.debug(bstack11l1l11_opy_ (u"ࠦࡕࡧࡴࡩࠢ࡬ࡷࠥ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡥࠢࡤࡷ࡛ࠥࡒࡍ࠽ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠦ៣"))
                url = bstack11l1l11ll11_opy_
                bstack11l1l1l11l1_opy_ = str(uuid.uuid4())
                bstack11l1l111ll1_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11l1l111ll1_opy_ or not bstack11l1l111ll1_opy_.strip():
                    bstack11l1l111ll1_opy_ = bstack11l1l1l11l1_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack11l1l11_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࡤࠨ៤") + bstack11l1l1l11l1_opy_ + bstack11l1l11_opy_ (u"ࠨ࡟ࠣ៥"),
                                                        suffix=bstack11l1l11_opy_ (u"ࠢࡠࠤ៦") + bstack11l1l111ll1_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack11l1l11_opy_ (u"ࠨࡹࡥࠫ៧")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11l1l11llll_opy_ = Path(temp_file.name)
                logger.debug(bstack11l1l11_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡦࡪ࡮ࡨࠤࡹࡵࠠࡵࡧࡰࡴࡴࡸࡡࡳࡻࠣࡰࡴࡩࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ៨").format(bstack11l1l11llll_opy_))
            else:
                bstack11l1l11llll_opy_ = Path(bstack11l1l11ll11_opy_)
                logger.debug(bstack11l1l11_opy_ (u"ࠥࡔࡦࡺࡨࠡ࡫ࡶࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡤࠡࡣࡶࠤࡱࡵࡣࡢ࡮ࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠧ៩").format(bstack11l1l11llll_opy_))
        except Exception as e:
            logger.error(bstack11l1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡰࡤࡷࡥ࡮ࡴࠠࡧ࡫࡯ࡩࠥ࡬ࡲࡰ࡯ࠣࡴࡦࡺࡨ࠰ࡗࡕࡐ࠿ࠦࡻࡾࠤ៪").format(e))
            return
        if bstack11l1l11llll_opy_ is None or not bstack11l1l11llll_opy_.exists():
            logger.error(bstack11l1l11_opy_ (u"࡙ࠧ࡯ࡶࡴࡦࡩࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠣ៫").format(bstack11l1l11llll_opy_))
            return
        if bstack11l1l11llll_opy_.stat().st_size > bstack11l1l1l1l1l_opy_:
            logger.error(bstack11l1l11_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡸ࡯ࡺࡦࠢࡨࡼࡨ࡫ࡥࡥࡵࠣࡱࡦࡾࡩ࡮ࡷࡰࠤࡦࡲ࡬ࡰࡹࡨࡨࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡻࡾࠤ៬").format(bstack11l1l1l1l1l_opy_))
            return
        bstack11l1l1l1lll_opy_ = bstack11l1l11_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥ៭")
        if bstack11l1l1l111l_opy_:
            try:
                params = json.loads(bstack11l1l1l111l_opy_)
                if bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥ៮") in params and params.get(bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦ៯")) is True:
                    bstack11l1l1l1lll_opy_ = bstack11l1l11_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢ៰")
            except Exception as bstack11l1l11l1ll_opy_:
                logger.error(bstack11l1l11_opy_ (u"ࠦࡏ࡙ࡏࡏࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡒࡤࡶࡦࡳࡳ࠻ࠢࡾࢁࠧ៱").format(bstack11l1l11l1ll_opy_))
        bstack11l1l1l1l11_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1ll111lllll_opy_ import bstack1ll11ll11l1_opy_
        if test_framework_state in bstack1ll11ll11l1_opy_.bstack11lll111ll1_opy_:
            if bstack11l1l1l1lll_opy_ == bstack11l1lll111l_opy_:
                bstack11l1l1l1l11_opy_ = True
            bstack11l1l1l1lll_opy_ = bstack11l1lll1111_opy_
        try:
            platform_index = os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ៲")]
            target_dir = os.path.join(bstack1l111lll1l1_opy_, bstack1l11lll1111_opy_ + str(platform_index),
                                      bstack11l1l1l1lll_opy_)
            if bstack11l1l1l1l11_opy_:
                target_dir = os.path.join(target_dir, bstack11l1l11l111_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack11l1l11_opy_ (u"ࠨࡃࡳࡧࡤࡸࡪࡪ࠯ࡷࡧࡵ࡭࡫࡯ࡥࡥࠢࡷࡥࡷ࡭ࡥࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤ៳").format(target_dir))
            file_name = os.path.basename(bstack11l1l11llll_opy_)
            bstack11l1l111l1l_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11l1l111l1l_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11l1l11lll1_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11l1l11lll1_opy_) + extension)):
                    bstack11l1l11lll1_opy_ += 1
                bstack11l1l111l1l_opy_ = os.path.join(target_dir, base_name + str(bstack11l1l11lll1_opy_) + extension)
            shutil.copy(bstack11l1l11llll_opy_, bstack11l1l111l1l_opy_)
            logger.info(bstack11l1l11_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡨࡵࡰࡪࡧࡧࠤࡹࡵ࠺ࠡࡽࢀࠦ៴").format(bstack11l1l111l1l_opy_))
        except Exception as e:
            logger.error(bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠ࡮ࡱࡹ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩࠥࡺ࡯ࠡࡶࡤࡶ࡬࡫ࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣ៵").format(e))
            return
        finally:
            if bstack11l1l11ll11_opy_.startswith(bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ៶")) or bstack11l1l11ll11_opy_.startswith(bstack11l1l11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ៷")):
                try:
                    if bstack11l1l11llll_opy_ is not None and bstack11l1l11llll_opy_.exists():
                        bstack11l1l11llll_opy_.unlink()
                        logger.debug(bstack11l1l11_opy_ (u"࡙ࠦ࡫࡭ࡱࡱࡵࡥࡷࡿࠠࡧ࡫࡯ࡩࠥࡪࡥ࡭ࡧࡷࡩࡩࡀࠠࡼࡿࠥ៸").format(bstack11l1l11llll_opy_))
                except Exception as ex:
                    logger.error(bstack11l1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠦ៹").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack11l1l11ll1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_, bstack1l111l11l_opy_=None)
    def bstack1llll1llll_opy_() -> None:
        bstack11l1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡈࡪࡲࡥࡵࡧࡶࠤࡦࡲ࡬ࠡࡨࡲࡰࡩ࡫ࡲࡴࠢࡺ࡬ࡴࡹࡥࠡࡰࡤࡱࡪࡹࠠࡴࡶࡤࡶࡹࠦࡷࡪࡶ࡫ࠤ࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧࠦࡦࡰ࡮࡯ࡳࡼ࡫ࡤࠡࡤࡼࠤࡦࠦ࡮ࡶ࡯ࡥࡩࡷࠦࡩ࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡫ࠠࡶࡵࡨࡶࠬࡹࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ៺")
        bstack11l1l1l1ll1_opy_ = bstack1l11ll1111l_opy_()
        pattern = re.compile(bstack11l1l11_opy_ (u"ࡲࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭࡝ࡦ࠮ࠦ៻"))
        if os.path.exists(bstack11l1l1l1ll1_opy_):
            for item in os.listdir(bstack11l1l1l1ll1_opy_):
                bstack11l1l11l1l1_opy_ = os.path.join(bstack11l1l1l1ll1_opy_, item)
                if os.path.isdir(bstack11l1l11l1l1_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11l1l11l1l1_opy_)
                    except Exception as e:
                        logger.error(bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤ៼").format(e))
        else:
            logger.info(bstack11l1l11_opy_ (u"ࠤࡗ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠢ៽").format(bstack11l1l1l1ll1_opy_))