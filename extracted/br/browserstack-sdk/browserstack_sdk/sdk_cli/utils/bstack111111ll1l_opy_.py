# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
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
from bstack_utils.helper import get_writable_dir
bstack1111ll1l111_opy_ = 100 * 1024 * 1024 # 100 bstack1111ll11111_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
BROWSERSTACK_ROOT_DIR = get_writable_dir()
UPLOADED_ATTACHMENTS_PREFIX = bstack1l1llll_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢẼ")
bstack111l1l1l111_opy_ = bstack1l1llll_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦẽ")
bstack111l1l11ll1_opy_ = bstack1l1llll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨẾ")
bstack111l1l111l1_opy_ = bstack1l1llll_opy_ (u"ࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨế")
bstack1111ll11ll1_opy_ = bstack1l1llll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥỀ")
_1111l1ll111_opy_ = threading.local()
def bstack111ll11l1l1_opy_(test_framework_state, test_hook_state):
    bstack1l1llll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡥࡵࠢࡷ࡬ࡪࠦࡣࡶࡴࡵࡩࡳࡺࠠࡵࡧࡶࡸࠥ࡫ࡶࡦࡰࡷࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡴࡩࡴࡨࡥࡩ࠳࡬ࡰࡥࡤࡰࠥࡹࡴࡰࡴࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡸ࡮࡯ࡶ࡮ࡧࠤࡧ࡫ࠠࡤࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡸ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡨࡢࡰࡧࡰࡪࡸࠠࠩࡵࡸࡧ࡭ࠦࡡࡴࠢࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺࠩࠋࠢࠣࠤࠥࡨࡥࡧࡱࡵࡩࠥࡧ࡮ࡺࠢࡩ࡭ࡱ࡫ࠠࡶࡲ࡯ࡳࡦࡪࡳࠡࡱࡦࡧࡺࡸ࠮ࠋࠢࠣࠤࠥࠨࠢࠣề")
    _1111l1ll111_opy_.test_framework_state = test_framework_state
    _1111l1ll111_opy_.test_hook_state = test_hook_state
