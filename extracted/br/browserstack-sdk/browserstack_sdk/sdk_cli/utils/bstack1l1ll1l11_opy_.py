# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
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
from bstack_utils.helper import bstack1l111llll1l_opy_
bstack11l11l1111l_opy_ = 100 * 1024 * 1024 # 100 bstack11l111llll1_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l111l1ll11_opy_ = bstack1l111llll1l_opy_()
bstack1l1111l1l1l_opy_ = bstack1111l_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᦩ")
bstack11l1l11ll11_opy_ = bstack1111l_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᦪ")
bstack11l1l11l111_opy_ = bstack1111l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᦫ")
bstack11l1l111lll_opy_ = bstack1111l_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤ᦬")
bstack11l111l1l1l_opy_ = bstack1111l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ᦭")
_11l111lllll_opy_ = threading.local()
def bstack11l1l1lll11_opy_(test_framework_state, test_hook_state):
    bstack1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡨࡸࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡸࡪࡹࡴࠡࡧࡹࡩࡳࡺࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡷ࡬ࡷ࡫ࡡࡥ࠯࡯ࡳࡨࡧ࡬ࠡࡵࡷࡳࡷࡧࡧࡦ࠰ࠍࠤࠥࠦࠠࡕࡪ࡬ࡷࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡴࡪࡲࡹࡱࡪࠠࡣࡧࠣࡧࡦࡲ࡬ࡦࡦࠣࡦࡾࠦࡴࡩࡧࠣࡩࡻ࡫࡮ࡵࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣࠬࡸࡻࡣࡩࠢࡤࡷࠥࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶࠬࠎࠥࠦࠠࠡࡤࡨࡪࡴࡸࡥࠡࡣࡱࡽࠥ࡬ࡩ࡭ࡧࠣࡹࡵࡲ࡯ࡢࡦࡶࠤࡴࡩࡣࡶࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ᦮")
    _11l111lllll_opy_.test_framework_state = test_framework_state
    _11l111lllll_opy_.test_hook_state = test_hook_state
