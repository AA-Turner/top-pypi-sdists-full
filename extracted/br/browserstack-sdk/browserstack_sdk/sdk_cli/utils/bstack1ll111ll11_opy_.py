# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
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
from bstack_utils.helper import bstack1l1l1llllll_opy_
bstack11llll11ll1_opy_ = 100 * 1024 * 1024 # 100 bstack11lll1ll1ll_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l1lll11l1l_opy_ = bstack1l1l1llllll_opy_()
bstack1l1llllll1l_opy_ = bstack1l1l1l1_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᖈ")
bstack1l111111111_opy_ = bstack1l1l1l1_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᖉ")
bstack1l1111111l1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᖊ")
bstack1l111111l11_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᖋ")
bstack11lll1lll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᖌ")
_11llll111ll_opy_ = threading.local()
def bstack1l111l1l11l_opy_(test_framework_state, test_hook_state):
    bstack1l1l1l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡨࡸࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡸࡪࡹࡴࠡࡧࡹࡩࡳࡺࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡࡵࡷࡳࡷࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࡕࡪ࡬ࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡴࡪࡲࡹࡱࡪࠠࡣࡧࠣࡧࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡴࡩࡧࠣࡩࡻ࡫࡮ࡵࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣࠬࡸࡻࡣࡩࠢࡤࡷࠥࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶࠬࠎࠥࠦࠠࠡࡤࡨࡪࡴࡸࡥࠡࡣࡱࡽࠥ࡬ࡩ࡭ࡧࠣࡹࡵࡲ࡯ࡢࡦࡶࠤࡴࡩࡣࡶࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᖍ")
    _11llll111ll_opy_.test_framework_state = test_framework_state
    _11llll111ll_opy_.test_hook_state = test_hook_state
