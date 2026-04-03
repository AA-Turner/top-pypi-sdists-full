# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
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
from bstack_utils.helper import bstack11ll11ll11l_opy_
bstack111l111111l_opy_ = 100 * 1024 * 1024 # 100 bstack111l111ll11_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack11ll11l1ll1_opy_ = bstack11ll11ll11l_opy_()
bstack11lll11111l_opy_ = bstack1ll1l11_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᯤ")
bstack111ll11ll11_opy_ = bstack1ll1l11_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᯥ")
bstack111ll11lll1_opy_ = bstack1ll1l11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨ᯦")
bstack111ll11l1ll_opy_ = bstack1ll1l11_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨᯧ")
bstack111l11111ll_opy_ = bstack1ll1l11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥᯨ")
_111l1111ll1_opy_ = threading.local()
def bstack111lllll111_opy_(test_framework_state, test_hook_state):
    bstack1ll1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡥࡵࠢࡷ࡬ࡪࠦࡣࡶࡴࡵࡩࡳࡺࠠࡵࡧࡶࡸࠥ࡫ࡶࡦࡰࡷࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡴࡩࡴࡨࡥࡩ࠳࡬ࡰࡥࡤࡰࠥࡹࡴࡰࡴࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡸ࡮࡯ࡶ࡮ࡧࠤࡧ࡫ࠠࡤࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡸ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡨࡢࡰࡧࡰࡪࡸࠠࠩࡵࡸࡧ࡭ࠦࡡࡴࠢࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺࠩࠋࠢࠣࠤࠥࡨࡥࡧࡱࡵࡩࠥࡧ࡮ࡺࠢࡩ࡭ࡱ࡫ࠠࡶࡲ࡯ࡳࡦࡪࡳࠡࡱࡦࡧࡺࡸ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᯩ")
    _111l1111ll1_opy_.test_framework_state = test_framework_state
    _111l1111ll1_opy_.test_hook_state = test_hook_state
