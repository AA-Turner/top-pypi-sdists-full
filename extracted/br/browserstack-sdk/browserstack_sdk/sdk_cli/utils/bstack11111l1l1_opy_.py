# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
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
from bstack_utils.helper import bstack11lllll1lll_opy_
bstack111llll1ll1_opy_ = 100 * 1024 * 1024 # 100 bstack111lllllll1_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l1111l1lll_opy_ = bstack11lllll1lll_opy_()
bstack1l1111l11ll_opy_ = bstack11lll1_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧ᧱")
bstack11l11l1llll_opy_ = bstack11lll1_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤ᧲")
bstack11l11ll11ll_opy_ = bstack11lll1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦ᧳")
bstack11l11ll1111_opy_ = bstack11lll1_opy_ (u"ࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠦ᧴")
bstack11l11111ll1_opy_ = bstack11lll1_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠣ᧵")
_111llllll11_opy_ = threading.local()
def bstack11l1l1llll1_opy_(test_framework_state, test_hook_state):
    bstack11lll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡗࡪࡺࠠࡵࡪࡨࠤࡨࡻࡲࡳࡧࡱࡸࠥࡺࡥࡴࡶࠣࡩࡻ࡫࡮ࡵࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡹ࡮ࡲࡦࡣࡧ࠱ࡱࡵࡣࡢ࡮ࠣࡷࡹࡵࡲࡢࡩࡨ࠲ࠏࠦࠠࠡࠢࡗ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡶ࡬ࡴࡻ࡬ࡥࠢࡥࡩࠥࡩࡡ࡭࡮ࡨࡨࠥࡨࡹࠡࡶ࡫ࡩࠥ࡫ࡶࡦࡰࡷࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥ࠮ࡳࡶࡥ࡫ࠤࡦࡹࠠࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠮ࠐࠠࠡࠢࠣࡦࡪ࡬࡯ࡳࡧࠣࡥࡳࡿࠠࡧ࡫࡯ࡩࠥࡻࡰ࡭ࡱࡤࡨࡸࠦ࡯ࡤࡥࡸࡶ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ᧶")
    _111llllll11_opy_.test_framework_state = test_framework_state
    _111llllll11_opy_.test_hook_state = test_hook_state
