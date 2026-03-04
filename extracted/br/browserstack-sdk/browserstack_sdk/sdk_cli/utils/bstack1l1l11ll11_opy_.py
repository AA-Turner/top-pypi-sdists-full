# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
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
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.helper import bstack1l111l11lll_opy_
bstack11l11l11lll_opy_ = 100 * 1024 * 1024 # 100 bstack11l11ll1lll_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l11l1lllll_opy_ = bstack1l111l11lll_opy_()
bstack1l111l1l111_opy_ = bstack1lll1l_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨ᣽")
bstack11l1l1llll1_opy_ = bstack1lll1l_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥ᣾")
bstack11l1l1lll11_opy_ = bstack1lll1l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧ᣿")
bstack11l1l1lll1l_opy_ = bstack1lll1l_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᤀ")
bstack11l11ll111l_opy_ = bstack1lll1l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᤁ")
_11l11l1l111_opy_ = threading.local()
def bstack11ll11l1ll1_opy_(test_framework_state, test_hook_state):
    bstack1lll1l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡘ࡫ࡴࠡࡶ࡫ࡩࠥࡩࡵࡳࡴࡨࡲࡹࠦࡴࡦࡵࡷࠤࡪࡼࡥ࡯ࡶࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡺࡨࡳࡧࡤࡨ࠲ࡲ࡯ࡤࡣ࡯ࠤࡸࡺ࡯ࡳࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࡘ࡭࡯ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡷ࡭ࡵࡵ࡭ࡦࠣࡦࡪࠦࡣࡢ࡮࡯ࡩࡩࠦࡢࡺࠢࡷ࡬ࡪࠦࡥࡷࡧࡱࡸࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠦࠨࡴࡷࡦ࡬ࠥࡧࡳࠡࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹ࠯ࠊࠡࠢࠣࠤࡧ࡫ࡦࡰࡴࡨࠤࡦࡴࡹࠡࡨ࡬ࡰࡪࠦࡵࡱ࡮ࡲࡥࡩࡹࠠࡰࡥࡦࡹࡷ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᤂ")
    _11l11l1l111_opy_.test_framework_state = test_framework_state
    _11l11l1l111_opy_.test_hook_state = test_hook_state
