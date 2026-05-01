# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack111l1l11_opy_(bstack1l1l11111_opy_):
    bstack111ll_opy_ (u"ࠢࠣࠤࡆࡥࡱࡲࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤ࡬ࡘࡐࡄࠢࡷࡳࠥ࡭ࡥࡵࠢࡥࡥࡨࡱࡥ࡯ࡦ࠰ࡶࡪࡹ࡯࡭ࡸࡨࡨࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡘࡥࡵࡷࡵࡲࡸࠦࡤࡪࡥࡷࠤࡴࡸࠠࡏࡱࡱࡩ࠳ࠨࠢࠣᰇ")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import bstack11l1l1l1_opy_
        from browserstack_sdk.sdk_cli.bstack111l11ll_opy_ import bstack11ll1l1ll_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack111111ll1l_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack111ll_opy_ (u"ࠣࡥࡤࡰࡱࡥࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷࡣ࡫ࡸ࡯࡮ࡡࡰࡳࡩࡥࡰࡰࡲࡨࡲ࠿ࠦࡣ࡭࡫ࠣࡲࡴࡺࠠࡳࡧࡤࡨࡾ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠤᰈ"))
            return None
        instance = next(iter(bstack11l1l1l1_opy_.bstack111l11l1l1_opy_.values()), None)
        if not instance:
            logger.debug(bstack111ll_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠ࡯ࡱࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡫ࡵࡵ࡯ࡦࠥᰉ"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack1l1l11111_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack111ll_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᰊ"): True}).encode(bstack111ll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᰋ"))
        req.client_worker_id = bstack111ll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᰌ").format(threading.get_ident(), os.getpid())
        logger.debug(bstack111ll_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡊࡲࡪࡸࡨࡶࡎࡴࡩࡵࠢࡵࡩ࡫ࡃࡻࡾࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿࢂࠨᰍ").format(
            instance.ref(), bstack1l1l11111_opy_))
        response = cli.bstack111111ll1l_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack111ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᰎ")))
            if caps:
                bstack11ll1l1ll_opy_.bstack11ll11l1_opy_(instance, bstack11ll1l1ll_opy_.bstack1ll111ll_opy_, caps)
                logger.debug(bstack111ll_opy_ (u"ࠣࡥࡤࡰࡱࡥࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷࡣ࡫ࡸ࡯࡮ࡡࡰࡳࡩࡥࡰࡰࡲࡨࡲ࠿ࠦࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠣࡷࡺࡩࡣࡦࡧࡧࡩࡩ࠲ࠠࡨࡱࡷࠤࢀࢃࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠤࡰ࡫ࡹࡴࠤᰏ").format(len(caps)))
                return caps
        logger.debug(bstack111ll_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤࡷ࡫ࡴࡶࡴࡱࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࡇࡣ࡯ࡷࡪࠦ࡯ࡳࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᰐ"))
        return None
    except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠥࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡥࡦࡳࡱࡰࡣࡲࡵࡤࡠࡲࡲࡴࡪࡴ࠺ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠧᰑ").format(e))
        return None