def bstack111lllll111_opy_():
    bstack11lll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡗ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡴࡩࡧࠣࡧࡺࡸࡲࡦࡰࡷࠤࡹ࡫ࡳࡵࠢࡨࡺࡪࡴࡴࠡࡵࡷࡥࡹ࡫ࠠࡧࡴࡲࡱࠥࡺࡨࡳࡧࡤࡨ࠲ࡲ࡯ࡤࡣ࡯ࠤࡸࡺ࡯ࡳࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡦࠦࡴࡶࡲ࡯ࡩࠥ࠮ࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪ࠲ࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࠫࠣࡳࡷࠦࠨࡏࡱࡱࡩ࠱ࠦࡎࡰࡰࡨ࠭ࠥ࡯ࡦࠡࡰࡲࡸࠥࡹࡥࡵ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ᧷")
    return (
        getattr(_111llllll11_opy_, bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࠬ᧸"), None),
        getattr(_111llllll11_opy_, bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࠨ᧹"), None)
    )
class bstack1ll1l1111_opy_:
    bstack11lll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡇ࡫࡯ࡩ࡚ࡶ࡬ࡰࡣࡧࡩࡷࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰࡤࡰ࡮ࡺࡹࠡࡶࡲࠤࡺࡶ࡬ࡰࡣࡧࠤࡦࡴࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡧࡧࡳࡦࡦࠣࡳࡳࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࡍࡹࠦࡳࡶࡲࡳࡳࡷࡺࡳࠡࡤࡲࡸ࡭ࠦ࡬ࡰࡥࡤࡰࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࡴࠢࡤࡲࡩࠦࡈࡕࡖࡓ࠳ࡍ࡚ࡔࡑࡕ࡙ࠣࡗࡒࡳ࠭ࠢࡤࡲࡩࠦࡣࡰࡲ࡬ࡩࡸࠦࡴࡩࡧࠣࡪ࡮ࡲࡥࠡ࡫ࡱࡸࡴࠦࡡࠡࡦࡨࡷ࡮࡭࡮ࡢࡶࡨࡨࠏࠦࠠࠡࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡽࡩࡵࡪ࡬ࡲࠥࡺࡨࡦࠢࡸࡷࡪࡸࠧࡴࠢ࡫ࡳࡲ࡫ࠠࡧࡱ࡯ࡨࡪࡸࠠࡶࡰࡧࡩࡷࠦࡾ࠰࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠰ࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠮ࠋࠢࠣࠤࠥࡏࡦࠡࡣࡱࠤࡴࡶࡴࡪࡱࡱࡥࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࠦࠨࡪࡰࠣࡎࡘࡕࡎࠡࡨࡲࡶࡲࡧࡴࠪࠢ࡬ࡷࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠠࡢࡰࡧࠤࡨࡵ࡮ࡵࡣ࡬ࡲࡸࠦࡡࠡࡶࡵࡹࡹ࡮ࡹࠡࡸࡤࡰࡺ࡫ࠊࠡࠢࠣࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡱࡥࡺࠢࠥࡦࡺ࡯࡬ࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧ࠲ࠠࡵࡪࡨࠤ࡫࡯࡬ࡦࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡴࡱࡧࡣࡦࡦࠣ࡭ࡳࠦࡴࡩࡧࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡩࡳࡱࡪࡥࡳ࠽ࠣࡳࡹ࡮ࡥࡳࡹ࡬ࡷࡪ࠲ࠊࠡࠢࠣࠤ࡮ࡺࠠࡥࡧࡩࡥࡺࡲࡴࡴࠢࡷࡳࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤ࠱ࠎࠥࠦࠠࠡࡖ࡫࡭ࡸࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡰࡨࠣࡥࡩࡪ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤ࡮ࡹࠠࡢࠢࡹࡳ࡮ࡪࠠ࡮ࡧࡷ࡬ࡴࡪ⠔ࡪࡶࠣ࡬ࡦࡴࡤ࡭ࡧࡶࠤࡦࡲ࡬ࠡࡧࡵࡶࡴࡸࡳࠡࡩࡵࡥࡨ࡫ࡦࡶ࡮࡯ࡽࠥࡨࡹࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠌࠣࠤࠥࠦࡴࡩࡧࡰࠤࡦࡴࡤࠡࡵ࡬ࡱࡵࡲࡹࠡࡴࡨࡸࡺࡸ࡮ࡪࡰࡪࠤࡼ࡯ࡴࡩࡱࡸࡸࠥࡺࡨࡳࡱࡺ࡭ࡳ࡭ࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࡶ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ᧺")
    @staticmethod
    def upload_attachment(bstack11l11111l1l_opy_: str, *bstack11l1111111l_opy_) -> None:
        if not bstack11l11111l1l_opy_ or not bstack11l11111l1l_opy_.strip():
            logger.error(bstack11lll1_opy_ (u"ࠣࡣࡧࡨࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡔࡷࡵࡶࡪࡦࡨࡨࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࠡ࡫ࡶࠤࡪࡳࡰࡵࡻࠣࡳࡷࠦࡎࡰࡰࡨ࠲ࠧ᧻"))
            return
        bstack11l11111lll_opy_ = bstack11l1111111l_opy_[0] if bstack11l1111111l_opy_ and len(bstack11l1111111l_opy_) > 0 else None
        bstack11l111111ll_opy_ = None
        test_framework_state, test_hook_state = bstack111lllll111_opy_()
        try:
            if bstack11l11111l1l_opy_.startswith(bstack11lll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ᧼")) or bstack11l11111l1l_opy_.startswith(bstack11lll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ᧽")):
                logger.debug(bstack11lll1_opy_ (u"ࠦࡕࡧࡴࡩࠢ࡬ࡷࠥ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡥࠢࡤࡷ࡛ࠥࡒࡍ࠽ࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠦ᧾"))
                url = bstack11l11111l1l_opy_
                bstack111llll1lll_opy_ = str(uuid.uuid4())
                bstack11l111111l1_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11l111111l1_opy_ or not bstack11l111111l1_opy_.strip():
                    bstack11l111111l1_opy_ = bstack111llll1lll_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack11lll1_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࡤࠨ᧿") + bstack111llll1lll_opy_ + bstack11lll1_opy_ (u"ࠨ࡟ࠣᨀ"),
                                                        suffix=bstack11lll1_opy_ (u"ࠢࡠࠤᨁ") + bstack11l111111l1_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack11lll1_opy_ (u"ࠨࡹࡥࠫᨂ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11l111111ll_opy_ = Path(temp_file.name)
                logger.debug(bstack11lll1_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡦࡪ࡮ࡨࠤࡹࡵࠠࡵࡧࡰࡴࡴࡸࡡࡳࡻࠣࡰࡴࡩࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᨃ").format(bstack11l111111ll_opy_))
            else:
                bstack11l111111ll_opy_ = Path(bstack11l11111l1l_opy_)
                logger.debug(bstack11lll1_opy_ (u"ࠥࡔࡦࡺࡨࠡ࡫ࡶࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡤࠡࡣࡶࠤࡱࡵࡣࡢ࡮ࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠧᨄ").format(bstack11l111111ll_opy_))
        except Exception as e:
            logger.error(bstack11lll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡰࡤࡷࡥ࡮ࡴࠠࡧ࡫࡯ࡩࠥ࡬ࡲࡰ࡯ࠣࡴࡦࡺࡨ࠰ࡗࡕࡐ࠿ࠦࡻࡾࠤᨅ").format(e))
            return
        if bstack11l111111ll_opy_ is None or not bstack11l111111ll_opy_.exists():
            logger.error(bstack11lll1_opy_ (u"࡙ࠧ࡯ࡶࡴࡦࡩࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠣᨆ").format(bstack11l111111ll_opy_))
            return
        if bstack11l111111ll_opy_.stat().st_size > bstack111llll1ll1_opy_:
            logger.error(bstack11lll1_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡸ࡯ࡺࡦࠢࡨࡼࡨ࡫ࡥࡥࡵࠣࡱࡦࡾࡩ࡮ࡷࡰࠤࡦࡲ࡬ࡰࡹࡨࡨࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡻࡾࠤᨇ").format(bstack111llll1ll1_opy_))
            return
        bstack111llllllll_opy_ = bstack11lll1_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᨈ")
        if bstack11l11111lll_opy_:
            try:
                params = json.loads(bstack11l11111lll_opy_)
                if bstack11lll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᨉ") in params and params.get(bstack11lll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᨊ")) is True:
                    bstack111llllllll_opy_ = bstack11lll1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᨋ")
            except Exception as bstack11l11111l11_opy_:
                logger.error(bstack11lll1_opy_ (u"ࠦࡏ࡙ࡏࡏࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡒࡤࡶࡦࡳࡳ࠻ࠢࡾࢁࠧᨌ").format(bstack11l11111l11_opy_))
        bstack111lllll1ll_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1ll1111l11l_opy_ import bstack1l1ll1111l1_opy_
        if test_framework_state in bstack1l1ll1111l1_opy_.bstack11l1ll11l1l_opy_:
            if bstack111llllllll_opy_ == bstack11l11ll11ll_opy_:
                bstack111lllll1ll_opy_ = True
            bstack111llllllll_opy_ = bstack11l11ll1111_opy_
        try:
            platform_index = os.environ[bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᨍ")]
            target_dir = os.path.join(bstack1l1111l1lll_opy_, bstack1l1111l11ll_opy_ + str(platform_index),
                                      bstack111llllllll_opy_)
            if bstack111lllll1ll_opy_:
                target_dir = os.path.join(target_dir, bstack11l11111ll1_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack11lll1_opy_ (u"ࠨࡃࡳࡧࡤࡸࡪࡪ࠯ࡷࡧࡵ࡭࡫࡯ࡥࡥࠢࡷࡥࡷ࡭ࡥࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᨎ").format(target_dir))
            file_name = os.path.basename(bstack11l111111ll_opy_)
            bstack11l11111111_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11l11111111_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack111lllll11l_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack111lllll11l_opy_) + extension)):
                    bstack111lllll11l_opy_ += 1
                bstack11l11111111_opy_ = os.path.join(target_dir, base_name + str(bstack111lllll11l_opy_) + extension)
            shutil.copy(bstack11l111111ll_opy_, bstack11l11111111_opy_)
            logger.info(bstack11lll1_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡨࡵࡰࡪࡧࡧࠤࡹࡵ࠺ࠡࡽࢀࠦᨏ").format(bstack11l11111111_opy_))
        except Exception as e:
            logger.error(bstack11lll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠ࡮ࡱࡹ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩࠥࡺ࡯ࠡࡶࡤࡶ࡬࡫ࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᨐ").format(e))
            return
        finally:
            if bstack11l11111l1l_opy_.startswith(bstack11lll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᨑ")) or bstack11l11111l1l_opy_.startswith(bstack11lll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᨒ")):
                try:
                    if bstack11l111111ll_opy_ is not None and bstack11l111111ll_opy_.exists():
                        bstack11l111111ll_opy_.unlink()
                        logger.debug(bstack11lll1_opy_ (u"࡙ࠦ࡫࡭ࡱࡱࡵࡥࡷࡿࠠࡧ࡫࡯ࡩࠥࡪࡥ࡭ࡧࡷࡩࡩࡀࠠࡼࡿࠥᨓ").format(bstack11l111111ll_opy_))
                except Exception as ex:
                    logger.error(bstack11lll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡩ࡭ࡱ࡫࠺ࠡࡽࢀࠦᨔ").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack11l1111l111_opy_, stage=STAGE.bstack1lllllll11_opy_, bstack1l11ll11l_opy_=None)
    def bstack111llll111_opy_() -> None:
        bstack11lll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡈࡪࡲࡥࡵࡧࡶࠤࡦࡲ࡬ࠡࡨࡲࡰࡩ࡫ࡲࡴࠢࡺ࡬ࡴࡹࡥࠡࡰࡤࡱࡪࡹࠠࡴࡶࡤࡶࡹࠦࡷࡪࡶ࡫ࠤ࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧࠦࡦࡰ࡮࡯ࡳࡼ࡫ࡤࠡࡤࡼࠤࡦࠦ࡮ࡶ࡯ࡥࡩࡷࠦࡩ࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡫ࠠࡶࡵࡨࡶࠬࡹࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᨕ")
        bstack111llllll1l_opy_ = bstack11lllll1lll_opy_()
        pattern = re.compile(bstack11lll1_opy_ (u"ࡲࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭࡝ࡦ࠮ࠦᨖ"))
        if os.path.exists(bstack111llllll1l_opy_):
            for item in os.listdir(bstack111llllll1l_opy_):
                bstack111lllll1l1_opy_ = os.path.join(bstack111llllll1l_opy_, item)
                if os.path.isdir(bstack111lllll1l1_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack111lllll1l1_opy_)
                    except Exception as e:
                        logger.error(bstack11lll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤᨗ").format(e))
        else:
            logger.info(bstack11lll1_opy_ (u"ࠤࡗ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃᨘࠢ").format(bstack111llllll1l_opy_))