def bstack111l111l11l_opy_():
    bstack1ll1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡒࡦࡶࡵ࡭ࡪࡼࡥࠡࡶ࡫ࡩࠥࡩࡵࡳࡴࡨࡲࡹࠦࡴࡦࡵࡷࠤࡪࡼࡥ࡯ࡶࠣࡷࡹࡧࡴࡦࠢࡩࡶࡴࡳࠠࡵࡪࡵࡩࡦࡪ࠭࡭ࡱࡦࡥࡱࠦࡳࡵࡱࡵࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡡࠡࡶࡸࡴࡱ࡫ࠠࠩࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠭ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨ࠭ࠥࡵࡲࠡࠪࡑࡳࡳ࡫ࠬࠡࡐࡲࡲࡪ࠯ࠠࡪࡨࠣࡲࡴࡺࠠࡴࡧࡷ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᯪ")
    return (
        getattr(_111l1111ll1_opy_, bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࠧᯫ"), None),
        getattr(_111l1111ll1_opy_, bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࠪᯬ"), None)
    )
class bstack1ll1ll11ll_opy_:
    bstack1ll1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡉ࡭ࡱ࡫ࡕࡱ࡮ࡲࡥࡩ࡫ࡲࠡࡲࡵࡳࡻ࡯ࡤࡦࡵࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࡦࡲࡩࡵࡻࠣࡸࡴࠦࡵࡱ࡮ࡲࡥࡩࠦࡡ࡯ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡢࡢࡵࡨࡨࠥࡵ࡮ࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࡏࡴࠡࡵࡸࡴࡵࡵࡲࡵࡵࠣࡦࡴࡺࡨࠡ࡮ࡲࡧࡦࡲࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࡶࠤࡦࡴࡤࠡࡊࡗࡘࡕ࠵ࡈࡕࡖࡓࡗ࡛ࠥࡒࡍࡵ࠯ࠤࡦࡴࡤࠡࡥࡲࡴ࡮࡫ࡳࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࡺ࡯ࠡࡣࠣࡨࡪࡹࡩࡨࡰࡤࡸࡪࡪࠊࠡࠢࠣࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡸ࡫ࡷ࡬࡮ࡴࠠࡵࡪࡨࠤࡺࡹࡥࡳࠩࡶࠤ࡭ࡵ࡭ࡦࠢࡩࡳࡱࡪࡥࡳࠢࡸࡲࡩ࡫ࡲࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࡊࡨࠣࡥࡳࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡶࡡࡳࡣࡰࡩࡹ࡫ࡲࠡࠪ࡬ࡲࠥࡐࡓࡐࡐࠣࡪࡴࡸ࡭ࡢࡶࠬࠤ࡮ࡹࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡤࡲࡩࠦࡣࡰࡰࡷࡥ࡮ࡴࡳࠡࡣࠣࡸࡷࡻࡴࡩࡻࠣࡺࡦࡲࡵࡦࠌࠣࠤࠥࠦࡦࡰࡴࠣࡸ࡭࡫ࠠ࡬ࡧࡼࠤࠧࡨࡵࡪ࡮ࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢ࠭ࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡶ࡬ࡢࡥࡨࡨࠥ࡯࡮ࠡࡶ࡫ࡩࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤ࡫ࡵ࡬ࡥࡧࡵ࠿ࠥࡵࡴࡩࡧࡵࡻ࡮ࡹࡥ࠭ࠌࠣࠤࠥࠦࡩࡵࠢࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦ࠳ࠐࠠࠡࠢࠣࡘ࡭࡯ࡳࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡲࡪࠥࡧࡤࡥࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡩࡴࠢࡤࠤࡻࡵࡩࡥࠢࡰࡩࡹ࡮࡯ࡥ⠖࡬ࡸࠥ࡮ࡡ࡯ࡦ࡯ࡩࡸࠦࡡ࡭࡮ࠣࡩࡷࡸ࡯ࡳࡵࠣ࡫ࡷࡧࡣࡦࡨࡸࡰࡱࡿࠠࡣࡻࠣࡰࡴ࡭ࡧࡪࡰࡪࠎࠥࠦࠠࠡࡶ࡫ࡩࡲࠦࡡ࡯ࡦࠣࡷ࡮ࡳࡰ࡭ࡻࠣࡶࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡵࡪࡵࡳࡼ࡯࡮ࡨࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡸ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᯭ")
    @staticmethod
    def upload_attachment(bstack111l1111lll_opy_: str, *bstack111l11111l1_opy_) -> None:
        if not bstack111l1111lll_opy_ or not bstack111l1111lll_opy_.strip():
            logger.error(bstack1ll1l11_opy_ (u"ࠥࡥࡩࡪ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡖࡲࡰࡸ࡬ࡨࡪࡪࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࠣ࡭ࡸࠦࡥ࡮ࡲࡷࡽࠥࡵࡲࠡࡐࡲࡲࡪ࠴ࠢᯮ"))
            return
        bstack111l111ll1l_opy_ = bstack111l11111l1_opy_[0] if bstack111l11111l1_opy_ and len(bstack111l11111l1_opy_) > 0 else None
        bstack1ll1llll11l_opy_ = None
        test_framework_state, test_hook_state = bstack111l111l11l_opy_()
        try:
            if bstack111l1111lll_opy_.startswith(bstack1ll1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᯯ")) or bstack111l1111lll_opy_.startswith(bstack1ll1l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᯰ")):
                logger.debug(bstack1ll1l11_opy_ (u"ࠨࡐࡢࡶ࡫ࠤ࡮ࡹࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡧࠤࡦࡹࠠࡖࡔࡏ࠿ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠨᯱ"))
                url = bstack111l1111lll_opy_
                bstack111l11l111l_opy_ = str(uuid.uuid4())
                bstack111l11l1111_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack111l11l1111_opy_ or not bstack111l11l1111_opy_.strip():
                    bstack111l11l1111_opy_ = bstack111l11l111l_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1ll1l11_opy_ (u"ࠢࡶࡲ࡯ࡳࡦࡪ࡟᯲ࠣ") + bstack111l11l111l_opy_ + bstack1ll1l11_opy_ (u"ࠣࡡ᯳ࠥ"),
                                                        suffix=bstack1ll1l11_opy_ (u"ࠤࡢࠦ᯴") + bstack111l11l1111_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1ll1l11_opy_ (u"ࠪࡻࡧ࠭᯵")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack1ll1llll11l_opy_ = Path(temp_file.name)
                logger.debug(bstack1ll1l11_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡨ࡬ࡰࡪࠦࡴࡰࠢࡷࡩࡲࡶ࡯ࡳࡣࡵࡽࠥࡲ࡯ࡤࡣࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦ᯶").format(bstack1ll1llll11l_opy_))
            else:
                bstack1ll1llll11l_opy_ = Path(bstack111l1111lll_opy_)
                logger.debug(bstack1ll1l11_opy_ (u"ࠧࡖࡡࡵࡪࠣ࡭ࡸࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡦࠣࡥࡸࠦ࡬ࡰࡥࡤࡰࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠢ᯷").format(bstack1ll1llll11l_opy_))
        except Exception as e:
            logger.error(bstack1ll1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡲࡦࡹࡧࡩ࡯ࠢࡩ࡭ࡱ࡫ࠠࡧࡴࡲࡱࠥࡶࡡࡵࡪ࠲࡙ࡗࡒ࠺ࠡࡽࢀࠦ᯸").format(e))
            return
        if bstack1ll1llll11l_opy_ is None or not bstack1ll1llll11l_opy_.exists():
            logger.error(bstack1ll1l11_opy_ (u"ࠢࡔࡱࡸࡶࡨ࡫ࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠥ᯹").format(bstack1ll1llll11l_opy_))
            return
        if bstack1ll1llll11l_opy_.stat().st_size > bstack111l111111l_opy_:
            logger.error(bstack1ll1l11_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡳࡪࡼࡨࠤࡪࡾࡣࡦࡧࡧࡷࠥࡳࡡࡹ࡫ࡰࡹࡲࠦࡡ࡭࡮ࡲࡻࡪࡪࠠࡴ࡫ࡽࡩࠥࡵࡦࠡࡽࢀࠦ᯺").format(bstack111l111111l_opy_))
            return
        bstack111l111lll1_opy_ = bstack1ll1l11_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧ᯻")
        if bstack111l111ll1l_opy_:
            try:
                params = json.loads(bstack111l111ll1l_opy_)
                if bstack1ll1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧ᯼") in params and params.get(bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨ᯽")) is True:
                    bstack111l111lll1_opy_ = bstack1ll1l11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤ᯾")
            except Exception as bstack111l111l111_opy_:
                logger.error(bstack1ll1l11_opy_ (u"ࠨࡊࡔࡑࡑࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡔࡦࡸࡡ࡮ࡵ࠽ࠤࢀࢃࠢ᯿").format(bstack111l111l111_opy_))
        bstack111l111l1ll_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1l11l11111l_opy_ import bstack1l11ll1llll_opy_
        if test_framework_state in bstack1l11ll1llll_opy_.bstack111lll1111l_opy_:
            if bstack111l111lll1_opy_ == bstack111ll11lll1_opy_:
                bstack111l111l1ll_opy_ = True
            bstack111l111lll1_opy_ = bstack111ll11l1ll_opy_
        try:
            platform_index = os.environ[bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᰀ")]
            target_dir = os.path.join(bstack11ll11l1ll1_opy_, bstack11lll11111l_opy_ + str(platform_index),
                                      bstack111l111lll1_opy_)
            if bstack111l111l1ll_opy_:
                target_dir = os.path.join(target_dir, bstack111l11111ll_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1ll1l11_opy_ (u"ࠣࡅࡵࡩࡦࡺࡥࡥ࠱ࡹࡩࡷ࡯ࡦࡪࡧࡧࠤࡹࡧࡲࡨࡧࡷࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᰁ").format(target_dir))
            file_name = os.path.basename(bstack1ll1llll11l_opy_)
            bstack111l1111l11_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack111l1111l11_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack111l1111111_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack111l1111111_opy_) + extension)):
                    bstack111l1111111_opy_ += 1
                bstack111l1111l11_opy_ = os.path.join(target_dir, base_name + str(bstack111l1111111_opy_) + extension)
            shutil.copy(bstack1ll1llll11l_opy_, bstack111l1111l11_opy_)
            logger.info(bstack1ll1l11_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡣࡰࡲ࡬ࡩࡩࠦࡴࡰ࠼ࠣࡿࢂࠨᰂ").format(bstack111l1111l11_opy_))
        except Exception as e:
            logger.error(bstack1ll1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡰࡳࡻ࡯࡮ࡨࠢࡩ࡭ࡱ࡫ࠠࡵࡱࠣࡸࡦࡸࡧࡦࡶࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᰃ").format(e))
            return
        finally:
            if bstack111l1111lll_opy_.startswith(bstack1ll1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᰄ")) or bstack111l1111lll_opy_.startswith(bstack1ll1l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᰅ")):
                try:
                    if bstack1ll1llll11l_opy_ is not None and bstack1ll1llll11l_opy_.exists():
                        bstack1ll1llll11l_opy_.unlink()
                        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡔࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡩ࡭ࡱ࡫ࠠࡥࡧ࡯ࡩࡹ࡫ࡤ࠻ࠢࡾࢁࠧᰆ").format(bstack1ll1llll11l_opy_))
                except Exception as ex:
                    logger.error(bstack1ll1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂࠨᰇ").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack111l1111l1l_opy_, stage=STAGE.bstack1ll11l11_opy_, bstack1lll1l1ll1_opy_=None)
    def bstack1111ll11l1_opy_() -> None:
        bstack1ll1l11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡊࡥ࡭ࡧࡷࡩࡸࠦࡡ࡭࡮ࠣࡪࡴࡲࡤࡦࡴࡶࠤࡼ࡮࡯ࡴࡧࠣࡲࡦࡳࡥࡴࠢࡶࡸࡦࡸࡴࠡࡹ࡬ࡸ࡭ࠦࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢࠡࡨࡲࡰࡱࡵࡷࡦࡦࠣࡦࡾࠦࡡࠡࡰࡸࡱࡧ࡫ࡲࠡ࡫ࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡦࠢࡸࡷࡪࡸࠧࡴࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᰈ")
        bstack111l111l1l1_opy_ = bstack11ll11ll11l_opy_()
        pattern = re.compile(bstack1ll1l11_opy_ (u"ࡴ࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯࡟ࡨ࠰ࠨᰉ"))
        if os.path.exists(bstack111l111l1l1_opy_):
            for item in os.listdir(bstack111l111l1l1_opy_):
                bstack111l111llll_opy_ = os.path.join(bstack111l111l1l1_opy_, item)
                if os.path.isdir(bstack111l111llll_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack111l111llll_opy_)
                    except Exception as e:
                        logger.error(bstack1ll1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᰊ").format(e))
        else:
            logger.info(bstack1ll1l11_opy_ (u"࡙ࠦ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠤᰋ").format(bstack111l111l1l1_opy_))