# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
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
from bstack_utils.helper import bstack1l11lll1lll_opy_
bstack11l1ll1llll_opy_ = 100 * 1024 * 1024 # 100 bstack11l1ll1lll1_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l1l11l1ll1_opy_ = bstack1l11lll1lll_opy_()
bstack1l11l1ll11l_opy_ = bstack11lllll_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᜢ")
bstack11ll11ll111_opy_ = bstack11lllll_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᜣ")
bstack11ll11ll11l_opy_ = bstack11lllll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᜤ")
bstack11ll11l1lll_opy_ = bstack11lllll_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᜥ")
bstack11l1lll1111_opy_ = bstack11lllll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᜦ")
_11l1lll111l_opy_ = threading.local()
def bstack11ll11lll1l_opy_(test_framework_state, test_hook_state):
    bstack11lllll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡥࡵࠢࡷ࡬ࡪࠦࡣࡶࡴࡵࡩࡳࡺࠠࡵࡧࡶࡸࠥ࡫ࡶࡦࡰࡷࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡴࡩࡴࡨࡥࡩ࠳࡬ࡰࡥࡤࡰࠥࡹࡴࡰࡴࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡸ࡮࡯ࡶ࡮ࡧࠤࡧ࡫ࠠࡤࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡸ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡨࡢࡰࡧࡰࡪࡸࠠࠩࡵࡸࡧ࡭ࠦࡡࡴࠢࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺࠩࠋࠢࠣࠤࠥࡨࡥࡧࡱࡵࡩࠥࡧ࡮ࡺࠢࡩ࡭ࡱ࡫ࠠࡶࡲ࡯ࡳࡦࡪࡳࠡࡱࡦࡧࡺࡸ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᜧ")
    _11l1lll111l_opy_.test_framework_state = test_framework_state
    _11l1lll111l_opy_.test_hook_state = test_hook_state
