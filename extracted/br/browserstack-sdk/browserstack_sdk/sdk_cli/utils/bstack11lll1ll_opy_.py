# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack11l11l1l1l_opy_(bstack11111lll_opy_):
    bstack1ll1lll_opy_ (u"ࠢࠣࠤࡆࡥࡱࡲࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤ࡬ࡘࡐࡄࠢࡷࡳࠥ࡭ࡥࡵࠢࡥࡥࡨࡱࡥ࡯ࡦ࠰ࡶࡪࡹ࡯࡭ࡸࡨࡨࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡘࡥࡵࡷࡵࡲࡸࠦࡤࡪࡥࡷࠤࡴࡸࠠࡏࡱࡱࡩ࠳ࠨࠢࠣᨁ")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import bstack11ll11l1_opy_
        from browserstack_sdk.sdk_cli.bstack1l1ll1111l_opy_ import bstack111l111ll_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack1l1llll1lll_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡥࡤࡰࡱࡥࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷࡣ࡫ࡸ࡯࡮ࡡࡰࡳࡩࡥࡰࡰࡲࡨࡲ࠿ࠦࡣ࡭࡫ࠣࡲࡴࡺࠠࡳࡧࡤࡨࡾ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠤᨂ"))
            return None
        instance = next(iter(bstack11ll11l1_opy_.bstack1111l1ll1l_opy_.values()), None)
        if not instance:
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠ࡯ࡱࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡫ࡵࡵ࡯ࡦࠥᨃ"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack11111lll_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack1ll1lll_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᨄ"): True}).encode(bstack1ll1lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᨅ"))
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᨆ").format(threading.get_ident(), os.getpid())
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡊࡲࡪࡸࡨࡶࡎࡴࡩࡵࠢࡵࡩ࡫ࡃࡻࡾࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿࢂࠨᨇ").format(
            instance.ref(), bstack11111lll_opy_))
        response = cli.bstack1l1llll1lll_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack1ll1lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᨈ")))
            if caps:
                bstack111l111ll_opy_.bstack1lll1111ll_opy_(instance, bstack111l111ll_opy_.bstack11l11l11_opy_, caps)
                logger.debug(bstack1ll1lll_opy_ (u"ࠣࡥࡤࡰࡱࡥࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷࡣ࡫ࡸ࡯࡮ࡡࡰࡳࡩࡥࡰࡰࡲࡨࡲ࠿ࠦࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠣࡷࡺࡩࡣࡦࡧࡧࡩࡩ࠲ࠠࡨࡱࡷࠤࢀࢃࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠤࡰ࡫ࡹࡴࠤᨉ").format(len(caps)))
                return caps
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤࡷ࡫ࡴࡶࡴࡱࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࡇࡣ࡯ࡷࡪࠦ࡯ࡳࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᨊ"))
        return None
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡥࡦࡳࡱࡰࡣࡲࡵࡤࡠࡲࡲࡴࡪࡴ࠺ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠧᨋ").format(e))
        return None