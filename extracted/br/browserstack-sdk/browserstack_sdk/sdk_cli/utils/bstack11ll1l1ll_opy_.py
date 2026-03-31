# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack1l1lll1l11_opy_(bstack11111lll1_opy_):
    bstack1ll11_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡨࡔࡓࡇࠥࡺ࡯ࠡࡩࡨࡸࠥࡨࡡࡤ࡭ࡨࡲࡩ࠳ࡲࡦࡵࡲࡰࡻ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡧ࡭ࡨࡺࠠࡰࡴࠣࡒࡴࡴࡥ࠯ࠤࠥࠦᨒ")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import bstack111l1ll111_opy_
        from browserstack_sdk.sdk_cli.bstack1l1ll1l11l_opy_ import bstack1l111lllll_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack1l1ll1ll111_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack1ll11_opy_ (u"ࠦࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࡟ࡧࡴࡲࡱࡤࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡦࡰ࡮ࠦ࡮ࡰࡶࠣࡶࡪࡧࡤࡺ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠧᨓ"))
            return None
        instance = next(iter(bstack111l1ll111_opy_.bstack1l1l111l_opy_.values()), None)
        if not instance:
            logger.debug(bstack1ll11_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡲࡴࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡧࡱࡸࡲࡩࠨᨔ"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack11111lll1_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack1ll11_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᨕ"): True}).encode(bstack1ll11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᨖ"))
        req.client_worker_id = bstack1ll11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᨗ").format(threading.get_ident(), os.getpid())
        logger.debug(bstack1ll11_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠥࡸࡥࡧ࠿ࡾࢁࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡾࠤᨘ").format(
            instance.ref(), bstack11111lll1_opy_))
        response = cli.bstack1l1ll1ll111_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack1ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᨙ")))
            if caps:
                bstack1l111lllll_opy_.bstack1l11lllll_opy_(instance, bstack1l111lllll_opy_.bstack1lll1l1111_opy_, caps)
                logger.debug(bstack1ll11_opy_ (u"ࠦࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࡟ࡧࡴࡲࡱࡤࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡇࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹࠦࡳࡶࡥࡦࡩࡪࡪࡥࡥ࠮ࠣ࡫ࡴࡺࠠࡼࡿࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠠ࡬ࡧࡼࡷࠧᨚ").format(len(caps)))
                return caps
        logger.debug(bstack1ll11_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡳࡧࡷࡹࡷࡴࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡀࡊࡦࡲࡳࡦࠢࡲࡶࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᨛ"))
        return None
    except Exception as e:
        logger.debug(bstack1ll11_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣ᨜").format(e))
        return None