def bstack1111l1llll1_opy_():
    bstack1l1llll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡒࡦࡶࡵ࡭ࡪࡼࡥࠡࡶ࡫ࡩࠥࡩࡵࡳࡴࡨࡲࡹࠦࡴࡦࡵࡷࠤࡪࡼࡥ࡯ࡶࠣࡷࡹࡧࡴࡦࠢࡩࡶࡴࡳࠠࡵࡪࡵࡩࡦࡪ࠭࡭ࡱࡦࡥࡱࠦࡳࡵࡱࡵࡥ࡬࡫࠮ࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡡࠡࡶࡸࡴࡱ࡫ࠠࠩࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠭ࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨ࠭ࠥࡵࡲࠡࠪࡑࡳࡳ࡫ࠬࠡࡐࡲࡲࡪ࠯ࠠࡪࡨࠣࡲࡴࡺࠠࡴࡧࡷ࠲ࠏࠦࠠࠡࠢࠥࠦࠧỂ")
    return (
        getattr(_1111l1ll111_opy_, bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࠧể"), None),
        getattr(_1111l1ll111_opy_, bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࠪỄ"), None)
    )
class FileUploader:
    bstack1l1llll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡉ࡭ࡱ࡫ࡕࡱ࡮ࡲࡥࡩ࡫ࡲࠡࡲࡵࡳࡻ࡯ࡤࡦࡵࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࡦࡲࡩࡵࡻࠣࡸࡴࠦࡵࡱ࡮ࡲࡥࡩࠦࡡ࡯ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡢࡢࡵࡨࡨࠥࡵ࡮ࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࡏࡴࠡࡵࡸࡴࡵࡵࡲࡵࡵࠣࡦࡴࡺࡨࠡ࡮ࡲࡧࡦࡲࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࡶࠤࡦࡴࡤࠡࡊࡗࡘࡕ࠵ࡈࡕࡖࡓࡗ࡛ࠥࡒࡍࡵ࠯ࠤࡦࡴࡤࠡࡥࡲࡴ࡮࡫ࡳࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࡺ࡯ࠡࡣࠣࡨࡪࡹࡩࡨࡰࡤࡸࡪࡪࠊࠡࠢࠣࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡸ࡫ࡷ࡬࡮ࡴࠠࡵࡪࡨࠤࡺࡹࡥࡳࠩࡶࠤ࡭ࡵ࡭ࡦࠢࡩࡳࡱࡪࡥࡳࠢࡸࡲࡩ࡫ࡲࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࡊࡨࠣࡥࡳࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡶࡡࡳࡣࡰࡩࡹ࡫ࡲࠡࠪ࡬ࡲࠥࡐࡓࡐࡐࠣࡪࡴࡸ࡭ࡢࡶࠬࠤ࡮ࡹࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡤࡲࡩࠦࡣࡰࡰࡷࡥ࡮ࡴࡳࠡࡣࠣࡸࡷࡻࡴࡩࡻࠣࡺࡦࡲࡵࡦࠌࠣࠤࠥࠦࡦࡰࡴࠣࡸ࡭࡫ࠠ࡬ࡧࡼࠤࠧࡨࡵࡪ࡮ࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢ࠭ࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡶ࡬ࡢࡥࡨࡨࠥ࡯࡮ࠡࡶ࡫ࡩࠥࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥࠤ࡫ࡵ࡬ࡥࡧࡵ࠿ࠥࡵࡴࡩࡧࡵࡻ࡮ࡹࡥ࠭ࠌࠣࠤࠥࠦࡩࡵࠢࡧࡩ࡫ࡧࡵ࡭ࡶࡶࠤࡹࡵࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦ࠳ࠐࠠࠡࠢࠣࡘ࡭࡯ࡳࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡲࡪࠥࡧࡤࡥࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡩࡴࠢࡤࠤࡻࡵࡩࡥࠢࡰࡩࡹ࡮࡯ࡥ⠖࡬ࡸࠥ࡮ࡡ࡯ࡦ࡯ࡩࡸࠦࡡ࡭࡮ࠣࡩࡷࡸ࡯ࡳࡵࠣ࡫ࡷࡧࡣࡦࡨࡸࡰࡱࡿࠠࡣࡻࠣࡰࡴ࡭ࡧࡪࡰࡪࠎࠥࠦࠠࠡࡶ࡫ࡩࡲࠦࡡ࡯ࡦࠣࡷ࡮ࡳࡰ࡭ࡻࠣࡶࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡵࡪࡵࡳࡼ࡯࡮ࡨࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡸ࠴ࠊࠡࠢࠣࠤࠧࠨࠢễ")
    @staticmethod
    def upload_attachment(bstack1111ll1l11l_opy_: str, *bstack1111ll111l1_opy_) -> None:
        if not bstack1111ll1l11l_opy_ or not bstack1111ll1l11l_opy_.strip():
            logger.error(bstack1l1llll_opy_ (u"ࠥࡥࡩࡪ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡖࡲࡰࡸ࡬ࡨࡪࡪࠠࡧ࡫࡯ࡩࠥࡶࡡࡵࡪࠣ࡭ࡸࠦࡥ࡮ࡲࡷࡽࠥࡵࡲࠡࡐࡲࡲࡪ࠴ࠢỆ"))
            return
        bstack1111l1ll1l1_opy_ = bstack1111ll111l1_opy_[0] if bstack1111ll111l1_opy_ and len(bstack1111ll111l1_opy_) > 0 else None
        bstack1ll11l1l1_opy_ = None
        test_framework_state, test_hook_state = bstack1111l1llll1_opy_()
        try:
            if bstack1111ll1l11l_opy_.startswith(bstack1l1llll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧệ")) or bstack1111ll1l11l_opy_.startswith(bstack1l1llll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢỈ")):
                logger.debug(bstack1l1llll_opy_ (u"ࠨࡐࡢࡶ࡫ࠤ࡮ࡹࠠࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡧࠤࡦࡹࠠࡖࡔࡏ࠿ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠨỉ"))
                url = bstack1111ll1l11l_opy_
                bstack1111l1lll1l_opy_ = str(uuid.uuid4())
                bstack1111ll1111l_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack1111ll1111l_opy_ or not bstack1111ll1111l_opy_.strip():
                    bstack1111ll1111l_opy_ = bstack1111l1lll1l_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1l1llll_opy_ (u"ࠢࡶࡲ࡯ࡳࡦࡪ࡟ࠣỊ") + bstack1111l1lll1l_opy_ + bstack1l1llll_opy_ (u"ࠣࡡࠥị"),
                                                        suffix=bstack1l1llll_opy_ (u"ࠤࡢࠦỌ") + bstack1111ll1111l_opy_)
                _1111ll1l1ll_opy_ = None
                try:
                    import ssl as _ssl
                    from bstack_utils.helper import get_merged_ca_bundle
                    _1111l1ll11l_opy_ = get_merged_ca_bundle()
                    if _1111l1ll11l_opy_:
                        _1111ll1l1ll_opy_ = _ssl.create_default_context(cafile=_1111l1ll11l_opy_)
                except Exception:
                    _1111ll1l1ll_opy_ = None
                with urllib.request.urlopen(url, context=_1111ll1l1ll_opy_) as response, open(temp_file.name, bstack1l1llll_opy_ (u"ࠪࡻࡧ࠭ọ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack1ll11l1l1_opy_ = Path(temp_file.name)
                logger.debug(bstack1l1llll_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡨ࡬ࡰࡪࠦࡴࡰࠢࡷࡩࡲࡶ࡯ࡳࡣࡵࡽࠥࡲ࡯ࡤࡣࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦỎ").format(bstack1ll11l1l1_opy_))
            else:
                bstack1ll11l1l1_opy_ = Path(bstack1111ll1l11l_opy_)
                logger.debug(bstack1l1llll_opy_ (u"ࠧࡖࡡࡵࡪࠣ࡭ࡸࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡦࠣࡥࡸࠦ࡬ࡰࡥࡤࡰࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠢỏ").format(bstack1ll11l1l1_opy_))
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡲࡦࡹࡧࡩ࡯ࠢࡩ࡭ࡱ࡫ࠠࡧࡴࡲࡱࠥࡶࡡࡵࡪ࠲࡙ࡗࡒ࠺ࠡࡽࢀࠦỐ").format(e))
            return
        if bstack1ll11l1l1_opy_ is None or not bstack1ll11l1l1_opy_.exists():
            logger.error(bstack1l1llll_opy_ (u"ࠢࡔࡱࡸࡶࡨ࡫ࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠥố").format(bstack1ll11l1l1_opy_))
            return
        if bstack1ll11l1l1_opy_.stat().st_size > bstack1111ll1l111_opy_:
            logger.error(bstack1l1llll_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡳࡪࡼࡨࠤࡪࡾࡣࡦࡧࡧࡷࠥࡳࡡࡹ࡫ࡰࡹࡲࠦࡡ࡭࡮ࡲࡻࡪࡪࠠࡴ࡫ࡽࡩࠥࡵࡦࠡࡽࢀࠦỒ").format(bstack1111ll1l111_opy_))
            return
        bstack1111l1lllll_opy_ = bstack1l1llll_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧồ")
        if bstack1111l1ll1l1_opy_:
            try:
                params = json.loads(bstack1111l1ll1l1_opy_)
                if bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧỔ") in params and params.get(bstack1l1llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨổ")) is True:
                    bstack1111l1lllll_opy_ = bstack1l1llll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤỖ")
            except Exception as bstack1111l1lll11_opy_:
                logger.error(bstack1l1llll_opy_ (u"ࠨࡊࡔࡑࡑࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡔࡦࡸࡡ࡮ࡵ࠽ࠤࢀࢃࠢỗ").format(bstack1111l1lll11_opy_))
        bstack1111ll11lll_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1l11l111l1l_opy_ import bstack1l1111ll11l_opy_
        if test_framework_state in bstack1l1111ll11l_opy_.hook_events:
            if bstack1111l1lllll_opy_ == bstack111l1l11ll1_opy_:
                bstack1111ll11lll_opy_ = True
            bstack1111l1lllll_opy_ = bstack111l1l111l1_opy_
        try:
            platform_index = os.environ[bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧỘ")]
            target_dir = os.path.join(BROWSERSTACK_ROOT_DIR, UPLOADED_ATTACHMENTS_PREFIX + str(platform_index),
                                      bstack1111l1lllll_opy_)
            if bstack1111ll11lll_opy_:
                target_dir = os.path.join(target_dir, bstack1111ll11ll1_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1l1llll_opy_ (u"ࠣࡅࡵࡩࡦࡺࡥࡥ࠱ࡹࡩࡷ࡯ࡦࡪࡧࡧࠤࡹࡧࡲࡨࡧࡷࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦộ").format(target_dir))
            file_name = os.path.basename(bstack1ll11l1l1_opy_)
            bstack1111ll111ll_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack1111ll111ll_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack1111l1ll1ll_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack1111l1ll1ll_opy_) + extension)):
                    bstack1111l1ll1ll_opy_ += 1
                bstack1111ll111ll_opy_ = os.path.join(target_dir, base_name + str(bstack1111l1ll1ll_opy_) + extension)
            shutil.copy(bstack1ll11l1l1_opy_, bstack1111ll111ll_opy_)
            logger.info(bstack1l1llll_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡣࡰࡲ࡬ࡩࡩࠦࡴࡰ࠼ࠣࡿࢂࠨỚ").format(bstack1111ll111ll_opy_))
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡰࡳࡻ࡯࡮ࡨࠢࡩ࡭ࡱ࡫ࠠࡵࡱࠣࡸࡦࡸࡧࡦࡶࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥớ").format(e))
            return
        finally:
            if bstack1111ll1l11l_opy_.startswith(bstack1l1llll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧỜ")) or bstack1111ll1l11l_opy_.startswith(bstack1l1llll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢờ")):
                try:
                    if bstack1ll11l1l1_opy_ is not None and bstack1ll11l1l1_opy_.exists():
                        bstack1ll11l1l1_opy_.unlink()
                        logger.debug(bstack1l1llll_opy_ (u"ࠨࡔࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡩ࡭ࡱ࡫ࠠࡥࡧ࡯ࡩࡹ࡫ࡤ࠻ࠢࡾࢁࠧỞ").format(bstack1ll11l1l1_opy_))
                except Exception as ex:
                    logger.error(bstack1l1llll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂࠨở").format(ex))
    @staticmethod
    @measure(event_name=EVENTS.bstack1111ll11l11_opy_, stage=STAGE.SINGLE, bstack11lllll111_opy_=None)
    def bstack11ll1111ll_opy_() -> None:
        bstack1l1llll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡊࡥ࡭ࡧࡷࡩࡸࠦࡡ࡭࡮ࠣࡪࡴࡲࡤࡦࡴࡶࠤࡼ࡮࡯ࡴࡧࠣࡲࡦࡳࡥࡴࠢࡶࡸࡦࡸࡴࠡࡹ࡬ࡸ࡭ࠦࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢࠡࡨࡲࡰࡱࡵࡷࡦࡦࠣࡦࡾࠦࡡࠡࡰࡸࡱࡧ࡫ࡲࠡ࡫ࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡦࠢࡸࡷࡪࡸࠧࡴࠢࢁ࠳࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧỠ")
        bstack1111ll11l1l_opy_ = get_writable_dir()
        pattern = re.compile(bstack1l1llll_opy_ (u"ࡴ࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯࡟ࡨ࠰ࠨỡ"))
        if os.path.exists(bstack1111ll11l1l_opy_):
            for item in os.listdir(bstack1111ll11l1l_opy_):
                bstack1111ll1l1l1_opy_ = os.path.join(bstack1111ll11l1l_opy_, item)
                if os.path.isdir(bstack1111ll1l1l1_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack1111ll1l1l1_opy_)
                    except Exception as e:
                        logger.error(bstack1l1llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦỢ").format(e))
        else:
            logger.info(bstack1l1llll_opy_ (u"࡙ࠦ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠤợ").format(bstack1111ll11l1l_opy_))