def bstack11l11l1l11l_opy_():
    bstack1lll1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡘࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡵࡪࡨࠤࡨࡻࡲࡳࡧࡱࡸࠥࡺࡥࡴࡶࠣࡩࡻ࡫࡮ࡵࠢࡶࡸࡦࡺࡥࠡࡨࡵࡳࡲࠦࡴࡩࡴࡨࡥࡩ࠳࡬ࡰࡥࡤࡰࠥࡹࡴࡰࡴࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡧࠠࡵࡷࡳࡰࡪࠦࠨࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࠬࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࠬࠤࡴࡸࠠࠩࡐࡲࡲࡪ࠲ࠠࡏࡱࡱࡩ࠮ࠦࡩࡧࠢࡱࡳࡹࠦࡳࡦࡶ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᤃ")
    return (
        getattr(_11l11l1l111_opy_, bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪ࠭ᤄ"), None),
        getattr(_11l11l1l111_opy_, bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࠩᤅ"), None)
    )
class bstack111l11lll1_opy_:
    bstack1lll1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡈ࡬ࡰࡪ࡛ࡰ࡭ࡱࡤࡨࡪࡸࠠࡱࡴࡲࡺ࡮ࡪࡥࡴࠢࡩࡹࡳࡩࡴࡪࡱࡱࡥࡱ࡯ࡴࡺࠢࡷࡳࠥࡻࡰ࡭ࡱࡤࡨࠥࡧ࡮ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡨࡡࡴࡧࡧࠤࡴࡴࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࡎࡺࠠࡴࡷࡳࡴࡴࡸࡴࡴࠢࡥࡳࡹ࡮ࠠ࡭ࡱࡦࡥࡱࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࡵࠣࡥࡳࡪࠠࡉࡖࡗࡔ࠴ࡎࡔࡕࡒࡖࠤ࡚ࡘࡌࡴ࠮ࠣࡥࡳࡪࠠࡤࡱࡳ࡭ࡪࡹࠠࡵࡪࡨࠤ࡫࡯࡬ࡦࠢ࡬ࡲࡹࡵࠠࡢࠢࡧࡩࡸ࡯ࡧ࡯ࡣࡷࡩࡩࠐࠠࠡࠢࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡷࡪࡶ࡫࡭ࡳࠦࡴࡩࡧࠣࡹࡸ࡫ࡲࠨࡵࠣ࡬ࡴࡳࡥࠡࡨࡲࡰࡩ࡫ࡲࠡࡷࡱࡨࡪࡸࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࡉࡧࠢࡤࡲࠥࡵࡰࡵ࡫ࡲࡲࡦࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡵࡧࡲࡢ࡯ࡨࡸࡪࡸࠠࠩ࡫ࡱࠤࡏ࡙ࡏࡏࠢࡩࡳࡷࡳࡡࡵࠫࠣ࡭ࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡣࡱࡨࠥࡩ࡯࡯ࡶࡤ࡭ࡳࡹࠠࡢࠢࡷࡶࡺࡺࡨࡺࠢࡹࡥࡱࡻࡥࠋࠢࠣࠤࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦ࡫ࡦࡻࠣࠦࡧࡻࡩ࡭ࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨࠬࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡵࡲࡡࡤࡧࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡪࡴࡲࡤࡦࡴ࠾ࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠬࠋࠢࠣࠤࠥ࡯ࡴࠡࡦࡨࡪࡦࡻ࡬ࡵࡵࠣࡸࡴࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥ࠲ࠏࠦࠠࠡࠢࡗ࡬࡮ࡹࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡱࡩࠤࡦࡪࡤࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥ࡯ࡳࠡࡣࠣࡺࡴ࡯ࡤࠡ࡯ࡨࡸ࡭ࡵࡤ⠕࡫ࡷࠤ࡭ࡧ࡮ࡥ࡮ࡨࡷࠥࡧ࡬࡭ࠢࡨࡶࡷࡵࡲࡴࠢࡪࡶࡦࡩࡥࡧࡷ࡯ࡰࡾࠦࡢࡺࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠍࠤࠥࠦࠠࡵࡪࡨࡱࠥࡧ࡮ࡥࠢࡶ࡭ࡲࡶ࡬ࡺࠢࡵࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥࡽࡩࡵࡪࡲࡹࡹࠦࡴࡩࡴࡲࡻ࡮ࡴࡧࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࡷ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᤆ")
    @staticmethod
    def upload_attachment(bstack11l11l1l1ll_opy_: str, *bstack11l11l11ll1_opy_) -> None:
        if not bstack11l11l1l1ll_opy_ or not bstack11l11l1l1ll_opy_.strip():
            logger.error(bstack1lll1l_opy_ (u"ࠤࡤࡨࡩࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡕࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࠢ࡬ࡷࠥ࡫࡭ࡱࡶࡼࠤࡴࡸࠠࡏࡱࡱࡩ࠳ࠨᤇ"))
            return
        bstack11l11ll1ll1_opy_ = bstack11l11l11ll1_opy_[0] if bstack11l11l11ll1_opy_ and len(bstack11l11l11ll1_opy_) > 0 else None
        bstack11l11l1ll11_opy_ = None
        test_framework_state, test_hook_state = bstack11l11l1l11l_opy_()
        try:
            if bstack11l11l1l1ll_opy_.startswith(bstack1lll1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᤈ")) or bstack11l11l1l1ll_opy_.startswith(bstack1lll1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᤉ")):
                logger.debug(bstack1lll1l_opy_ (u"ࠧࡖࡡࡵࡪࠣ࡭ࡸࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡦࠣࡥࡸࠦࡕࡓࡎ࠾ࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨ࠲ࠧᤊ"))
                url = bstack11l11l1l1ll_opy_
                bstack11l11ll1111_opy_ = str(uuid.uuid4())
                bstack11l11ll11l1_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11l11ll11l1_opy_ or not bstack11l11ll11l1_opy_.strip():
                    bstack11l11ll11l1_opy_ = bstack11l11ll1111_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1lll1l_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩࡥࠢᤋ") + bstack11l11ll1111_opy_ + bstack1lll1l_opy_ (u"ࠢࡠࠤᤌ"),
                                                        suffix=bstack1lll1l_opy_ (u"ࠣࡡࠥᤍ") + bstack11l11ll11l1_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1lll1l_opy_ (u"ࠩࡺࡦࠬᤎ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11l11l1ll11_opy_ = Path(temp_file.name)
                logger.debug(bstack1lll1l_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡧ࡫࡯ࡩࠥࡺ࡯ࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡱࡵࡣࡢࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᤏ").format(bstack11l11l1ll11_opy_))
            else:
                bstack11l11l1ll11_opy_ = Path(bstack11l11l1l1ll_opy_)
                logger.debug(bstack1lll1l_opy_ (u"ࠦࡕࡧࡴࡩࠢ࡬ࡷࠥ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡥࠢࡤࡷࠥࡲ࡯ࡤࡣ࡯ࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂࠨᤐ").format(bstack11l11l1ll11_opy_))
        except Exception as e:
            logger.error(bstack1lll1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡱࡥࡸࡦ࡯࡮ࠡࡨ࡬ࡰࡪࠦࡦࡳࡱࡰࠤࡵࡧࡴࡩ࠱ࡘࡖࡑࡀࠠࡼࡿࠥᤑ").format(e))
            return
        if bstack11l11l1ll11_opy_ is None or not bstack11l11l1ll11_opy_.exists():
            logger.error(bstack1lll1l_opy_ (u"ࠨࡓࡰࡷࡵࡧࡪࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠤᤒ").format(bstack11l11l1ll11_opy_))
            return
        if bstack11l11l1ll11_opy_.stat().st_size > bstack11l11l11lll_opy_:
            logger.error(bstack1lll1l_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡹࡩࡻࡧࠣࡩࡽࡩࡥࡦࡦࡶࠤࡲࡧࡸࡪ࡯ࡸࡱࠥࡧ࡬࡭ࡱࡺࡩࡩࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡼࡿࠥᤓ").format(bstack11l11l11lll_opy_))
            return
        bstack11l11l11l1l_opy_ = bstack1lll1l_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᤔ")
        if bstack11l11ll1ll1_opy_:
            try:
                params = json.loads(bstack11l11ll1ll1_opy_)
                if bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᤕ") in params and params.get(bstack1lll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᤖ")) is True:
                    bstack11l11l11l1l_opy_ = bstack1lll1l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᤗ")
            except Exception as bstack11l11l1lll1_opy_:
                logger.error(bstack1lll1l_opy_ (u"ࠧࡐࡓࡐࡐࠣࡴࡦࡸࡳࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡓࡥࡷࡧ࡭ࡴ࠼ࠣࡿࢂࠨᤘ").format(bstack11l11l1lll1_opy_))
        bstack11l11ll11ll_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1l1lll1lll1_opy_ import bstack1l1ll1lll1l_opy_
        if test_framework_state in bstack1l1ll1lll1l_opy_.bstack11l1lll11l1_opy_:
            if bstack11l11l11l1l_opy_ == bstack11l1l1lll11_opy_:
                bstack11l11ll11ll_opy_ = True
            bstack11l11l11l1l_opy_ = bstack11l1l1lll1l_opy_
        try:
            platform_index = os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᤙ")]
            target_dir = os.path.join(bstack1l11l1lllll_opy_, bstack1l111l1l111_opy_ + str(platform_index),
                                      bstack11l11l11l1l_opy_)
            if bstack11l11ll11ll_opy_:
                target_dir = os.path.join(target_dir, bstack11l11ll111l_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1lll1l_opy_ (u"ࠢࡄࡴࡨࡥࡹ࡫ࡤ࠰ࡸࡨࡶ࡮࡬ࡩࡦࡦࠣࡸࡦࡸࡧࡦࡶࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᤚ").format(target_dir))
            file_name = os.path.basename(bstack11l11l1ll11_opy_)
            bstack11l11l1ll1l_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11l11l1ll1l_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11l11l1l1l1_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11l11l1l1l1_opy_) + extension)):
                    bstack11l11l1l1l1_opy_ += 1
                bstack11l11l1ll1l_opy_ = os.path.join(target_dir, base_name + str(bstack11l11l1l1l1_opy_) + extension)
            shutil.copy(bstack11l11l1ll11_opy_, bstack11l11l1ll1l_opy_)
            logger.info(bstack1lll1l_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡩ࡯ࡱ࡫ࡨࡨࠥࡺ࡯࠻ࠢࡾࢁࠧᤛ").format(bstack11l11l1ll1l_opy_))
        except Exception as e:
            logger.error(bstack1lll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡯ࡲࡺ࡮ࡴࡧࠡࡨ࡬ࡰࡪࠦࡴࡰࠢࡷࡥࡷ࡭ࡥࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᤜ").format(e))
            return
        finally:
            if bstack11l11l1l1ll_opy_.startswith(bstack1lll1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᤝ")) or bstack11l11l1l1ll_opy_.startswith(bstack1lll1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᤞ")):
                try:
                    if bstack11l11l1ll11_opy_ is not None and bstack11l11l1ll11_opy_.exists():
                        bstack11l11l1ll11_opy_.unlink()
                        logger.debug(bstack1lll1l_opy_ (u"࡚ࠧࡥ࡮ࡲࡲࡶࡦࡸࡹࠡࡨ࡬ࡰࡪࠦࡤࡦ࡮ࡨࡸࡪࡪ࠺ࠡࡽࢀࠦ᤟").format(bstack11l11l1ll11_opy_))
                except Exception as ex:
                    logger.error(bstack1lll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡵࡧࡰࡴࡴࡸࡡࡳࡻࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠧᤠ").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack11l11l1llll_opy_, stage=STAGE.bstack1lllll1ll1_opy_, bstack1l11111ll1_opy_=None)
    def bstack1l1l111ll1_opy_() -> None:
        bstack1lll1l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡉ࡫࡬ࡦࡶࡨࡷࠥࡧ࡬࡭ࠢࡩࡳࡱࡪࡥࡳࡵࠣࡻ࡭ࡵࡳࡦࠢࡱࡥࡲ࡫ࡳࠡࡵࡷࡥࡷࡺࠠࡸ࡫ࡷ࡬ࠥࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨࠠࡧࡱ࡯ࡰࡴࡽࡥࡥࠢࡥࡽࠥࡧࠠ࡯ࡷࡰࡦࡪࡸࠠࡪࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡮ࡥࠡࡷࡶࡩࡷ࠭ࡳࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᤡ")
        bstack11l11ll1l1l_opy_ = bstack1l111l11lll_opy_()
        pattern = re.compile(bstack1lll1l_opy_ (u"ࡳࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮࡞ࡧ࠯ࠧᤢ"))
        if os.path.exists(bstack11l11ll1l1l_opy_):
            for item in os.listdir(bstack11l11ll1l1l_opy_):
                bstack11l11ll1l11_opy_ = os.path.join(bstack11l11ll1l1l_opy_, item)
                if os.path.isdir(bstack11l11ll1l11_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11l11ll1l11_opy_)
                    except Exception as e:
                        logger.error(bstack1lll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᤣ").format(e))
        else:
            logger.info(bstack1lll1l_opy_ (u"ࠥࡘ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠣᤤ").format(bstack11l11ll1l1l_opy_))