def bstack11llll11111_opy_():
    bstack1l1l1l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡕࡩࡹࡸࡩࡦࡸࡨࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷࡩࡸࡺࠠࡦࡸࡨࡲࡹࠦࡳࡵࡣࡷࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭ࡸࡥࡢࡦ࠰ࡰࡴࡩࡡ࡭ࠢࡶࡸࡴࡸࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡤࠤࡹࡻࡰ࡭ࡧࠣࠬࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨ࠰ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࠩࠡࡱࡵࠤ࠭ࡔ࡯࡯ࡧ࠯ࠤࡓࡵ࡮ࡦࠫࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡷࡪࡺ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᖎ")
    return (
        getattr(_11llll111ll_opy_, bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࠪᖏ"), None),
        getattr(_11llll111ll_opy_, bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪ࠭ᖐ"), None)
    )
class bstack111l11l11_opy_:
    bstack1l1l1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡌࡩ࡭ࡧࡘࡴࡱࡵࡡࡥࡧࡵࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡢ࡮࡬ࡸࡾࠦࡴࡰࠢࡸࡴࡱࡵࡡࡥࠢࡤࡲࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡥࡥࡸ࡫ࡤࠡࡱࡱࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࡋࡷࠤࡸࡻࡰࡱࡱࡵࡸࡸࠦࡢࡰࡶ࡫ࠤࡱࡵࡣࡢ࡮ࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹࠠࡢࡰࡧࠤࡍ࡚ࡔࡑ࠱ࡋࡘ࡙ࡖࡓࠡࡗࡕࡐࡸ࠲ࠠࡢࡰࡧࠤࡨࡵࡰࡪࡧࡶࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪࠦࡩ࡯ࡶࡲࠤࡦࠦࡤࡦࡵ࡬࡫ࡳࡧࡴࡦࡦࠍࠤࠥࠦࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡻ࡮ࡺࡨࡪࡰࠣࡸ࡭࡫ࠠࡶࡵࡨࡶࠬࡹࠠࡩࡱࡰࡩࠥ࡬࡯࡭ࡦࡨࡶࠥࡻ࡮ࡥࡧࡵࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࡍ࡫ࠦࡡ࡯ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡲࡤࡶࡦࡳࡥࡵࡧࡵࠤ࠭࡯࡮ࠡࡌࡖࡓࡓࠦࡦࡰࡴࡰࡥࡹ࠯ࠠࡪࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࡧ࡮ࡥࠢࡦࡳࡳࡺࡡࡪࡰࡶࠤࡦࠦࡴࡳࡷࡷ࡬ࡾࠦࡶࡢ࡮ࡸࡩࠏࠦࠠࠡࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡯ࡪࡿࠠࠣࡤࡸ࡭ࡱࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥ࠰ࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫ࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡲ࡯ࡥࡨ࡫ࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡧࡱ࡯ࡨࡪࡸ࠻ࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨ࠰ࠏࠦࠠࠡࠢ࡬ࡸࠥࡪࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡵࡦࠡࡣࡧࡨࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢ࡬ࡷࠥࡧࠠࡷࡱ࡬ࡨࠥࡳࡥࡵࡪࡲࡨ⠙࡯ࡴࠡࡪࡤࡲࡩࡲࡥࡴࠢࡤࡰࡱࠦࡥࡳࡴࡲࡶࡸࠦࡧࡳࡣࡦࡩ࡫ࡻ࡬࡭ࡻࠣࡦࡾࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠊࠡࠢࠣࠤࡹ࡮ࡥ࡮ࠢࡤࡲࡩࠦࡳࡪ࡯ࡳࡰࡾࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡸ࡭ࡸ࡯ࡸ࡫ࡱ࡫ࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࡴ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᖑ")
    @staticmethod
    def upload_attachment(bstack11lll1lllll_opy_: str, *bstack11lll1ll111_opy_) -> None:
        if not bstack11lll1lllll_opy_ or not bstack11lll1lllll_opy_.strip():
            logger.error(bstack1l1l1l1_opy_ (u"ࠨࡡࡥࡦࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡒࡵࡳࡻ࡯ࡤࡦࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࠦࡩࡴࠢࡨࡱࡵࡺࡹࠡࡱࡵࠤࡓࡵ࡮ࡦ࠰ࠥᖒ"))
            return
        bstack11llll1111l_opy_ = bstack11lll1ll111_opy_[0] if bstack11lll1ll111_opy_ and len(bstack11lll1ll111_opy_) > 0 else None
        bstack11lll1ll1l1_opy_ = None
        test_framework_state, test_hook_state = bstack11llll11111_opy_()
        try:
            if bstack11lll1lllll_opy_.startswith(bstack1l1l1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᖓ")) or bstack11lll1lllll_opy_.startswith(bstack1l1l1l1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᖔ")):
                logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡪࡵࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡪࠠࡢࡵ࡙ࠣࡗࡒ࠻ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠤᖕ"))
                url = bstack11lll1lllll_opy_
                bstack11llll111l1_opy_ = str(uuid.uuid4())
                bstack11llll11lll_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11llll11lll_opy_ or not bstack11llll11lll_opy_.strip():
                    bstack11llll11lll_opy_ = bstack11llll111l1_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1l1l1l1_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࡢࠦᖖ") + bstack11llll111l1_opy_ + bstack1l1l1l1_opy_ (u"ࠦࡤࠨᖗ"),
                                                        suffix=bstack1l1l1l1_opy_ (u"ࠧࡥࠢᖘ") + bstack11llll11lll_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1l1l1l1_opy_ (u"࠭ࡷࡣࠩᖙ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11lll1ll1l1_opy_ = Path(temp_file.name)
                logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤ࡫࡯࡬ࡦࠢࡷࡳࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࡮ࡲࡧࡦࡺࡩࡰࡰ࠽ࠤࢀࢃࠢᖚ").format(bstack11lll1ll1l1_opy_))
            else:
                bstack11lll1ll1l1_opy_ = Path(bstack11lll1lllll_opy_)
                logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡩࡴࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡩࠦࡡࡴࠢ࡯ࡳࡨࡧ࡬ࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠥᖛ").format(bstack11lll1ll1l1_opy_))
        except Exception as e:
            logger.error(bstack1l1l1l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡵࡢࡵࡣ࡬ࡲࠥ࡬ࡩ࡭ࡧࠣࡪࡷࡵ࡭ࠡࡲࡤࡸ࡭࠵ࡕࡓࡎ࠽ࠤࢀࢃࠢᖜ").format(e))
            return
        if bstack11lll1ll1l1_opy_ is None or not bstack11lll1ll1l1_opy_.exists():
            logger.error(bstack1l1l1l1_opy_ (u"ࠥࡗࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨᖝ").format(bstack11lll1ll1l1_opy_))
            return
        if bstack11lll1ll1l1_opy_.stat().st_size > bstack11llll11ll1_opy_:
            logger.error(bstack1l1l1l1_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡶ࡭ࡿ࡫ࠠࡦࡺࡦࡩࡪࡪࡳࠡ࡯ࡤࡼ࡮ࡳࡵ࡮ࠢࡤࡰࡱࡵࡷࡦࡦࠣࡷ࡮ࢀࡥࠡࡱࡩࠤࢀࢃࠢᖞ").format(bstack11llll11ll1_opy_))
            return
        bstack11lll1lll11_opy_ = bstack1l1l1l1_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᖟ")
        if bstack11llll1111l_opy_:
            try:
                params = json.loads(bstack11llll1111l_opy_)
                if bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᖠ") in params and params.get(bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᖡ")) is True:
                    bstack11lll1lll11_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᖢ")
            except Exception as bstack11lll1ll11l_opy_:
                logger.error(bstack1l1l1l1_opy_ (u"ࠤࡍࡗࡔࡔࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡐࡢࡴࡤࡱࡸࡀࠠࡼࡿࠥᖣ").format(bstack11lll1ll11l_opy_))
        bstack11llll1l111_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1ll1ll11ll1_opy_ import bstack1lll1llll11_opy_
        if test_framework_state in bstack1lll1llll11_opy_.bstack1l1111llll1_opy_:
            if bstack11lll1lll11_opy_ == bstack1l1111111l1_opy_:
                bstack11llll1l111_opy_ = True
            bstack11lll1lll11_opy_ = bstack1l111111l11_opy_
        try:
            platform_index = os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᖤ")]
            target_dir = os.path.join(bstack1l1lll11l1l_opy_, bstack1l1llllll1l_opy_ + str(platform_index),
                                      bstack11lll1lll11_opy_)
            if bstack11llll1l111_opy_:
                target_dir = os.path.join(target_dir, bstack11lll1lll1l_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡈࡸࡥࡢࡶࡨࡨ࠴ࡼࡥࡳ࡫ࡩ࡭ࡪࡪࠠࡵࡣࡵ࡫ࡪࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᖥ").format(target_dir))
            file_name = os.path.basename(bstack11lll1ll1l1_opy_)
            bstack11lll1l1lll_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11lll1l1lll_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11lll1llll1_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11lll1llll1_opy_) + extension)):
                    bstack11lll1llll1_opy_ += 1
                bstack11lll1l1lll_opy_ = os.path.join(target_dir, base_name + str(bstack11lll1llll1_opy_) + extension)
            shutil.copy(bstack11lll1ll1l1_opy_, bstack11lll1l1lll_opy_)
            logger.info(bstack1l1l1l1_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡦࡳࡵ࡯ࡥࡥࠢࡷࡳ࠿ࠦࡻࡾࠤᖦ").format(bstack11lll1l1lll_opy_))
        except Exception as e:
            logger.error(bstack1l1l1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡳ࡯ࡷ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࡸࡴࠦࡴࡢࡴࡪࡩࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᖧ").format(e))
            return
        finally:
            if bstack11lll1lllll_opy_.startswith(bstack1l1l1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᖨ")) or bstack11lll1lllll_opy_.startswith(bstack1l1l1l1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᖩ")):
                try:
                    if bstack11lll1ll1l1_opy_ is not None and bstack11lll1ll1l1_opy_.exists():
                        bstack11lll1ll1l1_opy_.unlink()
                        logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡗࡩࡲࡶ࡯ࡳࡣࡵࡽࠥ࡬ࡩ࡭ࡧࠣࡨࡪࡲࡥࡵࡧࡧ࠾ࠥࢁࡽࠣᖪ").format(bstack11lll1ll1l1_opy_))
                except Exception as ex:
                    logger.error(bstack1l1l1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤᖫ").format(ex))
    @staticmethod
    def bstack111l1111l_opy_() -> None:
        bstack1l1l1l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡆࡨࡰࡪࡺࡥࡴࠢࡤࡰࡱࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࡸࡪࡲࡷࡪࠦ࡮ࡢ࡯ࡨࡷࠥࡹࡴࡢࡴࡷࠤࡼ࡯ࡴࡩ࡙ࠢࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥࠤ࡫ࡵ࡬࡭ࡱࡺࡩࡩࠦࡢࡺࠢࡤࠤࡳࡻ࡭ࡣࡧࡵࠤ࡮ࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࡶ࡫ࡩࠥࡻࡳࡦࡴࠪࡷࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᖬ")
        bstack11llll11l11_opy_ = bstack1l1l1llllll_opy_()
        pattern = re.compile(bstack1l1l1l1_opy_ (u"ࡷࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࡢࡤࠬࠤᖭ"))
        if os.path.exists(bstack11llll11l11_opy_):
            for item in os.listdir(bstack11llll11l11_opy_):
                bstack11llll11l1l_opy_ = os.path.join(bstack11llll11l11_opy_, item)
                if os.path.isdir(bstack11llll11l1l_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11llll11l1l_opy_)
                    except Exception as e:
                        logger.error(bstack1l1l1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᖮ").format(e))
        else:
            logger.info(bstack1l1l1l1_opy_ (u"ࠢࡕࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧᖯ").format(bstack11llll11l11_opy_))