def bstack11l111l1111_opy_():
    bstack1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡕࡩࡹࡸࡩࡦࡸࡨࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡷࡩࡸࡺࠠࡦࡸࡨࡲࡹࠦࡳࡵࡣࡷࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭ࡸࡥࡢࡦ࠰ࡰࡴࡩࡡ࡭ࠢࡶࡸࡴࡸࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡤࠤࡹࡻࡰ࡭ࡧࠣࠬࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨ࠰ࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࠩࠡࡱࡵࠤ࠭ࡔ࡯࡯ࡧ࠯ࠤࡓࡵ࡮ࡦࠫࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡷࡪࡺ࠮ࠋࠢࠣࠤࠥࠨࠢࠣ᦯")
    return (
        getattr(_11l111lllll_opy_, bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࠪᦰ"), None),
        getattr(_11l111lllll_opy_, bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪ࠭ᦱ"), None)
    )
class bstack111l11l1_opy_:
    bstack1111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡌࡩ࡭ࡧࡘࡴࡱࡵࡡࡥࡧࡵࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡢ࡮࡬ࡸࡾࠦࡴࡰࠢࡸࡴࡱࡵࡡࡥࠢࡤࡲࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡥࡥࡸ࡫ࡤࠡࡱࡱࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࡋࡷࠤࡸࡻࡰࡱࡱࡵࡸࡸࠦࡢࡰࡶ࡫ࠤࡱࡵࡣࡢ࡮ࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹࠠࡢࡰࡧࠤࡍ࡚ࡔࡑ࠱ࡋࡘ࡙ࡖࡓࠡࡗࡕࡐࡸ࠲ࠠࡢࡰࡧࠤࡨࡵࡰࡪࡧࡶࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪࠦࡩ࡯ࡶࡲࠤࡦࠦࡤࡦࡵ࡬࡫ࡳࡧࡴࡦࡦࠍࠤࠥࠦࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡻ࡮ࡺࡨࡪࡰࠣࡸ࡭࡫ࠠࡶࡵࡨࡶࠬࡹࠠࡩࡱࡰࡩࠥ࡬࡯࡭ࡦࡨࡶࠥࡻ࡮ࡥࡧࡵࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࡍ࡫ࠦࡡ࡯ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡲࡤࡶࡦࡳࡥࡵࡧࡵࠤ࠭࡯࡮ࠡࡌࡖࡓࡓࠦࡦࡰࡴࡰࡥࡹ࠯ࠠࡪࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࡧ࡮ࡥࠢࡦࡳࡳࡺࡡࡪࡰࡶࠤࡦࠦࡴࡳࡷࡷ࡬ࡾࠦࡶࡢ࡮ࡸࡩࠏࠦࠠࠡࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡯ࡪࡿࠠࠣࡤࡸ࡭ࡱࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥ࠰ࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫ࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡲ࡯ࡥࡨ࡫ࡤࠡ࡫ࡱࠤࡹ࡮ࡥࠡࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨࠠࡧࡱ࡯ࡨࡪࡸ࠻ࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨ࠰ࠏࠦࠠࠡࠢ࡬ࡸࠥࡪࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡵࡦࠡࡣࡧࡨࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢ࡬ࡷࠥࡧࠠࡷࡱ࡬ࡨࠥࡳࡥࡵࡪࡲࡨ⠙࡯ࡴࠡࡪࡤࡲࡩࡲࡥࡴࠢࡤࡰࡱࠦࡥࡳࡴࡲࡶࡸࠦࡧࡳࡣࡦࡩ࡫ࡻ࡬࡭ࡻࠣࡦࡾࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠊࠡࠢࠣࠤࡹ࡮ࡥ࡮ࠢࡤࡲࡩࠦࡳࡪ࡯ࡳࡰࡾࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡸ࡭ࡸ࡯ࡸ࡫ࡱ࡫ࠥ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࡴ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᦲ")
    @staticmethod
    def upload_attachment(bstack11l111lll11_opy_: str, *bstack11l1111llll_opy_) -> None:
        if not bstack11l111lll11_opy_ or not bstack11l111lll11_opy_.strip():
            logger.error(bstack1111l_opy_ (u"ࠨࡡࡥࡦࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡒࡵࡳࡻ࡯ࡤࡦࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࠦࡩࡴࠢࡨࡱࡵࡺࡹࠡࡱࡵࠤࡓࡵ࡮ࡦ࠰ࠥᦳ"))
            return
        bstack11l111ll111_opy_ = bstack11l1111llll_opy_[0] if bstack11l1111llll_opy_ and len(bstack11l1111llll_opy_) > 0 else None
        bstack11l111l11l1_opy_ = None
        test_framework_state, test_hook_state = bstack11l111l1111_opy_()
        try:
            if bstack11l111lll11_opy_.startswith(bstack1111l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᦴ")) or bstack11l111lll11_opy_.startswith(bstack1111l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᦵ")):
                logger.debug(bstack1111l_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡪࡵࠣ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡪࠠࡢࡵ࡙ࠣࡗࡒ࠻ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠤᦶ"))
                url = bstack11l111lll11_opy_
                bstack11l11l11111_opy_ = str(uuid.uuid4())
                bstack11l111lll1l_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11l111lll1l_opy_ or not bstack11l111lll1l_opy_.strip():
                    bstack11l111lll1l_opy_ = bstack11l11l11111_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1111l_opy_ (u"ࠥࡹࡵࡲ࡯ࡢࡦࡢࠦᦷ") + bstack11l11l11111_opy_ + bstack1111l_opy_ (u"ࠦࡤࠨᦸ"),
                                                        suffix=bstack1111l_opy_ (u"ࠧࡥࠢᦹ") + bstack11l111lll1l_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1111l_opy_ (u"࠭ࡷࡣࠩᦺ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11l111l11l1_opy_ = Path(temp_file.name)
                logger.debug(bstack1111l_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤ࡫࡯࡬ࡦࠢࡷࡳࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࡮ࡲࡧࡦࡺࡩࡰࡰ࠽ࠤࢀࢃࠢᦻ").format(bstack11l111l11l1_opy_))
            else:
                bstack11l111l11l1_opy_ = Path(bstack11l111lll11_opy_)
                logger.debug(bstack1111l_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡩࡴࠢ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡩࠦࡡࡴࠢ࡯ࡳࡨࡧ࡬ࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠥᦼ").format(bstack11l111l11l1_opy_))
        except Exception as e:
            logger.error(bstack1111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡵࡢࡵࡣ࡬ࡲࠥ࡬ࡩ࡭ࡧࠣࡪࡷࡵ࡭ࠡࡲࡤࡸ࡭࠵ࡕࡓࡎ࠽ࠤࢀࢃࠢᦽ").format(e))
            return
        if bstack11l111l11l1_opy_ is None or not bstack11l111l11l1_opy_.exists():
            logger.error(bstack1111l_opy_ (u"ࠥࡗࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂࠨᦾ").format(bstack11l111l11l1_opy_))
            return
        if bstack11l111l11l1_opy_.stat().st_size > bstack11l11l1111l_opy_:
            logger.error(bstack1111l_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡶ࡭ࡿ࡫ࠠࡦࡺࡦࡩࡪࡪࡳࠡ࡯ࡤࡼ࡮ࡳࡵ࡮ࠢࡤࡰࡱࡵࡷࡦࡦࠣࡷ࡮ࢀࡥࠡࡱࡩࠤࢀࢃࠢᦿ").format(bstack11l11l1111l_opy_))
            return
        bstack11l111ll1ll_opy_ = bstack1111l_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᧀ")
        if bstack11l111ll111_opy_:
            try:
                params = json.loads(bstack11l111ll111_opy_)
                if bstack1111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᧁ") in params and params.get(bstack1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤᧂ")) is True:
                    bstack11l111ll1ll_opy_ = bstack1111l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᧃ")
            except Exception as bstack11l111l1ll1_opy_:
                logger.error(bstack1111l_opy_ (u"ࠤࡍࡗࡔࡔࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡐࡢࡴࡤࡱࡸࡀࠠࡼࡿࠥᧄ").format(bstack11l111l1ll1_opy_))
        bstack11l111ll1l1_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1l1ll1l1ll1_opy_ import bstack1l1ll11lll1_opy_
        if test_framework_state in bstack1l1ll11lll1_opy_.bstack11l1ll1l111_opy_:
            if bstack11l111ll1ll_opy_ == bstack11l1l11l111_opy_:
                bstack11l111ll1l1_opy_ = True
            bstack11l111ll1ll_opy_ = bstack11l1l111lll_opy_
        try:
            platform_index = os.environ[bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᧅ")]
            target_dir = os.path.join(bstack1l111l1ll11_opy_, bstack1l1111l1l1l_opy_ + str(platform_index),
                                      bstack11l111ll1ll_opy_)
            if bstack11l111ll1l1_opy_:
                target_dir = os.path.join(target_dir, bstack11l111l1l1l_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1111l_opy_ (u"ࠦࡈࡸࡥࡢࡶࡨࡨ࠴ࡼࡥࡳ࡫ࡩ࡭ࡪࡪࠠࡵࡣࡵ࡫ࡪࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᧆ").format(target_dir))
            file_name = os.path.basename(bstack11l111l11l1_opy_)
            bstack11l111l111l_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11l111l111l_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11l111ll11l_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11l111ll11l_opy_) + extension)):
                    bstack11l111ll11l_opy_ += 1
                bstack11l111l111l_opy_ = os.path.join(target_dir, base_name + str(bstack11l111ll11l_opy_) + extension)
            shutil.copy(bstack11l111l11l1_opy_, bstack11l111l111l_opy_)
            logger.info(bstack1111l_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡦࡳࡵ࡯ࡥࡥࠢࡷࡳ࠿ࠦࡻࡾࠤᧇ").format(bstack11l111l111l_opy_))
        except Exception as e:
            logger.error(bstack1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡳ࡯ࡷ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࡸࡴࠦࡴࡢࡴࡪࡩࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠼ࠣࡿࢂࠨᧈ").format(e))
            return
        finally:
            if bstack11l111lll11_opy_.startswith(bstack1111l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᧉ")) or bstack11l111lll11_opy_.startswith(bstack1111l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ᧊")):
                try:
                    if bstack11l111l11l1_opy_ is not None and bstack11l111l11l1_opy_.exists():
                        bstack11l111l11l1_opy_.unlink()
                        logger.debug(bstack1111l_opy_ (u"ࠤࡗࡩࡲࡶ࡯ࡳࡣࡵࡽࠥ࡬ࡩ࡭ࡧࠣࡨࡪࡲࡥࡵࡧࡧ࠾ࠥࢁࡽࠣ᧋").format(bstack11l111l11l1_opy_))
                except Exception as ex:
                    logger.error(bstack1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠤ᧌").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack11l111l1l11_opy_, stage=STAGE.bstack11lll111l_opy_, bstack11lll111_opy_=None)
    def bstack1ll1l1l111_opy_() -> None:
        bstack1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡆࡨࡰࡪࡺࡥࡴࠢࡤࡰࡱࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࡸࡪࡲࡷࡪࠦ࡮ࡢ࡯ࡨࡷࠥࡹࡴࡢࡴࡷࠤࡼ࡯ࡴࡩ࡙ࠢࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥࠤ࡫ࡵ࡬࡭ࡱࡺࡩࡩࠦࡢࡺࠢࡤࠤࡳࡻ࡭ࡣࡧࡵࠤ࡮ࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࡶ࡫ࡩࠥࡻࡳࡦࡴࠪࡷࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ᧍")
        bstack11l111l11ll_opy_ = bstack1l111llll1l_opy_()
        pattern = re.compile(bstack1111l_opy_ (u"ࡷࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࡢࡤࠬࠤ᧎"))
        if os.path.exists(bstack11l111l11ll_opy_):
            for item in os.listdir(bstack11l111l11ll_opy_):
                bstack11l111l1lll_opy_ = os.path.join(bstack11l111l11ll_opy_, item)
                if os.path.isdir(bstack11l111l1lll_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11l111l1lll_opy_)
                    except Exception as e:
                        logger.error(bstack1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢ᧏").format(e))
        else:
            logger.info(bstack1111l_opy_ (u"ࠢࡕࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧ᧐").format(bstack11l111l11ll_opy_))