def bstack11l1lll11ll_opy_():
    bstack11lllll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡒࡦࡶࡵ࡭ࡪࡼࡥࠡࡶ࡫ࡩࠥࡩࡵࡳࡴࡨࡲࡹࠦࡴࡦࡵࡷࠤࡪࡼࡥ࡯ࡶࠣࡷࡹࡧࡴࡦࠢࡩࡶࡴࡳࠠࡵࡪࡵࡩࡦࡪ࠭࡭ࡱࡦࡥࡱࠦࡳࡵࡱࡵࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡡࠡࡶࡸࡴࡱ࡫ࠠࠩࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠭ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨ࠭ࠥࡵࡲࠡࠪࡑࡳࡳ࡫ࠬࠡࡐࡲࡲࡪ࠯ࠠࡪࡨࠣࡲࡴࡺࠠࡴࡧࡷ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᜨ")
    return (
        getattr(_11l1lll111l_opy_, bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࠧᜩ"), None),
        getattr(_11l1lll111l_opy_, bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࠪᜪ"), None)
    )
class bstack11l1111l11_opy_:
    bstack11lllll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡉ࡭ࡱ࡫ࡕࡱ࡮ࡲࡥࡩ࡫ࡲࠡࡲࡵࡳࡻ࡯ࡤࡦࡵࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࡦࡲࡩࡵࡻࠣࡸࡴࠦࡵࡱ࡮ࡲࡥࡩࠦࡡ࡯ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡢࡢࡵࡨࡨࠥࡵ࡮ࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࡏࡴࠡࡵࡸࡴࡵࡵࡲࡵࡵࠣࡦࡴࡺࡨࠡ࡮ࡲࡧࡦࡲࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࡶࠤࡦࡴࡤࠡࡊࡗࡘࡕ࠵ࡈࡕࡖࡓࡗ࡛ࠥࡒࡍࡵ࠯ࠤࡦࡴࡤࠡࡥࡲࡴ࡮࡫ࡳࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࡺ࡯ࠡࡣࠣࡨࡪࡹࡩࡨࡰࡤࡸࡪࡪࠊࠡࠢࠣࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡸ࡫ࡷ࡬࡮ࡴࠠࡵࡪࡨࠤࡺࡹࡥࡳࠩࡶࠤ࡭ࡵ࡭ࡦࠢࡩࡳࡱࡪࡥࡳࠢࡸࡲࡩ࡫ࡲࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࡊࡨࠣࡥࡳࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡶࡡࡳࡣࡰࡩࡹ࡫ࡲࠡࠪ࡬ࡲࠥࡐࡓࡐࡐࠣࡪࡴࡸ࡭ࡢࡶࠬࠤ࡮ࡹࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡤࡲࡩࠦࡣࡰࡰࡷࡥ࡮ࡴࡳࠡࡣࠣࡸࡷࡻࡴࡩࡻࠣࡺࡦࡲࡵࡦࠌࠣࠤࠥࠦࡦࡰࡴࠣࡸ࡭࡫ࠠ࡬ࡧࡼࠤࠧࡨࡵࡪ࡮ࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢ࠭ࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡶ࡬ࡢࡥࡨࡨࠥ࡯࡮ࠡࡶ࡫ࡩࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤ࡫ࡵ࡬ࡥࡧࡵ࠿ࠥࡵࡴࡩࡧࡵࡻ࡮ࡹࡥ࠭ࠌࠣࠤࠥࠦࡩࡵࠢࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦ࠳ࠐࠠࠡࠢࠣࡘ࡭࡯ࡳࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡲࡪࠥࡧࡤࡥࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡩࡴࠢࡤࠤࡻࡵࡩࡥࠢࡰࡩࡹ࡮࡯ࡥ⠖࡬ࡸࠥ࡮ࡡ࡯ࡦ࡯ࡩࡸࠦࡡ࡭࡮ࠣࡩࡷࡸ࡯ࡳࡵࠣ࡫ࡷࡧࡣࡦࡨࡸࡰࡱࡿࠠࡣࡻࠣࡰࡴ࡭ࡧࡪࡰࡪࠎࠥࠦࠠࠡࡶ࡫ࡩࡲࠦࡡ࡯ࡦࠣࡷ࡮ࡳࡰ࡭ࡻࠣࡶࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡵࡪࡵࡳࡼ࡯࡮ࡨࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡸ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᜫ")
    @staticmethod
    def upload_attachment(bstack11l1ll1l11l_opy_: str, *bstack11l1lll1l1l_opy_) -> None:
        if not bstack11l1ll1l11l_opy_ or not bstack11l1ll1l11l_opy_.strip():
            logger.error(bstack11lllll_opy_ (u"ࠥࡥࡩࡪ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡖࡲࡰࡸ࡬ࡨࡪࡪࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࠣ࡭ࡸࠦࡥ࡮ࡲࡷࡽࠥࡵࡲࠡࡐࡲࡲࡪ࠴ࠢᜬ"))
            return
        bstack11l1llll111_opy_ = bstack11l1lll1l1l_opy_[0] if bstack11l1lll1l1l_opy_ and len(bstack11l1lll1l1l_opy_) > 0 else None
        bstack11l1ll1l1ll_opy_ = None
        test_framework_state, test_hook_state = bstack11l1lll11ll_opy_()
        try:
            if bstack11l1ll1l11l_opy_.startswith(bstack11lllll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᜭ")) or bstack11l1ll1l11l_opy_.startswith(bstack11lllll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᜮ")):
                logger.debug(bstack11lllll_opy_ (u"ࠨࡐࡢࡶ࡫ࠤ࡮ࡹࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡧࠤࡦࡹࠠࡖࡔࡏ࠿ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠨᜯ"))
                url = bstack11l1ll1l11l_opy_
                bstack11l1ll1l111_opy_ = str(uuid.uuid4())
                bstack11l1ll1l1l1_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11l1ll1l1l1_opy_ or not bstack11l1ll1l1l1_opy_.strip():
                    bstack11l1ll1l1l1_opy_ = bstack11l1ll1l111_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack11lllll_opy_ (u"ࠢࡶࡲ࡯ࡳࡦࡪ࡟ࠣᜰ") + bstack11l1ll1l111_opy_ + bstack11lllll_opy_ (u"ࠣࡡࠥᜱ"),
                                                        suffix=bstack11lllll_opy_ (u"ࠤࡢࠦᜲ") + bstack11l1ll1l1l1_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack11lllll_opy_ (u"ࠪࡻࡧ࠭ᜳ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11l1ll1l1ll_opy_ = Path(temp_file.name)
                logger.debug(bstack11lllll_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡨ࡬ࡰࡪࠦࡴࡰࠢࡷࡩࡲࡶ࡯ࡳࡣࡵࡽࠥࡲ࡯ࡤࡣࡷ࡭ࡴࡴ࠺ࠡࡽࢀ᜴ࠦ").format(bstack11l1ll1l1ll_opy_))
            else:
                bstack11l1ll1l1ll_opy_ = Path(bstack11l1ll1l11l_opy_)
                logger.debug(bstack11lllll_opy_ (u"ࠧࡖࡡࡵࡪࠣ࡭ࡸࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡦࠣࡥࡸࠦ࡬ࡰࡥࡤࡰࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠢ᜵").format(bstack11l1ll1l1ll_opy_))
        except Exception as e:
            logger.error(bstack11lllll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡲࡦࡹࡧࡩ࡯ࠢࡩ࡭ࡱ࡫ࠠࡧࡴࡲࡱࠥࡶࡡࡵࡪ࠲࡙ࡗࡒ࠺ࠡࡽࢀࠦ᜶").format(e))
            return
        if bstack11l1ll1l1ll_opy_ is None or not bstack11l1ll1l1ll_opy_.exists():
            logger.error(bstack11lllll_opy_ (u"ࠢࡔࡱࡸࡶࡨ࡫ࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠥ᜷").format(bstack11l1ll1l1ll_opy_))
            return
        if bstack11l1ll1l1ll_opy_.stat().st_size > bstack11l1ll1llll_opy_:
            logger.error(bstack11lllll_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡳࡪࡼࡨࠤࡪࡾࡣࡦࡧࡧࡷࠥࡳࡡࡹ࡫ࡰࡹࡲࠦࡡ࡭࡮ࡲࡻࡪࡪࠠࡴ࡫ࡽࡩࠥࡵࡦࠡࡽࢀࠦ᜸").format(bstack11l1ll1llll_opy_))
            return
        bstack11l1lll1l11_opy_ = bstack11lllll_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧ᜹")
        if bstack11l1llll111_opy_:
            try:
                params = json.loads(bstack11l1llll111_opy_)
                if bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧ᜺") in params and params.get(bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨ᜻")) is True:
                    bstack11l1lll1l11_opy_ = bstack11lllll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤ᜼")
            except Exception as bstack11l1lll1lll_opy_:
                logger.error(bstack11lllll_opy_ (u"ࠨࡊࡔࡑࡑࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡔࡦࡸࡡ࡮ࡵ࠽ࠤࢀࢃࠢ᜽").format(bstack11l1lll1lll_opy_))
        bstack11l1llll11l_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1ll1ll1111l_opy_ import bstack1ll1ll111l1_opy_
        if test_framework_state in bstack1ll1ll111l1_opy_.bstack11ll11ll1ll_opy_:
            if bstack11l1lll1l11_opy_ == bstack11ll11ll11l_opy_:
                bstack11l1llll11l_opy_ = True
            bstack11l1lll1l11_opy_ = bstack11ll11l1lll_opy_
        try:
            platform_index = os.environ[bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ᜾")]
            target_dir = os.path.join(bstack1l1l11l1ll1_opy_, bstack1l11l1ll11l_opy_ + str(platform_index),
                                      bstack11l1lll1l11_opy_)
            if bstack11l1llll11l_opy_:
                target_dir = os.path.join(target_dir, bstack11l1lll1111_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack11lllll_opy_ (u"ࠣࡅࡵࡩࡦࡺࡥࡥ࠱ࡹࡩࡷ࡯ࡦࡪࡧࡧࠤࡹࡧࡲࡨࡧࡷࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦ᜿").format(target_dir))
            file_name = os.path.basename(bstack11l1ll1l1ll_opy_)
            bstack11l1llll1l1_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11l1llll1l1_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11l1ll1ll1l_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11l1ll1ll1l_opy_) + extension)):
                    bstack11l1ll1ll1l_opy_ += 1
                bstack11l1llll1l1_opy_ = os.path.join(target_dir, base_name + str(bstack11l1ll1ll1l_opy_) + extension)
            shutil.copy(bstack11l1ll1l1ll_opy_, bstack11l1llll1l1_opy_)
            logger.info(bstack11lllll_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡣࡰࡲ࡬ࡩࡩࠦࡴࡰ࠼ࠣࡿࢂࠨᝀ").format(bstack11l1llll1l1_opy_))
        except Exception as e:
            logger.error(bstack11lllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡰࡳࡻ࡯࡮ࡨࠢࡩ࡭ࡱ࡫ࠠࡵࡱࠣࡸࡦࡸࡧࡦࡶࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᝁ").format(e))
            return
        finally:
            if bstack11l1ll1l11l_opy_.startswith(bstack11lllll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᝂ")) or bstack11l1ll1l11l_opy_.startswith(bstack11lllll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᝃ")):
                try:
                    if bstack11l1ll1l1ll_opy_ is not None and bstack11l1ll1l1ll_opy_.exists():
                        bstack11l1ll1l1ll_opy_.unlink()
                        logger.debug(bstack11lllll_opy_ (u"ࠨࡔࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡩ࡭ࡱ࡫ࠠࡥࡧ࡯ࡩࡹ࡫ࡤ࠻ࠢࡾࢁࠧᝄ").format(bstack11l1ll1l1ll_opy_))
                except Exception as ex:
                    logger.error(bstack11lllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂࠨᝅ").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack11l1lll1ll1_opy_, stage=STAGE.bstack1llll11111_opy_, bstack11lll11111_opy_=None)
    def bstack11lll111l1_opy_() -> None:
        bstack11lllll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡊࡥ࡭ࡧࡷࡩࡸࠦࡡ࡭࡮ࠣࡪࡴࡲࡤࡦࡴࡶࠤࡼ࡮࡯ࡴࡧࠣࡲࡦࡳࡥࡴࠢࡶࡸࡦࡸࡴࠡࡹ࡬ࡸ࡭ࠦࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢࠡࡨࡲࡰࡱࡵࡷࡦࡦࠣࡦࡾࠦࡡࠡࡰࡸࡱࡧ࡫ࡲࠡ࡫ࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡦࠢࡸࡷࡪࡸࠧࡴࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᝆ")
        bstack11l1ll1ll11_opy_ = bstack1l11lll1lll_opy_()
        pattern = re.compile(bstack11lllll_opy_ (u"ࡴ࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯࡟ࡨ࠰ࠨᝇ"))
        if os.path.exists(bstack11l1ll1ll11_opy_):
            for item in os.listdir(bstack11l1ll1ll11_opy_):
                bstack11l1lll11l1_opy_ = os.path.join(bstack11l1ll1ll11_opy_, item)
                if os.path.isdir(bstack11l1lll11l1_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11l1lll11l1_opy_)
                    except Exception as e:
                        logger.error(bstack11lllll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᝈ").format(e))
        else:
            logger.info(bstack11lllll_opy_ (u"࡙ࠦ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠤᝉ").format(bstack11l1ll1ll11_opy_))